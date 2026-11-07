# Memória de cálculo (gerada automaticamente)

> Arquivo gerado por `python -m citizen_energia.relatorio`. Não edite à mão: altere `citizen_energia/dados/parametros.json` e rode de novo.

**Necessidade analisada:** água quente para o banho de uma família de 4 pessoas na área da Enel SP. **Período de referência:** 12 meses, tarifas vigentes em novembro/2026.

## 1. Parâmetros e premissas

Tipos: **PUBLICO** = dado oficial/publicado; **MERCADO** = preço de referência; **ESTIMADO** = premissa da equipe (justificada na nota).

| Parâmetro | Valor | Unidade | Tipo | Ref. | Nota |
|---|---|---|---|---|---|
| `tarifa_b1_sem_impostos` | 0.78938 | R$/kWh | PUBLICO | R01 | Enel SP, B1 residencial convencional (TUSD 0,47242 + TE 0,31696), REH ANEEL nº 3.596/2026, vigente 04/07/2026 a 03/07/2027, bandeira verde. |
| `bandeira_amarela_adicional` | 0.01885 | R$/kWh | PUBLICO | R03 | R$ 1,885 a cada 100 kWh. Usado só na análise de sensibilidade. Nov/2026 = bandeira verde (R02). |
| `icms_faixas_sp` | [[90, 0.0], [200, 0.12], [999999, 0.18]] | [limite kWh/mês, alíquota] | PUBLICO | R05 | SP residencial: isento até 90 kWh; 12% de 91 a 200 kWh; 18% acima de 200 kWh (teto da LC 194/2022). A faixa vale para a conta inteira. |
| `pis_cofins_efetivo` | 0.06 | fração | ESTIMADO | R04 | PIS/COFINS variam mês a mês por distribuidora; 6% é a média usada em simulações públicas da tarifa Enel SP. Confira na sua conta. |
| `tarifa_social_kwh_gratuitos` | 80 | kWh/mês | PUBLICO | R06 | Lei 15.235/2025: 100% de desconto até 80 kWh/mês para famílias do CadÚnico com renda per capita até 1/2 salário mínimo. O excedente é cobrado normalmente. |
| `custo_disponibilidade_monofasico` | 30 | kWh/mês | PUBLICO | R07 | Mínimo faturável de ligação monofásica (bifásica 50, trifásica 100). |
| `pessoas` | 4 | pessoas | ESTIMADO | — | Família típica do público-alvo. O simulador aceita qualquer valor. |
| `banhos_por_pessoa_dia` | 1 | banho/dia | ESTIMADO | — |  |
| `minutos_por_banho` | 8 | min | ESTIMADO | R10 | Mesmo valor (banho diário de 8 min) usado em estudo de simulação de chuveiros no Sudeste. |
| `vazao_chuveiro` | 4.0 | L/min | ESTIMADO | — | Chuveiros elétricos de baixa pressão operam tipicamente entre 3 e 5 L/min. |
| `temperatura_banho` | 38 | °C | ESTIMADO | — | Temperatura de conforto usual. |
| `temperatura_agua_fria` | 20 | °C | ESTIMADO | — | Média anual aproximada da água da rede na Grande SP (acompanha a temperatura média do ar). No inverno é menor, no verão maior. |
| `eficiencia_chuveiro` | 0.95 | fração | ESTIMADO | — | Resistência imersa transfere quase todo o calor à água; perdas pequenas. |
| `consumo_total_mensal` | 220 | kWh/mês | ESTIMADO | R09 | Consumo total da casa. Com o chuveiro calculado (~80 kWh) ele fica em ~37% do total, coerente com a PPH (24% Sudeste em média; maior em casas de baixa renda, onde há menos outros aparelhos). |
| `beneficiaria_tarifa_social` | True | bool | ESTIMADO | R06 | Cenário base. O cenário sem benefício também é calculado. |
| `calor_especifico_agua` | 4186 | J/(kg·°C) | PUBLICO | — | Valor de referência de física. |
| `densidade_agua` | 1.0 | kg/L | PUBLICO | — |  |
| `irradiacao_mensal_plano_23graus` | 4.8, 4.7, 4.9, 4.6, 4.4, 4.2, 4.7, 4.9, 4.4, 4.6, 5.0, 4.8 | kWh/m²·dia (jan..dez) | PUBLICO | R11 | Irradiação diária média mensal no plano inclinado a 23° (São José dos Campos-SP, base CRESESB/SunData), usada como proxy da Grande SP (mesma latitude ~23°S). Para projeto real, consulte o SunData com a coordenada exata. |
| `performance_ratio_fv` | 0.75 | fração | ESTIMADO | R12 | Razão de desempenho de sistemas FV residenciais (literatura usa ~0,75–0,80). |
| `fracao_solar_aquecedor` | 0.7 | fração | PUBLICO | R13 | Redução média de 70% na eletricidade para aquecer água ao trocar chuveiro elétrico por aquecedor solar com apoio elétrico (estudo UFV/Ambiente Construído). Sensibilidade: 0,50 a 0,80. |
| `aquecedor_solar_kit_instalado` | 3359.57 | R$ | PUBLICO | R14 | SINAPI 103517 (09/2026, média nacional, não desonerado): kit compacto 200 L + coletor 2,0 m² + instalação. NÃO inclui conexões, válvulas e adaptações. |
| `aquecedor_solar_adaptacoes` | 0.25 | fração sobre o kit | ESTIMADO | R15 | Acréscimo para conexões, registros e ajustes hidráulicos. Casas sem tubulação de água quente podem custar muito mais (R15 cita R$ 10–18 mil em reformas extensas). |
| `aquecedor_solar_manutencao_anual` | 100 | R$/ano | ESTIMADO | — | Limpeza do coletor e verificação anual. |
| `aquecedor_solar_vida_util` | 15 | anos | ESTIMADO | — |  |
| `fv_custo_por_wp_pequeno` | 4.5 | R$/Wp | ESTIMADO | R16 | Greener 2025: R$ 3,62/Wp para 2 kWp e R$ 2,84/Wp para 4 kWp. Sistemas de ~1 kWp têm custo fixo (inversor, projeto, homologação) diluído em menos watts, por isso R$ 4,50/Wp. |
| `fv_potencia_modulo` | 0.55 | kWp | MERCADO | — | Módulo comercial típico (550 W). |
| `fv_manutencao_anual` | 100 | R$/ano | ESTIMADO | — | Limpeza e inspeção. |
| `fv_vida_util` | 25 | anos | ESTIMADO | — | Inversor normalmente precisa ser trocado antes (~10–12 anos). |
| `fv_fio_b_enel_sp` | 0.15 | R$/kWh | ESTIMADO | R17 | Fontes públicas divergem para a Enel SP (R$ 0,095 a 0,25/kWh). Usamos R$ 0,15 (ordem de grandeza da CPFL Paulista, também em SP) e testamos a faixa na sensibilidade. |
| `fv_percentual_fio_b_2026` | 0.6 | fração | PUBLICO | R08 | Lei 14.300/2022: em 2026, 60% do Fio B não é compensado (75% em 2027, 90% em 2028). |
| `habitos_custo_timer` | 20 | R$ | ESTIMADO | — | Timer/ampulheta de banho (opcional). |
| `taxa_desconto_anual` | 0.1 | fração/ano | ESTIMADO | — | Custo de oportunidade do dinheiro para o cálculo do VPL. |
| `fator_emissao_sin` | 0.0385 | tCO2/MWh | PUBLICO | R18 | Fator médio anual do SIN em 2023 (MCTI). Meses de 2025 ficaram entre 0,0215 e 0,0289 (R19). Usar o fator médio subestima o efeito de cortar consumo no horário de ponta, quando térmicas são acionadas. |
| `participacao_chuveiro_ponta` | 0.49 | fração | PUBLICO | R20 | Participação do chuveiro na ponta de carga residencial (estudo USP/PEA). Uso concentrado entre 18h e 19h. |

