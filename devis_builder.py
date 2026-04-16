from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(client, service, amount, quantity, invoice_date):
    file_path = "/Users/emiliehogg/Documents/Documents - MacBook Air de Emilie/GitHub/app_perso/devis.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"Client: {client}", styles["Normal"]),
        Paragraph(f"Description: {service}", styles["Normal"]),
        Paragraph(f"Prix unitaire: €{amount}", styles["Normal"]),
        Paragraph(f"Quantité: €{quantity}", styles["Normal"]),
        Paragraph(f"Date: {invoice_date}", styles["Normal"]),
    ]

    doc.build(content)
    return file_path

