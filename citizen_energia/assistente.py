"""
Módulo de conversa da contribuição de Energia do Citizen Assist AI.

Ideia central: o assistente NÃO inventa números. Toda resposta é montada a
partir de `calculos.py`, e toda resposta traz (1) as fontes usadas e
(2) as limitações da estimativa. Assim a coerência entre análise e
orientação é garantida pelo próprio código.

A detecção de intenção é por palavras-chave (determinística e testável).
Se o Citizen Assist AI do grupo usar um LLM, veja `integracao.py`.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from . import calculos as C

AVISO_GERAL = ("Estes valores são ESTIMATIVAS para uma família típica, não promessa de economia. "
               "Sua conta real depende do seu chuveiro, dos seus hábitos, do clima e das regras vigentes.")


@dataclass
class Resposta:
    intencao: str
    texto: str
    fontes: list[str] = field(default_factory=list)
    limitacoes: list[str] = field(default_factory=list)
    resumo: str = ""  # resposta direta em 1 frase, mostrada primeiro (ajuste A1 dos testes)

    def formatada(self, com_links: bool = False) -> str:
        partes = []
        if self.resumo:
            partes.append(f">> RESUMO: {self.resumo}")
        partes.append(self.texto.strip())
        if self.limitacoes:
            partes.append("Atenção:\n" + "\n".join(f"  - {l}" for l in self.limitacoes))
        if self.fontes:
            refs = C.carregar_referencias()
            # Títulos curtos por padrão; os links completos ficam em "fontes" (ajuste A6).
            if com_links:
                linhas = [f"  [{r}] {refs[r]['titulo']} — {refs[r]['url']}" for r in self.fontes if r in refs]
            else:
                linhas = [f"  [{r}] {refs[r]['titulo']}" for r in self.fontes if r in refs]
                linhas.append("  (Para ver os links, digite: fontes)")
            partes.append("De onde vêm esses números:\n" + "\n".join(linhas))
        return "\n\n".join(partes)


# --------------------------------------------------------------------------
# Utilidades de formatação (linguagem acessível)
# --------------------------------------------------------------------------
def reais(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(v: float, casas: int = 0) -> str:
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def normalizar(texto: str) -> str:
    """Minúsculas e sem acento: 'Aquecedor Solar' == 'aquecedor solar'."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


# --------------------------------------------------------------------------
# Intenções (ordem importa: a mais específica vem primeiro)
# --------------------------------------------------------------------------
INTENCOES: list[tuple[str, list[str]]] = [
    ("fontes", ["fonte", "referencia", "de onde vem", "de onde voce tirou"]),
    ("limitacoes", ["limitac", "garant", "certeza", "confia", "pode errar", "e verdade esses"]),
    # Ajuste A3: promessa de vendedor ("zera a conta") precisa de resposta direta.
    ("conta_zero", ["zera", "zerar", "conta zero", "conta zerada", "nao pagar nada", "vendedor"]),
    # Ajuste A4: quem mora de aluguel ou em apartamento não tem as mesmas opções.
    ("moradia", ["aluguel", "alugad", "apartamento", "apto", "predio", "condominio", "cdhu", "inquilin", "nao e minha"]),
    ("tarifa_social", ["tarifa social", "baixa renda", "cadunico", "cad unico", "luz do povo", "desconto na conta",
                       "desconto na luz", "gratuidade", "bolsa familia", "beneficio", "nis", "programa social"]),
    # Ajuste A5: "e se a tarifa aumentar?" caía em "não entendi".
    ("reajuste", ["reajuste", "tarifa aument", "conta aument", "luz aument", "aumento da", "aumentar a tarifa",
                  "se a tarifa", "ficar mais cara", "subir a conta", "subir a tarifa"]),
    ("bandeira", ["bandeira"]),
    ("aquecedor_solar", ["aquecedor solar", "solar termic", "boiler", "agua quente solar", "aquecimento solar", "placa de agua"]),
    ("fotovoltaico", ["fotovolt", "painel solar", "paineis solares", "placa solar", "placas solares", "energia solar",
                      "gerar energia", "gerar minha energia", "fio b", "lei 14.300", "lei 14300"]),
    ("comparar", ["vale a pena", "qual escolher", "qual o melhor", "qual e melhor", "qual e o melhor", "melhor opcao",
                  "melhor pra mim", "melhor para mim", "recomenda", "o que eu faco", "o que fazer"]),
    ("ambiente", ["co2", "carbono", "emiss", "meio ambiente", "ambiental", "planeta", "sustentav", "poluic"]),
    ("seguranca", ["resistencia", "queimou", "choque", "fiacao", "disjuntor", "seguranca", "cheiro de queimado"]),
    # Ajuste A2: "minha conta vem muito cara" caía em "não entendi".
    ("habitos", ["dica", "economizar", "reduzir", "diminuir", "banho curto", "habito", "gastar menos", "pagar menos",
                 "conta vem", "conta veio", "conta ta", "conta esta", "conta alta", "conta cara", "conta muito",
                 "conta pesada", "nao consigo pagar"]),
    ("chuveiro", ["chuveiro", "banho", "quanto gasta", "quanto custa", "consome", "consumo"]),
    ("ajuda", ["ajuda", "menu", "opcoes", "o que voce faz", "ola", "bom dia", "boa tarde", "boa noite"]),
]