## 2. Quanto o chuveiro consome (física)

O chuveiro elétrico é um aquecedor de passagem: precisa entregar, a cada segundo, o calor que a água que passa por ele precisa para subir de temperatura.

```
P = (ṁ · c · ΔT) / η
```

- ṁ (vazão mássica) = 4.0 L/min ÷ 60 = 0.0667 kg/s
- c (calor específico da água) = 4186 J/(kg·°C)
- ΔT = 38 − 20 = 18 °C
- η (eficiência) = 0.95
- **P = 0.0667 × 4186 × 18 / 0.95 = 5,288 W ≈ 5.29 kW**

Conferência de sanidade: chuveiros comerciais têm potência nominal entre ~4,5 e 7,5 kW, então o valor calculado é coerente.

Energia = Potência × Tempo:

- Tempo de chuveiro ligado por dia = 4 pessoas × 8 min ÷ 60 = 0.533 h/dia
- Energia em 30 dias = 5.288 kW × 0.533 h × 30 = **84.6 kWh/mês**
- Participação no consumo da casa (220 kWh/mês) = **38.5%**
- Calor útil entregue à água: 2.68 kWh/dia (é o que um aquecedor solar precisa fornecer).

## 3. Quanto custa 1 kWh (Enel SP, residencial)

Os impostos são calculados "por dentro" (o imposto incide sobre o próprio total):

