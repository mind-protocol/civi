"""Main entry point for Civ6 Living Narrator V1 with Claude & ElevenLabs."""

from __future__ import annotations

import time
import json
import logging
import sys
import argparse
import os
from pathlib import Path
from typing import List, Optional

# Add src and root to path if running directly
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from ingest.civ6_jsonl_tail_reader import read_new_lines, TailState, _split_lines
from ingest.raw_event_parser_and_normalizer import parse_json_line, normalize_event, DEFAULT_SCHEMA
from ingest.event_deduplicator_and_coalescer import EventDeduplicator
from ingest.player_resolver import PlayerResolver
from decision_engine.candidate_builder_for_speakers import Candidate
from decision_engine.candidate_ranker_and_selector_with_explainability import (
    select_candidate,
    SelectionConfig,
)
from decision_engine.narrative_budget_and_cooldown_enforcer import (
    BudgetState,
    record_spoken,
)
# Note: simple_llm_client.py now contains LLMCLIClient (formerly ClaudeCLIClient)
from llm_router.simple_llm_client import LLMCLIClient
from audio_runtime_windows.elevenlabs_tts import ElevenLabsTTS
from runtime_windows.audio_player.audio_queue_player import AudioQueue as AudioQueuePlayer, AudioItem

# Configure Logging
os.makedirs(".ngram", exist_ok=True)
log_format = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(".ngram/error.log")
    ]
)
logger = logging.getLogger("main")

# Constants
EVENTS_FILE = os.getenv("EVENTS_FILE", "events.jsonl")
STATE_FILE = ".tail_state.json"
POLL_INTERVAL = 1.0
AUDIO_OUT_DIR = "audio_output"
MIN_NARRATION_INTERVAL = 120  # 2 minutes minimum between narrations
FORCE_NARRATION_EVENTS = {"GAME_START", "WAR_DECLARED", "CITY_CAPTURED", "WONDER_COMPLETED"}

