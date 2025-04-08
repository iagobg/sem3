import random
import time
import os
import json
import datetime


simbolos = ['🐴','🐸','🐵','🐶','🐯','🐺','🐢'  ,'🐰']*2


pontos = 0
mesa = []
apostas = []
revelados = []
nome = ''
rankings = []
tempo_comeco = 0
duracao = 0

def criar_mesa():
    for i in range(0,4):
        mesa.append([])
        apostas.append([])
        for _ in range(0,4):
            num = random.randint(0,len(simbolos)-1)
            mesa[i].append(simbolos.pop(num))
            apostas[i].append('🛑')
    return

def iniciar_jogo():
    global nome, tempo_comeco
    carregar_rankings()
    tempo_comeco = datetime.datetime.now()
    criar_mesa()
    nome = input('Qual o seu nome? ')
    print(f'Olá {nome}, bem-vindo ao jogo da memória!')
    return

def salvar_rankings():
    print(rankings)
    try:
        with open('rankings.json', 'w') as arquivo:
            json.dump(rankings, arquivo)
    except Exception as e:
        print(f"Erro ao salvar os rankings: {e}")
    return

def carregar_rankings():
    global rankings
    try:
        with open('rankings.json', 'r') as arquivo:
            rankings = json.load(arquivo)
    except FileNotFoundError:
        rankings = []
    except Exception as e:
        print(f"Erro ao carregar os rankings: {e}")

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
    global revelados
    while True:
        try:
            chute = input('Qual quadrado você deseja revelar? (Número da Coluna,Número da Linha): ')
            chute = tuple(map(int, chute.split(',')))
            chute = (chute[0] - 1, chute[1] - 1)
            if len(chute) == 2 and all(0 <= num <= 3 for num in chute):
                if chute in revelados:
                    print('Quadrado já revelado')
                else:                
                    revelados.append(chute)
                    mostrar_mesa(apostas)
                    return chute
            else:
                print("Por favor, insira dois números entre 1 e 4 separados por vírgula.")
        except ValueError:
            print("Entrada inválida. Certifique-se de usar o formato correto: dois números separados por vírgula.")
            
def validar_chute(chute1,chute2):
    global pontos, revelados
    if mesa[chute1[1]][chute1[0]] == mesa[chute2[1]][chute2[0]]:
        print('Você acertou! 10 pontos!')
        pontos += 10
        return
    else:
        print('Os siímbolos são diferentes, você perdeu 5 pontos!')	
        pontos -= 5
        revelados = revelados[:-2]
        return
    
def apostar():
    mostrar_mesa(apostas)
    chute1 = chute()
    chute2 = chute()
    validar_chute(chute1,chute2)
    time.sleep(2)
    return

def finalizar_jogo():
    global nome, rankings, pontos, duracao
    duracao = datetime.datetime.now() - tempo_comeco
    duracao = round(duracao.total_seconds(),2)
    print(f'Você fez {pontos} pontos em {duracao} segundos!')
    rankings.append((nome,pontos,duracao))
    time.sleep(2)
    limpar_tela()
    salvar_rankings()
    mostrar_rankings()
    print('Fim de jogo!')
    return

def mostrar_rankings():
    global rankings
    rankings_ordenados = sorted(rankings, key=lambda x: x[1], reverse=True)
    print("Rankings:")
    print('='*40)
    for i, (nome, pontos,duracao) in enumerate(rankings_ordenados, start=1):
        print(f"{i}. {nome}: {pontos} pontos - {duracao} segundos")
    print('='*40)
    return


def gameloop():
    iniciar_jogo()
    global mesa, apostas, revelados, pontos
    print('='*40)
    print('Jogo da Memória')
    print('='*40)
    mostrar_mesa(mesa)
    contagem()
    while len(revelados) < 16:
        apostar()
    finalizar_jogo()
    return



gameloop()