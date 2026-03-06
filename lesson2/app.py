from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



@app.route("/")
def index():
    jobs = db_session.create_session().query(Jobs).all()
    return render_template("index.html", jobs=jobs)


if __name__ == '__main__':
    db_session.global_init('./db/testdb.sqlite')
    app.run()

