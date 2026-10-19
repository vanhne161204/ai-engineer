from .llm_client import LLMClient
class GuardedClient(LLMClient):
    def __init__(self, inner: LLMClient, max_input: int = 2000,
                 blocked: tuple[str, ...] = ())-> None:
        self._inner = inner
        self._max_input = max_input
        self._blocked = blocked

    def complete(self, system: str, user: str, **kwargs) -> str:
        if len(user) > self._max_input:
            return "[blocked: input too long]"
        wrapped = f"<user_input>\n{user}\n</user_input>"
        reply = self._inner.complete(system, wrapped, **kwargs)
        if any(b in reply for b in self._blocked):
            return "[blocked: policy violation]"
        return reply
      