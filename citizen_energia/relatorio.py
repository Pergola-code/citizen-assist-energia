"""
Gera os artefatos da análise a partir do motor de cálculo:

    docs/04_calculos_gerados.md   -> memória de cálculo passo a passo
    dados_resultados/*.csv        -> tabelas para conferência em planilha
    docs/img/*.png                -> gráficos usados no README e no vídeo

Uso: python -m citizen_energia.relatorio
Rodar de novo sempre que um parâmetro em dados/parametros.json mudar.
"""

from __future__ import annotations

import csv
from pathlib import Path

from . import calculos as C
from .assistente import num, reais

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
IMG = DOCS / "img"
SAIDA_CSV = RAIZ / "dados_resultados"

# Paleta categórica validada (CVD-safe); a "situação atual" fica em cinza neutro.
CORES = {"atual": "#8a8984", "habitos": "#2a78d6", "aquecedor_solar": "#eb6834",
         "fotovoltaico": "#1baf7a", "combinado": "#eda100"}
TINTA, TINTA_2, GRADE = "#0b0b0b", "#52514e", "#e4e3df"
NOMES_CURTOS = {"atual": "Atual", "habitos": "Banho 5 min", "aquecedor_solar": "Aquecedor solar",
                "fotovoltaico": "Fotovoltaico", "combinado": "Solar + 5 min"}


# --------------------------------------------------------------------------
def _md_tabela(cabecalho: list[str], linhas: list[list]) -> str:
    out = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def _salvar_csv(nome: str, linhas: list[dict]) -> None:
    SAIDA_CSV.mkdir(exist_ok=True)
    with open(SAIDA_CSV / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)


