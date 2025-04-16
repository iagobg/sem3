
contas_nome = ['Amanda','Jorge','Zeca']
contas_valor = [200,100,300]

while True:
    print('1. Incluir Conta')
    print('2. Listar Contas')
    print('3. Listar Contas em Ordem')
    print('4. Pesquisar Conta')
    print('5. Excluir conta')
    print('6. Sair')
    try:
        escolha = int(input('Escolha: '))
    except: 
        print('Input inválido')
        continue
    if escolha == 1:
        nome = input('Nome: ')
        valor = input('Valor: ')
        contas_nome.append(nome)
        contas_valor.append(valor)
    elif escolha == 2:
        print(contas_nome)
        for x in range(0,len(contas_nome)):
            print(f'{contas_nome[x]} - R${contas_valor[x]}')
    elif escolha == 3:
        print('1. Ordem Alfabética Crescente')
        print('2. Ordem Alfabética Descrecente')
        print('3. Ordem de Valor Crescente')
        print('4. Ordem de Valor Decrescente')
        try:
            escolha_ordem = int(input('Escolha: '))
        except: 
            print('Input inválido')
            break
        if escolha_ordem == 1:
            contas_nome_ordenada = sorted(zip(contas_nome,contas_valor))
        elif escolha_ordem == 2:
            contas_nome_ordenada = sorted(zip(contas_nome,contas_valor),reverse = True)
        elif escolha_ordem == 3:
            contas_nome_ordenada = sorted(zip(contas_valor,contas_nome))
        elif escolha_ordem == 4:
            contas_nome_ordenada = sorted(zip(contas_valor,contas_nome),reverse = True)
        else:
            continue
        for x in range (0,len(contas_nome_ordenada)):
            print(f'{contas_nome_ordenada[x][1]} - R${contas_nome_ordenada[x][0]}')
    elif escolha == 4:
        pesquisa = input('Qual nome da conta deseja pesquisar?')
        resultados = []
        for x in range(0,len(contas_nome)):
            if pesquisa.lower() in contas_nome[x].lower():
                resultados.append(((contas_nome[x]),(contas_valor[x])))
        if len(resultados) > 0:
            print('Contas encontradas:')
            for x in range(0,len(resultados)):
                print(f'{resultados[x][0]} - {resultados[x][1]}')
        else:
            print('Nenhuma conta encontrada com esse nome')
    elif escolha == 5:
        pesquisa = input('Qual nome da conta que deseja excluir?')
        for x in range(len(contas_nome)-1,0,-1):
            if pesquisa.lower() in contas_nome[x].lower():
                excluir_confirmacao = input(f'Deseja excluir a conta: {contas_nome[x]} - {contas_valor[x]}?')
                if excluir_confirmacao.lower() == 's':
                    del contas_nome[x]
                    del contas_valor[x]
                    print('Conta excluida.')
                else:
                    print('Conta não excluida.')
    else:
        break