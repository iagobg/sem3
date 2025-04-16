import {Router} from 'express'
import { PrismaClient } from '@prisma/client'

const router = Router()
const prisma = new PrismaClient()


router.get('/',async(req,res) =>{
    const filmes = await prisma.filme.findMany()
    res.status(200).json(filmes)
})

router.post('/', async(req, res) => {
    const { titulo, genero, duracao, preco, datacad, sinopse } = req.body

    if( !titulo || !genero || !duracao || !preco){
        res.status(400).json({erro:"Dados incompletos"})
    }

    const filme = await prisma.filme.create({
        data: {titulo, genero, duracao, preco}
    })

    res.status(201).json(filme)
})

router.put('/:id', async(req,res) =>{
    const {id} = req.params;

    
})

router.delete('/:id', async(req,res) => {
    const { id } = req.params;

    const filmealvo = await prisma.filme.findUnique({
        where: {id: parseInt(id)}
    });

    if (!filmealvo){
        res.status(400).json({erro: "Filme não encontrado"})
        return
    }

    await prisma.filme.delete({
        where: {id: parseInt(id)}
    });
    res.status(200).json({mensagem: "Filme deletado com sucesso"});



});

export default router
