# graph.py — с ЧЁТКИМИ стрелками и DRAGGABLE NODES

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


class DraggableGraph:
    def __init__(self, G, pos, ax, edge_labels=None, title="Граф", node_size=1500, node_color="lightblue"):
        self.G = G
        self.pos = dict(pos)
        self.ax = ax
        self.edge_labels = edge_labels or {}
        self.node_size = node_size
        self.node_color = node_color
        self.ax.set_title(title, fontsize=18)
        self.ax.axis('off')

        # Отключаем стандартное масштабирование
        self.ax.set_navigate(False)

        # Рисуем граф
        self.draw_graph()

        # Состояние перетаскивания
        self.selected_node = None
        self.press = None

        # Подключаем события
        self.cid_press = self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_title(self.ax.get_title(), fontsize=18)
        self.ax.axis('off')

        # Разделяем обычные рёбра и петли
        normal_edges = [(u, v) for u, v in self.G.edges() if u != v]
        self_loops = [(u, v) for u, v in self.G.edges() if u == v]

        # Рисуем рёбра
        if normal_edges:
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=normal_edges,
                ax=self.ax,
                edge_color="gray",
                width=2.5,
                arrows=True,
                arrowstyle='-|>',
                arrowsize=30,
                node_size=self.node_size,
                connectionstyle='arc3,rad=0.1'
            )

        if self_loops:
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=self_loops,
                ax=self.ax,
                connectionstyle='arc3,rad=0.6',
                edge_color="red",
                width=3.5,
                arrows=True,
                arrowstyle='-|>',
                arrowsize=40
            )

        # Узлы и метки
        nx.draw_networkx_nodes(
            self.G, self.pos,
            ax=self.ax,
            node_size=self.node_size,
            node_color=self.node_color,
            edgecolors="black",
            linewidths=1.5
        )
        nx.draw_networkx_labels(
            self.G, self.pos,
            ax=self.ax,
            font_size=16,
            font_weight="bold"
        )

        if self.edge_labels:
            nx.draw_networkx_edge_labels(
                self.G, self.pos, self.edge_labels,
                ax=self.ax,
                font_size=12,
                font_color="darkred",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none")
            )

        self.ax.figure.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        # Находим ближайший узел
        for node, (x, y) in self.pos.items():
            radius = 0.02 * max(self.ax.get_xlim()[1] - self.ax.get_xlim()[0],
                                self.ax.get_ylim()[1] - self.ax.get_ylim()[0])
            if abs(event.xdata - x) < radius and abs(event.ydata - y) < radius:
                self.selected_node = node
                self.press = (event.xdata, event.ydata)
                break

    def on_motion(self, event):
        if self.selected_node is None or self.press is None or event.inaxes != self.ax:
            return
        dx = event.xdata - self.press[0]
        dy = event.ydata - self.press[1]
        self.pos[self.selected_node] = (self.pos[self.selected_node][0] + dx,
                                        self.pos[self.selected_node][1] + dy)
        self.press = (event.xdata, event.ydata)
        self.draw_graph()

    def on_release(self, event):
        self.selected_node = None
        self.press = None


def plot_state_graph(transitions, filename="state_graph.png"):
    G = nx.DiGraph()
    edge_labels = {}

    for state, edges in transitions.items():
        for symbol, next_state in edges.items():
            G.add_edge(state, next_state)
            edge_labels[(state, next_state)] = symbol

    pos = nx.spring_layout(G, k=2.2, seed=42, iterations=100)

    fig, ax = plt.subplots(figsize=(14, 10))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

    # Создаём интерактивный граф
    draggable = DraggableGraph(
        G, pos, ax, edge_labels=edge_labels,
        title="Граф состояний автомата",
        node_size=1500, node_color="lightblue"
    )

    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0.5)
    plt.show()  # Теперь интерактивно!
    plt.close()


def plot_char_graph(dict_char, filename="char_graph.png"):
    G = nx.DiGraph()
    for char, next_chars in dict_char.items():
        for next_char in next_chars:
            G.add_edge(char, next_char)

    pos = nx.spring_layout(G, k=2.0, seed=42, iterations=100)

    fig, ax = plt.subplots(figsize=(14, 10))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

    # Создаём интерактивный граф
    edge_labels = {(u, v): '' for u, v in G.edges()}  # Можно добавить метки, если нужно

    draggable = DraggableGraph(
        G, pos, ax,
        title="Граф переходов между характеристиками",
        node_size=1800, node_color="lightgreen"
    )

    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0.5)
    plt.show()
    plt.close()
