"""
Interface de linha de comando do módulo de Energia.

Uso:
    python -m citizen_energia            # conversa interativa
    python -m citizen_energia "pergunta" # resposta única (bom para demonstrar no vídeo)
"""

import re
import sys

from . import calculos as C
from .assistente import responder, simulacao_personalizada

BANNER = """
==============================================================
  Citizen Assist AI  |  Módulo de Energia e Sustentabilidade
  Foco: gastar menos com o chuveiro elétrico (Grande SP)
  Digite sua pergunta, "simular" para usar seus dados, ou "sair".
==============================================================
"""


NAO_SEI = ("nao sei", "não sei", "sei la", "sei lá", "nao lembro", "não lembro", "ns", "?")


def extrair_numero(bruto: str) -> float | None:
    """
    Pega o primeiro número do texto: "4 pessoas" -> 4, "10 minutos" -> 10, "1.250,5" -> 1250.5.
    Ajuste A8: nos testes, as personas respondiam com unidade ("10 minutos") e eram rejeitadas.
    """
    achado = re.search(r"\d+(?:[.,]\d+)*", bruto)
    if not achado:
        return None
    txt = achado.group()
    if "," in txt:                       # formato brasileiro: 1.250,5
        txt = txt.replace(".", "").replace(",", ".")
    elif txt.count(".") == 1 and len(txt.split(".")[1]) == 3:
        txt = txt.replace(".", "")       # "1.250" = mil duzentos e cinquenta
    return float(txt)


def perguntar_numero(texto: str, padrao: float, minimo: float = 0, aceita_nao_sei: bool = False) -> float | None:
    """Lê um número com valor padrão; repete até receber algo válido."""
    while True:
        bruto = input(f"{texto} [{padrao:g}]: ").strip().lower()
        if not bruto:
            return padrao
        if aceita_nao_sei and bruto in NAO_SEI:
            return None
        valor = extrair_numero(bruto)
        if valor is not None and valor > minimo:
            return valor
        dica = " ou \"não sei\"" if aceita_nao_sei else ""
        print(f"  Não entendi. Digite um número (ex.: 4){dica}.")


def fluxo_simulacao() -> None:
    padrao = C.Perfil()
    print("\nVamos simular com os dados da sua casa (Enter usa o valor sugerido).")
    print("Dica: o consumo em kWh aparece na sua conta de luz, no campo \"Consumo\".")
    pessoas = max(1, round(perguntar_numero("Quantas pessoas tomam banho na casa?", padrao.pessoas)))
    minutos = perguntar_numero("Quantos minutos dura cada banho, em média?", padrao.minutos_por_banho)
    # Ajuste A9: o valor sugerido de consumo passa a ser estimado para ESTA família, não fixo em 220 kWh.
    estimado = C.estimar_consumo_total(pessoas, minutos)
    consumo = perguntar_numero("Consumo total da casa no mês, em kWh (está na conta de luz)? Se não souber, digite \"não sei\"",
                               round(estimado), aceita_nao_sei=True)
    if consumo is None:
        consumo = estimado
        print(f"  Sem problema: vou usar uma estimativa de {estimado:.0f} kWh para {pessoas} pessoas.")
    social = perguntar_sim_nao("Você tem Tarifa Social / Baixa Renda na conta?", True)
    casa_propria = perguntar_sim_nao("Você mora em CASA PRÓPRIA, com telhado?", True)
    perfil = C.Perfil(pessoas=pessoas, minutos_por_banho=minutos, consumo_total_mensal=consumo, tarifa_social=social)
    print()
    print(simulacao_personalizada(perfil, casa_propria=casa_propria).formatada())


def perguntar_sim_nao(texto: str, padrao: bool) -> bool:
    sugestao = "s" if padrao else "n"
    while True:
        bruto = input(f"{texto} (s/n) [{sugestao}]: ").strip().lower()
        if not bruto:
            return padrao
        if bruto in ("s", "sim", "ss", "tenho", "moro", "yes", "y"):
            return True
        if bruto in ("n", "nao", "não", "nn", "no") or bruto.startswith(("nao", "não")):
            return False
        print("  Responda s (sim) ou n (não).")


def main() -> None:
    if len(sys.argv) > 1:
        r = responder(" ".join(sys.argv[1:]))
        print(r.formatada(com_links=(r.intencao == "fontes")))
        return
    print(BANNER)
    while True:
        try:
            msg = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break
        if not msg:
            continue
        if msg.lower() in ("sair", "exit", "tchau"):
            print("Até logo! Lembre-se: cada minuto a menos no banho conta.")
            break
        if "simul" in msg.lower() or "meus dados" in msg.lower():
            fluxo_simulacao()
            continue
        r = responder(msg)
        print("\nAssistente:\n" + r.formatada(com_links=(r.intencao == "fontes")))


if __name__ == "__main__":
    main()
