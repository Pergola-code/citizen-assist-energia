# Roteiro do vídeo técnico (máx. 3 minutos)

YouTube **não listado**. Grave a tela com o terminal (fonte grande, ≥ 18 pt) e os gráficos de `docs/img/`. Fale devagar; corte pausas na edição.

| Tempo | Tela | Fala (sugestão) |
|---|---|---|
| 0:00–0:20 | Slide/README com título e nomes | "Somos [nomes]. Esta é a contribuição de Energias Renováveis ao Citizen Assist AI. Nosso público são famílias de baixa renda da Grande SP que usam chuveiro elétrico." |
| 0:20–0:45 | `docs/04_calculos_gerados.md`, seção 2 | "O chuveiro é um aquecedor de passagem: P = ṁ·c·ΔT/η. Com 4 litros por minuto e 18 graus de aumento, dá 5,3 kW. Numa família de 4 pessoas, com 8 minutos de banho, são 85 kWh por mês, 38% da conta." |
| 0:45–1:25 | `conta_anual.png` e `retorno_acumulado.png` | "Comparamos, para a mesma necessidade e os mesmos 12 meses: banho de 5 minutos, aquecedor solar de água e placas fotovoltaicas — as duas últimas renováveis. O hábito economiza ~R$ 500 por ano sem custo, em parte porque a conta cai abaixo de 200 kWh e o ICMS cai de 18 para 12%. O aquecedor solar se paga em ~6 anos e tira 3,7 kW do pico do fim da tarde. O fotovoltaico se paga em ~4 anos, mas exige mais dinheiro na entrada, homologação, e o Fio B sobe até 2028." |
| 1:25–2:25 | Terminal: `python -m citizen_energia` | Digitar: "quanto meu chuveiro gasta?" → "vale a pena aquecedor solar?" → "compare as opções" → `simular` com 3 pessoas, 10 min, 180 kWh. "Toda resposta mostra fontes e limitações, e os números vêm do mesmo código da análise." |
| 2:25–2:50 | Tabela de sensibilidade (seção 6) | "Não tratamos estimativa como certeza: se a casa precisar de obra, o retorno do aquecedor vai para quase 12 anos; com Fio B de 2028, o fotovoltaico passa para 4,5. Por isso o assistente recomenda: hábito primeiro, aquecedor solar para casa própria com telhado, fotovoltaico com ressalvas." |
| 2:50–3:00 | README | "Testamos com usuários e ajustamos a linguagem. Código, dados e referências estão no GitHub. Obrigado!" |

Checklist antes de publicar: duração ≤ 3:00 · áudio claro · link não listado funcionando em aba anônima.
