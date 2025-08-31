from fastapi import APIRouter

from app.services.ai_service import AIService
from app.requests.ai import SuggestRequest

router = APIRouter()


@router.post("/suggest")
async def suggest(payload: SuggestRequest):

    service = AIService()
    suggestion = await service.suggestDescription(payload.title.strip())
    return {"suggestion": suggestion}