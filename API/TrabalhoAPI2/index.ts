import express from 'express';
import clientesRouter from './routes/clientes';
import fornecedoresRouter from './routes/fornecedores';
import produtosRouter from './routes/produtos';
import vendasRouter from './routes/vendas';
import loginRouter from './routes/login';
import usuariosRouter from './routes/usuarios';
import segurancaRouter from './routes/seguranca';
import dotenv from 'dotenv'


dotenv.config()

const app = express();
const port = 3000;

app.use(express.json());

app.use('/clientes', clientesRouter);
app.use('/fornecedores', fornecedoresRouter);
app.use('/produtos', produtosRouter);
app.use('/vendas', vendasRouter);
app.use('/login', loginRouter);
app.use('/usuarios', usuariosRouter);


app.use('/seguranca', segurancaRouter);


app.get('/', (_req, res) => {
  res.status(200).send('Trabalho API: Sistema de vendas');
});

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
  console.log(`Acesse: http://localhost:${port}`);
});

export default app;