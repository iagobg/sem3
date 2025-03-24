import time
import random

nome = input('Nome do Apostador: ')
valor = float(input('Valor da Aposta R$: '))

input('Pressione Enter para iniciar o sorteio...')

figuras = '🍕🚗🎈'
jogo = ''


print("Suas Apostas: ", end='')

for _ in range(3):
    num = random.randint(0,2)
    print(figuras[num], end=' ', flush=True)
    time.sleep(1)
    jogo = jogo + figuras[num] 
    
    
if jogo[0] == jogo[1] and jogo[0] == jogo[2]:
    print(f'Parabens {nome}, você ganhou {valor*3}')
elif jogo[0] == jogo[1] or jogo[1] == jogo[2] or jogo[0] == 2:
    print(f'{nome}, você ganhou apenas {valor*1.5}')
else:
    print(f'{nome}, você perdeu')
