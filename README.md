# README

Este repositório contém três trabalhos relacionados à rasterização e preenchimento de formas em imagens digitais, implementados em Python utilizando bibliotecas como NumPy, PIL/Pillow e Matplotlib.

## Trabalho 1: Rasterização de Reta

Neste trabalho, foram explorados diferentes algoritmos para converter uma reta contínua em uma sequência de pixels, de forma a representar a reta em uma grade discreta. Os algoritmos implementados foram:

- **Método Analítico**: Utiliza diretamente a equação da reta (*y = mx + b*) para calcular os pixels, realizando arredondamentos para mapear os valores contínuos para inteiros.

- **Algoritmo DDA (Digital Differential Analyzer)**: Calcula incrementos constantes para *x* e *y* com base no maior delta entre as coordenadas, gerando os pontos da reta de forma incremental.

- **Algoritmo de Bresenham**: Utiliza apenas operações inteiras e um controle de erro acumulado para determinar quais pixels ativar, garantindo alta eficiência e precisão na aproximação da reta.

## Trabalho 2: Rasterização de Circunferência

Neste trabalho, foram aplicados algoritmos para desenhar círculos na tela, convertendo a definição contínua do círculo em uma sequência de pixels. Os métodos utilizados foram:

- **Equação Paramétrica**: Calcula os pontos da circunferência usando as equações:
  
  \[ x = x_c + r \cos(t) \quad \text{e} \quad y = y_c + r \sin(t) \]
  
  onde *t* varia de 0 a 360° (convertidos para radianos). Esse método gera uma lista de pontos que representa a circunferência.

- **Algoritmo de Bresenham para Círculos**: Uma extensão do algoritmo de Bresenham para linhas, adaptado para círculos. Ele utiliza um parâmetro de decisão para escolher, a cada passo, entre dois pixels candidatos, aproveitando a simetria do círculo para calcular os pontos dos 8 octantes.

## Trabalho 3: Preenchimento de Formas

Neste trabalho, o foco foi preencher internamente áreas delimitadas por bordas (como retângulos, círculos e polígonos). Os algoritmos utilizados foram:

- **Flood Fill Recursivo**: A partir de um ponto *seed* (dentro da área a preencher), o algoritmo recursivamente “espalha” a nova cor para os pixels vizinhos que possuem a cor alvo, preenchendo toda a área conectada.

- **Algoritmo de Varredura (Scanline) com Análise Geométrica**: Para cada linha da imagem, o algoritmo determina os intervalos que estão dentro da forma.
  
  - **Retângulo**: Percorre cada linha e preenche de *x_min* a *x_max*.
  - **Circunferência**: Para cada linha, utiliza a equação do círculo para calcular a interseção:
    
    \[ d_x = \sqrt{r^2 - (y - y_c)^2} \]
    
    e preenche o intervalo correspondente.
  - **Polígonos**: Calcula as interseções de cada linha com as arestas do polígono (utilizando interpolação linear), ordena essas interseções e preenche os intervalos internos.

---

Este repositório oferece uma abordagem prática e educacional para a rasterização e preenchimento de formas em imagens digitais, utilizando conceitos fundamentais da computação gráfica.
