# AI Engineer Roadmap — Theory + Practice (Free Resources)

*For someone who already has a software background. This skips programming foundations and focuses only on the AI layer: LLMs, APIs, prompting, RAG, agents, evaluation, and deployment. Every phase pairs a documentation/course (theory) with a project (practice) so you learn both at once.*

*This version is aligned with the [roadmap.sh AI Engineer roadmap](https://roadmap.sh/ai-engineer), which is deliberately **application-first**: an AI Engineer **uses pre-trained models** to build products — they do **not** build models from scratch or derive transformer math. If a resource ever feels like ML-researcher depth (training models, tokenizer internals, GPU math), you've drifted off this path. Come back to "use the model, ship the product."*

## How to use this

- Work top to bottom. Each phase builds on the last.
- For every phase: go through the theory resource **and** finish the project before moving on. Do not stack courses without building — that's the #1 way people stall.
- Suggested pace: ~1 phase per week if part-time, faster if full-time. The whole path is roughly 6–8 weeks.
- **Start light, go deeper only when you need to.** You do not need to understand how a transformer works internally to build great AI products. Learn *just enough* to reason about behavior, cost, and failure modes. The deep internals are optional and clearly marked below.
- LangChain note: it's a great practical spine (Phases 4–5), but learn the **raw model API first** (Phase 2) so you understand what LangChain abstracts. When something breaks, you'll know why.



## How this maps to [roadmap.sh](http://roadmap.sh)

If you're cross-referencing the official roadmap, here's where each phase lands:


| roadmap.sh section                                                                        | Phase here                                  |
| ----------------------------------------------------------------------------------------- | ------------------------------------------- |
| Introduction · LLMs · Common Terminology                                                  | Phase 1                                     |
| Using Pre-trained Models → **Choosing the Right Model**                                   | Phase 1                                     |
| OpenAI Platform · API · Managing Tokens                                                   | Phase 2                                     |
| Prompt Engineering                                                                        | Phase 3                                     |
| AI Safety and Ethics                                                                      | Woven into Phases 2–3 (see the Safety note) |
| Embeddings & Vector Databases · RAG                                                       | Phase 4                                     |
| AI Agents                                                                                 | Phase 5                                     |
| Multimodal AI                                                                             | Optional (see Phase 5b)                     |
| Open-Source AI · Hugging Face · Ollama                                                    | Bonus                                       |
| (Eval, observability, deployment, capstone go beyond roadmap.sh but matter for real jobs) | Phases 6–7                                  |


---



## Phase 1 — LLM fundamentals & choosing a model

**Goal:** Build a *working* mental model of LLMs — tokens, context windows, temperature, embeddings, and what "pre-trained" means — **plus** learn how to pick the right model for a job (the roadmap.sh "Choosing the Right Model" skill). You do **not** need to derive transformer math. You need enough intuition to reason about behavior, cost, and which model to reach for.

**Theory (start gentle → optional deeper)**

Start here (no math, no coding required):

- Andrew Ng — **"Generative AI for Everyone"** (free to audit) — [https://www.deeplearning.ai/courses/generative-ai-for-everyone](https://www.deeplearning.ai/courses/generative-ai-for-everyone) — the clearest plain-English intro to what generative AI can and can't do.
- Andrej Karpathy — **"Intro to Large Language Models"** (~1 hour, YouTube) — a friendly, no-math tour of how LLMs behave. Search the title on YouTube.
- 3Blue1Brown — **"But what is a GPT?"** (YouTube) — a beautifully visual explanation if you want intuition for what's happening inside, without equations.

Then, for **Choosing the Right Model** (this is the roadmap.sh node you were missing):

- Anthropic model overview — [https://docs.claude.com](https://docs.claude.com) (see the Models pages: capabilities, context windows, pricing)
- OpenAI models overview — [https://platform.openai.com/docs/models](https://platform.openai.com/docs/models)
- Live model comparisons (quality vs speed vs price): **Artificial Analysis** — [https://artificialanalysis.ai](https://artificialanalysis.ai) — and **LMArena** leaderboard — [https://lmarena.ai](https://lmarena.ai)

Optional — **only if you later want the internals** (this is where the old Phase 1 started, and it's genuinely harder — treat it as a deep dive, not a prerequisite):

- Hugging Face **LLM Course** — [https://huggingface.co/learn/llm-course](https://huggingface.co/learn/llm-course) (transformers, tokenization internals, the `transformers` library). Great, but it's closer to ML-engineer depth. Come back to it after Phase 4 if you're curious.

**Project (practice)**

- **Tokens & cost:** Write a small script using a tokenizer (`tiktoken`) that takes a sentence, shows how it becomes tokens, counts them, and estimates the API cost for a given model's price. This makes "context window" and "pricing" concrete.
- **Choosing a model (the key new exercise):** Take one real prompt (e.g. "summarize this support email in 3 bullets") and run it against 2–3 models across providers using their free tiers or playgrounds (e.g. Claude, a GPT model, Gemini). For each, note answer quality, speed, and cost. Write a 5-line note: *which model would I pick for this job, and why?* That decision — quality vs latency vs cost — is exactly what "AI Engineer: Choosing the Right Model" means.

*(The embeddings/cosine-similarity intuition moves to Phase 4, where it belongs — that's where roadmap.sh puts embeddings too.)*

---



## Phase 2 — Working with model APIs

**Goal:** Comfortably call an LLM API: messages format, system prompts, streaming, conversation history, structured (JSON) output, temperature, and token/cost management. On roadmap.sh this is the **OpenAI Platform / API / Managing Tokens** section.

**Theory (docs/course)**

- Anthropic **API Fundamentals** course — [https://github.com/anthropics/courses](https://github.com/anthropics/courses) (API keys, model params, multimodal prompts, streaming)
- Anthropic API docs — [https://docs.claude.com](https://docs.claude.com)
- OpenAI docs + **OpenAI Cookbook** — [https://github.com/openai/openai-cookbook](https://github.com/openai/openai-cookbook) (recipe-style, copy-paste examples)

**Project (practice)**

- Build a command-line chatbot from scratch (no framework) that: keeps conversation history, streams responses token-by-token, uses a system prompt, and lets you switch models (reuse the model comparison instinct from Phase 1).
- Add a mode that returns **structured JSON** (e.g. extract `{name, date, sentiment}` from a paragraph) and validate it in code.

> **Safety note (roadmap.sh "AI Safety and Ethics" starts here).** The moment you accept real user input, you inherit **prompt-injection** risk — a user (or a document) telling your model to ignore its instructions. As you build from here on, keep three habits: (1) never concatenate raw user text into a trusted system prompt without thinking about it, (2) constrain inputs and outputs (validate that JSON, cap lengths), and (3) know your use case so you can spot unsafe outputs. You'll apply this concretely when you add tools in Phase 5.

---



## Phase 3 — Prompt engineering

**Goal:** The highest-ROI skill on this roadmap. System prompts, few-shot examples, chain-of-thought, structured output, and how to *test* prompts instead of guessing.

**Theory (docs/course)**

- Anthropic **Prompt Engineering Interactive Tutorial** — [https://github.com/anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) (9 chapters, exercises, answer key — the best hands-on one)
- DeepLearning.AI **ChatGPT Prompt Engineering for Developers** (free) — [https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers)
- Reference: **Prompt Engineering Guide** — [https://www.promptingguide.ai](https://www.promptingguide.ai)

**Project (practice)**

- Pick a real task (classify support tickets, extract structured fields from messy text, or summarize with a fixed format).
- Write 3–4 prompt versions and build a tiny eval set (10–20 examples with expected answers) to measure which prompt wins. This directly feeds Phase 6.

---



## Phase 4 — RAG, embeddings & vector databases

**Goal:** The core architecture behind most real LLM products. Document loading → chunking → embeddings → vector store → retrieval → grounded answer with citations. **This is where LangChain earns its place.** On roadmap.sh this is two sections — **Embeddings & Vector Databases** then **RAG** — so tackle them in that order.

**Theory (docs/course)**

- **Embeddings first (the intuition):** Embed 10–20 sentences, compute cosine similarity, and confirm that semantically similar sentences score higher. *(This is the exercise moved from the old Phase 1 — it makes far more sense here, right before you use embeddings for retrieval.)*
- LangChain official docs — [https://python.langchain.com](https://python.langchain.com) (start with the RAG tutorial under "Tutorials")
- DeepLearning.AI **Retrieval Augmented Generation (RAG)** — [https://www.deeplearning.ai/courses/retrieval-augmented-generation](https://www.deeplearning.ai/courses/retrieval-augmented-generation)
- DeepLearning.AI **Building and Evaluating Advanced RAG** (chunking, retrieval quality)

**Project (practice)** — *this is your flagship project*

- Build a "chat with your documents" app: load PDFs → chunk them → embed → store in a vector DB (start with Chroma or FAISS locally, then try `pgvector` in Postgres) → retrieve the top chunks → answer questions **with source citations**.
- Deliberately break it: ask a question your docs don't cover and make it say "I don't know" instead of hallucinating. Handling empty retrieval well is what separates a demo from a real system.

---



## Phase 5 — AI agents & tool use

**Goal:** Give the model the ability to call tools and take multi-step actions: function/tool calling, the agent loop, and orchestration with LangGraph.

**Theory (docs/course)**

- Anthropic **Tool Use** course — [https://github.com/anthropics/courses](https://github.com/anthropics/courses)
- LangChain Academy **Introduction to LangGraph** (free, official) — [https://academy.langchain.com/courses/intro-to-langgraph](https://academy.langchain.com/courses/intro-to-langgraph) with runnable notebooks at [https://github.com/langchain-ai/langchain-academy](https://github.com/langchain-ai/langchain-academy)
- Hugging Face **AI Agents Course** — [https://huggingface.co/learn/agents-course](https://huggingface.co/learn/agents-course) (smolagents, LlamaIndex, LangGraph; certificate available)

**Project (practice)**

- Build an agent that has 2–3 tools: a web search, a calculator, and your RAG retriever from Phase 4. Watch it decide which tool to call.
- Rebuild it with LangGraph so it can loop and branch (e.g. retry a search, then answer). **Apply the Phase 2 safety note here:** add a guard so raw user input is never passed unsanitized into a tool — this is the most common real-world agent vulnerability.

---



## Phase 5b — Multimodal AI *(optional)*

**Goal:** roadmap.sh includes a **Multimodal AI** section. It's optional for your first job-ready portfolio, but worth a taste: images, audio, and speech in and out.

**Theory (docs/course)**

- Anthropic vision docs (image understanding) — [https://docs.claude.com](https://docs.claude.com)
- OpenAI vision, image generation, and Whisper (speech-to-text) docs — [https://platform.openai.com/docs](https://platform.openai.com/docs)

**Project (practice)**

- Add one modality to an existing project: e.g. let your Phase 4 doc-chat app accept a screenshot and answer questions about it, or add speech-to-text so you can ask questions by voice.

---



## Phase 6 — Evaluation, observability & deployment

**Goal:** No longer "advanced" — this is table stakes. Measure prompt/agent quality, trace what's happening, and ship it. *(This goes beyond roadmap.sh's node list but is what actually gets you hired.)*

**Theory (docs/course)**

- Anthropic **Prompt Evaluations** course — [https://github.com/anthropics/courses](https://github.com/anthropics/courses)
- LangSmith docs + LangChain Academy LangSmith courses — [https://academy.langchain.com](https://academy.langchain.com) (tracing, cost/latency monitoring, evals on live data)

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

- **Open-source models & Hugging Face / Ollama** — roadmap.sh has a whole "Open-Source AI" section. Once you're comfortable with hosted APIs, run models locally with Ollama ([https://ollama.com](https://ollama.com)) — models like Llama or Qwen — useful for privacy-sensitive RAG. Browse Hugging Face Hub to see what open models exist.
- **Hugging Face LLM Course** — [https://huggingface.co/learn/llm-course](https://huggingface.co/learn/llm-course) — the transformer-internals deep dive from Phase 1's optional list. Best done *after* Phase 4, when the internals will actually mean something to you.
- **MCP (Model Context Protocol) Course** — [https://huggingface.co/learn/mcp-course](https://huggingface.co/learn/mcp-course) (the emerging standard for connecting tools/data to models)
- **Fine-tuning** — only learn this *after* the above, and only when prompting + RAG genuinely can't solve your problem. It's often the wrong first tool.



## The two-spine summary

If you want the shortest "just tell me what to click" version:

1. **DeepLearning.AI short courses** for structured theory (Generative AI for Everyone → prompting → RAG → agents).
2. **LangChain Academy + LangChain docs** for the hands-on framework spine.
3. **Anthropic's courses repo** for API fundamentals, prompting, tool use, and evals done right.
4. **roadmap.sh/ai-engineer** as the map — use its "Choosing the Right Model" and safety nodes as checkpoints.

Alternate a course with its matching project from this roadmap. Never just watch — build after every unit.