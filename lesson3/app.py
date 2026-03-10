from data import db_session
from flask import redirect, render_template, flash, get_flashed_messages
from data.users import User, LoginForm
from flask import Flask, request, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms.jobs import JobAddForm
from data.jobs import Jobs
from data.users import User
from lesson2.register import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
def index():
    all_jobs = db_session.create_session().query(Jobs).all()
    return render_template('index.html', jobs=all_jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
    session = db_session.create_session()
    forms = JobAddForm()
    forms.collaborators.choices = [(us.id, str(us))
                                   for us in session.query(User).all()
                                   if us != current_user]
    if forms.validate_on_submit():
        job = Jobs(
            job=forms.job.data,
            work_size=forms.work_size.data,
            collaborators=', '.join(forms.collaborators.data),
            start_date=forms.start_date.data,
            end_date=forms.end_date.data,
            is_finished=forms.is_finished.data,
            team_leader=current_user.id
        )
        session.add(job)
        session.commit()
        session.close()
        flash("The work was successfully added!")
        return redirect('/')
    return render_template('add_job.html', title="Add Job", form=forms)


if __name__ == '__main__':
    db_session.global_init('./db/mass_explorer.db')

    app.run()
