import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Definição da janela de recorte
xmin, ymin, xmax, ymax = 100, 100, 400, 400

# Definição dos polígonos
poligonos = {
    "a": [[200, 200], [200, 500], [500, 200]],
    "b": [[90, 210], [230, 210], [280, 330], [160, 410], [40, 330]],
    "c": [[150, 100], [150, 150], [200, 150], [200, 200], [300, 200], [300, 150], 
          [350, 150], [350, 100], [350, 50], [300, 50], [300, 0], [200, 0], 
          [200, 50], [150, 50]],
    "d": [[120, 320], [120, 480], [380, 480], [380, 340], [300, 340], 
          [300, 410], [200, 410], [200, 320]]
}

# Função para aumentar o tamanho do polígono proporcionalmente
def aumentar_proporcionalmente(poligono, fator):
    centro_x = np.mean([p[0] for p in poligono])
    centro_y = np.mean([p[1] for p in poligono])
    
    novo_poligono = [
        [(x - centro_x) * fator + centro_x, (y - centro_y) * fator + centro_y] 
        for x, y in poligono
    ]
    
    return novo_poligono

poligonos["b"] = aumentar_proporcionalmente(poligonos["b"], 1.5)  # Aumenta 50%

# Funções para recorte do polígono
def inside(point, clip_edge):
    x, y = point
    edge_x1, edge_y1, edge_x2, edge_y2 = clip_edge
    return (x >= edge_x1 if edge_x1 == xmin else x <= edge_x1) if edge_x1 == edge_x2 else (y >= edge_y1 if edge_y1 == ymin else y <= edge_y1)

def intersection(p1, p2, clip_edge):
    x1, y1 = p1
    x2, y2 = p2
    edge_x1, edge_y1, edge_x2, edge_y2 = clip_edge

    if edge_x1 == edge_x2:
        x_int = edge_x1
        m = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        y_int = y1 + m * (x_int - x1)
    else:
        y_int = edge_y1
        m = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        x_int = x1 + (y_int - y1) / m if m != 0 else x1

    return (x_int, y_int)

def clip_polygon(polygon, clip_rect):
    x_min, x_max, y_min, y_max = clip_rect
    clip_edges = [
        (x_min, y_min, x_min, y_max),  # Esquerda
        (x_min, y_max, x_max, y_max),  # Superior
        (x_max, y_max, x_max, y_min),  # Direita
        (x_max, y_min, x_min, y_min)   # Inferior
    ]

    clipped_polygon = polygon[:]
    for clip_edge in clip_edges:
        new_polygon = []
        prev_point = clipped_polygon[-1]
        for curr_point in clipped_polygon:
            if inside(curr_point, clip_edge):
                if not inside(prev_point, clip_edge):
                    intersec = intersection(prev_point, curr_point, clip_edge)
                    new_polygon.append(intersec)
                new_polygon.append(curr_point)
            elif inside(prev_point, clip_edge):
                intersec = intersection(prev_point, curr_point, clip_edge)
                new_polygon.append(intersec)
            prev_point = curr_point
        clipped_polygon = new_polygon

    return clipped_polygon

# Lista para armazenar os polígonos recortados
poligonos_recortados = {chave: clip_polygon(poligono, (xmin, xmax, ymin, ymax)) for chave, poligono in poligonos.items()}
#print(poligonos_recortados)


print("\nPolígonos Recortados:")
for chave, poligono in poligonos_recortados.items():
    print(f"\n🔹 Polígono '{chave}':")
    for i, ponto in enumerate(poligono):
        print(f"  P{i}: {ponto}")


# Cores para os polígonos
cores_iniciais = {'a': 'green', 'b': 'red', 'c': 'yellow', 'd': 'pink'}
cores_finais = {'a': 'green', 'b': 'red', 'c': 'yellow', 'd': 'pink'}

# Criando animação para cada polígono em telas separadas
def animate_poligono(nome):
    poligono = poligonos[nome]
    poligono_recortado = poligonos_recortados[nome]
    
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        ax.set_xlim(-50, 550)
        ax.set_ylim(-50, 550)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

        # Desenhar a área de recorte
        ax.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], 'k-', linewidth=2, label="Região de Recorte")
        
        cor = cores_iniciais[nome] if frame == 0 else cores_finais[nome]
        if frame == 0:
            # Desenha o polígono original **com borda preta**
            poligono_x, poligono_y = zip(*poligono + [poligono[0]])
            ax.fill(poligono_x, poligono_y, facecolor=cor, edgecolor='black', linewidth=2, alpha=0.7, label=f'Polígono {nome.upper()}')
        elif frame == 1:
            # Desenha o polígono recortado **com borda preta**
            if poligono_recortado:
                clipped_x, clipped_y = zip(*poligono_recortado + [poligono_recortado[0]])
                ax.fill(clipped_x, clipped_y, facecolor=cor, edgecolor='black', linewidth=2, alpha=0.7, label=f'Recortado {nome.upper()}')

        ax.legend()

    ani = animation.FuncAnimation(fig, update, frames=2, interval=5000, repeat=False)
    plt.show()

# Executar animação para cada polígono separadamente
for nome in poligonos.keys():
    animate_poligono(nome)