# Ajuste A7: glossário. Só dispara quando a pessoa pergunta o SIGNIFICADO de um termo.
GLOSSARIO = {
    "kwh": ("kWh (quilowatt-hora)", "é a unidade de energia que aparece na sua conta de luz. 1 kWh é a energia de "
            "um aparelho de 1.000 watts ligado por 1 hora. Seu chuveiro gasta mais ou menos 1 kWh a cada 11 minutos."),
    "kwp": ("kWp (quilowatt-pico)", "é o \"tamanho\" de um sistema de placas solares: quanto ele gera com sol forte. "
            "Um sistema de 1 kWp gera uns 100 kWh por mês na Grande SP."),
    "kw": ("kW (quilowatt)", "é a força com que um aparelho puxa energia na hora em que está ligado. O chuveiro puxa "
           "uns 5 kW; uma geladeira, menos de 0,2 kW."),
    "fio b": ("Fio B", "é a parte da conta que paga os fios e postes da Enel. Quem tem placas solares continua "
              "pagando um pedaço dele sobre a energia que \"guarda\" na rede: 60% em 2026, 75% em 2027 e 90% em 2028."),
    "homolog": ("Homologação", "é a autorização da Enel para ligar placas solares na rede. O instalador faz o pedido; "
                "sem ela, a energia gerada não vira desconto na conta."),
    "payback": ("Retorno (payback)", "é o tempo que a economia na conta leva para devolver o dinheiro que você gastou."),
    "retorno": ("Retorno", "é o tempo que a economia na conta leva para devolver o dinheiro que você gastou."),
    "icms": ("ICMS", "é um imposto estadual que vem dentro da conta de luz. Em SP é 12% se você gasta até 200 kWh no mês "
             "e 18% acima disso, sobre a conta inteira."),
    "credito": ("Crédito de energia", "é a energia que suas placas solares mandam para a rede durante o dia. "
                "Ela volta como desconto quando você usa energia à noite."),
    "fracao solar": ("Fração solar", "é a parte do aquecimento da água que o sol consegue fazer. 70% quer dizer que "
                     "o sol faz 70% do trabalho e o chuveiro elétrico faz o resto."),
}
PERGUNTA_SIGNIFICADO = ["o que e", "o que significa", "que e isso", "que significa", "nao entendi o", "nao sei o que e",
                        "explica o", "explica a", "o que quer dizer", "oq e", "oque e"]


# Pedidos explícitos de comparação vencem qualquer tecnologia citada na frase
# ("compare aquecedor solar e placa fotovoltaica" -> comparar).
GATILHOS_COMPARACAO = ["compar", " vs ", " versus ", "diferenca entre", "ou placa", "ou aquecedor"]


def detectar_intencao(mensagem: str) -> str:
    m = f" {normalizar(mensagem)} "
    if any(g in m for g in GATILHOS_COMPARACAO):
        return "comparar"
    if m.strip() in ("oi", "oi!", "ola", "e ai", "hello"):
        return "ajuda"
    if any(p in m for p in PERGUNTA_SIGNIFICADO) and _termos_glossario(m):
        return "glossario"
    for intencao, gatilhos in INTENCOES:
        # O gatilho precisa começar no início de uma palavra:
        # evita que "ola" case dentro de "solar" ou "dica" dentro de "indicar".
        if any(re.search(r"(?<![a-z])" + re.escape(g), m) for g in gatilhos):
            return intencao
    # "solar" sozinho é ambíguo: pode ser aquecedor ou fotovoltaico.
    if "solar" in m:
        return "solar_ambiguo"
    return "nao_entendi"


def _termos_glossario(m: str) -> list[str]:
    """Termos do glossário presentes na mensagem ("kw" não conta se "kwh"/"kwp" já apareceram)."""
    achados = [t for t in GLOSSARIO if re.search(r"(?<![a-z])" + re.escape(t) + r"(?![a-z])", m)
               or (t in ("homolog",) and t in m)]
    if "kw" in achados and ("kwh" in achados or "kwp" in achados):
        achados.remove("kw")
    if "retorno" in achados and "payback" in achados:
        achados.remove("retorno")
    return achados


