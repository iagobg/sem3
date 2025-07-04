import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import { verificaToken } from '../middleware/verificaToken'

const prisma = new PrismaClient()
const router = Router()

const vendaSchema = z.object({
  clienteId: z.number().int().positive({ message: "ID do cliente deve ser positivo" }),
  produtoId: z.number().int().positive({ message: "ID do produto deve ser positivo" }),
  quantidade: z.number().int().positive({ message: "Quantidade deve ser positiva" })
})


router.get("/", verificaToken, async (req, res) => {
  try {
    const vendas = await prisma.venda.findMany({
      include: {
        cliente: true,
        produto: {
          include: {
            fornecedor: true
          }
        }
      }
    })
    res.status(200).json(vendas)
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})


router.post("/", verificaToken, async (req, res) => {
  const valida = vendaSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { clienteId, produtoId, quantidade } = valida.data


  const cliente = await prisma.cliente.findUnique({
    where: { id: clienteId }
  })

  if (!cliente) {
    res.status(400).json({ erro: "Cliente não encontrado" })
    return
  }


  const produto = await prisma.produto.findUnique({
    where: { id: produtoId }
  })

  if (!produto) {
    res.status(400).json({ erro: "Produto não encontrado" })
    return
  }


  if (produto.estoque < quantidade) {
    res.status(400).json({ 
      erro: `Estoque insuficiente. Disponível: ${produto.estoque}, Solicitado: ${quantidade}` 
    })
    return
  }

  const total = Number(produto.preco_venda) * quantidade


  if (Number(cliente.credito) < total) {
    res.status(400).json({ 
      erro: `Crédito insuficiente. Disponível: R$ ${cliente.credito}, Necessário: R$ ${total.toFixed(2)}` 
    })
    return
  }

  try {

    const [venda, produtoAtualizado, clienteAtualizado] = await prisma.$transaction([

      prisma.venda.create({
        data: {
          clienteId,
          produtoId,
          quantidade,
          preco_unitario: produto.preco_venda,
          total: total
        }
      }),

      prisma.produto.update({
        where: { id: produtoId },
        data: { estoque: { decrement: quantidade } }
      }),

      prisma.cliente.update({
        where: { id: clienteId },
        data: { credito: { decrement: total } }
      })
    ])

    res.status(201).json({ 
      venda, 
      produto: produtoAtualizado, 
      cliente: clienteAtualizado 
    })
  } catch (error) {
    res.status(400).json({ error })
  }
})


router.delete("/:id", verificaToken, async (req, res) => {
  const { id } = req.params

  try {
    const vendaExcluida = await prisma.venda.findUnique({
      where: { id: Number(id) }
    })

    if (!vendaExcluida) {
      res.status(404).json({ erro: "Venda não encontrada" })
      return
    }

    const [venda, produtoAtualizado, clienteAtualizado] = await prisma.$transaction([
      prisma.venda.delete({
        where: { id: Number(id) }
      }),
      prisma.produto.update({
        where: { id: vendaExcluida.produtoId },
        data: { estoque: { increment: vendaExcluida.quantidade } }
      }),
      prisma.cliente.update({
        where: { id: vendaExcluida.clienteId },
        data: { credito: { increment: Number(vendaExcluida.total) } }
      })
    ])

    res.status(200).json({ 
      venda, 
      produto: produtoAtualizado, 
      cliente: clienteAtualizado 
    })
  } catch (error) {
    res.status(400).json({ erro: error })
  }
})

router.get("/relatorio", verificaToken, async (req, res) => {
  const { dataInicio, dataFim } = req.query

  try {
    const where: any = {}
    
    if (dataInicio && dataFim) {
      where.data = {
        gte: new Date(dataInicio as string),
        lte: new Date(dataFim as string)
      }
    }

    const vendas = await prisma.venda.findMany({
      where,
      include: {
        cliente: true,
        produto: {
          include: {
            fornecedor: true
          }
        }
      },
      orderBy: {
        data: 'desc'
      }
    })

    const totalVendas = vendas.reduce((acc, venda) => acc + Number(venda.total), 0)
    const quantidadeVendas = vendas.length

    res.status(200).json({
      vendas,
      resumo: {
        quantidade_vendas: quantidadeVendas,
        total_vendas: totalVendas,
        ticket_medio: quantidadeVendas > 0 ? totalVendas / quantidadeVendas : 0
      }
    })
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})

export default router