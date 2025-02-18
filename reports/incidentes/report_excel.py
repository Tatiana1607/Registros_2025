import io
from flask import make_response
import pandas as pd
from app.models import Incidente

def excel_incidentes():
    """
    Genera un archivo Excel con la lista de incidentes.
    """
    incidentes = Incidente.query.all()  # Obtener todos los incidentes

    # Convertir los datos en un DataFrame de Pandas
    data = [
        {
            "ID": i.id,
            "RUT": i.rut,
            "Nombre Conductor": i.nombre_conductor,
            "Patente Camión": i.patente_camion,
            "Fecha Incidente": i.fecha_incidente.strftime("%Y-%m-%d"),
            "Lugar Incidente": i.lugar_incidente,
            "Tipo Incidente": i.tipo_incidente,
            "Detalles": i.detalles_incidente or "N/A",
            "Empresa Transporte": i.empresa.nombre if i.empresa else "N/A",
            "Centro Distribución": i.centro_distribucion.nombre if i.centro_distribucion else "N/A"
        }
        for i in incidentes
    ]

    df = pd.DataFrame(data)

    # Guardar el archivo en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Incidentes', index=False)

    output.seek(0)

    # Crear y devolver respuesta Flask con el archivo Excel
    response = make_response(output.read())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename="incidentes.xlsx"'
    return response
