export class ContaBancaria {
    private _numeroConta: string;
    private _saldo: number;

    constructor(numeroConta: string, saldoInicial: number) {
        this._numeroConta = numeroConta;
        this._saldo = saldoInicial;
    }
    consultarSaldo(): number {
        return this._saldo;
    }
    depositar(valor: number): void {
        this.validarValor(valor);
        this._saldo += valor;
    }
    sacar(valor: number): void {
        this.validarValor(valor);
        if (valor > this._saldo) {
            throw new Error("Saldo insuficiente para o saque.");
        }
        this._saldo -= valor;
    }
    private validarValor(valor: number) {
        if (valor <= 0) {
            throw new Error("O valor deve ser positivo.");
        }
    }

    transferir(valor: number, contaDestino: ContaBancaria): void {
        this.validarValor(valor);
        if (valor > this._saldo) {
            throw new Error("Saldo insuficiente para a transferência.");
        }
        this.sacar(valor);
        contaDestino.depositar(valor);
    }
    extrato(): string {
        return `Conta: ${this._numeroConta}, Saldo: R$ ${this._saldo.toFixed(2)}`;
    }
}
