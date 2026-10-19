import os
import sys

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from openai import OpenAI
import json 
from models.llm_client import LLMClient

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


MODEL = "gpt-4o-mini"
EXTRACT_PROMPT = """You are a data extraction tool. Read the user's paragraph and \
return a single JSON object with exactly these keys:
- "name": the person's name as a string, or null if none is mentioned
- "date": the date in YYYY-MM-DD format as a string, or null if none is mentioned
- "sentiment": exactly one of "positive", "negative", or "neutral"

Respond with the JSON object only. No prose, no explanation, no markdown code fences.

Example of the exact shape:
{"name": "Maria", "date": "2025-03-14", "sentiment": "positive"}"""
EXIT_COMMANDS = ["quit", "exit", "q"]

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Add it to .env or your environment.")
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = [{"role": "system", "content": EXTRACT_PROMPT}]
    
    print("Chatting (type 'quit' to exit)")

    
    # Stream the response
    def stream_response(client, messages):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )
        chunks = []
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                print("DELTA", delta, end="", flush=True)
                chunks.append(delta)
        return "".join(chunks)
    while True:
        user_input = input("You: ")
        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})
        print("bot: ", flush=True)
        reply = stream_response(client, messages)
        messages.append({"role": "assistant", "content": reply})
        print()

def ExtractionError(Exception):
    """Exception raised when the extraction fails."""
    pass
REQUIRED_KEYS = {"name", "date", "sentiment"}
def validate_extraction(raw):
    """
    Parse and validate the models'reply into a trusted extraction dict 
    Args:
        raw: The raw string the model returned
    Returns:
        A dict guaranteed to have keys name, date, and sentiment with a valid sentiment.
    Raises:
        ExtractionError: If the extraction is invalid or missing a required field.
    """
    try:
        extraction = json.loads(raw)
    except json.JSONDecodeError:
        raise ExtractionError("The model's reply was not valid JSON.")
    if not isinstance(extraction, dict):
        raise ExtractionError("The model's reply was not a JSON object.")
    
    missing = REQUIRED_KEYS - extraction.keys()
    if missing:
        raise ExtractionError(f"The model's reply is missing the following keys: {missing}")
    if extraction["sentiment"] not in {"positive", "negative", "neutral"}:
        raise ExtractionError(f"The model's reply has an invalid sentiment: {extraction['sentiment']}")
    return extraction

def extract(client, message, max_retry=3):
    """Extract structured data from a user's message using the model."""
    for attempt in range(max_retry):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": EXTRACT_PROMPT},
                    {"role": "user", "content": message},
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            return validate_extraction(response.choices[0].message.content)
        except ExtractionError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retry - 1:
                raise ExtractionError("All attempts to extract data failed.")
            print(f"Retrying... (attempt {attempt + 1} of {max_retry})")

def main1():
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Add it to .env or your environment.")
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    user_input = input("You: ")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": EXTRACT_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    print(response.choices[0].message.content)
    # print(json.loads(response.choices[0].message.content))
if __name__ == "__main__":
    main1()
from typing import Final, Any
EXTRACT_PROMPT: Final[str] = """You are a data extraction tool. Read the user's \
paragraph and return a single JSON object with exactly these keys:
- "name": the person's name as a string, or null if none is mentioned
- "date": the date in YYYY-MM-DD format as a string, or null if none is mentioned
- "sentiment": exactly one of "positive", "negative", or "neutral"
 
Respond with the JSON object only. No prose, no explanation, no markdown code fences.
 
Example of the exact shape:
{"name": "Maria", "date": "2025-03-14", "sentiment": "positive"}"""

EXIT_COMMANDS: Final[frozenset[str]] = frozenset({"quit", "exit", "q"})
REQUIRED_KEYS: Final[frozenset[str]] = frozenset[str]({"name", "date", "sentiment"})
VALID_SENTIMENTS: Final[frozenset[str]] = frozenset[str]({"positive", "negative", "neutral"})

class ExtractionError(Exception):
    """Exception raised when the extraction fails."""

class SentimentExtractor:
    """Extract {name, date, sentiment} from a paragraph of free text.

    Attributes: 
        client: The injected LLM adapter.
        max_retry: The maximum number of retries for the extraction.
    """
    def __init__(self, client: LLMClient, max_retry: int = 3) -> None:
        self.client = client
        self.max_retry = max_retry
    
    @staticmethod
    def validate(raw: str) -> dict[str, Any]:
        """Parse and validate the model's reply into a trusted dict.

        Args:
            raw: The raw string the model returned
        Returns:
            A dict guaranteed to have keys name, date, and valid sentiment.
        
        Raises:
            ExtractionError: If the reply is not JSON, not an object, missing 
            a required key, or carries an unknown sentiment value.
        """
        try:
            extraction = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ExtractionError(f"The model's reply was not valid JSON.") from exc
        if not isinstance(extraction, dict):
            raise ExtractionError("The model's reply was not a JSON object.")
        
        missing = REQUIRED_KEYS - extraction.keys()
        if missing:
            raise ExtractionError(f"The model's reply is missing required keys: {sorted(missing)}")
        
        if extract["sentiment"] not in VALID_SENTIMENTS:
            raise ExtractionError(f"The model's reply has an invalid sentiment: {extract['sentiment']}")
        return extraction



    def extract(self, message: str) -> dict[str, Any]:
        """Extract structured data from one message, retrying on bad output

        Args:
            message: The user's paragraph of free text.
        
        Returns:
            The validated extraction dict.
        
        Raises:
            ExtractionError: If every attempt produced invalid output.
    """
        last_error: ExtractionError | None = None
        for attempt in range(1, self.max_retry + 1):
            response = self.client.chat(
                messages=[
                    {"role": "system", "content": EXTRACT_PROMPT},
                    {"role": "user", "content": message},
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or ""
            try:
                return self.validate(raw)
            except ExtractionError as exc:
                last_error = exc
                print(f"Attempt {attempt}/{self.max_retry} failed: {exc}")

        raise ExtractionError(
            f"All {self.max_retry} attempts failed. Last error: {last_error}"
        )
    def stream_reply(self, messages: list[dict[str, str]]) -> str:
        """Stream one assistant reply to stdout and return the full text.

        Args:
            messages: The conversation so far, in OpenAI format.

        Returns:
            The complete reply assembled from the streamed chunks.
        """
        chunks: list[str] = []
        for chunk in self.client.chat(messages=messages, stream=True):
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                chunks.append(delta)
        print()
        return "".join(chunks)

    def run_chat(self) -> None:
        """Run the interactive streaming chat loop until the user exits."""
        messages: list[dict[str, str]] = [
            {"role": "system", "content": EXTRACT_PROMPT}
        ]
        print("Chatting (type 'quit' to exit)")
 
        while True:
            user_input = input("You: ")
            if user_input.lower().strip() in EXIT_COMMANDS:
                print("Goodbye!")
                break
            if not user_input.strip():
                continue
 
            messages.append({"role": "user", "content": user_input})
            print("bot: ", end="", flush=True)
            reply = self.stream_reply(messages)
            messages.append({"role": "assistant", "content": reply})
 
    def run_once(self) -> None:
        """Read one paragraph from stdin and print the validated extraction."""
        user_input = input("You: ")
        try:
            print(json.dumps(self.extract(user_input), ensure_ascii=False, indent=2))
        except ExtractionError as exc:
            print(f"Extraction failed: {exc}")
