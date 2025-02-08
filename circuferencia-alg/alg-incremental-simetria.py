import matplotlib.pyplot as plt
import numpy as np
import math

def incremental_circle_with_symmetry(xc, yc, r):
   
    points = []
    theta_step = 1 / r  # Incremento angular (1 / r)
    theta = 0

    # Calcula os pontos para 1/8 da circunferência
    while theta <= math.pi / 4:
        x = round(r * math.cos(theta))
        y = round(r * math.sin(theta))
        points.append((x, y))
        theta += theta_step

    # Espelha os pontos para os octantes restantes
    symmetric_points = []
    for x, y in points:
        symmetric_points.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ])

    return symmetric_points

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

    # Ajusta os eixos e o gráfico
    plt.title("Rasterização de Circunferência - Algoritmo Incremental com Simetria")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().set_xticks(np.arange(min_x, max_x + 1, 1))
    plt.gca().set_yticks(np.arange(min_y, max_y + 1, 1))
    plt.gca().set_xticks(np.arange(min_x - 0.5, max_x + 1, 1), minor=True)
    plt.gca().set_yticks(np.arange(min_y - 0.5, max_y + 1, 1), minor=True)
    plt.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()

# Parâmetros do círculo
xc, yc = 0, 0  # Centro
r = 50  # Raio

# Gera os pontos usando o Algoritmo Incremental com Simetria
circle_points = incremental_circle_with_symmetry(xc, yc, r)

# Plota a circunferência
plot_circle(circle_points, xc, yc, r)
