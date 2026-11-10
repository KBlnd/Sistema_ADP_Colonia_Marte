import numpy as np

LARGURA = 56

# ========== CONSTANTES DAS REGRAS DE DECISÃO ==========
LIMITE_ENERGIA = 50          # energia abaixo disso = reserva baixa
LIMITE_CONSUMO_ALTO = 70     # consumo acima disso = consumo alto


# ========== DADOS ==========
# Histórico para a regressão linear: vento x geração EÓLICA
vento_historico = [8.0, 10.0, 12.0]
energia_historico = [20.0, 25.0, 30.0]

# Hierarquia e estado inicial dos sistemas da colônia
sistemas = {
    "energetico": {"solar": True, "eolico": True},
    "suporte_vida": True,
    "iluminacao": True,
    "lazer": True,
}

# Sistemas essenciais nunca são desligados pelo modo economia
ESSENCIAIS = ("energetico", "suporte_vida")
# Ordem de corte: o que é menos importante é desligado primeiro
ORDEM_CORTE = ("lazer", "iluminacao")

# Dados atuais da colônia (chave-valor)
dados = {
    "energia": 0.0,
    "solar": 0.0,
    "eolica": 0.0,
    "geracao": 0.0,   # solar + eólica
    "consumo": 0.0,
    "vento": 0.0,
}


# ========== LÓGICA ==========
def analisar_energia(gerac: float, cons: float) -> str:
    if cons > gerac:
        return "alerta"
    elif gerac > cons:
        return "sobra"
    return "equilibrio"


def decidir(energ: float, cons: float, gerac: float):
    # Regras em ordem de prioridade. Retorna (resultado, sistemas_alterados).
    # 1) Energia baixa E consumo alto -> modo economia (corta o não essencial)
    if energ < LIMITE_ENERGIA and cons > LIMITE_CONSUMO_ALTO:
        desligados = []
        for nome in ORDEM_CORTE:
            if sistemas[nome]:
                sistemas[nome] = False
                desligados.append(nome)
        return "economia", desligados

    # 2) Energia baixa -> reduzir consumo
    if energ < LIMITE_ENERGIA:
        return "reduzir", []

    # 3) Energia ok, mas consumo maior que a geração -> reserva sendo gasta
    if cons > gerac:
        return "deficit", []

    # 4) Situação normalizada -> religa o que foi cortado (do mais importante)
    religados = []
    for nome in reversed(ORDEM_CORTE):
        if not sistemas[nome]:
            sistemas[nome] = True
            religados.append(nome)
    return "normal", religados


def calcular_previsao(vento_alvo: float):
    # Regressão linear simples (reta y = ax + b). Retorna (a, b, previsao).
    if len(vento_historico) < 2 or len(set(vento_historico)) < 2:
        return None
    a, b = np.polyfit(vento_historico, energia_historico, 1)
    return a, b, max(0.0, a * vento_alvo + b)


# ========== EXIBIÇÃO ==========
def titulo(texto: str) -> None:
    print()
    print("╔" + "═" * LARGURA + "╗")
    print("║" + texto.center(LARGURA) + "║")
    print("╚" + "═" * LARGURA + "╝")


def secao(texto: str) -> None:
    print()
    print(f"── {texto} " + "─" * (LARGURA - len(texto) - 4))


def linha(rotulo: str, valor: str) -> None:
    print(f"  {rotulo:<26}{valor:>12}")


def barra(valor: float, maximo: float, largura: int = 24) -> str:
    proporcao = 0 if maximo <= 0 else min(valor / maximo, 1)
    cheio = int(proporcao * largura)
    return "█" * cheio + "░" * (largura - cheio)


def pausar() -> None:
    input("\n  Pressione ENTER para voltar ao menu...")


def nomes(lista) -> str:
    return ", ".join(n.replace("iluminacao", "iluminação") for n in lista)


def mostrar_dados() -> None:
    secao("Dados cadastrados")
    linha("Energia disponível", f"{dados['energia']:.1f}")
    linha("Geração solar", f"{dados['solar']:.1f}")
    linha("Geração eólica", f"{dados['eolica']:.1f}")
    linha("Geração total", f"{dados['geracao']:.1f}")
    linha("Consumo atual", f"{dados['consumo']:.1f}")
    linha("Vento (km/h)", f"{dados['vento']:.1f}")


