"""Testes da interface web: API, validação e servidor HTTP real."""

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from citizen_energia import calculos as C
from citizen_energia.assistente import reais
from citizen_energia.web import Handler, api_perguntar, api_simular


def test_api_perguntar_devolve_resumo_e_fontes():
    d = api_perguntar({"mensagem": "placa solar zera a conta?"})
    assert d["intencao"] == "conta_zero" and d["resumo"] and d["fontes"]


def test_api_perguntar_vazia_da_erro():
    with pytest.raises(ValueError):
        api_perguntar({"mensagem": "  "})


def test_api_simular_nao_sei_estima_consumo():
    d = api_simular({"pessoas": 4, "minutos": 8, "consumo": "nao_sei", "tarifa_social": True})
    assert "estimei" in d["limitacoes"][0]


def test_api_simular_usa_mesmos_numeros_da_analise():
    d = api_simular({"pessoas": 4, "minutos": 8, "consumo": 220, "tarifa_social": True, "casa_propria": True})
    t = {l["chave"]: l for l in C.comparar()}
    assert reais(t["aquecedor_solar"]["investimento"]) in d["texto"]


@pytest.mark.parametrize("dados", [{"pessoas": "x", "minutos": 8}, {"pessoas": 0, "minutos": 8},
                                   {"pessoas": 4, "minutos": 8, "consumo": "abc"}, {"pessoas": 4, "minutos": 8, "consumo": 5}])
def test_api_simular_valida_entrada(dados):
    with pytest.raises(ValueError):
        api_simular(dados)


@pytest.fixture(scope="module")
def servidor():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def _post(url, corpo: bytes):
    req = urllib.request.Request(url, data=corpo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_servidor_entrega_pagina(servidor):
    with urllib.request.urlopen(servidor + "/") as r:
        assert r.status == 200 and b"Citizen Assist AI" in r.read()


def test_servidor_responde_pergunta(servidor):
    status, d = _post(servidor + "/api/perguntar", json.dumps({"mensagem": "moro de aluguel"}).encode())
    assert status == 200 and d["intencao"] == "moradia"


def test_servidor_rejeita_json_invalido(servidor):
    status, d = _post(servidor + "/api/perguntar", b"lixo")
    assert status == 400 and d["erro"] == "Requisição inválida."


def test_servidor_rota_inexistente(servidor):
    status, _ = _post(servidor + "/api/nada", b"{}")
    assert status == 404
