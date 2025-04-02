import random
import time
import sys

naipes = ['♠', '♥', '♦', '♣']
extras = ['J','Q','K','A']


def monta_baralho():
    baralho = []
    for i in range(2,11):
        for naipe in naipes:
            baralho.append(str(i)+naipe)
    for extra in extras:
        for naipe in naipes:
            baralho.append(extra+naipe)
    return baralho

baralho = monta_baralho()


cartas_jogador = []
cartas_mesa = []
mesa_parada = False
jogador_parado = False

    
def pontos_carta(carta):
    if (carta[0:2] == '10'):
        valor = 10
    elif carta[0].isdigit():
        valor = int(carta[0])
    elif(carta[0] == 'A'):
        valor = 11
    else:
        valor = 10
    return valor

def pontos_mao(cartas):
    pontos = 0
    ases = 0
    for carta in cartas:
        if carta[0] == 'A':
            ases += 1
        pontos += pontos_carta(carta)
    while pontos > 21 and ases > 0:
        pontos -= 10
        ases -= 1
    return pontos


def sacar(mao,pessoa):
    num = random.randint(0,len(baralho)-1)
    mao.append(baralho.pop(num))
    print(f'{pessoa} sacou {mao[-1]}')
    time.sleep(2)
    return 


def checar_blackjack(cartas):
    if len(cartas) == 2 and pontos_mao(cartas) == 21:
        return True
    else:
        return False
    

def avaliar():
    jogador = pontos_mao(cartas_jogador)
    mesa = pontos_mao(cartas_mesa)
    if jogador == mesa:
        return 'Empate'
    elif jogador >= mesa:
        return 'Jogador'
    else:
        return 'Mesa'
    
def estourou(cartas):
    if pontos_mao(cartas) > 21:
        return True
    else:
        return False

def fim_de_jogo():
    if checar_blackjack(cartas_jogador) or checar_blackjack(cartas_mesa):
        if checar_blackjack(cartas_jogador) and checar_blackjack(cartas_mesa):
            print('Ambos jogadores tiraram um blackjack! Empate!')
        elif checar_blackjack(cartas_jogador):
            print('Você tirou um blackjack! Parabéns, você venceu')
        else:
            print('A mesa tirou um blackjack! Você perdeu')
    elif estourou(cartas_jogador):
        print('Você estourou! Seus pontos passaram de 21 e você perdeu o jogo.')
    elif estourou(cartas_mesa):
        print('A mesa estourou! Você venceu')
    elif pontos_mao(cartas_jogador) > pontos_mao(cartas_mesa):
        print(f'A mesa fez {pontos_mao(cartas_mesa)} pontos e você {pontos_mao(cartas_jogador)}. Você venceu!')
    elif pontos_mao(cartas_jogador) < pontos_mao(cartas_mesa):
        print(f'A mesa fez {pontos_mao(cartas_mesa)} pontos e você {pontos_mao(cartas_jogador)}. Você perdeu!')
    else:
        print(f'Você e a mesa fizeram a mesma quantidade de pontos({pontos_mao(cartas_mesa)}), empate!')
    return





def gameloop():
    jogador_parado = False
    mesa_parada = False
    while not jogador_parado or not mesa_parada:
        if cartas_jogador == []:
            for _ in range(2):
                sacar(cartas_jogador,'Você')
            for _ in range(2):
                sacar(cartas_mesa,'A mesa')
        else:
            if checar_blackjack(cartas_jogador) or checar_blackjack(cartas_mesa):
                break
            pontos_jogador = pontos_mao(cartas_jogador)
            pontos_mesa = pontos_mao(cartas_mesa)
            print(f'Você tem {pontos_jogador} e a mesa tem {pontos_mesa}')
            if(not jogador_parado):
                escolha = input('Aperte S para continuar.')
                if escolha.lower() == 's':
                    sacar(cartas_jogador, 'Você')
                    if estourou(cartas_jogador):
                        break
                else:
                    jogador_parado = True
            if (not mesa_parada):
                if (not avaliar() == 'Mesa' or pontos_mao(cartas_mesa) < 13) and not pontos_mao(cartas_mesa) == 21:
                    sacar(cartas_mesa,'A mesa')
                    if estourou(cartas_mesa):
                        break
                else:
                    mesa_parada = True
    return

gameloop()
fim_de_jogo()
