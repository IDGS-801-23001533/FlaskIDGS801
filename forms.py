from wtforms import Form, StringField
from wtforms import SearchField,IntegerField,PasswordField,FloatField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):

    nombre=StringField('nombre',[
    validators.DataRequired(message="E que rollo, no lo dejes vacio W"),
    validators.length(min=4, max=20, message="Requiere minimo 4 caracteres (mamaste ana)")
    ])

    apaterno=StringField("apaterno",[
        validators.DataRequired(message="E que rollo, no lo dejes vacio W"),
        validators.Length(min=3, max=10, message="Eso no es un apellido jefe no diga mmds")
    ])

    email=EmailField("email",[
        validators.DataRequired(message="E que rollo, no lo dejes vacio W"),
        validators.email(message="Eso no es un correo padrino, metele @ y .com minimo")
    ])