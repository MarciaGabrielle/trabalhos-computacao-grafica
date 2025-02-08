import matplotlib.pyplot as plt
import numpy as np

def parametric_circle(xc, yc, r):
    points = []
    for t in range(0, 360):  # Percorre os ângulos de 0 a 360 graus
        rad = np.radians(t)  # Converte para radianos
        x = xc + round(r * np.cos(rad))  # Equação paramétrica para x
        y = yc + round(r * np.sin(rad))  # Equação paramétrica para y
        points.append((x, y))
    return points

def plot_circle(points, xc, yc, r):
    
    # Determina os limites do gráfico
    min_x = xc - r - 1
    max_x = xc + r + 1
    min_y = yc - r - 1
    max_y = yc + r + 1

    # Cria uma matriz para representar os pixels
    grid = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
    for x, y in points:
        grid[y - min_y][x - min_x] = 1

    # Plota os pixels como uma matriz binária
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap="Greys", origin="lower",
               extent=[min_x - 0.5, max_x + 0.5, min_y - 0.5, max_y + 0.5])

    # Plota a circunferência ideal para comparação (em azul, traço pontilhado)
    circle = plt.Circle((xc, yc), r, color="blue", fill=False, linestyle="dashed")
    plt.gca().add_artist(circle)

    # Ajusta os eixos e o gráfico
    plt.title("Rasterização de Circunferência - Equação Paramétrica")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().set_xticks(np.arange(min_x, max_x + 1, 1))
    plt.gca().set_yticks(np.arange(min_y, max_y + 1, 1))
    plt.gca().set_xticks(np.arange(min_x - 0.5, max_x + 1, 1), minor=True)
    plt.gca().set_yticks(np.arange(min_y - 0.5, max_y + 1, 1), minor=True)
    plt.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()

# --------------------------
# Programa Principal
# --------------------------

# Parâmetros do círculo
xc, yc = 0, 0  # Centro
r = 50          # Raio

# Gera os pontos usando a equação paramétrica
circle_points = parametric_circle(xc, yc, r)

# [NOVO] Fazemos aqui o "print" de cada coordenada obtida
print("Coordenadas rasterizadas do círculo:")
for i, (x, y) in enumerate(circle_points):
    print(f"Ponto {i}: ({x}, {y})")

# Agora, plota a circunferência
plot_circle(circle_points, xc, yc, r)
