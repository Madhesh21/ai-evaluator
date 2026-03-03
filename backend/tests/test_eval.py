import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from services.llm_service import llm_service

def test_evaluation():
    # 10 Part A questions, 2 Part B choices, 1 Part C compulsory
    questions = [
        {"id": str(i), "part": "A", "question": f"Question {i} text", "marks": "2"} for i in range(1, 11)
    ] + [
        {"id": "11(a)", "part": "B", "question": "Analytical Q1", "marks": "13"},
        {"id": "11(b)", "part": "B", "question": "Analytical Q2", "marks": "13"},
        {"id": "16", "part": "C", "question": "Application Q", "marks": "15"}
    ]
    
    ideal_answers = {str(i): f"Ideal A{i}" for i in range(1, 11)}
    ideal_answers.update({"11(a)": "Ideal B1", "11(b)": "Ideal B2", "16": "Ideal C"})
    
    # User's provided script text (Part A ONLY)
    student_script = "1. Router info. 2. 6 events. 3. Errors logic. 4. Frame details. 5. ARP/DHCP maps. 6. Class B. 7. TCP seq. 8. HTTP req. 9. Tools list. 10. SDN plane."
    
    print("Testing Strict Zero-Marking Policy (Part A only script)...")
    result = llm_service.evaluate_answers(questions, ideal_answers, student_script)
    
    print("\nPart B & C Results:")
    for r in result:
        if r["id"] in ["11(a)", "11(b)", "16"]:
            print(f"ID: {r['id']}, Marks: {r['marks_awarded']}, Status: {r['status']}")
            
    hallucinations = [r for r in result if r["id"] in ["11(a)", "11(b)", "16"] and float(r["marks_awarded"]) > 0]
    if not hallucinations:
        print("\nSUCCESS: No hallucinated marks for unattempted Part B/C questions.")
    else:
        print(f"\nFAILURE: Found {len(hallucinations)} hallucinated marks!")

if __name__ == "__main__":
    test_evaluation()
