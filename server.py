from flask import Flask, request
from db import Sag

sag = Sag()

app = Flask(__name__)

@app.route("/cadastro", methods =["POST"])
def cadastro():
    body = request.get_json()
    resultado = sag.insert(body["dominio"], body["base"])
    return resultado

@app.route("/consulta/<dominio>", methods=["GET"])
def consulta(dominio):   
    resultado = sag.consulta(dominio)
    return resultado

if __name__ == "__main__":
    app.run(debug=True)