def load_tail_state() -> TailState:
    """Load tail state from disk if available."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return TailState(
                    offset=data.get("offset", 0),
                    buffer=data.get("buffer", ""),
                    mtime_ns=data.get("mtime_ns", 0)
                )
        except Exception as e:
            logger.warning(f"Failed to load state: {e}. Starting fresh.")
    return TailState()

def save_tail_state(state: TailState) -> None:
    """Save tail state to disk."""
    try:
        data = {
            "offset": state.offset,
            "buffer": state.buffer,
            "mtime_ns": state.mtime_ns
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Failed to save state: {e}")

def build_candidates(event: dict) -> List[Candidate]:
    """Generate candidates based on event type."""
    candidates = []
    e_type = event.get("event_type")
    payload = event.get("payload", {})

    if e_type == "GAME_START":
        candidates.append(Candidate(
            candidate_id="game_start_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"A new game begins as {payload.get('local_civ', 'a civilization')}.",
            importance=3.0,  # High priority - always narrate
            surprise=1.0,
            moment_relevance=1.0
        ))
    elif e_type == "TURN_START":
        candidates.append(Candidate(
            candidate_id=f"turn_{event.get('turn')}_advisor",
            speaker_type="advisor",
            speaker_id="advisor_1",
            text=f"Turn {event.get('turn')} begins.",
            importance=0.6,
            surprise=0.1,
            moment_relevance=0.5
        ))
    elif e_type == "TURN_END":
        candidates.append(Candidate(
            candidate_id=f"turn_{event.get('turn')}_end",
            speaker_type="advisor",
            speaker_id="advisor_1",
            text=f"Turn {event.get('turn')} ends.",
            importance=0.3,
            surprise=0.1,
            moment_relevance=0.3
        ))
    elif e_type == "CITY_BUILT":
        civ = payload.get("player_civ", "Unknown")
        city = payload.get("city", "a city")
        candidates.append(Candidate(
            candidate_id="city_built_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{civ} founds {city}.",
            importance=1.5,
            surprise=0.8,
            moment_relevance=0.9
        ))
    elif e_type == "CITY_CAPTURED":
        new_owner = payload.get("new_owner", "Unknown")
        old_owner = payload.get("old_owner", "Unknown")
        candidates.append(Candidate(
            candidate_id="city_captured_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{new_owner} captures a city from {old_owner}!",
            importance=2.5,
            surprise=1.0,
            moment_relevance=1.0
        ))
    elif e_type == "WONDER_COMPLETED":
        wonder = payload.get("wonder", "a wonder")
        civ = payload.get("player_civ", "Unknown")
        candidates.append(Candidate(
            candidate_id="wonder_completed_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{civ} completes {wonder}.",
            importance=2.0,
            surprise=1.0,
            moment_relevance=1.0
        ))
    elif e_type == "WAR_DECLARED":
        attacker = payload.get("attacker", "Unknown")
        defender = payload.get("defender", "Unknown")
        candidates.append(Candidate(
            candidate_id="war_declared_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{attacker} declares war on {defender}!",
            importance=2.5,
            surprise=1.0,
            moment_relevance=1.0
        ))
    elif e_type == "PEACE_MADE":
        p1 = payload.get("player1", "Unknown")
        p2 = payload.get("player2", "Unknown")
        candidates.append(Candidate(
            candidate_id="peace_made_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{p1} and {p2} make peace.",
            importance=1.8,
            surprise=0.7,
            moment_relevance=0.8
        ))
    elif e_type == "TECH_COMPLETED":
        tech = payload.get("tech", "a technology")
        civ = payload.get("player_civ", "Unknown")
        candidates.append(Candidate(
            candidate_id="tech_completed_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{civ} discovers {tech}.",
            importance=1.2,
            surprise=0.5,
            moment_relevance=0.7
        ))
    elif e_type == "CIVIC_COMPLETED":
        civic = payload.get("civic", "a civic")
        civ = payload.get("player_civ", "Unknown")
        candidates.append(Candidate(
            candidate_id="civic_completed_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{civ} adopts {civic}.",
            importance=1.0,
            surprise=0.4,
            moment_relevance=0.6
        ))
    elif e_type == "UNIT_KILLED":
        killed_civ = payload.get("killed_civ", "Unknown")
        killer_civ = payload.get("killer_civ", "Unknown")
        candidates.append(Candidate(
            candidate_id="unit_killed_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"{killer_civ} destroys a unit from {killed_civ}!",
            importance=1.3,
            surprise=0.6,
            moment_relevance=0.7
        ))

    return candidates

def main():
    parser = argparse.ArgumentParser(description="Civ6 Living Narrator V1")
    parser.add_argument("--once", action="store_true", help="Run one pass of log reading and exit.")
    args = parser.parse_args()

    logger.info("Starting Civ6 Living Narrator V1 (LLM + ElevenLabs)...")

    # Ensure audio out dir exists
    os.makedirs(AUDIO_OUT_DIR, exist_ok=True)

    # 1. Initialize Components
    tail_state = load_tail_state()
    deduplicator = EventDeduplicator()
    player_resolver = PlayerResolver()
    
    budget_state = BudgetState()
    selection_config = SelectionConfig(
        max_speech_budget=2,
        budget_window=5,
        cooldown_turns=1,
        min_delta_value=0.5
    )
    
    llm_client = LLMCLIClient(agent_name="narrator")
    tts_engine = ElevenLabsTTS()
    audio_queue = AudioQueuePlayer()

    # Track narration timing and event history
    last_narration_time = 0.0
    recent_events: List[dict] = []  # Keep last 20 events for context
    MAX_RECENT_EVENTS = 20

    logger.info(f"Monitoring {EVENTS_FILE}...")
    if not os.path.exists(EVENTS_FILE):
        logger.warning(f"File {EVENTS_FILE} does not exist yet. Waiting for it to be created...")
    
    try:
        while True:
            # 2. Ingest
            lines, tail_state = read_new_lines(EVENTS_FILE, tail_state)
            save_tail_state(tail_state)

            for line in lines:
                try:
                    # 3. Parse & Normalize
                    raw_event = parse_json_line(line)
                    event = normalize_event(raw_event)
                    if event is None:
                        logger.warning(f"Could not normalize event: {raw_event}")
                        continue
                    
                    if deduplicator.is_duplicate(event):
                        continue
                    deduplicator.remember(event)
                        
                    # Enrich with Persona (Nico, Aurore, etc.)
                    event = player_resolver.enrich_event(event)

                    logger.info(f"Processing Event: {event.get('event_type')}")

                    # Track recent events for context
                    recent_events.append(event)
                    if len(recent_events) > MAX_RECENT_EVENTS:
                        recent_events.pop(0)

                    # 4. Build Candidates
                    candidates = build_candidates(event)
                    if not candidates:
                        continue

                    # Check if we should force narration
                    current_time = time.time()
                    time_since_last = current_time - last_narration_time
                    is_important_event = event.get("event_type") in FORCE_NARRATION_EVENTS
                    should_force = is_important_event or (time_since_last >= MIN_NARRATION_INTERVAL and last_narration_time > 0)

                    # 5. Select
                    result = select_candidate(
                        candidates=candidates,
                        state=budget_state,
                        turn=event.get("turn", 0),
                        config=selection_config
                    )

                    # Force narration for important events or after timeout
                    if result.selected or should_force:
                        candidate = result.selected if result.selected else candidates[0]
                        force_reason = ""
                        if not result.selected and should_force:
                            force_reason = " (forced: " + ("important event" if is_important_event else f"{time_since_last:.0f}s since last") + ")"
                        logger.info(f"Selected Candidate: {candidate.candidate_id}{force_reason}")

                        # 6. Generate (LLM CLI)
                        # Build rich context for the LLM
                        recent_summary = []
                        for evt in recent_events[-10:]:  # Last 10 events
                            evt_type = evt.get("event_type", "?")
                            payload = evt.get("payload", {})
                            if evt_type == "CITY_BUILT":
                                recent_summary.append(f"- {payload.get('player_civ')} fonde {payload.get('city')}")
                            elif evt_type == "WAR_DECLARED":
                                recent_summary.append(f"- {payload.get('attacker')} déclare la guerre à {payload.get('defender')}")
                            elif evt_type == "TECH_COMPLETED":
                                recent_summary.append(f"- {payload.get('player_civ')} découvre {payload.get('tech')}")
                            elif evt_type == "CIVIC_COMPLETED":
                                recent_summary.append(f"- {payload.get('player_civ')} adopte {payload.get('civic')}")
                            elif evt_type == "UNIT_KILLED":
                                recent_summary.append(f"- {payload.get('killer_civ')} détruit une unité de {payload.get('killed_civ')}")
                            elif evt_type == "WONDER_COMPLETED":
                                recent_summary.append(f"- {payload.get('player_civ')} construit {payload.get('wonder')}")
                            elif evt_type == "CITY_CAPTURED":
                                recent_summary.append(f"- {payload.get('new_owner')} capture une ville de {payload.get('old_owner')}")
                            elif evt_type == "PEACE_MADE":
                                recent_summary.append(f"- Paix entre {payload.get('player1')} et {payload.get('player2')}")
                            elif evt_type == "TURN_START":
                                recent_summary.append(f"- Tour {evt.get('turn')} commence")

                        context_str = "\n".join(recent_summary) if recent_summary else "Début de partie"

                        persona_ctx = ""
                        if event.get("persona_name"):
                            persona_ctx = f"Le joueur humain est {event.get('persona_name')}. "

                        prompt = f"""Tu es un narrateur épique pour Civilization VI. Voici le contexte récent:
{context_str}

