# routes/revenue.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from utils.revenue import analyze_revenue_event
from utils.revenue_v2 import analyze_revenue_event as analyze_revenue_event_v2
from utils.admin import get_event_analytics as analyze_revenue_event_admin


router = APIRouter(prefix="/revenue", tags=["revenue"])

class RevenueAnalysisInput(BaseModel):
    data: dict
    event: Optional[str] = ""
    query: Optional[str] = ""
    threadId: Optional[str] = None

@router.post("")
async def analyze_revenue(input: RevenueAnalysisInput) -> Any:
    try:
        result = analyze_revenue_event(input.data, input.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v2")
async def get_analytics(input: RevenueAnalysisInput) -> Any:
  try:
    # result = get_event_analytics(input.data, input.event, input.query)
    content, threadId = analyze_revenue_event_v2(
        query=input.query,
        data=input.data,
        event=input.event,
        previous_thread_id=input.threadId
    )
    return { "content": content, "threadId": threadId }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/admin")
async def get_analytics(input: RevenueAnalysisInput) -> Any:
  try:
    # result = get_event_analytics(input.data, input.event, input.query)
    content, threadId = analyze_revenue_event_admin(
        query=input.query,
        data=input.data,
        previous_thread_id=input.threadId
    )
    return { "content": content, "threadId": threadId }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))