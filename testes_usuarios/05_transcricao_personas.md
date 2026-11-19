# Transcrição da avaliação com personas simuladas (2ª rodada, versão ajustada)

> **Personas simuladas, não pessoas reais.** As perguntas foram escritas para imitar o jeito de falar do público (sem acento, abreviações, frases incompletas) e executadas no assistente real. As respostas abaixo são a saída real do programa. Gerado por `python testes_usuarios/gerar_transcricao.py`.

## P1 · Cida, 58, dona de casa, casa própria, Tarifa Social, pouca familiaridade com tecnologia

### "quanto gasta meu chuveiro"

Intenção antes dos ajustes: `chuveiro` → depois: `chuveiro`

```
>> RESUMO: o banho custa cerca de R$ 87,87 por mês (R$ 0,09 por minuto de chuveiro ligado).

O chuveiro elétrico costuma ser o aparelho que mais gasta numa casa como a sua.

Para 4 pessoas tomando banho de 8 minutos por dia:
  - O chuveiro puxa cerca de 5,3 kW enquanto está ligado (para esquentar a água de 20°C até 38°C).
  - Isso dá uns 85 kWh por mês (kWh é a unidade que aparece na sua conta de luz), ou 38% do que a casa gasta.
  - Custo aproximado: R$ 87,87 por mês só com banho.
  - Cada minuto de banho (com o chuveiro ligado) custa cerca de R$ 0,09.

Quer saber como diminuir esse gasto? Pergunte "como economizar no banho" ou "vale a pena aquecedor solar".

Atenção:
  - O cálculo usa uma vazão de 4 litros/minuto e água fria a 20°C (média do ano). No inverno o chuveiro gasta mais; no verão, menos.
  - Confira a potência real na etiqueta do seu chuveiro.

De onde vêm esses números:
  [R01] Resolução Homologatória ANEEL nº 3.596/2026 – tarifas Enel SP (B1 residencial: TUSD 472,42 + TE 316,96 R$/MWh; vigência 04/07/2026 a 03/07/2027)
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  [R10] Impacto das mudanças climáticas no consumo de chuveiros elétricos (banho diário de 8 min)
  (Para ver os links, digite: fontes)
```

### "minha conta vem muito cara"

Intenção antes dos ajustes: `nao_entendi` → depois: `habitos`

```
>> RESUMO: o chuveiro é cerca de 38% da conta; banho de 5 minutos economiza uns R$ 502,05 por ano, sem gastar nada.

Dá para economizar sem gastar nada. As ações que mais pesam, em ordem:

1. Banho de 5 minutos (hoje: 8 min). Na família de referência isso economiza cerca de 386 kWh e R$ 502,05 por ano.
   Dica: desligue o chuveiro enquanto se ensaboa. Um timer de cozinha ajuda as crianças.
2. Use a posição "verão" (morno) nos dias quentes: ela usa uma resistência menor.
3. Evite banho entre 18h e 21h quando possível: é o horário em que a rede está mais carregada.
4. Nunca mexa na resistência ou na fiação do chuveiro sozinho: chame um eletricista.

Por que a economia é tão boa? Em São Paulo, quando a conta passa de 200 kWh o ICMS sobe de 12% para 18% sobre a conta INTEIRA. Hoje seu kWh custa cerca de R$ 1,04 com impostos. Cair para menos de 200 kWh faz o imposto de todos os kWh baixar.

Atenção:
  - A economia só acontece se o hábito mudar de verdade, todos os dias.
  - O efeito da faixa de ICMS só aparece se o consumo total ficar abaixo de 200 kWh no mês.

De onde vêm esses números:
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  [R10] Impacto das mudanças climáticas no consumo de chuveiros elétricos (banho diário de 8 min)
  [R20] Chuveiro elétrico: 49% da ponta residencial; uso concentrado das 18h às 19h
  (Para ver os links, digite: fontes)
```

### "o que é kwh"

Intenção antes dos ajustes: `nao_entendi` → depois: `glossario`

```
>> RESUMO: kWh (quilowatt-hora) é a unidade de energia que aparece na sua conta de luz.

- kWh (quilowatt-hora): é a unidade de energia que aparece na sua conta de luz. 1 kWh é a energia de um aparelho de 1.000 watts ligado por 1 hora. Seu chuveiro gasta mais ou menos 1 kWh a cada 11 minutos.
```

