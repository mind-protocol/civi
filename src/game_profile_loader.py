#!/usr/bin/env python3
"""
Game Profile Loader for Living Narrator.
Loads game-specific configuration and adapts narrator behavior.
"""

import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class GameProfile:
    """Loaded game profile with all settings."""
    game_id: str
    game_name: str
    persona_file: str
    narrator_role: str

    # Input configuration
    uses_lua_log: bool
    uses_visual: bool
    visual_primary: bool  # True if screenshots are main input (no events)
    uses_voice: bool
    screenshot_interval: int

    # Urgency
    urgent_events: list[str] = field(default_factory=list)

    # Concepts (for narrator context)
    concepts: dict = field(default_factory=dict)

    # State files
    state_files: list[str] = field(default_factory=list)

    # Visual hints (CK3-specific)
    visual_hints: dict = field(default_factory=dict)

    # Player template
    player_fields: list[str] = field(default_factory=list)


def load_game_profile(game_id: str, config_dir: Optional[Path] = None) -> GameProfile:
    """Load a game profile by ID (e.g., 'civ6', 'ck3')."""
    if config_dir is None:
        config_dir = Path(__file__).parent.parent / "config" / "games"

    profile_path = config_dir / f"{game_id}.yaml"

    if not profile_path.exists():
        raise FileNotFoundError(f"Game profile not found: {profile_path}")

    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    game = data.get("game", {})
    narrator = data.get("narrator", {})
    input_cfg = data.get("input", {})
    concepts = data.get("concepts", {})
    visual_hints = data.get("visual_hints", {})
    player_template = data.get("player_template", {})

    return GameProfile(
        game_id=game.get("id", game_id),
        game_name=game.get("name", game_id.upper()),
        persona_file=narrator.get("persona_file", "CLAUDE.md"),
        narrator_role=narrator.get("role", "Narrator"),
        uses_lua_log=input_cfg.get("lua_log", False),
        uses_visual=input_cfg.get("visual", True),
        visual_primary=input_cfg.get("visual_primary", False),
        uses_voice=input_cfg.get("voice", True),
        screenshot_interval=input_cfg.get("screenshot_interval", 60),
        urgent_events=data.get("urgent_events", []),
        concepts=concepts,
        state_files=data.get("state_files", []),
        visual_hints=visual_hints,
        player_fields=player_template.get("fields", ["name"]),
    )


def get_persona_path(profile: GameProfile, narrator_dir: Optional[Path] = None, playthrough: Optional[str] = None) -> Path:
    """Get the full path to the narrator persona file.

    If a playthrough is specified, look for playthroughs/{playthrough}/CLAUDE.md first.
    """
    base_dir = Path(__file__).parent.parent

    # Check for playthrough-specific persona first
    if playthrough:
        playthrough_persona = base_dir / "playthroughs" / playthrough / "CLAUDE.md"
        if playthrough_persona.exists():
            return playthrough_persona

    # Default to game profile persona
    if narrator_dir is None:
        narrator_dir = base_dir / "narrator"

    return narrator_dir / profile.persona_file


def detect_game_from_config(config: dict) -> str:
    """Detect game from session config, defaulting to civ6."""
    return config.get("game", "civ6")


def list_available_games(config_dir: Optional[Path] = None) -> list[str]:
    """List all available game profiles."""
    if config_dir is None:
        config_dir = Path(__file__).parent.parent / "config" / "games"

    if not config_dir.exists():
        return []

    return [p.stem for p in config_dir.glob("*.yaml")]


if __name__ == "__main__":
    # Test the loader
    import json

    print("Available games:", list_available_games())

    for game_id in ["civ6", "ck3"]:
        try:
            profile = load_game_profile(game_id)
            print(f"\n=== {profile.game_name} ===")
            print(f"  Persona: {profile.persona_file}")
            print(f"  Role: {profile.narrator_role}")
            print(f"  Uses Lua log: {profile.uses_lua_log}")
            print(f"  Visual primary: {profile.visual_primary}")
            print(f"  Screenshot interval: {profile.screenshot_interval}s")
            print(f"  Urgent events: {len(profile.urgent_events)}")
            print(f"  Concepts: {list(profile.concepts.keys())}")
        except FileNotFoundError as e:
            print(f"  {e}")