# --------------------------------------------------------------------------
# Respostas
# --------------------------------------------------------------------------
def _tabela(perfil):
    return {l["chave"]: l for l in C.comparar(perfil)}


def r_chuveiro(perfil):
    s = C.resumo_perfil(perfil)
    texto = (
        f"O chuveiro elétrico costuma ser o aparelho que mais gasta numa casa como a sua.\n\n"
        f"Para {perfil.pessoas} pessoas tomando banho de {num(perfil.minutos_por_banho)} minutos por dia:\n"
        f"  - O chuveiro puxa cerca de {num(s['potencia_kw'], 1)} kW enquanto está ligado "
        f"(para esquentar a água de {num(perfil.temperatura_agua_fria)}°C até {num(perfil.temperatura_banho)}°C).\n"
        f"  - Isso dá uns {num(s['energia_chuveiro_mes'])} kWh por mês (kWh é a unidade que aparece na sua conta de luz), "
        f"ou {num(s['participacao_chuveiro']*100)}% do que a casa gasta.\n"
        f"  - Custo aproximado: {reais(s['custo_chuveiro_mes'])} por mês só com banho.\n"
        f"  - Cada minuto de banho (com o chuveiro ligado) custa cerca de {reais(s['custo_por_minuto_banho'])}.\n\n"
        f"Quer saber como diminuir esse gasto? Pergunte \"como economizar no banho\" ou \"vale a pena aquecedor solar\"."
    )
    resumo = (f"o banho custa cerca de {reais(s['custo_chuveiro_mes'])} por mês "
              f"({reais(s['custo_por_minuto_banho'])} por minuto de chuveiro ligado).")
    return Resposta("chuveiro", texto, ["R01", "R05", "R09", "R10"],
                    ["O cálculo usa uma vazão de 4 litros/minuto e água fria a 20°C (média do ano). No inverno o chuveiro gasta mais; no verão, menos.",
                     "Confira a potência real na etiqueta do seu chuveiro."], resumo)


def r_habitos(perfil):
    t = _tabela(perfil)
    h = t["habitos"]
    s = C.resumo_perfil(perfil)
    texto = (
        "Dá para economizar sem gastar nada. As ações que mais pesam, em ordem:\n\n"
        f"1. Banho de 5 minutos (hoje: {num(perfil.minutos_por_banho)} min). Na família de referência isso economiza "
        f"cerca de {num(h['kwh_evitados_ano'])} kWh e {reais(h['economia_anual'])} por ano.\n"
        "   Dica: desligue o chuveiro enquanto se ensaboa. Um timer de cozinha ajuda as crianças.\n"
        "2. Use a posição \"verão\" (morno) nos dias quentes: ela usa uma resistência menor.\n"
        "3. Evite banho entre 18h e 21h quando possível: é o horário em que a rede está mais carregada.\n"
        "4. Nunca mexa na resistência ou na fiação do chuveiro sozinho: chame um eletricista.\n\n"
        f"Por que a economia é tão boa? Em São Paulo, quando a conta passa de 200 kWh o ICMS sobe de 12% para 18% "
        f"sobre a conta INTEIRA. Hoje seu kWh custa cerca de {reais(s['preco_kwh_final'])} com impostos. "
        "Cair para menos de 200 kWh faz o imposto de todos os kWh baixar."
    )
    resumo = (f"o chuveiro é cerca de {num(s['participacao_chuveiro']*100)}% da conta; banho de 5 minutos economiza "
              f"uns {reais(h['economia_anual'])} por ano, sem gastar nada.")
    return Resposta("habitos", texto, ["R05", "R09", "R10", "R20"],
                    ["A economia só acontece se o hábito mudar de verdade, todos os dias.",
                     "O efeito da faixa de ICMS só aparece se o consumo total ficar abaixo de 200 kWh no mês."], resumo)


