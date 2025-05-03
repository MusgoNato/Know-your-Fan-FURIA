import sqlite3

class DataBase:
    _instance = None
    _conn = None

    def __new__(cls, db_file='know_your_fan.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Conecta ao banco, desativando a cheagem de treahds, sendo possivel a implementação de uma unica conexao ao banco em varios lugares
            cls._conn = sqlite3.connect(db_file, check_same_thread=False)
        return cls._instance
    
    def create_table(self):
        cursor = self.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                email TEXT,
                endereco TEXT,
                idade TEXT,
                cpf TEXT UNIQUE,
                interesses TEXT,
                atividades TEXT,
                eventos TEXT,
                compras TEXT,
                user_photo TEXT
            )
        ''')
        self.commit()


    def insert_user(self, nome, email, endereco, idade, cpf, interesses, atividades, eventos, compras, user_photo):
        cursor = self.cursor()
        cursor.execute('''
            INSERT INTO fans (nome, email, endereco, idade, cpf, interesses, atividades, eventos, compras, user_photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, email, endereco, idade, cpf, interesses, atividades, eventos, compras, user_photo))
        self.commit()

        print("Novo usuario no banco de dados!")


    @property
    def connection(self):
        return self._conn

    def cursor(self):
        return self._conn.cursor()

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()
        DataBase._instance = None
        DataBase._conn = None
