import math

while True:
    choice = int(input('Número do exercicio: '))
    if choice == 1:
        pessoas = int(input('Número de pessoas: '))
        peixes = int(input('Número de peixes: '))
        print(f'Pagar R$: {pessoas*20+max(0,(peixes-pessoas)*12):.2f}')
        
    elif choice == 2:
        numero = int(input('Número: '))
        divisores = []
        for x in range (1,numero):
            if numero % x == 0:
                divisores.append(x)
        if sum(divisores) == numero:
            print('O número é perfeito')
        else:
            print('O número não é perfeito')
            
    elif choice == 3:
        produto = input('Produto: ')
        etiquetas = int(input('No de Etiquetas: '))
        for x in range (0, etiquetas, 2):
            if x+1 < etiquetas:
                print(f'{produto} {produto}')
            else:
                print(produto)
                
    elif choice == 4:
        chinc = int(input('Número de chincilas: '))
        anos = int(input('Anos de criação: '))
        for x in range(0,anos):
            print(f'{x+1} ano : {chinc} chinchilas')
            chinc *= 3
    elif choice == 5:
        numeros = []
        print('Informe números ou 0 para sair:')
        while True:
            num = int(input('Número: '))
            if num == 0:
                break
            else:
                numeros.append(num)
        print('-'*10)
        print(f'Números digitados: {len(numeros)}')
        print(f'Soma dos números: {sum(numeros)}')
        print(f'Maior número: {max(numeros)}')
        
    else:
        print('Numero Invalido')
        break