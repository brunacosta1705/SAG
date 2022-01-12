from flask import Flask, request

from db import Sag

app = Flask(__name__)

@app.route("/")
def homepage():
    return "TESTEE"

@app.route("/cadastro", methods =["POST"])
def cadastro():
    body = request.get_json()
    print(body)
    return body
    
@app.route("/consulta/<dominio>", methods=["GET"])
def consulta(dominio):   
    sag = Sag()  
    resultado = sag.consulta(dominio)
    
    return resultado

if __name__ == "__main__":
    app.run(debug=True)