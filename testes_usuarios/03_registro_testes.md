# Registro dos testes

> **Transparência:** os testes registrados aqui foram feitos com **5 personas simuladas**, não com pessoas reais. Este trabalho foi feito individualmente e, no prazo disponível, não foi possível entrevistar participantes. As personas representam perfis do público-alvo. As perguntas imitam o jeito de falar desse público e foram **executadas no assistente real**. Tudo o que está registrado como resultado (intenção detectada, texto da resposta, entradas aceitas ou rejeitadas) é saída real do programa, e não opinião inventada de pessoas. O protocolo para testes com pessoas reais continua em [`01_protocolo.md`](01_protocolo.md) e é o próximo passo recomendado.

## Método

1. **Personas:** 5 perfis do público (tabela abaixo), variando idade, familiaridade com tecnologia, tipo de moradia, Tarifa Social e situação de compra.
2. **Situações:** 18 perguntas livres no estilo de cada persona (sem acento, abreviações como "mto" e "q", frases incompletas) e 1 simulação com respostas naturais ("4 pessoas", "10 minutos", "não sei", "não, é alugada").
3. **Critérios objetivos** (verificáveis rodando o programa):
   - **C1 – Entendimento da pergunta:** o assistente reconheceu o assunto, ou respondeu "não entendi"?
   - **C2 – Resposta direta:** a informação que a persona pediu aparece logo no começo da resposta?
   - **C3 – Linguagem:** termos técnicos (kWh, kWp, Fio B, homologação, payback) aparecem sem explicação?
   - **C4 – Adequação ao caso:** a resposta serve para a situação da persona (por exemplo, aluguel)?
   - **C5 – Entrada da simulação:** respostas naturais são aceitas?
4. **Duas rodadas:** a 1ª na versão entregue em 07/11 (commit `b8fe1c7`) e a 2ª depois dos ajustes. Transcrição completa da 2ª rodada: [`05_transcricao_personas.md`](05_transcricao_personas.md).

## Personas

| ID | Perfil | Moradia | Tarifa Social | Objetivo no teste |
|---|---|---|---|---|
| P1 | Cida, 58, dona de casa, pouca familiaridade com tecnologia | casa própria | sim | entender por que a conta está alta |
| P2 | Jefferson, 34, motoboy, usa celular, escreve abreviado | casa alugada | não | saber se dá para usar energia solar |
| P3 | Rosana, 45, diarista, família de 5 | casa própria | Bolsa Família | checar a promessa de um vendedor de placa solar |
| P4 | Antônio, 67, aposentado | apartamento (CDHU) | sim | saber o que funciona em apartamento |
| P5 | Larissa, 22, estudante, desconfiada | casa dos pais | não sabe | checar se os números são confiáveis |

## Resultados por situação (1ª rodada → 2ª rodada)

| Persona | Pergunta (como digitada) | 1ª rodada | Problema | 2ª rodada |
|---|---|---|---|---|
| P1 | quanto gasta meu chuveiro | `chuveiro` | custo por minuto só na 6ª linha; "kWh" e "kW" sem explicação (C2, C3) | resumo na 1ª linha + kWh explicado |
| P1 | minha conta vem muito cara | **não entendi** | C1 | `habitos`, com resumo |
| P1 | o que é kwh | **não entendi** | C1, C3 | `glossario` |
| P1 | como faço pra pagar menos | `habitos` | economia em R$ só no meio do texto (C2) | resumo na 1ª linha |
| P2 | chuveiro gasta mto? | `chuveiro` | ok (abreviação entendida) | ok |
| P2 | moro de aluguel da pra colocar aquecedor solar? | `aquecedor_solar` | falava como se fosse viável; o aviso de aluguel ficava só nas limitações (C4) | `moradia`: o que funciona para inquilino |
| P2 | vale a pena placa solar | `fotovoltaico` | "kWp", "Fio B", "homologação", "compensada" sem explicação (C3) | texto em linguagem simples + resumo |
| P3 | um vendedor falou q a placa solar zera minha conta é verdade? | `fotovoltaico` | não respondia "zera ou não"; o aviso estava na última linha (C2, C4) | `conta_zero`: começa com "NÃO" e mostra a conta antes e depois |
| P3 | e o aquecedor solar? | `aquecedor_solar` | ok | resumo com "casa própria" em destaque |
| P3 | qual é melhor pra mim | `comparar` | resposta longa (~370 palavras); recomendação só no fim (C2) | resumo com a recomendação na 1ª linha |
| P3 | tenho bolsa familia tenho desconto na luz? | **não entendi** | C1 | `tarifa_social`, citando Bolsa Família |
| P4 | moro em apartamento | **não entendi** | C1, C4 | `moradia` |
| P4 | o que da pra fazer no apartamento | **não entendi** | C1, C4 | `moradia` |
| P4 | a resistencia queimou posso trocar sozinho | `seguranca` | ok | ok |
| P5 | esses numeros sao confiaveis? | **não entendi** | C1 ("confiaveis" não casava com "confiavel") | `limitacoes`, com resumo |
| P5 | de onde vem os dados | `fontes` | ok | ok |
| P5 | quanto co2 eu economizo | `ambiente` | ok | ok |
| P5 | e se a tarifa aumentar | **não entendi** | C1 | `reajuste`, calculado com tarifa +10% |

### Simulação (P1 e P2)

| Entrada digitada | 1ª rodada | 2ª rodada |
|---|---|---|
| "4 pessoas" | rejeitada ("Digite só o número") | aceita (4) |
| "10 minutos" | rejeitada | aceita (10) |
| "não sei" (consumo em kWh) | rejeitada sem saída: só seguia com Enter | aceita: estima o consumo pelo tamanho da família |
| "não, é alugada" (casa própria?) | pergunta não existia: oferecia aquecedor e placas a inquilinos | marca solar como "geralmente não é possível" |

## Resumo quantitativo

| Medida | 1ª rodada | 2ª rodada |
|---|---|---|
| Perguntas que caíram em "não entendi" (C1) | **7 de 18 (39%)** | **0 de 18** |
| Respostas principais que começam com a resposta direta em 1 frase (C2) | 0 de 8 | 8 de 8 |
| Respostas não adequadas à moradia da persona (C4) | 3 | 0 |
| Entradas naturais aceitas na simulação (C5) | 0 de 4 | 4 de 4 |
| Testes automatizados | 49 | 74 (25 novos, cobrindo as frases das personas) |

## O que esta avaliação NÃO mede

- **Compreensão real:** se uma pessoa de verdade entende o texto. As personas mostram se o assistente reconhece a pergunta e se a resposta contém a informação, mas não substituem perguntar a alguém "o que você entendeu?".
- **Satisfação e confiança:** notas de clareza e utilidade de 1 a 5 só podem vir de pessoas reais.
- **Perguntas imprevistas:** as frases foram escritas pela própria avaliação; usuários reais vão falar coisas diferentes.

Por isso, o próximo passo recomendado é aplicar [`01_protocolo.md`](01_protocolo.md) com pelo menos 3 pessoas reais.
