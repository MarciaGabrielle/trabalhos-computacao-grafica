import matplotlib.pyplot as plt
import numpy as np

def bresenham_circle(xc, yc, r):
    
    x = 0
    y = r
    p = 1 - r  # Parâmetro de decisão inicial

    points = []

    while x <= y:
        # Adiciona os pontos dos 8 octantes
        points.extend([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ])

        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * x - 2 * y + 5
            y -= 1

        x += 1

    return points

def plot_circle(points, xc, yc, r):
    
    # Determina o tamanho da grade
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    # Cria uma matriz para armazenar os pixels
    grid = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
    for x, y in points:
        grid[y - min_y][x - min_x] = 1  # Ativa os pixels

    # Plota os pixels na matriz
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap="Greys", origin="lower",
               extent=[min_x - 0.5, max_x + 0.5, min_y - 0.5, max_y + 0.5])

    # Plota a circunferência ideal
    circle = plt.Circle((xc, yc), r, color='blue', fill=False, linestyle='dashed')
    plt.gca().add_artist(circle)

    # Ajusta o gráfico
    plt.title("Rasterização de Circunferência - Algoritmo de Bresenham")
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

# Gera os pontos usando o algoritmo
circle_points = bresenham_circle(xc, yc, r)

# Plota a circunferência
plot_circle(circle_points, xc, yc, r)
