from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EmergencyAccess(FlaskForm):
    astronaut_id = IntegerField('ID астронавта', validators=[DataRequired(), NumberRange(1)])
    astronaut_pass = PasswordField('Пароль астронавта', validators=[DataRequired()])
    captain_id = IntegerField('ID капитана', validators=[DataRequired(), NumberRange(1)])
    captain_pass = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')