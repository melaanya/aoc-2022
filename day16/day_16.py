from dataclasses import dataclass, field
from collections import deque
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
    node: str, graph: dict[str, Node], distances: dict[str, dict[str, float]]
) -> int:
    """Implements BFS to find max cost path."""
    queue = deque()
    queue.append((node, 0, 30, set([node])))

    max_flow = float("-inf")
    while len(queue):
        node, total_flow, minutes_left, vertices = queue.popleft()
        max_flow = max(total_flow, max_flow)

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
                queue.append((neighb_node, cur_flow, minutes_go_open, s))
    return max_flow


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
    flow_rate = 0
    minutes_left = 30
    max_flow = find_max_cost("AA", graph, distances)
    print(f"{max_flow=}")
