from models import db
from collections import defaultdict, deque


class RabbitHoleScript:
    def __init__(self, in_memory_db):
        self.categories = in_memory_db.categories
        self.category_tree = in_memory_db.category_tree
        self.similarities = in_memory_db.similarities

    def create_adjacency_list_optimized(self):
        adjacency_list = defaultdict(set)
        for cat1, cat2 in self.similarities:
            adjacency_list[cat1].add(cat2)
            adjacency_list[cat2].add(cat1)
        return adjacency_list

    def bfs_deepest_paths(self, start, adjacency_list):
        queue = deque([(start, [start])])
        visited = set()
        deepest_paths = []
        max_length = 0

        while queue:
            vertex, path = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                if len(path) > max_length:
                    max_length = len(path)
                    deepest_paths = [path]
                elif len(path) == max_length:
                    deepest_paths.append(path)

                for neighbor in adjacency_list[vertex]:
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))

        return max_length - 1, deepest_paths

    def calculate_node_degrees(self, adjacency_list):
        node_degrees = defaultdict(int)
        for node in adjacency_list:
            node_degrees[node] = len(adjacency_list[node])
        return node_degrees

    def find_longest_rabbit_hole_optimized(self, adjacency_list):
        node_degrees = self.calculate_node_degrees(adjacency_list)

        min_degree = min(node_degrees.values())
        lowest_degree_nodes = [node for node, degree in node_degrees.items() if degree == min_degree]

        max_length = 0
        longest_paths = []

        for category in lowest_degree_nodes:
            length, paths = self.bfs_deepest_paths(category, adjacency_list)
            if length > max_length:
                max_length = length
                longest_paths = paths
            elif length == max_length:
                longest_paths.extend(paths)

        normalized_paths = {tuple(sorted(path)) for path in longest_paths}
        return [list(path) for path in normalized_paths]

    def bfs_connected_component(self, start, adjacency_list, visited):
        queue = deque([start])
        connected_component = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                connected_component.append(node)
                for neighbor in adjacency_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return connected_component

    def find_rabbit_islands_optimized(self, adjacency_list):
        visited = set()
        rabbit_islands = []

        for category in adjacency_list:
            if category not in visited:
                connected_component = self.bfs_connected_component(category, adjacency_list, visited)
                rabbit_islands.append(connected_component)

        return rabbit_islands


rabbit_hole_script = RabbitHoleScript(db)
