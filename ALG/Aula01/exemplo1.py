import math

nome = input('Nome: ')
idade = int(input('Idade: '))
salario = float(input('Salário R$: '))

'''
COmentario de
Varias Linhas
'''


print(f"Seu nome é {nome}")
print(f'Sua idade é {idade} anos')
print(f'Seu salário é de R$ {salario:9.2f}')


if idade < 18:
    print("Você é menor de idade")
else:
    print("Você é maior de idade")


print('-'*20)


bairro = input('Bairro: ').upper()

match bairro:
    case 'CENTRO':
        print ('Você mora aqui perto...')
    case 'FRAGATA' | 'TRES VENDAS':
        print ('Ainda é perto')
    case 'LARANJAL':
        print('Você mora longe')
    case _:
        print('Não sei a distäância') 
      
    