### "como faço pra pagar menos"

Intenção antes dos ajustes: `habitos` → depois: `habitos`

```
>> RESUMO: o chuveiro é cerca de 38% da conta; banho de 5 minutos economiza uns R$ 502,05 por ano, sem gastar nada.

Dá para economizar sem gastar nada. As ações que mais pesam, em ordem:

1. Banho de 5 minutos (hoje: 8 min). Na família de referência isso economiza cerca de 386 kWh e R$ 502,05 por ano.
   Dica: desligue o chuveiro enquanto se ensaboa. Um timer de cozinha ajuda as crianças.
2. Use a posição "verão" (morno) nos dias quentes: ela usa uma resistência menor.
3. Evite banho entre 18h e 21h quando possível: é o horário em que a rede está mais carregada.
4. Nunca mexa na resistência ou na fiação do chuveiro sozinho: chame um eletricista.

Por que a economia é tão boa? Em São Paulo, quando a conta passa de 200 kWh o ICMS sobe de 12% para 18% sobre a conta INTEIRA. Hoje seu kWh custa cerca de R$ 1,04 com impostos. Cair para menos de 200 kWh faz o imposto de todos os kWh baixar.

Atenção:
  - A economia só acontece se o hábito mudar de verdade, todos os dias.
  - O efeito da faixa de ICMS só aparece se o consumo total ficar abaixo de 200 kWh no mês.

De onde vêm esses números:
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  [R10] Impacto das mudanças climáticas no consumo de chuveiros elétricos (banho diário de 8 min)
  [R20] Chuveiro elétrico: 49% da ponta residencial; uso concentrado das 18h às 19h
  (Para ver os links, digite: fontes)
```

## P2 · Jefferson, 34, motoboy, casa alugada, 3 pessoas, sem Tarifa Social, usa celular

### "chuveiro gasta mto?"

Intenção antes dos ajustes: `chuveiro` → depois: `chuveiro`

```
>> RESUMO: o banho custa cerca de R$ 87,87 por mês (R$ 0,09 por minuto de chuveiro ligado).

O chuveiro elétrico costuma ser o aparelho que mais gasta numa casa como a sua.

Para 4 pessoas tomando banho de 8 minutos por dia:
  - O chuveiro puxa cerca de 5,3 kW enquanto está ligado (para esquentar a água de 20°C até 38°C).
  - Isso dá uns 85 kWh por mês (kWh é a unidade que aparece na sua conta de luz), ou 38% do que a casa gasta.
  - Custo aproximado: R$ 87,87 por mês só com banho.
  - Cada minuto de banho (com o chuveiro ligado) custa cerca de R$ 0,09.

Quer saber como diminuir esse gasto? Pergunte "como economizar no banho" ou "vale a pena aquecedor solar".

Atenção:
  - O cálculo usa uma vazão de 4 litros/minuto e água fria a 20°C (média do ano). No inverno o chuveiro gasta mais; no verão, menos.
  - Confira a potência real na etiqueta do seu chuveiro.

De onde vêm esses números:
  [R01] Resolução Homologatória ANEEL nº 3.596/2026 – tarifas Enel SP (B1 residencial: TUSD 472,42 + TE 316,96 R$/MWh; vigência 04/07/2026 a 03/07/2027)
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  [R10] Impacto das mudanças climáticas no consumo de chuveiros elétricos (banho diário de 8 min)
  (Para ver os links, digite: fontes)
```

### "moro de aluguel da pra colocar aquecedor solar?"

Intenção antes dos ajustes: `aquecedor_solar` → depois: `moradia`

```
>> RESUMO: aquecedor solar e placas geralmente não dão; o banho de 5 minutos funciona em qualquer casa e economiza uns R$ 502,05 por ano.

Para quem mora de aluguel ou em apartamento, o aquecedor solar e as placas solares geralmente não são possíveis: precisam de telhado próprio e de obra. O que funciona para você:

  1. Banho de 5 minutos: economiza cerca de R$ 502,05 por ano e não precisa de obra nem de autorização.
  2. Use a posição "verão" (morno) do chuveiro nos dias quentes.
  3. Confira se você tem direito à Tarifa Social (pergunte "tenho direito à tarifa social?").
  4. Energia por assinatura (geração compartilhada): você paga uma empresa que tem uma usina solar e recebe desconto na conta, sem instalar nada. Confira se o desconto compensa e se não há multa para cancelar.

Se for aluguel de casa: dá para conversar com o dono sobre instalar um aquecedor solar, porque ele valoriza o imóvel. Em prédio, o condomínio pode instalar um sistema coletivo.

Atenção:
  - A energia por assinatura não foi calculada aqui: o desconto varia de empresa para empresa.

De onde vêm esses números:
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R06] Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês (Luz do Povo)
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  (Para ver os links, digite: fontes)
```

