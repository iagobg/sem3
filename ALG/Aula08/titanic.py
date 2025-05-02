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

    homens, mulheres, h_sobreviventes, m_sobreviventes = 0, 0, 0, 0

    for passageiro in titanic:
        if passageiro['Sex'] == 'male':
            homens += 1
            if passageiro['Survived'] == '1':
                h_sobreviventes += 1
        if passageiro['Sex'] == 'female':
            mulheres += 1
            if passageiro['Survived'] == '1':
                m_sobreviventes += 1     

    print("Total de Passageiros \n"
        f"Masculino: {homens}\n"
        f"    Sobreviventes: {h_sobreviventes}\n"
        f"    Mortos: {homens-h_sobreviventes}\n"
        f"Feminino: {mulheres}\n"
        f"    Sobreviventes: {m_sobreviventes}\n"
        f"    Mortos: {mulheres-m_sobreviventes}")
    return

def media_top10():
    titulo("Media de Idade e 10 mais velhos")
    idade_total = 0
    passageiros_com_idade = 0
    mais_velhos = []
    for passageiro in titanic:
        if passageiro['Age'].isdigit():
            idade_total += int(passageiro['Age'])
            passageiros_com_idade += 1
            if len(mais_velhos) < 10:
                mais_velhos.append(passageiro)
                mais_velhos.sort(key = lambda x: x["Age"], reverse=True)
            else:
                if int(passageiro['Age']) > int(mais_velhos[9]['Age']):
                    mais_velhos.append(passageiro)
                    mais_velhos.sort(key = lambda x: x["Age"], reverse=True)
                    mais_velhos.pop()             
    print(
        f"Media das Idades: {(idade_total / passageiros_com_idade):.2f}\n"
        f"Lista dos mais idosos\n"
        f"Nome{' ' * 48}Idade   Sobrevivente"
    )
    for passageiro in mais_velhos:
        print(f'{passageiro["Name"]:<50} - {passageiro["Age"]:>4} - {"Sim" if passageiro["Survived"] == "1" else "Não"}')
    
    return

def dados_classe():
    titulo('Dados por Classe')
    primeira_classe, primeira_classe_sob, segunda_classe, segunda_classe_sob, terceira_classe, terceira_classe_sob = 0,0,0,0,0,0
    for passageiro in titanic:
        if passageiro['Pclass'] == '1':
            primeira_classe += 1
            if passageiro['Survived'] == '1':
                primeira_classe_sob += 1
        elif passageiro['Pclass'] == '2':
            segunda_classe += 1
            if passageiro['Survived'] == '1':
                segunda_classe_sob += 1
        elif passageiro['Pclass'] == '3':
            terceira_classe += 1
            if passageiro['Survived'] == '1':
                terceira_classe_sob += 1
    print(primeira_classe)
    print(
        f"Total de Passageiros: {len(titanic)}\n"
       f"1a Classe: {primeira_classe}\n"
       f"   Sobreviventes: {primeira_classe_sob} ({(primeira_classe_sob/primeira_classe*100):.2f}%)\n"
       f"   Mortos: {primeira_classe-primeira_classe_sob} ({((primeira_classe-primeira_classe_sob)/primeira_classe*100):.2f}%)\n"
       f"2a Classe: {segunda_classe}\n"
       f"   Sobreviventes: {segunda_classe_sob} ({(segunda_classe_sob/segunda_classe*100):.2f}%)\n"
       f"   Mortos: {segunda_classe-segunda_classe_sob} ({((segunda_classe-segunda_classe_sob)/segunda_classe*100):.2f}%)\n"
       f"3a Classe: {terceira_classe}\n"
       f"   Sobreviventes: {terceira_classe_sob} ({(terceira_classe_sob/terceira_classe*100):.2f}%)\n"
       f"   Mortos: {terceira_classe-terceira_classe_sob} ({((terceira_classe-terceira_classe_sob)/terceira_classe*100):.2f}%)\n"

        
        )
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
    
