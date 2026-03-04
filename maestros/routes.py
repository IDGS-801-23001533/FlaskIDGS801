from . import maestros
import forms
from flask import Flask, render_template, request, redirect, url_for
from models import db, Maestros
from flask_wtf.csrf import CSRFProtect

@maestros.route("/MaestrosIndex", methods=["GET", "POST"])
def indexMaestros():
	create_form=forms.UserForm3(request.form)
	#la linea de abajo es como hacer un select * form alumnos
	maestro=Maestros.query.all()
	return render_template("maestros/MaestrosIndex.html", form=create_form, maestro=maestro)

@maestros.route('/detallesMaestros',methods=['GET', 'POST'])
def detallesMaestros():
	create_form=forms.UserForm3(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		#Select donde se busca solo por el ID
		maes = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		matricula=request.args.get('matricula')
		nombre=maes.nombre
		apellidos=maes.apellidos
		especialidad=maes.especialidad
		email=maes.email
		return render_template("Maestros/Detalles.html", matricula = matricula, nombre = nombre, apellidos = apellidos, email = email, especialidad=especialidad)

@maestros.route('/CrearMaestros',methods=['GET','POST'])
def crearMaestros():
	create_form=forms.UserForm3(request.form)
	if request.method=='POST':
		maes=Maestros(	nombre=create_form.nombre.data,
						apellidos=create_form.apellidos.data,
						especialidad=create_form.especialidad.data,
						email=create_form.email.data)
		db.session.add(maes)
		db.session.commit()
		return redirect(url_for('maestros.indexMaestros'))
	
	return render_template("maestros/Agregar.html")

@maestros.route('/modificarMaestros',methods=['GET','POST'])
def modificarMaestros():
	create_form=forms.UserForm3(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		#Select en base al matricula
		maes = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=str.rstrip(maes.nombre)
		create_form.apellidos.data=maes.apellidos
		create_form.especialidad.data=maes.especialidad
		create_form.email.data=maes.email
	if request.method=='POST':
		matricula=create_form.matricula.data
		maes = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		maes.matricula=matricula
		maes.nombre=str.rstrip(create_form.nombre.data)
		maes.apellidos=create_form.apellidos.data
		maes.especialidad=create_form.especialidad.data
		maes.email=create_form.email.data
		db.session.add(maes)
		db.session.commit()
		return redirect(url_for('maestros.indexMaestros'))
	return render_template('maestros/Modificar.html', form=create_form)

@maestros.route("/eliminarMaestros", methods=['GET','POST'])
def eliminarMaestros():
    create_form = forms.UserForm3(request.form)
    if request.method == 'GET':
        matricula =  request.args.get('matricula')
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes:
            create_form.matricula.data = maes.matricula
            create_form.nombre.data = maes.nombre
            create_form.apellidos.data = maes.apellidos
            create_form.especialidad.data = maes.especialidad
            create_form.email.data = maes.email
        return render_template("maestros/Eliminar.html", form = create_form)
        
    if request.method == 'POST':
        matricula =  create_form.matricula.data
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes:
            db.session.delete(maes)
            db.session.commit()
        return redirect(url_for('maestros.indexMaestros'))
    return render_template("maestros/Eliminar.html", form = create_form)