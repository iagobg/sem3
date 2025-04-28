clientes = [
    {"nome": "Pedro Santos", "idade": 30},
    {"nome": "Aline Costa", "idade": 42},
    {"nome": "Maria de Mattos", "idade": 25},
    {"nome": "Carlos de Nóbrega", "idade": 34},
    {"nome": "Bianca Cardoso", "idade": 27}
]


clientes.append({"nome": "Lucas de Souza", "idade":20})

print(clientes[0]["nome"])


for cliente in clientes:
    print(cliente["nome"])
    

for num, cliente in enumerate(clientes, start=1):
    print(f"{num}º cliente: {cliente["nome"]}")


clientes2 = sorted(clientes,key=lambda cliente: cliente["nome"])    



for num, cliente in enumerate(clientes2, start=1):
    print(f"{num}º cliente: {cliente["nome"]}")

