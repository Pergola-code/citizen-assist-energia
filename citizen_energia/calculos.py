"""
Motor de cálculo da contribuição de Energia do Citizen Assist AI.

Necessidade analisada: aquecer a água do banho de uma família de baixa renda
na área da Enel SP (Grande São Paulo) durante 12 meses.

Alternativas comparadas para ESSA MESMA necessidade e ESSE MESMO período:
    atual           -> chuveiro elétrico como está hoje (linha de base)
    habitos         -> mesmo chuveiro, banhos mais curtos (eficiência, custo ~0)
    aquecedor_solar -> aquecedor solar térmico (RENOVÁVEL) com chuveiro de apoio
    fotovoltaico    -> placas fotovoltaicas (RENOVÁVEL) dimensionadas para
                       compensar a energia do chuveiro
    combinado       -> hábitos + aquecedor solar

Princípio do código: nenhum número "mágico" fica escondido aqui. Tudo vem de
dados/parametros.json, onde cada valor tem unidade, tipo e fonte.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, replace
from pathlib import Path

PASTA_DADOS = Path(__file__).parent / "dados"
DIAS_NO_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


# --------------------------------------------------------------------------
# Leitura dos dados
# --------------------------------------------------------------------------
def carregar_parametros_brutos() -> dict:
    """Lê o JSON completo (com notas e fontes) — usado pelo relatório."""
    with open(PASTA_DADOS / "parametros.json", encoding="utf-8") as f:
        return json.load(f)


def carregar_referencias() -> dict:
    with open(PASTA_DADOS / "referencias.json", encoding="utf-8") as f:
        return json.load(f)


def carregar_parametros() -> dict:
    """Achata o JSON em {nome: valor} para facilitar o uso nos cálculos."""
    bruto = carregar_parametros_brutos()
    planos = {}
    for grupo, itens in bruto.items():
        if grupo.startswith("_") or not isinstance(itens, dict):
            continue
        for nome, item in itens.items():
            planos[nome] = item["valor"]
    return planos


P = carregar_parametros()


# --------------------------------------------------------------------------
# Perfil da família (entrada do simulador)
# --------------------------------------------------------------------------
@dataclass
class Perfil:
    pessoas: int = P["pessoas"]
    banhos_por_pessoa_dia: float = P["banhos_por_pessoa_dia"]
    minutos_por_banho: float = P["minutos_por_banho"]
    vazao_l_min: float = P["vazao_chuveiro"]
    temperatura_banho: float = P["temperatura_banho"]
    temperatura_agua_fria: float = P["temperatura_agua_fria"]
    eficiencia_chuveiro: float = P["eficiencia_chuveiro"]
    consumo_total_mensal: float = P["consumo_total_mensal"]
    tarifa_social: bool = P["beneficiaria_tarifa_social"]

    def validar(self) -> None:
        if self.pessoas <= 0 or self.minutos_por_banho <= 0:
            raise ValueError("Pessoas e minutos de banho precisam ser maiores que zero.")
        if self.temperatura_banho <= self.temperatura_agua_fria:
            raise ValueError("A temperatura do banho precisa ser maior que a da água fria.")
        if not 0 < self.eficiencia_chuveiro <= 1:
            raise ValueError("Eficiência deve estar entre 0 e 1.")


# --------------------------------------------------------------------------
# Física do chuveiro: P = m_ponto · c · ΔT / η
# --------------------------------------------------------------------------
def potencia_chuveiro_kw(perfil: Perfil) -> float:
    """
    Potência elétrica necessária para aquecer a água na vazão do banho.

    Por quê: o chuveiro é um aquecedor "de passagem". Toda a água que passa
    precisa ganhar ΔT graus naquele instante, então a potência é
    (massa por segundo) x (calor específico) x (ΔT), dividida pela eficiência.
    """
    massa_por_segundo = perfil.vazao_l_min * P["densidade_agua"] / 60  # kg/s
    delta_t = perfil.temperatura_banho - perfil.temperatura_agua_fria   # °C
    potencia_w = massa_por_segundo * P["calor_especifico_agua"] * delta_t / perfil.eficiencia_chuveiro
    return potencia_w / 1000


def horas_banho_por_dia(perfil: Perfil) -> float:
    return perfil.pessoas * perfil.banhos_por_pessoa_dia * perfil.minutos_por_banho / 60


def energia_chuveiro_mes_kwh(perfil: Perfil, dias: int) -> float:
    """Energia = Potência x Tempo (kW x h = kWh)."""
    return potencia_chuveiro_kw(perfil) * horas_banho_por_dia(perfil) * dias


def energia_termica_dia_kwh(perfil: Perfil) -> float:
    """Calor útil que a água do banho recebe por dia (sem perdas)."""
    litros = perfil.pessoas * perfil.banhos_por_pessoa_dia * perfil.minutos_por_banho * perfil.vazao_l_min
    delta_t = perfil.temperatura_banho - perfil.temperatura_agua_fria
    return litros * P["densidade_agua"] * P["calor_especifico_agua"] * delta_t / 3.6e6


# --------------------------------------------------------------------------
# Conta de luz
# --------------------------------------------------------------------------
def aliquota_icms(consumo_kwh: float) -> float:
    """Faixa de ICMS residencial em SP. A alíquota vale para a conta inteira."""
    for limite, aliquota in P["icms_faixas_sp"]:
        if consumo_kwh <= limite:
            return aliquota
    return P["icms_faixas_sp"][-1][1]


def conta_mensal(consumo_kwh: float, tarifa_social: bool, credito_disponivel_kwh: float = 0.0,
                 bandeira_adicional: float = 0.0, fio_b: float | None = None,
                 pct_fio_b: float | None = None) -> dict:
    """
    Estima a conta de um mês (sem contribuição de iluminação pública).

    - Tarifa Social: os primeiros 80 kWh não são cobrados; o resto é cobrado inteiro.
    - Créditos de geração solar (FV) abatem kWh, mas em 2026 60% do Fio B
      continua sendo cobrado sobre o kWh compensado (Lei 14.300).
    - ICMS e PIS/COFINS são "por dentro": total = valor / (1 - impostos).

    Simplificação documentada: a faixa de ICMS é aplicada sobre o consumo medido.
    """
    fio_b = P["fv_fio_b_enel_sp"] if fio_b is None else fio_b
    pct_fio_b = P["fv_percentual_fio_b_2026"] if pct_fio_b is None else pct_fio_b
    tarifa = P["tarifa_b1_sem_impostos"] + bandeira_adicional

    gratuitos = min(P["tarifa_social_kwh_gratuitos"], consumo_kwh) if tarifa_social else 0.0
    faturavel = consumo_kwh - gratuitos
    minimo = 0.0 if tarifa_social else P["custo_disponibilidade_monofasico"]

    compensado = max(0.0, min(credito_disponivel_kwh, faturavel - minimo))
    faturavel_rede = max(faturavel - compensado, minimo)

    valor_sem_impostos = faturavel_rede * tarifa + compensado * pct_fio_b * fio_b
    icms = aliquota_icms(consumo_kwh)
    impostos = icms + P["pis_cofins_efetivo"]
    total = valor_sem_impostos / (1 - impostos)

    return {
        "consumo_kwh": consumo_kwh,
        "kwh_gratuitos": gratuitos,
        "kwh_compensados": compensado,
        "icms": icms,
        "valor_sem_impostos": valor_sem_impostos,
        "total": total,
    }


def tarifa_final_por_kwh(consumo_kwh: float) -> float:
    """Preço de 1 kWh com impostos na faixa de consumo informada."""
    return P["tarifa_b1_sem_impostos"] / (1 - aliquota_icms(consumo_kwh) - P["pis_cofins_efetivo"])


# --------------------------------------------------------------------------
# Alternativas
# --------------------------------------------------------------------------
@dataclass
class ResultadoAlternativa:
    chave: str
    nome: str
    renovavel: bool
    investimento: float
    manutencao_anual: float
    vida_util: int
    energia_chuveiro_rede_kwh: list = field(default_factory=list)  # 12 meses
    geracao_fv_kwh: list = field(default_factory=list)
    contas: list = field(default_factory=list)
    detalhes: dict = field(default_factory=dict)

    @property
    def energia_anual_rede(self) -> float:
        return sum(self.energia_chuveiro_rede_kwh)

    @property
    def custo_contas_anual(self) -> float:
        return sum(c["total"] for c in self.contas)


def _irradiacao_media() -> float:
    return sum(P["irradiacao_mensal_plano_23graus"]) / 12


def dimensionar_fv_kwp(energia_anual_kwh: float, exato: bool = False) -> float:
    """
    kWp necessários = energia anual / (irradiação média x 365 x PR).
    Arredondamos para cima em número inteiro de módulos (não existe meio módulo).
    """
    producao_por_kwp = _irradiacao_media() * 365 * P["performance_ratio_fv"]
    kwp_teorico = energia_anual_kwh / producao_por_kwp
    if exato:
        # Comparação normalizada: sistema hipotético do tamanho EXATO do banho (sem arredondar módulos).
        return kwp_teorico
    modulos = max(1, math.ceil(kwp_teorico / P["fv_potencia_modulo"]))
    return round(modulos * P["fv_potencia_modulo"], 3)


def simular(chave: str, perfil: Perfil | None = None, *, minutos_habito: float = 5,
            fracao_solar: float | None = None, custo_aquecedor_mult: float = 1.0,
            fio_b: float | None = None, bandeira_adicional: float = 0.0,
            custo_wp: float | None = None, pct_fio_b: float | None = None,
            fv_exato: bool = False) -> ResultadoAlternativa:
    """Simula 12 meses de uma alternativa. Os argumentos extras servem à sensibilidade."""
    perfil = perfil or Perfil()
    perfil.validar()
    f_solar = P["fracao_solar_aquecedor"] if fracao_solar is None else fracao_solar
    custo_wp = P["fv_custo_por_wp_pequeno"] if custo_wp is None else custo_wp

    # "Outros usos" da casa ficam constantes em todas as alternativas.
    chuveiro_mes_tipico = energia_chuveiro_mes_kwh(perfil, 30)
    outros_usos = max(0.0, perfil.consumo_total_mensal - chuveiro_mes_tipico)

    usa_habito = chave in ("habitos", "combinado")
    usa_aquecedor = chave in ("aquecedor_solar", "combinado")
    usa_fv = chave == "fotovoltaico"
    perfil_banho = replace(perfil, minutos_por_banho=min(minutos_habito, perfil.minutos_por_banho)) if usa_habito else perfil

    nomes = {
        "atual": ("Chuveiro elétrico (situação atual)", False),
        "habitos": (f"Banhos de {minutos_habito:g} min (mudança de hábito)", False),
        "aquecedor_solar": ("Aquecedor solar de água + chuveiro de apoio", True),
        "fotovoltaico": ("Placas solares fotovoltaicas", True),
        "combinado": (f"Aquecedor solar + banhos de {minutos_habito:g} min", True),
    }
    if chave not in nomes:
        raise ValueError(f"Alternativa desconhecida: {chave}")

    investimento, manutencao, vida = 0.0, 0.0, 10
    detalhes = {}
    if usa_habito:
        investimento += P["habitos_custo_timer"]
    if usa_aquecedor:
        kit = P["aquecedor_solar_kit_instalado"] * custo_aquecedor_mult
        investimento += kit * (1 + P["aquecedor_solar_adaptacoes"])
        manutencao += P["aquecedor_solar_manutencao_anual"]
        vida = P["aquecedor_solar_vida_util"]
        detalhes["fracao_solar_media"] = f_solar
    kwp = 0.0
    if usa_fv:
        energia_alvo = sum(energia_chuveiro_mes_kwh(perfil, d) for d in DIAS_NO_MES)
        kwp = dimensionar_fv_kwp(energia_alvo, exato=fv_exato)
        investimento += kwp * 1000 * custo_wp
        manutencao += P["fv_manutencao_anual"]
        vida = P["fv_vida_util"]
        detalhes["kwp"] = kwp

    h_med = _irradiacao_media()
    energia_rede, geracao, contas = [], [], []
    banco_creditos = 0.0
    for i, dias in enumerate(DIAS_NO_MES):
        e_chuveiro = energia_chuveiro_mes_kwh(perfil_banho, dias)
        h_mes = P["irradiacao_mensal_plano_23graus"][i]
        if usa_aquecedor:
            # Fração solar varia com a irradiação do mês (menos sol -> menos água aquecida).
            f_mes = min(0.95, f_solar * h_mes / h_med)
            e_chuveiro *= (1 - f_mes)
        gen = kwp * h_mes * dias * P["performance_ratio_fv"] if usa_fv else 0.0

        consumo_mes = outros_usos * dias / 30 + e_chuveiro
        banco_creditos += gen
        conta = conta_mensal(consumo_mes, perfil.tarifa_social, banco_creditos,
                             bandeira_adicional=bandeira_adicional, fio_b=fio_b, pct_fio_b=pct_fio_b)
        banco_creditos -= conta["kwh_compensados"]

        energia_rede.append(e_chuveiro)
        geracao.append(gen)
        contas.append(conta)

    detalhes["creditos_sobrando_kwh"] = banco_creditos
    nome, renovavel = nomes[chave]
    return ResultadoAlternativa(chave, nome, renovavel, investimento, manutencao, vida,
                                energia_rede, geracao, contas, detalhes)


# --------------------------------------------------------------------------
# Indicadores de comparação
# --------------------------------------------------------------------------
def vpl(fluxo_anual: float, investimento: float, anos: int, taxa: float) -> float:
    """Valor Presente Líquido: quanto o investimento 'vale hoje' somando economias futuras descontadas."""
    return -investimento + sum(fluxo_anual / (1 + taxa) ** t for t in range(1, anos + 1))


def fv_normalizado(perfil: Perfil | None = None) -> dict:
    """
    Fotovoltaico dimensionado para gerar EXATAMENTE a energia do banho (100%, não 137%).
    Responde à pergunta justa: "para a mesma necessidade, quanto o FV economiza?".
    Sistema hipotético (não existe fração de módulo), usado só para comparar.
    """
    perfil = perfil or Perfil()
    base = simular("atual", perfil)
    r = simular("fotovoltaico", perfil, fv_exato=True)
    economia = base.custo_contas_anual - r.custo_contas_anual - r.manutencao_anual
    return {
        "kwp": r.detalhes["kwp"],
        "geracao_ano": sum(r.geracao_fv_kwh),
        "investimento": r.investimento,
        "economia_anual": economia,
        "payback_anos": r.investimento / economia if economia > 0 else math.inf,
        "fracao_do_banho": sum(r.geracao_fv_kwh) / base.energia_anual_rede,
    }


def comparar(perfil: Perfil | None = None, **kwargs) -> list[dict]:
    """Roda todas as alternativas e devolve indicadores lado a lado (mesma família, mesmos 12 meses)."""
    perfil = perfil or Perfil()
    base = simular("atual", perfil, **kwargs)
    linhas = []
    for chave in ["atual", "habitos", "aquecedor_solar", "fotovoltaico", "combinado"]:
        r = base if chave == "atual" else simular(chave, perfil, **kwargs)
        economia_conta = base.custo_contas_anual - r.custo_contas_anual
        economia_liquida = economia_conta - r.manutencao_anual

        # Energia "evitada da rede": para FV conta a energia compensada pela geração.
        kwh_evitados = (base.energia_anual_rede - r.energia_anual_rede) + sum(r.geracao_fv_kwh) \
            - max(0.0, r.detalhes.get("creditos_sobrando_kwh", 0.0))
        co2_kg = kwh_evitados / 1000 * P["fator_emissao_sin"] * 1000

        if r.investimento <= 0 or economia_liquida <= 0:
            payback = 0.0 if (r.investimento <= 0 and economia_liquida >= 0) else math.inf
        else:
            payback = r.investimento / economia_liquida
        horizonte = min(10, r.vida_util)

        # Potência que deixa de ser puxada da rede no horário de ponta.
        p_base = potencia_chuveiro_kw(perfil)
        if chave in ("aquecedor_solar", "combinado"):
            reducao_ponta = p_base * P["fracao_solar_aquecedor"]
        else:
            reducao_ponta = 0.0  # hábito encurta o tempo, não a potência; FV não gera à noite

        linhas.append({
            "chave": chave,
            "alternativa": r.nome,
            "renovavel": r.renovavel,
            "kwh_chuveiro_rede_ano": round(r.energia_anual_rede, 1),
            "geracao_fv_ano": round(sum(r.geracao_fv_kwh), 1),
            "kwh_evitados_ano": round(kwh_evitados, 1),
            "conta_anual": round(r.custo_contas_anual, 2),
            "economia_anual": round(economia_liquida, 2),
            "investimento": round(r.investimento, 2),
            # Normaliza pelo tamanho: quanto se investe para evitar 1 kWh por ano.
            "invest_por_kwh_ano": round(r.investimento / kwh_evitados, 2) if kwh_evitados > 0 else None,
            "payback_anos": round(payback, 1) if math.isfinite(payback) else None,
            "vpl_10a": round(vpl(economia_liquida, r.investimento, horizonte, P["taxa_desconto_anual"]), 2),
            "co2_evitado_kg_ano": round(co2_kg, 1),
            "reducao_ponta_kw": round(reducao_ponta, 2),
            "kwp": r.detalhes.get("kwp"),
        })
    return linhas


def _perfil_com_banho(perfil: Perfil, minutos: float) -> Perfil:
    """Muda a duração do banho mantendo os 'outros usos' da casa iguais."""
    outros = perfil.consumo_total_mensal - energia_chuveiro_mes_kwh(perfil, 30)
    novo = replace(perfil, minutos_por_banho=minutos)
    return replace(novo, consumo_total_mensal=outros + energia_chuveiro_mes_kwh(novo, 30))


def sensibilidade(perfil: Perfil | None = None) -> list[dict]:
    """
    Testa como os resultados mudam quando as premissas incertas mudam.
    Isso é o que impede tratar estimativa como 'resultado garantido'.
    """
    perfil = perfil or Perfil()
    cenarios = [
        ("Cenário base", {}, perfil),
        ("Fração solar baixa (50%)", {"fracao_solar": 0.50}, perfil),
        ("Fração solar alta (80%)", {"fracao_solar": 0.80}, perfil),
        ("Aquecedor 2x mais caro (casa precisa de obra)", {"custo_aquecedor_mult": 2.0}, perfil),
        ("Fio B baixo (R$ 0,095/kWh)", {"fio_b": 0.095}, perfil),
        ("Fio B alto (R$ 0,25/kWh)", {"fio_b": 0.25}, perfil),
        ("FV mais barato (R$ 3,62/Wp)", {"custo_wp": 3.62}, perfil),
        ("FV pequeno mais caro (R$ 6,50/Wp)", {"custo_wp": 6.50}, perfil),
        ("Fio B não compensado a 90% (regra de 2028)", {"pct_fio_b": 0.90}, perfil),
        ("Bandeira amarela o ano todo", {"bandeira_adicional": P["bandeira_amarela_adicional"]}, perfil),
        ("Família SEM Tarifa Social", {}, replace(perfil, tarifa_social=False)),
        ("Banhos de 12 min (família gasta mais)", {}, _perfil_com_banho(perfil, 12)),
    ]
    saida = []
    for nome, kwargs, pf in cenarios:
        tabela = {l["chave"]: l for l in comparar(pf, **kwargs)}
        saida.append({
            "cenario": nome,
            "habitos_economia": tabela["habitos"]["economia_anual"],
            "solar_economia": tabela["aquecedor_solar"]["economia_anual"],
            "solar_payback": tabela["aquecedor_solar"]["payback_anos"],
            "fv_economia": tabela["fotovoltaico"]["economia_anual"],
            "fv_payback": tabela["fotovoltaico"]["payback_anos"],
            "combinado_economia": tabela["combinado"]["economia_anual"],
            "combinado_payback": tabela["combinado"]["payback_anos"],
        })
    return saida


def estimar_consumo_total(pessoas: int, minutos_por_banho: float) -> float:
    """
    Estima o consumo mensal da casa quando a pessoa não sabe o valor da conta:
    "outros usos" da família de referência (escalados pelo nº de pessoas, com metade fixa
    — geladeira não dobra com o dobro de gente) + chuveiro calculado para esta família.
    """
    ref = Perfil()
    outros_ref = ref.consumo_total_mensal - energia_chuveiro_mes_kwh(ref, 30)
    outros = outros_ref * (0.5 + 0.5 * pessoas / ref.pessoas)
    chuveiro = energia_chuveiro_mes_kwh(replace(ref, pessoas=pessoas, minutos_por_banho=minutos_por_banho), 30)
    return outros + chuveiro


def resumo_perfil(perfil: Perfil | None = None) -> dict:
    """Números-chave da situação atual, usados pelo assistente."""
    perfil = perfil or Perfil()
    pot = potencia_chuveiro_kw(perfil)
    e_mes = energia_chuveiro_mes_kwh(perfil, 30)
    consumo = perfil.consumo_total_mensal
    conta = conta_mensal(consumo, perfil.tarifa_social)
    preco_kwh = tarifa_final_por_kwh(consumo)
    return {
        "potencia_kw": pot,
        "energia_chuveiro_mes": e_mes,
        "participacao_chuveiro": e_mes / consumo if consumo else 0,
        "custo_chuveiro_mes": e_mes * preco_kwh,
        "custo_por_minuto_banho": pot / 60 * preco_kwh,
        "conta_mes": conta["total"],
        "preco_kwh_final": preco_kwh,
        "icms": conta["icms"],
        "energia_termica_dia": energia_termica_dia_kwh(perfil),
    }
