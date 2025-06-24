import flet as ft
import requests


API_URL = "http://localhost:3000/produtos" 

def graf_caros(page):
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
    
    produtos_ordenados = sorted(produtos, key = lambda x: x['preco'], reverse=True)[:10]
    
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
    
    
    
    return ft.Column(
        [ft.Text("Gráficos dos Top 10 Produtos mais Caros", size = 22, weight = 'bold')] +
        [ft.Text(f"{produto['nome']} - R$ {produto['preco']}") for produto in produtos_ordenados],
        spacing = 10,
        scroll=ft.ScrollMode.AUTO
    )