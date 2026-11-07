# 8. Uso de IA generativa

O enunciado permite o uso criterioso de IA generativa, com a equipe responsável por verificar dados, cálculos, referências e recomendações.

## Onde a IA foi usada

- Apoio na busca de fontes públicas (tarifas, legislação, custos de referência).
- Apoio na escrita de código e documentação.

## Como verificamos (checklist da equipe)

Marque cada item depois de conferir pessoalmente:

- [ ] Abrimos cada link de `06_referencias.md` e conferimos que o número citado está na fonte.
- [ ] Conferimos a tarifa da Enel SP numa conta de luz real ou no site da ANEEL.
- [ ] Refizemos à mão (ou em planilha) o cálculo da potência do chuveiro (seção 2 de `04_calculos_gerados.md`).
- [ ] Refizemos à mão a conta de luz de referência (seção 3).
- [ ] Conferimos um mês da tabela mensal e o retorno de uma alternativa.
- [ ] Rodamos `python -m pytest -q` (todos os testes passando).
- [ ] Cada integrante sabe explicar: por que P = ṁ·c·ΔT/η, o degrau do ICMS, o que é fração solar, o que é Fio B e por que o aquecedor solar alivia o pico e o fotovoltaico não.

## Decisões tomadas pela equipe (não delegadas à IA)

- Escolha do público e da necessidade.
- Escolha das alternativas e da ordem de recomendação.
- Valores das premissas estimadas e das faixas de sensibilidade.
