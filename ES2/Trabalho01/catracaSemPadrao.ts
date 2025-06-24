class CatracaSemPadrao {
    private cartaoValido: boolean = false;
    private liberada: boolean = false;
    private bloqueada: boolean = false;
    private passando: boolean = false;
    private usuarioAtual: string = "";

    lerCartao(nomeUsuario: string, cartaoValido: boolean): void {
        if (this.passando) {
            console.log("Aguarde, usuário passando pela catraca...");
            return;
        }

        if (this.bloqueada) {
            console.log("Catraca bloqueada! Contacte o administrador.");
            return;
        }

        if (!cartaoValido) {
            console.log("Cartão inválido! Acesso negado.");
            this.bloquearTemporariamente();
            return;
        }

        this.cartaoValido = true;
        this.usuarioAtual = nomeUsuario;
        this.liberada = true;
        console.log(`Cartão válido! Acesso liberado para ${nomeUsuario}.`);
        console.log("Passe pela catraca em 10 segundos...");


        setTimeout(() => {
            if (this.liberada && !this.passando) {
                this.resetar();
                console.log("Tempo esgotado! Catraca bloqueada novamente.");
            }
        }, 10000);
    }

    passarPelaCatraca(): void {
        if (this.bloqueada) {
            console.log("Catraca bloqueada! Acesso negado.");
            return;
        }

        if (!this.liberada) {
            console.log("Apresente um cartão válido primeiro!");
            return;
        }

        if (this.passando) {
            console.log("Aguarde, usuário passando...");
            return;
        }

        this.passando = true;
        console.log(`${this.usuarioAtual} passando pela catraca...`);


        setTimeout(() => {
            console.log(`${this.usuarioAtual} passou pela catraca com sucesso!`);
            this.resetar();
        }, 2000);
    }

    private bloquearTemporariamente(): void {
        this.bloqueada = true;
        console.log("Catraca bloqueada por 5 segundos devido a cartão inválido.");
        
        setTimeout(() => {
            this.bloqueada = false;
            console.log("Catraca desbloqueada.");
        }, 5000);
    }

    private resetar(): void {
        this.cartaoValido = false;
        this.liberada = false;
        this.passando = false;
        this.usuarioAtual = "";
    }

    obterStatus(): string {
        if (this.bloqueada) return "Bloqueada";
        if (this.passando) return "Usuário passando";
        if (this.liberada) return "Liberada - aguardando passagem";
        return "Aguardando cartão";
    }

    desbloquearForcado(): void {
        this.bloqueada = false;
        this.resetar();
        console.log("Catraca desbloqueada pelo administrador.");
    }
}





// EXEMPLO DE USO
const catraca1 = new CatracaSemPadrao();


console.log("=== TESTE SEM PADRÃO STATE ===");

// Esse é um teste simples para verificar o funcionamento da catraca.
// O cenário é o seguinte:
// 1. Usuário tenta passar sem cartão lido (deve falhar).
// 2. Usuário lê um cartão válido (deve ser bem-sucedido).
// 3. Usuário tenta passar pela catraca (deve ser bem-sucedido).
// 4. Usuário tenta ler um cartão enquanto outro está passando (deve falhar).
// 5. Usuário lê um cartão válido após o anterior passar (deve ser bem-sucedido).
// 6. Usuário tenta passar novamente (deve falhar pois demorou demais).



console.log("Status:", catraca1.obterStatus());
setTimeout(() => catraca1.passarPelaCatraca(), 2000); // Usuário não passa pois não há cartão lido
setTimeout(() => catraca1.lerCartao("João Silva", true), 4000); // Deve ser bem-sucedido pois é um cartão válido
setTimeout(() => catraca1.passarPelaCatraca(), 6000); // Usuário passa, pois a catraca está liberada
setTimeout(() => catraca1.lerCartao("Maria Santos", true), 7000); // Deve falhar pois alguém está passando
setTimeout(() => catraca1.lerCartao("Maria Santos", true), 10000); // Deve ser bem sucedida pois o usuario anterior já passou
setTimeout(() => catraca1.passarPelaCatraca(), 20000); // Usuário não passa pois demorou demais.


