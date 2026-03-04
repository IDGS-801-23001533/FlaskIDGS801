
from . import alumnos
import forms
from flask import Flask, render_template, request, redirect, url_for
from models import db, Alumnos
from flask_wtf.csrf import CSRFProtect

@alumnos.route("/AlumnosIndex", methods=["GET", "POST"])
def indexAlumnos():
	create_form=forms.UserForm2(request.form)
	#la linea de abajo es como hacer un select * form alumnos
	alumno=Alumnos.query.all()
	return render_template("alumnos/AlumnosIndex.html", form=create_form, alumno=alumno)

@alumnos.route('/DetallesAlumnos',methods=['GET', 'POST'])
def detallesAlumnos():
	create_form=forms.UserForm2(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		#Select donde se busca solo por el ID
		alumn1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alumn1.nombre
		apaterno=alumn1.apaterno
		email=alumn1.email
		telefono=alumn1.telefono
		return render_template("Alumnos/Detalles.html", id = id, nombre = nombre, apaterno = apaterno, email = email, telefono=telefono)

@alumnos.route('/CrearAlumnos',methods=['GET','POST'])
def crearAlumnos():
	create_form=forms.UserForm2(request.form)
	if request.method=='POST':
		alum=Alumnos(	nombre=create_form.nombre.data,
						apaterno=create_form.apaterno.data,
					  	email=create_form.email.data,
						telefono=create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.indexAlumnos'))
	
	return render_template("Alumnos/Agregar.html")

@alumnos.route('/ModificarAlumnos',methods=['GET','POST'])
def modificarAlumnos():
	create_form=forms.UserForm2(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		#Select en base al id
		alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=str.rstrip(alum.nombre)
		create_form.apaterno.data=alum.apaterno
		create_form.email.data=alum.email
		create_form.telefono.data=alum.telefono
	if request.method=='POST':
		id=create_form.id.data
		alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum.id=id
		alum.nombre=str.rstrip(create_form.nombre.data)
		alum.apaterno=create_form.apaterno.data
		alum.email=create_form.email.data
		alum.telefono=create_form.telefono.data
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.indexAlumnos'))
	return render_template('Alumnos/Modificar.html', form=create_form)

@alumnos.route("/EliminarAlumnos", methods=['GET','POST'])
def eliminarAlumnos():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id =  request.args.get('id')
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum:
            create_form.id.data = alum.id
            create_form.nombre.data = alum.nombre
            create_form.apaterno.data = alum.apaterno
            create_form.email.data = alum.email
            create_form.telefono.data = alum.telefono
        return render_template("Alumnos/Eliminar.html", form = create_form)
        
    if request.method == 'POST':
        id =  create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum:
            db.session.delete(alum)
            db.session.commit()
        return redirect(url_for('alumnos.indexAlumnos'))
    return render_template("Alumnos/Eliminar.html", form = create_form)