from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from models.ollama_client import OllamaClient
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

MODEL = "gpt-4o-mini"


from typing import Any, Callable, Final

from interact.base_experiment import BaseExperiment
from models.llm_client import LLMClient
from utils.paths import STATIC_DIR    
LABELS: Final[list[tuple[str, ...]]] = (
    "Billing",
    "Technical",
    "Account/Login",
    "General Question"
)

DEFS: Final[str] = """Billing = charges, refunds, payment issues,
payment methods. 
Technical = crashed, bugs, errors, things not working.
Account/Login = sign-in, passwords, 2FA, locked accounts (even if angry about charges)
General Question = info requests that fit none of the above.
"""
UNKNOWN_LABEL: Final[str] = "UNKNOWN"
PromptBuilder = Callable[[str], str]

class PromptEngineering(BaseExperiment):
    """Scores four prompt strategies against a set same labelled test set."""

    def __init__(self, client: LLMClient) -> None:
        super().__init__(client)
        self.prompts: dict[str, PromptBuilder] = {
            "zeroshot": self.prompt_zeroshot,
            "zeroshot_with_defs": self.prompt_zeroshot_with_defs,
            "fewshot": self.prompt_fewshot,
            "chainofthought": self.prompt_chainofthought,
        }

    # Prompt strategies
    @staticmethod
    def prompt_zeroshot(ticket: str) -> str:
        return (f"Classify into exactly one of {list(LABELS)}. "
                f'Reply with only the label. \nTicket: "{ticket}"')

    # Zero-shot with definitions
    @staticmethod
    def prompt_zeroshot_with_defs(t: str) -> str:
        return f"""{DEFS} \nRule: if billing is mentioned but the real problems is
        access, choose Account/Login. \nClassify into exactly one of {LABELS}.
        Reply with only the label.\nTicket: \"{t}\""""

    # Few-shot classification
    @staticmethod
    def prompt_fewshot(t: str) -> str:
        return f"""{DEFS}
        Examples:
        You billed my car twice -> Billing
        Reset link never arrives -> Account/login
        Please add CSV export -> Feature Request
        Classify into exactly one of {LABELS}. Reply with only the label.
        Ticket: "{t}" """

    # Chain of thought classification
    @staticmethod
    def prompt_chainofthought(t: str) -> str:
        return f"""{DEFS} \nThink in one sentence about the core problem,
        then on the new line output 'Label: <one label>`.\nTicket: \"{t}\""""

    # running and scoring
    def parse_label(self, text: str) -> str:
        """Put a label out of a reply, bare or in 'Label: X' form.
        
        Without this the chain-of-thought prompt would score zero:
        its reply is a sentence of reasoning followed by the label, which
        never equals the gold string on its own.
        Args:
            text: The model's reply to a prompt.
        Returns:
            The matched label, or UNKNOWN if none was found.
        """
        lines = text.strip().splitlines()
        if not lines:
            return UNKNOWN_LABEL
        last = lines[-1].replace("Label:", "").strip().lower()
        for label in LABELS:
            if label.lower() in last:
                return label
        return UNKNOWN_LABEL

    def classify(self, build: PromptBuilder, ticket: str) -> str:
        """Classify one ticket with one prompt strategy."""
        reply = self.send([{"role": "user", "content": build(ticket)}], temperature=0.0)
        return self.parse_label(reply)

    def load_cases(self) -> list[dict[str, Any]]:
        """Load the labelled test set from static/ticket.json"""
        return self.load_json(STATIC_DIR / "tickets.json")

    def run(self) -> None:
        """Score every prompt over the test set and print accuracy + misses."""
        tests = self.load_cases()
 
        for name, build in self.prompts.items():
            correct = 0
            misses: list[tuple[str, str, str]] = []
 
            for case in tests:
                predicted = self.classify(build, case["text"])
                if predicted == case["label"]:
                    correct += 1
                else:
                    misses.append((case["label"], predicted, case["text"]))
 
            accuracy = 100 * correct / len(tests)
            print(f"{name}: {correct}/{len(tests)} correct ({accuracy:.1f}%)")
            if misses:
                print("Misses:")
                for gold, predicted, text in misses:
                    print(f"  {gold} -> {predicted} ({text[:60]})")
            print()

    
        
