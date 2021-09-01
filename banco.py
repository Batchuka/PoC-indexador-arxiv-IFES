"""
Projeto de Implementação – Sistema Recuperação de Artigos

Teylor Moreto Guaitolini - 20191CECA70271
Matheus Corteletti Delfino - 20191CECA70212
"""


import sqlite3


class Banco:
    def __init__(self):
        self.conn = sqlite3.connect("banco.db")



    def __del__(self):
        self.conn.close()



    def create(self):
        """Cria as tabelas no banco de dados"""
        self.__cursor = self.conn.cursor()
        try:
            sqlstatement = "CREATE TABLE usuarios(PK_CPF VARCHAR(11) NOT NULL PRIMARY KEY, Senha VARCHAR(32) NOT NULL);"
            self.__cursor.execute(sqlstatement)

            sqlstatement = "CREATE TABLE artigos(PK_ID TEXT(255), Titulo TEXT(255), Resumo TEXT(255), Link TEXT(255), Consulta TEXT(255), FK_CPF VARCHAR(11), FOREIGN KEY (FK_CPF) REFERENCES usuarios(PK_CPF));"
            self.__cursor.execute(sqlstatement)
        except sqlite3.OperationalError:
            # print Exception.
            print("Erro. Verifique seu SQL")

        self.conn.commit()



    def insert(self, sqlstatement, dados):
        """Insere registros no banco de dados"""
        self.__cursor = self.conn.cursor()
        try:
            self.__cursor.execute(sqlstatement, dados)
        except sqlite3.OperationalError:
            print("Erro. Verifique seu SQL")

        self.conn.commit()



    def select(self, sqlstatement):
        """Seleciona registros do banco de dados"""
        self.__cursor = self.conn.cursor()

        try:
            self.__cursor.execute(sqlstatement)
        except sqlite3.OperationalError:
            print("Erro. Verifique seu SQL")

        self.dados = self.__cursor.fetchall()