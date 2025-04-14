import math

while True:
    try:
        choice = int(input('Número do exercicio: '))
    except:
        print('Input inválido')
        break
    if choice == 1:
        numeros = [15,30,50,72,95]
        numeros2 = [num for num in numeros if num % 10 == 0]
        print(numeros2)
    if choice == 2:
        nomes = ["ana júlia", "joão antônio", "luis eduardo", "maria helena"]
        nomes2 = [nome.upper() for nome in nomes]
        nomes3 = [' '.join(palavra.capitalize() for palavra in nome.split()) for nome in nomes]
        print(nomes,nomes2,nomes3)
    if choice == 3:
        numeros = [10, 16, 20, 25, 36, 40]
        raizes = [int(math.sqrt(num)) for num in numeros if math.sqrt(num).is_integer()]
        print(raizes)
    else:
        print('Numero Invalido')
        break