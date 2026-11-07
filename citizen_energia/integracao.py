"""
Pontos de integração com o restante do Citizen Assist AI.

Há dois jeitos de plugar este módulo no assistente do grupo:

1) Roteamento direto (sem LLM)
   O assistente principal detecta que o assunto é energia e chama
   `responder_para_citizen_assist(mensagem)`. Recebe um dicionário pronto para exibir.

2) Assistente com LLM (ex.: chatbot com modelo de linguagem)
   Use `contexto_para_llm()` como parte do prompt de sistema. Ele entrega os
   NÚMEROS JÁ CALCULADOS e as regras de uso, para que o modelo não invente
   valores e sempre cite fontes e limitações.
"""

from __future__ import annotations

import json

from . import calculos as C
from .assistente import detectar_intencao, responder

PALAVRAS_ENERGIA = ["energia", "luz", "conta de luz", "chuveiro", "banho", "kwh", "solar", "fotovolt",
                    "aquecedor", "tarifa", "bandeira", "enel", "eletric", "economizar"]


def e_assunto_de_energia(mensagem: str) -> bool:
    """Filtro simples para o roteador do assistente principal."""
    from .assistente import normalizar
    m = normalizar(mensagem)
    return any(p in m for p in PALAVRAS_ENERGIA)


def responder_para_citizen_assist(mensagem: str, perfil: C.Perfil | None = None) -> dict:
    r = responder(mensagem, perfil)
    refs = C.carregar_referencias()
    return {
        "modulo": "energia",
        "intencao": r.intencao,
        "texto": r.texto,
        "limitacoes": r.limitacoes,
        "fontes": [{"id": f, "titulo": refs[f]["titulo"], "url": refs[f]["url"]} for f in r.fontes if f in refs],
        "texto_formatado": r.formatada(),
    }


def contexto_para_llm(perfil: C.Perfil | None = None) -> str:
    """Bloco de contexto 'aterrado' (grounded) para um LLM."""
    perfil = perfil or C.Perfil()
    dados = {
        "perfil_referencia": perfil.__dict__,
        "situacao_atual": {k: round(v, 3) for k, v in C.resumo_perfil(perfil).items()},
        "comparacao_12_meses": C.comparar(perfil),
        "sensibilidade": C.sensibilidade(perfil),
        "referencias": C.carregar_referencias(),
    }
    regras = (
        "Você é o módulo de energia do Citizen Assist AI. Público: famílias de baixa renda da Grande SP.\n"
        "REGRAS: (1) Use SOMENTE os números do JSON abaixo; não invente valores. "
        "(2) Diga sempre que são estimativas, não garantias. "
        "(3) Cite as referências pelo id (ex.: [R01]). "
        "(4) Linguagem simples, frases curtas. "
        "(5) Recomende primeiro mudança de hábito (custo zero); depois aquecedor solar se a casa for própria e "
        "tiver telhado; placas fotovoltaicas com ressalvas de investimento inicial e Fio B. "
        "(6) Segurança elétrica: oriente procurar eletricista; nunca ensine mexer na fiação.\n"
    )
    return regras + "DADOS:\n" + json.dumps(dados, ensure_ascii=False, indent=1, default=str)


__all__ = ["e_assunto_de_energia", "responder_para_citizen_assist", "contexto_para_llm", "detectar_intencao"]
