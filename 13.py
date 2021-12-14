class Paper:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.coordonnees = []
            self.instructions = []
            for line in f.readlines():
                line = line.replace('\n', '')
                if not line:
                    continue
                if ',' in line:
                    valeur_y, valeur_x = line.split(',')
                    self.coordonnees.append((int(valeur_x), int(valeur_y)))
                else:
                    *_junk, instruction = line.split(' ')
                    self.instructions.append(instruction)
                    
    def print_result(self):
        self.fold_all()
        max_x = max(c[0] for c in self.coordonnees)
        max_y = max(c[1] for c in self.coordonnees)
        for i in range(max_x + 1):
            line = ''
            for j in range(max_y + 1):
                if (i, j) in self.coordonnees:
                    line += '#'
                else:
                    line += ' '
            print(line)
        
                    
    def fold_all(self):
        while self.instructions:
            self.next_fold()
                    
    def next_fold(self):
        if not self.instructions:
            return
        instruction = self.instructions.pop(0)
        axe, value = instruction.split('=')
        value = int(value)
        if axe == 'y':
            self.fold_horizontal(value)
        else:
            self.fold_vertical(value)
        return len(self.coordonnees)
                    
    def fold_horizontal(self, value):
        coordonnees_ok = [c for c in self.coordonnees if c[0] < value]
        coordonnees_to_report = [c for c in self.coordonnees if c[0] > value]
        for valeur_x, valeur_y in coordonnees_to_report:
            valeur_x = value - (valeur_x - value)
            coordonnees_ok.append((valeur_x, valeur_y))
        self.coordonnees = list(set(coordonnees_ok))
        return self.coordonnees
        
    def fold_vertical(self, value):
        coordonnees_ok = [c for c in self.coordonnees if c[1] < value]
        coordonnees_to_report = [c for c in self.coordonnees if c[1] > value]
        for valeur_x, valeur_y in coordonnees_to_report:
            valeur_y = value - (valeur_y - value)
            coordonnees_ok.append((valeur_x, valeur_y))
        self.coordonnees = list(set(coordonnees_ok))
        return self.coordonnees