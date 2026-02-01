"""Resolves in-game player entities to real-world personas."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "personas_and_voices.yaml"

class PlayerResolver:
    def __init__(self) -> None:
        self.config = self._load_config()
        self.players_config = self.config.get("players", {})

    def _load_config(self) -> Dict[str, Any]:
        if not CONFIG_PATH.exists():
            return {}
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def resolve_persona(self, event: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """
        Determines the real-world persona associated with an event.
        Returns a dict with 'name' and 'description' if found, else None.
        """
        # 1. Local Human Player (Nico)
        if event.get("is_local"):
             return self.players_config.get("local_player")
        
        # 2. Other Human Player (Aurore)
        # In Civ6, if is_human is true but it's not the local player, it's the guest (Aurore)
        if event.get("is_human"):
             return self.players_config.get("aurore")
        
        # 3. AI Player
        if event.get("is_human") is False:
             leader = event.get("player_leader") or event.get("leader") or "une IA"
             civ = event.get("player_civ") or event.get("civ") or "une civilisation inconnue"
             return {
                 "name": f"l'IA ({leader} représentant {civ})",
                 "description": "Un adversaire dirigé par l'ordinateur."
             }
        
        return None

    def enrich_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Adds 'persona_name' to the event if resolved."""
        persona = self.resolve_persona(event)
        if persona:
            event["persona_name"] = persona.get("name")
        return event
