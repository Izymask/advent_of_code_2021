class Map:
    def __init__(self, path):
        mesures = []
        walls = []
        self.low_points = []
        with open(path, 'r') as f:
            for line in f.readlines():
                mesures.append([int(m) for m in line.replace('\n', '')])
        self.mesures = mesures
        
        for i, m in enumerate(mesures):
            for j, valeur in enumerate(m):
                if valeur == 9:
                    walls.append((i, j))
        self.walls = walls
        
    def get_result(self):
        import math
        bassins = self.get_bassins()
        taille = [len(b) for b in bassins]
        return math.prod(sorted(taille, reverse=True)[:3])
        
    def get_bassins(self):
        self.get_risk_level()
        return [self.get_bassin(*point) for point in self.low_points]
        
    def get_risk_level(self):
        risk_values = []
        for i, line in enumerate(self.mesures):
            for j, valeur in enumerate(line):
                if self.is_low_point(i, j):
                    self.low_points.append((i, j))
                    risk_values.append(valeur)
        return sum(rv + 1 for rv in risk_values)
        
    def is_low_point(self, index_1, index_2):
        point_value = self.mesures[index_1][index_2]
        return all(v > point_value for v in self.get_surroundings_values(index_1, index_2))
        
    def get_surroundings_values(self, index_1, index_2):
        values = []
        for i in range(index_1 - 1, index_1 + 2):
            for j in range(index_2 - 1, index_2 + 2):
                if (i == index_1 and j == index_2) or i < 0 or j < 0:
                    continue
                try:
                    values.append(self.mesures[i][j])
                except IndexError:
                    continue
        return values
        
    def get_bassin(self, index_1, index_2):
        walls = self.walls
        actual = (index_1, index_2)
        bassin = {actual: {'up': False, 'right': False, 'down': False, 'left': False}}
        largeur = len(self.mesures[0])
        longueur = len(self.mesures)
        
        def is_check(coords, infos):
            index_1, index_2 = coords
            if not infos.get('up') and (index_1 - 1, index_2) not in walls and index_1 - 1 >= 0:
                return False
            if not infos.get('right') and (index_1, index_2 + 1) not in walls and index_2 + 1 < largeur:
                return False
            if not infos.get('down') and (index_1 + 1, index_2) not in walls and index_1 + 1 < longueur:
                return False
            if not infos.get('left') and (index_1, index_2 - 1) not in walls and index_2 - 1 >= 0:
                return False
            return True
        
        while not (all(is_check(coords, infos) for coords, infos in bassin.items())):
            self.bassin = bassin
            i, j = actual
            point_from = actual
            if not bassin.get(actual).get('up'):
                bassin[actual]['up'] = True
                if i - 1 < 0:
                    continue
                try:
                    new_value = self.mesures[i-1][j]
                    if new_value == 9:
                        continue
                    actual = (i - 1, j)
                    if actual not in bassin:
                        bassin[actual] = {'up': False, 'right': False, 'down': False, 'left': False}
                    bassin[actual]['down'] = True
                except IndexError:
                    continue
            elif not bassin.get(actual).get('right'):
                bassin[actual]['right'] = True
                try:
                    new_value = self.mesures[i][j + 1]
                    if new_value == 9:
                        continue
                    actual = (i, j + 1)
                    if actual not in bassin:
                        bassin[actual] = {'up': False, 'right': False, 'down': False, 'left': False}
                    bassin[actual]['left'] = True
                except IndexError:
                    continue        
            elif not bassin.get(actual).get('down'):
                bassin[actual]['down'] = True
                try:
                    new_value = self.mesures[i+1][j]
                    if new_value == 9:
                        continue
                    actual = (i + 1, j)
                    if actual not in bassin:
                        bassin[actual] = {'up': False, 'right': False, 'down': False, 'left': False}
                    bassin[actual]['up'] = True
                except IndexError:
                    continue
            elif not bassin.get(actual).get('left'):
                bassin[actual]['left'] = True
                if j - 1 < 0:
                    continue
                try:
                    new_value = self.mesures[i][j - 1]
                    if new_value == 9:
                        continue
                    actual = (i, j - 1)
                    if actual not in bassin:
                        bassin[actual] = {'up': False, 'right': False, 'down': False, 'left': False}
                    bassin[actual]['right'] = True
                except IndexError:
                    continue 
            if bassin[actual].get('up') and bassin[actual].get('right') and bassin[actual].get('down') and bassin[actual].get('left'):
                try:
                    actual = [k for k, v in m.bassin.items() if not is_check(k, v)][0] 
                except IndexError:
                    continue
        return bassin
        