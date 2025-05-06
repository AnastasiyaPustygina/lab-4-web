from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Optional

class UserForm(FlaskForm):
    id = HiddenField()
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[Optional()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[Optional()])
    role_id = SelectField('Роль', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')