def r_aquecedor(perfil):
    t = _tabela(perfil)
    a = t["aquecedor_solar"]
    texto = (
        "Aquecedor solar de água é uma fonte RENOVÁVEL: uma placa no telhado esquenta a água com o calor do sol "
        "e guarda num reservatório (boiler). O chuveiro elétrico fica só como apoio nos dias nublados.\n\n"
        f"Para a família de referência:\n"
        f"  - Investimento estimado: {reais(a['investimento'])} (kit de 200 litros + instalação + adaptações).\n"
        f"  - Economia estimada: {reais(a['economia_anual'])} por ano (já descontada a manutenção).\n"
        f"  - Se paga em cerca de {num(a['payback_anos'], 1)} anos. Dura uns 15 anos.\n"
        f"  - Alivia a rede elétrica no fim da tarde (18h às 21h), quando todo mundo liga o chuveiro ao mesmo tempo.\n\n"
        "Quando faz sentido: casa própria, telhado com sol (de preferência voltado para o norte) e lugar para o "
        "reservatório acima do chuveiro. Peça orçamento a instaladores com equipamento etiquetado pelo INMETRO."
    )
    resumo = (f"vale a pena para quem tem CASA PRÓPRIA com telhado: custa uns {reais(a['investimento'])} e se paga "
              f"em cerca de {num(a['payback_anos'], 0)} anos. Para aluguel ou apartamento, em geral não dá.")
    return Resposta("aquecedor_solar", texto, ["R13", "R14", "R15", "R11"],
                    ["A economia assume que o sol cobre 70% da energia do banho. Em teste com 50%, o retorno passa para ~8 anos.",
                     "Se a casa não tiver tubulação de água quente, a obra pode dobrar o custo e o retorno passa de 10 anos.",
                     "Não serve para quem mora de aluguel sem autorização do dono, nem para a maioria dos apartamentos."], resumo)


def r_fotovoltaico(perfil):
    t = _tabela(perfil)
    f = t["fotovoltaico"]
    texto = (
        "Placas fotovoltaicas são RENOVÁVEIS: transformam luz do sol em eletricidade. A energia que sobra durante "
        "o dia vai para a rede e vira crédito na sua conta.\n\n"
        f"Para cobrir a energia do chuveiro da família de referência:\n"
        f"  - 2 placas ({num(f['kwp'], 1)} kWp), gerando uns {num(f['geracao_fv_ano'] / 12)} kWh por mês.\n"
        f"  - Investimento estimado: {reais(f['investimento'])}.\n"
        f"  - Economia estimada: {reais(f['economia_anual'])} por ano; se paga em cerca de {num(f['payback_anos'], 1)} anos.\n\n"
        "Pontos importantes:\n"
        "  - O banho é à noite e as placas geram de dia: você depende dos créditos na rede.\n"
        "  - Você continua pagando uma parte da conta: a lei cobra uma taxa pelo uso dos fios da Enel (o \"Fio B\"), "
        "que vai subir até 2028.\n"
        "  - Precisa de projeto, instalador e autorização da Enel (homologação). A conta NÃO zera: pergunte \"placa solar zera a conta?\"."
    )
    resumo = (f"custa uns {reais(f['investimento'])} e se paga em cerca de {num(f['payback_anos'], 0)} anos, mas exige "
              "casa própria, autorização da Enel e a conta não zera.")
    return Resposta("fotovoltaico", texto, ["R16", "R08", "R17", "R11", "R12"],
                    ["O valor do Fio B da Enel SP não é publicado de forma simples; usamos R$ 0,15/kWh e testamos de R$ 0,095 a R$ 0,25.",
                     "Sistemas pequenos podem custar mais por watt. A R$ 6,50/Wp o retorno vai para ~6 anos.",
                     "Não reduz o pico de consumo às 18h–21h, porque não há geração à noite.",
                     "Quem não tem telhado pode pesquisar geração compartilhada (\"energia por assinatura\"), que não foi calculada aqui."], resumo)


