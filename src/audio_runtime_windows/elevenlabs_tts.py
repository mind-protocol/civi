"""ElevenLabs TTS helper."""

import os
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Try to load .env from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

logger = logging.getLogger("elevenlabs_tts")

class ElevenLabsTTS:
    def __init__(self) -> None:
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            logger.error("ELEVENLABS_API_KEY not found in environment")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        # Default voice (Narrator-like) - "Roger"
        self.default_voice_id = "CwhRBWXzGAHq8TQ4Fs17"

    def generate_audio(self, text: str, voice_id: str = None, output_path: str = "output.mp3") -> bool:
        """Generate audio file from text using ElevenLabs."""
        if not self.api_key:
            return False
        
        voice_id = voice_id or self.default_voice_id
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                logger.info(f"Audio saved to {output_path}")
                return True
            else:
                logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exception during ElevenLabs TTS: {e}")
            return False
