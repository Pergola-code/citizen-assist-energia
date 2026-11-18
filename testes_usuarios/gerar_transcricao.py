"""
Reexecuta as perguntas das personas simuladas e grava a transcrição real das respostas.
Uso: python testes_usuarios/gerar_transcricao.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from citizen_energia.assistente import responder  # noqa: E402

# Intenção detectada na versão ANTES dos ajustes (commit b8fe1c7), registrada na 1ª rodada.
PERSONAS = {
    "P1 · Cida, 58, dona de casa, casa própria, Tarifa Social, pouca familiaridade com tecnologia": [
        ("quanto gasta meu chuveiro", "chuveiro"), ("minha conta vem muito cara", "nao_entendi"),
        ("o que é kwh", "nao_entendi"), ("como faço pra pagar menos", "habitos")],
    "P2 · Jefferson, 34, motoboy, casa alugada, 3 pessoas, sem Tarifa Social, usa celular": [
        ("chuveiro gasta mto?", "chuveiro"), ("moro de aluguel da pra colocar aquecedor solar?", "aquecedor_solar"),
        ("vale a pena placa solar", "fotovoltaico")],
    "P3 · Rosana, 45, diarista, casa própria, 5 pessoas, Bolsa Família, abordada por vendedor de placa solar": [
        ("um vendedor falou q a placa solar zera minha conta é verdade?", "fotovoltaico"),
        ("e o aquecedor solar?", "aquecedor_solar"), ("qual é melhor pra mim", "comparar"),
        ("tenho bolsa familia tenho desconto na luz?", "nao_entendi")],
    "P4 · Antônio, 67, aposentado, apartamento (CDHU), 2 pessoas": [
        ("moro em apartamento", "nao_entendi"), ("o que da pra fazer no apartamento", "nao_entendi"),
        ("a resistencia queimou posso trocar sozinho", "seguranca")],
    "P5 · Larissa, 22, estudante, mora com os pais, familiar com tecnologia, desconfiada de números": [
        ("esses numeros sao confiaveis?", "nao_entendi"), ("de onde vem os dados", "fontes"),
        ("quanto co2 eu economizo", "ambiente"), ("e se a tarifa aumentar", "nao_entendi")],
}


def main():
    out = ["# Transcrição da avaliação com personas simuladas (2ª rodada, versão ajustada)\n",
           "> **Personas simuladas, não pessoas reais.** As perguntas foram escritas para imitar o jeito de falar do "
           "público (sem acento, abreviações, frases incompletas) e executadas no assistente real. As respostas abaixo "
           "são a saída real do programa. Gerado por `python testes_usuarios/gerar_transcricao.py`.\n"]
    for persona, perguntas in PERSONAS.items():
        out.append(f"## {persona}\n")
        for pergunta, antes in perguntas:
            r = responder(pergunta)
            out.append(f"### \"{pergunta}\"\n")
            out.append(f"Intenção antes dos ajustes: `{antes}` → depois: `{r.intencao}`\n")
            out.append("```\n" + r.formatada() + "\n```\n")
    (RAIZ / "testes_usuarios" / "05_transcricao_personas.md").write_text("\n".join(out), encoding="utf-8")
    print("Gerado: testes_usuarios/05_transcricao_personas.md")


if __name__ == "__main__":
    main()
