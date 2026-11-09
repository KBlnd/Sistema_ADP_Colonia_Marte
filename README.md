# Sistema A.D.P. | Colônia de Marte

**FIAP · Ciência da Computação · Etapa 3 · Missão Aurora · 2026**

O **Sistema A.D.P. (Análise, Decisão e Previsão)** é um projeto acadêmico desenvolvido em Python para simular o acompanhamento energético de uma colônia em Marte. O programa reúne informações sobre energia disponível, geração, consumo e velocidade do vento. Com esses dados, identifica situações que exigem atenção, recomenda medidas de economia e estima a geração eólica.

O objetivo da equipe foi juntar, em um único programa, os conteúdos estudados nesta etapa da FIAP. O resultado é uma aplicação de terminal, com menu interativo, funções separadas e uma previsão feita por regressão linear simples.

## Integrantes

| Integrante | Curso |
| --- | --- |
| Henrique Floriano Alcantara | Ciência da Computação |
| Nicolas França | Ciência da Computação |
| Joao Pedro Candido Souza | Ciência da Computação |
| Katia Regina Bispo | Ciência da Computação |
| Yago Souza Araujo | Ciência da Computação |

## O que o programa faz

Ao iniciar o A.D.P., o usuário encontra um menu com cinco opções e o comando para sair. Primeiro, cadastra quatro informações: energia disponível, geração de energia, consumo de energia e velocidade do vento. Depois, pode consultar cada análise separadamente.

A opção **Analisar energia** compara geração e consumo. Se o consumo for maior, aparece um alerta; se a geração superar o consumo, o programa sugere armazenar o excedente; se os valores forem iguais, informa equilíbrio.

A opção **Decidir** observa a energia disponível e o consumo. Quando a energia está abaixo de 50 e o consumo passa de 70, recomenda entrar em modo de economia e desligar sistemas não essenciais. Se apenas a energia estiver abaixo de 50, recomenda reduzir o consumo. Nos demais casos, informa operação normal.

A opção **Prever energia gerada** usa a velocidade do vento para estimar a produção eólica. Já **Mostrar sistemas** apresenta a estrutura dos subsistemas cadastrados.

**Importante:** as ações de economia e armazenamento são recomendações exibidas no terminal. Esta versão não controla equipamentos nem altera automaticamente o estado dos subsistemas.

## Organização dos dados

Os históricos de vento e geração eólica foram registrados em duas listas. Cada posição corresponde à mesma observação nas duas variáveis:

```python
vento_historico = [8, 10, 12]
energia_historico = [20, 25, 30]
```

Os sistemas da colônia são representados por um dicionário, com uma divisão interna para as fontes energéticas:

```python
sistemas = {
    "energetico": {"solar": True, "eolico": True},
    "suporte_vida": True,
    "iluminacao": False,
    "lazer": False,
}
```

Essa organização permite consultar os subsistemas e seus estados iniciais. Os valores informados durante a execução ficam em variáveis e não são gravados em arquivo.

## Regras de análise e decisão

O código separa a comparação entre geração e consumo da decisão baseada na energia disponível. Isso facilita entender por que cada mensagem aparece.

| Condição | Resposta |
| --- | --- |
| Consumo maior que geração | Alerta de consumo acima da geração |
| Geração maior que consumo | Sugestão de armazenar o excedente |
| Geração igual ao consumo | Equilíbrio |
| Energia menor que 50 **e** consumo maior que 70 | Recomendação de modo de economia |
| Energia menor que 50, sem consumo acima de 70 | Recomendação de reduzir o consumo |
| Energia igual ou maior que 50 | Mensagem de operação normal na função de decisão |

As funções são independentes. Por isso, é possível receber um alerta na análise de geração e consumo e, ao mesmo tempo, uma mensagem de operação normal na função de decisão: cada uma verifica critérios diferentes.

## Previsão com regressão linear

Para estimar a geração eólica, a função `prever_energia(vento)` utiliza `numpy.polyfit()` com grau 1. Ela ajusta uma reta aos três pares de dados históricos.

```python
m, b = np.polyfit(vento_historico, energia_historico, 1)
energia_nova = m * vento + b
```

Com os dados definidos no projeto, a relação obtida é **energia prevista = 2,5 × velocidade do vento**. Assim, para um vento de **11 km/h**, o programa apresenta **27,50 unidades de energia**.

