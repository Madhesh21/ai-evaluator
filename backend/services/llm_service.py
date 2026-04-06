import os
import json
import google.generativeai as genai
import PIL.Image
import io
from typing import List, Dict
import time
import re
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def _call_gemini_with_retry(self, prompt_or_parts, max_retries=3):
        for attempt in range(max_retries):
            try:
                return self.model.generate_content(prompt_or_parts)
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota" in error_str or "Exhausted" in error_str:
                    print(f"Rate limit hit. Attempt {attempt + 1}/{max_retries}.")
                    delay = 30 # Default delay
                    match = re.search(r"retry in (\d+\.?\d*)s", error_str)
                    if match:
                        delay = float(match.group(1)) + 1
                    
                    if attempt < max_retries - 1:
                        print(f"Sleeping for {delay} seconds before retrying...")
                        time.sleep(delay)
                        continue
                print(f"Error calling Gemini: {e}")
                raise e

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
                
                # Priority list: avoiding models with 0 or 20 quota limits
                if 'models/gemini-flash-latest' in available_models:
                    self.model_name = 'models/gemini-flash-latest'
                elif 'models/gemini-2.5-flash-lite' in available_models:
                    self.model_name = 'models/gemini-2.5-flash-lite'
                elif 'models/gemini-pro-latest' in available_models:
                    self.model_name = 'models/gemini-pro-latest'
                elif available_models:
                    self.model_name = available_models[-1] # Try last
                else:
                    self.model_name = 'gemini-1.5-flash' # Fallback default
                
                print(f"Selected Model: {self.model_name}")
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Error listing models: {e}. Defaulting to gemini-pro")
                self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_questions(self, raw_text: str) -> List[Dict[str, str]]:
        """
        Parses raw text and uses Gemini to extract structured questions with Part info.
        """
        if not self.api_key:
            return [{"id": "0", "question": "API Key missing. Please set GEMINI_API_KEY.", "marks": "0", "part": "A", "co": "-", "bl": "-"}]

        prompt = f"""
        Extract all questions from the following text extracted from a university question paper.
        
        The paper MUST be divided into three parts:
        - PART-A: Simple, short questions. (Usually Q1-Q10)
        - PART-B: Analytical questions with choices. (Usually 11-15, often 11(a) OR 11(b)).
        - PART-C: A single compulsory application-based question (Usually 16).
        
        For each question, identify:
        - Question Number (id): e.g., "1", "11(a)", "11(b)(i)".
        - Question Text (question): The full text.
        - Marks (marks): Total marks.
        - Part (part): "A", "B", or "C".
        - Course Outcome (CO): e.g., CO1.
        - Bloom's Level (BL): e.g., L1.
        
        Specific Instructions:
        1. Capture EVERY question.
        2. For PART-B, if there is an "OR" choice (e.g., 11(a) OR 11(b)), extract BOTH as separate items.
        
        Return results ONLY as a VALID JSON list of objects.
        Example:
        [
            {{"id": "1", "question": "...", "marks": "2", "part": "A", "co": "CO1", "bl": "L1"}},
            {{"id": "11(a)", "question": "...", "marks": "13", "part": "B", "co": "CO2", "bl": "L3"}}
        ]

        Text to process:
        {raw_text}
        """
        
        try:
            response = self._call_gemini_with_retry(prompt)
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            questions = json.loads(content)
            return questions
        except Exception as e:
            print(f"Error in extract_questions: {e}")
            raise Exception(f"Failed to extract questions: {str(e)}")

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
            marks_int = 2 

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
            response = self._call_gemini_with_retry(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Failed to generate answer: {str(e)}")

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
            Do not include any introductory or concluding remarks.
            If the image contains diagrams, briefly describe them in [brackets].
            """
            
            response = self._call_gemini_with_retry([prompt, image])
            return response.text.strip()
        except Exception as e:
            print(f"Error in transcribe_image: {e}")
            raise Exception(f"Failed to transcribe image: {str(e)}")

    def evaluate_answers(self, questions: List[Dict], ideal_answers: Dict[str, str], student_script: str) -> List[Dict]:
        """
        Evaluates student answers with strict choice logic and NO HALLUCINATIONS.
        """
        if not self.api_key:
            return []

        prompt = f"""
        You are an objective and technical examiner for a university. 
        Evaluate the 'STUDENT ANSWER SCRIPT' against the 'QUESTIONS & IDEAL ANSWERS' provided.
        
        ### EVALUATION RULES:
        1. **MAPPING FIRST**: Before grading, scan the entire student script to locate answers. 
           - Look for question numbers (1, Q1, etc.) or technical keywords from the question/ideal answer.
           - Even if the student's numbering is slightly wrong or missing, if the content clearly answers a question, evaluate it.
        2. **STRICT EVIDENCE FOR MARKS**: Award marks based on the technical correctness found in the script. 
           - **0 marks**: Only if there is absolutely NO related content in the script for that question.
           - **Partial/Full marks**: Based on the content provided compared to the ideal answer.
        3. **PART-B CHOICE LOGIC**: For Part B (Analytical), identify which choice the student has attempted (e.g., 11(a) or 11(b)).
           - Mark the attempted choice.
           - Mark the NOT attempted choice as Status: "Alternative Choice Chosen" and 0 marks.
        4. **NO HALLUCINATION**: Do not imagine content that isn't there. If the script is genuinely blank or unrelated, mark 0.
        
        ### QUESTIONS & IDEAL ANSWERS:
        {json.dumps([{"id": q["id"], "part": q.get("part", "A"), "question": q["question"], "max_marks": q["marks"], "ideal": ideal_answers.get(q["id"], "Evaluate based on general Computer Networks knowledge.")} for q in questions], indent=2)}
        
        ### STUDENT ANSWER SCRIPT:
        {student_script}
        
        ### EXPECTED JSON OUTPUT:
        Return a JSON list of objects:
        [
            {{"id": "...", "marks_awarded": "...", "feedback": "...", "status": "Attempted" | "Not Attempted" | "Alternative Choice Chosen"}}
        ]
        """
        
        try:
            response = self._call_gemini_with_retry(prompt)
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            evaluation = json.loads(content)
            return evaluation
        except Exception as e:
            print(f"Error in evaluate_answers: {e}")
            raise Exception(f"Failed to evaluate answers: {str(e)}")

llm_service = LLMService()
