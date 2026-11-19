# 3. Metodologia e conceitos de energia aplicados

Implementação em [`citizen_energia/calculos.py`](../citizen_energia/calculos.py). Números completos em [`04_calculos_gerados.md`](04_calculos_gerados.md).

## 3.1 Potência e energia do chuveiro

O chuveiro elétrico é um **aquecedor de passagem**: a resistência converte energia elétrica em calor (efeito Joule) e transfere esse calor à água no instante em que ela passa. A potência necessária vem do balanço de energia:

```
P = ṁ · c · ΔT / η
```

| Símbolo | Significado | Valor de referência |
|---|---|---|
| ṁ | vazão mássica de água | 4 L/min = 0,0667 kg/s |
| c | calor específico da água | 4186 J/(kg·°C) |
| ΔT | temperatura do banho − temperatura da água fria | 38 − 20 = 18 °C |
| η | eficiência (fração da energia elétrica que vira calor útil na água) | 0,95 |

**P ≈ 5,29 kW.** A energia é **E = P · t**: 4 pessoas × 8 min = 32 min/dia = 0,533 h/dia → **~85 kWh/mês**.

Conceitos envolvidos: **potência** (taxa de uso de energia, kW) × **energia** (quantidade consumida, kWh); **eficiência** (η); **calor sensível** (Q = m·c·ΔT).

## 3.2 Conta de luz

```
Valor = (kWh faturáveis × tarifa + kWh compensados × 60% × Fio B) / (1 − ICMS − PIS/COFINS)
```

- **kWh faturáveis** = consumo − 80 kWh gratuitos (se Tarifa Social).
- **ICMS por faixa de consumo** (0%, 12% ou 18%) sobre a conta inteira, o que cria um **degrau em 200 kWh**.
- **kWh compensados**: créditos de geração fotovoltaica. Pela Lei 14.300/2022, 60% do Fio B não é compensado em 2026.

## 3.3 Alternativas comparadas

Todas atendem **a mesma necessidade** (água quente do banho da mesma família) no **mesmo período** (12 meses), simuladas mês a mês.

| # | Alternativa | Tipo | Como foi modelada |
|---|---|---|---|
| 0 | Chuveiro elétrico atual | linha de base | P · t |
| 1 | Banhos de 5 min | eficiência / hábito | mesma potência, menos tempo |
| 2 | Aquecedor solar de água com apoio elétrico | **renovável (solar térmica)** | sol fornece fração f do calor; f do mês = 70% × irradiação do mês ÷ irradiação média (máx. 95%) |
| 3 | Placas fotovoltaicas | **renovável (solar fotovoltaica)** | potência dimensionada para a energia anual do chuveiro, em módulos inteiros de 550 W; geração = kWp × irradiação × dias × PR; créditos com Fio B |
| 4 | Combinado (1 + 2) | renovável + hábito | as duas medidas juntas |

### Por que aquecedor solar E fotovoltaico?

São duas formas diferentes de usar a mesma fonte renovável:

- O **aquecedor solar** converte luz em **calor** direto na água. A conversão é mais eficiente (coletores térmicos aproveitam ~40–60% da radiação, contra ~15–22% de um módulo fotovoltaico), mas a energia fica "presa" em água quente no reservatório.
- O **fotovoltaico** converte luz em **eletricidade**, que pode ser usada em qualquer aparelho ou enviada à rede. Como o banho é à noite, a energia passa pela rede e volta como crédito — e aí entram as regras do Fio B.

Conferência física do aquecedor: coletor de 2 m² × 4,63 kWh/m²·dia × ~40% ≈ **3,7 kWh/dia de calor**, acima dos **2,68 kWh/dia** que o banho precisa na média. Por isso uma fração solar de 70% é plausível (não chega a 100% por causa de dias nublados, inverno e perdas noturnas do reservatório).

### Comparação justa do fotovoltaico

Módulos só existem em tamanhos inteiros (550 W), e o menor sistema que cobre o banho (2 módulos) gera 137% da energia necessária. Para comparar a **mesma necessidade**, também simulamos um sistema hipotético do tamanho exato do banho (`calculos.fv_normalizado`). Os dois resultados são apresentados.

## 3.4 Indicadores

| Indicador | Fórmula | Para que serve |
|---|---|---|
| Economia líquida anual | conta(base) − conta(alternativa) − manutenção | quanto sobra no bolso |
| Retorno simples (payback) | investimento ÷ economia líquida | em quantos anos se paga |
| VPL 10 anos | −I + Σ economia/(1,10)^t | valor do investimento hoje, com custo do dinheiro |
| Investimento por kWh evitado/ano | I ÷ kWh evitados | compara alternativas de tamanhos diferentes |
| CO₂ evitado | kWh evitados × fator do SIN | impacto climático direto |
| Alívio no pico | potência do chuveiro × fração solar | impacto no sistema elétrico às 18h–21h |

## 3.5 Sensibilidade

Para não tratar estimativa como certeza, recalculamos tudo variando **uma premissa por vez**: fração solar (50% e 80%), custo do aquecedor (2×), Fio B (R$ 0,095 e 0,25), regra de 2028 (90% do Fio B), custo FV (R$ 3,62 e 6,50/Wp), bandeira amarela o ano todo, família sem Tarifa Social e banhos de 12 min.
