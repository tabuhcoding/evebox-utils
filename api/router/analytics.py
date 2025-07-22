from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from utils.analytics_v2 import get_event_analytics as get_event_analytics_v2
from utils.analytics import get_event_analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

class EventAnalyticsInput(BaseModel):
  data: Optional[dict] = None
  event: Optional[str] = ""
  query: Optional[str] = ""
  threadId: Optional[str] = None

@router.post("/v2")
async def get_analytics(input: EventAnalyticsInput) -> Any:
  try:
    # result = get_event_analytics(input.data, input.event, input.query)
    content, threadId, usage = get_event_analytics_v2(
        query=input.query,
        data=input.data,
        event=input.event,
        previous_thread_id=input.threadId
    )
    return { "content": content, "threadId": threadId, "usage": usage }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("")
async def get_analytics(input: EventAnalyticsInput) -> Any:
  try:
    result = get_event_analytics(input.data, input.query)
    return { "result": result }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))