### "vale a pena placa solar"

Intenção antes dos ajustes: `fotovoltaico` → depois: `fotovoltaico`

```
>> RESUMO: custa uns R$ 4.950,00 e se paga em cerca de 4 anos, mas exige casa própria, autorização da Enel e a conta não zera.

Placas fotovoltaicas são RENOVÁVEIS: transformam luz do sol em eletricidade. A energia que sobra durante o dia vai para a rede e vira crédito na sua conta.

Para cobrir a energia do chuveiro da família de referência:
  - 2 placas (1,1 kWp), gerando uns 117 kWh por mês.
  - Investimento estimado: R$ 4.950,00.
  - Economia estimada: R$ 1.193,44 por ano; se paga em cerca de 4,1 anos.

Pontos importantes:
  - O banho é à noite e as placas geram de dia: você depende dos créditos na rede.
  - Você continua pagando uma parte da conta: a lei cobra uma taxa pelo uso dos fios da Enel (o "Fio B"), que vai subir até 2028.
  - Precisa de projeto, instalador e autorização da Enel (homologação). A conta NÃO zera: pergunte "placa solar zera a conta?".

Atenção:
  - O valor do Fio B da Enel SP não é publicado de forma simples; usamos R$ 0,15/kWh e testamos de R$ 0,095 a R$ 0,25.
  - Sistemas pequenos podem custar mais por watt. A R$ 6,50/Wp o retorno vai para ~6 anos.
  - Não reduz o pico de consumo às 18h–21h, porque não há geração à noite.
  - Quem não tem telhado pode pesquisar geração compartilhada ("energia por assinatura"), que não foi calculada aqui.

De onde vêm esses números:
  [R16] Estudo Estratégico Geração Distribuída 2025 (Greener): R$ 3,62/Wp (2 kWp), R$ 2,84/Wp (4 kWp)
  [R08] Consumidores passarão a arcar com 60% do Fio B a partir de 2026 (Lei 14.300/2022)
  [R17] Tarifação do Fio B (Lei 14.300) – exemplos por distribuidora
  [R11] Irradiação solar diária média mensal – São José dos Campos, plano horizontal e 23° (base CRESESB/SunData)
  [R12] Produtividade de sistemas FV conectados à rede e Performance Ratio (~80%)
  (Para ver os links, digite: fontes)
```

## P3 · Rosana, 45, diarista, casa própria, 5 pessoas, Bolsa Família, abordada por vendedor de placa solar

### "um vendedor falou q a placa solar zera minha conta é verdade?"

Intenção antes dos ajustes: `fotovoltaico` → depois: `conta_zero`

```
>> RESUMO: não zera. Diminui (na família de referência, de R$ 148,59 para R$ 40,80 por mês), mas sempre sobra uma parte para pagar.

NÃO. Placa solar diminui a conta, mas não zera. Mesmo com placas, você continua pagando:
  1. Uma taxa pelo uso dos fios da Enel sobre a energia que as placas mandam para a rede (o "Fio B"). Ela sobe de 60% em 2026 para 90% em 2028.
  2. A taxa de iluminação pública da prefeitura.
  3. Um valor mínimo da ligação, para quem não tem Tarifa Social.
  4. A energia do banho é à noite, quando as placas não geram: ela vem da rede e é descontada dos créditos.

Na família de referência, com 2 placas, a conta média cairia de R$ 148,59 para R$ 40,80 por mês (sem iluminação pública). É uma boa economia, mas não é zero.

Antes de fechar negócio: peça 3 orçamentos, desconfie de pressa ("promoção só hoje"), confira se a empresa faz a homologação na Enel e se o equipamento tem selo do INMETRO.

Atenção:
  - Valores para a família de referência. Com mais placas a conta cai mais, mas o investimento sobe.
  - O retorno estimado das 2 placas é de 4,1 anos.

De onde vêm esses números:
  [R08] Consumidores passarão a arcar com 60% do Fio B a partir de 2026 (Lei 14.300/2022)
  [R17] Tarifação do Fio B (Lei 14.300) – exemplos por distribuidora
  [R16] Estudo Estratégico Geração Distribuída 2025 (Greener): R$ 3,62/Wp (2 kWp), R$ 2,84/Wp (4 kWp)
  [R07] Resolução Normativa ANEEL nº 1.000/2021 – custo de disponibilidade (30/50/100 kWh)
  (Para ver os links, digite: fontes)
```

