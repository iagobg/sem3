import { PrismaClient, Categoria } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  console.log('Iniciando seed do banco de dados...')

  // Limpar dados existentes
  await prisma.venda.deleteMany()
  await prisma.produto.deleteMany()
  await prisma.cliente.deleteMany()
  await prisma.fornecedor.deleteMany()

  // Criar fornecedores
  const fornecedor1 = await prisma.fornecedor.create({
    data: {
      nome: 'Tech Solutions Ltda',
      cnpj: '12.345.678/0001-90',
      telefone: '(11) 99999-1234',
      email: 'contato@techsolutions.com',
      endereco: 'Rua das Tecnologias, 123 - São Paulo, SP'
    }
  })

  const fornecedor2 = await prisma.fornecedor.create({
    data: {
      nome: 'Moda & Estilo',
      cnpj: '98.765.432/0001-10',
      telefone: '(11) 88888-5678',
      email: 'vendas@modaestilo.com',
      endereco: 'Av. da Moda, 456 - Rio de Janeiro, RJ'
    }
  })

  // Criar clientes
  const cliente1 = await prisma.cliente.create({
    data: {
      nome: 'João Silva Santos',
      cpf: '123.456.789-00',
      telefone: '(11) 91234-5678',
      email: 'joao.silva@email.com',
      endereco: 'Rua A, 123 - Centro, São Paulo, SP',
      credito: 5000.00
    }
  })

  const cliente2 = await prisma.cliente.create({
    data: {
      nome: 'Maria Oliveira Costa',
      cpf: '987.654.321-00',
      telefone: '(11) 98765-4321',
      email: 'maria.costa@email.com',
      endereco: 'Av. B, 456 - Jardins, São Paulo, SP',
      credito: 3000.00
    }
  })

  // Criar produtos
  const produto1 = await prisma.produto.create({
    data: {
      nome: 'Notebook Dell Inspiron',
      descricao: 'Notebook com processador Intel i5, 8GB RAM, SSD 256GB',
      categoria: Categoria.ELETRONICOS,
      preco_compra: 2000.00,
      preco_venda: 2800.00,
      estoque: 10,
      estoque_min: 3,
      fornecedorId: fornecedor1.id
    }
  })

  const produto2 = await prisma.produto.create({
    data: {
      nome: 'Mouse Wireless Logitech',
      descricao: 'Mouse sem fio com precisão óptica',
      categoria: Categoria.ELETRONICOS,
      preco_compra: 50.00,
      preco_venda: 89.90,
      estoque: 25,
      estoque_min: 5,
      fornecedorId: fornecedor1.id
    }
  })

  const produto3 = await prisma.produto.create({
    data: {
      nome: 'Camiseta Polo Masculina',
      descricao: 'Camiseta polo 100% algodão, diversas cores',
      categoria: Categoria.ROUPAS,
      preco_compra: 25.00,
      preco_venda: 49.90,
      estoque: 50,
      estoque_min: 10,
      fornecedorId: fornecedor2.id
    }
  })

  const produto4 = await prisma.produto.create({
    data: {
      nome: 'Livro "Programação com Node.js"',
      descricao: 'Guia completo para desenvolvimento backend',
      categoria: Categoria.LIVROS,
      preco_compra: 30.00,
      preco_venda: 59.90,
      estoque: 15,
      estoque_min: 5,
      fornecedorId: fornecedor1.id
    }
  })

  // Criar algumas vendas de exemplo
  await prisma.venda.create({
    data: {
      clienteId: cliente1.id,
      produtoId: produto2.id,
      quantidade: 2,
      preco_unitario: 89.90,
      total: 179.80
    }
  })

  await prisma.venda.create({
    data: {
      clienteId: cliente2.id,
      produtoId: produto3.id,
      quantidade: 3,
      preco_unitario: 49.90,
      total: 149.70
    }
  })

  // Atualizar estoque e crédito dos clientes após as vendas
  await prisma.produto.update({
    where: { id: produto2.id },
    data: { estoque: { decrement: 2 } }
  })

  await prisma.produto.update({
    where: { id: produto3.id },
    data: { estoque: { decrement: 3 } }
  })

  await prisma.cliente.update({
    where: { id: cliente1.id },
    data: { credito: { decrement: 179.80 } }
  })

  await prisma.cliente.update({
    where: { id: cliente2.id },
    data: { credito: { decrement: 149.70 } }
  })

  console.log('Seed concluído com sucesso!')
  console.log('Dados criados:')
  console.log('- 2 Fornecedores')
  console.log('- 2 Clientes')
  console.log('- 4 Produtos')
  console.log('- 2 Vendas')
}

main()
  .catch((e) => {
    console.error('Erro durante o seed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })