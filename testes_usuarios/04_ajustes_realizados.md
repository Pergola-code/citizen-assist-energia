# Ajustes realizados

## Ajustes a partir de verificação técnica interna (antes dos testes com usuários)

Estes ajustes vieram de testes automatizados e revisão da equipe, não de usuários:

| # | O que foi observado | Ajuste | Onde |
|---|---|---|---|
| T1 | A mensagem "solar" era entendida como saudação, porque "olá" aparece dentro de "s**ola**r". | Gatilhos passaram a exigir início de palavra; "solar" sozinho gera a pergunta "aquecedor ou fotovoltaica?". | `assistente.py` · `test_ola_nao_confunde_com_solar` |
| T2 | "Vale a pena aquecedor solar?" caía na comparação geral, não na resposta sobre o aquecedor. | Tecnologias específicas passaram a ter prioridade; só pedidos explícitos ("compare", "ou", "vs") vão para a comparação. | `assistente.py` · `test_intencoes` |
| T3 | "O que é Fio B?" caía em segurança elétrica (gatilho "fio"). | "fio b" e "Lei 14.300" viraram gatilhos do fotovoltaico; segurança usa "fiação". | `assistente.py` |
| T4 | Simulação com consumo baixo e muitos banhos gerava chuveiro > 60% da conta sem aviso. | Alerta automático para revisar os dados informados. | `assistente.py` · `test_alerta_quando_dados_parecem_inconsistentes` |
| T5 | A comparação FV parecia injusta: o menor sistema (2 módulos) gera 137% da energia do banho. | Inclusão do indicador "investimento por kWh evitado/ano" e nota explicativa. | `calculos.py`, `04_calculos_gerados.md` |

## Ajustes a partir dos testes com usuários

> ⚠️ **PREENCHER depois dos testes reais.** Um ajuste por linha, ligado ao problema que o motivou.

| # | Problema observado (participantes) | Ajuste feito | Arquivo/função | Commit | Confirmado na 2ª rodada? |
|---|---|---|---|---|---|
| U1 | — | — | — | — | — |
| U2 | — | — | — | — | — |
| U3 | — | — | — | — | — |

Exemplos de ajustes comuns (use só se o problema realmente aparecer):
- trocar "kWh" por "kWh (unidade da conta de luz)" na primeira menção;
- trocar "payback" por "em quanto tempo se paga";
- encurtar a resposta de comparação mostrando primeiro só a recomendação.
