from geral.cripto import *

# teste da cifra utilizada na senha dos usuários
def run():
    senha = '12345'
    cifrado = cifrar(senha)
    print("senha cifrada: " + cifrado)
    print("senha salva é igual à senha cifrada?")
    print(valida_senha(cifrado, senha))
