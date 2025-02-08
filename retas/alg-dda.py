import matplotlib.pyplot as plt
import numpy as np

def draw_line_dda(x1, y1, x2, y2):
    # Calcula os deltas
    dx = x2 - x1
    dy = y2 - y1

    # Determina o número de passos
    steps = int(max(abs(dx), abs(dy)))  # O maior delta determina os passos

    # Calcula os incrementos em cada direção
    x_inc = dx / steps
    y_inc = dy / steps

    # Lista para armazenar os pixels
    pixels = []

    # Valores iniciais
    x, y = x1, y1

    # Itera para determinar os pixels
    for _ in range(steps + 1):
        pixels.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return pixels

def plot_pixels_with_ideal_line(pixels, x1, y1, x2, y2, title="Rasterização de Linha - Método DDA"):
    # Determinar o tamanho da grade
    min_x = min(p[0] for p in pixels)
    min_y = min(p[1] for p in pixels)
    max_x = max(max(x for x, y in pixels), x2) + 1
    max_y = max(max(y for x, y in pixels), y2) + 1

    # Criar a matriz de pixels
    grid = np.zeros((max_y - min_y, max_x - min_x))
    for x, y in pixels:
        grid[y - min_y][x - min_x] = 1  # Ativar o pixel correspondente

    # Plotar os pixels com ajustes no extent
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap="Greys", origin="lower", extent=[min_x - 0.5, max_x - 0.5, min_y - 0.5, max_y - 0.5])

    # Plotar a linha ideal
    x_ideal = np.linspace(x1, x2, 1000)
    y_ideal = y1 + (y2 - y1) * (x_ideal - x1) / (x2 - x1)  # Fórmula da reta
    plt.plot(x_ideal, y_ideal, color="green", label="Reta Ideal")

    # Ajustar o gráfico
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.xticks(np.arange(min_x, max_x, 1))
    plt.yticks(np.arange(min_y, max_y, 1))
    plt.gca().set_xticks(np.arange(min_x - 0.5, max_x, 1), minor=True)
    plt.gca().set_yticks(np.arange(min_y - 0.5, max_y, 1), minor=True)
    plt.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend()
    plt.show()

# Exemplo de uso
x1, y1 = 10, 10
x2, y2 = 5, 5  # Exemplo do slide
pixels_dda = draw_line_dda(x1, y1, x2, y2)
plot_pixels_with_ideal_line(pixels_dda, x1, y1, x2, y2)
