#python -m flask run --reload --debugger
from flask import Flask, redirect, url_for, render_template, request
from graphviz import dot
from Analizador.grammar import parse
import graphviz

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
        return render_template('analyze.html', initial="")

@app.route("/")
def home():
    return render_template("index.html")

headingsSimbolos = ("Entorno", "Nombre", "Tipo", "Valor", "Fila", "Columna")

@app.route('/output', methods=["POST", "GET"])
def output():
    global tmp_val
    result = parse(tmp_val)
    app.c = result[1]
    if request.method == "POST":
        return redirect(url_for("grafo"))
    else:
        return render_template('output.html', input=result[0], headings=headingsSimbolos, data=result[2])

@app.route('/grafo')
def grafo():
    dot = app.c
    return dot.pipe().decode('utf-8')

if __name__ == "__main__":
    app.run()