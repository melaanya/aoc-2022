from dataclasses import dataclass, field
from collections import defaultdict, deque
from pathlib import Path
import re


@dataclass(order=True)
class Node:
    id: str = field(compare=False)
    flow_rate: int
    children: list[str] = field(compare=False)
    visited: bool = False


def get_distances(graph: dict[str, Node]) -> dict[str, dict[str, float]]:
    """Implements Floyd-Warshall algorithm."""
    distances = {
        x: {
            y: 1 if y in graph[x].children else 0 if x == y else float("+inf")
            for y in graph
        }
        for x in graph
    }
    for k in graph:
        for i in graph:
            for j in graph:
                distances[i][j] = min(
                    distances[i][j], distances[i][k] + distances[k][j]
                )
    return distances


def find_max_cost(
    node: str,
    graph: dict[str, Node],
    distances: dict[str, dict[str, float]],
    minutes_left: int,
) -> int:
    """Implements BFS to find max cost path."""
    queue = deque()
    queue.append((node, 0, minutes_left, frozenset()))

    path_best_flow = defaultdict(int)
    while len(queue):
        node, total_flow, minutes_left, vertices = queue.popleft()
        path_best_flow[vertices] = max(total_flow, path_best_flow[vertices])

        for neighb_node in distances:
            minutes_go_open = minutes_left - distances[node][neighb_node] - 1
            if (
                graph[neighb_node].flow_rate != 0
                and not neighb_node in vertices
                and minutes_go_open > 0
            ):
                cur_flow = total_flow + graph[neighb_node].flow_rate * minutes_go_open
                s = set(vertices)
                s.add(neighb_node)
                queue.append((neighb_node, cur_flow, minutes_go_open, frozenset(s)))
    return path_best_flow


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.read().splitlines()

    graph = {}
    for line in lines:
        valve_from, *valve_to = re.findall("[A-Z]{2}", line)
        flow_rate = int(re.search("-?\d+", line).group())
        graph[valve_from] = Node(valve_from, flow_rate, valve_to)

    distances = get_distances(graph)

    # part 1
    minutes_left = 30
    path_to_flow = find_max_cost("AA", graph, distances, minutes_left)
    max_flow = max(path_to_flow.values())
    print(f"{max_flow=}")

    # part 2
    minutes_left = 26
    path_to_flow = find_max_cost("AA", graph, distances, minutes_left)
    best_sum = 0
    for left_path, left_count in path_to_flow.items():
        for right_path, right_count in path_to_flow.items():
            if not left_path & right_path:
                best_sum = max(best_sum, left_count + right_count)

    print(f"{best_sum=}")
