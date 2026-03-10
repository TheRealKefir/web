from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectMultipleField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobAddForm(FlaskForm):
    job = StringField("Description", validators=[DataRequired()])
    work_size = IntegerField("Work Size, h", validators=[DataRequired()])
    collaborators = SelectMultipleField("Collaborators")
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date")
    is_finished = BooleanField("Finished?")
    submit = SubmitField("Create")
