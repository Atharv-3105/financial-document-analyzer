from pydantic import BaseModel
from typing import Dict, Any, Optional

class QueueResponse(BaseModel):
    status: str
    job_id: str
    message: str
class AnalysisResponse(BaseModel):
    status: str
    file: Optional[str] = None
    structured_analysis: Optional[Dict[str, Any]] = None
    
class ErrorResponse(BaseModel):
    detail: str