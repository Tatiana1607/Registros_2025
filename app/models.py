import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Iniicalizamos la base de datos
db = SQLAlchemy()

# Tabla de Empresas de Transporte
class EmpresaTransporte(db.Model):
    __tablename__ = 'empresa_transporte'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False, unique = True)

    def __repr__(self):
        return f"<EmpresaTransporte {self.nombre}>"

# Tabla de empresas de terceros
class EmpresaExternos(db.Model):
    __tablename__ = 'empresa_externos'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False, unique = True)

    def __repr__(self):
        return f"<EmpresaExternos {self.nombre}>"

class CentroDistribucion(db.Model):
    __tablename__ = 'centros_distribucion'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False, unique = True)

    def __repr__(self):
        return f"<CentroDistribucion {self.nombre}>"

# Tabla para Hallazgos
class Hallazgo(db.Model):
    __tablename__ = 'hallazgos'

    id = db.Column(db.Integer, primary_key = True)
    rut = db.Column(db.String(12), nullable = False, unique = True)
    nombre_completo = db.Column(db.String(100), nullable = False)
    area = db.Column(db.String(100), nullable = False)
    fecha = db.Column(db.Date, nullable = False)
    motivo_desvinculacion = db.Column(db.String(100), nullable = False) #Lista desplegable
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa_externos.id'), nullable = False)
    centro_distribucion_id = db.Column(db.Integer, db.ForeignKey('centros_distribucion.id'), nullable = False) #Lista desplegable

    empresa = db.relationship('EmpresaExternos', backref = db.backref('hallazgos', lazy = True))
    centro_distribucion = db.relationship('CentroDistribucion', backref = db.backref('hallazgos', lazy = True))

    @validates('rut')
    def validate_rut(self, key, value):
        # Expresión regular para validar el formato del RUT chileno
        rut_pattern = r'^\d{7,8}-[0-9kK]$'

        if not re.match(rut_pattern, value):
            raise ValueError("El formato del RUT debe ser sin puntos y con guion 12345678-9")
        return value
    
    def __repr__(self):
        return f"<Hallazgo {self.nombre_completo}, {self.rut}>"

# Sub-tablas para Motivos de Desvinculación
class HurtoRoboMercaderia(Hallazgo):
    pass

class ConsumoMercaderia(Hallazgo):
    pass

class ConsumoSustanciasIlicitas(Hallazgo):
    pass

class MalasPracticas(Hallazgo):
    pass
    detalles_motivo = db.Column(db.String(255),nullable = False) #Este campoes obligatorio para "Malas prácticas"

class Danos(Hallazgo):
    pass
    detalles_dano = db.Column(db.String(255), nullable = False) #Este campo es obligatorio para "Daños"

#Modelo para la tabla de Incidentes
class Incidente(db.Model):
    __tablename__ = 'incidentes'

    id = db.Column(db.Integer, primary_key = True)
    fecha_incidente = db.Column(db.Date, nullable = False)
    rut = db.Column(db.String(12), nullable = False) #Permitimos duplicados
    nombre_conductor = db.Column(db.String(100), nullable = False)
    lugar_incidente = db.Column(db.String(100), nullable = False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa_transporte.id'), nullable = False)
    patente_camion = db.Column(db.String(10), nullable = False)
    tipo_incidente = db.Column(db.String(100)) #Lista desplegable
    centro_distribucion_id = db.Column(db.Integer, db.ForeignKey('centros_distribucion.id'), nullable = False) #Lista desplegable

    empresa = db.relationship('EmpresaTransporte', backref = db.backref('incidente', lazy = True))
    centro_distribucion = db.relationship('CentroDistribucion', backref = db.backref('incidente', lazy = True))

    @validates('rut')
    def validate_rut(self, key, value):
        rut_pattern = r'^\d{7,8}-[0-9kK]$'
        if not re.match(rut_pattern, value):
            raise ValueError("El formato del RUT debe ser sin puntos y con guion 12345678-9")
        return value
    
    def __repr__(self):
        return f"<Incidente {self.nombre_completo}, {self.rut}>"

    #Sub-tablas para Tipos de Incidentes
class RoboParcial(Incidente):
    pass

class RoboTotal(Incidente):
    pass

class Volcamiento(Incidente):
    pass

class RupturaSello(Incidente):
    pass

class OtrosIncidentes(Incidente):
    pass
    detalles_incidente = db.Column(db.String(255), nullable = False) #Campo adicional para "Otros"
