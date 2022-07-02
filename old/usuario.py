"""
Projeto de Implementação – Sistema Recuperação de Artigos

Teylor Moreto Guaitolini - 20191CECA70271
Matheus Corteletti Delfino - 20191CECA70212
"""


from banco import Banco
from procgen import is_cpf_valido, pausa
from arxiv import Arxiv
from api_whoosh import Whoosh
import os
import xmltodict
import csv



# -----------------------------------
# Abre o banco
# -----------------------------------
if not os.path.exists('banco.db'):
    db = Banco()
    db.create()
else:
    db = Banco()


class Usuario:


    def __init__(self, cpf='', senha=''):
        self.__cpf = cpf
        self.__senha = senha



    @property
    def cpf(self):
        return self.__cpf



    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf



    @property
    def senha(self):
        return self.__senha



    @senha.setter
    def senha(self, senha):
        self.__senha = senha



    def cadastro(self):
        """
        Cadastra um usuário
        :return: null
        """
        self.cpf = input('CPF: ')
        self.senha = input('Digite uma Senha: ')
        senha2 = input('Repita a Senha: ')

        if not is_cpf_valido(self.cpf):
            print('CPF Inválido')
        elif not (self.senha == senha2):
            print('As senhas não bateram.')
        else:
            db.select("SELECT * FROM usuarios WHERE PK_CPF={}".format(self.cpf))

            if not db.dados:

                db.insert("INSERT INTO usuarios (PK_CPF, Senha) VALUES (?, ?)", (self.cpf, self.senha))
                print('Cadastro Válido!')

            else:

                print("O CPF digitado já consta cadastrado no sistema!")



    def login(self):
        """
        Faz a verificação do login
        :return:True or False
        """
        self.cpf = input('CPF: ')
        self.senha = input('Senha: ')

        db.select("SELECT * FROM usuarios WHERE PK_CPF={}".format(self.cpf))

        for dados in db.dados:
            if (dados[0] == self.cpf) and (dados[1] == self.senha):
                return True

        print("CPF ou Senha inválidos!")
        pausa()

        return False



    def busca_arxiv(self):
        texto = input('Palavra chave para a consulta: ')
        quantidade = input('Quantidade de arquivos: ')
        arxiv = Arxiv(texto, quantidade)
        xml = arxiv.busca()
        doc = xmltodict.parse(xml)

        consultas = len(doc['feed']['entry'])

        if int(quantidade) == consultas:

            for i in range(consultas):

                id = doc['feed']['entry'][i]['id']
                titulo = doc['feed']['entry'][i]['title']
                resumo = doc['feed']['entry'][i]['summary']
                link = doc['feed']['entry'][i]['link'][-1]['@href']

                print('\n------------- ARTIGO {} -------------'.format(i+1))
                print('ID: ', id)
                print('Título: ', titulo)
                print('Resumo: ', resumo)
                print('Link: ', link)

                sqlstatement = "INSERT INTO artigos (PK_ID, Titulo, Resumo, Link, Consulta, FK_CPF) VALUES (?, ?, ?, ?, ?, ?)"

                db.insert(sqlstatement, (id, titulo, resumo, link, texto, self.cpf))

                whoosh = Whoosh(id, resumo)

                whoosh.indice()

        else:

            id = doc['feed']['entry']['id']
            titulo = doc['feed']['entry']['title']
            resumo = doc['feed']['entry']['summary']
            link = doc['feed']['entry']['link'][-1]['@href']

            print('\n------------- ARTIGO -------------')
            print('ID: ', id)
            print('Título: ', titulo)
            print('Resumo: ', resumo)
            print('Link: ', link)

            sqlstatement = "INSERT INTO artigos (PK_ID, Titulo, Resumo, Link, Consulta, FK_CPF) VALUES (?, ?, ?, ?, ?, ?)"

            db.insert(sqlstatement, (id, titulo, resumo, link, texto, self.cpf))

            whoosh = Whoosh(id, resumo)

            whoosh.indice()



    def listar_artigos(self):

        db.select("SELECT * FROM artigos WHERE FK_CPF={}".format(self.cpf))

        print('\nUsuário "{}" possui {} artigos cadastrados.'.format(self.cpf, len(db.dados)))

        for i, dados in enumerate(db.dados):
            print('\n------------- ARTIGO {} -------------'.format(i+1))
            print('ID: ', dados[0])
            print('Título: ', dados[1])
            print('Resumo: ', dados[2])
            print('Link: ', dados[3])

        print('\nDeseja exportar os dados dos artigos recuperados em um arquivo formato CSV? (Digite Sim para exportar)')

        if input('-> ').upper() == 'SIM':
            arq = open('artigos_recuperados.csv', 'w', newline='', encoding='utf-8')

            writer = csv.writer(arq, delimiter=';')

            for dados in db.dados:
                writer.writerow([dados[0], dados[1], dados[2], dados[3]])

            arq.close()

            print('\nO arquivo "artigos_recuperados.csv" foi gerado com sucesso!')



    def busca_local(self):

        parametro = input('Digite o parametro: ')

        whoosh = Whoosh()

        results = whoosh.busca(parametro)


        print('\nArtigos Recuperados: {}'.format(len(results)))

        id = ''
        titulo = ''
        resumo = ''
        link = ''

        for id in results:

            db.select("SELECT * FROM artigos WHERE PK_ID='{}'".format(id))

            for i, dados in enumerate(db.dados):

                id = db.dados[0][0]
                titulo = db.dados[0][1]
                resumo = db.dados[0][2]
                link = db.dados[0][3]

                print('\n------------- ARTIGO {} -------------'.format(i + 1))
                print('ID: ', id)
                print('Título: ', titulo)
                print('Resumo: ', resumo)
                print('Link: ', link)


        print(
            '\nDeseja exportar os dados dos artigos recuperados em um arquivo formato CSV? (Digite Sim para exportar)')


        if input('-> ').upper() == 'SIM':
            arq = open('artigos_recuperados.csv', 'w', newline='', encoding='utf-8')

            writer = csv.writer(arq, delimiter=';')

            writer.writerow([id, titulo, resumo, link])

            arq.close()

            print('\nO arquivo "artigos_recuperados.csv" foi gerado com sucesso!')