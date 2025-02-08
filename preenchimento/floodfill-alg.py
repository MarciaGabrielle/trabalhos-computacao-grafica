import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import sys

# Aumenta o limite de recursão, se necessário (embora as formas menores reduzam o risco)
sys.setrecursionlimit(10**6)

def flood_fill_recursive(img_array, x, y, target_color, fill_color):
    # Verifica se o ponto está fora dos limites
    if x < 0 or x >= img_array.shape[1] or y < 0 or y >= img_array.shape[0]:
        return
    # Se o pixel não tem a cor alvo, não faz nada
    if img_array[y, x] != target_color:
        return
    
    # Preenche o pixel
    img_array[y, x] = fill_color
    
    # Chama recursivamente para os vizinhos
    flood_fill_recursive(img_array, x + 1, y, target_color, fill_color)  # direita
    flood_fill_recursive(img_array, x - 1, y, target_color, fill_color)  # esquerda
    flood_fill_recursive(img_array, x, y + 1, target_color, fill_color)  # abaixo
    flood_fill_recursive(img_array, x, y - 1, target_color, fill_color)  # acima

def draw_circle(img, xc, yc, r):
    """
    Desenha uma circunferência com borda preta na imagem usando o algoritmo do ponto médio.
    
    Parâmetros:
      - img: objeto PIL.Image.
      - xc, yc: coordenadas do centro.
      - r: raio da circunferência.
    
    Retorna a imagem modificada.
    """
    draw = ImageDraw.Draw(img)
    x = 0
    y = r
    d = 1 - r
    while y >= x:
        draw_circle_points(draw, xc, yc, x, y, fill=0)  # desenha com cor 0 (preto)
        x += 1
        if d < 0:
            d = d + 2 * x + 1
        else:
            y -= 1
            d = d + 2 * (x - y) + 1
    return img

def draw_circle_points(draw, xc, yc, x, y, fill):
    """
    Desenha os 8 pontos simétricos correspondentes a um ponto da circunferência.
    """
    points = [
        (xc + x, yc + y), (xc - x, yc + y),
        (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x),
        (xc + y, yc - x), (xc - y, yc - x)
    ]
    for point in points:
        draw.point(point, fill=fill)

def draw_rectangle(img, x1, y1, x2, y2):
    """
    Desenha um retângulo com borda preta na imagem.
    
    Parâmetros:
      - img: objeto PIL.Image.
      - (x1, y1): canto superior esquerdo.
      - (x2, y2): canto inferior direito.
    
    Retorna a imagem modificada.
    """
    draw = ImageDraw.Draw(img)
    draw.rectangle([x1, y1, x2, y2], outline=0)
    return img

def draw_polygon(img, points):
    """
    Desenha um polígono com borda preta na imagem a partir de uma lista de pontos.
    
    Parâmetros:
      - img: objeto PIL.Image.
      - points: lista de tuplas (x, y) dos vértices do polígono.
    
    Retorna a imagem modificada.
    """
    draw = ImageDraw.Draw(img)
    draw.polygon(points, outline=0)
    return img

def normalize_coordinates(points, padding=10):
    """
    Normaliza as coordenadas dos pontos para que fiquem todos positivos e com uma margem (padding).
    
    Retorna:
      - normalized_points: lista de pontos normalizados.
      - width, height: dimensões necessárias para a imagem.
    """
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)
    width = int(max_x - min_x + 2 * padding)
    height = int(max_y - min_y + 2 * padding)
    normalized_points = [(p[0] - min_x + padding, p[1] - min_y + padding) for p in points]
    return normalized_points, width, height

def find_seed_point(polygon, img_array):
    """
    Tenta encontrar um ponto interno (seed) para iniciar o preenchimento do polígono.
    
    Retorna (seed_x, seed_y) se encontrar um ponto com cor branca (255); caso contrário, retorna (None, None).
    """
    min_x = min(p[0] for p in polygon)
    max_x = max(p[0] for p in polygon)
    min_y = min(p[1] for p in polygon)
    max_y = max(p[1] for p in polygon)
    seed_x = (min_x + max_x) // 2
    seed_y = (min_y + max_y) // 2
    if img_array[seed_y, seed_x] == 255:
        return seed_x, seed_y
    else:
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if img_array[y, x] == 255:
                    return x, y
    return None, None

