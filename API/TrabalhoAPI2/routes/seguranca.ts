import { PrismaClient } from '@prisma/client'
import { Router, Request, Response } from 'express'
import fs from 'fs'
import path from 'path'
import { verificaToken } from '../middleware/verificaToken'

const prisma = new PrismaClient()
const router = Router()

router.get('/backup', verificaToken, async (req, res) => {
    try {
        const usuarios = await prisma.usuario.findMany()
        const clientes = await prisma.cliente.findMany()
        const produtos = await prisma.produto.findMany()
        const fornecedores = await prisma.fornecedor.findMany()
        const vendas = await prisma.venda.findMany()
        const logs = await prisma.log.findMany()

        const dadosBackup = {
            usuarios,
            clientes,
            produtos,
            fornecedores,
            vendas,
            logs,
            dataBackup: new Date().toISOString()
        }
        const caminho = path.resolve(process.cwd(), 'backup.json');
        console.log('Salvando backup em:', caminho);
        fs.writeFileSync(caminho, JSON.stringify(dadosBackup, null, 2))

        res.json({ mensagem: 'Backup gerado com sucesso!', arquivo: 'backup.json' })
    } catch (erro) {
        console.error(erro)
        res.status(500).json({ erro: 'Erro ao gerar o backup.' })
    }
})

router.post('/restore', verificaToken, async (req: any, res: any) => {
    try {
        const caminho = path.resolve(process.cwd(), 'backup.json')
        if (!fs.existsSync(caminho)) {
            return res.status(404).json({ erro: 'Arquivo de backup.json não encontrado.' })
        }

        const conteudo = fs.readFileSync(caminho, 'utf8')
        const dados = JSON.parse(conteudo)

        // 1. Deletar todos os registros (ordem reversa das relações)
        await prisma.log.deleteMany();
        await prisma.venda.deleteMany();
        await prisma.cliente.deleteMany();
        await prisma.produto.deleteMany();
        await prisma.fornecedor.deleteMany();
        await prisma.usuario.deleteMany();


        // 2. Inserir os dados (ordem correta para respeitar as chaves estrangeiras (FKs))
        for (const usuario of dados.usuarios) {
            await prisma.usuario.create({ data: usuario });
        }

        for (const fornecedor of dados.fornecedores) {
            await prisma.fornecedor.create({ data: fornecedor });
        }

        for (const produto of dados.produtos) {
            await prisma.produto.create({ data: produto });
        }

        for (const cliente of dados.clientes) {
            await prisma.cliente.create({ data: cliente });
        }

        for (const venda of dados.vendas) {
            await prisma.venda.create({ data: venda });
        }

        for (const log of dados.logs) {
            await prisma.log.create({ data: log });
        }

        res.json({ mensagem: 'Dados restaurados com sucesso a partir do backup' })

    } catch (erro) {
        console.error(erro)
        res.status(500).json({ erro: 'Erro ao restaurar os dados.' })
    }
})

export default router