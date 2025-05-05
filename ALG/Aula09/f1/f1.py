import csv
from itertools import groupby

winners=[]


with open('winners.csv', mode="r", encoding="utf-8") as file:
    dados_csv = csv.DictReader(file)
    for linha in dados_csv:
        winners.append(linha)

def pilotos_top10():
    vitorias_pilotos = [(piloto, sum(1 for corrida in winners if corrida['Winner'] == piloto)) for piloto in {corrida['Winner'] for corrida in winners}]
    vitorias_pilotos.sort(key=lambda x: x[1], reverse=True)
    print('Pilotos com mais vitórias:')
    for i in range(0, 10):
        print(f"{vitorias_pilotos[i][0]:20s} - {vitorias_pilotos[i][1]:4} vitórias")
    return

def equipes_10():
    equipes_10 = [(equipe, total) for equipe, total in [(equipe, sum(1 for corrida in winners if corrida['Car'] == equipe)) for equipe in {corrida['Car'] for corrida in winners}] if total >= 10]
    equipes_10.sort(key=lambda x: x[1])
    print('Equipes com 10 vitórias ou mais')
    for equipe in equipes_10:
        print(f"{equipe[0]:30s} - {equipe[1]:4}")
    return

def provas_longas():
    def conversor_tempo(time):
        if not time or time.strip() == '':
            return 0
        tempo_dividido = time.split(':')
        milisegundos = tempo_dividido[-1].split('.')
        ms = int(milisegundos[1]) if len(milisegundos) > 1 else 0
        sec = int(milisegundos[0]) * 1000
        min = int(tempo_dividido[-2]) * 60000
        hr = int(tempo_dividido[-3]) * 3600000 if len(tempo_dividido) > 2 else 0
        tempo_convertido = ms + sec + min+ hr
        return tempo_convertido
    winners_sorted_by_time = sorted(winners,key=lambda x: conversor_tempo(x['Time']), reverse=True)
    for i, race in enumerate(winners_sorted_by_time):
        print(f"{(i+1):2} - {race['Time']:12} - {race['Grand Prix']:20} - {race['Date']}")
        if i == 9:
            break
    return

while True:
    print("Fórmula 1")
    print("1. A lista dos 10 pilotos com maior número de vitórias na história da F1 (em ordem decrescente de vitórias)")
    print("2. A lista das Equipas com 10 ou + vitórias na F1 (em ordem crescente de vitórias)")
    print("3. A lista das 10 provas com vitórias com maior tempo da história da F1 (em ordem decrescente de tempo) Tempo, Piloto, Equipe, GP e Dat")
    print("4. Finalizar")
    opcao = int(input("Opção:"))
    if opcao == 1:
        pilotos_top10()
    elif opcao == 2:
        equipes_10()
    elif opcao == 3:
        provas_longas()
    else:
        break