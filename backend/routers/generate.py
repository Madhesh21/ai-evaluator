from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import llm_service

router = APIRouter()

class GeneratePayload(BaseModel):
    text: str
    marks: str = "2" # Default to 2 marks

@router.post("/extract-questions")
async def extract_questions(payload: GeneratePayload):
    try:
        questions = llm_service.extract_questions(payload.text)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-answers")
async def generate_answers(payload: GeneratePayload):
    """
    Expects text (Question) and marks.
    """
    try:
        answer = llm_service.generate_ideal_answer(payload.text, payload.marks)
        return {"ideal_answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class EvaluatePayload(BaseModel):
    questions: list
    ideal_answers: dict
    answer_script: str

@router.post("/evaluate")
async def evaluate_answers(payload: EvaluatePayload):
    try:
        evaluation = llm_service.evaluate_answers(
            payload.questions, 
            payload.ideal_answers, 
            payload.answer_script
        )
        return {"evaluation": evaluation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
