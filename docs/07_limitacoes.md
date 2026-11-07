# 7. Condições e limitações das recomendações

**Nenhuma economia, geração ou custo apresentado é resultado garantido.** São estimativas para uma família de referência sob as condições abaixo. O assistente repete isso em toda resposta com números.

## Condições assumidas

| Condição | Valor assumido | O que acontece se for diferente |
|---|---|---|
| Distribuidora | Enel SP, tarifa B1 convencional | Outras distribuidoras têm tarifa e Fio B diferentes |
| Tarifas | vigentes em nov/2026 (até 03/07/2027) | Reajuste anual em julho muda todos os valores |
| Bandeira | verde | Amarela/vermelha aumentam a economia de todas as alternativas |
| Tipo de imóvel | casa própria com telhado | Apartamento/aluguel: só a mudança de hábito é viável |
| Família | 4 pessoas, 8 min de banho, 220 kWh/mês | Use o `simular` com os dados reais |
| Água fria | 20 °C (média anual) | No inverno o chuveiro gasta mais; no verão, menos |
| Irradiação | São José dos Campos (mesma latitude) | Sombra, telhado voltado ao sul ou inclinação ruim reduzem a geração |
| Aquecedor solar | fração solar 70%, custo SINAPI + 25% | Testado de 50% a 80% e com custo 2× |
| Fotovoltaico | R$ 4,50/Wp, Fio B R$ 0,15/kWh, 60% não compensado | Testado de R$ 3,62 a 6,50/Wp, Fio B de 0,095 a 0,25 e regra de 2028 (90%) |

## Limitações do modelo

1. **Fração solar de literatura:** o valor de 70% vem de simulação em Viçosa-MG, não de medição na Grande SP.
2. **Fio B da Enel SP não verificado na fonte primária:** fontes secundárias divergem; por isso há faixa de sensibilidade.
3. **ICMS sobre energia compensada:** a faixa de ICMS foi aplicada sobre o consumo medido; o tratamento fiscal real dos créditos pode diferir.
4. **Sem reajuste de tarifa, inflação, degradação de painéis ou troca de inversor** no horizonte de 10 anos.
5. **Sem financiamento:** famílias de baixa renda geralmente precisariam de crédito; juros aumentam o retorno.
6. **CO₂ pelo fator médio do SIN:** subestima o efeito de reduzir consumo no horário de pico (quando térmicas operam) e ignora as emissões da fabricação dos equipamentos (sem análise de ciclo de vida).
7. **Assistente baseado em palavras-chave:** perguntas muito fora do roteiro caem em "não entendi" e recebem o menu de opções.
8. **Tarifa Social:** modelada apenas a gratuidade de 80 kWh; descontos para renda entre ½ e 1 salário mínimo por pessoa não foram modelados.

## O que o assistente orienta para reduzir riscos

- Pedir **pelo menos 3 orçamentos** e conferir equipamento com etiqueta INMETRO.
- Desconfiar de promessa de "conta zero".
- Chamar **eletricista** para qualquer mexida em fiação, resistência ou disjuntor.
- Conferir a potência real na etiqueta do chuveiro e o consumo real na conta.
