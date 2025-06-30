import flet as ft

from telas.crud_produtos import crud_produtos
from telas.graf_vendas import graf_vendas

def main(page: ft.Page):
    page.title = "Sistema de Vendas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    snack = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack
    page.overlay.append(snack)

    conteudo_dinamico = ft.Column()

    def navigate(e):
        rota = e.control.data
        if rota == "crud_produtos":
            conteudo_dinamico.controls = [crud_produtos(page)]
        elif rota == "graf_vendas":
            conteudo_dinamico.controls = [graf_vendas(page)]
        page.update()

    nav_buttons = ft.Row([
        ft.ElevatedButton("CRUD Produtos", data="crud_produtos", on_click=navigate),
        ft.ElevatedButton("Gráfico de Vendas", data="graf_vendas", on_click=navigate),
    ], alignment=ft.MainAxisAlignment.CENTER)

    conteudo_dinamico.controls = [crud_produtos(page)]

    page.add(
        ft.Column([
            ft.Text("Sistema de Vendas", size=30, weight="bold", text_align="center"),
            nav_buttons,
            ft.Divider(),
            conteudo_dinamico
        ], scroll=ft.ScrollMode.AUTO)
    )

ft.app(target=main)