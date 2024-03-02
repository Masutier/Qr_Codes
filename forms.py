from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import InputRequired, Length

class QrCodeForm(FlaskForm):
    address = StringField('Dirección Web', validators=[InputRequired(), Length(min=15, max=200)])
    fileName = StringField('Nommbre Final .png', validators=[InputRequired(), Length(min=5, max=100)])

    box_size = IntegerField('Tamaño de Caja', validators=[InputRequired()])
    border = StringField('Tamaño del Border', validators=[InputRequired()])
    fill = StringField('Color de Pixel', validators=[InputRequired(), Length(min=8, max=100)])
    back_color = StringField('Color de Fondo', validators=[InputRequired(), Length(min=8, max=100)])

    # imgcenter
