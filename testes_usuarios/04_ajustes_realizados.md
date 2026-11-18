# Ajustes realizados

## Ajustes a partir da avaliação com personas simuladas

Cada ajuste está ligado ao problema registrado em [`03_registro_testes.md`](03_registro_testes.md) e tem teste automatizado em `tests/test_assistente.py` para não voltar a acontecer.

| # | Problema (persona · critério) | Ajuste feito | Onde |
|---|---|---|---|
| A1 | Informação pedida enterrada no meio de respostas de 200 a 370 palavras (P1, P3 · C2) | Toda resposta principal começa com **">> RESUMO:"**, uma frase com a resposta direta | `Resposta.resumo` / `formatada()` · `test_toda_resposta_principal_comeca_com_resumo` |
| A2 | "minha conta vem muito cara" → não entendi (P1 · C1) | Gatilhos de "conta alta/cara/vem/veio" levam às dicas de economia | `INTENCOES["habitos"]` · `test_frases_das_personas` |
| A3 | Promessa de vendedor ("zera a conta?") sem resposta direta (P3 · C2, C4) | Nova intenção `conta_zero`: começa com "NÃO", explica o que continua sendo cobrado e mostra a conta antes e depois, calculada pelo motor | `r_conta_zero` · `test_conta_zero_diz_nao_e_usa_numeros_do_motor` |
| A4 | Aluguel e apartamento recebiam orientação de solar como se fosse viável (P2, P4 · C1, C4) | Nova intenção `moradia` (o que funciona para inquilinos) e nova pergunta "casa própria?" na simulação | `r_moradia`, `simulacao_personalizada(casa_propria=)` · `test_simulacao_sem_casa_propria_nao_oferece_solar` |
| A5 | "e se a tarifa aumentar" → não entendi (P5 · C1) | Nova intenção `reajuste`, que recalcula as alternativas com tarifa +10% | `r_reajuste` · `test_reajuste_aumenta_economia` |
| A6 | Links longos em toda resposta poluíam a leitura no celular (P1, P2 · legibilidade) | Respostas mostram só o título da fonte; os links completos aparecem ao digitar "fontes" | `formatada(com_links=)` |
| A7 | "o que é kwh" → não entendi; kWh, kWp, Fio B e homologação apareciam sem explicação (P1, P2 · C1, C3) | Glossário com 10 termos em linguagem simples; textos do chuveiro, do fotovoltaico e da comparação reescritos sem jargão | `GLOSSARIO`, `r_glossario` · `test_glossario_explica_o_termo_perguntado` |
| A8 | Simulação rejeitava "4 pessoas" e "10 minutos" (P1 · C5) | Extração do primeiro número do texto, aceitando o formato brasileiro (1.250,5) | `__main__.extrair_numero` · `test_extrair_numero` |
| A9 | Quem não sabe o consumo da conta não tinha saída (P1 · C5) | Aceita "não sei" e estima o consumo pelo tamanho da família; o valor sugerido deixa de ser fixo em 220 kWh | `calculos.estimar_consumo_total` · `test_estimativa_de_consumo_cresce_com_a_familia` |
| A10 | "bolsa familia" e "confiaveis" não eram reconhecidos (P3, P5 · C1) | Novos gatilhos para Tarifa Social (Bolsa Família, NIS, benefício) e para limitações ("confia") | `INTENCOES` · `test_frases_das_personas` |

## Ajustes a partir da verificação técnica interna (antes das personas)

| # | O que foi observado | Ajuste | Onde |
|---|---|---|---|
| T1 | A mensagem "solar" era entendida como saudação, porque "ola" aparece dentro de "s**ola**r" | Gatilhos passaram a exigir início de palavra; "solar" sozinho gera a pergunta "aquecedor ou fotovoltaica?" | `assistente.py` · `test_ola_nao_confunde_com_solar` |
| T2 | "Vale a pena aquecedor solar?" caía na comparação geral | Tecnologias específicas passaram a ter prioridade; só pedidos explícitos ("compare", "ou", "vs") vão para a comparação | `assistente.py` · `test_intencoes` |
| T3 | "O que é Fio B?" caía em segurança elétrica (gatilho "fio") | Segurança passou a usar "fiação"; hoje a pergunta vai para o glossário (A7) | `assistente.py` |
| T4 | Simulação com consumo baixo e muitos banhos gerava chuveiro acima de 60% da conta sem aviso | Alerta automático para revisar os dados informados | `test_alerta_quando_dados_parecem_inconsistentes` |
| T5 | Comparação com o fotovoltaico parecia injusta: o menor sistema (2 módulos) gera 137% da energia do banho | Indicador "investimento por kWh evitado/ano" e nota explicativa | `calculos.py`, `docs/04_calculos_gerados.md` |

## Pendente: testes com pessoas reais

> Preencher se os testes com pessoas forem feitos (ver [`01_protocolo.md`](01_protocolo.md)).

| # | Problema observado (participantes) | Ajuste feito | Arquivo/função |
|---|---|---|---|
| U1 | — | — | — |