### "e o aquecedor solar?"

Intenção antes dos ajustes: `aquecedor_solar` → depois: `aquecedor_solar`

```
>> RESUMO: vale a pena para quem tem CASA PRÓPRIA com telhado: custa uns R$ 4.199,46 e se paga em cerca de 6 anos. Para aluguel ou apartamento, em geral não dá.

Aquecedor solar de água é uma fonte RENOVÁVEL: uma placa no telhado esquenta a água com o calor do sol e guarda num reservatório (boiler). O chuveiro elétrico fica só como apoio nos dias nublados.

Para a família de referência:
  - Investimento estimado: R$ 4.199,46 (kit de 200 litros + instalação + adaptações).
  - Economia estimada: R$ 724,23 por ano (já descontada a manutenção).
  - Se paga em cerca de 5,8 anos. Dura uns 15 anos.
  - Alivia a rede elétrica no fim da tarde (18h às 21h), quando todo mundo liga o chuveiro ao mesmo tempo.

Quando faz sentido: casa própria, telhado com sol (de preferência voltado para o norte) e lugar para o reservatório acima do chuveiro. Peça orçamento a instaladores com equipamento etiquetado pelo INMETRO.

Atenção:
  - A economia assume que o sol cobre 70% da energia do banho. Em teste com 50%, o retorno passa para ~8 anos.
  - Se a casa não tiver tubulação de água quente, a obra pode dobrar o custo e o retorno passa de 10 anos.
  - Não serve para quem mora de aluguel sem autorização do dono, nem para a maioria dos apartamentos.

De onde vêm esses números:
  [R13] Altoé, Oliveira Filho e Carlo (2012). Análise energética de sistemas solares térmicos... Ambiente Construído 12(3), 75-87
  [R14] SINAPI 103517 – Aquecedor solar compacto 200 L, fornecimento e instalação (ref. 09/2026)
  [R15] Quanto custa instalar aquecimento solar de água para 4 pessoas em 2026
  [R11] Irradiação solar diária média mensal – São José dos Campos, plano horizontal e 23° (base CRESESB/SunData)
  (Para ver os links, digite: fontes)
```

### "qual é melhor pra mim"

Intenção antes dos ajustes: `comparar` → depois: `comparar`

