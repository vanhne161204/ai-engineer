"""Single entry point. The only file that knows about concrete classes.
 
    python main.py prompts --provider openai
    python main.py prompts --provider ollama --model llama3.2:3b
    python main.py redteam
    python main.py sentiment
"""
 
from __future__ import annotations
 
import argparse
import os
import sys
 
from dotenv import load_dotenv
 
from interact.prompt_engineer_specification import PromptEngineering
from interact.ai_safety_and_ethics import SafetyRedTeam
from interact.chat_sentiment import SentimentExtractor
from models.model_repo import get_client
from utils.paths import ENV_FILE
 
EXPERIMENTS = {
    "prompts": PromptEngineering,
    "redteam": SafetyRedTeam,
    "sentiment": SentimentExtractor,
}
 
 
def parse_args() -> argparse.Namespace:
    """Parse the command line."""
    parser = argparse.ArgumentParser(description="Run one experiment.")
    parser.add_argument("experiment", choices=sorted(EXPERIMENTS))
    parser.add_argument("--provider", default="openai", help="openai or ollama")
    parser.add_argument("--model", default=None, help="override the model name")
    return parser.parse_args()
 
 
def main() -> int:
    """Wire a client to an experiment and run it."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv(ENV_FILE)

    args = parse_args()
    if args.provider == "openai" and not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Add it to .env.")
 
    client = get_client(args.provider, args.model)
    experiment = EXPERIMENTS[args.experiment](client)
 
    if isinstance(experiment, SentimentExtractor):
        experiment.run_chat()
    else:
        experiment.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())