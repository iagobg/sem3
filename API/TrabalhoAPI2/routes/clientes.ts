import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import nodemailer from "nodemailer"
import { verificaToken } from '../middleware/verificaToken'

const prisma = new PrismaClient()
const router = Router()

const clienteSchema = z.object({
  nome: z.string().min(3, { message: "Nome deve possuir, no mínimo, 3 caracteres" }),
  cpf: z.string().min(11, { message: "CPF deve possuir 11 caracteres" }),
  telefone: z.string().min(10, { message: "Telefone deve possuir, no mínimo, 10 caracteres" }),
  email: z.string().email().min(5, { message: "E-mail deve ser válido" }),
  endereco: z.string().min(10, { message: "Endereço deve possuir, no mínimo, 10 caracteres" }),
  credito: z.number().optional()
})

router.get("/", verificaToken, async (req, res) => {
  try {
    const clientes = await prisma.cliente.findMany({
      include: {
        vendas: {
          include: {
            produto: true
          }
        }
      }
    })
    res.status(200).json(clientes)
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})

router.post("/", verificaToken, async (req, res) => {
  const valida = clienteSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { nome, cpf, telefone, email, endereco, credito } = valida.data

  try {
    const cliente = await prisma.cliente.create({
      data: { nome, cpf, telefone, email, endereco, credito: credito || 0 }
    })
    res.status(201).json(cliente)
  } catch (error) {
    res.status(400).json({ error })
  }
})

router.put("/:id", verificaToken, async (req, res) => {
  const { id } = req.params
  
  const valida = clienteSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  const { nome, cpf, telefone, email, endereco, credito } = valida.data

  try {
    const cliente = await prisma.cliente.update({
      where: { id: Number(id) },
      data: { nome, cpf, telefone, email, endereco, credito: credito || 0 }
    })
    res.status(200).json(cliente)
  } catch (error) {
    res.status(400).json({ error })
  }
})

router.delete("/:id", verificaToken, async (req, res) => {
  const { id } = req.params

  try {
    const cliente = await prisma.cliente.delete({
      where: { id: Number(id) }
    })
    res.status(200).json(cliente)
  } catch (error) {
    res.status(400).json({ erro: error })
  }
})

function gerarRelatorioHTML(dados: any) {
  let html = `
    <html>
    <body style="font-family: Arial, sans-serif;">
    <h2>Sistema de Vendas: Relatório de Compras</h2>
    <h3>Cliente: ${dados.nome} - CPF: ${dados.cpf}</h3>
    <h3>Telefone: ${dados.telefone}</h3>
    <h3>Endereço: ${dados.endereco}</h3>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
      <thead style="background-color: #f0f0f0;">
        <tr>
          <th>Data</th>
          <th>Produto</th>
          <th>Quantidade</th>
          <th>Preço Unit.</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
  `

  let totalGeral = 0
  for (const venda of dados.vendas) {
    totalGeral += Number(venda.total)
    
    const data = new Date(venda.data)
    const dataFormatada = data.toLocaleString('pt-BR', {
      timeZone: 'America/Sao_Paulo',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })

    html += `
      <tr>
        <td>${dataFormatada}</td>
        <td>${venda.produto.nome}</td>
        <td style="text-align: center;">${venda.quantidade}</td>
        <td style="text-align: right;">R$ ${Number(venda.preco_unitario).toLocaleString("pt-br", { minimumFractionDigits: 2 })}</td>
        <td style="text-align: right;">R$ ${Number(venda.total).toLocaleString("pt-br", { minimumFractionDigits: 2 })}</td>
      </tr>
    `
  }

  html += `
      <tr style="font-weight: bold; background-color: #e0e0e0;">
        <td colspan="4" style="text-align: right;">Total Geral:</td>
        <td style="text-align: right;">R$ ${totalGeral.toLocaleString("pt-br", { minimumFractionDigits: 2 })}</td>
      </tr>
    </tbody>
    </table>
    <h3>Crédito Disponível: R$ ${Number(dados.credito).toLocaleString("pt-br", { minimumFractionDigits: 2 })}</h3>
    </body>
    </html>
  `

  return html
}

const transporter = nodemailer.createTransport({
  host: "sandbox.smtp.mailtrap.io",
  port: 587,
  secure: false,
  auth: {
    user: "f32cf70b10fb9c", 
    pass: "6b738a1d5c3b71",
  },
})

async function enviaEmail(dados: any) {
  const mensagem = gerarRelatorioHTML(dados)

  const info = await transporter.sendMail({
    from: 'Sistema de Vendas <vendas@empresa.com>',
    to: dados.email,
    subject: "Relatório de Compras",
    text: "Seu relatório de compras em anexo.",
    html: mensagem,
  })

  console.log("Message sent:", info.messageId)
}

router.get("/email/:id", async (req, res) => {
  const { id } = req.params
  
  try {
    const cliente = await prisma.cliente.findFirst({
      where: { id: Number(id) },
      include: {
        vendas: {
          include: {
            produto: true
          }
        }
      }
    })

    if (!cliente) {
      res.status(404).json({ erro: "Cliente não encontrado" })
      return
    }

    await enviaEmail(cliente)
    res.status(200).json({ mensagem: "Email enviado com sucesso", cliente })
  } catch (error) {
    res.status(500).json({ erro: error })
  }
})

export default router