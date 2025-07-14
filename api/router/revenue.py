# routes/revenue.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from utils.revenue import analyze_revenue_event

router = APIRouter(prefix="/revenue", tags=["revenue"])

class RevenueAnalysisInput(BaseModel):
    data: dict
    query: Optional[str] = ""

@router.post("")
async def analyze_revenue(input: RevenueAnalysisInput) -> Any:
    try:
        result = analyze_revenue_event(input.data, input.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
