"""Testes do assistente: intenção certa, números coerentes com a análise, fontes e limitações sempre presentes."""

import pytest

from citizen_energia import calculos as C
from citizen_energia.assistente import detectar_intencao, num, reais, responder, simulacao_personalizada
from citizen_energia.integracao import contexto_para_llm, e_assunto_de_energia, responder_para_citizen_assist


@pytest.mark.parametrize("pergunta,intencao", [
    ("Quanto meu chuveiro gasta?", "chuveiro"),
    ("Como economizar no banho?", "habitos"),
    ("Vale a pena aquecedor solar?", "aquecedor_solar"),
    ("e placa fotovoltaica?", "fotovoltaico"),
    ("o que é fio B", "fotovoltaico"),
    ("compare aquecedor solar e placa fotovoltaica", "comparar"),
    ("qual a melhor opção pra mim?", "comparar"),
    ("tenho cadúnico, tenho desconto?", "tarifa_social"),
    ("qual o impacto no meio ambiente", "ambiente"),
    ("o chuveiro deu choque", "seguranca"),
    ("solar", "solar_ambiguo"),
    ("oi", "ajuda"),
    ("de onde vêm esses números?", "fontes"),
    ("isso é garantido?", "limitacoes"),
    ("qual a bandeira desse mês", "bandeira"),
    ("asdfgh", "nao_entendi"),
])
def test_intencoes(pergunta, intencao):
    assert detectar_intencao(pergunta) == intencao


def test_ola_nao_confunde_com_solar():
    assert detectar_intencao("aquecedor solar") == "aquecedor_solar"


@pytest.mark.parametrize("pergunta", ["quanto gasta o chuveiro", "como economizar", "aquecedor solar",
                                      "placa fotovoltaica", "compare", "meio ambiente"])
def test_respostas_tecnicas_trazem_fontes_e_limitacoes(pergunta):
    r = responder(pergunta)
    assert r.fontes, "toda resposta com número precisa citar fonte"
    assert r.limitacoes, "toda resposta com estimativa precisa dizer a limitação"
    assert "De onde vêm esses números" in r.formatada()


def test_numeros_da_resposta_sao_os_da_analise():
    """Coerência: o texto do assistente usa exatamente os valores do motor de cálculo."""
    t = {l["chave"]: l for l in C.comparar()}
    texto = responder("vale a pena aquecedor solar").texto
    assert reais(t["aquecedor_solar"]["investimento"]) in texto
    assert reais(t["aquecedor_solar"]["economia_anual"]) in texto
    texto_cmp = responder("compare as opções").texto
    assert reais(t["fotovoltaico"]["economia_anual"]) in texto_cmp


def test_simulacao_personalizada_reage_ao_perfil():
    pequeno = simulacao_personalizada(C.Perfil(pessoas=2, minutos_por_banho=5, consumo_total_mensal=150))
    grande = simulacao_personalizada(C.Perfil(pessoas=6, minutos_por_banho=10, consumo_total_mensal=350))
    assert pequeno.texto != grande.texto
    assert "ESTIMATIVAS" in pequeno.formatada()


def test_alerta_quando_dados_parecem_inconsistentes():
    r = simulacao_personalizada(C.Perfil(pessoas=6, minutos_por_banho=15, consumo_total_mensal=150))
    assert any("60%" in l for l in r.limitacoes)


def test_integracao_devolve_estrutura_estavel():
    d = responder_para_citizen_assist("quanto meu chuveiro gasta")
    assert set(d) >= {"modulo", "intencao", "texto", "limitacoes", "fontes", "texto_formatado"}
    assert d["fontes"][0]["url"].startswith("http")


def test_roteador_reconhece_assunto():
    assert e_assunto_de_energia("minha conta de luz veio alta")
    assert not e_assunto_de_energia("onde fica o posto de saúde?")


def test_contexto_llm_contem_regras_e_dados():
    ctx = contexto_para_llm()
    assert "não invente valores" in ctx and "comparacao_12_meses" in ctx


def test_formatacao_brasileira():
    assert reais(1234.5) == "R$ 1.234,50"
    assert num(3.14159, 2) == "3,14"
