import { PrismaClient, Clube, Jogador } from "@prisma/client"
import { Router } from "express"
import { z } from 'zod'

//const prisma = new PrismaClient()

const prisma = new PrismaClient({
    log: ['query', 'info', 'warn', 'error'],
})

const router = Router()

const jogadorSchema = z.object({
    nome: z.string().min(3,
        { message: "Nome deve ter, no mínimo, 3 caracteres" }),
    datanasc: z.string().datetime({message: "Informe uma data válida"}),
    salario: z.number().positive({message: "Salario deve ser um nomero positivo"}),
    nacionalidade: z.string(),
    clubeId: z.number()
    })

router.get("/", async (req, res) => {
    try {
        const jogadors = await prisma.jogador.findMany({
            orderBy: { id: 'desc' },
        })
        res.status(200).json(jogadors)
        // res.status(200).json(viagens)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})

router.post("/", async (req, res) => {
    const result = jogadorSchema.safeParse(req.body)

    if (!result.success) {
        res.status(400).json({ erro: result.error.issues })
        return
    }

    const { nome, datanasc, salario, nacionalidade, clubeId} = result.data

    try {
        const jogador = await prisma.jogador.create({
            data: { nome, datanasc, salario, nacionalidade, clubeId }
        })
        res.status(201).json(jogador)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

router.put("/:id", async (req, res) => {
    // recebe o id passado como parâmetro
    const { id } = req.params

//    const viagemSchema2 = viagemSchema.partial()

    const result = jogadorSchema.safeParse(req.body)

    if (!result.success) {
        res.status(400).json({ erro: result.error.issues })
        return
    }

    const { nome, datanasc, salario, nacionalidade, clubeId } = result.data

    try {
        const jogador = await prisma.jogador.update({
            where: { id: Number(id) },
            data: { nome, datanasc, salario, nacionalidade, clubeId }
        })
        res.status(200).json(jogador)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

router.delete("/:id", async (req, res) => {
    // recebe o id passado como parâmetro
    const { id } = req.params

    // realiza a exclusão da viagem
    try {
        const jogador = await prisma.jogador.delete({
            where: { id: Number(id) }
        })
        res.status(200).json(jogador)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

export default router