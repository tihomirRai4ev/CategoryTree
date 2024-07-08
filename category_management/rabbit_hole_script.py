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

    def bfs_deepest_path(self, start, adjacency_list):
        queue = deque([(start, [start])])
        visited = set()
        deepest_path = []

        while queue:
            vertex, path = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                if len(path) > len(deepest_path):
                    deepest_path = path

                for neighbor in adjacency_list[vertex]:
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))

        return len(deepest_path) - 1, deepest_path

    def find_longest_rabbit_hole_optimized(self, adjacency_list):
        max_length = 0
        longest_paths = []

        for category in adjacency_list:
            length, path = self.bfs_deepest_path(category, adjacency_list)
            if length > max_length:
                max_length = length
                longest_paths = [path]
            elif length == max_length:
                longest_paths.append(path)

        # Normalize paths to avoid duplicates due to reverse paths
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
