"""
Interface web do módulo de Energia do Citizen Assist AI.

Uso:
    python -m citizen_energia.web            # abre http://localhost:8000 no navegador
    python -m citizen_energia.web --porta 8080 --sem-navegador

Por que um servidor tão simples (só biblioteca padrão)?
  - Não exige instalar nada além do Python.
  - A página chama as MESMAS funções da análise (`responder`, `simulacao_personalizada`),
    então os números mostrados ao cidadão continuam idênticos aos dos cálculos.
  - Funciona no celular: basta abrir o endereço da máquina na mesma rede Wi-Fi.
"""

from __future__ import annotations

import argparse
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import calculos as C
from .assistente import simulacao_personalizada
from .integracao import resposta_para_dict, responder_para_citizen_assist

PAGINA = Path(__file__).parent / "web" / "index.html"
LIMITE_CORPO = 10_000  # bytes: perguntas são curtas; evita abuso


def api_perguntar(dados: dict) -> dict:
    mensagem = str(dados.get("mensagem", "")).strip()[:500]
    if not mensagem:
        raise ValueError("Escreva uma pergunta.")
    return responder_para_citizen_assist(mensagem)


def api_simular(dados: dict) -> dict:
    """Valida os dados do formulário e roda a simulação personalizada."""
    try:
        pessoas = int(dados.get("pessoas"))
        minutos = float(dados.get("minutos"))
    except (TypeError, ValueError):
        raise ValueError("Informe o número de pessoas e os minutos de banho.")
    if not (1 <= pessoas <= 20 and 1 <= minutos <= 60):
        raise ValueError("Use entre 1 e 20 pessoas e entre 1 e 60 minutos de banho.")
    consumo = dados.get("consumo")
    estimado = consumo in (None, "", "nao_sei")
    if estimado:
        consumo = C.estimar_consumo_total(pessoas, minutos)
    else:
        try:
            consumo = float(str(consumo).replace(",", "."))
        except ValueError:
            raise ValueError("O consumo deve ser um número em kWh (ou marque 'não sei').")
        if not 10 <= consumo <= 2000:
            raise ValueError("O consumo deve estar entre 10 e 2.000 kWh por mês.")
    perfil = C.Perfil(pessoas=pessoas, minutos_por_banho=minutos, consumo_total_mensal=consumo,
                      tarifa_social=bool(dados.get("tarifa_social", False)))
    r = simulacao_personalizada(perfil, casa_propria=bool(dados.get("casa_propria", True)))
    saida = resposta_para_dict(r)
    if estimado:
        saida["limitacoes"].insert(0, f"Como você não sabia o consumo, estimei {consumo:.0f} kWh/mês "
                                      f"para {pessoas} pessoas. Confira o valor real na sua conta de luz.")
    return saida


ROTAS = {"/api/perguntar": api_perguntar, "/api/simular": api_simular}


class Handler(BaseHTTPRequestHandler):
    def _enviar(self, codigo: int, corpo: bytes, tipo: str) -> None:
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(corpo)

    def _json(self, codigo: int, dados: dict) -> None:
        self._enviar(codigo, json.dumps(dados, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):  # noqa: N802 (nome exigido pela biblioteca)
        if self.path in ("/", "/index.html"):
            self._enviar(200, PAGINA.read_bytes(), "text/html; charset=utf-8")
        else:
            self._json(404, {"erro": "Página não encontrada."})

    def do_POST(self):  # noqa: N802
        rota = ROTAS.get(self.path)
        if rota is None:
            return self._json(404, {"erro": "Rota não encontrada."})
        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho > LIMITE_CORPO:
            return self._json(413, {"erro": "Mensagem grande demais."})
        try:
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except json.JSONDecodeError:
            return self._json(400, {"erro": "Requisição inválida."})
        if not isinstance(dados, dict):
            return self._json(400, {"erro": "Requisição inválida."})
        try:
            self._json(200, rota(dados))
        except ValueError as e:  # erros de validação com mensagem para o cidadão
            self._json(400, {"erro": str(e)})

    def log_message(self, formato, *args):  # silencia o log padrão do terminal
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Interface web do módulo de Energia do Citizen Assist AI")
    parser.add_argument("--porta", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1", help="use 0.0.0.0 para acessar pelo celular na mesma rede")
    parser.add_argument("--sem-navegador", action="store_true")
    args = parser.parse_args()
    servidor = ThreadingHTTPServer((args.host, args.porta), Handler)
    url = f"http://localhost:{args.porta}"
    print(f"Citizen Assist AI · Energia rodando em {url}  (Ctrl+C para sair)")
    if not args.sem_navegador:
        webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
