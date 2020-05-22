from typing import Dict, List, Optional, Tuple
from collections import deque


def bfs(graph: Dict[str, List[str]], start_node: str) -> List[str]:
    """
    Breadth-first search.

    References
    ----------
    https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
    """
    visited = [start_node]
    queue = deque([start_node])

    while queue:  # FIFO = first in, first out
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    return visited


def dfs(graph: Dict[str, List[str]], start_node: str) -> List[str]:
    """
    Depth-first search.

    References
    ----------
    https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode
    """
    visited = []
    stack = [start_node]

    while stack:  # LIFO = last in, first out
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            for neighbor in graph[node]:
                stack.append(neighbor)

    return visited


def dfs_recursive(graph: Dict[str, List[str]], start_node: str) -> List[str]:
    """
    Depth-first search (recursive implementation).

    References
    ----------
    https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode
    """
    visited = []

    def dfs_aux(node: str) -> List[str]:
        visited.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_aux(neighbor)
        return visited

    return dfs_aux(start_node)


def build_path(dest_src: Dict[str, str], start_node: str, end_node: str
             ) -> List[str]:
    """
    Build path from a sequence of destination --> source.
    """
    if not dest_src:
        return []

    path = deque()
    while end_node != start_node:
        path.appendleft(end_node)
        end_node = dest_src[end_node]
    if path:
        path.appendleft(start_node)

    return list(path)


def shortest_path_bfs(graph: Dict[str, List[str]],
                      start_node: str,
                      end_node: Optional[str] = None
                     ) -> Dict[str, str]:
    """
    Breadth-first search to find the shortest path between 2 nodes in an
    unweighted graph. Special case of Dijkstra's algorithm.

    Modification of `bfs` to return the source --> destination nodes and to stop
    as soon as the end node is found.
    """
    if end_node:
        assert end_node in graph, f'`end_node` "{end_node:s}" not found in the graph'
    
    visited = [start_node]
    queue = deque([start_node])
    dest_src = {}

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                dest_src[neighbor] = node
                visited.append(neighbor)
                queue.append(neighbor)
            if end_node and (neighbor == end_node):
                return dest_src
    if end_node:  # end node was not found
        raise ValueError('Path was not found.')
    else:  # end node was not given
        return dest_src


def shortest_path(graph: Dict[str, List[str]], start_node: str, end_node: str
                 ) -> List[str]:
    """
    Find the shortest path between 2 nodes in an unweighted graph.
    """
    dest_src = shortest_path_bfs(graph, start_node, end_node)
    return build_path(dest_src, start_node, end_node)


def dict_is_subset(small: dict, large: dict) -> bool:
    small_dict_items = small.items()
    large_dict_items = large.items()
    return all(item in large_dict_items for item in small_dict_items)


def dijkstra(graph: Dict[str, Dict[str, int]], start_node: str
            ) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Use Dijkstra's algorithm to find the shortest path from a starting node.
    
    References
    ----------
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    """
    assert start_node in graph, f'`start_node` "{start_node:s}" not found in the graph'

    # Initialize
    inf = float('inf')
    unvisited_nodes = {n for n, d in graph.items() if d}  # only connected nodes
    dist = {n: inf for n in unvisited_nodes}
    dist[start_node] = 0
    dest_src = {}

    while unvisited_nodes:

        # Find the unvisited node with smallest distance
        min_dist = inf
        for n in unvisited_nodes:
            d = dist[n]
            if d < min_dist:
                node, min_dist = n, d

        unvisited_nodes.remove(node)

        # Update the distances if they are smaller than the current value
        for neighbor, length in graph[node].items():
            test_path = dist[node] + length
            if test_path < dist[neighbor]:
                dist[neighbor] = test_path
                dest_src[neighbor] = node

    return dist, dest_src


# ==============================================================================
# Unit tests
# ==============================================================================

assert build_path({'B': 'A'}, 'A', 'B') == ['A', 'B']
assert build_path({'B': 'A', 'C': 'B', 'D': 'C'}, 'A', 'D') == ['A', 'B', 'C', 'D']
# A --> B --> C --> D
assert build_path({'B': 'A', 'C': 'A', 'D': 'B', 'E': 'B'}, 'A', 'E') == ['A', 'B', 'E']

assert dict_is_subset({'a': 1}, {'a': 1, 'b': 2})
assert not dict_is_subset({'a': 2}, {'a': 1, 'b': 2})
assert not dict_is_subset({'a': 1, 'b': 2}, {'a': 1})

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
    'G': [],
}

assert bfs(graph, 'A') == ['A', 'B', 'C', 'D', 'E', 'F']
assert dfs(graph, 'A') == ['A', 'C', 'F', 'E', 'B', 'D']
assert dfs_recursive(graph, 'A') == ['A', 'B', 'D', 'E', 'F', 'C']

assert dict_is_subset({'F': 'C', 'C': 'A'}, shortest_path_bfs(graph, 'A', 'F'))
assert shortest_path(graph, 'A', 'F') == ['A', 'C', 'F']

graph_distances_uniform = {k: {v2: 1 for v2 in v} for k, v in graph.items()}
result = dijkstra(graph_distances_uniform, 'A')
expected = ({'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2},
            {'B': 'A', 'C': 'A', 'D': 'B', 'E': 'B', 'F': 'C'})
assert result == expected

graph_distances = {
  'A': {'B': 1, 'C': 3},
  'B': {'A': 1, 'D': 5},
  'C': {'A': 3, 'D': 1},
  'D': {'B': 5, 'C': 1},
}
result = dijkstra(graph_distances, 'A')
expected = ({'A': 0, 'B': 1, 'C': 3, 'D': 4}, {'B': 'A', 'C': 'A', 'D': 'C'})
assert result == expected
