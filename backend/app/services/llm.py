"""
LLM Service - unified interface for local and cloud models
"""
import httpx
import json
from typing import Optional, List, Dict, Any
from app.config import settings

class LLMService:
    """Handles LLM interactions with both local and cloud providers"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        
    async def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Send chat messages to LLM and get response"""
        if self.provider == "ollama":
            return await self._ollama_chat(messages, temperature)
        elif self.provider == "openai":
            return await self._openai_chat(messages, temperature)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def _ollama_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Call local Ollama model"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "stream": False
                    },
                    timeout=300.0  # 5 min timeout for complex queries
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
    
    async def _openai_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Call OpenAI API (fallback for complex tasks)"""
        import openai
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI error: {str(e)}")
    
    async def stream_chat(self, messages: List[Dict[str, str]], temperature: float = 0.7):
        """Stream LLM responses (for long-running queries)"""
        if self.provider == "ollama":
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{settings.OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "stream": True
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            yield data.get("message", {}).get("content", "")
    
    async def analyze_text(self, text: str, task: str = "summarize") -> str:
        """Specialized text analysis"""
        prompt = f"Please {task} the following text:\n\n{text}"
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, temperature=0.5)
    
    async def generate_hypothesis(self, context: str) -> str:
        """Generate research hypothesis from context"""
        prompt = f"Based on this context, generate a clear, testable hypothesis:\n\n{context}"
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, temperature=0.8)

# Singleton instance
llm_service = LLMService()
