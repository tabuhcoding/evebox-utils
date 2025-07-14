from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from utils.analytics import get_event_analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

class EventAnalyticsInput(BaseModel):
  data: dict
  query: Optional[str] = ""

@router.post("")
async def get_analytics(input: EventAnalyticsInput) -> Any:
  try:
    result = get_event_analytics(input.data, input.query)
    return { "result": result }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))