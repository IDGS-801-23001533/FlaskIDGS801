from config import DevelopmentConfig
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from flask_migrate import Migrate

from config import DevelopmentConfig
import forms
from models import db, Alumnos
from maestros.routes import maestros
from alumnos.routes import alumnos


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
db.init_app(app)
csrf=CSRFProtect(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
	return render_template("index.html")

if __name__ == '__main__':
	csrf.init_app(app)

	with app.app_context():
		db.create_all()
	app.run()
