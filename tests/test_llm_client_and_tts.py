"""Tests for LLM Client and TTS integration."""

import unittest
from unittest.mock import patch, MagicMock
import json
import os
from src.llm_router.simple_llm_client import LLMCLIClient
from src.audio_runtime_windows.elevenlabs_tts import ElevenLabsTTS


class TestLLMCLIClient(unittest.TestCase):
    @patch("subprocess.run")
    @patch.dict(os.environ, {"SELECTED_MODEL": "claude"})
    def test_generate_json_claude_success(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = 'Some chat... {"tool": "speak", "parameters": {"text": "Hello world"}} ... more chat'
        mock_run.return_value = mock_process

        client = LLMCLIClient(agent_name="test_agent")
        client.model = "claude"
        response = client.generate_json("Test prompt")

        self.assertEqual(response["tool"], "speak")
        self.assertEqual(response["parameters"]["text"], "Hello world")

        args, kwargs = mock_run.call_args
        command = args[0]
        self.assertIn("cd agents/test_agent", command)
        self.assertIn("claude -p", command)
        self.assertTrue(kwargs.get("shell"))

    @patch("subprocess.run")
    @patch.dict(os.environ, {"SELECTED_MODEL": "gemini"})
    def test_generate_json_gemini_success(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = '{"tool": "speak", "parameters": {"text": "Bonjour"}}'
        mock_run.return_value = mock_process

        client = LLMCLIClient(agent_name="test_agent")
        client.model = "gemini"
        response = client.generate_json("Test prompt")

        self.assertEqual(response["tool"], "speak")
        self.assertEqual(response["parameters"]["text"], "Bonjour")

        args, kwargs = mock_run.call_args
        command = args[0]
        self.assertEqual(command[0], "gemini")
        self.assertIn("Test prompt", command)
        self.assertEqual(kwargs.get("cwd"), "agents/test_agent")

    @patch("subprocess.run")
    def test_generate_json_failure(self, mock_run):
        mock_run.side_effect = Exception("CLI failed")

        client = LLMCLIClient()
        response = client.generate_json("Test")

        self.assertEqual(response["mood"], "error")

class TestElevenLabsTTS(unittest.TestCase):
    @patch("requests.post")
    def test_generate_audio_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_post.return_value = mock_response

        # Mock env var if needed, or rely on logic handling missing key gracefully
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "fake_key"}):
            tts = ElevenLabsTTS()
            result = tts.generate_audio("Hello", output_path="test_audio.mp3")
            
            self.assertTrue(result)
            self.assertTrue(os.path.exists("test_audio.mp3"))
            
            # Clean up
            if os.path.exists("test_audio.mp3"):
                os.remove("test_audio.mp3")

    @patch("requests.post")
    def test_generate_audio_api_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "fake_key"}):
            tts = ElevenLabsTTS()
            result = tts.generate_audio("Hello")
            self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
