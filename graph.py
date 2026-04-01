# graph.py — с оптимизацией графа состояний (объединение эквивалентных состояний)

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches
from collections import defaultdict


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


def optimize_state_graph(transitions):
    """
    Оптимизирует граф состояний, объединяя состояния с одинаковыми
    исходящими переходами. Не создает лишних циклов.
    """
    # Создаем копию словаря переходов
    opt_transitions = {}

    # Копируем все состояния
    for state, edges in transitions.items():
        opt_transitions[state] = {}
        for symbol, next_states in edges.items():
            if isinstance(next_states, list):
                opt_transitions[state][symbol] = next_states.copy()
            else:
                opt_transitions[state][symbol] = next_states

    # Группируем состояния по их исходящим переходам
    state_groups = defaultdict(list)

    for state in opt_transitions.keys():
        if state == 'Z':  # Не объединяем конечное состояние
            continue

        # Создаем ключ из исходящих переходов
        outgoing = []
        if state in opt_transitions:
            for symbol, next_states in opt_transitions[state].items():
                if isinstance(next_states, list):
                    for target in sorted(next_states):
                        outgoing.append((symbol, target))
                else:
                    outgoing.append((symbol, next_states))

        # Сортируем и преобразуем в кортеж
        key = tuple(sorted(outgoing))
        state_groups[key].append(state)

    # Создаем отображение для объединения состояний
    state_mapping = {}

    # Находим группы для объединения
    for group_states in state_groups.values():
        if len(group_states) > 1:
            # Выбираем первое состояние как основное
            main_state = group_states[0]
            for state in group_states[1:]:
                state_mapping[state] = main_state

    # Если нет состояний для объединения, возвращаем исходный граф
    if not state_mapping:
        return opt_transitions

    # Применяем отображение
    result = {}

    # Сначала переносим все состояния, которые не были объединены
    for state in opt_transitions.keys():
        if state in state_mapping:
            continue
        result[state] = {}
        for symbol, next_states in opt_transitions[state].items():
            if isinstance(next_states, list):
                # Заменяем целевые состояния
                new_targets = []
                for target in next_states:
                    new_target = state_mapping.get(target, target)
                    if new_target not in new_targets:
                        new_targets.append(new_target)
                result[state][symbol] = new_targets if len(new_targets) > 1 else new_targets[0]
            else:
                new_target = state_mapping.get(next_states, next_states)
                result[state][symbol] = new_target

    # Добавляем объединенные состояния
    for old_state, new_state in state_mapping.items():
        if new_state not in result:
            result[new_state] = {}

        # Переносим переходы из объединенного состояния
        if old_state in opt_transitions:
            for symbol, next_states in opt_transitions[old_state].items():
                if isinstance(next_states, list):
                    new_targets = []
                    for target in next_states:
                        new_target = state_mapping.get(target, target)
                        if new_target not in new_targets:
                            new_targets.append(new_target)

                    if symbol in result[new_state]:
                        existing = result[new_state][symbol]
                        if isinstance(existing, list):
                            for t in new_targets:
                                if t not in existing:
                                    existing.append(t)
                        else:
                            if existing not in new_targets:
                                new_targets.append(existing)
                            result[new_state][symbol] = new_targets
                    else:
                        result[new_state][symbol] = new_targets if len(new_targets) > 1 else new_targets[0]
                else:
                    new_target = state_mapping.get(next_states, next_states)
                    if symbol in result[new_state]:
                        existing = result[new_state][symbol]
                        if isinstance(existing, list):
                            if new_target not in existing:
                                existing.append(new_target)
                        else:
                            if existing != new_target:
                                result[new_state][symbol] = [existing, new_target]
                    else:
                        result[new_state][symbol] = new_target

    # Удаляем состояния, которые были объединены
    for old_state in state_mapping.keys():
        if old_state in result:
            del result[old_state]

    return result


def plot_state_graph(transitions, filename="state_graph.png", optimize=True):
    """
    Строит граф состояний

    Args:
        transitions: словарь переходов
        filename: имя файла для сохранения
        optimize: если True, выполняет оптимизацию (объединение эквивалентных состояний)
    """
    # Оптимизируем граф если нужно
    if optimize:
        transitions = optimize_state_graph(transitions)
        title_suffix = " (оптимизированный)"
    else:
        title_suffix = ""

    G = nx.DiGraph()
    edge_labels = {}  # (source, target) -> label

    for state, edges in transitions.items():
        for symbol, next_states in edges.items():
            # Убедимся, что next_states — список
            if isinstance(next_states, list):
                targets = next_states
            else:
                targets = [next_states]

            for target in targets:
                G.add_edge(state, target)

                # Собираем метки для каждого ребра (u, v)
                key = (state, target)
                if key in edge_labels:
                    if symbol not in edge_labels[key]:
                        edge_labels[key] += f"|{symbol}"
                else:
                    edge_labels[key] = symbol

    # Раскладка
    pos = nx.spring_layout(G, k=2.5, seed=42, iterations=100)

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

    # Рёбра с чёткими стрелками
    nx.draw_networkx_edges(
        G, pos,
        ax=ax,
        edge_color="gray",
        width=2.5,
        arrows=True,
        arrowstyle='-|>',
        arrowsize=30,
        connectionstyle='arc3,rad=0.1'
    )

    # Узлы
    nx.draw_networkx_nodes(
        G, pos,
        ax=ax,
        node_size=1800,
        node_color="lightblue",
        edgecolors="black",
        linewidths=1.5
    )

    # Метки узлов
    nx.draw_networkx_labels(
        G, pos,
        ax=ax,
        font_size=14,
        font_weight="bold"
    )

    # Метки рёбер
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels,
        ax=ax,
        font_size=12,
        font_color="darkred",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none"),
        rotate=False
    )

    # Добавляем информацию о количестве состояний
    if optimize:
        ax.set_title(f"Граф состояний (NFA){title_suffix}", fontsize=18, fontweight="bold")
        # Добавляем легенду с информацией об оптимизации
        info_text = f"Всего состояний: {G.number_of_nodes()} (было: {len(transitions) if 'transitions' in locals() else '?'})"
        ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    else:
        ax.set_title("Граф состояний (NFA)", fontsize=18, fontweight="bold")

    ax.axis("off")

    # Сохраняем
    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0.3)

    # Показываем с перетаскиванием
    draggable = DraggableGraph(
        G, pos, ax,
        edge_labels=edge_labels,
        title=f"Граф состояний (NFA){title_suffix}",
        node_size=1800,
        node_color="lightblue"
    )
    plt.show()
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
    edge_labels = {(u, v): '' for u, v in G.edges()}

    draggable = DraggableGraph(
        G, pos, ax,
        title="Граф переходов между характеристиками",
        node_size=1800, node_color="lightgreen"
    )

    plt.savefig(filename, dpi=200, bbox_inches='tight', pad_inches=0.5)
    plt.show()
    plt.close()