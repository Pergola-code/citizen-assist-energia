# 1. Definição do contexto

## Público atendido

Famílias de baixa renda que moram em **casas** (não apartamentos) na área de concessão da **Enel Distribuição São Paulo** — capital e 23 municípios da Região Metropolitana — e que aquecem a água do banho com **chuveiro elétrico**. Parte dessas famílias está no CadÚnico e recebe a **Tarifa Social de Energia Elétrica**.

Por que esse recorte:

- O chuveiro elétrico está em praticamente todas as casas do Sul e Sudeste e é o maior consumidor da residência: cerca de **24% do consumo residencial no Sudeste** segundo a Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel, e mais nas famílias de baixa renda, que têm menos outros aparelhos [R09].
- Desde a Lei 15.235/2025, os primeiros **80 kWh/mês são gratuitos** para quem tem Tarifa Social, mas **todo kWh acima disso é cobrado com preço cheio** [R06]. O chuveiro sozinho já passa desse limite, então cada minuto de banho pesa no bolso mesmo de quem tem o benefício.
- A tarifa residencial da Enel SP subiu em julho de 2026 (efeito médio de 10,18%) e está em **R$ 0,78938/kWh sem impostos** [R01].

## Necessidade energética abordada

**Aquecer a água do banho** de uma família durante um ano, gastando menos dinheiro e menos energia da rede.

Família de referência (premissas detalhadas em [`02_dados_e_premissas.md`](02_dados_e_premissas.md)):

| Item | Valor |
|---|---|
| Pessoas | 4 |
| Banho | 1 por pessoa/dia, 8 min |
| Consumo total da casa | 220 kWh/mês |
| Tarifa Social | sim |
| **Potência calculada do chuveiro** | **5,29 kW** |
| **Energia do chuveiro** | **~85 kWh/mês (38% do consumo)** |
| **Conta estimada** | **R$ 145/mês (sem iluminação pública)** |

Há também uma dimensão coletiva: o chuveiro responde por **cerca de metade da carga residencial no horário de pico** [R20]. Reduzir esse pico alivia a rede e diminui o acionamento de usinas térmicas.

## Como as orientações contribuem

O cidadão desse público raramente sabe quanto o chuveiro custa, não entende as regras de bandeira, ICMS e Tarifa Social, e é alvo de vendedores prometendo "conta zero" com energia solar. O módulo de Energia do Citizen Assist AI:

1. **Traduz a conta de luz** em algo concreto: "cada minuto de banho custa ~R$ 0,09".
2. **Compara alternativas reais** para a mesma necessidade, com custo, retorno, viabilidade e impacto ambiental.
3. **Recomenda em ordem de prioridade** (hábito → aquecedor solar → fotovoltaico) explicando para quem cada uma faz sentido.
4. **Protege o cidadão** de promessas exageradas: toda resposta diz que é estimativa, mostra as fontes e as limitações, e orienta pedir três orçamentos.
5. **Personaliza** com os dados da própria conta (`simular`).
