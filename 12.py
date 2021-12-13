class Map:
    def __init__(self, path):
        self.paths = []
        self.caves = {}
        with open(path, 'r') as f:
            for line in f.readlines():
                name1, name2 = line.replace('\n', '').split('-')
                cave1 = self.caves.get(name1, Cave(name1))
                cave2 = self.caves.get(name2, Cave(name2))
                cave1.add_link(cave2)
                cave2.add_link(cave1)
                self.caves[name1] = cave1
                self.caves[name2] = cave2
        self.caves.pop('end')
        
    def find_paths(self, start=['start'], one_small_twice=False):
        # one_small_twice = tell if one of the small caves can be visited twice
        last_visited_cave = start[-1]
        if last_visited_cave == 'end':
            path = '-'.join(c for c in start)
            self.paths.append(path)
            return
        actual = self.caves.get(last_visited_cave)        
        for next_cave in actual.links:
            if next_cave.is_small:
                if next_cave.name in start:
                    if not one_small_twice:
                        continue
                    if any(start.count(sc) == 2 for sc in [name for name in self.caves.keys() if name.islower()]):
                        continue                    
            self.find_paths(start + [next_cave.name], one_small_twice=one_small_twice)
        return len(self.paths)
        

class Cave:
    def __init__(self, name, links=None):
        self.links = links or set()
        self.name = name
        
    @property
    def is_small(self):
        return self.name.islower()
        
    def add_link(self, cave):
        if cave.name == 'start':
            return
        self.links.add(cave)