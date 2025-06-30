import flet as ft
import requests
import json

URL_API = "http://localhost:3000/produtos"

def crud_produtos(pagina):
    modo_edicao = ft.Ref[bool]()
    modo_edicao.current = False
    id_produto_atual = ft.Ref[int]()
    id_produto_atual.current = None

    campo_nome = ft.TextField(label="Nome do Produto", expand=4)
    campo_descricao = ft.TextField(label="Descrição", expand=4)
    campo_categoria = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("ELETRONICOS"),
            ft.dropdown.Option("ROUPAS"),
            ft.dropdown.Option("CASA"),
            ft.dropdown.Option("ESPORTE"),
            ft.dropdown.Option("LIVROS"),
            ft.dropdown.Option("OUTROS")
        ],
        expand=2)
    campo_preco_compra = ft.TextField(label="Preço de Compra R$", expand=2)
    campo_preco_venda = ft.TextField(label="Preço de Venda R$", expand=2)
    campo_estoque = ft.TextField(label="Estoque", expand=1)
    campo_estoque_min = ft.TextField(label="Estoque Mínimo", expand=1)
    campo_fornecedor_id = ft.TextField(label="ID do Fornecedor", expand=2)

    titulo = ft.Text("Adicionar Produto", size=30, weight="bold", text_align="center")

    container_formulario = ft.Container(
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.GREY_100,
        border=ft.border.all(2, ft.Colors.GREY_400)
    )

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cód.")),
            ft.DataColumn(ft.Text("Nome do Produto")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Preço Compra R$")),
            ft.DataColumn(ft.Text("Preço Venda R$")),
            ft.DataColumn(ft.Text("Estoque")),
            ft.DataColumn(ft.Text("Estoque Mínimo")),
            ft.DataColumn(ft.Text("Fornecedor")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
        expand=True
    )

    def mostrar_mensagem(texto, erro=False):
        pagina.snack_bar = ft.SnackBar(
            ft.Text(texto),
            bgcolor=ft.Colors.RED_400 if erro else ft.Colors.GREEN_400
        )
        pagina.snack_bar.open = True
        pagina.update()

    def definir_modo_edicao(editar, dados_produto=None):
        modo_edicao.current = editar
        if editar and dados_produto:
            id_produto_atual.current = dados_produto["id"]
            campo_nome.value = dados_produto["nome"]
            campo_descricao.value = dados_produto.get("descricao", "")
            campo_categoria.value = dados_produto["categoria"]
            campo_preco_compra.value = str(dados_produto["preco_compra"])
            campo_preco_venda.value = str(dados_produto["preco_venda"])
            campo_estoque.value = str(dados_produto["estoque"])
            campo_estoque_min.value = str(dados_produto["estoque_min"])
            campo_fornecedor_id.value = str(dados_produto["fornecedor"]["id"]) if dados_produto.get("fornecedor") else ""

            titulo.value = "Editar Produto"
            titulo.color = ft.Colors.ORANGE_600
            container_formulario.bgcolor = ft.Colors.ORANGE_50
            container_formulario.border = ft.border.all(2, ft.Colors.ORANGE_400)

            botao_principal.text = "Alterar"
            botao_principal.bgcolor = ft.Colors.ORANGE_400
            botao_principal.color = ft.Colors.WHITE
            botao_cancelar.visible = True
        else:
            id_produto_atual.current = None
            titulo.value = "Adicionar Produto"
            titulo.color = None
            container_formulario.bgcolor = ft.Colors.GREY_100
            container_formulario.border = ft.border.all(2, ft.Colors.GREY_400)

            botao_principal.text = "Enviar"
            botao_principal.bgcolor = None
            botao_principal.color = None
            botao_cancelar.visible = False

        pagina.update()

    def editar_produto(dados):
        definir_modo_edicao(True, dados)

    def carregar_produtos():
        try:
            resposta = requests.get(URL_API)
            resposta.raise_for_status()
            produtos = resposta.json()

            tabela.rows.clear()

            for produto in reversed(produtos):
                fornecedor_nome = produto.get("fornecedor", {}).get("nome", "N/A")

                botao_editar = ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.BLUE_400,
                    tooltip="Editar produto",
                    on_click=lambda e, p=produto: editar_produto(p)
                )

                botao_excluir = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_400,
                    tooltip="Deletar produto",
                    on_click=lambda e, pid=produto["id"]: deletar_produto(pid)
                )

                try:
                    preco_compra = float(produto["preco_compra"])
                    preco_venda = float(produto["preco_venda"])
                except (ValueError, TypeError):
                    preco_compra = 0.0
                    preco_venda = 0.0

                linha = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(produto["id"]))),
                        ft.DataCell(ft.Text(produto["nome"])),
                        ft.DataCell(ft.Text(produto.get("descricao", ""))),
                        ft.DataCell(ft.Text(produto["categoria"])),
                        ft.DataCell(ft.Text(f"R$ {preco_compra:.2f}")),
                        ft.DataCell(ft.Text(f"R$ {preco_venda:.2f}")),
                        ft.DataCell(ft.Text(str(produto["estoque"]))),
                        ft.DataCell(ft.Text(str(produto["estoque_min"]))),
                        ft.DataCell(ft.Text(fornecedor_nome)),
                        ft.DataCell(ft.Row([botao_editar, botao_excluir], spacing=5)),
                    ],
                    on_select_changed=lambda e, p=produto: editar_produto(p) if e.control.selected else None
                )

                tabela.rows.append(linha)

            pagina.update()
            mostrar_mensagem(f"Carregados {len(produtos)} produtos")
        except requests.exceptions.RequestException as e:
            mostrar_mensagem(f"Erro de conexão: {str(e)}", True)
        except json.JSONDecodeError:
            mostrar_mensagem("Erro ao decodificar resposta da API", True)
        except Exception as e:
            mostrar_mensagem(f"Erro inesperado: {str(e)}", True)

    def deletar_produto(produto_id):
        try:
            resposta = requests.delete(f"{URL_API}/{produto_id}")
            if resposta.status_code == 200:
                mostrar_mensagem("Produto deletado com sucesso!")
                carregar_produtos()
                if modo_edicao.current and id_produto_atual.current == produto_id:
                    definir_modo_edicao(False)
                    limpar_campos()
            elif resposta.status_code == 404:
                mostrar_mensagem("Produto não encontrado", True)
            else:
                mostrar_mensagem(f"Erro ao deletar produto: {resposta.status_code}", True)
        except requests.exceptions.RequestException as e:
            mostrar_mensagem(f"Erro de conexão: {str(e)}", True)
        except Exception as e:
            mostrar_mensagem(f"Erro inesperado: {str(e)}", True)

    def enviar_click(e):
        if not campo_nome.value or not campo_nome.value.strip():
            mostrar_mensagem("Nome do produto é obrigatório", True)
            return
        if not campo_categoria.value:
            mostrar_mensagem("Categoria é obrigatória", True)
            return
        if not campo_fornecedor_id.value:
            mostrar_mensagem("ID do fornecedor é obrigatório", True)
            return

        try:
            produto = {
                "nome": campo_nome.value.strip(),
                "descricao": campo_descricao.value.strip() if campo_descricao.value else "",
                "categoria": campo_categoria.value,
                "preco_compra": float(campo_preco_compra.value),
                "preco_venda": float(campo_preco_venda.value),
                "estoque": int(campo_estoque.value),
                "estoque_min": int(campo_estoque_min.value),
                "fornecedorId": int(campo_fornecedor_id.value)
            }

            resposta = requests.post(URL_API, json=produto, headers={"Content-Type": "application/json"})
            if resposta.status_code == 201:
                mostrar_mensagem("Produto cadastrado com sucesso!")
                limpar_campos()
                definir_modo_edicao(False)
                carregar_produtos()
            else:
                try:
                    erro_api = resposta.json()
                    mostrar_mensagem(f"Erro: {erro_api}", True)
                except:
                    mostrar_mensagem(f"Erro HTTP: {resposta.status_code}", True)
        except ValueError:
            mostrar_mensagem("Verifique os valores numéricos", True)
        except Exception as e:
            mostrar_mensagem(f"Erro: {str(e)}", True)

    def alterar_click(e):
        if not campo_nome.value or not campo_nome.value.strip():
            mostrar_mensagem("Nome do produto é obrigatório", True)
            return
        if not campo_categoria.value:
            mostrar_mensagem("Categoria é obrigatória", True)
            return
        if not campo_fornecedor_id.value:
            mostrar_mensagem("ID do fornecedor é obrigatório", True)
            return

        try:
            produto = {
                "nome": campo_nome.value.strip(),
                "descricao": campo_descricao.value.strip() if campo_descricao.value else "",
                "categoria": campo_categoria.value,
                "preco_compra": float(campo_preco_compra.value),
                "preco_venda": float(campo_preco_venda.value),
                "estoque": int(campo_estoque.value),
                "estoque_min": int(campo_estoque_min.value),
                "fornecedorId": int(campo_fornecedor_id.value)
            }

            resposta = requests.put(f"{URL_API}/{id_produto_atual.current}", json=produto, headers={"Content-Type": "application/json"})
            if resposta.status_code == 200:
                mostrar_mensagem("Produto alterado com sucesso!")
                limpar_campos()
                definir_modo_edicao(False)
                carregar_produtos()
            else:
                try:
                    erro_api = resposta.json()
                    mostrar_mensagem(f"Erro: {erro_api}", True)
                except:
                    mostrar_mensagem(f"Erro HTTP: {resposta.status_code}", True)
        except ValueError:
            mostrar_mensagem("Verifique os valores numéricos", True)
        except Exception as e:
            mostrar_mensagem(f"Erro: {str(e)}", True)

    def limpar_campos(e=None):
        campo_nome.value = ""
        campo_descricao.value = ""
        campo_categoria.value = None
        campo_preco_compra.value = ""
        campo_preco_venda.value = ""
        campo_estoque.value = ""
        campo_estoque_min.value = ""
        campo_fornecedor_id.value = ""
        pagina.update()

    def cancelar_edicao(e):
        definir_modo_edicao(False)
        limpar_campos()

    def botao_principal_click(e):
        if modo_edicao.current:
            alterar_click(e)
        else:
            enviar_click(e)

    botao_principal = ft.ElevatedButton("Enviar", on_click=botao_principal_click)
    botao_cancelar = ft.ElevatedButton("Cancelar", on_click=cancelar_edicao, bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE, visible=False)

    botoes = ft.Row([
        botao_principal,
        botao_cancelar,
        ft.ElevatedButton("Limpar", on_click=limpar_campos),
    ])

    campos_formulario = ft.Column([
        ft.Row([campo_nome, campo_descricao], spacing=10),
        ft.Row([campo_categoria, campo_preco_compra, campo_preco_venda], spacing=10),
        ft.Row([campo_estoque, campo_estoque_min, campo_fornecedor_id], spacing=10),
        botoes,
    ], spacing=15)

    container_formulario.content = campos_formulario

    layout = ft.Column([
        titulo,
        container_formulario,
        ft.Divider(),
        ft.Text("Lista de Produtos", size=24, weight="bold"),
        ft.Container(
            content=ft.Column([tabela], scroll=ft.ScrollMode.ALWAYS),
            padding=10,
            border_radius=5,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            expand=True,
            height=500
        )
    ], spacing=24, scroll=ft.ScrollMode.AUTO)

    carregar_produtos()
    return layout
