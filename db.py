import psycopg2 as db

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

    #insert
    def insert(self, *args):
        try:
            sql = "INSERT INTO autenticacao (chave, dominio, dtcriacao,base) VALUES (%s)"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Erro ao inserir ", e)

if __name__ == "__main__":
    sag = Sag()
    #sag.insert('2', 'semalo.com.br', '11/01/2022', 'D')



