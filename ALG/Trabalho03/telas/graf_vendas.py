import flet as ft
import requests
import json
from collections import defaultdict
from datetime import datetime, timedelta

URL_API = "http://localhost:3000/vendas"
CATEGORIAS_ORDEM = ['ELETRONICOS', 'ROUPAS', 'CASA', 'ESPORTE', 'LIVROS', 'OUTROS']

def graf_vendas(pagina):
    categorias = CATEGORIAS_ORDEM
    dados_grafico = []

    campo_data_inicio = ft.TextField(
        label="Data Início (YYYY-MM-DD)",
        width=200,
        value=(datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    )
    campo_data_fim = ft.TextField(
        label="Data Fim (YYYY-MM-DD)", 
        width=200,
        value=datetime.now().strftime("%Y-%m-%d")
    )

    cartao_total_vendas = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Total Vendas", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("R$ 0,00", size=20, color=ft.Colors.GREEN_600),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            alignment=ft.alignment.center
        ),
        width=180,
        height=150
    )

    cartao_quantidade_vendas = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Qtd. Vendas", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("0", size=20, color=ft.Colors.BLUE_600),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            alignment=ft.alignment.center
        ),
        width=180,
        height=150
    )

    cartao_ticket_medio = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Ticket Médio", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("R$ 0,00", size=20, color=ft.Colors.ORANGE_600),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            alignment=ft.alignment.center
        ),
        width=180,
        height=150
    )

    grafico = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.Colors.GREY_400),
        left_axis=ft.ChartAxis(
            labels_size=40,
            title=ft.Text("Valor das Vendas (R$)"),
            title_size=16,
        ),
        bottom_axis=ft.ChartAxis(
            labels_size=16,
            title=ft.Text("Categorias de Produtos"),
            title_size=16,
        ),
        width=800,
        height=400,
        bgcolor=ft.Colors.WHITE,
        max_y=1000,
    )

    carregando = ft.ProgressRing(visible=False)

    def mostrar_mensagem(texto, erro=False):
        pagina.snack_bar = ft.SnackBar(
            ft.Text(texto),
            bgcolor=ft.Colors.RED_400 if erro else ft.Colors.GREEN_400
        )
        pagina.snack_bar.open = True
        pagina.update()

    def carregar_dados():
        carregando.visible = True
        pagina.update()
        
        try:
            parametros = {}
            if campo_data_inicio.value:
                parametros['dataInicio'] = campo_data_inicio.value
            if campo_data_fim.value:
                parametros['dataFim'] = campo_data_fim.value
            
            url = f"{URL_API}/relatorio"
            if parametros:
                query = "&".join([f"{k}={v}" for k, v in parametros.items()])
                url += f"?{query}"
            
            print(f"Buscando dados de: {url}")
            resposta = requests.get(url)
            resposta.raise_for_status()
            dados = resposta.json()
            
            vendas = dados.get("vendas", [])
            resumo = dados.get("resumo", {})

            print(f"{len(vendas)} vendas carregadas")

            cartao_total_vendas.content.content.controls[1].value = f"R$ {resumo.get('total_vendas', 0):.2f}"
            cartao_quantidade_vendas.content.content.controls[1].value = str(resumo.get('quantidade_vendas', 0))
            cartao_ticket_medio.content.content.controls[1].value = f"R$ {resumo.get('ticket_medio', 0):.2f}"
            
            vendas_por_categoria = defaultdict(lambda: {'total': 0, 'quantidade': 0})
            
            for venda in vendas:
                categoria = venda['produto']['categoria']
                total = float(venda['total'])
                quantidade = int(venda['quantidade'])
                
                vendas_por_categoria[categoria]['total'] += total
                vendas_por_categoria[categoria]['quantidade'] += quantidade
            
            grupos_barras = []
            valor_maximo = 0

            cores_categorias = {
                'ELETRONICOS': ft.Colors.BLUE_400,
                'ROUPAS': ft.Colors.PINK_400,
                'CASA': ft.Colors.GREEN_400,
                'ESPORTE': ft.Colors.ORANGE_400,
                'LIVROS': ft.Colors.PURPLE_400,
                'OUTROS': ft.Colors.GREY_400
            }

            for i, categoria in enumerate(categorias):
                total = vendas_por_categoria[categoria]['total']
                valor_maximo = max(valor_maximo, total)
                grupos_barras.append(
                    ft.BarChartGroup(
                        x=i,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=total,
                                width=40,
                                color=cores_categorias.get(categoria, ft.Colors.BLUE_400),
                                border_radius=0,
                            )
                        ],
                    )
                )

            grafico.bar_groups = grupos_barras
            grafico.max_y = valor_maximo * 1.1 if valor_maximo > 0 else 1000
            grafico.bottom_axis.labels = [
                ft.ChartAxisLabel(value=i, label=ft.Text(cat[:8])) 
                for i, cat in enumerate(categorias)
            ]

            carregando.visible = False
            pagina.update()

            if len(vendas) == 0:
                mostrar_mensagem("Nenhuma venda encontrada no período selecionado")
            else:
                mostrar_mensagem(f"Dados de {len(vendas)} vendas carregados")
            
        except requests.exceptions.RequestException as e:
            carregando.visible = False
            pagina.update()
            print(f"Erro de requisição: {e}")
            mostrar_mensagem(f"Erro de conexão: {str(e)}", True)
        except json.JSONDecodeError as e:
            carregando.visible = False
            pagina.update()
            print(f"Erro de decodificação JSON: {e}")
            mostrar_mensagem("Erro ao decodificar resposta da API", True)
        except Exception as e:
            carregando.visible = False
            pagina.update()
            print(f"Erro inesperado: {e}")
            mostrar_mensagem(f"Erro inesperado: {str(e)}", True)

    def ao_clicar_atualizar(e):
        carregar_dados()

    def ao_clicar_limpar_filtros(e):
        campo_data_inicio.value = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        campo_data_fim.value = datetime.now().strftime("%Y-%m-%d")
        pagina.update()
        carregar_dados()

    itens_legenda = []
    cores_categorias_legenda = {
        'ELETRÔNICOS': ft.Colors.BLUE_400,
        'ROUPAS': ft.Colors.PINK_400,
        'CASA': ft.Colors.GREEN_400,
        'ESPORTE': ft.Colors.ORANGE_400,
        'LIVROS': ft.Colors.PURPLE_400,
        'OUTROS': ft.Colors.GREY_400
    }

    for categoria, cor in cores_categorias_legenda.items():
        itens_legenda.append(
            ft.Row([
                ft.Container(
                    width=20,
                    height=20,
                    bgcolor=cor,
                    border_radius=3
                ),
                ft.Text(categoria, size=12)
            ], spacing=5)
        )

    layout = ft.Column([
        ft.Text("Dashboard de Vendas por Categoria", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Row([
            cartao_total_vendas,
            cartao_quantidade_vendas,
            cartao_ticket_medio
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ft.Divider(),
        ft.Row([
            campo_data_inicio,
            campo_data_fim,
            ft.ElevatedButton("Atualizar", on_click=ao_clicar_atualizar, icon=ft.Icons.REFRESH),
            ft.ElevatedButton("Limpar Filtros", on_click=ao_clicar_limpar_filtros, icon=ft.Icons.CLEAR),
            carregando
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Text("Vendas por Categoria de Produto", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Row([
            ft.Container(
                content=grafico,
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Legenda", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    *itens_legenda
                ], spacing=8),
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_300),
                width=150
            )
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=20)
    ], spacing=20, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    print("Carregando dados iniciais de vendas...")
    carregar_dados()

    return layout