def mostrar_analise() -> None:
    s, w = dados["solar"], dados["eolica"]
    g, c = dados["geracao"], dados["consumo"]
    secao("Análise de energia")
    maximo = max(g, c, 1)
    print(f"  Solar     {barra(s, maximo)}  {s:.1f}")
    print(f"  Eólica    {barra(w, maximo)}  {w:.1f}")
    print(f"  Geração   {barra(g, maximo)}  {g:.1f}")
    print(f"  Consumo   {barra(c, maximo)}  {c:.1f}")
    print()
    resultado = analisar_energia(g, c)
    if resultado == "alerta":
        print("  [ALERTA] Consumo maior que geração!")
    elif resultado == "sobra":
        print("  [SUGESTÃO] Armazenar energia excedente!")
    else:
        print("  [OK] Equilíbrio entre geração e consumo!")


def mostrar_decisao() -> None:
    e, c, g = dados["energia"], dados["consumo"], dados["geracao"]
    secao("Decisão automática")
    print(f"  Energia   {barra(e, 100)}  {e:.1f}  (baixa: abaixo de {LIMITE_ENERGIA})")
    print(f"  Consumo   {barra(c, 100)}  {c:.1f}  (alto: acima de {LIMITE_CONSUMO_ALTO})")
    print(f"  Geração   {barra(g, 100)}  {g:.1f}")
    print()
    resultado, alterados = decidir(e, c, g)
    if resultado == "economia":
        print("  [ALERTA] Modo de economia ativado!")
        if alterados:
            print(f"           Sistemas desligados: {nomes(alterados)}")
        else:
            print("           Sistemas não essenciais já estavam desligados.")
        print("           Suporte à vida mantido ligado.")
    elif resultado == "reduzir":
        print("  [ALERTA] Energia baixa. Recomenda-se reduzir o consumo.")
    elif resultado == "deficit":
        print("  [ATENÇÃO] Consumo maior que a geração: a reserva está sendo gasta.")
        print("            Recomenda-se reduzir o consumo.")
    else:
        print("  [OK] Operação normal.")
        if alterados:
            print(f"       Sistemas religados: {nomes(alterados)}")


def mostrar_previsao() -> None:
    secao("Previsão de geração eólica")
    try:
        v = ler_float("Velocidade do vento para prever (km/h)")
    except ValueError:
        print("  [ERRO] Digite apenas números válidos.")
        return
    if v < 0:
        print("  [ERRO] A velocidade do vento não pode ser negativa.")
        return

    resultado = calcular_previsao(v)
    if resultado is None:
        print("  [ALERTA] Dados insuficientes para calcular previsão.")
        return
    a, b, previsao = resultado

    print("\n  Histórico (vento x geração eólica):")
    print("  ┌─────┬──────────────┬──────────┐")
    print("  │  #  │ Vento (km/h) │ Energia  │")
    print("  ├─────┼──────────────┼──────────┤")
    for i, (vh, eh) in enumerate(zip(vento_historico, energia_historico), 1):
        print(f"  │ {i:>3} │ {vh:>12.1f} │ {eh:>8.1f} │")
    print("  └─────┴──────────────┴──────────┘")

    print(f"\n  Modelo: energia = {a:.3f} x vento + {b:.3f}")
    print(f"  Vento informado: {v:.1f} km/h")
    print(f"\n  >> Previsão: {previsao:.2f} unidades de energia eólica")

    print("\n  Abrindo gráfico... (feche a janela para voltar ao menu)")
    abrir_grafico(a, b, v, previsao)


