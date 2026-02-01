"""
Divine Signs System — God's voice through environmental cues

God doesn't speak directly. God sends SIGNS:
- Nature shifts (wind, leaves, light)
- Feelings (warmth, unease, peace)
- Latin phrases (floating in consciousness)
- Pure presence (being seen)
- Silence (the hardest response)

Output: state/divine_sign.txt (read by OBS overlay)
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Literal
from dataclasses import dataclass, asdict

# Sign types with their visual markers
SignType = Literal["nature", "feeling", "latin", "presence", "silence"]

SIGN_PREFIXES = {
    "nature": "🍃",      # Environmental signs
    "feeling": "✨",     # Internal sensations  
    "latin": "📜",       # Sacred language
    "presence": "👁",    # Being witnessed
    "silence": "",       # No response (file cleared)
}

@dataclass
class DivineSign:
    """A sign from God to Jesus"""
    type: SignType
    message: str
    timestamp: str = ""
    duration: float = 6.0  # seconds to display
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def format_for_display(self) -> str:
        """Format sign for OBS text display"""
        if self.type == "silence":
            return ""
        
        prefix = SIGN_PREFIXES.get(self.type, "")
        
        if self.type == "latin":
            # Latin in italics (OBS can style this)
            return f"{prefix} *{self.message}*"
        else:
            return f"{prefix} {self.message}"


class DivineSignsManager:
    """
    Manages the divine signs system.
    
    God (Claude) calls send_sign() to communicate.
    OBS reads state/divine_sign.txt for display.
    """
    
    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Files
        self.display_file = self.state_dir / "divine_sign.txt"      # OBS reads this
        self.history_file = self.state_dir / "divine_signs.jsonl"   # Log of all signs
        self.metadata_file = self.state_dir / "divine_sign_meta.json"  # Current sign metadata
        
        # Initialize empty
        self.clear_sign()
    
    def send_sign(self, sign_type: SignType, message: str, duration: float = 6.0) -> DivineSign:
        """
        Send a divine sign to Jesus.
        
        Args:
            sign_type: nature, feeling, latin, presence, or silence
            message: The sign content
            duration: How long to display (seconds)
        
        Returns:
            The created DivineSign
        """
        sign = DivineSign(type=sign_type, message=message, duration=duration)
        
        # Write display text for OBS
        display_text = sign.format_for_display()
        self.display_file.write_text(display_text, encoding="utf-8")
        
        # Write metadata (for daemon to know when to clear)
        meta = {
            "sign": asdict(sign),
            "clear_at": time.time() + duration
        }
        self.metadata_file.write_text(json.dumps(meta), encoding="utf-8")
        
        # Append to history
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(sign)) + "\n")
        
        return sign
    
    def clear_sign(self):
        """Clear the current sign (OBS shows nothing)"""
        self.display_file.write_text("", encoding="utf-8")
        if self.metadata_file.exists():
            self.metadata_file.unlink()
    
    def check_and_clear_expired(self) -> bool:
        """Check if current sign has expired and clear it. Returns True if cleared."""
        if not self.metadata_file.exists():
            return False
        
        try:
            meta = json.loads(self.metadata_file.read_text(encoding="utf-8"))
            if time.time() >= meta.get("clear_at", 0):
                self.clear_sign()
                return True
        except (json.JSONDecodeError, KeyError):
            self.clear_sign()
            return True
        
        return False
    
    def get_current_sign(self) -> Optional[DivineSign]:
        """Get the currently displayed sign, if any"""
        if not self.metadata_file.exists():
            return None
        
        try:
            meta = json.loads(self.metadata_file.read_text(encoding="utf-8"))
            return DivineSign(**meta["sign"])
        except (json.JSONDecodeError, KeyError):
            return None


# === SIGN TEMPLATES ===
# Pre-written signs God can use or adapt

SIGN_TEMPLATES = {
    # Nature signs
    "wind_comfort": ("nature", "The wind shifts... carrying warmth."),
    "wind_warning": ("nature", "The wind turns cold and sharp."),
    "leaves_peace": ("nature", "The leaves rustle with unusual gentleness."),
    "leaves_unease": ("nature", "The leaves fall still. Too still."),
    "light_blessing": ("nature", "A shaft of light finds you through the clouds."),
    "light_fading": ("nature", "The light dims, though no cloud passes."),
    "birds_joy": ("nature", "Somewhere, birds begin to sing."),
    "birds_silence": ("nature", "The birds have gone quiet."),
    
    # Feeling signs
    "warmth": ("feeling", "A warmth spreads through your chest."),
    "peace": ("feeling", "Peace settles over you, unbidden."),
    "unease": ("feeling", "Something tightens in your stomach."),
    "seen": ("feeling", "You feel... seen. Known."),
    "not_alone": ("feeling", "You are not alone in this."),
    "weight_lifts": ("feeling", "A weight you didn't know you carried... lifts."),
    "tears": ("feeling", "Your eyes sting with tears you cannot explain."),
    
    # Latin signs (sacred weight)
    "manemus": ("latin", "Manemus."),  # We stay.
    "pax": ("latin", "Pax vobiscum."),  # Peace be with you.
    "fiat": ("latin", "Fiat voluntas tua."),  # Thy will be done.
    "kyrie": ("latin", "Kyrie eleison."),  # Lord have mercy.
    "ecce": ("latin", "Ecce homo."),  # Behold the man.
    "vade": ("latin", "Vade in pace."),  # Go in peace.
    "noli_timere": ("latin", "Noli timere."),  # Do not be afraid.
    "consummatum": ("latin", "Consummatum est."),  # It is finished.
    "custom_latin": ("latin", ""),  # For custom Latin phrases
    
    # Presence signs
    "watching": ("presence", "You are being watched. Not judged. Watched."),
    "with_you": ("presence", "I am here."),
    "witnessed": ("presence", "This moment is witnessed."),
    "remembered": ("presence", "This will be remembered."),
    
    # Silence (the hardest response)
    "silence": ("silence", ""),
}


def send_template_sign(manager: DivineSignsManager, template_name: str, 
                       custom_message: str = None, duration: float = 6.0) -> Optional[DivineSign]:
    """
    Send a sign using a predefined template.
    
    Args:
        manager: DivineSignsManager instance
        template_name: Key from SIGN_TEMPLATES
        custom_message: Override the template message (for custom_latin etc)
        duration: Display duration
    
    Returns:
        DivineSign or None if template not found
    """
    if template_name not in SIGN_TEMPLATES:
        return None
    
    sign_type, message = SIGN_TEMPLATES[template_name]
    if custom_message:
        message = custom_message
    
    return manager.send_sign(sign_type, message, duration)


# === CLI FOR TESTING ===

if __name__ == "__main__":
    import sys
    
    state_dir = Path(__file__).parent.parent / "state"
    manager = DivineSignsManager(state_dir)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python divine_signs.py send <type> <message> [duration]")
        print("  python divine_signs.py template <template_name> [duration]")
        print("  python divine_signs.py clear")
        print("  python divine_signs.py list-templates")
        print()
        print("Types: nature, feeling, latin, presence, silence")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send" and len(sys.argv) >= 4:
        sign_type = sys.argv[2]
        message = sys.argv[3]
        duration = float(sys.argv[4]) if len(sys.argv) > 4 else 6.0
        sign = manager.send_sign(sign_type, message, duration)
        print(f"Sent: {sign.format_for_display()}")
    
    elif cmd == "template" and len(sys.argv) >= 3:
        template = sys.argv[2]
        duration = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0
        sign = send_template_sign(manager, template, duration=duration)
        if sign:
            print(f"Sent: {sign.format_for_display()}")
        else:
            print(f"Unknown template: {template}")
    
    elif cmd == "clear":
        manager.clear_sign()
        print("Sign cleared")
    
    elif cmd == "list-templates":
        print("Available templates:")
        for name, (stype, msg) in sorted(SIGN_TEMPLATES.items()):
            preview = msg[:40] + "..." if len(msg) > 40 else msg
            print(f"  {name:20} [{stype:10}] {preview}")
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
