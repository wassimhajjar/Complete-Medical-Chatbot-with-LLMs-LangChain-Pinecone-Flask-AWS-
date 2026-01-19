import itertools
from typing import Any, List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult

class RotatingGemini(BaseChatModel):
    # List of keys from DIFFERENT Google Cloud projects
    api_keys: List[str]
    model_name: str = "gemini-3-flash-preview"
    temperature: float = 0.7
    
    # Internal state to cycle keys
    _key_cycle: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a non-ending iterator for the keys
        self._key_cycle = itertools.cycle(self.api_keys)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # We will try up to the number of keys we have
        for _ in range(len(self.api_keys)):
            current_key = next(self._key_cycle)
            try:
                # Initialize a temporary model with the current key
                llm = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    google_api_key=current_key,
                    temperature=self.temperature,
                    max_retries=0 # We handle retries via rotation instead
                )
                return llm._generate(messages, stop=stop, **kwargs)
            
            except Exception as e:
                # Check specifically for Rate Limit (Error 429)
                if "429" in str(e) or "Resource has been exhausted" in str(e):
                    print(f"⚠️ Key exhausted. Rotating to next project...")
                    continue
                else:
                    # If it's a different error (like a syntax error), raise it
                    raise e
        
        raise RuntimeError("❌ All API keys from all projects have reached their limits.")

    @property
    def _llm_type(self) -> str:
        return "rotating_gemini"