import { PrismaClient, Clube, Jogador } from "@prisma/client"
import { Router } from "express"
import { z } from 'zod'

//const prisma = new PrismaClient()

const prisma = new PrismaClient({
    log: ['query', 'info', 'warn', 'error'],
})

const router = Router()

const clubeSchema = z.object({
    nome: z.string().min(3,
        { message: "Nome deve ter, no mínimo, 3 caracteres" }),
    estado: z.string().length(2,
        {message: "Estado deve possuir 2 caracterers"})
    })

router.get("/", async (req, res) => {
    try {
        const clubes = await prisma.clube.findMany({
            orderBy: { id: 'desc' },
        })
        res.status(200).json(clubes)
        // res.status(200).json(viagens)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})

router.post("/", async (req, res) => {
    const result = clubeSchema.safeParse(req.body)

    if (!result.success) {
        res.status(400).json({ erro: result.error.issues })
        return
    }

    const { nome, estado} = result.data

    try {
        const clube = await prisma.clube.create({
            data: { nome, estado }
        })
        res.status(201).json(clube)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

router.put("/:id", async (req, res) => {
    // recebe o id passado como parâmetro
    const { id } = req.params

//    const viagemSchema2 = viagemSchema.partial()

    const result = clubeSchema.safeParse(req.body)

    if (!result.success) {
        res.status(400).json({ erro: result.error.issues })
        return
    }

    const { nome, estado } = result.data

    try {
        const clube = await prisma.clube.update({
            where: { id: Number(id) },
            data: { nome, estado }
        })
        res.status(200).json(clube)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

router.delete("/:id", async (req, res) => {
    // recebe o id passado como parâmetro
    const { id } = req.params

    // realiza a exclusão da viagem
    try {
        const clube = await prisma.clube.delete({
            where: { id: Number(id) }
        })
        res.status(200).json(clube)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

export default router