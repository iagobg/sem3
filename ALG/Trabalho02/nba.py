import csv

nba=[]

with open('nba.csv', mode='r', encoding="utf-8")as file:
    dados_csv = csv.DictReader(file)
    for linha in dados_csv:
        nba.append(linha)

def jogadores_media():
    jogadores = sorted(nba, key=lambda x: float(x['pts']), reverse=True)
    print('Top 10 média de pontos')
    for i in range(0,10):
        print(f"{i+1} - {jogadores[i]['player_name']} ({jogadores[i]['season']}) {jogadores[i]['pts']}")
    return


def jogadores_pontos():
    jogadores = sorted(nba, key=lambda x: round(float(x['pts'])*int(x['gp'])), reverse=True)
    print('Top 10 pontos feitos em uma única temporada')
    for i in range(0,10):
        print(f"{i+1} - {jogadores[i]['player_name']} ({jogadores[i]['season']}) {round(float(jogadores[i]['pts']) * int(jogadores[i]['gp']))}")
    return

def jogadores_30():
    jogadores_30 = [jogador for jogador in nba if float(jogador['age'])>29]
    jogadores_30 = sorted(jogadores_30, key=lambda x: float(x['pts']), reverse=True)
    for i in range(0,10):
        print(f"{i+1} - {jogadores_30[i]['player_name']} ({jogadores_30[i]['season']}, {round(float(jogadores_30[i]['age']))} anos) {jogadores_30[i]['pts']}")
    return


def top_estatistica():
    estatisticas = {
        1: ['gp', 'Partidas Jogadas'],
        2: ['pts', 'Médias de pontos'],
        3: ['reb', 'Rebotes'],
        4: ['ast', 'Assistências']
    }
    print('Qual estatistica deseja filtrar?')
    for key, value in estatisticas.items():
        print(f'{key}. {value[1]}')
    opcao2 = int(input("Opção:"))
    opcao2 = estatisticas.get(opcao2)
    if opcao2 is None:
        print('Opção inválida')
        return
    ano = input("Qual temporada deseja analisar? (E.g. 1996-97)")
    jogadores = [jogador for jogador in nba if jogador['season'] == ano]
    if len(jogadores) == 0:
        print('Temporada inválida')
        return
    jogadores = sorted(jogadores, key=lambda x:float(x[opcao2[0]]), reverse = True)
    for i in range(0,10):
        print(f"{i+1} - {jogadores[i]['player_name']} ({jogadores[i]['season']}) {(float(jogadores[i][opcao2[0]]))}")
    return

def jogadores_pais():
    americanos = {jogador['player_name'] for jogador in nba if jogador['country'] == 'USA'}
    extrangeiros = {jogador['player_name'] for jogador in nba if jogador['country'] != 'USA'}
    uniao = americanos | extrangeiros
    print(f'Jogadores americanos: {len(americanos)}')
    print(f'Jogadores extrangeiros: {len(extrangeiros)}')
    print(f'Jogadores total: {len(uniao)}')
    return

while True:
    print("Estatísticas NBA 96-22")
    print("1. Top 10 média de pontos feitos por um atleta em uma única temporada")
    print("2. Top 10 pontos feitos por um atleta em uma única temporada")
    print("3. Top 10 média de pontos feitos por um atleta de 30 anos ou mais em uma única temporada")
    print("4. Top 10 estatistica de uma temporada específica")
    print("5. Comparação de jogadores americanos com extrangeiros")
    print("6. Finalizar")
    opcao = int(input("Opção:"))
    if opcao == 1:
        jogadores_media()
        input()
    elif opcao == 2:
        jogadores_pontos()
        input()
    elif opcao == 3:
        jogadores_30()
        input()
    elif opcao == 4:
        top_estatistica()
        input()
    elif opcao == 5:
        jogadores_pais()
        input()
    else:
        break