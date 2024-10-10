from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, FloatField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BillingForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    jya_id = IntegerField('JYA ID', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField('Payment Method', choices=[
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de Credito', 'Tarjeta de Credito'),
        ('Tarjeta de Debito', 'Tarjeta de Debito'),
        ('Otro', 'Otro')
    ], validators=[DataRequired()])
    payment_date = DateField('Payment Date', validators=[DataRequired()])
    observation = StringField('Observation', validators=[])
    submit = SubmitField('Submit')