import matplotlib.pyplot as plt
import numpy as np

def bresenham_line_general(x0, y0, x1, y1):
    """
    Bresenham 'genérico' para desenhar retas em qualquer octante.
    Retorna uma lista de (x, y) de todos os pixels da reta.
    """
    pixels = []

    # deltas absolutos
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    # determinar direção (sinal) de cada eixo
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    # erro inicial
    err = dx - dy
    
    x, y = x0, y0
    
    while True:
        pixels.append((x, y))
        
        # Se chegamos ao destino, paramos
        if x == x1 and y == y1:
            break
        
        # Calcula o "erro dobrado"
        e2 = 2 * err
        
        # Se e2 > -dy, andamos no eixo x
        if e2 > -dy:
            err -= dy
            x += sx

        # Se e2 < dx, andamos também no eixo y
        if e2 < dx:
            err += dx
            y += sy

    return pixels

def plot_pixels_with_ideal_line(pixels, x0, y0, x1, y1, title="Bresenham (Genérico)"):
    # Determinar o tamanho da grade
    min_x = min(min(p[0] for p in pixels), x0, x1)
    min_y = min(min(p[1] for p in pixels), y0, y1)
    max_x = max(max(p[0] for p in pixels), x0, x1) + 1
    max_y = max(max(p[1] for p in pixels), y0, y1) + 1

    # Criar a matriz de pixels
    grid = np.zeros((max_y - min_y, max_x - min_x))
    for x, y in pixels:
        grid[y - min_y][x - min_x] = 1  # Ativar o pixel correspondente

    # Plotar os pixels como imagem
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap="Greys", origin="lower",
               extent=[min_x - 0.5, max_x - 0.5, min_y - 0.5, max_y - 0.5])

    # Plotar a linha ideal (contínua)
    x_ideal = np.linspace(x0, x1, 1000)
    # evitar divisão por zero se x1 == x0
    if x1 != x0:
        y_ideal = y0 + (y1 - y0) * (x_ideal - x0) / (x1 - x0)
    else:
        # reta vertical
        x_ideal = np.full_like(x_ideal, x0)
        y_ideal = np.linspace(y0, y1, 1000)
    
    plt.plot(x_ideal, y_ideal, color="green", label="Linha Ideal")

    # Ajustar o gráfico
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.xticks(np.arange(min_x, max_x + 1))
    plt.yticks(np.arange(min_y, max_y + 1))
    plt.gca().set_xticks(np.arange(min_x - 0.5, max_x + 0.5), minor=True)
    plt.gca().set_yticks(np.arange(min_y - 0.5, max_y + 0.5), minor=True)
    plt.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend()
    plt.show()

# -------------- TESTES -------------- #

# 1) Primeiro octante: inclinação 0 <= m <= 1
#    Ex: (0,0) -> (5,2)
pixels = bresenham_line_general(0, 0, 3, 7)
plot_pixels_with_ideal_line(pixels, 0, 0, 3, 7, "Bresenham General - Octante 1")

# 2) Inclinação > 1: Ex: (0,0) -> (3,7)
pixels = bresenham_line_general(10, 10, 5, 5)
plot_pixels_with_ideal_line(pixels, 10, 10, 5, 5, "Bresenham - Reta com inclinação negativa")

# 3) Reta decrescente (m negativo): Ex: (0,5) -> (5,0)
pixels = bresenham_line_general(0, 5, 5, 0)
plot_pixels_with_ideal_line(pixels, 0, 5, 5, 0, "Bresenham General - m < 0")

# 4) Reta invertida (x1 < x0)
pixels = bresenham_line_general(10, 4, 3, 1)
plot_pixels_with_ideal_line(pixels, 10, 4, 3, 1, "Bresenham General - X invertido")

# 5) Reta vertical
pixels = bresenham_line_general(2, 2, 2, 8)
plot_pixels_with_ideal_line(pixels, 2, 2, 2, 8, "Bresenham General - Vertical")
