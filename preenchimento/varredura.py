import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import sys

# Opcional: aumenta o limite de recursão (não é necessário para o método de varredura)
sys.setrecursionlimit(10**6)

def fill_rectangle_scanline(arr, x_min, y_min, x_max, y_max, fill_color):
    for y in range(y_min, y_max + 1):
        if y < 0 or y >= arr.shape[0]:
            continue  # ignora linhas fora da imagem
        # Garante que os valores de x estejam dentro dos limites da imagem
        x1 = max(x_min, 0)
        x2 = min(x_max, arr.shape[1] - 1)
        # Como já passamos coordenadas internas, podemos preencher diretamente
        arr[y, x1:x2 + 1] = fill_color

def fill_circle_scanline(arr, xc, yc, R, fill_color):
    for y in range(int(yc - R), int(yc + R) + 1):
        if y < 0 or y >= arr.shape[0]:
            continue  # ignora linhas fora da imagem
        dy = y - yc
        dx = int(np.sqrt(R * R - dy * dy))
        x_min = int(xc - dx)
        x_max = int(xc + dx)
        # Ajusta os limites horizontais para a imagem
        x_min = max(x_min, 0)
        x_max = min(x_max, arr.shape[1] - 1)
        for x in range(x_min, x_max + 1):
            # Preenche apenas se o pixel não for parte da borda (valor 0)
            if arr[y, x] != 0:
                arr[y, x] = fill_color

def fill_polygon_scanline(arr, polygon, fill_color):
    n = len(polygon)
    y_min = min(y for (x, y) in polygon)
    y_max = max(y for (x, y) in polygon)
    for y in range(y_min, y_max + 1):
        intersections = []
        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]
            # Ignora arestas horizontais
            if y1 == y2:
                continue
            # Define o lado inferior e superior da aresta
            if y1 < y2:
                y_low, y_high = y1, y2
                x_low, x_high = x1, x2
            else:
                y_low, y_high = y2, y1
                x_low, x_high = x2, x1
            # A interseção ocorre se y estiver entre y_low (inclusive) e y_high (exclusiva)
            if y_low <= y < y_high:
                # Interpolação linear para determinar a coordenada x de interseção
                x_int = x_low + (y - y_low) * (x_high - x_low) / (y_high - y_low)
                intersections.append(x_int)
        intersections.sort()
        # Preenche os intervalos entre pares de interseções
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start = int(np.ceil(intersections[i]))
                x_end = int(np.floor(intersections[i + 1]))
                for x in range(x_start, x_end + 1):
                    if arr[y, x] != 0:  # não sobrescreve a borda
                        arr[y, x] = fill_color

def normalize_coordinates(points, padding=10):
    """
    Normaliza as coordenadas de um conjunto de pontos para que fiquem todos positivos
    e com uma margem (padding).
    
    Retorna:
      - normalized_points: lista de pontos normalizados
      - width, height: dimensões necessárias para a imagem
    """
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)
    width = int(max_x - min_x + 2 * padding)
    height = int(max_y - min_y + 2 * padding)
    normalized_points = [(p[0] - min_x + padding, p[1] - min_y + padding) for p in points]
    return normalized_points, width, height

def main():
    # Tamanho da imagem (usado para retângulo e circunferência)
    img_size = (300, 300)
    
    # ========= Retângulo =========
    img_rect = Image.new('L', img_size, 255)  # Fundo branco
    draw_rect = ImageDraw.Draw(img_rect)
    # Define as coordenadas do retângulo (outline)
    # Alterado para obter um retângulo (não um quadrado)
    rect_x1, rect_y1 = 50, 50
    rect_x2, rect_y2 = 250, 180  # largura maior que a altura
    draw_rect.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline=0)  # Borda preta
    arr_rect = np.array(img_rect)
    # Preenche o interior (excluindo a borda)
    fill_rectangle_scanline(arr_rect, rect_x1 + 1, rect_y1 + 1, rect_x2 - 1, rect_y2 - 1, fill_color=150)
    img_rect_filled = Image.fromarray(arr_rect)
    
    # ========= Circunferência =========
    img_circle = Image.new('L', img_size, 255)
    draw_circle_outline = ImageDraw.Draw(img_circle)
    # Define centro e raio da circunferência
    xc, yc, R = 150, 150, 100
    draw_circle_outline.ellipse([xc - R, yc - R, xc + R, yc + R], outline=0)  # Borda preta
    arr_circle = np.array(img_circle)
    fill_circle_scanline(arr_circle, xc, yc, R, fill_color=150)
    img_circle_filled = Image.fromarray(arr_circle)
    
    # ========= Polígono 1 =========
    polygon1 = [(-15, -15), (0, -15), (8, -8), (15, -15),
                (30, -15), (30, 0), (8, 13), (-15, 0)]
    # Normaliza as coordenadas para que fiquem dentro de uma imagem
    norm_poly1, w1, h1 = normalize_coordinates(polygon1, padding=20)
    norm_poly1 = [(int(x), int(y)) for (x, y) in norm_poly1]
    img_poly1 = Image.new('L', (w1, h1), 255)
    draw_poly1 = ImageDraw.Draw(img_poly1)
    draw_poly1.polygon(norm_poly1, outline=0)
    arr_poly1 = np.array(img_poly1)
    fill_polygon_scanline(arr_poly1, norm_poly1, fill_color=150)
    img_poly1_filled = Image.fromarray(arr_poly1)
    
    # ========= Polígono 2 =========
    polygon2 = [(-20, -15), (5, -25), (30, -5), (26, 5), (-10, 10), (-5, -2)]
    norm_poly2, w2, h2 = normalize_coordinates(polygon2, padding=20)
    norm_poly2 = [(int(x), int(y)) for (x, y) in norm_poly2]
    img_poly2 = Image.new('L', (w2, h2), 255)
    draw_poly2 = ImageDraw.Draw(img_poly2)
    draw_poly2.polygon(norm_poly2, outline=0)
    arr_poly2 = np.array(img_poly2)
    fill_polygon_scanline(arr_poly2, norm_poly2, fill_color=150)
    img_poly2_filled = Image.fromarray(arr_poly2)
    
    # ========= Plotando os Resultados =========
    plt.figure(figsize=(12, 12))
    
    plt.subplot(2, 2, 1)
    plt.imshow(img_rect_filled, cmap="gray")
    plt.title("Retângulo Preenchido (Scanline)")
    plt.axis("off")
    
    plt.subplot(2, 2, 2)
    plt.imshow(img_circle_filled, cmap="gray")
    plt.title("Circunferência Preenchida (Scanline)")
    plt.axis("off")
    
    plt.subplot(2, 2, 3)
    plt.imshow(img_poly1_filled, cmap="gray")
    plt.title("Polígono 1 Preenchido (Scanline)")
    plt.axis("off")
    
    plt.subplot(2, 2, 4)
    plt.imshow(img_poly2_filled, cmap="gray")
    plt.title("Polígono 2 Preenchido (Scanline)")
    plt.axis("off")
    
    plt.show()

if __name__ == "__main__":
    main()
