import pdfplumber
import io
from typing import Optional
from services.llm_service import llm_service

ocr_service = None

class OCRService:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """
        Extracts text from a PDF file using a hybrid approach:
        1. Tries digital text extraction first (fast).
        2. Falls back to Gemini Vision if digital extraction yields little/no text (slow but accurate).
        """
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    # 1. Try fast digital extraction
                    extracted_text = page.extract_text() or ""
                    
                    # If we found substantial text (>50 chars), assume it's digitally readable
                    if len(extracted_text.strip()) > 50:
                        text += extracted_text + "\n\n"
                    else:
                        # 2. Fallback to Gemini Vision for scanned/handwritten pages
                        try:
                            # Convert page to image
                            image = page.to_image(resolution=300).original
                            
                            # Convert PIL image to bytes for the LLM service
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='PNG')
                            img_bytes = img_byte_arr.getvalue()
                            
                            page_text = llm_service.transcribe_image(img_bytes)
                            if page_text:
                                text += page_text + "\n\n"
                        except Exception as e:
                            print(f"Error invoking Gemini on PDF page: {e}")
                            
            return text.strip()
        except Exception as e:
            return f"Error during PDF extraction: {str(e)}"

    def extract_text_from_image(self, file_bytes: bytes) -> str:
        """
        Extracts text from an image using Gemini Vision (LLMService).
        """
        return llm_service.transcribe_image(file_bytes)

ocr_service = OCRService()
