# Roteiro do vídeo técnico (máx. 3 minutos)

YouTube **não listado**. São ~390 palavras de fala, que dão ~2:50 num ritmo calmo. Ensaie uma vez com cronômetro.

## Antes de gravar

- Terminal com fonte grande (18 pt ou mais) e janela limpa (`cls` no Windows, `clear` no Mac/Linux).
- Deixe abertos, em abas: `README.md`, `docs/04_calculos_gerados.md` (seções 2 e 6), `docs/img/conta_anual.png`, `docs/img/retorno_acumulado.png` e o terminal na pasta do projeto.
- Gravador: OBS Studio, Win+G (Windows) ou Cmd+Shift+5 (Mac). Microfone de fone de ouvido já resolve.
- Se forem 3 pessoas: A fala as cenas 1 e 2, B as cenas 3 e 4, C as cenas 5 a 7.

## Cenas

### 1 · Abertura (0:00–0:15)
**Mostrar:** `README.md`, título e tabela de integrantes.
**Falar:**
> "Olá! Somos [nomes], da turma 1CC. Este vídeo apresenta a contribuição de Energias Renováveis ao Citizen Assist AI: um módulo que ajuda famílias de baixa renda a gastar menos com o chuveiro elétrico."

### 2 · Público e necessidade (0:15–0:40)
**Mostrar:** `docs/01_contexto.md`, tabela da família de referência.
**Falar:**
> "Nosso público são famílias da Grande São Paulo atendidas pela Enel, muitas com Tarifa Social. Desde 2025 elas não pagam os primeiros 80 kWh do mês, mas tudo acima disso é cobrado cheio. E o maior vilão da conta é o chuveiro elétrico, que ainda pesa no horário de pico, entre 18 e 21 horas."

### 3 · Análise de consumo (0:40–1:05)
**Mostrar:** `docs/04_calculos_gerados.md`, seção 2 (fórmula P = ṁ·c·ΔT/η).
**Falar:**
> "Calculamos o consumo pela física. O chuveiro aquece a água enquanto ela passa: a potência é a vazão, vezes o calor específico da água, vezes o aumento de temperatura, dividido pela eficiência. Com 4 litros por minuto e 18 graus de aquecimento, dá 5,3 quilowatts. Numa família de 4 pessoas, com banhos de 8 minutos, são 85 kWh por mês: 38% da conta."

### 4 · Comparação das alternativas (1:05–1:40)
**Mostrar:** `conta_anual.png` e, na segunda metade da fala, `retorno_acumulado.png`.
**Falar:**
> "Comparamos três alternativas para essa mesma necessidade, no mesmo período de 12 meses. Primeira: banho de 5 minutos. Custa quase nada e economiza uns 500 reais por ano, em parte porque a conta cai abaixo de 200 kWh e o ICMS cai de 18 para 12%. Segunda: aquecedor solar de água, uma fonte renovável. Custa cerca de 4.200 reais, se paga em uns 6 anos e tira 3,7 quilowatts do horário de pico. Terceira: placas fotovoltaicas, também renováveis. Se pagam em uns 4 anos, mas exigem mais dinheiro na entrada e homologação, e a cobrança do Fio B sobe até 2028."

### 5 · Demonstração do assistente (1:40–2:30)
**Mostrar:** terminal.
**Fazer:**
1. `python -m citizen_energia`
2. Digitar: `quanto meu chuveiro gasta?`
3. Digitar: `vale a pena aquecedor solar?` e rolar até "Atenção" e "De onde vêm esses números".
4. Digitar: `simular` e responder 3, 10, 180, n.

**Falar** (enquanto faz):
> "Agora o assistente funcionando. Pergunto quanto o chuveiro gasta, e ele responde em linguagem simples, até com o custo de cada minuto de banho. Pergunto se vale a pena aquecedor solar. Repare que toda resposta traz as fontes e avisa que os números são estimativas. Com 'simular', o cidadão usa os dados da própria conta de luz. Os números das respostas saem do mesmo código da análise, e um teste automatizado garante isso."

### 6 · Limitações e recomendação (2:30–2:50)
**Mostrar:** `docs/04_calculos_gerados.md`, seção 6 (tabela de sensibilidade).
**Falar:**
> "Testamos as incertezas. Se a casa precisar de obra, o aquecedor leva quase 12 anos para se pagar. Por isso o assistente recomenda: hábito primeiro, aquecedor solar para quem tem casa própria e telhado, e fotovoltaico com ressalvas."

### 7 · Encerramento (2:50–3:00)
**Mostrar:** pasta `testes_usuarios/` e depois o `README.md`.
**Falar:**
> "Testamos com [N] pessoas e ajustamos a linguagem. Código, dados e referências estão no GitHub. Obrigado!"

## Antes de publicar

- Duração de no máximo 3:00 e áudio claro.
- Visibilidade **não listado**; abra o link numa aba anônima para conferir que funciona.
