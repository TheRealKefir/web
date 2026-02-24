from flask import Flask, render_template

app = Flask(__name__)



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

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