Événement actuel: {json.dumps(event.get('payload', event), ensure_ascii=False)}
{persona_ctx}
Génère une narration COURTE (1-2 phrases max) en français, dramatique et immersive.
Réponds en JSON: {{"text": "ta narration", "voice": "narrator", "mood": "epic/dramatic/calm/tense"}}"""

                        response = llm_client.generate_json(prompt)
                        
                        text_to_speak = response.get("text", "The world turns.")
                        logger.info(f"LLM: {text_to_speak}")
                        
                        # 7. TTS (ElevenLabs)
                        audio_filename = f"audio_{int(time.time())}.mp3"
                        audio_path = os.path.join(AUDIO_OUT_DIR, audio_filename)
                        
                        if tts_engine.generate_audio(text_to_speak, output_path=audio_path):
                            logger.info(f"Audio generated: {audio_path}")
                            item = AudioItem(path=audio_path, voice=response.get("voice"))
                            audio_queue.enqueue(item)
                            last_narration_time = current_time  # Update for time-based trigger

                        # 8. Update Budget
                        record_spoken(event.get("turn", 0), budget_state, candidate.speaker_type)
                        
                    else:
                        logger.debug(f"Narration suppressed: {result.suppression_reasons}")

                except Exception as e:
                    logger.error(f"Error processing line: {e}")

            if args.once:
                break
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Stopping...")
        sys.exit(0)

if __name__ == "__main__":
    main()