def r_comparar(perfil):
    t = _tabela(perfil)
    linhas = []
    for chave in ["habitos", "aquecedor_solar", "fotovoltaico", "combinado"]:
        l = t[chave]
        pb = "imediato" if not l["payback_anos"] else f"{num(l['payback_anos'], 1)} anos"
        ren = " (renovável)" if l["renovavel"] else ""
        linhas.append(f"  - {l['alternativa']}{ren}: investe {reais(l['investimento'])}, "
                      f"economiza {reais(l['economia_anual'])}/ano, retorno {pb}, evita {num(l['co2_evitado_kg_ano'])} kg de CO2/ano.")
        if chave == "fotovoltaico":
            fvn = C.fv_normalizado(perfil)
            linhas.append(f"    (2 placas geram mais do que o banho gasta. Só para o banho, a economia seria de "
                          f"~{reais(fvn['economia_anual'])}/ano, com retorno de {num(fvn['payback_anos'], 1)} anos.)")
    texto = (
        "Comparação para a mesma necessidade (água quente do banho) em 12 meses:\n\n" + "\n".join(linhas) + "\n\n"
        "O que eu recomendo, em ordem:\n"
        "1. Comece JÁ pelos banhos mais curtos: custo zero e economia imediata.\n"
        "2. Se a casa é sua e tem telhado com sol, o aquecedor solar é a opção renovável mais segura: "
        "não depende de regra de compensação e alivia a rede no horário de pico.\n"
        f"3. As placas fotovoltaicas também se pagam rápido (~{num(C.fv_normalizado(perfil)['payback_anos'], 0)} anos, "
        "comparando só a energia do banho), mas exigem mais dinheiro na entrada, "
        "autorização da Enel e dependem de uma taxa (Fio B) que vai subir até 2028. "
        "Considere se tiver acesso a crédito barato ou a um programa social."
    )
    resumo = ("comece pelo banho de 5 minutos (custo zero). Se a casa for sua e tiver telhado, o próximo passo "
              "é o aquecedor solar.")
    return Resposta("comparar", texto, ["R01", "R06", "R08", "R13", "R14", "R16", "R18"],
                    ["Os números são para a família de referência (4 pessoas, 8 min de banho, 220 kWh/mês, com Tarifa Social).",
                     "O ranking entre aquecedor solar e placas muda conforme o preço real e o custo de obra na sua casa.",
                     "Use o simulador para colocar os dados da SUA conta (digite: simular)."], resumo)


def r_tarifa_social(perfil):
    texto = (
        "Tarifa Social de Energia (Luz do Povo): desde a Lei 15.235/2025, famílias inscritas no CadÚnico com renda "
        "de até meio salário mínimo por pessoa não pagam a energia dos primeiros 80 kWh do mês.\n\n"
        "O que isso significa na prática:\n"
        "  - Acima de 80 kWh, cada kWh é cobrado com preço cheio.\n"
        "  - Como o chuveiro empurra a conta para bem acima de 80 kWh, cada minuto de banho economizado "
        "sai do seu bolso, mesmo para quem tem o benefício.\n\n"
        "Como pedir: mantenha o CadÚnico atualizado no CRAS da sua cidade e confira na conta da Enel se aparece "
        "\"Tarifa Social\" ou \"Baixa Renda\". Se não aparecer, procure a Enel com o NIS em mãos."
    )
    resumo = ("se sua família está no CadÚnico com renda de até meio salário mínimo por pessoa, os primeiros 80 kWh "
              "do mês são de graça. Quem recebe Bolsa Família geralmente se encaixa.")
    texto = texto.replace("Como pedir:", "Bolsa Família: quem recebe já está no CadÚnico e costuma ter direito. Como pedir:")
    return Resposta("tarifa_social", texto, ["R06"],
                    ["As regras podem mudar. Confirme as condições no site da ANEEL ou na Enel.",
                     "Famílias com renda entre meio e um salário mínimo por pessoa têm regras diferentes; confira com a Enel."], resumo)


def r_bandeira(perfil):
    s = C.resumo_perfil(perfil)
    extra = s["energia_chuveiro_mes"] * C.P["bandeira_amarela_adicional"] / (1 - s["icms"] - C.P["pis_cofins_efetivo"])
    texto = (
        "A bandeira tarifária mostra se gerar energia está mais caro (por exemplo, quando falta chuva e o país usa "
        "usinas térmicas). Em novembro de 2026 a bandeira é verde: sem cobrança extra.\n\n"
        f"Na bandeira amarela, só o chuveiro da família de referência custaria uns {reais(extra)} a mais por mês. "
        "Em bandeira amarela ou vermelha, vale ainda mais encurtar o banho."
    )
    return Resposta("bandeira", texto, ["R02", "R03"],
                    ["A cor muda todo mês; a ANEEL anuncia no fim do mês anterior."])


def r_ambiente(perfil):
    t = _tabela(perfil)
    texto = (
        "A eletricidade brasileira é das mais limpas do mundo (muita hidrelétrica, solar e eólica), então o CO2 "
        "evitado por família é pequeno:\n\n"
        f"  - Banhos de 5 min: ~{num(t['habitos']['co2_evitado_kg_ano'])} kg de CO2 por ano.\n"
        f"  - Aquecedor solar: ~{num(t['aquecedor_solar']['co2_evitado_kg_ano'])} kg por ano.\n"
        f"  - Placas fotovoltaicas: ~{num(t['fotovoltaico']['co2_evitado_kg_ano'])} kg por ano.\n\n"
        "O maior ganho ambiental é outro: o chuveiro é responsável por quase metade do pico de consumo das casas "
        "no fim da tarde. É nesse horário que o sistema mais aciona usinas térmicas, que poluem mais. "
        "O aquecedor solar e o banho mais curto reduzem esse pico; as placas fotovoltaicas não, porque não geram à noite.\n\n"
        "Também há impactos na fabricação: placas e coletores usam vidro, alumínio e cobre, e precisam de descarte "
        "correto no fim da vida útil."
    )
    return Resposta("ambiente", texto, ["R18", "R19", "R20"],
                    ["Usamos o fator médio do SIN (2023). Ele subestima o efeito de cortar consumo no pico.",
                     "Não fizemos análise de ciclo de vida completa dos equipamentos."])


