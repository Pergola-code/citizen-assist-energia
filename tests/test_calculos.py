"""Testes do motor de cálculo: física, conta de luz e coerência das alternativas."""

import math

import pytest

from citizen_energia import calculos as C


def test_potencia_chuveiro_bate_com_formula_fisica():
    p = C.Perfil(vazao_l_min=4, temperatura_banho=38, temperatura_agua_fria=20, eficiencia_chuveiro=1.0)
    # 4 L/min = 0,0667 kg/s; 0,0667 * 4186 * 18 = 5023 W
    assert C.potencia_chuveiro_kw(p) == pytest.approx(5.023, rel=1e-3)


def test_potencia_dentro_da_faixa_comercial():
    assert 4.5 <= C.potencia_chuveiro_kw(C.Perfil()) <= 7.5


def test_energia_proporcional_ao_tempo():
    e8 = C.energia_chuveiro_mes_kwh(C.Perfil(minutos_por_banho=8), 30)
    e4 = C.energia_chuveiro_mes_kwh(C.Perfil(minutos_por_banho=4), 30)
    assert e4 == pytest.approx(e8 / 2)


@pytest.mark.parametrize("consumo,aliquota", [(50, 0.0), (90, 0.0), (91, 0.12), (200, 0.12), (201, 0.18)])
def test_faixas_icms_sp(consumo, aliquota):
    assert C.aliquota_icms(consumo) == aliquota


def test_tarifa_social_zera_ate_80_kwh():
    assert C.conta_mensal(75, tarifa_social=True)["total"] == 0
    conta = C.conta_mensal(120, tarifa_social=True)
    esperado = 40 * C.P["tarifa_b1_sem_impostos"] / (1 - 0.12 - C.P["pis_cofins_efetivo"])
    assert conta["total"] == pytest.approx(esperado)


def test_conta_sem_beneficio_cobra_minimo_de_disponibilidade():
    conta = C.conta_mensal(10, tarifa_social=False)
    assert conta["total"] == pytest.approx(30 * C.P["tarifa_b1_sem_impostos"] / (1 - C.P["pis_cofins_efetivo"]))


def test_credito_fv_paga_fio_b():
    sem = C.conta_mensal(220, tarifa_social=False)
    com = C.conta_mensal(220, tarifa_social=False, credito_disponivel_kwh=100)
    assert com["kwh_compensados"] == 100
    # O crédito reduz a conta, mas não por inteiro: 60% do Fio B continua cobrado.
    reducao_bruta = (sem["valor_sem_impostos"] - com["valor_sem_impostos"])
    assert reducao_bruta == pytest.approx(100 * (C.P["tarifa_b1_sem_impostos"] - 0.6 * C.P["fv_fio_b_enel_sp"]))


def test_todas_alternativas_economizam_e_mesmo_periodo():
    tabela = {l["chave"]: l for l in C.comparar()}
    for chave in ["habitos", "aquecedor_solar", "fotovoltaico", "combinado"]:
        assert tabela[chave]["economia_anual"] > 0
    assert len(C.simular("aquecedor_solar").contas) == 12


def test_combinado_economiza_mais_que_cada_parte():
    t = {l["chave"]: l for l in C.comparar()}
    assert t["combinado"]["kwh_evitados_ano"] > t["habitos"]["kwh_evitados_ano"]
    assert t["combinado"]["kwh_evitados_ano"] > t["aquecedor_solar"]["kwh_evitados_ano"]


def test_ha_pelo_menos_uma_alternativa_renovavel():
    assert any(l["renovavel"] for l in C.comparar())


def test_fracao_solar_mensal_nunca_passa_de_95_porcento():
    base = C.simular("atual")
    solar = C.simular("aquecedor_solar", fracao_solar=0.95)
    for e_base, e_sol in zip(base.energia_chuveiro_rede_kwh, solar.energia_chuveiro_rede_kwh):
        assert e_sol >= 0.05 * e_base - 1e-9


def test_dimensionamento_fv_em_modulos_inteiros():
    kwp = C.dimensionar_fv_kwp(1000)
    assert math.isclose(kwp / C.P["fv_potencia_modulo"], round(kwp / C.P["fv_potencia_modulo"]))


def test_sensibilidade_fracao_baixa_piora_retorno():
    s = {x["cenario"]: x for x in C.sensibilidade()}
    assert s["Fração solar baixa (50%)"]["solar_payback"] > s["Cenário base"]["solar_payback"]
    assert s["Fio B não compensado a 90% (regra de 2028)"]["fv_payback"] > s["Cenário base"]["fv_payback"]


def test_perfil_invalido_gera_erro():
    with pytest.raises(ValueError):
        C.simular("atual", C.Perfil(temperatura_banho=15, temperatura_agua_fria=20))


def test_todo_parametro_tem_tipo_e_unidade():
    bruto = C.carregar_parametros_brutos()
    refs = C.carregar_referencias()
    for grupo, itens in bruto.items():
        if grupo.startswith("_") or not isinstance(itens, dict):
            continue
        for nome, item in itens.items():
            assert item["tipo"] in {"PUBLICO", "MERCADO", "ESTIMADO"}, nome
            assert item["unidade"], nome
            assert item["ref"] is None or item["ref"] in refs, nome
