from fpdf import FPDF
import datetime
from typing import List, Dict

class ReportService:
    def generate_evaluation_pdf(self, evaluation_results: List[Dict], student_name: str = "Student") -> bytes:
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(26, 35, 126) # Indigo 900
        pdf.cell(0, 15, "University Assessment Report", ln=True, align='C')
        
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(10)
        
        # Student Info
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(40, 10, "Student Name:", 0)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, student_name, 1, ln=True)
        pdf.ln(5)
        
        # Summary
        total_score = sum(float(r.get("marks_awarded", 0)) for r in evaluation_results)
        total_score = min(100, total_score) # Cap at 100
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Evaluation Summary", ln=True)
        pdf.set_draw_color(26, 35, 126)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(50, 10, "Total Score:", 0)
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(46, 125, 50) # Green 800
        pdf.cell(0, 10, f"{total_score} / 100", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)
        
        # Detailed Results Table
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Detailed Breakdown", ln=True)
        
        # Table Header
        pdf.set_fill_color(232, 234, 246) # Indigo 50
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(15, 10, "ID", 1, 0, 'C', True)
        pdf.cell(110, 10, "Feedback", 1, 0, 'C', True)
        pdf.cell(30, 10, "Status", 1, 0, 'C', True)
        pdf.cell(35, 10, "Marks", 1, 1, 'C', True)
        
        # Table Rows
        pdf.set_font("Arial", '', 9)
        for res in evaluation_results:
            # Multi-line feedback handling
            feedback = res.get("feedback", "No feedback provided.")
            status = res.get("status", "N/A")
            marks = res.get("marks_awarded", "0")
            qid = res.get("id", "-")
            
            # Use multi_cell for feedback to wrap text
            old_x = pdf.get_x()
            old_y = pdf.get_y()
            
            # Find height needed for feedback cell
            pdf.set_xy(old_x + 15, old_y)
            feedback_height = pdf.get_string_width(feedback) / 110 # Estimation
            # Actually fpdf does this better with multi_cell
            
            # Start row
            h = 10 # Default height
            
            pdf.cell(15, h, qid, 1, 0, 'C')
            
            # Feedback Cell (wrapped)
            curr_x = pdf.get_x()
            curr_y = pdf.get_y()
            pdf.multi_cell(110, 5, feedback, 1, 'L')
            new_y = pdf.get_y()
            h = new_y - curr_y
            if h < 10: h = 10 # Ensure min height
            
            # Go back and finish other cells for this row if multi_cell changed position
            pdf.set_xy(curr_x + 110, curr_y)
            pdf.cell(30, h, status, 1, 0, 'C')
            pdf.cell(35, h, str(marks), 1, 1, 'C')
            
            # Ensure next row starts at the correct Y
            pdf.set_y(new_y if new_y > curr_y + h else curr_y + h)

        # Footer
        pdf.set_y(-30)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "This is an AI-generated assessment report. Please verify with official university records.", align='C', ln=True)
        pdf.cell(0, 10, f"Page {pdf.page_no()}", align='C')
        
        return pdf.output()

report_service = ReportService()
