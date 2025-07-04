import { PrismaClient } from "@prisma/client"
import { Router } from "express"
import bcrypt from 'bcrypt'
import jwt from "jsonwebtoken"

const prisma = new PrismaClient()

const router = Router()

router.post("/", async (req, res) => {
    const { email, senha } = req.body

    // em termos de segurança, o recomendado é exibir uma mensagem padrão
    // a fim de evitar de dar "dicas" sobre o processo de login para hackers
    const mensaPadrao = "Login ou senha incorretos"

    if (!email || !senha) {
        // res.status(400).json({ erro: "Informe e-mail e senha do usuário" })
        res.status(400).json({ erro: mensaPadrao })
        return
    }

    try {
        const usuario = await prisma.usuario.findFirst({
            where: { email }
        })

        if (usuario == null) {
            // res.status(400).json({ erro: "E-mail inválido" })
            res.status(400).json({ erro: mensaPadrao })
            return
        }

        if (usuario.ativo === false) {
            res.status(400).json({ erro: "Usuário desativado após muitas tentativas incorretas" })
            return
        }

        // se o e-mail existe, faz-se a comparação dos hashs
        if (bcrypt.compareSync(senha, usuario.senha)) {

            // Captura o último acesso antes de atualizar
            const ultimoAcessoAnterior = usuario.ultimoAcesso
            console.log("senha correta")
            // se usuário legítimo, gera-se o token
            try {
                // Registra o log de acesso bem-sucedido
                await prisma.usuario.update({
                    where: { id: usuario.id },
                    data: {
                        tentativas: 0, // zera as tentativas
                        ultimoAcesso: new Date() // atualiza o último acesso
                    }
                })
                
                console.log("Último acesso atualizado para:", new Date())
            } catch (error) {
                console.error("Erro ao atualizar o último acesso:", error)
                res.status(500).json({ erro: "Erro ao registrar o acesso" })
                return
            }
            const token = jwt.sign({
                userLogadoId: usuario.id,
                userLogadoNome: usuario.nome
            },
                process.env.JWT_KEY as string,
                { expiresIn: "1h" }
            )

            // Prepara a mensagem de boas-vindas com último acesso
            console.log("Último acesso anterior:", ultimoAcessoAnterior)
            let mensagemBoasVindas = `Bem-vindo ${usuario.nome}. `
            if (ultimoAcessoAnterior) {
                const dataFormatada = ultimoAcessoAnterior.toLocaleString('pt-BR', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                })
                mensagemBoasVindas += `Seu último acesso ao sistema foi em ${dataFormatada}`
            } else {
                mensagemBoasVindas += `Este é o seu primeiro acesso ao sistema`
            }

            res.status(200).json({
                id: usuario.id,
                nome: usuario.nome,
                email: usuario.email,
                token,
                mensagem: mensagemBoasVindas
            })
        } else {

            const acao = "Tentativa de acesso ao sistema"
            const descricao = "Usuário: " + usuario.id + " - " + usuario.nome

            // registra um log de erro de senha
            const log = await prisma.log.create({
                data: { acao, descricao, usuarioId: usuario.id }
            })
            // console.log(log)

            // Incrementa tentativas e desativa após 3 tentativas incorretas
            const novasTentativas = usuario.tentativas + 1
            await prisma.usuario.update({
                where: { id: usuario.id },
                data: {
                    tentativas: novasTentativas,
                    ultimoAcesso: new Date(),
                    ativo: novasTentativas >= 3 ? false : true // desativa após 3 tentativas
                }
            })

            res.status(400).json({ erro: mensaPadrao })
        }
    } catch (error) {
        res.status(400).json(error)
    }
})

export default router