def r_seguranca(perfil):
    texto = (
        "Segurança em primeiro lugar:\n"
        "  - Troca de resistência, fiação ou disjuntor deve ser feita por eletricista.\n"
        "  - Chuveiro precisa de fio de bitola correta e aterramento. Fio esquentando, cheiro de queimado ou "
        "choque são sinais de risco: desligue o disjuntor e chame um profissional.\n"
        "  - Nunca troque o disjuntor por um maior para ele \"parar de cair\"."
    )
    return Resposta("seguranca", texto, [], ["Este assistente não substitui avaliação de um eletricista."])


def r_fontes(perfil):
    refs = C.carregar_referencias()
    texto = "Todas as fontes usadas nos cálculos:\n\n" + "\n".join(
        f"  [{k}] {v['titulo']} ({v['orgao']}) — {v['url']}" for k, v in refs.items())
    return Resposta("fontes", texto, resumo="todos os números vêm de fontes públicas (ANEEL, leis, SINAPI, MCTI, estudos). Links abaixo.")


def r_limitacoes(perfil):
    texto = (
        "O que você precisa saber sobre estes números:\n"
        "  - São estimativas para uma família típica, não promessa. A economia real depende de você.\n"
        "  - Usamos tarifas vigentes em novembro de 2026 (Enel SP). Elas mudam todo ano em julho.\n"
        "  - Irradiação solar de uma cidade vizinha de mesma latitude, porque é próxima da Grande SP.\n"
        "  - O desempenho do aquecedor solar (70%) vem de um estudo em Minas Gerais; testamos de 50% a 80%.\n"
        "  - Preços de equipamento variam muito. Sempre peça pelo menos 3 orçamentos.\n"
        "  - Não calculamos financiamento nem juros de empréstimo. O efeito de um aumento da tarifa você vê "
        "perguntando \"e se a tarifa aumentar?\"."
    )
    return Resposta("limitacoes", texto, ["R01", "R11", "R13", "R14", "R16"], [],
                    "são estimativas confiáveis para ter uma ideia, com fontes públicas, mas NÃO são garantia de economia.")


def r_conta_zero(perfil):
    t = _tabela(perfil)
    fv = C.simular("fotovoltaico", perfil)
    base = C.simular("atual", perfil)
    conta_antes = base.custo_contas_anual / 12
    conta_depois = fv.custo_contas_anual / 12
    texto = (
        "NÃO. Placa solar diminui a conta, mas não zera. Mesmo com placas, você continua pagando:\n"
        "  1. Uma taxa pelo uso dos fios da Enel sobre a energia que as placas mandam para a rede (o \"Fio B\"). "
        "Ela sobe de 60% em 2026 para 90% em 2028.\n"
        "  2. A taxa de iluminação pública da prefeitura.\n"
        "  3. Um valor mínimo da ligação, para quem não tem Tarifa Social.\n"
        "  4. A energia do banho é à noite, quando as placas não geram: ela vem da rede e é descontada dos créditos.\n\n"
        f"Na família de referência, com 2 placas, a conta média cairia de {reais(conta_antes)} para "
        f"{reais(conta_depois)} por mês (sem iluminação pública). É uma boa economia, mas não é zero.\n\n"
        "Antes de fechar negócio: peça 3 orçamentos, desconfie de pressa (\"promoção só hoje\"), confira se a empresa "
        "faz a homologação na Enel e se o equipamento tem selo do INMETRO."
    )
    resumo = (f"não zera. Diminui (na família de referência, de {reais(conta_antes)} para {reais(conta_depois)} por mês), "
              "mas sempre sobra uma parte para pagar.")
    return Resposta("conta_zero", texto, ["R08", "R17", "R16", "R07"],
                    ["Valores para a família de referência. Com mais placas a conta cai mais, mas o investimento sobe.",
                     f"O retorno estimado das 2 placas é de {num(t['fotovoltaico']['payback_anos'], 1)} anos."], resumo)


