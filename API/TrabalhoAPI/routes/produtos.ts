import { PrismaClient, Categoria } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'

const prisma = new PrismaClient()
const router = Router()

const produtoSchema = z.object({
  nome: z.string().min(3, { message: "Nome deve possuir, no mínimo, 3 caracteres" }),
  descricao: z.string().optional(),
  categoria: z.nativeEnum(Categoria),
  preco_compra: z.number().positive({ message: "Preço de compra deve ser positivo" }),
  preco_venda: z.number().positive({ message: "Preço de venda deve ser positivo" }),
  estoque: z.number().int().min(0, { message: "Estoque não pode ser negativo" }),
  estoque_min: z.number().int().min(1, { message: "Estoque mínimo deve ser pelo menos 1" }),
  fornecedorId: z.number().int().positive({ message: "ID do fornecedor deve ser positivo" })
})


router.get("/", async (req, res) => {
  try {
    const produtos = await prisma.produto.findMany({
      include: {
        fornecedor: true,
        vendas: true
      }
    })
    res.status(200).json(produtos)
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})


router.post("/", async (req, res) => {
  const valida = produtoSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { nome, descricao, categoria, preco_compra, preco_venda, estoque, estoque_min, fornecedorId } = valida.data


  const fornecedor = await prisma.fornecedor.findUnique({
    where: { id: fornecedorId }
  })

  if (!fornecedor) {
    res.status(400).json({ erro: "Fornecedor não encontrado" })
    return
  }

  try {
    const produto = await prisma.produto.create({
      data: { 
        nome, 
        descricao, 
        categoria, 
        preco_compra, 
        preco_venda, 
        estoque, 
        estoque_min, 
        fornecedorId 
      }
    })
    res.status(201).json(produto)
  } catch (error) {
    res.status(400).json({ error })
  }
})


router.put("/:id", async (req, res) => {
  const { id } = req.params
  
  const valida = produtoSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { nome, descricao, categoria, preco_compra, preco_venda, estoque, estoque_min, fornecedorId } = valida.data


  const fornecedor = await prisma.fornecedor.findUnique({
    where: { id: fornecedorId }
  })

  if (!fornecedor) {
    res.status(400).json({ erro: "Fornecedor não encontrado" })
    return
  }

  try {
    const produto = await prisma.produto.update({
      where: { id: Number(id) },
      data: { 
        nome, 
        descricao, 
        categoria, 
        preco_compra, 
        preco_venda, 
        estoque, 
        estoque_min, 
        fornecedorId 
      }
    })
    res.status(200).json(produto)
  } catch (error) {
    res.status(400).json({ error })
  }
})


router.delete("/:id", async (req, res) => {
  const { id } = req.params

  try {
    const produto = await prisma.produto.delete({
      where: { id: Number(id) }
    })
    res.status(200).json(produto)
  } catch (error) {
    res.status(400).json({ erro: error })
  }
})


router.get("/estoque-baixo", async (req, res) => {
  try {
    const produtos = await prisma.produto.findMany({
      where: {
        estoque: {
          lte: prisma.produto.fields.estoque_min
        }
      },
      include: {
        fornecedor: true
      }
    })
    res.status(200).json(produtos)
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})

export default router