# 5. Recomendações e justificativas

Valores do cenário base (família de referência, 12 meses). Faixas vêm da [análise de sensibilidade](04_calculos_gerados.md#6-análise-de-sensibilidade).

## 5.1 Matriz de decisão

| Critério | Banhos de 5 min | Aquecedor solar | Fotovoltaico (1,1 kWp) |
|---|---|---|---|
| **Custo inicial** | R$ 20 | R$ 4.199 (até ~R$ 8.400 com obra) | R$ 4.950 (R$ 4.000–7.150) |
| **Economia líquida/ano** | R$ 502 | R$ 724 (R$ 526–823) | R$ 1.193 (R$ 1.082–1.254) |
| **Retorno** | imediato | 5,8 anos (5,1–11,6) | 4,1 anos (3,3–6,0) |
| **Investimento por kWh evitado/ano** | R$ 0,05 | R$ 5,83 | R$ 3,52 |
| **Comparação justa (FV do tamanho exato do banho)** | — | — | R$ 3.626 · R$ 847/ano · 4,3 anos |
| **Renovável** | não (eficiência) | sim — solar térmica | sim — solar fotovoltaica |
| **CO₂ evitado/ano** | 15 kg | 28 kg | 54 kg |
| **Alívio no pico 18h–21h** | não muda a potência | ~3,7 kW por casa, em média (menos em dia nublado) | nenhum (não gera à noite) |
| **Exige casa própria / telhado** | não | sim | sim |
| **Burocracia** | nenhuma | nenhuma (só instalação) | projeto + homologação na Enel |
| **Depende de regra regulatória** | não | não | sim (Fio B: 60% → 90% até 2028) |
| **Manutenção** | — | limpeza anual do coletor | limpeza; troca do inversor em ~10–12 anos |
| **Risco principal** | hábito não se manter | custo de obra; inverno | preço de sistema pequeno; regra pós-2029 incerta |

## 5.2 Justificativa por alternativa

### Banhos de 5 minutos — recomendada para todos, primeiro
- **Custo:** praticamente zero. **Viabilidade:** total — vale para casa, apartamento, aluguel.
- **Por que economiza tanto:** além dos 386 kWh/ano evitados, a casa cai de 220 para ~188 kWh/mês, abaixo do degrau de 200 kWh do ICMS-SP. A alíquota da conta inteira cai de 18% para 12%. É um efeito real, mas só existe se o consumo total cruzar o limite.
- **Ambiental:** reduz energia **e água**: 3 min × 4 L/min × 365 dias ≈ 4.380 L/ano por pessoa, ~17.500 L/ano para a família. Não muda a potência no pico, mas encurta o tempo do chuveiro ligado nesse horário.
- **Limitação:** depende de comportamento contínuo.

### Aquecedor solar de água — recomendada para casa própria com telhado
- **Custo:** referência pública SINAPI (R$ 3.359,57 instalado) + 25% de adaptações. Em casas sem tubulação de água quente pode dobrar, e o retorno passa de 10 anos.
- **Viabilidade:** telhado com sol (idealmente voltado ao norte), estrutura para ~250 kg de reservatório cheio, caixa d'água acima do boiler. Não serve para a maioria dos apartamentos nem para aluguel sem autorização.
- **Ambiental:** fonte renovável; a principal vantagem sistêmica é **tirar ~3,7 kW do pico** por casa, horário em que o sistema aciona térmicas — o fator médio do SIN subestima esse benefício. Fabricação usa cobre, vidro e aço inox (recicláveis).
- **Por que ela vem antes do fotovoltaico na recomendação**, mesmo com retorno um pouco maior: não depende de regras de compensação que vão piorar até 2028, não exige homologação e é a única que ajuda a rede no horário crítico. Programas habitacionais (como o Minha Casa Minha Vida) já usam esse equipamento para o público de baixa renda.

### Placas fotovoltaicas — recomendada com ressalvas
- **Custo:** maior desembolso inicial; sistemas muito pequenos custam mais por watt.
- **Viabilidade:** telhado próprio, projeto elétrico, instalador habilitado e homologação na Enel. A energia do banho (noturna) depende 100% de créditos na rede.
- **Regras:** Lei 14.300/2022 — 60% do Fio B não compensado em 2026, 75% em 2027, 90% em 2028; após 2029 a regra ainda é incerta. No cenário de 90%, o retorno passa de 4,1 para 4,5 anos.
- **Comparação justa:** como o menor sistema real gera 137% da energia do banho, também simulamos um sistema hipotético do tamanho exato do banho (0,81 kWp): R$ 3.626, R$ 847/ano, retorno de 4,3 anos. A vantagem anual sobre o aquecedor solar cai de R$ 469 para R$ 123.
- **Ambiental:** maior CO₂ evitado (gera mais kWh porque o menor sistema viável, 2 módulos, produz 137% da energia do banho). Não alivia o pico noturno. Módulos e inversores exigem descarte adequado ao fim da vida útil.
- **Alternativa para quem não tem telhado:** geração compartilhada ("energia por assinatura") — citada pelo assistente, mas não calculada.

## 5.3 Coerência entre análise e respostas do assistente

As respostas do assistente são **montadas a partir das mesmas funções** que geram as tabelas acima (`calculos.comparar`, `calculos.resumo_perfil`). O teste `test_numeros_da_resposta_sao_os_da_analise` verifica que os valores exibidos ao cidadão são idênticos aos da análise. Se um parâmetro mudar no JSON, tabelas, gráficos e respostas mudam juntos.
