Step 4 in depth — going from "chatting with a model" to "calling one from code"

The heart of this step is a mental shift, not a big pile of new theory. Up until now you've typed into a text box and read replies. Now you write the loop: your code decides what to send, holds the conversation history, and does something with the reply (print it, parse it, save it). Once that clicks, everything later — agents, RAG, tool use — is just a fancier version of the same loop. So the goal of Step 4 isn't to memorize parameters; it's to get comfortable owning the request/response cycle.

Here's how I'd think about each piece.

The concepts, and why each one matters

The API and the Chat Completions shape. The one idea to internalize: a chat model is stateless. It does not remember your last message. Every call, you send the entire conversation back as a list of messages, each tagged with a role — system, user, or assistant. The "memory" in a chatbot is an illusion you create by appending to that list and resending it. This is the single most important realization in the whole step, and your build makes you feel it directly. (Anthropic's Messages API works the same way; the system prompt is a separate top-level field rather than a message with role: system, but the mental model is identical.)

The system prompt is the standing instruction that shapes the model's persona and rules for the whole conversation — tone, role, constraints. user/assistant messages are the back-and-forth; the system prompt is the frame around all of them.

The sampling parameters all control the same thing from different angles: how the model picks the next token.

Temperature — the master randomness dial. Low (≈0–0.3) = focused, repeatable, good for extraction and code. High (≈0.8–1.2) = varied, creative. This is the one you'll actually reach for most.
Top-P (nucleus) and Top-K — alternative ways to restrict the candidate pool the model samples from. Top-P keeps the smallest set of tokens whose probabilities sum to p; Top-K keeps the top k tokens. In practice you tune either temperature or top-p, not both at once.
Max tokens — a hard cap on output length. Note it caps the response, not the whole conversation.
Stop sequences — strings that force the model to stop generating when it produces them. Useful when you want output to end at a delimiter.
Repetition / frequency / presence penalties — nudge the model away from repeating itself.

You don't need to master all of these now. Know what each dial does, and remember you'll meet them properly in Step 5 under "LLM Configuration." For this build, temperature is the only one you truly need.

Tokens and pricing. Models don't see words, they see tokens (roughly ¾ of a word in English). You pay per token, split into input (everything you send, including the growing history and system prompt) and output. Two consequences worth feeling early: a long conversation gets more expensive every turn because you resend the whole history, and there's a context-window ceiling on how much you can send at all. Counting tokens (OpenAI's tiktoken, or Anthropic's token-counting endpoint) is how you keep both cost and context under control.

Fine-tuning — awareness only. As the roadmap says, don't touch this yet. The order you reach for tools is: prompting → RAG → fine-tuning, and you almost never get to the third. Just file away one sentence: fine-tuning permanently teaches a model a style or task by retraining it on your examples; it's costly, needs a prepared dataset, and is rarely the right first answer. That's the whole assignment for fine-tuning at Step 4.

The build, staged so each part teaches one thing

I'd resist writing it all at once. Build it in four passes — each pass adds exactly one concept, so when something breaks you know why.

Pass 1 — One round trip. Hard-code a single user message, call the API, print the reply. No loop, no history. The only goal is: keys work, the SDK is installed, a response comes back. Get the API key out of an environment variable, never in the source.

Pass 2 — The conversation loop (this is the real lesson). Create a messages list seeded with your system prompt. Then loop: read the user's input from the terminal, append it as a user message, send the whole list, append the model's reply back as an assistant message, print it. Because you're appending both sides and resending everything, the bot now "remembers." Add a quit command to break the loop. When this works, you've understood statelessness by building around it — that's the milestone that matters.

Pass 3 — Streaming. Switch the call to streaming mode so the reply prints token-by-token as it arrives instead of appearing all at once. This changes the shape of your code: instead of one response object, you iterate over chunks and print each piece as it lands (flushing so it shows immediately). One gotcha to watch: you have to accumulate the streamed chunks into the full text yourself so you can append the complete reply back into your history.

Pass 4 — JSON extraction mode. Add a second mode (a flag, or a command like /extract). In this mode you feed the model a paragraph and a system prompt telling it to return only a JSON object with a fixed shape — say {name, date, sentiment} — and nothing else. Then the important part: validate it in code. Parse the returned string; if parsing fails or a key is missing, handle it rather than trusting the model. This is your first taste of treating model output as untrusted data that must be checked — a habit that carries all the way through agents and tool use.

For that last pass, a few things make it much more reliable:

Set temperature low (0 or near it). You want determinism, not creativity.
Be explicit and rigid in the prompt: state the exact keys, say "respond with JSON only, no prose, no markdown fences," and give one example of the exact shape you want.
Wrap the parse in a try/except. When it fails, either retry once or surface a clean error — don't let a stray backtick crash the program.
If you're on the OpenAI API, look at its JSON/structured-output mode, which constrains the model to valid JSON for you. Anthropic's approach is to prompt firmly and optionally prefill the assistant turn with an opening {. Either way, your code still validates — the API feature reduces failures, it doesn't excuse skipping the check.
A good "done" bar for the step

You can say you've finished Step 4 when: you can explain out loud why you have to resend the whole history each turn; your CLI bot holds a coherent multi-turn conversation with a system prompt; the reply streams in live; and your extraction mode produces JSON that your own code confirms is valid (and fails gracefully when it isn't). If all four are true, you've got the request/response loop in your hands — which is exactly the foundation Step 5 (prompting) and everything after build on.

One practical note: the roadmap says either provider is fine. Since your later steps and the "gentle resource" both lean on Anthropic's courses and docs, and since you're talking to me, doing the build against Anthropic's Messages API keeps everything consistent — but the concepts transfer completely, so pick whichever you'll actually stick with.

If you'd like, I can sketch the actual skeleton code for the four-pass build (in Python, against either API) so you have a scaffold to fill in rather than a blank file.