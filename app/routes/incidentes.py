from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.forms import IncidenteForm
from app.models import db, Incidente
from sqlalchemy import func
from reports.incidentes.report_pdf import pdf_incidentes
from reports.incidentes.report_excel import excel_incidentes

bp = Blueprint('incidentes', __name__, url_prefix='/incidentes')

@bp.route('reporte/pdf')
def reporte_pdf():
    return pdf_incidentes()

@bp.route('reporte/excel')
def report_excel():
    return excel_incidentes

@bp.route('/')
def index():
    if request.method == 'POST':
        rut = request.form.get('rut', '').strip()
        nombre = request.form.get('nombre', '').strip()

        query = Incidente.query
        if rut:
            query = query.filter(Incidente.rut.ilike(f'%{rut}%'))
        if nombre:
            query = query.filter(Incidente.nombre_conductor.ilike(f'%{nombre}%'))
        incidentes = query.all()
    
    else:
        incidentes = Incidente.query.all()
        
    return render_template('incidentes/admin.html', incidentes=incidentes)

@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Ruta para registrar un nuevo incidente"""
    form = IncidenteForm()
    if form.validate_on_submit():
        nuevo_incidente = Incidente(
            rut=form.rut.data,
            nombre_conductor=form.nombre_conductor.data,
            patente_camion=form.patente_camion.data,
            fecha_incidente=form.fecha_incidente.data,
            lugar_incidente=form.lugar_incidente.data,
            tipo_incidente=form.tipo_incidente.data,
            detalles_incidente=form.detalles_incidente.data,
            empresa_id=form.empresa_id.data,
            centro_distribucion_id=form.centro_distribucion_id.data
        )
        db.session.add(nuevo_incidente)
        db.session.commit()
        flash('Incidente registrado correctamente', 'success')
        return redirect(url_for('incidentes.index'))
    return render_template('incidentes/formulario.html', form=form)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Ruta para editar un incidente existente"""
    incidente = Incidente.query.get_or_404(id)
    form = IncidenteForm(obj=incidente)
    if form.validate_on_submit():
        incidente.rut = form.rut.data
        incidente.nombre_conductor = form.nombre_conductor.data
        incidente.patente_camion = form.patente_camion.data
        incidente.fecha_incidente = form.fecha_incidente.data
        incidente.lugar_incidente = form.lugar_incidente.data
        incidente.tipo_incidente = form.tipo_incidente.data
        incidente.detalles_incidente = form.detalles_incidente.data
        incidente.empresa_id = form.empresa_id.data
        incidente.centro_distribucion_id = form.centro_distribucion_id.data
        db.session.commit()
        flash('Incidente actualizado correctamente', 'success')
        return redirect(url_for('incidentes.index'))
    return render_template('incidentes/formulario.html', form=form, incidente=incidente)

@bp.route('/graficos', methods=['GET'])
def graficos():
    """Ruta para generar datos de gráficos de incidentes"""
    data = db.session.query(
        Incidente.tipo_incidente, func.count(Incidente.id)
    ).group_by(Incidente.tipo_incidente).all()

    # Preparar datos para Chart.js
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    return jsonify({'labels': labels, 'counts': counts})