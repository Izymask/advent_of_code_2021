import networkx as nx

class Cave:
    def __init__(self, path):
        self.base_map = {}
        self.path_values = []
        with open(path, 'r') as f:
            for i, line in enumerate(f.readlines()):
                for j, value in enumerate(line.replace('\n', '')):
                    self.base_map[(i, j)] = int(value)
        # Full map for 15.2
        self.full_map = {}
        self.longueur = max(c[0] for c in self.base_map) + 1
        self.largeur = max(c[1] for c in self.base_map) + 1
        for i in range(5):
            for coords, value in self.base_map.items():
                index_1, index_2 = coords
                self.full_map[(index_1 + (i * self.longueur), index_2)] = ((value + i) % 9) or 9
        temporary_map = self.full_map.copy()
        for j in range(5):
            for coords, value in temporary_map.items():
                index_1, index_2 = coords
                self.full_map[(index_1, index_2 + (j * self.largeur))] = ((value + j) % 9) or 9
                    
    def run(self, use_full_map=False):
        map_to_use = self.full_map if use_full_map else self.base_map
        graph = self.create_graph(map_to_use)
        return nx.dijkstra_path_length(graph, (0, 0), max(map_to_use))
        
    # Copyright Debnet
    def create_graph(self, map_to_use):
        graph = nx.DiGraph()
        graph.add_nodes_from(map_to_use)
        for x, y in map_to_use:
            for sx, sy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                dx, dy = x + sx, y + sy
                weight = map_to_use.get((dx, dy))
                if not weight:
                    continue
                graph.add_edge((x, y), (dx, dy), weight=weight)
        return graph            
        
