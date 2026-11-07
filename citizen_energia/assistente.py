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

    def formatada(self) -> str:
        partes = [self.texto.strip()]
        if self.limitacoes:
            partes.append("Atenção:\n" + "\n".join(f"  - {l}" for l in self.limitacoes))
        if self.fontes:
            refs = C.carregar_referencias()
            linhas = [f"  [{r}] {refs[r]['titulo']} — {refs[r]['url']}" for r in self.fontes if r in refs]
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
    ("limitacoes", ["limitac", "garant", "certeza", "confiavel", "pode errar"]),
    ("tarifa_social", ["tarifa social", "baixa renda", "cadunico", "cad unico", "luz do povo", "desconto na conta", "gratuidade"]),
    ("bandeira", ["bandeira"]),
    ("aquecedor_solar", ["aquecedor solar", "solar termic", "boiler", "agua quente solar", "aquecimento solar", "placa de agua"]),
    ("fotovoltaico", ["fotovolt", "painel solar", "paineis solares", "placa solar", "placas solares", "energia solar",
                      "gerar energia", "gerar minha energia", "fio b", "lei 14.300", "lei 14300"]),
    ("comparar", ["vale a pena", "qual escolher", "qual o melhor", "qual e melhor", "melhor opcao", "recomenda",
                  "o que eu faco", "o que fazer"]),
    ("ambiente", ["co2", "carbono", "emiss", "meio ambiente", "ambiental", "planeta", "sustentav", "poluic"]),
    ("seguranca", ["resistencia", "queimou", "choque", "fiacao", "disjuntor", "seguranca", "cheiro de queimado"]),
    ("habitos", ["dica", "economizar", "reduzir", "diminuir", "banho curto", "habito", "gastar menos", "pagar menos"]),
    ("chuveiro", ["chuveiro", "banho", "quanto gasta", "quanto custa", "consome", "consumo"]),
    ("ajuda", ["ajuda", "menu", "opcoes", "o que voce faz", "ola", "bom dia", "boa tarde", "boa noite"]),
]

# Pedidos explícitos de comparação vencem qualquer tecnologia citada na frase
# ("compare aquecedor solar e placa fotovoltaica" -> comparar).
GATILHOS_COMPARACAO = ["compar", " vs ", " versus ", "diferenca entre", "ou placa", "ou aquecedor"]


def detectar_intencao(mensagem: str) -> str:
    m = f" {normalizar(mensagem)} "
    if any(g in m for g in GATILHOS_COMPARACAO):
        return "comparar"
    if m.strip() in ("oi", "oi!", "ola", "e ai", "hello"):
        return "ajuda"
    for intencao, gatilhos in INTENCOES:
        # O gatilho precisa começar no início de uma palavra:
        # evita que "ola" case dentro de "solar" ou "dica" dentro de "indicar".
        if any(re.search(r"(?<![a-z])" + re.escape(g), m) for g in gatilhos):
            return intencao
    # "solar" sozinho é ambíguo: pode ser aquecedor ou fotovoltaico.
    if "solar" in m:
        return "solar_ambiguo"
    return "nao_entendi"


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
        f"  - Isso dá uns {num(s['energia_chuveiro_mes'])} kWh por mês, ou {num(s['participacao_chuveiro']*100)}% da conta.\n"
        f"  - Custo aproximado: {reais(s['custo_chuveiro_mes'])} por mês só com banho.\n"
        f"  - Cada minuto de banho (com o chuveiro ligado) custa cerca de {reais(s['custo_por_minuto_banho'])}.\n\n"
        f"Quer saber como diminuir esse gasto? Pergunte \"como economizar no banho\" ou \"vale a pena aquecedor solar\"."
    )
    return Resposta("chuveiro", texto, ["R01", "R05", "R09", "R10"],
                    ["O cálculo usa uma vazão de 4 litros/minuto e água fria a 20°C (média do ano). No inverno o chuveiro gasta mais; no verão, menos.",
                     "Confira a potência real na etiqueta do seu chuveiro."])


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
    return Resposta("habitos", texto, ["R05", "R09", "R10", "R20"],
                    ["A economia só acontece se o hábito mudar de verdade, todos os dias.",
                     "O efeito da faixa de ICMS só aparece se o consumo total ficar abaixo de 200 kWh no mês."])


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
        f"  - Tira cerca de {num(a['reducao_ponta_kw'], 1)} kW da rede no horário de pico, o que ajuda o sistema elétrico.\n\n"
        "Quando faz sentido: casa própria, telhado com sol (de preferência voltado para o norte) e lugar para o "
        "reservatório acima do chuveiro. Peça orçamento a instaladores com equipamento etiquetado pelo INMETRO."
    )
    return Resposta("aquecedor_solar", texto, ["R13", "R14", "R15", "R11"],
                    ["A economia assume que o sol cobre 70% da energia do banho. Em teste com 50%, o retorno passa para ~8 anos.",
                     "Se a casa não tiver tubulação de água quente, a obra pode dobrar o custo e o retorno passa de 10 anos.",
                     "Não serve para quem mora de aluguel sem autorização do dono, nem para a maioria dos apartamentos."])


