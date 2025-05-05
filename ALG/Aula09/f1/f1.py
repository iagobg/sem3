import csv

winners=[]


with open('winners.csv', mode="r", encoding="utf-8") as file:
    dados_csv = csv.DictReader(file)
    for linha in dados_csv:
        winners.append(linha)

def pilotos_top10():
    pilotos = []
    for item in winners:
        vencedor = item['winner']
        pilotos
    return

def equipes_10():
    return

def provas_longas():
    return

while True:
    titulo("Fórmula 1",'=')
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