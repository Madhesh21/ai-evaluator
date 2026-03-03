import json
import os
import sys

# Add the backend directory to the path so we can import services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.report_service import report_service

def test_report_generation():
    evaluation_results = [
        {
            "id": "1",
            "marks_awarded": "2",
            "feedback": "Correct definition of Router and Gateway. Good detail on operating layers.",
            "status": "Attempted"
        },
        {
            "id": "2",
            "marks_awarded": "1",
            "feedback": "Partially correct. Identified 3 events but should be 6.",
            "status": "Attempted"
        },
        {
            "id": "11(a)",
            "marks_awarded": "13",
            "feedback": "Excellent explanation of OSI layers.",
            "status": "Attempted"
        },
        {
            "id": "11(b)",
            "marks_awarded": "0",
            "feedback": "Alternative choice chosen.",
            "status": "Alternative Choice Chosen"
        }
    ]
    
    print("Generating test PDF report...")
    pdf_bytes = report_service.generate_evaluation_pdf(evaluation_results, "Test Student")
    
    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    
    print(f"Success! Report generated and saved to: {os.path.abspath('test_report.pdf')}")

if __name__ == "__main__":
    test_report_generation()
