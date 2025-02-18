from app import create_app, db
from models import EmpresaTransporte, EmpresaExternos, CentroDistribucion

app = create_app()
with app.app_context():

#Datos iniciales para empresa de trasnporte
    empresa_transporte = [
        "Transportes Acevedo",
        "Transportes Bastias",
        "Callegari",
        "Transportes Carga Inteligente",
        "CCTI",
        "Transportes Infinity",
        "Transportes Joselyn del Pilar Sanchez",
        "Transportes Julieta",
        "Transportes Manqueñir",
        "Transportes Maria Conejera/Martel",
        "Transportes RYF",
        "Transpores Ruta Sur",
        "Transportes Sahid",
        "Transportes Tamara Lecaros",
        "Transportes Vidal"
    ]

    for nombre in empresa_transporte:
        if not EmpresaTransporte.query.filter_by(nombre=nombre).first():
            db.session.add(EmpresaTransporte(nombre=nombre))


#Datos iniciales para empresas externas
    empresas_externas = [
        "B&Z",
        "DIMAC",
        "GYG",
        "MANPOWER",
        "XINERLINK",
        "MACROSERVICE",
        "M&L",
        "SAEP",
        "GRUPO AMERICA LIMPIEZA",
        "COLCHAGUA",
        "INOCLEAN"
    ]

    for nombre in empresas_externas:
        if not EmpresaExternos.query.filter_by(nombre=nombre).first():
            db.session.add(EmpresaExternos(nombre=nombre))

#Datos iniciales para centros de distribucion
    centros = [
        "La Farfana",
        "Icestar",
        "Centro de producción"
    ]

    for centro in centros:
        if not CentroDistribucion.query.filter_by(nombre=centro).first():
            db.session.add(CentroDistribucion(nombre=centro))

    db.session.commit()
    print("Datos iniciales insertados correctamente")

