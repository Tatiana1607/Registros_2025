from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import EmpresaTransporte, EmpresaExternos, CentroDistribucion
from flask import current_app
import re

#Validacion del RUT chileno
def validate_rut (form, field):
    rut_pattern = r'^\d{7,8}-[0-9kK]$'
    if not re.match(rut_pattern, field.data):
        raise ValidationError ("El formato del RUT debe ser sin puntos y con guion (ejemplo: 12345678-9)")

    #Validación del dígito verificador
    rut_body, dv = field.data.split('-')
    rut_body = int(rut_body)
    dv = dv.lower()
    suma = 0
    factor = 2

    for digit in reversed(str(rut_body)):
        suma += int(digit) * factor
        factor = 9 if factor == 2 else factor -1

    expected_dv = 'k' if (11 - suma % 11) == 10 else str(11 - suma % 11 % 10)
    if dv != expected_dv:
        raise ValidationError("El Rut ingresado no es válido.")


#Formulario para el registro de Hallazgos
class HallazgoForm(FlaskForm):
    rut = StringField('RUT', validators=[DataRequired(), validate_rut])
    nombre_completo = StringField('Nombre Completo', validators = [DataRequired(), Length(min=2, max=100)])
    area = StringField('Area', validators=[DataRequired(), Length(min=2, max=100)])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    motivo_desvinculacion = SelectField('Motivo de Desvinculación',
                                        choices=[('hurto_robo_mercaderia', 'Hurto/Robo de mercadería'),
                                                    ('consumo_mercaderia', 'Consumo de mercadería'),
                                                    ('consumo_sustancias_ilicitas', 'Consumo de sustancias ilícitas'),
                                                    ('malas_practicas' , 'Malas prácticas'),
                                                    ('danos', 'Daños')],
                                        validators = [DataRequired()])
    empresa_id = SelectField('Empresa Externa', coerce=int, validators = [DataRequired()])
    centro_distribucion_id = SelectField('Centro de Distribución', coerce=int, validators = [DataRequired()])
    submit = SubmitField ('Registrar Hallazgo')

    def __init__(self, *args, **kwargs):
        super(HallazgoForm, self).__init__(*args, **kwargs)
        with current_app.app_context():
            self.empresa_id.choices = [(empresa.id, empresa.nombre) for empresa in EmpresaExternos.query.all()]
            self.centro_distribucion_id.choices = [(centro.id, centro.nombre) for centro in CentroDistribucion.query.all()]

#Formulario para el registro de Incidentes
class IncidenteForm(FlaskForm):
    rut = StringField('RUT', validators = [DataRequired(), validate_rut])
    nombre_conductor = StringField('Nombre del Conductor', validators = [DataRequired(), Length(min=2, max=100)])
    patente_camion = StringField('Patente del Camión', validators = [DataRequired(), Length(min=2, max=10)])
    empresa_id = SelectField('Empresa de transporte', coerce=int,
                            choices=[(empresa.id, empresa.nombre) for empresa in EmpresaTransporte.query.all()],
                            validators = [DataRequired()])
    fecha_incidente = DateField('Fecha del Incidente', format = '%Y-%m-%d', validators = [DataRequired()])
    lugar_incidente = StringField('Lugar del Incidente', validators = [DataRequired(), Length(min=2, max=100)])
    tipo_incidente = SelectField('Tipo de incidente',
                                choices=[('robo_parcial', 'Robo parcial'),
                                            ('robo_total', 'Robo total'),
                                            ('accidente', 'Accidente'),
                                            ('ruptura_sello', 'Ruptura de sello'),
                                            ('otros', 'Otros')],
                                validators = [DataRequired()])
    detalles_incidente = StringField('Detalles del Incidente', validators = [Length(min=2, max=255)])
    centro_distribucion_id = SelectField('Centro de Distribución', coerce=int, validators = [DataRequired()])
    submit = SubmitField('Registrar Incidente')

    def __init__(self, *args, **kwargs):
        super(IncidenteForm, self).__init__(*args, **kwargs)
        from app.models import EmpresaExternos, CentroDistribucion
        with current_app.app_context():
            self.empresa_id.choices = [(empresa.id, empresa.nombre) for empresa in EmpresaTransporte.query.all()]
            self.centro_distribucion_id.choices = [(centro.id, centro.nombre) for centro in CentroDistribucion.query.all()]
