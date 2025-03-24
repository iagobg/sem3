import math
import random
import time

while True:
    choice = int(input('Número do exercicio: '))
    if choice == 1:
        senha = input('Senha: ')
        minusculo = False
        maiusculo = False
        digito = False
        for char in senha:
            if char.islower():
                minusculo = True
            if char.isupper():
                maiusculo = True
            if char.isdigit():
                digito = True
        if (minusculo and maiusculo and digito and len(senha) > 7 and len(senha) < 13):
            print('Senha válida.')
        else:
            print('Senha Inválida')
    elif choice == 2:
        nome = input('Nome Completo: ').split()
        if len(nome) <= 1:
            print('Por favor digite o nome completo')
        else:
            print(f'Nome no Crachá: {nome[0].upper()}')
    elif choice == 3:
        palavra = input('Palavra: ')
        letra = palavra[0]
        descubra = ''
        for char in palavra:
            if char.lower() == letra.lower():
                descubra += letra.upper()
            else:
                descubra += '_'
        print(f'Descubra: {descubra}')
    elif choice == 4:
        palavra = input('Palavra: ')
        if palavra.lower() == palavra[::-1].lower():
            print(f'A palavra {palavra} é um palíndromo')
        else:
            print(f'{palavra} não é um palíndromo')
    elif choice == 5:
        email = input('Informe o seu email:')
        dominio = email.split('@')
        if len(dominio) == 2 and '.' in dominio[1] and not ' ' in email:
            print('Email válido!')
        else:
            print('Email inválido!')
        
    elif choice == 6:
        input('Pressione para jogar!')
        rolagens = []
        natural = [7,11]
        craps = [2,3,12]
        for i in range(2):
            time.sleep(1)
            num = random.randint(1,6)
            print(f'Você rolou {num} no {i+1}o dado')
            rolagens.append(num)
        if sum(rolagens) in natural:
            print(f'Parabéns, você ganhou! (Natural)')
        elif sum(rolagens) in craps:
            print(f'Você pardeu! (craps)')
        else:
            ponto = sum(rolagens)
            while True:   
                input(f'Pressione para continuar jogando! Você tem que rolar {ponto}')
                for i in range(2):
                    time.sleep(1)
                    num = random.randint(1,6)
                    print(f'Você rolou {num} no {i+1}o dado')
                    rolagens.append(num)
                if sum(rolagens) == 7:
                    print('Você perdeu!')
                    break
                if sum(rolagens) == ponto:
                    print('Você ganhou!')
                    break
                else:
                    print('Você ainda está no jogo!')
        
    else:
        print('Exercício não encontrado')
        break