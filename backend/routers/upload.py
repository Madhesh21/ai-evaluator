from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ocr_service import ocr_service

router = APIRouter()

@router.post("/process-document")
async def process_document(file: UploadFile = File(...), doc_type: str = "question_paper"):
    """
    Upload and process a document (Question Paper or Answer Script).
    doc_type: 'question_paper' or 'answer_script'
    """
    contents = await file.read()
    
    try:
        if file.content_type == "application/pdf":
            text = ocr_service.extract_text_from_pdf(contents)
        elif file.content_type in ["image/jpeg", "image/png", "image/jpg"]:
            text = ocr_service.extract_text_from_image(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload PDF or Image.")
        
        return {
            "filename": file.filename,
            "doc_type": doc_type,
            "extracted_text": text,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
