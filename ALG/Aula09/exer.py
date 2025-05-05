def reverso(texto):
    if len(texto) == 1:
        print(texto)
        return
    else:
        print(texto[-1],end="")
        reverso(texto[:-1])

def reverso2(texto):
    if len(texto) == 1:
        return texto
    else:
        return (texto[-1]+texto[:-1])

reverso('texto')
print(reverso2('texto'))