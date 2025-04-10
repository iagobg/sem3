import time
import curses
import random

snake = [(2,3),(2,4)]
snake_head = (2,4)
refresh_rate = 60
tamanho_tabuleiro = 8

cabeca_snake = '↓↓'
direcao_snake = 's'
comida = (4,4)
ultima_direcao = 's'
tempo_mover = 60
reducao_mover = 4
pontos = 0
comeu = False
mudar_direcao = True

game_over = False

teclas = {
    curses.KEY_UP: 'n',
    curses.KEY_DOWN: 's',
    curses.KEY_RIGHT: 'l',
    curses.KEY_LEFT: 'o',
}

def direcao_valida(nova):
    if ((ultima_direcao == 'n' and nova == 's') or 
        (ultima_direcao == 's' and nova == 'n') or 
        (ultima_direcao == 'l' and nova == 'o') or
        (ultima_direcao == 'o' and nova == 'l')):
        return False
    else:
        return True

def atualizar_cabeca():
    global cabeca_snake
    if direcao_snake == 'n':
        cabeca_snake = '↑↑'
    elif direcao_snake == 's':
        cabeca_snake = '↓↓'
    elif direcao_snake == 'l':
        cabeca_snake = '→→'
    elif direcao_snake == 'o':
        cabeca_snake = '←←'


def detectar_tecla(tela):
    global direcao_snake, mudar_direcao
    tecla = tela.getch()
    if tecla in teclas:
        nova_direcao = teclas[tecla]
        if direcao_valida(nova_direcao) and mudar_direcao:
            direcao_snake = nova_direcao
            atualizar_cabeca()
            mudar_direcao = False
    return

def proximo_quadrado():
    if direcao_snake == 'n':
        return (snake_head[0],snake_head[1]-1)
    elif direcao_snake == 's':
        return (snake_head[0],snake_head[1]+1)
    elif direcao_snake == 'l':
        return (snake_head[0]+1,snake_head[1])
    elif direcao_snake == 'o':
        return (snake_head[0]-1,snake_head[1])

def checar_colisao(proximo):
    if proximo in snake:
        return False
    elif proximo[0] < 0 or proximo[1] < 0 or proximo[0] > tamanho_tabuleiro-1 or proximo[1] > tamanho_tabuleiro - 1:
        return False
    elif proximo == comida:
        comer()
    return True
        

def comer():
    global comeu,reducao_mover, comida
    comeu = True
    reducao_mover = min(reducao_mover*1.2,refresh_rate)
    coordenadas_validas = list({(x, y) for x in range(tamanho_tabuleiro) for y in range(tamanho_tabuleiro)} - set(snake))
    comida = random.choice(coordenadas_validas)
    return

def mover():
    global tempo_mover, comeu, mudar_direcao
    if tempo_mover <= 0:
        global snake_head, ultima_direcao, game_over
        proximo = proximo_quadrado()
        if not comeu:
            snake.pop(0)
        comeu = False
        if not checar_colisao(proximo):
            game_over = True
            return
        else:
            snake.append(proximo)
            snake_head = proximo
            ultima_direcao = direcao_snake
            tempo_mover = 60
            mudar_direcao = True

    else:
        tempo_mover -= reducao_mover
    return


def game_loop(tela):
    global tamanho_tabuleiro
    tela.nodelay(True)
    tamanho_tabuleiro = min(tela.getmaxyx())
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    while game_over == False:
        detectar_tecla(tela)
        mover()
        tela.clear()
        for y in range(0,tamanho_tabuleiro):
            for x in range (0, tamanho_tabuleiro):
                if (x,y) in snake:
                    if (x,y) == snake_head:
                        tela.addstr(y, x*2, cabeca_snake, curses.color_pair(2))
                    else:
                        tela.addstr(y, x*2, '  ', curses.color_pair(2))
                elif comida == (x,y):
                        tela.addstr(y, x*2, '  ', curses.color_pair(3))
                else:
                    tela.addstr(y, x*2, '  ', curses.color_pair(1))
                    
        tela.refresh()
        time.sleep(1/refresh_rate)
    print('Game over!')
    return

curses.wrapper(game_loop)