Trata-se de uma demonstração didática de regressão linear. Os três registros são exemplos definidos para o exercício, e o programa não especifica uma unidade física de energia nem representa um modelo validado de geração eólica em Marte.

## Como executar

É necessário ter **Python 3** e a biblioteca **NumPy** instalados. No terminal, dentro da pasta do projeto, execute:

```bash
python -m pip install numpy
```

Em seguida, rode o arquivo principal. Por exemplo, caso ele esteja salvo como `main.py`:

```bash
python main.py
```

Se o seu ambiente usa `python3`, substitua `python` por `python3` nos comandos. O nome `main.py` é apenas um exemplo; utilize o nome real do arquivo enviado ao repositório.

## Exemplo de entrada e saída

O exemplo abaixo mostra um cenário de energia crítica. Após escolher **1 — Cadastrar dados**, informe:

```text
Quanto sua colônia tem de energia: 40
Quanto sua colônia gera de energia: 40
Quanto sua colônia consome de energia: 80
Velocidade do vento (km/h): 11
```

Ao selecionar **2 — Analisar energia**, o programa responde:

```text
ALERTA: consumo maior que geração!
```

Na opção **3 — Decidir**, a saída é:

```text
Energia crítica e consumo alto! Entrar em modo de economia: desligar o que não é essencial.
```

Na opção **4 — Prever energia gerada**, a previsão é de **27,50 unidades**. A opção **5 — Mostrar sistemas** imprime o dicionário de subsistemas, e a opção **0** encerra o programa.

Esses são **cenários ilustrativos calculados a partir das regras do código**. O programa também trata entradas não numéricas com `try/except` e exige o cadastro antes de permitir as consultas. A validação ainda pode ser ampliada para impedir valores negativos ou fisicamente incoerentes.

## Estrutura do programa

O projeto utiliza quatro funções principais: `analisar_energia()` compara geração e consumo; `decidir()` aplica as regras condicionais; `prever_energia()` calcula a estimativa; e `main()` organiza o menu, recebe os dados e controla o fluxo de execução.

A implementação usa listas, dicionários, funções, `if/elif/else`, o operador lógico `and`, repetição com `while` e tratamento de erros de conversão. A única biblioteca externa utilizada é o **NumPy**.

## Resultados e limitações

O A.D.P. reúne três tarefas que antes poderiam ser tratadas separadamente: acompanhar dados, aplicar regras e fazer previsões. Com isso, a equipe conseguiu demonstrar, em um mesmo programa, conceitos de programação estruturada, organização de informações, lógica e modelagem matemática.

O sistema ainda é um protótipo acadêmico. Não recebe leituras de sensores, não mantém histórico de cadastros entre execuções, não calcula reservas acumuladas e não aciona sistemas físicos. Como evolução, seria possível salvar medições, validar limites de entrada, ampliar o conjunto de dados da regressão e simular a mudança de estado dos subsistemas quando uma regra de economia fosse acionada.

## Repositório oficial

O código e a documentação deste projeto estão disponíveis no GitHub: [Sistema A.D.P. — Colônia de Marte](https://github.com/YagoSDev/Sistema_ADP_Colonia_Marte).

## Relatório técnico

A explicação acadêmica detalhada do projeto está no documento **Relatório Técnico — Etapa 3 — Sistema A.D.P.**. O PDF apresenta a organização dos dados, as regras, a previsão, exemplos e as limitações da implementação.

Para disponibilizá-lo neste repositório, envie o arquivo `Relatorio_FIAP_Etapa3_Sistema_ADP.pdf` junto ao código e ao README. Depois, este link funcionará:

[Consultar relatório técnico (PDF)](./Relatorio_FIAP_Etapa3_Sistema_ADP.pdf)

## Materiais de referência

O trabalho foi desenvolvido com base nos oito capítulos da Etapa 3 da missão Aurora, disponibilizados pela FIAP em 2026. Entre os conteúdos aplicados diretamente estão lógica booleana, programação estruturada, estruturas de dados, vetores e NumPy, regressão linear simples e fundamentos de energia solar e eólica. Os demais capítulos ajudam a contextualizar a organização computacional da colônia.

O relatório técnico traz a relação dos oito capítulos e os títulos completos dos materiais utilizados.

---

**Projeto acadêmico em equipe · FIAP · Ciência da Computação · Etapa 3 · 2026**
