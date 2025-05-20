from fpdf import FPDF
from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm import Session
import os
from app.utils.config_loader import get_config
from fastapi import HTTPException, status
from app.utils.file_handler import save_file

# Get file storage path from configuration
PDF_DIRECTORY = get_config("PDF_DIRECTORY", "./pdf_reports")

# Ensure the PDF directory exists
os.makedirs(PDF_DIRECTORY, exist_ok=True)

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Tire Recycling and Fleet Management Report", 0, 1, "C")
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_title(self, title: str):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, 0, 1, "C")
        self.ln(5)

    def add_text(self, text: str):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln(5)

    def add_table(self, headers: List[str], data: List[Dict[str, str]]):
        self.set_font("Arial", "B", 12)
        for header in headers:
            self.cell(40, 10, header, 1, 0, "C")
        self.ln()

        self.set_font("Arial", "", 12)
        for row in data:
            for header in headers:
                self.cell(40, 10, str(row.get(header, "")), 1, 0, "C")
            self.ln()

def generate_pdf(data: List[Dict[str, str]], title: str) -> str:
    """
    Generate a generic PDF report with a title and table of data.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_title(title)

    # If data is not empty, use the first dictionary to get headers
    if data:
        headers = list(data[0].keys())
        pdf.add_table(headers, data)

    file_name = f"{title.replace(' ', '_').lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(PDF_DIRECTORY, file_name)
    pdf.output(file_path)
    return file_path


def generate_order_report(order_id: int, customer_name: str, items: List[Dict[str, str]], total_price: float) -> str:
    """
    Generate a PDF report for an order.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_title(f"Order Report - ID: {order_id}")
    pdf.add_text(f"Customer Name: {customer_name}")
    pdf.add_text(f"Total Price: {total_price} SAR")
    pdf.add_table(["Item Name", "Quantity", "Unit Price", "Total"], items)

    file_path = os.path.join(PDF_DIRECTORY, f"order_report_{order_id}.pdf")
    pdf.output(file_path)
    return file_path

def generate_mission_report(mission_id: int, driver_name: str, orders: List[Dict[str, str]], distance: float) -> str:
    """
    Generate a PDF report for a mission.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_title(f"Mission Report - ID: {mission_id}")
    pdf.add_text(f"Driver Name: {driver_name}")
    pdf.add_text(f"Total Distance: {distance} km")
    pdf.add_table(["Order ID", "Customer Name", "Items Count", "Status"], orders)

    file_path = os.path.join(PDF_DIRECTORY, f"mission_report_{mission_id}.pdf")
    pdf.output(file_path)
    return file_path

def generate_audit_log_report(logs: List[Dict[str, str]]) -> str:
    """
    Generate a PDF report for audit logs.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_title("Audit Log Report")
    pdf.add_table(["Timestamp", "User", "Action", "Description"], logs)

    file_path = os.path.join(PDF_DIRECTORY, "audit_log_report.pdf")
    pdf.output(file_path)
    return file_path


# Download a report file by ID
def download_report(db: Session, report_id: int):
    report_path = f"./pdf_reports/report_{report_id}.pdf"  # Updated to match the directory
    try:
        return save_file(report_path)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