```
Preço final = Tarifa sem impostos / (1 − ICMS − PIS/COFINS)
```

- Conta de 150 kWh → ICMS 12%: 0.78938 / (1 − 0.12 − 0.06) = **R$ 0.9627/kWh**

- Conta de 220 kWh → ICMS 18%: 0.78938 / (1 − 0.18 − 0.06) = **R$ 1.0387/kWh**


**Efeito de degrau do ICMS:** quando o consumo passa de 200 kWh, a alíquota sobe de 12% para 18% sobre a conta toda. Por isso reduzir o consumo de 220 para menos de 200 kWh economiza mais do que os kWh cortados "valem" isoladamente.


Conta de referência (220 kWh, com Tarifa Social): (220 − 80 gratuitos) × 0.78938 / (1 − 0.18 − 0.06) = **R$ 145,41/mês** (sem iluminação pública).

## 4. As alternativas, mês a mês

Energia do chuveiro retirada da rede (kWh) e geração fotovoltaica (kWh), por mês:

| Mês | Irrad. (kWh/m²·dia) | Atual | Banho 5 min | Aquecedor solar | Fotovoltaico | Solar + 5 min | Geração FV |
|---|---|---|---|---|---|---|---|
| jan | 4.8 | 87.4 | 54.6 | 24.5 | 87.4 | 15.3 | 122.8 |
| fev | 4.7 | 79.0 | 49.4 | 23.3 | 79.0 | 14.6 | 108.6 |
| mar | 4.9 | 87.4 | 54.6 | 23.2 | 87.4 | 14.5 | 125.3 |
| abr | 4.6 | 84.6 | 52.9 | 26.2 | 84.6 | 16.4 | 113.8 |
| mai | 4.4 | 87.4 | 54.6 | 29.7 | 87.4 | 18.6 | 112.5 |
| jun | 4.2 | 84.6 | 52.9 | 31.3 | 84.6 | 19.6 | 104.0 |
| jul | 4.7 | 87.4 | 54.6 | 25.8 | 87.4 | 16.1 | 120.2 |
| ago | 4.9 | 87.4 | 54.6 | 23.2 | 87.4 | 14.5 | 125.3 |
| set | 4.4 | 84.6 | 52.9 | 28.8 | 84.6 | 18.0 | 108.9 |
| out | 4.6 | 87.4 | 54.6 | 27.1 | 87.4 | 16.9 | 117.6 |
| nov | 5.0 | 84.6 | 52.9 | 21.2 | 84.6 | 13.2 | 123.8 |
| dez | 4.8 | 87.4 | 54.6 | 24.5 | 87.4 | 15.3 | 122.8 |
| **Total** |  | **1029** | **643** | **309** | **1029** | **193** | **1406** |

