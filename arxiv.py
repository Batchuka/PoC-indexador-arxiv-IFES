"""
Projeto de Implementação – Sistema Recuperação de Artigos

Teylor Moreto Guaitolini - 20191CECA70271
Matheus Corteletti Delfino - 20191CECA70212
"""


import urllib, urllib.request


class Arxiv:


    def __init__(self, texto, quantidade):
        self.__texto = texto
        self.__quantidade = quantidade


    @property
    def texto(self):
        return self.__texto


    @texto.setter
    def texto(self, texto):
        self.__texto = texto


    @property
    def quantidade(self):
        return self.__quantidade


    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade


    def busca(self):
        url = 'http://export.arxiv.org/api/query?search_query=ti:'+self.__texto+'&start=0&max_results='+self.__quantidade+''
        data = urllib.request.urlopen(url)
        xml = data.read().decode('utf-8')
        return xml