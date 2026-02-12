from wtforms import Form, StringField
from wtforms import SearchField,IntegerField,PasswordField,FloatField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    matricula=IntegerField("id",[
        validators.number_range(min=1, max=20, message="Papi hablo en chino o que? Nomas entre 1 y 20")
    ])

    nombre=StringField('nombre',[
    validators.DataRequired(message="E que rollo, no lo dejes vacio W"),
    validators.length(min=4, max=20, message="Requiere minimo 4 caracteres (mamaste ana)")
    ])

    apa=StringField("Apaterno",[
        validators.DataRequired(message="E que rollo, no lo dejes vacio W"),
        validators.Length(min=3, max=10, message="Eso no es un apellido jefe no diga mmds")
    ])

    email=EmailField("Correo",[
        validators.DataRequired(message="E que rollo, no lo dejes vacio W"),
        validators.email(message="Eso no es un correo padrino, metele @ y .com minimo")
    ])