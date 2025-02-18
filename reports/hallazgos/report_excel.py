import io
from flask import make_response
import pandas as pd
from app.models import Hallazgo

def excel_hallazgos():
    """Generar un archivo Excel con la lista de hallazgos."""

    hallazgos = Hallazgo.query.all() # Obtener todos los hallazgos

    # Convertir los datos en un DataFrame de Pandas
    data = [
        {
            "ID": h.id,
            "RUT": h.rut,
            "Nombre completo": h.nombre_completo,
            "Motivo desvinculación": h.motivo_desvinculacion,
            "Empresa externa": h.empresa.nombre if h.empresa else "N/A",
            "Centro distribución": h.centro_distribucion.nombre if centro_distribucion else "N/A",
            "Fecha desvinculación": h.fecha.strtime("%Y-%m-%d")
        }
        for h in hallazgos
    ]

    df = pd.DataFrame(data)

    # Guardar el archivo en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlswriter') as writer:
        df.to_excel(writer, sheet_name='Hallazgos', index=False)
    
    output.seek(0)

    # Crear y devolver respuesta Flask con el archivo Excel 
    response = make_response(output.read())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename= "hallazgos.xlsx"'
    return response