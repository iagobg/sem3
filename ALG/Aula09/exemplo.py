while True:
    try:
        choice = int(input('Número do exercicio: '))
    except:
        print('Input inválido')
        break
    if choice == 1:
        def contagem(n):
            if n==0:
                print("Fim")
            else:
                print(n)
                contagem(n-1)          
        contagem(5)
    if choice == 2:
        def fatorial(n):
            if n == 1:
                return 1
            else:
                return n * fatorial(n-1)
        print(fatorial(5))
    else:
        break
