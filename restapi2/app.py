from data import db_session
from data.users import User
from flask import Flask, request, make_response, redirect, render_template, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_restful import Api
from forms.user import RegisterForm
from data.jobs import Jobs
import users_api


app = Flask(__name__)
api = Api(app)
api.add_resource(users_api.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(users_api.UsersListResource, '/api/v2/users')

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('login.html',
#                                message="Неправильный логин или пароль",
#                                form=form)
#     return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = ... #JobAddForm()
    db_sess = db_session.create_session()
    form.collaborators.choices = [(u.id, str(u)) for u in db_sess.query(User).all() if u.id != current_user.id]
    if form.validate_on_submit():
        # print([k, v.data) for k, v in form._fields.items()])
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=' ,'.join(form.collaborators.data),
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
            team_leader=current_user.id

        )
        db_sess.add(job)
        db_sess.commit()

        flash('Работа загружена')
        return redirect('/')
    return render_template('add_job.html', title='Добавление формы', form=form)



if __name__ == 'main':
    app.run()