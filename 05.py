class Map:
    def __init__(self, path):
        self.moves = []
        max_x = max_y = 0
        with open(path, 'r') as f:
            for line in f.readlines():
                coord_1, coord_2 = line.replace('\n', '').replace(' ', '').split('->')
                p1 = Point(*[int(c) for c in coord_1.split(',')])
                if p1.x > max_x:
                    max_x = p1.x
                if p1.y > max_y:
                    max_y = p1.y
                p2 = Point(*[int(c) for c in coord_2.split(',')])
                if p2.x > max_x:
                    max_x = p2.x
                if p2.y > max_y:
                    max_y = p2.y
                self.moves.append((p1, p2))
        self.matrix = [[0 for i in range(max_x + 1)] for j in range(max_y + 1)]
                
    def make_move(self, move, diagonales):
        p1, p2 = move
        if not diagonales:
            if p1.x != p2.x and p1.y != p2.y:
                return
        if p1.x < p2.x:
            mod_x = 1
        else:
            mod_x = -1
            
        if p1.y < p2.y:
            mod_y = 1
        else:
            mod_y = -1
            
        self.matrix[p1.y][p1.x] += 1
        while not Point.are_equals(p1, p2):
            if p1.x != p2.x:
                p1.x += mod_x
            if p1.y != p2.y:
                p1.y += mod_y
            self.matrix[p1.y][p1.x] += 1
            
    def get_overlaps(self, overlap_value=2):
        result = 0
        for line in self.matrix:
            result += len([p for p in line if p >= overlap_value])
        return result
    
    def run(self, diagonales=False):
        for move in self.moves:
            self.make_move(move, diagonales=diagonales)
        
            
class Point:
    def __init__(self, valeur_x, valeur_y):
        self.x = valeur_x
        self.y = valeur_y
        
    @staticmethod
    def are_equals(point1, point2):
        return point1.x == point2.x and point1.y == point2.y
    
    def __str__(self):
        return f'{self.x}, {self.y}'