### 4.1 Como cada alternativa foi modelada

- **Hábitos:** mesma potência, banho de 5 min em vez de 8 min. Custo: R$ 20,00 (timer).
- **Aquecedor solar (renovável):** o sol fornece em média 70% da energia do banho (fração solar); a fração de cada mês é proporcional à irradiação do mês, limitada a 95%. O chuveiro elétrico cobre o resto. Custo = SINAPI R$ 3.359,57 × (1 + 25% de adaptações) = R$ 4.199,46.
  - Conferência física: coletor de 2 m² × 4,63 kWh/m²·dia × ~40% de eficiência do sistema ≈ 3,7 kWh/dia de calor, acima dos 2.68 kWh/dia necessários na média. A fração não chega a 100% por causa de dias nublados, perdas noturnas do reservatório e do inverno.
- **Fotovoltaico (renovável):** produtividade = irradiação média × 365 × PR = 1278 kWh/kWp·ano. Para os 1029 kWh/ano do chuveiro seriam 0.81 kWp; arredondando para módulos inteiros de 550 W → **1.1 kWp** (R$ 4.950,00 a R$ 4.5/Wp). Como o banho é à noite, toda a geração vai para a rede e volta como crédito; sobre cada kWh compensado paga-se 60% do Fio B (R$ 0.15/kWh). Créditos que sobraram no fim do ano: 0 kWh.
  - Observação de justiça na comparação: como não existe meio módulo, o menor sistema que cobre o chuveiro gera 137% da energia do banho; o excedente abate outros usos da casa. Por isso comparamos também o *investimento por kWh evitado*, que neutraliza o tamanho.
- **Combinado:** hábitos + aquecedor solar.

## 5. Comparação final (mesma necessidade, mesmos 12 meses)

| Alternativa | Renovável | kWh evitados/ano | Conta anual | Economia líquida/ano | Investimento | R$ investido por kWh/ano | Retorno simples | VPL 10 anos (10% a.a.) | CO2 evitado (kg/ano) | Alívio no pico (kW) |
|---|---|---|---|---|---|---|---|---|---|---|
| Chuveiro elétrico (situação atual) | não | 0 | R$ 1.783,03 | R$ 0,00 | R$ 0,00 | — | — | R$ 0,00 | 0,0 | 0,0 |
| Banhos de 5 min (mudança de hábito) | não | 386 | R$ 1.280,98 | R$ 502,05 | R$ 20,00 | R$ 0,05 | imediato | R$ 3.064,85 | 14,9 | 0,0 |
| Aquecedor solar de água + chuveiro de apoio | sim | 721 | R$ 958,80 | R$ 724,23 | R$ 4.199,46 | R$ 5,83 | 5,8 anos | R$ 250,62 | 27,7 | 3,7 |
| Placas solares fotovoltaicas | sim | 1.406 | R$ 489,59 | R$ 1.193,44 | R$ 4.950,00 | R$ 3,52 | 4,1 anos | R$ 2.383,18 | 54,1 | 0,0 |
| Aquecedor solar + banhos de 5 min | sim | 836 | R$ 847,38 | R$ 835,65 | R$ 4.219,46 | R$ 5,04 | 5,0 anos | R$ 915,23 | 32,2 | 3,7 |

Definições: *economia líquida* = redução da conta − manutenção anual; *retorno simples* = investimento ÷ economia líquida; *VPL* = −investimento + Σ economia/(1,10)^t, t = 1..10 (horizonte comum de 10 anos, sem valor residual, sem reajuste de tarifa — conservador); *CO2* = kWh evitados × fator médio do SIN; *alívio no pico* = potência do chuveiro × fração solar (o FV não gera às 18h–21h).