```
>> RESUMO: comece pelo banho de 5 minutos (custo zero). Se a casa for sua e tiver telhado, o próximo passo é o aquecedor solar.

Comparação para a mesma necessidade (água quente do banho) em 12 meses:

  - Banhos de 5 min (mudança de hábito): investe R$ 20,00, economiza R$ 502,05/ano, retorno imediato, evita 15 kg de CO2/ano.
  - Aquecedor solar de água + chuveiro de apoio (renovável): investe R$ 4.199,46, economiza R$ 724,23/ano, retorno 5,8 anos, evita 28 kg de CO2/ano.
  - Placas solares fotovoltaicas (renovável): investe R$ 4.950,00, economiza R$ 1.193,44/ano, retorno 4,1 anos, evita 54 kg de CO2/ano.
    (2 placas geram mais do que o banho gasta. Só para o banho, a economia seria de ~R$ 847,42/ano, com retorno de 4,3 anos.)
  - Aquecedor solar + banhos de 5 min (renovável): investe R$ 4.219,46, economiza R$ 835,65/ano, retorno 5,0 anos, evita 32 kg de CO2/ano.

O que eu recomendo, em ordem:
1. Comece JÁ pelos banhos mais curtos: custo zero e economia imediata.
2. Se a casa é sua e tem telhado com sol, o aquecedor solar é a opção renovável mais segura: não depende de regra de compensação e alivia a rede no horário de pico.
3. As placas fotovoltaicas também se pagam rápido (~4 anos, comparando só a energia do banho), mas exigem mais dinheiro na entrada, autorização da Enel e dependem de uma taxa (Fio B) que vai subir até 2028. Considere se tiver acesso a crédito barato ou a um programa social.

Atenção:
  - Os números são para a família de referência (4 pessoas, 8 min de banho, 220 kWh/mês, com Tarifa Social).
  - O ranking entre aquecedor solar e placas muda conforme o preço real e o custo de obra na sua casa.
  - Use o simulador para colocar os dados da SUA conta (digite: simular).

De onde vêm esses números:
  [R01] Resolução Homologatória ANEEL nº 3.596/2026 – tarifas Enel SP (B1 residencial: TUSD 472,42 + TE 316,96 R$/MWh; vigência 04/07/2026 a 03/07/2027)
  [R06] Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês (Luz do Povo)
  [R08] Consumidores passarão a arcar com 60% do Fio B a partir de 2026 (Lei 14.300/2022)
  [R13] Altoé, Oliveira Filho e Carlo (2012). Análise energética de sistemas solares térmicos... Ambiente Construído 12(3), 75-87
  [R14] SINAPI 103517 – Aquecedor solar compacto 200 L, fornecimento e instalação (ref. 09/2026)
  [R16] Estudo Estratégico Geração Distribuída 2025 (Greener): R$ 3,62/Wp (2 kWp), R$ 2,84/Wp (4 kWp)
  [R18] SIN registra 38,5 kg CO2/MWh em 2023, menor taxa desde 2012 (MCTI)
  (Para ver os links, digite: fontes)
```

### "tenho bolsa familia tenho desconto na luz?"

Intenção antes dos ajustes: `nao_entendi` → depois: `tarifa_social`

```
>> RESUMO: se sua família está no CadÚnico com renda de até meio salário mínimo por pessoa, os primeiros 80 kWh do mês são de graça. Quem recebe Bolsa Família geralmente se encaixa.

Tarifa Social de Energia (Luz do Povo): desde a Lei 15.235/2025, famílias inscritas no CadÚnico com renda de até meio salário mínimo por pessoa não pagam a energia dos primeiros 80 kWh do mês.

O que isso significa na prática:
  - Acima de 80 kWh, cada kWh é cobrado com preço cheio.
  - Como o chuveiro empurra a conta para bem acima de 80 kWh, cada minuto de banho economizado sai do seu bolso, mesmo para quem tem o benefício.

Bolsa Família: quem recebe já está no CadÚnico e costuma ter direito. Como pedir: mantenha o CadÚnico atualizado no CRAS da sua cidade e confira na conta da Enel se aparece "Tarifa Social" ou "Baixa Renda". Se não aparecer, procure a Enel com o NIS em mãos.

Atenção:
  - As regras podem mudar. Confirme as condições no site da ANEEL ou na Enel.
  - Famílias com renda entre meio e um salário mínimo por pessoa têm regras diferentes; confira com a Enel.

De onde vêm esses números:
  [R06] Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês (Luz do Povo)
  (Para ver os links, digite: fontes)
```

## P4 · Antônio, 67, aposentado, apartamento (CDHU), 2 pessoas

### "moro em apartamento"

Intenção antes dos ajustes: `nao_entendi` → depois: `moradia`

```
>> RESUMO: aquecedor solar e placas geralmente não dão; o banho de 5 minutos funciona em qualquer casa e economiza uns R$ 502,05 por ano.

Para quem mora de aluguel ou em apartamento, o aquecedor solar e as placas solares geralmente não são possíveis: precisam de telhado próprio e de obra. O que funciona para você:

  1. Banho de 5 minutos: economiza cerca de R$ 502,05 por ano e não precisa de obra nem de autorização.
  2. Use a posição "verão" (morno) do chuveiro nos dias quentes.
  3. Confira se você tem direito à Tarifa Social (pergunte "tenho direito à tarifa social?").
  4. Energia por assinatura (geração compartilhada): você paga uma empresa que tem uma usina solar e recebe desconto na conta, sem instalar nada. Confira se o desconto compensa e se não há multa para cancelar.

Se for aluguel de casa: dá para conversar com o dono sobre instalar um aquecedor solar, porque ele valoriza o imóvel. Em prédio, o condomínio pode instalar um sistema coletivo.

Atenção:
  - A energia por assinatura não foi calculada aqui: o desconto varia de empresa para empresa.

De onde vêm esses números:
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R06] Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês (Luz do Povo)
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  (Para ver os links, digite: fontes)
```

