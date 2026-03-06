from flask import Flask, render_template, redirect
from forms import EmergencyAccess

app = Flask(__name__)

profs = [
    "инженер-исследователь",
    "пилот", "строитель", "экзобиолог", "врач", "инженер по терраформированию", "климатолог",
    "специалист по радиационной защите", "астрогеолог", "гляциолог", "инженер жизнеобеспечения", "метеоролог",
    "оператор марсохода"
]
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

title = input()
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title=title)

@app.route('/training/<prof>')
def training(prof):
    print(prof)
    context = {
        "title": title,
        prof: prof
    }
    return render_template('train.html', **context)

@app.route('/list_prof/<type>')
def list_prof(type):
    context = {
        "title": title,
        "type": type,
        "profs": profs
    }
    return render_template('list_profs.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = EmergencyAccess()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/success')
def success():
    return render_template('success.html')




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
