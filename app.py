#python -m flask run --reload --debugger
from flask import Flask, redirect, url_for, render_template, request
from Analizador.grammar import parse

app = Flask(__name__)

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]
        global tmp_val
        tmp_val=inpt
        tmp_val = str(tmp_val).replace('||', '!!!')
        tmp_val = str(tmp_val).replace('global ', '')
        tmp_val = str(tmp_val).replace('local ', '')
        return redirect(url_for("output"))
    else:
        f = open("./entrada.txt", "r")
        entrada = f.read()
        return render_template('analyze.html', initial="")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/output')
def output():
    global tmp_val
    result = parse(tmp_val)
    return render_template('output.html', input=result)

if __name__ == "__main__":
    app.run()