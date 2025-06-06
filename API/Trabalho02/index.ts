import express from 'express';

import routesClientes from './routes/clientes'
import routesPets from './routes/pets'
import routesServices from './routes/servicos'
import routesAppointments from './routes/agendamentos'
import routesItensAgendamentos from './routes/itensAgendamentos'

const app = express();
const PORT = 3000;


app.use("/clientes", routesClientes)
app.use("/pets", routesPets)
app.use("/servicos", routesServices)
app.use("/agendamentos", routesAppointments)
app.use("/itensAgendamentos", routesItensAgendamentos)

app.get('/', (req,res) => {
  res.send('API: Pet Shop')
})

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta: ${PORT}`)
})