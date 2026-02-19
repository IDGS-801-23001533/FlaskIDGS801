from config import DevelopmentConfig
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g

from config import DevelopmentConfig
import forms
from models import db, Alumnos


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf=CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route("/")
@app.route("/index")
def index():
	create_form=forms.UserForm2(request.form)
	#la linea de abajo es como hacer un select * form alumnos
	alumno=Alumnos.query.all()
	return render_template("index.html", form=create_form, alumno=alumno)

@app.route('/detalles',methods=['GET', 'POST'])
def detalles():
	create_form=forms.UserForm2(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		#Select donde se busca solo por el ID
		alumn1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alumn1.nombre
		apaterno=alumn1.apaterno
		email=alumn1.email
		return render_template("Detalles.html", id = id, nombre = nombre, apaterno = apaterno, email = email)

@app.route('/alumnos',methods=['GET','POST'])
def alumnos():
	create_form=forms.UserForm2(request.form)
	if request.method=='POST':
		alum=Alumnos(	nombre=create_form.nombre.data,
						apaterno=create_form.apaterno.data,
					  	email=create_form.email.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('index'))
	
	return render_template("Alumnos.html")

@app.route('/modificar',methods=['GET','POST'])
def modificar():
	create_form=forms.UserForm2(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		#Select en base al id
		alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=str.rstrip(alum.nombre)
		create_form.apaterno.data=alum.apaterno
		create_form.email.data=alum.email
	if request.method=='POST':
		id=create_form.id.data
		alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum.id=id
		alum.nombre=str.rstrip(create_form.nombre.data)
		alum.apaterno=create_form.apaterno.data
		alum.email=create_form.email.data
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('Modificar.html', form=create_form)


if __name__ == '__main__':
	csrf.init_app(app)

	with app.app_context():
		db.create_all()
	app.run()
