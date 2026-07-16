# -*- coding: utf-8 -*-
"""
Gera o gráfico radar da evolução do aluno ao longo das AGES.

A ideia do gráfico é ser CUMULATIVO: em cada eixo (competência), o valor de uma
AGES nunca pode ser menor do que o da AGES anterior. Por isso, após definir os
valores estimados, aplicamos o "máximo acumulado" ao longo das quatro passagens
(np.maximum.accumulate), garantindo curvas que só crescem (ou se mantêm), nunca
recuando.

Requer: matplotlib e numpy. Gera 'fig-radar-ages.png' neste mesmo diretório.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --- Competências (eixos), em sentido horário a partir do topo -------------
EIXOS = [
    "Comunicação",
    "Trabalho\nem equipe",
    "Liderança",
    "Programação",
    "Design",
    "Qualidade",
    "Adaptabilidade",
]

# --- Valores estimados (0-100), na ordem dos eixos acima --------------------
#     Linhas = AGES I, II, III, IV.
VALORES_BASE = np.array([
    [40, 40, 30, 38, 35, 42, 38],  # AGES I  — Focus
    [52, 55, 42, 50, 52, 62, 55],  # AGES II — Decola
    [68, 62, 65, 82, 47, 78, 72],  # AGES III — Totem Interativo
    [85, 80, 88, 68, 50, 76, 78],  # AGES IV — Estudify
], dtype=float)

# --- Torna os valores cumulativos: cada AGES >= a anterior em cada eixo ------
VALORES = np.maximum.accumulate(VALORES_BASE, axis=0)

SERIES = [
    ("AGES I — Focus",             "#4C72B0"),
    ("AGES II — Decola",           "#DD8452"),
    ("AGES III — Totem Interativo", "#55A868"),
    ("AGES IV — Estudify",         "#C44E52"),
]

# --- Ângulos dos eixos (fecha o polígono repetindo o primeiro) --------------
N = len(EIXOS)
angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angulos += angulos[:1]

fig = plt.figure(figsize=(9, 9.5))
ax = fig.add_subplot(111, polar=True)

# Topo = primeiro eixo, sentido horário (como no gráfico original)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Eixos angulares (competências)
ax.set_xticks(angulos[:-1])
ax.set_xticklabels(EIXOS, fontsize=15)
ax.tick_params(axis="x", pad=18)

# Escala radial 0-100
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=10, color="#8a8a8a")
ax.set_rlabel_position(9)

# Grade discreta
ax.grid(color="#d9d9d9", linewidth=1.0)
ax.spines["polar"].set_color("#d9d9d9")
ax.set_axisbelow(True)

# --- Plota cada AGES --------------------------------------------------------
handles = []
for (rotulo, cor), linha in zip(SERIES, VALORES):
    dados = linha.tolist()
    dados += dados[:1]
    ax.plot(angulos, dados, color=cor, linewidth=2.2, zorder=3)
    ax.fill(angulos, dados, color=cor, alpha=0.10, zorder=2)
    handles.append(Patch(facecolor=cor, edgecolor=cor, label=rotulo, alpha=0.9))

# --- Legenda (2 colunas; matplotlib preenche coluna-a-coluna: I,II | III,IV) -
ax.legend(
    handles=handles,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.06),
    ncol=2,
    frameon=False,
    fontsize=14,
    handlelength=1.4,
    columnspacing=3.0,
)

plt.tight_layout()

saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig-radar-ages.png")
fig.savefig(saida, dpi=200, bbox_inches="tight", facecolor="white")
print("Gerado:", saida)
