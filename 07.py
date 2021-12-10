class SubMarine:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.crabs = [int(c) for c in f.read().replace('\n', '').split(',')]
            
    def get_distances(self, use_crab_method):
        min_pos = min(self.crabs)
        max_pos = max(self.crabs)
        if not use_crab_method:
            return [sum(abs(i - crab_pos) for crab_pos in self.crabs) for i in range(min_pos, max_pos + 1)]
        return [sum(sum(j for j in range (abs(i - crab_pos) + 1)) for crab_pos in self.crabs) for i in range(min_pos, max_pos + 1)]
        
    def get_shortest_distance(self, use_crab_method=False):
        distances = self.get_distances(use_crab_method)
        return min(distances)
