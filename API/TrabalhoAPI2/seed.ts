import { PrismaClient, Categoria } from '@prisma/client'
const prisma = new PrismaClient()

function gerarDataVenda(base: Date, incremento: number) {
  const data = new Date(base)
  data.setDate(data.getDate() + incremento)
  return data
}

function gerarCNPJ(i: number) {
  return `${11123123123123+i}`
}

function gerarCPF(i: number) {
  return `${11123123123+i}`
}

const nomesClientes = [
  'Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda', 'Gabriel', 'Helena',
  'Igor', 'Juliana', 'Kleber', 'Larissa', 'Marcos', 'Natalia', 'Otávio', 'Patrícia',
  'Quintino', 'Rafaela', 'Samuel', 'Tatiane'
]

const nomesFornecedores = [
  'Distribuidora Alpha', 'Comercial Beta', 'Importadora Gama', 'Atacadão Delta',
  'Central Epsilon', 'Global Zeta', 'Fornecedora Eta', 'Distribuidora Theta',
  'Grupo Iota', 'Comércio Kappa'
]

const nomesProdutos = [
  'Notebook Dell', 'Mouse Logitech', 'Teclado Mecânico', 'Monitor LG', 'Headset Gamer',
  'Webcam HD', 'Pen Drive 64GB', 'HD Externo 1TB', 'Cabo HDMI', 'Carregador USB-C',
  'Smartphone Samsung', 'Tablet Lenovo', 'Impressora HP', 'Scanner Epson', 'Roteador TP-Link',
  'Caixa de Som JBL', 'Microfone Condensador', 'Luminária LED', 'Estabilizador APC', 'Cadeira Gamer'
]

async function main() {
  console.log('Limpando dados anteriores...')
  await prisma.venda.deleteMany()
  await prisma.produto.deleteMany()
  await prisma.cliente.deleteMany()
  await prisma.fornecedor.deleteMany()

  console.log('Criando fornecedores...')
  const fornecedores = []
  for (let i = 0; i < nomesFornecedores.length; i++) {
    const fornecedor = await prisma.fornecedor.create({
      data: {
        nome: nomesFornecedores[i],
        cnpj: gerarCNPJ(i),
        telefone: `(11) 90000-00${i.toString().padStart(2, '0')}`,
        email: `contato@${nomesFornecedores[i].toLowerCase().replace(/ /g, '')}.com`,
        endereco: `Rua ${i + 1}, Centro, Cidade - Estado`
      }
    })
    fornecedores.push(fornecedor)
  }

  console.log('Criando clientes...')
  const clientes = []
  for (let i = 0; i < nomesClientes.length; i++) {
    const cliente = await prisma.cliente.create({
      data: {
        nome: nomesClientes[i],
        cpf: gerarCPF(i),
        telefone: `(11) 98888-00${i.toString().padStart(2, '0')}`,
        email: `cliente${i}@email.com`,
        endereco: `Av. ${i + 1}, Bairro, Cidade`,
        credito: 2000 + (i % 5) * 1000
      }
    })
    clientes.push(cliente)
  }

  console.log('Criando produtos...')
  const produtos = []
  const categorias = Object.values(Categoria)
  for (let i = 0; i < nomesProdutos.length; i++) {
    const produto = await prisma.produto.create({
      data: {
        nome: nomesProdutos[i],
        descricao: `Descrição do ${nomesProdutos[i]}`,
        categoria: categorias[i % categorias.length],
        preco_compra: 50 + i * 10,
        preco_venda: 80 + i * 15,
        estoque: 10 + (i % 5) * 5,
        estoque_min: 3,
        fornecedorId: fornecedores[i % fornecedores.length].id
      }
    })
    produtos.push(produto)
  }

  console.log('Criando vendas...')
  const dataBase = new Date('2025-01-01')
  let vendasCriadas = 0
  let dia = 0

  while (vendasCriadas < 50) {
    const cliente = clientes[Math.floor(Math.random() * clientes.length)]
    const produto = produtos[Math.floor(Math.random() * produtos.length)]

    const quantidade = Math.floor(Math.random() * 3) + 1
    const preco = produto.preco_venda
    const total = Number(preco) * quantidade

    if (Number(cliente.credito) >= total && produto.estoque >= quantidade) {
      await prisma.venda.create({
        data: {
          clienteId: cliente.id,
          produtoId: produto.id,
          quantidade,
          preco_unitario: preco,
          total,
          data: gerarDataVenda(dataBase, dia++)
        }
      })

      await prisma.produto.update({
        where: { id: produto.id },
        data: { estoque: { decrement: quantidade } }
      })

      await prisma.cliente.update({
        where: { id: cliente.id },
        data: { credito: { decrement: total } }
      })

      vendasCriadas++
    }
  }

  console.log(`Seed finalizado com sucesso!`)
  console.log(`Fornecedores: ${fornecedores.length}`)
  console.log(`Clientes: ${clientes.length}`)
  console.log(`Produtos: ${produtos.length}`)
  console.log(`Vendas: ${vendasCriadas}`)
}

main()
  .catch((e) => {
    console.error('Erro durante o seed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
