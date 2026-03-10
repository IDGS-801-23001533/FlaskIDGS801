from . import cursos
from flask import render_template, request, redirect, url_for
from models import db, Cursos, Maestros, Alumnos, Inscripcion


@cursos.route("/CursosIndex", methods=["GET", "POST"])
def indexCursos():
    lista_cursos = Cursos.query.all()
    return render_template("cursos/CursosIndex.html", cursos=lista_cursos)


@cursos.route('/detallesCursos', methods=['GET', 'POST'])
def detallesCursos():
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Cursos).filter(Cursos.id == id).first()
        return render_template("cursos/Detalles.html", curso=curso)

@cursos.route('/InscribirCursos', methods=['GET', 'POST'])
def InsripcionesCursos():
    curso_id = request.args.get('curso_id')
    alumno_id = request.args.get('alumno_id')
    if alumno_id and curso_id:
        inscripcion = Inscripcion(
            alumno_id=int(alumno_id),
            curso_id=int(curso_id)
        )
        db.session.add(inscripcion)
        db.session.commit()
    subquery = db.session.query(Inscripcion.alumno_id).filter(
        Inscripcion.curso_id == curso_id
    )
    alumnos = Alumnos.query.filter(
        ~Alumnos.id.in_(subquery)
    ).all()
    return render_template(
        "cursos/Inscribir.html",
        alumnos=alumnos,
        curso_id=curso_id
    )

@cursos.route('/CrearCursos', methods=['GET', 'POST'])
def crearCursos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        maestro_id = request.form.get('maestro_id')
        alumnos_ids = request.form.getlist('alumnos')
        nuevo_curso = Cursos(
            nombre=nombre,
            descripcion=descripcion,
            maestro_id=maestro_id
        )
        db.session.add(nuevo_curso)
        db.session.flush() 
        for alumno_id in alumnos_ids:
            inscripcion = Inscripcion(
                alumno_id=int(alumno_id),
                curso_id=nuevo_curso.id)
            db.session.add(inscripcion)
        db.session.commit()
        return redirect(url_for('cursos.indexCursos'))
    maestros = Maestros.query.all()
    alumnos = Alumnos.query.all()
    return render_template("cursos/Agregar.html", maestros=maestros, alumnos=alumnos)


@cursos.route('/modificarCursos', methods=['GET', 'POST'])
def modificarCursos():
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Cursos).filter(Cursos.id == id).first()
        maestros = Maestros.query.all()
        alumnos = Alumnos.query.all()
        alumnos_inscritos = [a.id for a in curso.alumnos]
        return render_template("cursos/Modificar.html",
                               curso=curso,
                               maestros=maestros,
                               alumnos=alumnos,
                               alumnos_inscritos=alumnos_inscritos)

    if request.method == 'POST':
        id = request.form.get('id')
        curso = db.session.query(Cursos).filter(Cursos.id == id).first()
        curso.nombre = request.form.get('nombre')
        curso.descripcion = request.form.get('descripcion')
        curso.maestro_id = request.form.get('maestro_id')
        Inscripcion.query.filter_by(curso_id=curso.id).delete()
        alumnos_ids = request.form.getlist('alumnos')
        for alumno_id in alumnos_ids:
            inscripcion = Inscripcion(
                alumno_id=int(alumno_id),
                curso_id=curso.id)
            db.session.add(inscripcion)
        db.session.commit()
        return redirect(url_for('cursos.indexCursos'))

@cursos.route("/eliminarCursos", methods=['GET', 'POST'])
def eliminarCursos():
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Cursos).filter(Cursos.id == id).first()
        return render_template("cursos/Eliminar.html", curso=curso)

    if request.method == 'POST':
        id = request.form.get('id')
        curso = db.session.query(Cursos).filter(Cursos.id == id).first()
        if curso:
            Inscripcion.query.filter_by(curso_id=curso.id).delete()
            db.session.delete(curso)
            db.session.commit()
        return redirect(url_for('cursos.indexCursos'))
