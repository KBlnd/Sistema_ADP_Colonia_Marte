import numpy as np

# ========== DADOS ==========
# listas (requisito 1)

vento_historico = [8, 10, 12]
energia_historico = [20, 25, 30]

# chave-valor + hierarquia (requisitos 1 e 2)
sistemas = {
    "energetico": {"solar": True, "eolico": True},
    "suporte_vida": True,
    "iluminacao": False,
    "lazer": False,
}

# ========== FUNÇÕES ==========

def analisar_energia(gerac, cons):
    if cons > gerac:
        print("ALERTA: consumo maior que geração!\n")
    elif gerac > cons:
        print("SUGESTÃO: armazenar energia excedente!\n")
    else:
        print("Equilíbrio!\n")

def decidir(energ, cons):
    if energ < 50 and cons > 70:
        print("Energia crítica e consumo alto! Entrar em modo de economia: desligar o que não é essencial.\n")
    elif energ < 50:
        print("Colônia está consumindo muita energia. Reduzir consumo de energia!\n")
    else:
        print("Operação dos sistemas e o consumo estão normais!\n")

def prever_energia(vento):
    m, b = np.polyfit(vento_historico, energia_historico, 1)
    energia_nova = m * vento + b
    print(f"Com o ventos de {vento} km/h, a previsão da quantidade de energia que será gerada pela Energia Eólica é de: {energia_nova:.2f}")

# ========== MAIN ==========
def main():
    print("\nSistema A.D.P da colônia de Marte\n")
    energia = geracao_energia = consumo_energia = velocidade_vento = None
    while True:
        print("---------MENU-----------")
        print("    1- Cadastrar dados")
        print("    2- Analisar energia da colônia")
        print("    3- Decidir")
        print("    4- Prever energia gerada")
        print("5 - Mostrar sistemas")
        print("    0- Sair")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite apenas números!\n")
            continue
        if opcao == 1:
            try:
                energia = float(input("Quanto sua colônia tem de energia: "))
                geracao_energia = float(input("Quanto sua colônia gera de energia: "))
                consumo_energia = float(input("Quanto sua colônia consome de energia: "))
                velocidade_vento = float(input("Velocidade do vento (km/h): "))
            except ValueError:
                print("Valor inválido! Cadastre novamente.\n")
                energia = geracao_energia = consumo_energia = velocidade_vento = None
        elif opcao in (2, 3, 4, 5):
            if energia is None:
                print("Cadastre os dados na opção 1 primeiro!\n")
            elif opcao == 2:
                analisar_energia(geracao_energia, consumo_energia)
            elif opcao == 3:
                decidir(energia, consumo_energia)
            elif opcao == 4:
                prever_energia(velocidade_vento)
            else:
                print(sistemas)
        elif opcao == 0:
            print("Obrigado por usar!")
            break
        else:
            print("Opção inválida!\n")

if __name__ == "__main__":
    main()
