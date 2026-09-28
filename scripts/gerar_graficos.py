import matplotlib.pyplot as plt
import numpy as np
import os

# Pasta onde os gráficos serão salvos
PASTA = "resultados/graficos"
os.makedirs(PASTA, exist_ok=True)

protocolos = ["RIP", "OSPF", "BGP"]


# ============================================================
# GRÁFICO 1 - TEMPO DE CONVERGÊNCIA
# ============================================================

convergencia_ms = [16694, 223, 181]

plt.figure(figsize=(8, 5))
barras = plt.bar(protocolos, convergencia_ms)

plt.title("Tempo de Convergência após Falha do Enlace R3–R5")
plt.ylabel("Tempo de convergência (ms)")
plt.xlabel("Protocolo")

for barra, valor in zip(barras, convergencia_ms):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height(),
        f"{valor} ms",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig(
    os.path.join(PASTA, "convergencia_protocolos.png"),
    dpi=300
)
plt.close()


# ============================================================
# GRÁFICO 2 - LATÊNCIA MÉDIA R1 -> R5
# ============================================================

latencia_ms = [0.162, 0.219, 0.210]

plt.figure(figsize=(8, 5))
barras = plt.bar(protocolos, latencia_ms)

plt.title("Latência Média entre R1 e R5")
plt.ylabel("Latência média (ms)")
plt.xlabel("Protocolo")

for barra, valor in zip(barras, latencia_ms):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height(),
        f"{valor:.3f} ms",
        ha="center",
        va="bottom"
    )

plt.ylim(0, 0.25)
plt.tight_layout()
plt.savefig(
    os.path.join(PASTA, "latencia_media_protocolos.png"),
    dpi=300
)
plt.close()


# ============================================================
# GRÁFICO 3 - QUANTIDADE DE ROTAS POR ROTEADOR
# ============================================================

roteadores = ["R1", "R2", "R3", "R4", "R5"]

rotas_rip = [8, 8, 7, 7, 8]
rotas_ospf = [8, 8, 7, 7, 8]
rotas_bgp = [4, 4, 4, 4, 4]

x = np.arange(len(roteadores))
largura = 0.25

plt.figure(figsize=(9, 5))

barras_rip = plt.bar(
    x - largura,
    rotas_rip,
    largura,
    label="RIP"
)

barras_ospf = plt.bar(
    x,
    rotas_ospf,
    largura,
    label="OSPF"
)

barras_bgp = plt.bar(
    x + largura,
    rotas_bgp,
    largura,
    label="BGP"
)

plt.title("Quantidade de Rotas por Roteador")
plt.ylabel("Quantidade de rotas")
plt.xlabel("Roteador")

plt.xticks(x, roteadores)
plt.ylim(0, 10)
plt.legend()

for barras in [barras_rip, barras_ospf, barras_bgp]:
    for barra in barras:
        altura = barra.get_height()

        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            f"{int(altura)}",
            ha="center",
            va="bottom"
        )

plt.tight_layout()
plt.savefig(
    os.path.join(PASTA, "quantidade_rotas_protocolos.png"),
    dpi=300
)
plt.close()


# ============================================================
# GRÁFICO 4 - TAXA DE TRÁFEGO DE CONTROLE
# ============================================================

# RIP:
# 328 bytes observados em 60 segundos
# (328 * 8) / 60 = 43.73 bit/s
#
# OSPF:
# 576 bytes observados em 60 segundos
# (576 * 8) / 60 = 76.80 bit/s
#
# BGP:
# 76 bytes de payload BGP observados em 130 segundos
# (76 * 8) / 130 = 4.68 bit/s

taxa_controle = [43.73, 76.80, 4.68]

plt.figure(figsize=(8, 5))
barras = plt.bar(protocolos, taxa_controle)

plt.title("Taxa Média de Tráfego de Controle Observado")
plt.ylabel("Taxa média (bit/s)")
plt.xlabel("Protocolo")

for barra, valor in zip(barras, taxa_controle):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height(),
        f"{valor:.2f} bit/s",
        ha="center",
        va="bottom"
    )

plt.ylim(0, 90)
plt.tight_layout()
plt.savefig(
    os.path.join(PASTA, "taxa_trafego_controle.png"),
    dpi=300
)
plt.close()


# ============================================================
# FINALIZAÇÃO
# ============================================================

print("Todos os gráficos foram gerados com sucesso.")
print(f"Arquivos salvos em: {PASTA}")
