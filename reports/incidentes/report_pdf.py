from flask import render_template, make_response
from weasyprint import HTML
from app.models import Incidente

def pdf_incidentes():
    """Generar in PDF con la lisra de incidentes usando una plantilla HTML."""
    incidentes = Incidente.query.all() # Obtener todos los incidentes

    # Renderizar plantilla HTML con los datos 
    rendered_html = render_template('reports/incidentes_pdf.html', incidentes=incidentes)

    # Convertir HTML a PDF
    pdf_file = HTML(string=rendered_html).write_pdf()

    # Crear y devolder respuesta Flask con el PDF
    response = make_response(pdf_file)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="incidentes.pdf"'
    return response