### "o que da pra fazer no apartamento"

Intenção antes dos ajustes: `nao_entendi` → depois: `moradia`

```
>> RESUMO: aquecedor solar e placas geralmente não dão; o banho de 5 minutos funciona em qualquer casa e economiza uns R$ 502,05 por ano.

Para quem mora de aluguel ou em apartamento, o aquecedor solar e as placas solares geralmente não são possíveis: precisam de telhado próprio e de obra. O que funciona para você:

  1. Banho de 5 minutos: economiza cerca de R$ 502,05 por ano e não precisa de obra nem de autorização.
  2. Use a posição "verão" (morno) do chuveiro nos dias quentes.
  3. Confira se você tem direito à Tarifa Social (pergunte "tenho direito à tarifa social?").
  4. Energia por assinatura (geração compartilhada): você paga uma empresa que tem uma usina solar e recebe desconto na conta, sem instalar nada. Confira se o desconto compensa e se não há multa para cancelar.

Se for aluguel de casa: dá para conversar com o dono sobre instalar um aquecedor solar, porque ele valoriza o imóvel. Em prédio, o condomínio pode instalar um sistema coletivo.

Atenção:
  - A energia por assinatura não foi calculada aqui: o desconto varia de empresa para empresa.

De onde vêm esses números:
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18%
  [R06] Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês (Luz do Povo)
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste
  (Para ver os links, digite: fontes)
```

### "a resistencia queimou posso trocar sozinho"

Intenção antes dos ajustes: `seguranca` → depois: `seguranca`

```
Segurança em primeiro lugar:
  - Troca de resistência, fiação ou disjuntor deve ser feita por eletricista.
  - Chuveiro precisa de fio de bitola correta e aterramento. Fio esquentando, cheiro de queimado ou choque são sinais de risco: desligue o disjuntor e chame um profissional.
  - Nunca troque o disjuntor por um maior para ele "parar de cair".

Atenção:
  - Este assistente não substitui avaliação de um eletricista.
```

## P5 · Larissa, 22, estudante, mora com os pais, familiar com tecnologia, desconfiada de números

### "esses numeros sao confiaveis?"

Intenção antes dos ajustes: `nao_entendi` → depois: `limitacoes`

```
>> RESUMO: são estimativas confiáveis para ter uma ideia, com fontes públicas, mas NÃO são garantia de economia.

O que você precisa saber sobre estes números:
  - São estimativas para uma família típica, não promessa. A economia real depende de você.
  - Usamos tarifas vigentes em novembro de 2026 (Enel SP). Elas mudam todo ano em julho.
  - Irradiação solar de uma cidade vizinha de mesma latitude, porque é próxima da Grande SP.
  - O desempenho do aquecedor solar (70%) vem de um estudo em Minas Gerais; testamos de 50% a 80%.
  - Preços de equipamento variam muito. Sempre peça pelo menos 3 orçamentos.
  - Não calculamos financiamento nem juros de empréstimo. O efeito de um aumento da tarifa você vê perguntando "e se a tarifa aumentar?".

De onde vêm esses números:
  [R01] Resolução Homologatória ANEEL nº 3.596/2026 – tarifas Enel SP (B1 residencial: TUSD 472,42 + TE 316,96 R$/MWh; vigência 04/07/2026 a 03/07/2027)
  [R11] Irradiação solar diária média mensal – São José dos Campos, plano horizontal e 23° (base CRESESB/SunData)
  [R13] Altoé, Oliveira Filho e Carlo (2012). Análise energética de sistemas solares térmicos... Ambiente Construído 12(3), 75-87
  [R14] SINAPI 103517 – Aquecedor solar compacto 200 L, fornecimento e instalação (ref. 09/2026)
  [R16] Estudo Estratégico Geração Distribuída 2025 (Greener): R$ 3,62/Wp (2 kWp), R$ 2,84/Wp (4 kWp)
  (Para ver os links, digite: fontes)
```

### "de onde vem os dados"

