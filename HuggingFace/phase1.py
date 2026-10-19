import os
from getpass import getpass

from huggingface_hub import login
from transformers import AutoTokenizer

text = "I'm learning transformers!"

# Try to use a token from the environment first.
# If it is not set, the script will ask you to enter it securely.
token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
if not token:
    token = getpass("Enter your Hugging Face access token: ")

if token:
    login(token=token, add_to_git_credential=False)
    os.environ["HF_TOKEN"] = token

for model in [
    "bert-base-uncased",
    "gpt2",
]:
    tokenizer = AutoTokenizer.from_pretrained(model, token=token)
    token_count = tokenizer(text, return_length=True)["length"]
    # ids = tokenizer(text)["input_ids"]
    # print(model, len(ids), tokenizer.convert_ids_to_tokens(ids))
    print(token_count, "tokens in", model)
def estimate_cost(text, tokenizer, price_per_million=3.0):
    length = tokenizer(text, return_length=True)["length"]
    return length, length / 1_000_000 * price_per_million

# Example usage:
# length, cost = estimate_cost(text, tokenizer, price_per_million=3.0)
# print(f"Estimated cost for {length} tokens: ${cost:.2f}")