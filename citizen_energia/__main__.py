"""
Interface de linha de comando do módulo de Energia.

Uso:
    python -m citizen_energia            # conversa interativa
    python -m citizen_energia "pergunta" # resposta única (bom para demonstrar no vídeo)
"""

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


def perguntar_numero(texto: str, padrao: float, minimo: float = 0) -> float:
    """Lê um número com valor padrão; repete até receber algo válido."""
    while True:
        bruto = input(f"{texto} [{padrao:g}]: ").strip().replace(",", ".")
        if not bruto:
            return padrao
        try:
            valor = float(bruto)
            if valor > minimo:
                return valor
        except ValueError:
            pass
        print("  Não entendi. Digite só o número (ex.: 4).")


def fluxo_simulacao() -> None:
    padrao = C.Perfil()
    print("\nVamos simular com os dados da sua casa (Enter usa o valor sugerido).")
    print("Dica: o consumo em kWh aparece na sua conta de luz, no campo \"Consumo\".")
    pessoas = int(perguntar_numero("Quantas pessoas tomam banho na casa?", padrao.pessoas))
    minutos = perguntar_numero("Quantos minutos dura cada banho, em média?", padrao.minutos_por_banho)
    consumo = perguntar_numero("Consumo total da casa no mês (kWh)?", padrao.consumo_total_mensal)
    social = input("Você tem Tarifa Social / Baixa Renda na conta? (s/n) [s]: ").strip().lower() not in ("n", "nao", "não")
    perfil = C.Perfil(pessoas=pessoas, minutos_por_banho=minutos, consumo_total_mensal=consumo, tarifa_social=social)
    print()
    print(simulacao_personalizada(perfil).formatada())


def main() -> None:
    if len(sys.argv) > 1:
        print(responder(" ".join(sys.argv[1:])).formatada())
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
        print("\nAssistente:\n" + responder(msg).formatada())


if __name__ == "__main__":
    main()