## 6. Análise de sensibilidade

Cada linha muda UMA premissa incerta e recalcula tudo. Serve para mostrar que os resultados são estimativas com faixa de variação, não números garantidos.

| Cenário | Hábitos: economia/ano | Aquecedor: economia | Aquecedor: retorno | FV: economia | FV: retorno | Combinado: economia | Combinado: retorno |
|---|---|---|---|---|---|---|---|
| Cenário base | R$ 502,05 | R$ 724,23 | 5,8 anos | R$ 1.193,44 | 4,1 anos | R$ 835,65 | 5,0 anos |
| Fração solar baixa (50%) | R$ 502,05 | R$ 526,01 | 8,0 anos | R$ 1.193,44 | 4,1 anos | R$ 711,76 | 5,9 anos |
| Fração solar alta (80%) | R$ 502,05 | R$ 823,34 | 5,1 anos | R$ 1.193,44 | 4,1 anos | R$ 897,59 | 4,7 anos |
| Aquecedor 2x mais caro (casa precisa de obra) | R$ 502,05 | R$ 724,23 | 11,6 anos | R$ 1.193,44 | 4,1 anos | R$ 835,65 | 10,1 anos |
| Fio B baixo (R$ 0,095/kWh) | R$ 502,05 | R$ 724,23 | 5,8 anos | R$ 1.254,47 | 3,9 anos | R$ 835,65 | 5,0 anos |
| Fio B alto (R$ 0,25/kWh) | R$ 502,05 | R$ 724,23 | 5,8 anos | R$ 1.082,48 | 4,6 anos | R$ 835,65 | 5,0 anos |
| FV mais barato (R$ 3,62/Wp) | R$ 502,05 | R$ 724,23 | 5,8 anos | R$ 1.193,44 | 3,3 anos | R$ 835,65 | 5,0 anos |
| FV pequeno mais caro (R$ 6,50/Wp) | R$ 502,05 | R$ 724,23 | 5,8 anos | R$ 1.193,44 | 6,0 anos | R$ 835,65 | 5,0 anos |
| Fio B não compensado a 90% (regra de 2028) | R$ 502,05 | R$ 724,23 | 5,8 anos | R$ 1.110,22 | 4,5 anos | R$ 835,65 | 5,0 anos |
| Bandeira amarela o ano todo | R$ 514,03 | R$ 743,91 | 5,6 anos | R$ 1.228,30 | 4,0 anos | R$ 857,99 | 4,9 anos |
| Família SEM Tarifa Social | R$ 575,00 | R$ 797,19 | 5,3 anos | R$ 1.193,44 | 4,1 anos | R$ 908,61 | 4,6 anos |
| Banhos de 12 min (família gasta mais) | R$ 1.036,60 | R$ 1.110,23 | 3,8 anos | R$ 1.840,16 | 4,0 anos | R$ 1.370,20 | 3,1 anos |

## 7. Leitura dos resultados

1. **Hábito é o primeiro passo:** R$ 502,05/ano com custo quase zero. Parte do ganho vem do degrau do ICMS (a casa cai abaixo de 200 kWh).
2. **Aquecedor solar** retorna em ~5,8 anos, é a única alternativa que reduz o pico do fim da tarde (~3,7 kW por casa) e não depende de regras de compensação. É sensível ao custo de obra: se a instalação dobrar de preço, o retorno passa de 10 anos.
3. **Fotovoltaico** tem o menor custo por kWh evitado e retorno de ~4,1 anos no cenário base, mas exige o maior desembolso inicial, homologação, telhado próprio e fica menos favorável com o Fio B subindo até 2028. Não alivia o pico noturno.
4. **Recomendação do assistente:** hábitos já; aquecedor solar para quem tem casa própria e telhado; fotovoltaico como opção para quem tem acesso a crédito barato ou programa social, sempre com 3 orçamentos.
