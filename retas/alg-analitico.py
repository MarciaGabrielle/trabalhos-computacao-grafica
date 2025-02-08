import matplotlib.pyplot as plt
import numpy as np

def draw_line_analytic(x1, y1, x2, y2):
    # Se x1 > x2, inverte os pontos
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    dx = x2 - x1
    dy = y2 - y1
    
    # Trata reta vertical (dx=0) para evitar divisão por zero
    if dx == 0:
        pixels = []
        step = 1 if y2 >= y1 else -1
        for y in range(y1, y2 + step, step):
            pixels.append((x1, y))
        return pixels

    m = dy / dx  # Inclinação
    b = y1 - m * x1

    pixels = []
    for x in range(x1, x2 + 1):
        y = m * x + b
        pixels.append((x, round(y)))
    return pixels

def plot_pixels_with_ideal_line(pixels, x1, y1, x2, y2, title="Rasterização de Linha - Método Analítico"):
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

# Exemplo
x1, y1 = 10, 10
x2, y2 = 5, 5
pixels_analytic = draw_line_analytic(x1, y1, x2, y2)
plot_pixels_with_ideal_line(pixels_analytic, x1, y1, x2, y2)


x3, y3 = 0, 0
x4, y4 = 7, 3
pixels_analytic = draw_line_analytic(x3, y3, x4, y4)
plot_pixels_with_ideal_line(pixels_analytic, x3, y3, x4, y4)