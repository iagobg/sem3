import flet as ft
import requests

API_URL = "http://localhost:3000/produtos" 

def graf_marcas(page):

    def obter_produtos_api():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()

        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar produtos: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    produtos = obter_produtos_api()
    
    dicionario = {}

    for p in produtos:
        marca = p['marca']
        dicionario[marca] = dicionario.get(marca, 0) + 1

    if not dicionario:
        return ft.Text("Nenhum dado disponível.")

    cores = [
        ft.Colors.BLUE,
        ft.Colors.GREEN,
        ft.Colors.ORANGE,
        ft.Colors.PINK,
        ft.Colors.PURPLE,
        ft.Colors.CYAN,
        ft.Colors.RED,
        ft.Colors.YELLOW,
        ft.Colors.AMBER,
        ft.Colors.BROWN
    ]

    largura_max = 500
    maior_qtd = max(dicionario.values())
    total_produtos = sum(dicionario.values())
    marcas_ordenadas = sorted(dicionario.items(), key=lambda x: x[1], reverse=True)
    top10marcas = marcas_ordenadas[:10]
    contagem_outras = len(marcas_ordenadas)-10
    
    if contagem_outras > 0:
        top10marcas.append(("Outras", contagem_outras))

    linhas = []

    for i, (marca, qtd) in enumerate(top10marcas):
        referencia_qtd = sum(qtd for _, qtd in top10marcas)
        largura_barra = (qtd / referencia_qtd) * largura_max
        percentual = (qtd / total_produtos) * 100
        cor = cores[i % len(cores)]

        barra = ft.Container(
            width=largura_barra,
            height=30,
            bgcolor=cor,
            border_radius=5,
        )

        linha = ft.Row(
            [
                ft.Text(marca, width=100),
                barra,
                ft.Text(f"{qtd} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        linhas.append(linha)

    return ft.Column(
        [ft.Text("Produtos por Marca", size=22, weight="bold")] + linhas,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
