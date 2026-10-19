# AI Engineer Roadmap

My notes and practice code for learning AI engineering. The plan follows the
[roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer) path, using free resources.

## What's in this repo

| Path | What it is |
| --- | --- |
| `ai-engineer-roadmap.md` | First version of the roadmap, in 7 phases. |
| `ai-engineer-roadmap1.md` | Longer version of the phases, mapped to roadmap.sh. |
| `ai-engineer-roadmap2.md`, `ai-engineer-roadmap3.md` | Roadmap in 12 steps, in the same order as roadmap.sh. |
| `Step4-doc.md` | Step 4 in depth: calling a model from code. |
| `HuggingFace/phase1.py` | Loads tokenizers from Hugging Face and compares them. |
| `Project-practices/` | Small experiments with OpenAI and Ollama models (see below). |
| `run_redteam.py` | Prompt-injection test: runs attacks against a bot with no guards and a bot with guards. |

## Project-practices

A small app that runs one experiment at a time against a model.

| Experiment | What it does |
| --- | --- |
| `prompts` | Tries prompt engineering techniques. |
| `redteam` | Runs prompt-injection attacks from `static/attacks.json`. |
| `sentiment` | Chat that pulls name, date and sentiment out of free text as JSON. |

### Setup

```bash
cd Project-practices
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Create a `.env` file in `Project-practices/`:

```
OPENAI_API_KEY=sk-...
```

### Run

```bash
python main.py prompts --provider openai
python main.py prompts --provider ollama --model llama3.2:3b
python main.py redteam
python main.py sentiment
```

To use `--provider ollama`, install [Ollama](https://ollama.com) and pull the model first:

```bash
ollama pull llama3.2:3b
```

## HuggingFace

```bash
pip install transformers huggingface_hub
```

Set `HF_TOKEN` as an environment variable. If it is not set,
the script asks you for the token.

```bash
python HuggingFace/phase1.py
```

## Secrets

`.env` files are in `.gitignore`. Never put an API key or token in the code.
