alunos = [
    {'nome':'Ricardo', 'curso': 'Espanhol', 'valor': 350},
    {'nome':'Maria', 'curso': 'Inglês', 'valor': 400},
    {'nome':'Fátima', 'curso': 'Franês', 'valor': 450},
    {'nome':'Pedro', 'curso': 'Espanhol', 'valor': 320},
    {'nome':'Bruna', 'curso': 'Inglês', 'valor': 420}
]

grupos = {}


for aluno in alunos:
    curso = aluno['curso']
    valor = aluno['valor']
    grupos[curso] = grupos.get(curso,0) + valor
    
print(grupos)

grupos2 = {}
for aluno in alunos:
    curso = aluno['curso']
    grupos2[curso] = grupos2.get(curso,0) + 1
print(grupos2)
    

grupos3 = dict(sorted(grupos.items(),key=lambda grupo: grupo[1],reverse=True))

for curso, valor in grupos3.items():
    print(f"{curso:20s} R${valor:9.2f}")
