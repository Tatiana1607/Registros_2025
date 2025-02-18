from flask import render_template, make_response
from weasyprint import HTML
from app.models import Hallazgo 

def pdf_hallazgos():
    """Generar un PDF con la lista de hallazgos usando una plantilla HTML."""

    hallazgos = Hallazgo.query.all() #Obtener todos los hallazgos
    
    # Renderizar plantilla HTML con los datos 
    rendered_html = render_template('reports/hallazgos_pdf.html', hallazgos=hallazgos)

    # Convertir HTML a PDF 
    pdf_file = HTML(string=rendered_html).write_pdf()

    # Crear y devolver respuesta Flask con el PDF
    respondse = make_response(pdf_file)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="hallazgos.pdf"'
    return response 

    
