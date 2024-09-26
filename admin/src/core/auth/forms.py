from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class registryForm(FlaskForm):

    email = EmailField("email", validators=[InputRequired(), Length(max=60)])
    alias = StringField("alias", validators=[InputRequired(), Length(max=15)])
    password = PasswordField(
        "password",
        validators=[
            InputRequired(),
            Length(min=3, max=255),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repetir contraseña")

