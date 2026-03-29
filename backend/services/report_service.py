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
        
        pdf.set_font("Arial", 'B', 10)
        with pdf.table(
            col_widths=(15, 110, 30, 35),
            text_align=("CENTER", "LEFT", "CENTER", "CENTER"),
            line_height=8
        ) as table:
            # Table Header
            row = table.row()
            row.cell("ID")
            row.cell("Feedback", align="CENTER")
            row.cell("Status")
            row.cell("Marks")
            
            # Table Rows
            pdf.set_font("Arial", '', 9)
            for res in evaluation_results:
                feedback = str(res.get("feedback", "No feedback provided."))
                status = str(res.get("status", "N/A"))
                marks = str(res.get("marks_awarded", "0"))
                qid = str(res.get("id", "-"))
                
                row = table.row()
                row.cell(qid)
                row.cell(feedback)
                row.cell(status)
                row.cell(marks)

        # Footer
        pdf.set_y(-30)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "This is an AI-generated assessment report. Please verify with official university records.", align='C', ln=True)
        pdf.cell(0, 10, f"Page {pdf.page_no()}", align='C')
        
        return bytes(pdf.output())

report_service = ReportService()
