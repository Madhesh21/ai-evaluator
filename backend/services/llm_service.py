import os
import json
import google.generativeai as genai
import PIL.Image
import io
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=self.api_key)
            
            # Robust model selection
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                print(f"Available Gemini Models: {available_models}")
                
                # Priority list
                if 'models/gemini-1.5-flash' in available_models:
                    self.model_name = 'models/gemini-1.5-flash'
                elif 'models/gemini-1.5-flash-001' in available_models:
                    self.model_name = 'models/gemini-1.5-flash-001'
                elif 'models/gemini-pro' in available_models:
                    self.model_name = 'models/gemini-pro'
                elif available_models:
                    self.model_name = available_models[0]
                else:
                    self.model_name = 'gemini-1.5-flash' # Fallback default
                
                print(f"Selected Model: {self.model_name}")
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Error listing models: {e}. Defaulting to gemini-pro")
                self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_questions(self, raw_text: str) -> List[Dict[str, str]]:
        """
        Parses raw text and uses Gemini to extract structured questions.
        """
        if not self.api_key:
            return [{"id": "0", "question": "API Key missing. Please set GEMINI_API_KEY.", "marks": "0", "co": "-", "bl": "-"}]

        prompt = f"""
        Extract all questions from the following text. 
        For each question, identify:
        - Question Number (id)
        - Question Text (question)
        - Marks (marks)
        - Course Outcome (CO) e.g., CO1, CO2 (if present, else predict)
        - Bloom's Level (BL) e.g., L1, L2, L3 (if present, else predict)
        
        Return the result ONLY as a VALID JSON list of objects.
        Example format:
        [
            {{"id": "1", "question": "What is...", "marks": "2", "co": "CO1", "bl": "L1"}}
        ]

        Text to process:
        {raw_text[:3000]}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Cleanup json string if extracted with markdown fences
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            questions = json.loads(content)
            return questions
        except Exception as e:
            print(f"Error in extract_questions: {e}")
            return []

    def generate_ideal_answer(self, question: str, marks: str = "2", context: str = "") -> str:
        """
        Generates an ideal answer using Gemini, tailoring length to marks.
        """
        if not self.api_key:
            return "Error: GEMINI_API_KEY not set in backend."

        # Determine detail level based on marks
        try:
            marks_int = int(marks)
        except:
            marks_int = 2 # Default to short answer if marks parsing fails

        if marks_int <= 3:
            length_instruction = "Give a concise, direct answer in 3-5 lines."
        else:
            length_instruction = "Give a detailed, elaborated answer with points, examples, or steps as appropriate."

        prompt = f"""
        You are an expert evaluator for Computer Networks.
        Write a perfect technical answer for the following question.
        
        Question: {question}
        Marks: {marks}
        
        Instructions:
        - {length_instruction}
        - Include key technical terms.
        - Use Bullet points for readability if needed.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating answer: {str(e)}"

    def transcribe_image(self, image_bytes: bytes) -> str:
        """
        Transcribes handwriting from an image using Gemini Vision capabilities.
        """
        if not self.api_key:
            return "Error: GEMINI_API_KEY not set."

        try:
            image = PIL.Image.open(io.BytesIO(image_bytes))
            
            prompt = """
            Transcribe the handwritten text from this image page. 
            Output ONLY the text content. 
            Maintain the original structure (paragraphs, lists) as much as possible.
            Do not include any introductory or concluding remarks like "Here is the text".
            If the image contains diagrams, briefly describe them in [brackets].
            """
            
            response = self.model.generate_content([prompt, image])
            return response.text.strip()
        except Exception as e:
            print(f"Error in transcribe_image: {e}")
            return f"Error transcribing image: {str(e)}"

llm_service = LLMService()
