import flet as ft
from telas.cad_produtos import cad_produtos
from telas.graf_marcas import graf_marcas
from telas.graf_caros import graf_caros

def main(page: ft.Page):
    page.title = "Loja de Esportes"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    snack = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack
    page.overlay.append(snack)  # necessário para que o snack apareça na tela

    conteudo_dinamico = ft.Column()  # Aqui vamos renderizar o conteúdo que muda

    def navigate(e):
        rota = e.control.data
        if rota == "cad_produtos":
            conteudo_dinamico.controls = [cad_produtos(page)]
        elif rota == "graf_marcas":
            conteudo_dinamico.controls = [graf_marcas(page)]
        elif rota == "graf_caros":
            conteudo_dinamico.controls = [graf_caros(page)]
        page.update()

    nav_buttons = ft.Row([
        ft.ElevatedButton("Cadastro de Produtos", data="cad_produtos", on_click=navigate),
        ft.ElevatedButton("Gráfico por Marcas", data="graf_marcas", on_click=navigate),
        ft.ElevatedButton("Gráfico + Caros", data="graf_caros", on_click=navigate),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Carrega conteúdo inicial (ex: produtos)
    conteudo_dinamico.controls = [cad_produtos(page)]

    page.add(
        ft.Column([
            ft.Text("Loja de Esportes - Cadastro de Produtos", size=30, weight="bold", text_align="center"),
            nav_buttons,
            ft.Divider(),
            conteudo_dinamico
        ], scroll=ft.ScrollMode.AUTO)
    )

ft.app(target=main)
