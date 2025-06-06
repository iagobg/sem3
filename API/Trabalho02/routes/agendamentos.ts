import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'

const prisma = new PrismaClient()

const router = Router()

const agendamentosSchema = z.object({
    clienteId: z.number(),
    petId: z.number(),
    nome: z.string().min(5,
        {message: "Nome deve pssuir, no mínimo, 5 caracteres"}),
    email: z.string().email(
        {message: "Email inválido"})
})

router.get("/",async (req, res) => {
    try {
        const agendamentos = await prisma.agendamento.findMany()
        res.status(200).json(agendamentos)
    } catch (error) {
        res.status(500).json({ erro:error})
    }
})

router.post("/", async(req, res) => {
    const valida = agendamentosSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error})
        return
    }

    const {nome, email} = valida.data

    try {
        const agendamento = await prisma.agendamento.create({
            data: {nome, email}
        })
        res.status(201).json(agendamento)
    } catch(error) {
        res.status(400).json({error})
    }
})

router.delete("/:id", async (req,res) =>{
    const {id} = req.params

    try {
        const agendamento = await prisma.agendamento.delete({
            where: { id: Number(id)}
        })
        res.status(200).json(agendamento)
    } catch(error) {
        res.status(400).json({erro: error})
    }
})


export default router