def main():
    # ========= Parte 1: Retângulo e Circunferência =========
    # Usamos uma imagem menor para evitar muitos níveis de recursão
    width, height = 150, 150
    img = Image.new('L', (width, height), 255)  # Fundo branco
    
    # Desenha uma circunferência e um retângulo com borda preta
    # A circunferência: centro em (75, 50) e raio 20
    img = draw_circle(img, 75, 50, 20)
    # O retângulo: canto superior esquerdo (40, 80) e inferior direito (110, 120)
    img = draw_rectangle(img, 40, 80, 110, 120)
    
    # Converte a imagem para um array NumPy
    img_array = np.array(img)
    
    # Preenche a área interna da circunferência
    # (O pixel seed deve estar dentro da área branca; neste caso, (75, 50))
    flood_fill_recursive(img_array, 75, 50, 255, 150)
    # Preenche a área interna do retângulo (por exemplo, (70, 100))
    flood_fill_recursive(img_array, 70, 100, 255, 150)
    
    # Exibe o resultado
    img_filled = Image.fromarray(img_array)
    plt.figure(figsize=(6,6))
    plt.imshow(img_filled, cmap="gray")
    plt.title("Recursive Flood Fill: Círculo e Retângulo")
    plt.axis("off")
    plt.show()
    
    # ========= Parte 2: Polígono 1 =========
    polygon1 = [(-15, -15), (0, -15), (8, -8), (15, -15),
                (30, -15), (30, 0), (8, 13), (-15, 0)]
    # Normaliza as coordenadas com um padding para caber na imagem
    norm_poly1, w1, h1 = normalize_coordinates(polygon1, padding=20)
    norm_poly1 = [(int(x), int(y)) for (x, y) in norm_poly1]
    
    img_poly1 = Image.new('L', (w1, h1), 255)
    img_poly1 = draw_polygon(img_poly1, norm_poly1)
    img_poly1_array = np.array(img_poly1)
    
    # Encontra um ponto seed dentro do polígono para iniciar o flood fill
    seed_x1, seed_y1 = find_seed_point(norm_poly1, img_poly1_array)
    if seed_x1 is not None and seed_y1 is not None:
        flood_fill_recursive(img_poly1_array, seed_x1, seed_y1, 255, 150)
    
    img_poly1_filled = Image.fromarray(img_poly1_array)
    plt.figure(figsize=(6,6))
    plt.imshow(img_poly1_filled, cmap="gray")
    plt.title("Recursive Flood Fill: Polígono 1")
    plt.axis("off")
    plt.show()
    
    # ========= Parte 3: Polígono 2 =========
    polygon2 = [(-20, -15), (5, -25), (30, -5), (26, 5), (-10, 10), (-5, -2)]
    norm_poly2, w2, h2 = normalize_coordinates(polygon2, padding=20)
    norm_poly2 = [(int(x), int(y)) for (x, y) in norm_poly2]
    
    img_poly2 = Image.new('L', (w2, h2), 255)
    img_poly2 = draw_polygon(img_poly2, norm_poly2)
    img_poly2_array = np.array(img_poly2)
    
    seed_x2, seed_y2 = find_seed_point(norm_poly2, img_poly2_array)
    if seed_x2 is not None and seed_y2 is not None:
        flood_fill_recursive(img_poly2_array, seed_x2, seed_y2, 255, 150)
    
    img_poly2_filled = Image.fromarray(img_poly2_array)
    plt.figure(figsize=(6,6))
    plt.imshow(img_poly2_filled, cmap="gray")
    plt.title("Recursive Flood Fill: Polígono 2")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
