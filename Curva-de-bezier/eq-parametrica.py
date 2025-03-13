import numpy as np
import matplotlib.pyplot as plt

# Funções para calcular pontos intermediários da curva de Bézier
def bezier_quad(P0, P1, P2, t):
    """Curva de Bézier Quadrática"""
    return (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t ** 2 * P2

def bezier_cubic(P0, P1, P2, P3, t):
    """Curva de Bézier Cúbica"""
    return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3

# Definir pontos de controle
P0 = np.array([0, 0])
P1 = np.array([1, 2])
P2 = np.array([3, 3])
P3 = np.array([4, 0])         

# Gerar pontos da curva
t_values = np.linspace(0, 1, 100)
bezier_points = np.array([bezier_cubic(P0, P1, P2, P3, t) for t in t_values])

# Configurar a figura e os eixos
fig, ax = plt.subplots()
ax.set_xlim(-1, 5)
ax.set_ylim(-1, 4)
ax.set_title("Curva de Bézier - Equação Paramétrica")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Plotar os pontos de controle
ax.plot([P0[0], P1[0], P2[0], P3[0]], [P0[1], P1[1], P2[1], P3[1]], 'ro--', alpha=0.5, label="Pontos de Controle")

# Plotar a curva de Bézier
ax.plot(bezier_points[:, 0], bezier_points[:, 1], 'b-', lw=2, label="Curva de Bézier")

# Exibir a legenda
plt.legend()
plt.show()
