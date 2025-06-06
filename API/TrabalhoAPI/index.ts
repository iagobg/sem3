import express from 'express'
import clientesRouter from './routes/clientes'
import fornecedoresRouter from './routes/fornecedores'
import produtosRouter from './routes/produtos'
import vendasRouter from './routes/vendas'

const app = express()
const port = 3000

app.use(express.json())

app.use('/clientes', clientesRouter)
app.use('/fornecedores', fornecedoresRouter)
app.use('/produtos', produtosRouter)
app.use('/vendas', vendasRouter)


app.get('/', (req, res) => {
  res.send('Trabalho API: Sistema de vendas')
})

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`)
  console.log(`Acesse: http://localhost:${port}`)
})

export default app