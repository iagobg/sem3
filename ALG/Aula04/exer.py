while True:
    contas_nome = []
    contas_valor = []
    print('1. Incluir Conta')
    print('2. Listar Contas')
    print('3. Listar Contas em Ordem')
    print('4. Pesquisar Conta')
    print('5. Excluir conta')
    print('6. Sair')
    try:
        choice = int(input('Escolha: '))
    except: 
        print('Input inválido')
        break
    if choice == 1:
        nome = input('Nome')
        valor = input('Valor:')
        contas_nome.append(nome)
        contas_valor.append(valor)
    elif choice == 2:
        print(contas_nome)
        for x in range(0,len(contas_nome)):
            print(f'{contas_nome[x]} - R${contas_valor[x]}')
    elif choice == 3:
        contas_nome_ordenada = sorted(zip(contas_valor,contas_nome))
        for x in range (0,len(contas_nome_ordenada)):
            print(f'{contas_nome_ordenada[x][1]} - R${contas_nome_ordenada[x][0]}')
    elif choice == 4:
        pesquisa = input('Qual nome da conta deseja pesquisar?')
        resultados = []
        for x in range(0,len(contas_nome)):
            if pesquisa in contas_nome[x]:
                resultados.append((contas_nome[x]),(contas_valor[x]))
        print('Contas encontradas:')
        for x in range(0,len(resultados)):
            print(f'{resultados[x][0]} - {resultados[x][1]}')
    else:
        break