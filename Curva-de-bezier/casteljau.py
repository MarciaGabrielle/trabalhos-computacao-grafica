import numpy as np
import matplotlib.pyplot as plt

def PMCurva(P0, P1, P2, P3):
    """
    Calcula os pontos intermediários da curva de Bézier usando o método de De Casteljau.
    Retorna os novos pontos para subdivisão.
    """
    # Primeira subdivisão
    P0xN1 = (P0 + P1) / 2
    P1xN1 = (P1 + P2) / 2
    P2xN1 = (P2 + P3) / 2
    
    # Segunda subdivisão
    P0xN2 = (P0xN1 + P1xN1) / 2
    P1xN2 = (P1xN1 + P2xN1) / 2
    
    # Terceira subdivisão (ponto na curva)
    P0xN3 = (P0xN2 + P1xN2) / 2
    
    return P0xN1, P1xN1, P2xN1, P0xN2, P1xN2, P0xN3

def casteljau_recursive(P0, P1, P2, P3, t, curve_points):
    """
    Algoritmo de De Casteljau recursivo para calcular pontos da curva de Bézier.
    """
    if t > 0.005:
        e = t / 2
        P0xN1, P1xN1, P2xN1, P0xN2, P1xN2, P0xN3 = PMCurva(P0, P1, P2, P3)
        casteljau_recursive(P0, P0xN1, P0xN2, P0xN3, e, curve_points)
        casteljau_recursive(P0xN3, P1xN2, P2xN1, P3, e, curve_points)
    else:
        curve_points.append(P0)

# Definir os pontos de controle
P0 = np.array([0, 0])
P1 = np.array([1, 2])
P2 = np.array([3, 3])
P3 = np.array([4, 0])         

# Criar a curva de Bézier via recursão
bezier_curve = []
casteljau_recursive(P0, P1, P2, P3, 1, bezier_curve)
bezier_curve = np.array(bezier_curve)

# Criar a figura
fig, ax = plt.subplots()
ax.set_xlim(-1, 5)
ax.set_ylim(-1, 4)
ax.set_title("Curva de Bézier - Algoritmo de Casteljau Recursivo")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Plotar o polígono de controle (em vermelho)
control_points = [P0, P1, P2, P3]
ax.plot([p[0] for p in control_points],
        [p[1] for p in control_points],
        'ro--', label="Pontos de Controle")

# -------------------------------
# Cálculo e plot dos pontos intermediários (em verde)
P0xN1, P1xN1, P2xN1, P0xN2, P1xN2, P0xN3 = PMCurva(P0, P1, P2, P3)

# Subdivisão 1 (liga P0xN1, P1xN1, P2xN1)
ax.plot([P0xN1[0], P1xN1[0], P2xN1[0]],
        [P0xN1[1], P1xN1[1], P2xN1[1]],
        'go--', label="Subdivisão 1")

# Subdivisão 2 (liga P0xN2, P1xN2)
ax.plot([P0xN2[0], P1xN2[0]],
        [P0xN2[1], P1xN2[1]],
        'go--', label="Subdivisão 2")

# Ponto resultante na curva (P0xN3)
ax.plot(P0xN3[0], P0xN3[1], 'go', label="Ponto na Curva")
# -------------------------------

# Plotar a curva de Bézier (em azul)
if len(bezier_curve) > 0:
    ax.plot(bezier_curve[:, 0], bezier_curve[:, 1], 'b-', lw=2, label="Curva de Bézier")

plt.legend()
plt.show()
