import { ContaBancaria } from "./ContaBancaria";
test("Deve ser possuivel depositar um valor na conta bancaria", () => {
    const conta = new ContaBancaria("12345", 1000);
    conta.depositar(500);
    expect(conta.consultarSaldo()).toBe(1500);
});

test("Deve ser possivel sacar um valor da conta bancaria", () => {
    const conta = new ContaBancaria("12345", 1000);
    conta.sacar(300);
    expect(conta.consultarSaldo()).toBe(700);
}
);

test("Deve lançar um erro ao tentar sacar um valor maior que o saldo", () => {
    const conta = new ContaBancaria("12345", 1000);
    expect(() => conta.sacar(1200)).toThrow("Saldo insuficiente para o saque.");
});

test("Deve lançar um erro ao tentar sacar um valor negativo", () => {
    const conta = new ContaBancaria("12345", 1000);
    expect(() => conta.sacar(-100)).toThrow("O valor deve ser positivo.");
});

test("Deve ser possivel transferir um valor para outra conta bancaria", () => {
    const conta1 = new ContaBancaria("12345", 1000);
    const conta2 = new ContaBancaria("67890", 500);
    conta1.transferir(300, conta2);
    expect(conta1.consultarSaldo()).toBe(700);
    expect(conta2.consultarSaldo()).toBe(800);
});

test("Deve lançar um erro ao tentar transferir um valor maior que o saldo", () => {
    const conta1 = new ContaBancaria("12345", 1000);
    const conta2 = new ContaBancaria("67890", 500);
    expect(() => conta1.transferir(1200, conta2)).toThrow("Saldo insuficiente para a transferência.");
});
test("Deve lançar um erro ao tentar transferir um valor negativo", () => {
    const conta1 = new ContaBancaria("12345", 1000);
    const conta2 = new ContaBancaria("67890", 500);
    expect(() => conta1.transferir(-100, conta2)).toThrow("O valor deve ser positivo.");
});
test("Deve retornar o extrato da conta bancaria", () => {
    const conta = new ContaBancaria("12345", 1000);
    expect(conta.extrato()).toBe("Conta: 12345, Saldo: R$ 1000.00");
});
test("Deve lançar um erro ao tentar depositar um valor negativo", () => {
    const conta = new ContaBancaria("12345", 1000);
    expect(() => conta.depositar(-100)).toThrow("O valor deve ser positivo.");
});