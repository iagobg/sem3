palavra = 'computador'
letra = input('letra: ')
if palavra.find(letra) >= 0:
    print('Ok! Letra consta na palvara')
else:
    print('Erro, letra não consta.')