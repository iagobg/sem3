import csv

titanic = []

with open('titanic.csv', mode="r") as arg:
    dados_csv = csv.DictReader(arg)
    for linha in dados_csv:
        titanic.append(linha)
    
survivors = [x for x in titanic if x['Survived'] == '1']

def titulo(mensa, traco="-"):
    print()
    print(mensa.upper())
    print(traco*50)

def dados_sexo():
    titulo("Dados por Sexo")
    homens = [passageiro for passageiro in titanic if passageiro['Sex'] == "Male"]
    mulheres = [passageiro for passageiro in titanic if passageiro['Sex'] == "Female"]
    h_sobrevivementes = [passageiro for passageiro in homens if passageiro['Survived'] == "1"]
    m_sobrevivementes = [passageiro for passageiro in mulheres if passageiro['Survived'] == "1"]
    print(f"De {len(titanic)} passageiros, haviam {len(homens)} homens ({len(h_sobrevivementes)} sobreviveram, {len(homens)-len(h_sobrevivementes)})e  {len(mulheres)} mulheres ({len(m_sobrevivementes)} sobreviveram, {len(mulheres)-len(m_sobrevivementes)}")
    return

def media_top10():
    return

def dados_classe():
    return


while True:
    titulo("Passageiros do Titanic",'=')
    print("1. Dados por Sexo e Sobreviventes")
    print("2. Média de Idade e 10+ Idosos")
    print("3. Dados por Classe e Sobreviventes")
    print("4. Finalizar")
    opcao = int(input("Opção:"))
    if opcao == 1:
        dados_sexo()
    elif opcao == 2:
        media_top10()
    elif opcao == 3:
        dados_classe()
    else:
        break
    
