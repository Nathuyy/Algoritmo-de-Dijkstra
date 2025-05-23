import matplotlib.pyplot as plt
import networkx as nx
import heapq

grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

G = nx.DiGraph()
for u in grafo:
    for v, w in grafo[u].items():
        G.add_edge(u, v, weight=w)

pos = nx.spring_layout(G, seed=42)

def desenhar_grafo(distancias, atual=None, caminho=[], caminho_minimo=[]):
    plt.figure(figsize=(8, 6))
    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_colors = []
    edge_colors = []

    for node in G.nodes():
        if node == atual:
            node_colors.append("orange")  # Nó atual
        elif node in caminho_minimo:
            node_colors.append("green")  # Nó no caminho mínimo
        elif node in caminho:
            node_colors.append("lightgreen")  # Já visitados
        else:
            node_colors.append("lightblue")  # Ainda não visitados

    caminho_minimo_arestas = list(zip(caminho_minimo, caminho_minimo[1:]))
    for u, v in G.edges():
        if (u, v) in caminho_minimo_arestas:
            edge_colors.append("red")
        else:
            edge_colors.append("black")

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500,
            font_size=16, font_weight='bold', arrowsize=20, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14)

    titulo = f"Visitando: {atual}" if atual else "Caminho mínimo"
    plt.title(titulo, fontsize=16, pad=20)

    texto = "\n".join([f"{n}: {d if d < float('inf') else '∞'}" for n, d in distancias.items()])
    plt.gcf().text(0.01, 0.5, f"Distâncias:\n{texto}", fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def dijkstra_visual(grafo, inicio):
    distancias = {vertice: float('infinity') for vertice in grafo}
    distancias[inicio] = 0
    predecessores = {vertice: None for vertice in grafo}
    fila = [(0, inicio)]
    visitados = set()

    while fila:
        distancia_atual, vertice_atual = heapq.heappop(fila)
        if vertice_atual in visitados:
            continue
        visitados.add(vertice_atual)

        desenhar_grafo(distancias, atual=vertice_atual, caminho=visitados)

        for vizinho, peso in grafo[vertice_atual].items():
            if vizinho in visitados:
                continue
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                predecessores[vizinho] = vertice_atual
                heapq.heappush(fila, (nova_distancia, vizinho))

    return distancias, predecessores

def reconstruir_caminho(predecessores, inicio, fim):
    caminho = []
    atual = fim
    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]
    caminho.reverse()
    if caminho[0] == inicio:
        return caminho
    else:
        return []  

distancias, predecessores = dijkstra_visual(grafo, 'A')

destino = 'D'  

caminho_minimo = reconstruir_caminho(predecessores, 'A', destino)

if caminho_minimo:
    print(f"Caminho mínimo de A até {destino}: {' -> '.join(caminho_minimo)}")
    print(f"Distância total: {distancias[destino]}")
else:
    print(f"Não existe caminho de A até {destino}")

desenhar_grafo(distancias, atual=None, caminho=distancias.keys(), caminho_minimo=caminho_minimo)