def r_moradia(perfil):
    t = _tabela(perfil)
    h = t["habitos"]
    texto = (
        "Para quem mora de aluguel ou em apartamento, o aquecedor solar e as placas solares geralmente não são "
        "possíveis: precisam de telhado próprio e de obra. O que funciona para você:\n\n"
        f"  1. Banho de 5 minutos: economiza cerca de {reais(h['economia_anual'])} por ano e não precisa de obra nem "
        "de autorização.\n"
        "  2. Use a posição \"verão\" (morno) do chuveiro nos dias quentes.\n"
        "  3. Confira se você tem direito à Tarifa Social (pergunte \"tenho direito à tarifa social?\").\n"
        "  4. Energia por assinatura (geração compartilhada): você paga uma empresa que tem uma usina solar e recebe "
        "desconto na conta, sem instalar nada. Confira se o desconto compensa e se não há multa para cancelar.\n\n"
        "Se for aluguel de casa: dá para conversar com o dono sobre instalar um aquecedor solar, porque ele valoriza "
        "o imóvel. Em prédio, o condomínio pode instalar um sistema coletivo."
    )
    resumo = (f"aquecedor solar e placas geralmente não dão; o banho de 5 minutos funciona em qualquer casa e "
              f"economiza uns {reais(h['economia_anual'])} por ano.")
    return Resposta("moradia", texto, ["R05", "R06", "R09"],
                    ["A energia por assinatura não foi calculada aqui: o desconto varia de empresa para empresa."], resumo)


def r_reajuste(perfil):
    base = _tabela(perfil)
    aumento = 0.10
    extra = C.P["tarifa_b1_sem_impostos"] * aumento
    alta = {l["chave"]: l for l in C.comparar(perfil, bandeira_adicional=extra)}
    linhas = []
    for chave in ["habitos", "aquecedor_solar", "fotovoltaico"]:
        b, a = base[chave], alta[chave]
        pb = "imediato" if not a["payback_anos"] else f"{num(a['payback_anos'], 1)} anos"
        linhas.append(f"  - {b['alternativa']}: economia passa de {reais(b['economia_anual'])} para "
                      f"{reais(a['economia_anual'])} por ano (retorno {pb}).")
    texto = (
        "A tarifa da Enel muda todo ano, em julho. Em 2026 o aumento médio foi de cerca de 10%. Quando a tarifa sobe, "
        "TODAS as opções passam a economizar mais, porque cada kWh evitado vale mais dinheiro.\n\n"
        "Se a tarifa subir 10%:\n" + "\n".join(linhas) + "\n\n"
        "Nossas contas principais NÃO incluem aumento futuro de tarifa de propósito, para não prometer economia demais."
    )
    resumo = "se a tarifa subir, todas as opções economizam mais e se pagam mais rápido."
    return Resposta("reajuste", texto, ["R01"],
                    ["Ninguém sabe quanto será o próximo reajuste; 10% é só um exemplo, parecido com o de 2026."], resumo)


def r_glossario(perfil, mensagem: str = ""):
    termos = _termos_glossario(f" {normalizar(mensagem)} ") or list(GLOSSARIO)
    linhas = [f"  - {GLOSSARIO[t][0]}: {GLOSSARIO[t][1]}" for t in termos]
    texto = "\n".join(linhas)
    resumo = GLOSSARIO[termos[0]][0] + " " + GLOSSARIO[termos[0]][1].split(". ")[0] + "." if len(termos) == 1 else \
        "veja abaixo o que cada palavra quer dizer."
    return Resposta("glossario", texto, [], [], resumo)


def r_ajuda(perfil):
    texto = (
        "Oi! Eu sou o módulo de Energia do Citizen Assist AI. Ajudo você a gastar menos com o chuveiro elétrico. "
        "Você pode perguntar, por exemplo:\n"
        "  - Quanto meu chuveiro gasta?\n"
        "  - Como economizar no banho?\n"
        "  - Vale a pena aquecedor solar?\n"
        "  - E placa solar fotovoltaica?\n"
        "  - Compare as opções\n"
        "  - Tenho direito à tarifa social?\n"
        "  - Moro de aluguel, o que dá pra fazer?\n"
        "  - Placa solar zera a conta?\n"
        "  - O que é kWh?\n"
        "  - Qual o impacto no meio ambiente?\n"
        "  - De onde vêm esses números?\n"
        "Ou digite \"simular\" para calcular com os dados da sua casa."
    )
    return Resposta("ajuda", texto)


def r_solar_ambiguo(perfil):
    texto = (
        "Existem dois tipos de \"solar\" para casa:\n"
        "  1. Aquecedor solar: esquenta a ÁGUA do banho direto com o sol.\n"
        "  2. Placa fotovoltaica: gera ELETRICIDADE.\n"
        "Sobre qual você quer saber? Pode perguntar \"aquecedor solar\" ou \"placa fotovoltaica\", ou \"compare as opções\"."
    )
    return Resposta("solar_ambiguo", texto)


