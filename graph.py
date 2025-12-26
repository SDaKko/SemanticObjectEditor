# graph.py — с ЧЁТКИМИ стрелками на всех рёбрах

import networkx as nx
import matplotlib.pyplot as plt


def plot_state_graph(transitions, filename="state_graph.png"):
    G = nx.DiGraph()
    edge_labels = {}

    for state, edges in transitions.items():
        for symbol, next_state in edges.items():
            G.add_edge(state, next_state)
            edge_labels[(state, next_state)] = symbol

    # Увеличиваем k — больше пространства
    pos = nx.spring_layout(G, k=2.2, seed=42, iterations=100)  # ← k больше

    plt.figure(figsize=(14, 10))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

    normal_edges = [(u, v) for (u, v) in G.edges() if u != v]
    if normal_edges:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=normal_edges,
            edge_color="gray",
            width=2.5,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=30,
            node_size=1500,
            connectionstyle='arc3,rad=0.1'
        )

    self_loops = [(u, v) for (u, v) in G.edges() if u == v]
    if self_loops:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=self_loops,
            connectionstyle='arc3,rad=0.6',  # ← как у характеристик
            edge_color="red",
            width=3.5,                      # ← как у характеристик
            arrows=True,
            arrowstyle='-|>',
            arrowsize=40                    # ← как у характеристик
        )

    nx.draw_networkx_nodes(
        G, pos,
        node_size=1500,
        node_color="lightblue",
        edgecolors="black",
        linewidths=1.5
    )
    nx.draw_networkx_labels(
        G, pos,
        font_size=16,
        font_weight="bold"
    )

    if edge_labels:
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels,
            font_size=12,
            font_color="darkred",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none")
        )

    plt.title("Граф состояний автомата", fontsize=18)
    plt.axis('off')
    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0.5)
    plt.close()


def plot_char_graph(dict_char, filename="char_graph.png"):
    G = nx.DiGraph()
    for char, next_chars in dict_char.items():
        for next_char in next_chars:
            G.add_edge(char, next_char)

    # Используем только spring_layout
    pos = nx.spring_layout(G, k=2.0, seed=42, iterations=100)

    plt.figure(figsize=(14, 10))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

    normal_edges = [(u, v) for (u, v) in G.edges() if u != v]
    if normal_edges:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=normal_edges,
            edge_color="gray",
            width=3,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=35,
            node_size=1800,
            connectionstyle='arc3,rad=0.1'
        )

    self_loops = [(u, v) for (u, v) in G.edges() if u == v]
    if self_loops:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=self_loops,
            connectionstyle='arc3,rad=0.6',
            edge_color="red",
            width=3.5,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=40
        )

    nx.draw_networkx_nodes(
        G, pos,
        node_size=1800,
        node_color="lightgreen",
        edgecolors="black",
        linewidths=1.5
    )
    nx.draw_networkx_labels(
        G, pos,
        font_size=16,
        font_weight="bold"
    )

    plt.title("Граф переходов между характеристиками", fontsize=18)
    plt.axis('off')
    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0.5)
    plt.close()