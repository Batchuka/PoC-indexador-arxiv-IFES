"""
Projeto de Implementação – Sistema Recuperação de Artigos

Teylor Moreto Guaitolini - 20191CECA70271
Matheus Corteletti Delfino - 20191CECA70212
"""


from procgen import clear, menu1, pausa, menu2
from usuario import Usuario


usuario = Usuario()

# -----------------------------------
# Laço principal
# -----------------------------------
while True:
    clear()

    opcao_menu1 = menu1()

    if opcao_menu1 == "1":
        logado = usuario.login()

        while logado:
            clear()

            opcao_menu2 = menu2()

            if opcao_menu2 == "1":
                usuario.busca_arxiv()
                pausa()

            elif opcao_menu2 == "2":
                usuario.busca_local()
                # print('Não Implementado totalmente.')
                pausa()

            elif opcao_menu2 == "3":
                usuario.listar_artigos()
                pausa()

            elif opcao_menu2 == "4":
                exit()

            else:
                pausa('A opção deve ser de 1-4! Pressione Enter para continuar...')


    elif opcao_menu1 == "2":
        usuario.cadastro()
        pausa()


    else:
        pausa('A opção deve ser 1 ou 2! Pressione Enter para continuar...')