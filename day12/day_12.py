from dataclasses import dataclass, field
from pathlib import Path

MAX_DIST = 100000
S_E_REPLACEMENT = {"S": "a", "E": "z"}


@dataclass
class Node:
    id: tuple[int, int]
    visited: bool = False
    children: list[str] = field(default_factory=list)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return id.__hash__()


@dataclass
class Graph:
    nodes: dict[tuple[int, int], Node] = field(default_factory=dict)


def bfs(
    graph: Graph, start: tuple[int, int], ends: set[tuple[int, int]]
) -> dict[tuple[int, int] : int]:
    distances = {node.id: MAX_DIST for node in graph.nodes.values()}
    start_node = graph.nodes[start]

    queue = []
    start_node.visited = True
    distances[start_node.id] = 0
    queue.append(start_node)

    while len(queue):
        cur_node = queue.pop(0)
        for neighb in cur_node.children:
            neighb_node = graph.nodes[neighb]
            if not neighb_node.visited:
                distances[neighb_node.id] = distances[cur_node.id] + 1
                neighb_node.visited = True
                queue.append(neighb_node)
                if neighb in ends:
                    return distances

    print("End not found")
    return distances


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        input = fp.read()

    n = input.find("\n")
    m = len(input) // n
    matrix = input.replace("\n", "")

    # build graphs
    start, end = None, None
    ends_part_2 = set()
    graph_part_1, graph_part_2 = Graph(), Graph()

    for i in range(m):
        for j in range(n):
            el = matrix[i * n + j]
            if el == "S":
                start = (i, j)
            elif el == "E":
                end = (i, j)
            el = S_E_REPLACEMENT.get(el, el)
            if el == "a":
                ends_part_2.add((i, j))

            neighbours = []
            if i != 0:
                neighbours.append((i - 1, j))
            if j != 0:
                neighbours.append((i, j - 1))
            if i != m - 1:
                neighbours.append((i + 1, j))
            if j != n - 1:
                neighbours.append((i, j + 1))

            children_part_1, children_part_2 = [], []
            for neighbour in neighbours:
                neighbour_el = matrix[neighbour[0] * n + neighbour[1]]
                neighbour_el = S_E_REPLACEMENT.get(neighbour_el, neighbour_el)
                slope = ord(neighbour_el) - ord(el)

                if slope <= 1:
                    children_part_1.append(neighbour)
                if slope == -1 or slope == 0 or slope > 1:
                    children_part_2.append(neighbour)

            graph_part_1.nodes[(i, j)] = Node((i, j), children=children_part_1)
            graph_part_2.nodes[(i, j)] = Node((i, j), children=children_part_2)

    # part 1
    distances = bfs(graph_part_1, start, {end})
    print(f"{distances[end]=}")

    # part 2
    distances = bfs(graph_part_2, end, ends_part_2)
    shortest_distance = min(distances[node] for node in ends_part_2)
    print(f"{shortest_distance=}")
