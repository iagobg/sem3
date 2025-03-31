import random
import time
import sys

naipes = ['♠️','♥️','♦️','♣️']
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
    for carta in cartas:
        if pontos_carta(carta) == 21 and pontos+pontos_carta(carta) > 21:
            pontos += 1
        else:
            pontos += pontos_carta(carta)
    return pontos


def sacar(mao,pessoa):
    num = random.randint(0,len(baralho)-1)
    mao.append(baralho.pop(num))
    print(f'{pessoa} sacou {cartas_jogador[-1]}')
    time.sleep(2)
    return 

def avaliar():
    jogador = pontos_mao(cartas_jogador)
    mesa = pontos_mao(cartas_mesa) 
    if jogador == mesa:
        return 'Empate'
    elif jogador >= mesa:
        return 'Jogador'
    else:
        return 'Mesa'
    
    

def fim_de_jogo():
    resultado = avaliar()
    if resultado == 'Empate':
        print('O jogo empatou!')
    elif resultado == 'Jogador':
        print('Você venceu!')
    elif resultado == 'Mesa':
        print('Você perdeu!')
    return

mesa_parada = False
jogador_parado = False

while True:
    if (cartas_jogador == []):
        for i in range(2):
            sacar(cartas_jogador,'Você')
        for i in range(2):
            sacar(cartas_mesa,'A mesa')
            time.sleep(2)
        pontos_jogador = pontos_mao(cartas_jogador)
        pontos_mesa = pontos_mao(cartas_mesa)
        print(f'Você tem {pontos_jogador} e a mesa tem {pontos_mesa}')
        if (pontos_jogador == 21 and pontos_mesa == 21):
            print('Ambos conseguiram um blackjack! Empate.')
        elif(pontos_mesa == 21):
            print('Você perdeu, a mesa conseguiu um blackjack!')
        elif(pontos_jogador==21):
            print('Blackjack! Você ganhou!')
        break
    else:
        if(not jogador_parado):
            escolha = input('Aperte S para continuar.')
            if escolha.lower() == 's':
                sacar(cartas_jogador)
                
                pontos_jogador = pontos_mao(cartas_jogador)
                if pontos_jogador > 21:
                    print('Você passou de 21, infelizmente você perdeu!')
                    break
                else:
                    print(f'Você está agora com {pontos_mao(cartas_jogador)}')
        if (not mesa_parada):
            #TODO MESA