Intenção antes dos ajustes: `fontes` → depois: `fontes`

```
>> RESUMO: todos os números vêm de fontes públicas (ANEEL, leis, SINAPI, MCTI, estudos). Links abaixo.

Todas as fontes usadas nos cálculos:

  [R01] Resolução Homologatória ANEEL nº 3.596/2026 – tarifas Enel SP (B1 residencial: TUSD 472,42 + TE 316,96 R$/MWh; vigência 04/07/2026 a 03/07/2027) (ANEEL (documento publicado pela Enel)) — https://www.enel.com.br/content/dam/enel-br/megamenu/para-voc%C3%AA/REH%203596.2026%20Enel%20SP.pdf
  [R02] Bandeira tarifária permanece verde em novembro de 2026 (30/10/2026) (Agência iNFRA) — https://agenciainfra.com/blog/?p=49598
  [R03] Aneel aciona bandeira verde em outubro; amarela vigorou de maio a setembro de 2026 (R$ 1,885/100 kWh) (Jornal do Brasil) — https://www.jb.com.br/editorias/?p=382
  [R04] Simulação de tarifa Enel SP com ICMS e PIS/COFINS por dentro (Calculadora do Mundo) — https://www.calculadoradomundo.com.br/energia/tarifa-energia-por-distribuidora/enel-sp
  [R05] ICMS sobre energia em SP: isenção até 90 kWh (Decreto 50.473/2006; RICMS Anexo I art. 29) e faixas 12%/18% (SEFAZ-SP / Esfera Energia) — https://legislacao.fazenda.sp.gov.br/Paginas/an1art029.aspx
  [R06] Lei 15.235/2025 – Tarifa Social: gratuidade até 80 kWh/mês (Luz do Povo) (ANEEL / Cenário Energia) — https://cenarioenergia.com.br/2025/10/21/aneel-abre-consulta-publica-para-regulamentar-gratuidade-da-conta-de-energia-ate-80-kwh-mes-para-baixa-renda/
  [R07] Resolução Normativa ANEEL nº 1.000/2021 – custo de disponibilidade (30/50/100 kWh) (ANEEL) — https://www.gov.br/aneel
  [R08] Consumidores passarão a arcar com 60% do Fio B a partir de 2026 (Lei 14.300/2022) (Canal Solar) — https://canalsolar.com.br/consumidores-60-do-fio-b-2026/
  [R09] Pesquisa de Posse e Hábitos (PPH) Eletrobras/Procel – chuveiro ~24% do consumo residencial no Sudeste (ENCAC/ANTAC (cita PPH 2019)) — https://eventos.antac.org.br/index.php/encac/article/download/7083/5799/33783
  [R10] Impacto das mudanças climáticas no consumo de chuveiros elétricos (banho diário de 8 min) (ENCAC/ANTAC) — https://eventos.antac.org.br/index.php/encac/article/download/7083/5799/33783
  [R11] Irradiação solar diária média mensal – São José dos Campos, plano horizontal e 23° (base CRESESB/SunData) (USP – e-Disciplinas (PEA)) — https://edisciplinas.usp.br/mod/resource/view.php?id=4094582
  [R12] Produtividade de sistemas FV conectados à rede e Performance Ratio (~80%) (Congresso Brasileiro de Energia Solar) — https://anaiscbens.emnuvens.com.br/cbens/article/download/2063/2046/2047
  [R13] Altoé, Oliveira Filho e Carlo (2012). Análise energética de sistemas solares térmicos... Ambiente Construído 12(3), 75-87 (UFRGS – Ambiente Construído) — https://seer.ufrgs.br/index.php/ambienteconstruido/article/view/25706
  [R14] SINAPI 103517 – Aquecedor solar compacto 200 L, fornecimento e instalação (ref. 09/2026) (CAIXA/IBGE via Orcamentor) — https://orcamentor.com/composicao/103517/
  [R15] Quanto custa instalar aquecimento solar de água para 4 pessoas em 2026 (Monitor do Mercado) — https://monitordomercado.com.br/economia-2/422211-quanto-custa-instalar-aquecimento-solar-de-agua-para-4-pessoas-em-2026-o-boiler-e-apenas-uma-parte-do-projeto/
  [R16] Estudo Estratégico Geração Distribuída 2025 (Greener): R$ 3,62/Wp (2 kWp), R$ 2,84/Wp (4 kWp) (Greener via Olhar Digital) — https://olhardigital.com.br/curiosidades/?p=10663
  [R17] Tarifação do Fio B (Lei 14.300) – exemplos por distribuidora (Canal Solar) — https://canalsolar.com.br/tarifacao-do-fio-b-previsto-na-lei-14-300/
  [R18] SIN registra 38,5 kg CO2/MWh em 2023, menor taxa desde 2012 (MCTI) (MCTI via O Setor Elétrico) — https://www.osetoreletrico.com.br/?p=159478
  [R19] Fatores de emissão do SIN jan–abr/2025 (21,5 a 28,9 kg CO2/MWh) (MCTI via Canal Solar) — https://canalsolar.com.br/emissoes-de-co%e2%82%82-geracao-eletrica-mcti/
  [R20] Chuveiro elétrico: 49% da ponta residencial; uso concentrado das 18h às 19h (USP – Boletim Técnico PEA) — https://repositorio.usp.br/directbitstream/38e53bbb-af84-461c-875f-e775bb055343/BT-PEA-96_08_251016_082227.pdf
  [R21] Tarifa de energia elétrica – Enel São Paulo (tabela B1 residencial, REH 3.596/2026) (Enel Distribuição São Paulo) — https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-de-energia-eletrica.html
```

