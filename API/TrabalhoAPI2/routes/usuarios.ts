import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import bcrypt from 'bcrypt'
import { verificaToken } from '../middleware/verificaToken'

const prisma = new PrismaClient()

const router = Router()

const usuarioSchema = z.object({
    nome: z.string().min(10,
        { message: "Nome deve possuir, no mínimo, 10 caracteres" }),
    email: z.string().email().min(10,
        { message: "E-mail, no mínimo, 10 caracteres" }),
    senha: z.string(),
    clienteId: z.string().optional(),
    ativo: z.boolean().optional()
})

router.get("/", async (req, res) => {
    try {
        const usuarios = await prisma.usuario.findMany()
        res.status(200).json(usuarios)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})


function validaSenha(senha: string) {

    const mensa: string[] = []

    if (senha.length < 8) {
        mensa.push("Erro... senha deve possuir, no mínimo, 8 caracteres")
    }

    let pequenas = 0
    let grandes = 0
    let numeros = 0
    let simbolos = 0

    for (const letra of senha) {
        if ((/[a-z]/).test(letra)) {
            pequenas++
        }
        else if ((/[A-Z]/).test(letra)) {
            grandes++
        }
        else if ((/[0-9]/).test(letra)) {
            numeros++
        } else {
            simbolos++
        }
    }

    if (pequenas == 0) {
        mensa.push("Erro... senha deve possuir letra(s) minúscula(s)")
    }

    if (grandes == 0) {
        mensa.push("Erro... senha deve possuir letra(s) maiúscula(s)")
    }

    if (numeros == 0) {
        mensa.push("Erro... senha deve possuir número(s)")
    }

    if (simbolos == 0) {
        mensa.push("Erro... senha deve possuir símbolo(s)")
    }

    return mensa
}
router.post("/", async (req, res) => {
    const valida = usuarioSchema.safeParse(req.body);
    if (!valida.success) {
        res.status(400).json({ erro: valida.error });
        return;
    }
    const { nome, email, senha, clienteId } = valida.data;
    
    const mensagensErro = validaSenha(senha);
    if (mensagensErro.length > 0) {
        res.status(400).json({ erro: mensagensErro.join("; ") });
        return;
    }
    
    if (clienteId) {
        const cliente = await prisma.cliente.findUnique({
            where: { id: Number(clienteId) }
        });
        if (!cliente) {
            res.status(400).json({ erro: "Cliente não encontrado" });
            return;
        }

        if (cliente.usuarioId) {
            res.status(400).json({ erro: "Cliente já possui um usuário vinculado" });
            return;
        }
    }
    
    const salt = bcrypt.genSaltSync(12);
    const hash = bcrypt.hashSync(senha, salt);
    
    try {
        const result = await prisma.$transaction(async (prisma) => {
            const usuario = await prisma.usuario.create({
                data: { nome, email, senha: hash }
            });
            
            if (clienteId) {
                await prisma.cliente.update({
                    where: { id: Number(clienteId) },
                    data: { usuarioId: usuario.id }
                });
            }
            
            return usuario;
        });
        
        res.status(201).json(result);
    } catch (error) {
        console.error("Error creating user:", error);
        res.status(400).json({ erro: "Erro ao criar usuário" });
    }
});

router.delete("/:id", async (req, res) => {
    const { id } = req.params

    try {
        const usuario = await prisma.usuario.delete({
            where: { id }
        })
        res.status(200).json(usuario)
    } catch (error) {
        res.status(400).json({ erro: error })
    }
})

router.put("/:id", async (req, res) => {
    const { id } = req.params

    const valida = usuarioSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    const { nome, email, senha } = valida.data

    try {
        const usuario = await prisma.usuario.update({
            where: { id },
            data: { nome, email, senha}
        })
        res.status(200).json(usuario)
    } catch (error) {
        res.status(400).json({ error })
    }
})

export default router
