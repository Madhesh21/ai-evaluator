from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.report_service import report_service

router = APIRouter(tags=["report"])

class ReportPayload(BaseModel):
    evaluation_results: List[Dict]
    student_name: Optional[str] = "Student"

@router.post("/generate-report")
async def generate_report(payload: ReportPayload):
    try:
        pdf_bytes = report_service.generate_evaluation_pdf(
            payload.evaluation_results, 
            payload.student_name
        )
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=Evaluation_Report_{payload.student_name.replace(' ', '_')}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
