from typing import Counter
import psycopg2 as db
from flask import jsonify

from datetime import datetime

class Config:
    def __init__(self):
        self.config = {
            "postgres" :{
                "user": "postgres",
                "password" : "senha123",
                "host" : "localhost",
                "port" : "5432", 
                "database" : "sag"
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()

        except Exception as e:
            print("Erro na conexão ", e)
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn
    
    @property
    def cursor(self):
        return self.cur
    
    def commit(self):
        self.connection.commit()
    
    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
    
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

class Sag(Connection):
    def __init__(self):
        Connection.__init__(self)

    #cadastro
    #/cadastro/
    def insert(self,dominio,base):
        try:
            #CONSULTA A EMPRESA NO BANCO E RETORNA A LISTA VAZIA SE NAO EXISTIR E COM VALOR SE EXISTIR
            sql = f"select chave from autenticacao where dominio = '" + dominio + "'"
            consulta = self.query(sql)

            #EMPRESA JÁ EXISTE NO BANCO
            if len(consulta) >= 1:
                return {"status" : "0",
                        "mensagem" : "Dominio já existente " + dominio}

            #EMPRESA NAO EXISTE , VAI INSERIR
            elif len(consulta) == 0:
                data = datetime.today().strftime('%Y-%m-%d')

                sql = f"INSERT INTO autenticacao (dominio, dtcriacao,base) VALUES ('" + dominio + "','" + data + "','" + base + "')"
                self.execute(sql)
                self.commit()
                return {"status" : "1", 
                        "mensagem" : "Empresa inserida com sucesso"}  

        except Exception as e:
            return {"status":"-1", "consulta" : consulta}

    #consulta empresa
    #/consulta/dominio
    def consulta(self,dominio):
        try:   
            sql = f"select case when (dtcriacao+INTERVAL'30 days') > CURRENT_DATE then '1' else '0' end from autenticacao where dominio = '" + dominio +"'"
            status_empresa = self.query(sql)
            return {"status": status_empresa[0][0]}

        except Exception as e:
           return {"status":"-1",
           "mensagem" : "Dominio nao encontrado"}

#if __name__ == "__main__":