def r_fotovoltaico(perfil):
    t = _tabela(perfil)
    f = t["fotovoltaico"]
    texto = (
        "Placas fotovoltaicas são RENOVÁVEIS: transformam luz do sol em eletricidade. A energia que sobra durante "
        "o dia vai para a rede e vira crédito na sua conta.\n\n"
        f"Para cobrir a energia do chuveiro da família de referência:\n"
        f"  - Sistema de {num(f['kwp'], 1)} kWp (2 placas), gerando uns {num(f['geracao_fv_ano'])} kWh por ano.\n"
        f"  - Investimento estimado: {reais(f['investimento'])}.\n"
        f"  - Economia estimada: {reais(f['economia_anual'])} por ano; se paga em cerca de {num(f['payback_anos'], 1)} anos.\n\n"
        "Pontos importantes:\n"
        "  - O banho é à noite e as placas geram de dia: você depende dos créditos na rede.\n"
        "  - Pela Lei 14.300, parte da tarifa (o \"Fio B\") não é compensada: 60% em 2026, 75% em 2027 e 90% em 2028.\n"
        "  - Precisa de projeto, instalador e homologação na Enel. Desconfie de promessa de \"conta zero\"."
    )
    return Resposta("fotovoltaico", texto, ["R16", "R08", "R17", "R11", "R12"],
                    ["O valor do Fio B da Enel SP não é publicado de forma simples; usamos R$ 0,15/kWh e testamos de R$ 0,095 a R$ 0,25.",
                     "Sistemas pequenos podem custar mais por watt. A R$ 6,50/Wp o retorno vai para ~6 anos.",
                     "Não reduz o pico de consumo às 18h–21h, porque não há geração à noite.",
                     "Quem não tem telhado pode pesquisar geração compartilhada (\"energia por assinatura\"), que não foi calculada aqui."])


def r_comparar(perfil):
    t = _tabela(perfil)
    linhas = []
    for chave in ["habitos", "aquecedor_solar", "fotovoltaico", "combinado"]:
        l = t[chave]
        pb = "imediato" if not l["payback_anos"] else f"{num(l['payback_anos'], 1)} anos"
        ren = " (renovável)" if l["renovavel"] else ""
        linhas.append(f"  - {l['alternativa']}{ren}: investe {reais(l['investimento'])}, "
                      f"economiza {reais(l['economia_anual'])}/ano, retorno {pb}, evita {num(l['co2_evitado_kg_ano'])} kg de CO2/ano.")
    texto = (
        "Comparação para a mesma necessidade (água quente do banho) em 12 meses:\n\n" + "\n".join(linhas) + "\n\n"
        "O que eu recomendo, em ordem:\n"
        "1. Comece JÁ pelos banhos mais curtos: custo zero e economia imediata.\n"
        "2. Se a casa é sua e tem telhado com sol, o aquecedor solar é a opção renovável mais segura: "
        "não depende de regra de compensação e alivia a rede no horário de pico.\n"
        "3. As placas fotovoltaicas dão o maior retorno financeiro no cálculo, mas exigem mais dinheiro na entrada, "
        "homologação e dependem de regras (Fio B) que vão ficar menos favoráveis até 2028. "
        "Considere se tiver acesso a crédito barato ou a um programa social."
    )
    return Resposta("comparar", texto, ["R01", "R06", "R08", "R13", "R14", "R16", "R18"],
                    ["Os números são para a família de referência (4 pessoas, 8 min de banho, 220 kWh/mês, com Tarifa Social).",
                     "O ranking entre aquecedor solar e placas muda conforme o preço real e o custo de obra na sua casa.",
                     "Use o simulador para colocar os dados da SUA conta."])


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
    return Resposta("tarifa_social", texto, ["R06"],
                    ["As regras podem mudar. Confirme as condições no site da ANEEL ou na Enel.",
                     "Famílias com renda entre meio e um salário mínimo por pessoa têm regras diferentes; confira com a Enel."])


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
    return Resposta("fontes", texto)


