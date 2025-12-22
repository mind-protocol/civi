"""LLM client using Claude or Gemini CLI."""

from __future__ import annotations

import json
import subprocess
import os
import logging
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("llm_client")

class LLMCLIClient:
    def __init__(self, agent_name: str = "narrator") -> None:
        self.agent_path = f"agents/{agent_name}"
        self.model = os.getenv("SELECTED_MODEL", "claude")

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Call LLM CLI to generate a response."""
        if "gemini" in self.model.lower():
            return self._call_gemini(prompt, use_continue=True)
        return self._call_claude(prompt, use_continue=True)

    def _call_gemini(self, prompt: str, use_continue: bool) -> Dict[str, Any]:
        """Call Gemini CLI, retry without --continue on failure."""
        continue_flag = "--continue" if use_continue else ""
        # Assuming Gemini CLI accepts -y for yes/confirm and -p for prompt
        full_command = f'cd {self.agent_path} && gemini -p "{prompt}" {continue_flag} -y'

        logger.info(f"Calling Gemini CLI for agent in {self.agent_path} (model={self.model}, continue={use_continue})")

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout.strip()
            
            # Try to find JSON in the output
            start = output.find("{")
            end = output.rfind("}") + 1
            if start != -1 and end != -1:
                json_str = output[start:end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass

            logger.error(f"Could not find valid JSON in Gemini output: {output}")
            
            # Retry logic
            if use_continue:
                logger.info("Retrying without --continue...")
                return self._call_gemini(prompt, use_continue=False)
            
            return {
                "text": "Le brouillard de guerre obscurcit le chemin.",
                "voice": "narrator",
                "mood": "neutral"
            }

        except subprocess.CalledProcessError as e:
            logger.error(f"Gemini CLI failed: {e.stderr}")
            if use_continue:
                logger.info("Retrying without --continue...")
                return self._call_gemini(prompt, use_continue=False)
            return {
                "text": "Le silence tombe sur le royaume.",
                "voice": "narrator",
                "mood": "error"
            }
        except Exception as e:
            logger.error(f"Unexpected error calling Gemini: {e}")
            if use_continue:
                logger.info("Retrying without --continue...")
                return self._call_gemini(prompt, use_continue=False)
            return {
                "text": "Une erreur ancienne s'est produite.",
                "voice": "narrator",
                "mood": "error"
            }

    def _call_claude(self, prompt: str, use_continue: bool) -> Dict[str, Any]:
        """Call Claude CLI, retry without --continue on failure."""
        continue_flag = "--continue" if use_continue else ""
        full_command = f'cd {self.agent_path} && claude -p "{prompt}" {continue_flag} --dangerously-skip-permissions'

        logger.info(f"Calling Claude CLI for agent in {self.agent_path} (continue={use_continue})")

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout.strip()

            # Try to find JSON in the output (Claude might output some conversational text)
            start = output.find("{")
            end = output.rfind("}") + 1
            if start != -1 and end != -1:
                json_str = output[start:end]
                return json.loads(json_str)

            logger.error(f"Could not find JSON in Claude output: {output}")
            # If --continue failed to produce JSON, retry without it
            if use_continue:
                logger.info("Retrying without --continue...")
                return self._call_claude(prompt, use_continue=False)
            return {
                "text": "Le brouillard de guerre obscurcit le chemin.",
                "voice": "narrator",
                "mood": "neutral"
            }

        except subprocess.CalledProcessError as e:
            logger.error(f"Claude CLI failed: {e.stderr}")
            # Retry without --continue on error
            if use_continue:
                logger.info("Retrying without --continue...")
                return self._call_claude(prompt, use_continue=False)
            return {
                "text": "Le silence tombe sur le royaume.",
                "voice": "narrator",
                "mood": "error"
            }
        except Exception as e:
            logger.error(f"Unexpected error calling Claude: {e}")
            if use_continue:
                logger.info("Retrying without --continue...")
                return self._call_claude(prompt, use_continue=False)
            return {
                "text": "Une erreur ancienne s'est produite.",
                "voice": "narrator",
                "mood": "error"
            }

# Alias for backward compatibility if needed, though we will update main.py
ClaudeCLIClient = LLMCLIClient