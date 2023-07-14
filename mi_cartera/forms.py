from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def date_le_today(form, field):
    if field.data > date.today():
        raise ValidationError("Must be lower than today")
    

def validaPwd(form, field):
    if field.data != form.pwd.data:
        raise ValidationError("Las contraseñas no coinciden")
    
class MovementForm(FlaskForm):
    date = DateField("Fecha", validators=[DataRequired("La Fecha es obligatoria"), date_le_today])
    abstract = StringField("Concepto", validators=[DataRequired("Concepto obligatorio"), Length(min=5, message="Debe tener al menos 5 caracteres")])
    amount = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])
    currency = SelectField("Moneda", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR", "Euros"), ("USD", "Dólares americanos")])

    submit = SubmitField("Enviar")

    def validate_date(self, field):
        if field.data > date.today():
            raise ValidationError("Must be lower than today (like a method)")

class RegisterForm(FlaskForm):
    user = StringField("Nombre de usuario", validators=[DataRequired()])
    pwd = StringField("Contraseña", validators=[DataRequired()])
    rpt_pwd = StringField("Repita Contraseña", validators=[DataRequired(), validaPwd])

    submit = SubmitField("Enviar")