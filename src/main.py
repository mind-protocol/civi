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
from ingest.raw_event_parser_and_normalizer import parse_json_line, DEFAULT_SCHEMA
from ingest.event_deduplicator_and_coalescer import EventDeduplicator
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
EVENTS_FILE = "events.jsonl"
STATE_FILE = ".tail_state.json"
POLL_INTERVAL = 1.0
AUDIO_OUT_DIR = "audio_output"

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

def build_mock_candidates(event: dict) -> List[Candidate]:
    """Generate mock candidates based on event type."""
    candidates = []
    e_type = event.get("event_type")
    
    if e_type == "TURN_START":
        candidates.append(Candidate(
            candidate_id=f"turn_{event.get('turn')}_advisor",
            speaker_type="advisor",
            speaker_id="advisor_1",
            text=f"Turn {event.get('turn')} begins.",
            importance=0.8,
            surprise=0.1,
            moment_relevance=0.5
        ))
    elif e_type == "CITY_BUILT":
        candidates.append(Candidate(
            candidate_id="city_built_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text="A new city rises.",
            importance=1.5,
            surprise=0.8,
            moment_relevance=0.9
        ))
    elif e_type == "WONDER_COMPLETED":
        candidates.append(Candidate(
            candidate_id="wonder_completed_narrator",
            speaker_type="narrator",
            speaker_id=None,
            text=f"The {event.get('wonder')} has been completed.",
            importance=2.0,
            surprise=1.0,
            moment_relevance=1.0
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
    
    logger.info(f"Monitoring {EVENTS_FILE}...")
    
    try:
        while True:
            # 2. Ingest
            lines, tail_state = read_new_lines(EVENTS_FILE, tail_state)
            save_tail_state(tail_state)

            for line in lines:
                try:
                    # 3. Parse & Normalize
                    raw_event = parse_json_line(line)
                    event = raw_event
                    
                    if deduplicator.is_duplicate(event):
                        continue
                    deduplicator.remember(event)
                        
                    logger.info(f"Processing Event: {event.get('event_type')}")
                    
                    # 4. Build Candidates
                    candidates = build_mock_candidates(event)
                    if not candidates:
                        continue
                        
                    # 5. Select
                    result = select_candidate(
                        candidates=candidates,
                        state=budget_state,
                        turn=event.get("turn", 0),
                        config=selection_config
                    )
                    
                    if result.selected:
                        candidate = result.selected
                        logger.info(f"Selected Candidate: {candidate.candidate_id}")
                        
                        # 6. Generate (LLM CLI)
                        prompt = f"The following event occurred in Civilization VI: {json.dumps(event)}. As a narrator/advisor, respond in French (TOUJOURS EN FRANÇAIS) in a single sentence as a JSON object with 'text', 'voice', and 'mood' keys."
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