def r_limitacoes(perfil):
    texto = (
        "O que você precisa saber sobre estes números:\n"
        "  - São estimativas para uma família típica, não promessa. A economia real depende de você.\n"
        "  - Usamos tarifas vigentes em novembro de 2026 (Enel SP). Elas mudam todo ano em julho.\n"
        "  - Irradiação solar de uma cidade vizinha de mesma latitude, porque é próxima da Grande SP.\n"
        "  - O desempenho do aquecedor solar (70%) vem de um estudo em Minas Gerais; testamos de 50% a 80%.\n"
        "  - Preços de equipamento variam muito. Sempre peça pelo menos 3 orçamentos.\n"
        "  - Não calculamos financiamento, juros de empréstimo, nem aumento futuro da tarifa."
    )
    return Resposta("limitacoes", texto, ["R01", "R11", "R13", "R14", "R16"])


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
    r = r_ajuda(perfil)
    r.intencao = "nao_entendi"
    r.texto = "Não entendi bem. " + r.texto.split("Você pode perguntar", 1)[0].replace("Oi! ", "") + \
        "Você pode perguntar" + r.texto.split("Você pode perguntar", 1)[1]
    return r


RESPOSTAS = {
    "chuveiro": r_chuveiro, "habitos": r_habitos, "aquecedor_solar": r_aquecedor,
    "fotovoltaico": r_fotovoltaico, "comparar": r_comparar, "tarifa_social": r_tarifa_social,
    "bandeira": r_bandeira, "ambiente": r_ambiente, "seguranca": r_seguranca, "fontes": r_fontes,
    "limitacoes": r_limitacoes, "ajuda": r_ajuda, "solar_ambiguo": r_solar_ambiguo, "nao_entendi": r_nao_entendi,
}


def responder(mensagem: str, perfil: C.Perfil | None = None) -> Resposta:
    """Ponto de entrada: recebe a pergunta do cidadão e devolve a resposta estruturada."""
    perfil = perfil or C.Perfil()
    return RESPOSTAS[detectar_intencao(mensagem)](perfil)


def simulacao_personalizada(perfil: C.Perfil) -> Resposta:
    """Resposta para os dados que o próprio usuário informou."""
    perfil.validar()
    s = C.resumo_perfil(perfil)
    t = _tabela(perfil)
    linhas = []
    for chave in ["habitos", "aquecedor_solar", "fotovoltaico", "combinado"]:
        l = t[chave]
        pb = "imediato" if not l["payback_anos"] else (f"{num(l['payback_anos'], 1)} anos" if l["payback_anos"] else "não se paga")
        linhas.append(f"  - {l['alternativa']}: economia ~{reais(l['economia_anual'])}/ano | investimento {reais(l['investimento'])} | retorno {pb}")
    texto = (
        f"Sua casa: {perfil.pessoas} pessoas, banhos de {num(perfil.minutos_por_banho)} min, {num(perfil.consumo_total_mensal)} kWh/mês"
        f"{', com Tarifa Social' if perfil.tarifa_social else ''}.\n\n"
        f"  - Seu chuveiro deve gastar ~{num(s['energia_chuveiro_mes'])} kWh/mês ({num(s['participacao_chuveiro']*100)}% do consumo), "
        f"cerca de {reais(s['custo_chuveiro_mes'])} por mês.\n"
        f"  - Conta estimada hoje: {reais(s['conta_mes'])} por mês (sem iluminação pública).\n\n"
        "O que cada opção faria por você:\n" + "\n".join(linhas)
    )
    lim = ["Estes valores são ESTIMATIVAS feitas com os dados que você informou, não promessa de economia. "
           "O resultado real depende do seu chuveiro, dos hábitos, do clima e das regras vigentes."]
    if s["participacao_chuveiro"] > 0.6:
        lim.append("O chuveiro calculado ficou acima de 60% do seu consumo: confira os minutos e o consumo total informados.")
    return Resposta("simulacao", texto, ["R01", "R05", "R06", "R08", "R13", "R14", "R16"], lim)
