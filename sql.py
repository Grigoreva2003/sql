from data import db_session
from users import User
from flask import Flask, redirect, render_template
import datetime
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.fields.simple import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('db/mars_explorer.db')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField("Ваш возраст", validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'success'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        people = session.query(User).all()
        data = []

        for one in people:
            data.append(one.id)

        id = max(data) + 1

        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            surname=form.surname.data,
            speciality=form.speciality.data,
            position=form.position.data,
            hashed_password=form.password.data,
            address=form.address.data,
            id=id,
            modified_date=datetime.datetime.now()
        )

        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run()
