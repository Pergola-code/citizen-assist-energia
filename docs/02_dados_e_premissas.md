# 2. Dados, unidades e premissas

**Período de referência:** 12 meses (ano típico, janeiro a dezembro), com tarifas vigentes em **novembro de 2026**.
**Unidades:** energia em kWh, potência em kW (ou kWp para placas fotovoltaicas), irradiação em kWh/m²·dia, dinheiro em R$ correntes de 2026, emissões em kg de CO₂.

Todos os dados estão em [`citizen_energia/dados/parametros.json`](../citizen_energia/dados/parametros.json), cada um com **valor, unidade, tipo e referência**. A tabela completa, gerada pelo código, está na seção 1 de [`04_calculos_gerados.md`](04_calculos_gerados.md).

## Classificação dos dados

| Tipo | Significado | Exemplos |
|---|---|---|
| **PUBLICO** | Dado oficial ou publicado, verificável | tarifa Enel SP (REH 3.596/2026), faixas de ICMS-SP, Tarifa Social (Lei 15.235/2025), Fio B 60% (Lei 14.300), custo SINAPI do aquecedor solar, irradiação CRESESB, fator de emissão do SIN (MCTI) |
| **MERCADO** | Preço ou especificação típica de mercado | potência de módulo FV de 550 W |
| **ESTIMADO** | Premissa da equipe, justificada | família de 4 pessoas, banho de 8 min, vazão 4 L/min, água fria a 20 °C, consumo de 220 kWh/mês, R$ 4,50/Wp para sistema FV pequeno, Fio B da Enel SP = R$ 0,15/kWh |

## Dados principais

| Dado | Valor | Unidade | Tipo | Fonte |
|---|---|---|---|---|
| Tarifa B1 Enel SP (TUSD + TE), sem impostos | 0,78938 | R$/kWh | PUBLICO | R01 |
| Bandeira de nov/2026 | verde (sem adicional) | — | PUBLICO | R02 |
| Bandeira amarela (sensibilidade) | 0,01885 | R$/kWh | PUBLICO | R03 |
| ICMS residencial SP | 0% até 90 kWh; 12% até 200 kWh; 18% acima | — | PUBLICO | R05 |
| PIS/COFINS efetivo | 6 | % | ESTIMADO | R04 |
| Tarifa Social: kWh gratuitos | 80 | kWh/mês | PUBLICO | R06 |
| Irradiação no plano inclinado 23° (jan…dez) | 4,8 · 4,7 · 4,9 · 4,6 · 4,4 · 4,2 · 4,7 · 4,9 · 4,4 · 4,6 · 5,0 · 4,8 | kWh/m²·dia | PUBLICO | R11 |
| Fração solar do aquecedor solar | 70 | % | PUBLICO | R13 |
| Aquecedor solar 200 L instalado (SINAPI 103517, 09/2026) | 3.359,57 | R$ | PUBLICO | R14 |
| Adaptações hidráulicas | +25 | % do kit | ESTIMADO | R15 |
| Custo FV sistema pequeno | 4,50 | R$/Wp | ESTIMADO | R16 |
| Fio B não compensado em 2026 | 60 | % | PUBLICO | R08 |
| Fio B Enel SP | 0,15 | R$/kWh | ESTIMADO | R17 |
| Performance ratio FV | 0,75 | — | ESTIMADO | R12 |
| Fator de emissão do SIN (2023) | 0,0385 | tCO₂/MWh | PUBLICO | R18 |

## Por que cada estimativa é razoável

- **Banho de 8 min:** mesmo valor usado em estudo de simulação de chuveiros no Sudeste [R10]. O simulador aceita o valor real da família.
- **Vazão de 4 L/min e água fria a 20 °C:** com esses valores a física dá **5,29 kW**, dentro da faixa de potência dos chuveiros vendidos (4,5–7,5 kW). Isso valida as duas premissas juntas.
- **Consumo de 220 kWh/mês:** com o chuveiro calculado, ele fica em 38% do total — acima da média do Sudeste (24%), o que é esperado em casas de baixa renda, com poucos outros aparelhos. O simulador alerta quando o chuveiro passa de 60% do consumo informado (dado provavelmente inconsistente).
- **Irradiação de São José dos Campos:** a cidade está na mesma latitude da Grande SP (~23 °S) e o dado vem da base CRESESB/SunData. Para um projeto real, deve-se consultar o SunData com a coordenada exata.
- **Fração solar de 70%:** vem de estudo publicado (simulação EnergyPlus, Viçosa-MG). Como o clima é diferente, testamos 50% e 80% na sensibilidade.
- **Fio B da Enel SP:** as fontes públicas divergem (R$ 0,095 a R$ 0,25/kWh). Usamos R$ 0,15, da ordem da CPFL Paulista (outra distribuidora paulista), e testamos os extremos.
- **R$ 4,50/Wp:** o Greener 2025 indica R$ 3,62/Wp para 2 kWp e R$ 2,84/Wp para 4 kWp. Sistemas de ~1 kWp têm custo fixo (inversor, projeto, homologação) diluído em menos watts, por isso valor mais alto. Testamos R$ 3,62 e R$ 6,50.

## O que NÃO foi considerado (e por quê)

- Contribuição de iluminação pública (CIP/COSIP): igual em todas as alternativas, não muda a comparação.
- Reajuste tarifário futuro: omitido de propósito (postura conservadora; com reajuste, todas as alternativas economizariam mais).
- Financiamento e juros: dependem da linha de crédito da família.
- Variação mensal da temperatura da água fria: usamos a média anual.
