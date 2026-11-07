# Protocolo dos testes com usuários

**Objetivo:** verificar se as orientações de energia do assistente são **compreendidas** e **úteis** para o público, e ajustar o que não funcionar.

## Participantes

- **Mínimo de 5 pessoas**, de preferência do público-alvo ou próximas dele (familiares, vizinhos, colegas que pagam conta de luz, alguém que conheça o CadÚnico).
- Variedade: ao menos 1 pessoa com mais de 50 anos e 1 pessoa sem familiaridade com tecnologia.
- **Privacidade:** não registrar nome, CPF, endereço, NIS ou foto da conta. Usar códigos (P1, P2…), faixa etária e se mora em casa/apartamento. Pedir consentimento verbal antes (modelo abaixo).

> "Estamos testando um assistente de um trabalho da faculdade. Vamos anotar só suas respostas e comentários, sem seu nome. Você pode parar quando quiser. Tudo bem?"

## Como aplicar (15–20 min por pessoa)

1. Explique em uma frase: "É um assistente que ajuda a gastar menos com o chuveiro."
2. Rode `python -m citizen_energia` e **deixe a pessoa digitar** (ou dite exatamente o que ela falar).
3. Proponha as **6 situações** de `02_roteiro_e_formulario.md`, sem explicar o resultado antes.
4. Depois de cada resposta, faça as perguntas de compreensão e anote **as palavras da pessoa**.
5. No fim, aplique as perguntas gerais.
6. Registre tudo em `03_registro_testes.md`.

## Critérios de sucesso

| Medida | Meta |
|---|---|
| Acerta a pergunta de compreensão | ≥ 4 de 6 situações por pessoa |
| Nota de clareza (1 a 5) | média ≥ 4 |
| Nota de utilidade (1 a 5) | média ≥ 4 |
| Entende que os números são estimativas | ≥ 4 de 5 pessoas |

## Depois dos testes

- Agrupe os problemas que apareceram em **2 ou mais** pessoas.
- Corrija no código/textos (em `assistente.py` ou `parametros.json`), rode `python -m pytest -q` e registre em `04_ajustes_realizados.md` (o que mudou, por quê, qual teste motivou, commit).
- Se possível, faça uma **2ª rodada curta** com 2 pessoas para confirmar que o ajuste resolveu.
