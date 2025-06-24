interface EstadoCatraca {
    lerCartao(contexto: CatracaComPadrao, nomeUsuario: string, cartaoValido: boolean): void;
    passarPelaCatraca(contexto: CatracaComPadrao): void;
    obterStatus(): string;
}


class CatracaComPadrao {
    private estado: EstadoCatraca;
    private usuarioAtual: string = "";

    constructor() {
        this.estado = new EstadoAguardandoCartao();
    }

    definirEstado(estado: EstadoCatraca): void {
        this.estado = estado;
    }

    lerCartao(nomeUsuario: string, cartaoValido: boolean): void {
        this.estado.lerCartao(this, nomeUsuario, cartaoValido);
    }

    passarPelaCatraca(): void {
        this.estado.passarPelaCatraca(this);
    }

    obterStatus(): string {
        return this.estado.obterStatus();
    }


    definirUsuarioAtual(nomeUsuario: string): void {
        this.usuarioAtual = nomeUsuario;
    }

    obterUsuarioAtual(): string {
        return this.usuarioAtual;
    }

    limparUsuarioAtual(): void {
        this.usuarioAtual = "";
    }

    desbloquearForcado(): void {
        this.definirEstado(new EstadoAguardandoCartao());
        this.limparUsuarioAtual();
        console.log("Catraca desbloqueada pelo administrador.");
    }
}

class EstadoAguardandoCartao implements EstadoCatraca {
    lerCartao(contexto: CatracaComPadrao, nomeUsuario: string, cartaoValido: boolean): void {
        if (!cartaoValido) {
            console.log("Cartão inválido! Acesso negado.");
            contexto.definirEstado(new EstadoBloqueada());
            

            setTimeout(() => {
                if (contexto.obterStatus() === "Bloqueada") {
                    contexto.definirEstado(new EstadoAguardandoCartao());
                    console.log("Catraca desbloqueada automaticamente.");
                }
            }, 5000);
            return;
        }

        contexto.definirUsuarioAtual(nomeUsuario);
        console.log(`Cartão válido! Acesso liberado para ${nomeUsuario}.`);
        console.log("Passe pela catraca em 10 segundos...");
        contexto.definirEstado(new EstadoLiberada());


        setTimeout(() => {
            if (contexto.obterStatus() === "Liberada - aguardando passagem") {
                contexto.definirEstado(new EstadoAguardandoCartao());
                contexto.limparUsuarioAtual();
                console.log("Tempo esgotado! Catraca bloqueada novamente.");
            }
        }, 10000);
    }

    passarPelaCatraca(contexto: CatracaComPadrao): void {
        console.log("Apresente um cartão válido primeiro!");
    }

    obterStatus(): string {
        return "Aguardando cartão";
    }
}


class EstadoLiberada implements EstadoCatraca {
    lerCartao(contexto: CatracaComPadrao, nomeUsuario: string, cartaoValido: boolean): void {
        console.log("Catraca já está liberada. Passe pela catraca primeiro.");
    }

    passarPelaCatraca(contexto: CatracaComPadrao): void {
        const usuario = contexto.obterUsuarioAtual();
        console.log(`${usuario} passando pela catraca...`);
        contexto.definirEstado(new EstadoUsuarioPassando(usuario));
        

        setTimeout(() => {
            const estadoAtual = contexto.obterStatus();
            if (estadoAtual === "Usuário passando") {
                console.log(`${usuario} passou pela catraca com sucesso!`);
                contexto.definirEstado(new EstadoAguardandoCartao());
                contexto.limparUsuarioAtual();
            }
        }, 2000);
    }

    obterStatus(): string {
        return "Liberada - aguardando passagem";
    }
}


class EstadoUsuarioPassando implements EstadoCatraca {
    private usuario: string;

    constructor(usuario: string) {
        this.usuario = usuario;
    }

    lerCartao(contexto: CatracaComPadrao, nomeUsuario: string, cartaoValido: boolean): void {
        console.log("Aguarde, usuário passando pela catraca...");
    }

    passarPelaCatraca(contexto: CatracaComPadrao): void {
        console.log("Aguarde, usuário passando pela catraca...");
    }

    obterStatus(): string {
        return "Usuário passando";
    }
}


class EstadoBloqueada implements EstadoCatraca {
    lerCartao(contexto: CatracaComPadrao, nomeUsuario: string, cartaoValido: boolean): void {
        console.log("Catraca bloqueada! Contacte o administrador.");
    }

    passarPelaCatraca(contexto: CatracaComPadrao): void {
        console.log("Catraca bloqueada! Acesso negado.");
    }

    obterStatus(): string {
        return "Bloqueada";
    }
}

// EXEMPLO DE USO
const catraca2 = new CatracaComPadrao();

// Esse é um teste simples para verificar o funcionamento da catraca.
// O cenário é o seguinte:
// 1. Usuário tenta passar sem cartão lido (deve falhar).
// 2. Usuário lê um cartão válido (deve ser bem-sucedido).
// 3. Usuário tenta passar pela catraca (deve ser bem-sucedido).
// 4. Usuário tenta ler um cartão enquanto outro está passando (deve falhar).
// 5. Usuário lê um cartão válido após o anterior passar (deve ser bem-sucedido).
// 6. Usuário tenta passar novamente (deve falhar pois demorou demais).

// OBS: O teste é idêntico ao anterior, o que demonstra que externamente o comportamento é o mesmo, mas internamente a lógica é diferente.

console.log("=== TESTE COM PADRÃO STATE ===");

console.log("Status:", catraca2.obterStatus());
setTimeout(() => catraca2.passarPelaCatraca(), 2000); // Usuário não passa pois não há cartão lido
setTimeout(() => catraca2.lerCartao("João Silva", true), 4000); // Deve ser bem-sucedido pois é um cartão válido
setTimeout(() => catraca2.passarPelaCatraca(), 6000); // Usuário passa, pois a catraca está liberada
setTimeout(() => catraca2.lerCartao("Maria Santos", true), 7000); // Deve falhar pois alguém está passando
setTimeout(() => catraca2.lerCartao("Maria Santos", true), 10000); // Deve ser bem sucedida pois o usuario anterior já passou
setTimeout(() => catraca2.passarPelaCatraca(), 20000); // Usuário não passa pois demorou demais.
    