from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ..forms import HallazgoForm
from app.models import db, Hallazgo, EmpresaExternos, CentroDistribucion
from sqlalchemy import func
from reports.hallazgos.report_pdf import pdf_hallazgos
from reports.hallazgos.report_excel import excel_hallazgos

bp = Blueprint('hallazgos', __name__, url_prefix='/hallazgos')

@bp.route('/reporte/pdf')
def reporte_pdf():
    return pdf_hallazgos()

@bp.route('/reporte/excel')
def reporte_excel():
    return excel_hallazgos()

@bp.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        rut = request.form.get('rut', '').strip()
        nombre = request.form.get('nombre', '').strip()

        query = Hallazgo.query
        if rut:
            query = query.filter(Hallazgo.rut.ilike(f'%{rut}%'))
        if nombre:
            query = query.filter(Hallazgo.nombre_completo.ilike(f'%{nombre}%'))
        hallazgo = query.all()
    
    else:
        hallazgos = Hallazgo.query.all()
        
    return render_template('hallazgos/admin.html', hallazgos=hallazgos)

@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Ruta para registrar un nuevo hallazgo"""
    form = HallazgoForm()
    if form.validate_on_submit():
        nuevo_hallazgo = Hallazgo(
            rut=form.rut.data,
            nombre_completo=form.nombre_completo.data,
            area=form.area.data,
            fecha=form.fecha.data,
            motivo_desvinculacion=form.motivo_desvinculacion.data,
            empresa_id=form.empresa_id.data,
            centro_distribucion_id=form.centro_distribucion_id.data
        )
        db.session.add(nuevo_hallazgo)
        db.session.commit()
        flash('Hallazgo registrado correctamente', 'success')
        return redirect(url_for('hallazgos.index'))
    return render_template('hallazgos/formulario.html', form=form)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Ruta para editar un hallazgo existente"""
    hallazgo = Hallazgo.query.get_or_404(id)
    form = HallazgoForm(obj=hallazgo)
    if form.validate_on_submit():
        hallazgo.rut = form.rut.data
        hallazgo.nombre_completo = form.nombre_completo.data
        hallazgo.area = form.area.data
        hallazgo.fecha = form.fecha.data
        hallazgo.motivo_desvinculacion = form.motivo_desvinculacion.data
        hallazgo.empresa_id = form.empresa_id.data
        hallazgo.centro_distribucion_id = form.centro_distribucion_id.data
        db.session.commit()
        flash('Hallazgo actualizado correctamente', 'succes')
        return redirect(url_for('hallazgos.index'))
    return render_template('hallazgos/formulario.html', form=form, hallazgo=hallazgo)

@bp.route('/graficos', methods=['GET'])
def graficos():
    """Ruta para generar datos de gráficos de hallazgos"""
    data = db.session.query(
        Hallazgo.motivo_desvinculacion, func.count(Hallazgo.id)
    ).group_by(Hallazgo.motivo_desvinculacion).all()

    #Preparar datos para Chart.js
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    return jsonify({'labels': labels, 'counts': counts})