def abrir_grafico(a: float, b: float, v: float, previsao: float) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("  [ALERTA] matplotlib não instalado (pip install matplotlib).")
        return
    plt.scatter(vento_historico, energia_historico, color="blue", label="Histórico")
    x_plot = np.linspace(min(vento_historico + [v]) - 2, max(vento_historico + [v]) + 2, 100)
    plt.plot(x_plot, a * x_plot + b, color="red", label="Ajuste Linear")
    plt.scatter(v, previsao, color="green", marker="X", s=100, label="Previsão")
    plt.xlabel("Velocidade do Vento (km/h)")
    plt.ylabel("Energia Eólica Gerada")
    plt.title("Regressão Linear: Vento vs Energia Eólica")
    plt.legend()
    plt.grid(True)
    plt.show()


def imprimir_arvore(estrutura: dict, prefixo: str = "") -> None:
    # Percorre a hierarquia de forma recursiva, desenhando uma árvore.
    itens = list(estrutura.items())
    for i, (nome, valor) in enumerate(itens):
        ultimo = i == len(itens) - 1
        ramo = "└── " if ultimo else "├── "
        if isinstance(valor, dict):
            print(f"  {prefixo}{ramo}{nome}")
            imprimir_arvore(valor, prefixo + ("    " if ultimo else "│   "))
        else:
            status = "[LIGADO]   " if valor else "[DESLIGADO]"
            marca = "  (essencial)" if nome in ESSENCIAIS else ""
            print(f"  {prefixo}{ramo}{nome:<14} {status}{marca}")


def mostrar_sistemas() -> None:
    secao("Estado dos sistemas da colônia")
    print("  colônia")
    imprimir_arvore(sistemas)


def mostrar_menu() -> None:
    titulo("SISTEMA A.D.P  -  COLÔNIA DE MARTE")
    print("   [1]  Cadastrar dados")
    print("   [2]  Analisar energia da colônia")
    print("   [3]  Decidir (regras automáticas)")
    print("   [4]  Prever geração eólica")
    print("   [5]  Mostrar sistemas")
    print("   [0]  Sair")
    print("  " + "─" * LARGURA)


# ========== ENTRADA DE DADOS ==========
def ler_float(mensagem: str) -> float:
    return float(input(f"  {mensagem}: ").replace(",", "."))


def cadastrar_dados() -> bool:
    secao("Cadastro de dados")
    try:
        e = ler_float("Energia disponível")
        s = ler_float("Geração solar")
        w = ler_float("Geração eólica")
        c = ler_float("Consumo atual")
        v = ler_float("Velocidade do vento (km/h)")
    except ValueError:
        print("  [ERRO] Digite apenas números válidos.")
        return False

    if min(e, s, w, c, v) < 0:
        print("  [ERRO] Os valores físicos não podem ser negativos.")
        return False

    # Previsão feita ANTES de incluir o novo ponto no histórico,
    # para comparar o que o modelo previa com o que foi observado.
    anterior = calcular_previsao(v)

    dados.update(energia=e, solar=s, eolica=w, geracao=s + w, consumo=c, vento=v)

    # Alimenta o modelo com o novo dado (histórico contínuo)
    vento_historico.append(v)
    energia_historico.append(w)

    print("  [OK] Dados cadastrados e histórico atualizado com sucesso!")
    if anterior is not None:
        previsto = anterior[2]
        print(f"\n  Verificação do modelo (antes deste registro):")
        linha("Eólica prevista", f"{previsto:.1f}")
        linha("Eólica observada", f"{w:.1f}")
        linha("Diferença", f"{abs(w - previsto):.1f}")
    return True


# ========== MAIN ==========
def main():
    dados_cadastrados = False

    while True:
        mostrar_menu()
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "0":
            print("\n  Encerrando o sistema A.D.P... Até logo!\n")
            break
        elif opcao == "1":
            if cadastrar_dados():
                dados_cadastrados = True
                mostrar_dados()
        elif opcao in ("2", "3"):
            if not dados_cadastrados:
                print("  [ALERTA] Cadastre os dados primeiro (opção 1).")
            elif opcao == "2":
                mostrar_analise()
            else:
                mostrar_decisao()
        elif opcao == "4":
            mostrar_previsao()
        elif opcao == "5":
            mostrar_sistemas()
        else:
            print("  [ALERTA] Opção inválida.")

        pausar()


if __name__ == "__main__":
    main()