# AI Engineer Roadmap — Theory + Practice (Free Resources)

*For someone who already has a software background. This skips programming foundations and focuses only on the AI layer: LLMs, APIs, prompting, RAG, agents, evaluation, and deployment. Every phase pairs a documentation/course (theory) with a project (practice) so you learn both at once.*

## How to use this

- Work top to bottom. Each phase builds on the last.
- For every phase: read/watch the theory resource **and** finish the project before moving on. Do not stack courses without building — that's the #1 way people stall.
- Suggested pace: ~1 phase per week if part-time, faster if full-time. The whole path is roughly 6–8 weeks.
- LangChain note: it's a great practical spine (Phases 4–5), but learn the **raw model API first** (Phase 2) so you understand what LangChain abstracts. When something breaks, you'll know why.

---

## Phase 1 — LLM fundamentals

**Goal:** Build a correct mental model of how LLMs work: tokens, context windows, embeddings, temperature, and what "pre-trained" actually means. You don't need to derive transformer math — just enough to reason about behavior and cost.

**Theory (docs/course)**
- Hugging Face **LLM Course** — https://huggingface.co/learn/llm-course (how transformers/tokenization/embeddings work, hands-on with the `transformers` library)
- Optional deeper intuition: Andrej Karpathy's "Intro to Large Language Models" and "Let's build GPT" on YouTube

**Project (practice)**
- Write a small script using a tokenizer (`tiktoken` or Hugging Face `tokenizers`) that shows how a sentence becomes tokens, counts tokens, and estimates API cost.
- Embed 10–20 sentences, compute cosine similarity between them, and confirm that semantically similar sentences score higher. This is the intuition RAG is built on.

---

## Phase 2 — Working with model APIs

**Goal:** Comfortably call an LLM API: messages format, system prompts, streaming, conversation history, structured (JSON) output, temperature, and token/cost management.

**Theory (docs/course)**
- Anthropic **API Fundamentals** course — https://github.com/anthropics/courses (API keys, model params, multimodal prompts, streaming)
- Anthropic API docs — https://docs.claude.com
- OpenAI docs + **OpenAI Cookbook** — https://github.com/openai/openai-cookbook (recipe-style, copy-paste examples)

**Project (practice)**
- Build a command-line chatbot from scratch (no framework) that: keeps conversation history, streams responses token-by-token, uses a system prompt, and lets you switch models.
- Add a mode that returns **structured JSON** (e.g. extract `{name, date, sentiment}` from a paragraph) and validate it in code.

---

## Phase 3 — Prompt engineering

**Goal:** The highest-ROI skill on this roadmap. System prompts, few-shot examples, chain-of-thought, structured output, and how to test prompts instead of guessing.

**Theory (docs/course)**
- Anthropic **Prompt Engineering Interactive Tutorial** — https://github.com/anthropics/prompt-eng-interactive-tutorial (9 chapters, exercises, answer key — the best hands-on one)
- DeepLearning.AI **ChatGPT Prompt Engineering for Developers** (free) — https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers
- Reference: **Prompt Engineering Guide** — https://www.promptingguide.ai

**Project (practice)**
- Pick a real task (classify support tickets, extract structured fields from messy text, or summarize with a fixed format).
- Write 3–4 prompt versions and build a tiny eval set (10–20 examples with expected answers) to measure which prompt wins. This directly feeds Phase 6.

---

## Phase 4 — RAG, embeddings & vector databases

**Goal:** The core architecture behind most real LLM products. Document loading → chunking → embeddings → vector store → retrieval → grounded answer with citations. **This is where LangChain earns its place.**

**Theory (docs/course)**
- LangChain official docs — https://python.langchain.com (start with the RAG tutorial under "Tutorials")
- DeepLearning.AI **Retrieval Augmented Generation (RAG)** — https://www.deeplearning.ai/courses/retrieval-augmented-generation
- DeepLearning.AI **Building and Evaluating Advanced RAG** (chunking, retrieval quality)

**Project (practice)** — *this is your flagship project*
- Build a "chat with your documents" app: load PDFs → chunk them → embed → store in a vector DB (start with Chroma or FAISS locally, then try `pgvector` in Postgres) → retrieve the top chunks → answer questions **with source citations**.
- Deliberately break it: ask a question your docs don't cover and make it say "I don't know" instead of hallucinating. Handling empty retrieval well is what separates a demo from a real system.

---

## Phase 5 — AI agents & tool use

**Goal:** Give the model the ability to call tools and take multi-step actions: function/tool calling, the agent loop, and orchestration with LangGraph.

**Theory (docs/course)**
- Anthropic **Tool Use** course — https://github.com/anthropics/courses
- LangChain Academy **Introduction to LangGraph** (free, official) — https://academy.langchain.com/courses/intro-to-langgraph with runnable notebooks at https://github.com/langchain-ai/langchain-academy
- Hugging Face **AI Agents Course** — https://huggingface.co/learn/agents-course (smolagents, LlamaIndex, LangGraph; certificate available)

**Project (practice)**
- Build an agent that has 2–3 tools: a web search, a calculator, and your RAG retriever from Phase 4. Watch it decide which tool to call.
- Rebuild it with LangGraph so it can loop and branch (e.g. retry a search, then answer). Add a guard so raw user input is never passed unsanitized into a tool.

---

## Phase 6 — Evaluation, observability & deployment

**Goal:** No longer "advanced" — this is table stakes. Measure prompt/agent quality, trace what's happening, and ship it.

**Theory (docs/course)**
- Anthropic **Prompt Evaluations** course — https://github.com/anthropics/courses
- LangSmith docs + LangChain Academy LangSmith courses — https://academy.langchain.com (tracing, cost/latency monitoring, evals on live data)

**Project (practice)**
- Add an eval suite to your RAG/agent app: a dataset of questions with expected answers, scored automatically.
- Add tracing (LangSmith) so you can see each step and its cost.
- Deploy it: wrap it in FastAPI (or Streamlit/Gradio for speed) and host on the **Hugging Face Spaces** free tier.

---

## Phase 7 — Capstone

**Goal:** One portfolio-worthy project that combines everything.

- Build an **agentic RAG assistant** over a domain you personally care about (your notes, a codebase's docs, a hobby dataset).
- It should: retrieve from your documents, use at least one tool, cite sources, have an eval set, emit traces, and be deployed with a clean README explaining the architecture.
- This single project demonstrates every skill above and is what you show employers.

---

## Bonus / optional next steps

- **MCP (Model Context Protocol) Course** — https://huggingface.co/learn/mcp-course (the emerging standard for connecting tools/data to models)
- **Fine-tuning** — only learn this *after* the above, and only when prompting + RAG genuinely can't solve your problem. It's often the wrong first tool.
- **Open-source models locally** — Ollama (https://ollama.com) to run models like Llama or Qwen on your own machine; useful for privacy-sensitive RAG.

## The two-spine summary

If you want the shortest "just tell me what to click" version:
1. **DeepLearning.AI short courses** for structured theory (prompting → LangChain → RAG → agents).
2. **LangChain Academy + LangChain docs** for the hands-on framework spine.
3. **Anthropic's courses repo** for prompting, tool use, and evals done right.
4. **Hugging Face LLM + Agents courses** for deeper theory and open-model practice.

Alternate a course with its matching project from this roadmap. Never just watch — build after every unit.
