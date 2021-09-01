"""
Projeto de Implementação – Sistema Recuperação de Artigos

Teylor Moreto Guaitolini - 20191CECA70271
Matheus Corteletti Delfino - 20191CECA70212
"""


def clear():
    """Limpa a tela
    """
    print('\n'*100)


def pausa(mensagem="Pressione Enter para continuar..."):
    """Executa uma pausa, tem como opcional uma mensagem
    """
    print("")
    input(mensagem)


def is_cpf_valido(cpf: str) -> bool:
    if len(cpf) != 11:
        return False

    if cpf in (c * 11 for c in "1234567890"):
        return False

    cpf_reverso = cpf[::-1]
    for i in range(2, 0, -1):
        cpf_enumerado = enumerate(cpf_reverso[i:], start=2)
        dv_calculado = sum(map(lambda x: int(x[1]) * x[0], cpf_enumerado)) * 10 % 11
        if cpf_reverso[i - 1:i] != str(dv_calculado % 10):
            return False

    return True


def menu1():
    print("SISTEMA RECUPERAÇÃO DE ARTIGOS")
    print("1 – Efetuar Login")
    print("2 – Cadastrar Novo Usuário")
    opcao = input("DIGITE SUA OPÇÃO: ")
    return opcao


def menu2():
    print("SISTEMA RECUPERAÇÃO DE ARTIGOS")
    print("1 – REALIZAR BUSCA ARXIV")
    print("2 – REALIZAR BUSCA LOCAL")
    print("3 – LISTAR ARTIGOS")
    print("4 – SAIR")
    opcao = input("DIGITE SUA OPÇÃO: ")
    return opcao