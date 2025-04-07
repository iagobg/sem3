import random
import time
import os

simbolos = ['🐴','🐸','🐵','🐶','🐯','🐺','🐢','🐰','🐴','🐸','🐵','🐶','🐯','🐺','🐢','🐰']
mesa = []
apostas = []
revelados = []

def criar_mesa():
    for i in range(0,4):
        mesa.append([])
        apostas.append([])
        for _ in range(0,4):
            num = random.randint(0,len(simbolos)-1)
            mesa[i].append(simbolos.pop(num))
            apostas[i].append('🛑')
    return


def mostrar_mesa(tabuleiro):
    limpar_tela()
    print("    1   2   3   4")
    for y in range(0,len(tabuleiro)):
        print(f'{y+1}',end='')
        for x in range(0,len(tabuleiro[y])):
            if (x,y) in revelados:
                print(f'  {mesa[y][x]}',end='')
            else:
                print(f'  {tabuleiro[y][x]}',end='')
        print('\n')
    return

def contagem():
    print('Memorize a posição dos bixos!')
    print('Contagem: ', end='')
    for i in range (10,0,-1):
        print (f'{i}... ',end='',flush=True)
        time.sleep(0.2)
    limpar_tela()
    return

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def chute():
    while True:
        try:
            chute = input('Qual quadrado você deseja revelar? (Número da Coluna,Número da Linha): ')
            chute = tuple(map(int, chute.split(',')))
            chute = (chute[0] - 1, chute[1] - 1)
            if len(chute) == 2 and all(0 <= num <= 3 for num in chute):
                if chute in revelados:
                    print('Quadrado já revelado')
                else:
                    print(f"Input válido: {chute}")
                    return chute
            else:
                print("Por favor, insira dois números entre 1 e 4 separados por vírgula.")
        except ValueError:
            print("Entrada inválida. Certifique-se de usar o formato correto: dois números separados por vírgula.")
            
def validar_chute(chute1,chute2):
    if mesa[chute1[1]][chute1[0]] == mesa[chute2[1]][chute2[0]]:
        print('Você acertou!')
        return True
    else:
        print('Os siímbolos são diferentes')
        return False

def gameloop():
    print('='*40)
    print('Jogo da Memória')
    print('='*40)
    criar_mesa()    
    mostrar_mesa(mesa)
    contagem()
    while len(revelados) < 16:
        mostrar_mesa(apostas)
        chute1 = chute()
        revelados.append(chute1)
        mostrar_mesa(apostas)
        chute2 = chute()
        revelados.append(chute2)
        if not validar_chute(chute1,chute2):
            revelados.pop()
            revelados.pop()
        time.sleep(2)
    print('Parabéns, você ganhou!')
    return


gameloop()