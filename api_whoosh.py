"""
Projeto de Implementação – Sistema Recuperação de Artigos

Teylor Moreto Guaitolini - 20191CECA70271
Matheus Corteletti Delfino - 20191CECA70212
"""


import os.path
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
import whoosh.index as index
from whoosh.qparser import QueryParser



schema = Schema(id=ID(stored=True), resumo=TEXT)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    indice = index.create_in("indexdir", schema)



class Whoosh:


    def __init__(self, id='', resumo=''):
        self.__id = id
        self.__resumo = resumo



    @property
    def id(self):
        return self.__id



    @id.setter
    def id(self, id):
        self.__id = id



    @property
    def resumo(self):
        return self.__resumo



    @resumo.setter
    def resumo(self, resumo):
        self.__resumo = resumo



    def indice(self):
        ix = index.open_dir('indexdir')

        writer = ix.writer()

        writer.add_document(id=u''+self.id, resumo=u''+self.resumo)

        writer.commit()



    def busca(self, parametro):

        ix = index.open_dir('indexdir')

        query = QueryParser('resumo', ix.schema).parse(u''+parametro)

        with ix.searcher() as s:

            results = s.search(query, limit=None)

            list_results = []

            for i in results:
                list_results.append(i['id'])

            return list_results