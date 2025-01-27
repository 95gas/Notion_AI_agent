from llama_index.llms.openai import OpenAI
import os

class LLM:
    def __init__(self):
        """
        Initialize the llm
        """
        self.openai_model = os.getenv("OPENAI_MODEL_NAME_CHAT")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self._openai_llm = None

    def openai_llm(self) -> OpenAI:
        """Lazy initialization of the OpenAI LLM."""
        if self._openai_llm is None:
            return OpenAI(model=self.openai_model)
        return self._openai_llm