import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'

const prisma = new PrismaClient()

const router = Router()

const clientesSchema = z.object({
    nome: z.string().min(5,
        {message: "Nome deve pssuir, no mínimo, 5 caracteres"}),
    email: z.string().email(
        {message: "Email inválido"})
})

router.get("/",async (req, res) => {
    try {
        const clientes = await prisma.cliente.findMany()
        res.status(200).json(clientes)
    } catch (error) {
        res.status(500).json({ erro:error})
    }
})

router.post("/", async(req, res) => {
    const valida = clientesSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error})
        return
    }

    const {nome, email} = valida.data

    try {
        const cliente = await prisma.cliente.create({
            data: {nome, email}
        })
        res.status(201).json(cliente)
    } catch(error) {
        res.status(400).json({error})
    }
})

router.delete("/:id", async (req,res) =>{
    const {id} = req.params

    try {
        const cliente = await prisma.cliente.delete({
            where: { id: Number(id)}
        })
        res.status(200).json(cliente)
    } catch(error) {
        res.status(400).json({erro: error})
    }
})


export default router