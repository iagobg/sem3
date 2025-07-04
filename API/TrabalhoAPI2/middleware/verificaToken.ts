import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

interface TokenInterface {
    userLogadoId: string
    userLogadoNome: string
}

declare global {
  namespace Express {
    interface Request {
      userLogadoId?: string
      userLogadoNome?: string
    }
  }
}

export function verificaToken(req: Request, res: Response, next: NextFunction) {
    // console.log("Esta rota irá solicitar o token...")
    // next()  // se existir, executa a função seguinte (ou seja, a chamada na rota)
    // res.json({ erro: "Erro" })
    const { authorization } = req.headers

    if (!authorization) {
        res.status(401).json({ erro: "Token não informado" })
        return
    }

    const token = authorization.split(" ")[1]

    try {
        const decode = jwt.verify(token, process.env.JWT_KEY as string)
        console.log(decode)
        const { userLogadoId, userLogadoNome } = decode as TokenInterface

        // acrescenta na requisição os dados do usuário logado
        req.userLogadoId = userLogadoId
        req.userLogadoNome = userLogadoNome

        next()
    } catch (erro) {
        res.status(401).json({ erro: "Token inválido" })
    }
}