def r_nao_entendi(perfil):
    texto = (
        "Desculpe, não entendi. Tente com outras palavras, por exemplo:\n"
        "  - \"quanto meu chuveiro gasta?\"\n"
        "  - \"como pagar menos?\"\n"
        "  - \"moro de aluguel, o que fazer?\"\n"
        "  - \"vale a pena aquecedor solar?\"\n"
        "Ou digite \"simular\" para eu calcular com os dados da sua casa, ou \"ajuda\" para ver tudo o que sei responder."
    )
    return Resposta("nao_entendi", texto)


RESPOSTAS = {
    "chuveiro": r_chuveiro, "habitos": r_habitos, "aquecedor_solar": r_aquecedor,
    "fotovoltaico": r_fotovoltaico, "comparar": r_comparar, "tarifa_social": r_tarifa_social,
    "bandeira": r_bandeira, "ambiente": r_ambiente, "seguranca": r_seguranca, "fontes": r_fontes,
    "limitacoes": r_limitacoes, "ajuda": r_ajuda, "solar_ambiguo": r_solar_ambiguo, "nao_entendi": r_nao_entendi,
    "conta_zero": r_conta_zero, "moradia": r_moradia, "reajuste": r_reajuste,
}


def responder(mensagem: str, perfil: C.Perfil | None = None) -> Resposta:
    """Ponto de entrada: recebe a pergunta do cidadão e devolve a resposta estruturada."""
    perfil = perfil or C.Perfil()
    intencao = detectar_intencao(mensagem)
    if intencao == "glossario":
        return r_glossario(perfil, mensagem)
    return RESPOSTAS[intencao](perfil)


def simulacao_personalizada(perfil: C.Perfil, casa_propria: bool = True) -> Resposta:
    """Resposta para os dados que o próprio usuário informou."""
    perfil.validar()
    s = C.resumo_perfil(perfil)
    t = _tabela(perfil)
    linhas = []
    for chave in ["habitos", "aquecedor_solar", "fotovoltaico", "combinado"]:
        l = t[chave]
        pb = "imediato" if not l["payback_anos"] else (f"{num(l['payback_anos'], 1)} anos" if l["payback_anos"] else "não se paga")
        if not casa_propria and chave != "habitos":
            # Ajuste A4: não oferecer como se fosse viável o que precisa de telhado próprio.
            linhas.append(f"  - {l['alternativa']}: geralmente NÃO é possível em aluguel/apartamento "
                          f"(precisa de telhado próprio e obra).")
            continue
        linhas.append(f"  - {l['alternativa']}: economia ~{reais(l['economia_anual'])}/ano | investimento {reais(l['investimento'])} | retorno {pb}")
    texto = (
        f"Sua casa: {perfil.pessoas} pessoas, banhos de {num(perfil.minutos_por_banho)} min, {num(perfil.consumo_total_mensal)} kWh/mês"
        f"{', com Tarifa Social' if perfil.tarifa_social else ''}.\n\n"
        f"  - Seu chuveiro deve gastar ~{num(s['energia_chuveiro_mes'])} kWh/mês ({num(s['participacao_chuveiro']*100)}% do consumo), "
        f"cerca de {reais(s['custo_chuveiro_mes'])} por mês.\n"
        f"  - Conta estimada hoje: {reais(s['conta_mes'])} por mês (sem iluminação pública).\n\n"
        "O que cada opção faria por você:\n" + "\n".join(linhas)
    )
    h = t["habitos"]
    resumo = (f"seu banho custa uns {reais(s['custo_chuveiro_mes'])} por mês; com banhos de 5 minutos você "
              f"economizaria cerca de {reais(h['economia_anual'])} por ano."
              if perfil.minutos_por_banho > 5 else
              f"seu banho custa uns {reais(s['custo_chuveiro_mes'])} por mês e você já toma banhos curtos. Parabéns!")
    lim = ["Estes valores são ESTIMATIVAS feitas com os dados que você informou, não promessa de economia. "
           "O resultado real depende do seu chuveiro, dos hábitos, do clima e das regras vigentes."]
    if s["participacao_chuveiro"] > 0.6:
        lim.append("O chuveiro calculado ficou acima de 60% do seu consumo: confira os minutos e o consumo total informados.")
    return Resposta("simulacao", texto, ["R01", "R05", "R06", "R08", "R13", "R14", "R16"], lim, resumo)