### "quanto co2 eu economizo"

Intenção antes dos ajustes: `ambiente` → depois: `ambiente`

```
A eletricidade brasileira é das mais limpas do mundo (muita hidrelétrica, solar e eólica), então o CO2 evitado por família é pequeno:

  - Banhos de 5 min: ~15 kg de CO2 por ano.
  - Aquecedor solar: ~28 kg por ano.
  - Placas fotovoltaicas: ~54 kg por ano.

O maior ganho ambiental é outro: o chuveiro é responsável por quase metade do pico de consumo das casas no fim da tarde. É nesse horário que o sistema mais aciona usinas térmicas, que poluem mais. O aquecedor solar e o banho mais curto reduzem esse pico; as placas fotovoltaicas não, porque não geram à noite.

Também há impactos na fabricação: placas e coletores usam vidro, alumínio e cobre, e precisam de descarte correto no fim da vida útil.

Atenção:
  - Usamos o fator médio do SIN (2023). Ele subestima o efeito de cortar consumo no pico.
  - Não fizemos análise de ciclo de vida completa dos equipamentos.

De onde vêm esses números:
  [R18] SIN registra 38,5 kg CO2/MWh em 2023, menor taxa desde 2012 (MCTI)
  [R19] Fatores de emissão do SIN jan–abr/2025 (21,5 a 28,9 kg CO2/MWh)
  [R20] Chuveiro elétrico: 49% da ponta residencial; uso concentrado das 18h às 19h
  (Para ver os links, digite: fontes)
```

### "e se a tarifa aumentar"

Intenção antes dos ajustes: `nao_entendi` → depois: `reajuste`

```
>> RESUMO: se a tarifa subir, todas as opções economizam mais e se pagam mais rápido.

A tarifa da Enel muda todo ano, em julho. Em 2026 o aumento médio foi de cerca de 10%. Quando a tarifa sobe, TODAS as opções passam a economizar mais, porque cada kWh evitado vale mais dinheiro.

Se a tarifa subir 10%:
  - Banhos de 5 min (mudança de hábito): economia passa de R$ 502,05 para R$ 552,25 por ano (retorno imediato).
  - Aquecedor solar de água + chuveiro de apoio: economia passa de R$ 724,23 para R$ 806,65 por ano (retorno 5,2 anos).
  - Placas solares fotovoltaicas: economia passa de R$ 1.193,44 para R$ 1.339,43 por ano (retorno 3,7 anos).

Nossas contas principais NÃO incluem aumento futuro de tarifa de propósito, para não prometer economia demais.

Atenção:
  - Ninguém sabe quanto será o próximo reajuste; 10% é só um exemplo, parecido com o de 2026.

De onde vêm esses números:
  [R01] Resolução Homologatória ANEEL nº 3.596/2026 – tarifas Enel SP (B1 residencial: TUSD 472,42 + TE 316,96 R$/MWh; vigência 04/07/2026 a 03/07/2027)
  (Para ver os links, digite: fontes)
```
