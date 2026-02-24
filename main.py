from flask import Flask, render_template

app = Flask(__name__)

profs = [
    "инженер-исследователь",
    "пилот", "строитель", "экзобиолог", "врач", "инженер по терраформированию", "климатолог",
    "специалист по радиационной защите", "астрогеолог", "гляциолог", "инженер жизнеобеспечения", "метеоролог",
    "оператор марсохода"
]


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

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