def gerar_markdown() -> str:
    perfil = C.Perfil()
    P = C.P
    bruto = C.carregar_parametros_brutos()
    s = C.resumo_perfil(perfil)
    tab = C.comparar(perfil)
    sens = C.sensibilidade(perfil)
    sims = {k: C.simular(k, perfil) for k in CORES}

    m_dot = perfil.vazao_l_min / 60
    dt = perfil.temperatura_banho - perfil.temperatura_agua_fria
    h_dia = C.horas_banho_por_dia(perfil)

    md = []
    md.append("# Memória de cálculo (gerada automaticamente)\n")
    md.append("> Arquivo gerado por `python -m citizen_energia.relatorio`. Não edite à mão: altere "
              "`citizen_energia/dados/parametros.json` e rode de novo.\n")
    md.append(f"**Necessidade analisada:** água quente para o banho de uma família de {perfil.pessoas} pessoas "
              f"na área da Enel SP. **Período de referência:** 12 meses, tarifas vigentes em novembro/2026.\n")

    md.append("## 1. Parâmetros e premissas\n")
    md.append("Tipos: **PUBLICO** = dado oficial/publicado; **MERCADO** = preço de referência; "
              "**ESTIMADO** = premissa da equipe (justificada na nota).\n")
    linhas = []
    for grupo, itens in bruto.items():
        if grupo.startswith("_") or not isinstance(itens, dict):
            continue
        for nome, it in itens.items():
            v = it["valor"]
            if isinstance(v, list) and len(v) > 4:
                v = ", ".join(str(x) for x in v)
            linhas.append([f"`{nome}`", v, it["unidade"], it["tipo"], it["ref"] or "—", it["nota"]])
    md.append(_md_tabela(["Parâmetro", "Valor", "Unidade", "Tipo", "Ref.", "Nota"], linhas) + "\n")

    md.append("## 2. Quanto o chuveiro consome (física)\n")
    md.append("O chuveiro elétrico é um aquecedor de passagem: precisa entregar, a cada segundo, o calor que "
              "a água que passa por ele precisa para subir de temperatura.\n")
    md.append("```\nP = (ṁ · c · ΔT) / η\n```\n")
    md.append(f"- ṁ (vazão mássica) = {perfil.vazao_l_min} L/min ÷ 60 = {m_dot:.4f} kg/s\n"
              f"- c (calor específico da água) = {P['calor_especifico_agua']} J/(kg·°C)\n"
              f"- ΔT = {perfil.temperatura_banho} − {perfil.temperatura_agua_fria} = {dt} °C\n"
              f"- η (eficiência) = {perfil.eficiencia_chuveiro}\n"
              f"- **P = {m_dot:.4f} × {P['calor_especifico_agua']} × {dt} / {perfil.eficiencia_chuveiro} "
              f"= {s['potencia_kw']*1000:,.0f} W ≈ {s['potencia_kw']:.2f} kW**\n")
    md.append("Conferência de sanidade: chuveiros comerciais têm potência nominal entre ~4,5 e 7,5 kW, então "
              "o valor calculado é coerente.\n")
    md.append("Energia = Potência × Tempo:\n")
    md.append(f"- Tempo de chuveiro ligado por dia = {perfil.pessoas} pessoas × {perfil.minutos_por_banho} min ÷ 60 = "
              f"{h_dia:.3f} h/dia\n"
              f"- Energia em 30 dias = {s['potencia_kw']:.3f} kW × {h_dia:.3f} h × 30 = **{s['energia_chuveiro_mes']:.1f} kWh/mês**\n"
              f"- Participação no consumo da casa ({perfil.consumo_total_mensal} kWh/mês) = "
              f"**{s['participacao_chuveiro']*100:.1f}%**\n"
              f"- Calor útil entregue à água: {s['energia_termica_dia']:.2f} kWh/dia "
              f"(é o que um aquecedor solar precisa fornecer).\n")

    md.append("## 3. Quanto custa 1 kWh (Enel SP, residencial)\n")
    md.append("Os impostos são calculados \"por dentro\" (o imposto incide sobre o próprio total):\n")
    md.append("```\nPreço final = Tarifa sem impostos / (1 − ICMS − PIS/COFINS)\n```\n")
    for c in (150, 220):
        ic = C.aliquota_icms(c)
        md.append(f"- Conta de {c} kWh → ICMS {ic*100:.0f}%: {P['tarifa_b1_sem_impostos']} / (1 − {ic} − "
                  f"{P['pis_cofins_efetivo']}) = **R$ {C.tarifa_final_por_kwh(c):.4f}/kWh**\n")
    md.append("\n**Efeito de degrau do ICMS:** quando o consumo passa de 200 kWh, a alíquota sobe de 12% para 18% "
              "sobre a conta toda. Por isso reduzir o consumo de 220 para menos de 200 kWh economiza mais do que "
              "os kWh cortados \"valem\" isoladamente.\n")
    c0 = C.conta_mensal(perfil.consumo_total_mensal, True)
    md.append(f"\nConta de referência ({perfil.consumo_total_mensal} kWh, com Tarifa Social): "
              f"({perfil.consumo_total_mensal} − {c0['kwh_gratuitos']:.0f} gratuitos) × {P['tarifa_b1_sem_impostos']} "
              f"/ (1 − {c0['icms']} − {P['pis_cofins_efetivo']}) = **{reais(c0['total'])}/mês** "
              f"(sem iluminação pública).\n")

    md.append("## 4. As alternativas, mês a mês\n")
    md.append("Energia do chuveiro retirada da rede (kWh) e geração fotovoltaica (kWh), por mês:\n")
    cab = ["Mês", "Irrad. (kWh/m²·dia)"] + [NOMES_CURTOS[k] for k in CORES] + ["Geração FV"]
    linhas = []
    for i, mes in enumerate(C.MESES):
        linhas.append([mes, P["irradiacao_mensal_plano_23graus"][i]] +
                      [f"{sims[k].energia_chuveiro_rede_kwh[i]:.1f}" for k in CORES] +
                      [f"{sims['fotovoltaico'].geracao_fv_kwh[i]:.1f}"])
    linhas.append(["**Total**", ""] + [f"**{sims[k].energia_anual_rede:.0f}**" for k in CORES] +
                  [f"**{sum(sims['fotovoltaico'].geracao_fv_kwh):.0f}**"])
    md.append(_md_tabela(cab, linhas) + "\n")

    fv = sims["fotovoltaico"]
    prod_kwp = sum(P["irradiacao_mensal_plano_23graus"]) / 12 * 365 * P["performance_ratio_fv"]
    md.append("### 4.1 Como cada alternativa foi modelada\n")
    md.append(f"- **Hábitos:** mesma potência, banho de 5 min em vez de {perfil.minutos_por_banho} min. "
              f"Custo: {reais(P['habitos_custo_timer'])} (timer).\n"
              f"- **Aquecedor solar (renovável):** o sol fornece em média {P['fracao_solar_aquecedor']*100:.0f}% da energia do banho "
              f"(fração solar); a fração de cada mês é proporcional à irradiação do mês, limitada a 95%. "
              f"O chuveiro elétrico cobre o resto. Custo = SINAPI {reais(P['aquecedor_solar_kit_instalado'])} × "
              f"(1 + {P['aquecedor_solar_adaptacoes']:.0%} de adaptações) = {reais(sims['aquecedor_solar'].investimento)}.\n"
              f"  - Conferência física: coletor de 2 m² × 4,63 kWh/m²·dia × ~40% de eficiência do sistema ≈ 3,7 kWh/dia "
              f"de calor, acima dos {s['energia_termica_dia']:.2f} kWh/dia necessários na média. A fração não chega "
              f"a 100% por causa de dias nublados, perdas noturnas do reservatório e do inverno.\n"
              f"- **Fotovoltaico (renovável):** produtividade = irradiação média × 365 × PR = {prod_kwp:.0f} kWh/kWp·ano. "
              f"Para os {sims['atual'].energia_anual_rede:.0f} kWh/ano do chuveiro seriam "
              f"{sims['atual'].energia_anual_rede/prod_kwp:.2f} kWp; arredondando para módulos inteiros de 550 W → "
              f"**{fv.detalhes['kwp']} kWp** ({reais(fv.investimento)} a R$ {P['fv_custo_por_wp_pequeno']}/Wp). "
              f"Como o banho é à noite, toda a geração vai para a rede e volta como crédito; sobre cada kWh compensado "
              f"paga-se {P['fv_percentual_fio_b_2026']:.0%} do Fio B (R$ {P['fv_fio_b_enel_sp']}/kWh). "
              f"Créditos que sobraram no fim do ano: {fv.detalhes['creditos_sobrando_kwh']:.0f} kWh.\n"
              f"  - Observação de justiça na comparação: como não existe meio módulo, o menor sistema que cobre o "
              f"chuveiro gera {sum(fv.geracao_fv_kwh)/sims['atual'].energia_anual_rede:.0%} da energia do banho; o "
              f"excedente abate outros usos da casa. Por isso comparamos também o *investimento por kWh evitado*, "
              f"que neutraliza o tamanho.\n"
              f"- **Combinado:** hábitos + aquecedor solar.\n")

    md.append("## 5. Comparação final (mesma necessidade, mesmos 12 meses)\n")
    cab = ["Alternativa", "Renovável", "kWh evitados/ano", "Conta anual", "Economia líquida/ano", "Investimento",
           "R$ investido por kWh/ano", "Retorno simples", "VPL 10 anos (10% a.a.)", "CO2 evitado (kg/ano)",
           "Alívio no pico (kW)"]
    linhas = []
    for l in tab:
        pb = "—" if l["chave"] == "atual" else ("imediato" if not l["payback_anos"] else f"{num(l['payback_anos'], 1)} anos")
        linhas.append([l["alternativa"], "sim" if l["renovavel"] else "não", num(l["kwh_evitados_ano"]),
                       reais(l["conta_anual"]), reais(l["economia_anual"]), reais(l["investimento"]),
                       "—" if l["invest_por_kwh_ano"] is None else reais(l["invest_por_kwh_ano"]),
                       pb, reais(l["vpl_10a"]), num(l["co2_evitado_kg_ano"], 1), num(l["reducao_ponta_kw"], 1)])
    md.append(_md_tabela(cab, linhas) + "\n")
    md.append("Definições: *economia líquida* = redução da conta − manutenção anual; *retorno simples* = investimento ÷ "
              "economia líquida; *VPL* = −investimento + Σ economia/(1,10)^t, t = 1..10 (horizonte comum de 10 anos, "
              "sem valor residual, sem reajuste de tarifa — conservador); *CO2* = kWh evitados × fator médio do SIN; "
              "*alívio no pico* = potência do chuveiro × fração solar (o FV não gera às 18h–21h).\n")

    fvn = C.fv_normalizado(perfil)
    fvr = {l["chave"]: l for l in tab}
    md.append("### 5.1 Comparação normalizada do fotovoltaico\n")
    md.append(
        f"O menor sistema real (2 módulos, {num(fvr['fotovoltaico']['kwp'], 1)} kWp) gera "
        f"{sum(sims['fotovoltaico'].geracao_fv_kwh) / sims['atual'].energia_anual_rede:.0%} da energia do banho, então "
        "parte da economia da tabela acima vem de abater OUTROS usos da casa. Para comparar a mesma necessidade, "
        f"simulamos um sistema hipotético do tamanho exato do banho ({num(fvn['kwp'], 2)} kWp, "
        f"{fvn['fracao_do_banho']:.0%} da energia do banho):\n")
    md.append(_md_tabela(["Fotovoltaico", "kWp", "Investimento", "Economia líquida/ano", "Retorno"], [
        ["Sistema real (2 módulos)", num(fvr["fotovoltaico"]["kwp"], 2), reais(fvr["fotovoltaico"]["investimento"]),
         reais(fvr["fotovoltaico"]["economia_anual"]), f"{num(fvr['fotovoltaico']['payback_anos'], 1)} anos"],
        ["**Normalizado (só o banho)**", num(fvn["kwp"], 2), reais(fvn["investimento"]),
         f"**{reais(fvn['economia_anual'])}**", f"**{num(fvn['payback_anos'], 1)} anos**"],
        ["Aquecedor solar (referência)", "—", reais(fvr["aquecedor_solar"]["investimento"]),
         reais(fvr["aquecedor_solar"]["economia_anual"]), f"{num(fvr['aquecedor_solar']['payback_anos'], 1)} anos"],
    ]) + "\n")
    md.append("Conclusão: atendendo exatamente a mesma necessidade, o fotovoltaico ainda se paga um pouco mais rápido que "
              "o aquecedor solar no cenário base, mas a diferença de economia anual cai de "
              f"{reais(fvr['fotovoltaico']['economia_anual'] - fvr['aquecedor_solar']['economia_anual'])} para "
              f"{reais(fvn['economia_anual'] - fvr['aquecedor_solar']['economia_anual'])}. Essa vantagem depende de regras "
              "de compensação que pioram até 2028 e não inclui alívio do pico noturno.\n")

    md.append("## 6. Análise de sensibilidade\n")
    md.append("Cada linha muda UMA premissa incerta e recalcula tudo. Serve para mostrar que os resultados são "
              "estimativas com faixa de variação, não números garantidos.\n")
    cab = ["Cenário", "Hábitos: economia/ano", "Aquecedor: economia", "Aquecedor: retorno", "FV: economia",
           "FV: retorno", "Combinado: economia", "Combinado: retorno"]
    fmt = lambda v: "—" if v is None else f"{num(v, 1)} anos"
    linhas = [[x["cenario"], reais(x["habitos_economia"]), reais(x["solar_economia"]), fmt(x["solar_payback"]),
               reais(x["fv_economia"]), fmt(x["fv_payback"]), reais(x["combinado_economia"]),
               fmt(x["combinado_payback"])] for x in sens]
    md.append(_md_tabela(cab, linhas) + "\n")

    md.append("## 7. Leitura dos resultados\n")
    t = {l["chave"]: l for l in tab}
    md.append(
        f"1. **Hábito é o primeiro passo:** {reais(t['habitos']['economia_anual'])}/ano com custo quase zero. Parte do "
        "ganho vem do degrau do ICMS (a casa cai abaixo de 200 kWh).\n"
        f"2. **Aquecedor solar** retorna em ~{num(t['aquecedor_solar']['payback_anos'], 1)} anos, é a única alternativa que "
        f"reduz o pico do fim da tarde (~{num(t['aquecedor_solar']['reducao_ponta_kw'], 1)} kW por casa) e não depende de "
        "regras de compensação. É sensível ao custo de obra: se a instalação dobrar de preço, o retorno passa de 10 anos.\n"
        f"3. **Fotovoltaico** tem o menor custo por kWh evitado e retorno de ~{num(t['fotovoltaico']['payback_anos'], 1)} anos no "
        "cenário base, mas exige o maior desembolso inicial, homologação, telhado próprio e fica menos favorável com o "
        "Fio B subindo até 2028. Não alivia o pico noturno.\n"
        "4. **Recomendação do assistente:** hábitos já; aquecedor solar para quem tem casa própria e telhado; "
        "fotovoltaico como opção para quem tem acesso a crédito barato ou programa social, sempre com 3 orçamentos.\n")

    _salvar_csv("comparacao_12_meses.csv", tab)
    _salvar_csv("sensibilidade.csv", sens)
    mensal = []
    for i, mes in enumerate(C.MESES):
        linha = {"mes": mes, "irradiacao_kwh_m2_dia": P["irradiacao_mensal_plano_23graus"][i]}
        for k in CORES:
            linha[f"kwh_chuveiro_rede_{k}"] = round(sims[k].energia_chuveiro_rede_kwh[i], 2)
            linha[f"conta_{k}"] = round(sims[k].contas[i]["total"], 2)
        linha["geracao_fv_kwh"] = round(sims["fotovoltaico"].geracao_fv_kwh[i], 2)
        mensal.append(linha)
    _salvar_csv("resultados_mensais.csv", mensal)
    return "\n".join(md)


