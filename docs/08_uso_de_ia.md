# 8. Uso de IA generativa

O enunciado permite o uso criterioso de IA generativa, sendo o autor responsável por verificar dados, cálculos, referências e recomendações e por demonstrar compreensão das decisões adotadas.

## Onde a IA foi usada

- Busca de fontes públicas (tarifas, legislação, custos de referência, fatores de emissão).
- Escrita de código, testes automatizados e documentação.
- **Avaliação com personas simuladas:** a IA ajudou a criar 5 personas do público e a escrever perguntas no estilo delas. As perguntas foram executadas no assistente real; os resultados registrados são saídas reais do programa. As personas **não são pessoas reais** e não substituem testes com usuários (ver `testes_usuarios/03_registro_testes.md`).
- Montagem do vídeo técnico (slides, gráficos e gravação da demonstração do terminal).

## Verificações realizadas

- [x] Cada número de fonte usado em `parametros.json` foi lido na página citada em `06_referencias.md` (consulta em nov/2026). Onde as fontes divergem (Fio B da Enel SP), o valor está marcado como ESTIMADO e há faixa de sensibilidade.
- [x] Potência do chuveiro, energia mensal, conta de referência, economia do hábito e retorno do aquecedor solar foram **recalculados de forma independente**, fora do código do projeto, e bateram com os valores de `04_calculos_gerados.md`.
- [x] Conferência física: a potência calculada (5,29 kW) está dentro da faixa dos chuveiros vendidos (4,5–7,5 kW), e o coletor de 2 m² fornece mais calor que o necessário na média (3,7 contra 2,7 kWh/dia).
- [x] `python -m pytest -q`: 74 testes passando, incluindo o teste que garante que as respostas do assistente usam exatamente os números da análise.
- [ ] Sei explicar: por que P = ṁ·c·ΔT/η, o degrau do ICMS em 200 kWh, o que é fração solar, o que é Fio B e por que o aquecedor solar alivia o pico e o fotovoltaico não. *(Marcar depois de revisar.)*

## Decisões propostas com apoio de IA e assumidas pelo autor

- Escolha do público (baixa renda, Enel SP) e da necessidade (água quente do banho).
- Escolha das alternativas (hábito, aquecedor solar, fotovoltaico) e da ordem de recomendação.
- Valores das premissas estimadas e das faixas de sensibilidade.
