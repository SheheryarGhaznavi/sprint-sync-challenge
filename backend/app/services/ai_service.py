from typing import Optional
import httpx

from app.config.open_ai import getOpenAI
from app.services.base_service import BaseService


class AIService(BaseService):


    def __init__(self):
        self.settings = getOpenAI()



    async def suggestDescription(self, title: str) -> str:

        # Graceful fallback if no key
        if not self.settings.openai_api_key:
            return f"Draft: {title}. Add details about goals, deliverables, and acceptance criteria."

        prompt = (
            "You are a helpful assistant that expands a short task title into a concise task description. "
            "Keep it under 120 words, include goals, deliverables, and a brief acceptance criteria.\n"
            f"Title: {title}\nDescription:"
        )

        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}

        try:
            async with httpx.AsyncClient(timeout=15) as client:

                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": self.settings.openai_model,
                        "messages": [
                            {"role": "system", "content": "You expand titles into descriptions."},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.4,
                        "max_tokens": 220,
                    },
                )

                print("AI response")
                print(resp.json())

                if resp.status_code >= 400:
                    return f"Draft: {title}. Add details about goals, deliverables, and acceptance criteria."

                data = resp.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                return content.strip() or f"Draft: {title}. Add details..."

        except Exception:
            return f"Draft: {title}. Add details about goals, deliverables, and acceptance criteria."