# --------------------------------------------------------------------------
def gerar_graficos() -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    IMG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.edgecolor": GRADE, "axes.labelcolor": TINTA_2,
                         "xtick.color": TINTA_2, "ytick.color": TINTA_2, "text.color": TINTA,
                         "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "#fcfcfb",
                         "axes.facecolor": "#fcfcfb"})
    perfil = C.Perfil()
    tab = C.comparar(perfil)
    arquivos = []

    # 1) Conta anual por alternativa (magnitude -> barras, rótulo direto em cada barra)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    nomes = [NOMES_CURTOS[l["chave"]] for l in tab]
    vals = [l["conta_anual"] for l in tab]
    barras = ax.bar(nomes, vals, color=[CORES[l["chave"]] for l in tab], width=0.62, edgecolor="#fcfcfb", linewidth=2)
    for b, v in zip(barras, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 25, reais(v).replace(",00", ""), ha="center", color=TINTA, fontsize=10)
    ax.set_ylabel("R$ por ano")
    ax.set_title("Conta de luz estimada em 12 meses (família de referência)", loc="left", fontsize=13)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    p = IMG / "conta_anual.png"
    fig.savefig(p, dpi=160)
    arquivos.append(p)
    plt.close(fig)

    # 2) Energia do chuveiro tirada da rede, mês a mês (mudança no tempo -> linhas, rótulo no fim)
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    for k in CORES:
        r = C.simular(k, perfil)
        serie = r.energia_chuveiro_rede_kwh if k != "fotovoltaico" else \
            [max(0, e - g) for e, g in zip(r.energia_chuveiro_rede_kwh, r.geracao_fv_kwh)]
        estilo = "--" if k == "atual" else "-"
        ax.plot(C.MESES, serie, estilo, color=CORES[k], linewidth=2, marker="o", markersize=4, label=NOMES_CURTOS[k])
        ax.annotate(NOMES_CURTOS[k], (11, serie[-1]), xytext=(8, 0), textcoords="offset points",
                    va="center", color=TINTA_2, fontsize=9)
    ax.set_ylabel("kWh do chuveiro pagos à rede")
    ax.set_title("Energia do banho que ainda vem da rede, mês a mês\n(FV = consumo do chuveiro − geração, saldo via créditos)",
                 loc="left", fontsize=12)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.1), fontsize=9)
    ax.set_xlim(-0.3, 12.8)
    fig.tight_layout()
    p = IMG / "energia_mensal.png"
    fig.savefig(p, dpi=160)
    arquivos.append(p)
    plt.close(fig)

    # 3) Fluxo de caixa acumulado (retorno do investimento ao longo de 10 anos)
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    anos = list(range(0, 11))
    for l in tab:
        if l["chave"] == "atual":
            continue
        acum = [-l["investimento"] + l["economia_anual"] * a for a in anos]
        ax.plot(anos, acum, color=CORES[l["chave"]], linewidth=2, label=NOMES_CURTOS[l["chave"]])
        ax.annotate(NOMES_CURTOS[l["chave"]], (10, acum[-1]), xytext=(6, 0), textcoords="offset points",
                    va="center", color=TINTA_2, fontsize=9)
    ax.axhline(0, color=TINTA_2, linewidth=1)
    ax.set_xlabel("Anos")
    ax.set_ylabel("Saldo acumulado (R$)")
    ax.set_title("Quando cada alternativa se paga (saldo = economia acumulada − investimento)", loc="left", fontsize=12)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    ax.set_xlim(0, 11.8)
    fig.tight_layout()
    p = IMG / "retorno_acumulado.png"
    fig.savefig(p, dpi=160)
    arquivos.append(p)
    plt.close(fig)
    return arquivos


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    md = gerar_markdown()
    (DOCS / "04_calculos_gerados.md").write_text(md, encoding="utf-8")
    imgs = gerar_graficos()
    print("Gerado: docs/04_calculos_gerados.md, dados_resultados/*.csv e", ", ".join(i.name for i in imgs))


if __name__ == "__main__":
    main()
