import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import { verificaToken } from '../middleware/verificaToken'

const prisma = new PrismaClient()
const router = Router()

const fornecedorSchema = z.object({
  nome: z.string().min(3, { message: "Nome deve possuir, no mínimo, 3 caracteres" }),
  cnpj: z.string().min(14, { message: "CNPJ deve possuir 14 caracteres" }),
  telefone: z.string().min(10, { message: "Telefone deve possuir, no mínimo, 10 caracteres" }),
  email: z.string().email().min(5, { message: "E-mail deve ser válido" }),
  endereco: z.string().min(10, { message: "Endereço deve possuir, no mínimo, 10 caracteres" })
})

router.get("/", verificaToken, async (req, res) => {
  try {
    const fornecedores = await prisma.fornecedor.findMany({
      include: {
        produtos: true
      }
    })
    res.status(200).json(fornecedores)
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})

router.post("/", verificaToken, async (req, res) => {
  const valida = fornecedorSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { nome, cnpj, telefone, email, endereco } = valida.data

  try {
    const fornecedor = await prisma.fornecedor.create({
      data: { nome, cnpj, telefone, email, endereco }
    })
    res.status(201).json(fornecedor)
  } catch (error) {
    res.status(400).json({ error })
  }
})


router.put("/:id", verificaToken, async (req, res) => {
  const { id } = req.params
  
  const valida = fornecedorSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { nome, cnpj, telefone, email, endereco } = valida.data

  try {
    const fornecedor = await prisma.fornecedor.update({
      where: { id: Number(id) },
      data: { nome, cnpj, telefone, email, endereco }
    })
    res.status(200).json(fornecedor)
  } catch (error) {
    res.status(400).json({ error })
  }
})

router.delete("/:id", verificaToken, async (req, res) => {
  const { id } = req.params

  try {
    const fornecedor = await prisma.fornecedor.delete({
      where: { id: Number(id) }
    })
    res.status(200).json(fornecedor)
  } catch (error) {
    res.status(400).json({ erro: error })
  }
})

export default router