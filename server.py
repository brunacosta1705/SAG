from flask import Flask, request, json, Response
from db import Sag

sag = Sag()

app = Flask(__name__)

@app.route("/cadastro", methods =["POST"])
def cadastro():
    body = request.get_json()
    resultado = sag.insert(body["dominio"], body["base"])

    status_http = Response()

    return {"status_code" : status_http.status_code,
            "resposta" : resultado}

@app.route("/consulta/<dominio>", methods=["GET"])
def consulta(dominio): 

    resultado = sag.consulta(dominio)
    status_http = Response()


    return {"status_code" : status_http.status_code,
            "resposta" : resultado}

if __name__ == "__main__":
    app.run(debug=True)