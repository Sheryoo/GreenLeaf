import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from werkzeug.utils import secure_filename
from reportlab.lib.colors import green, red


def generate_classification_report(data):
    pdf_name = f"report_{secure_filename(data[0])}_{data[6]}.pdf"
    if not os.path.exists('public/pdf'):
        os.makedirs('public/pdf')
    pdf_path = os.path.join('public/pdf', pdf_name)
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    normal_style = styles['Heading2']
    text_style = styles['Heading3']

    confidence_color = green if data[1] > 80 else red
    confidence_style = ParagraphStyle(
        name="confidence", parent=normal_style, textColor=confidence_color)

    report_content = []
    title_style = ParagraphStyle(
        name="title",
        parent=heading_style,
        alignment=1,
        fontSize=24
    )
    report_content.append(
        Paragraph(f"{data[0].split(' ')[0]} Classification Report:\n", title_style))

    report_content.append(
        Paragraph(f"<b>Confidence:</b>{data[1]}", confidence_style))

    report_content.append(
        Paragraph(f"<b>Predictions:</b> {data[0]}", normal_style))
    report_content.append(
        Paragraph("<b>Description:</b>", normal_style))
    report_content.append(
        Paragraph(f"{data[2]}", text_style))
    report_content.append(
        Paragraph("<b>Temperature:</b>", normal_style))
    report_content.append(
        Paragraph(f"{data[3]}", text_style))
    report_content.append(
        Paragraph("<b>Sunlight:</b> ", normal_style))
    report_content.append(
        Paragraph(f"{data[4]}", text_style))
    report_content.append(
        Paragraph("<b>Watering:</b>", normal_style))
    report_content.append(
        Paragraph(f"{data[5]}", text_style))

    pdf.build(report_content)

    return "/uploads/pdf/" + pdf_name
