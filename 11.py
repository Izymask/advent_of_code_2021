class Population:
    def __init__(self, path):
        self.nb_flashes = 0
        self.octopuses = []
        with open(path, 'r') as f:
            for line in f.readlines():
                self.octopuses.append([{'power': int(p), 'flash': False} for p in line.replace('\n', '')])
                
    def run(self, nb_days):
        for i in range(nb_days):
            self.next_day()
        return self.nb_flashes
        
    def get_day_all_flashes(self):
        days = 0
        while True:
            previous_flashes = self.nb_flashes
            self.next_day()
            days += 1
            if self.nb_flashes - previous_flashes == 100:
                return days
    
    def next_day(self):
        self.reset_flash()
        to_flash = []
        for i, line in enumerate(self.octopuses):
            for j, octopuse in enumerate(line):
                power = octopuse.get('power') + 1
                octopuse['power'] = power
                if power > 9:
                    to_flash.append((i, j))
        while to_flash:
            i, j = to_flash.pop(0)
            new_flashes = self.flash(i, j)
            if new_flashes:
                to_flash.extend(new_flashes)
        return self.nb_flashes
                
    def reset_flash(self):
        for line in self.octopuses:
            for octopuse in line:
                octopuse['flash'] = False
          
    def flash(self, i, j):
        new_flashes = []
        octopuse = self.octopuses[i][j]
        if octopuse.get('flash'):
            return
        octopuse['flash'] = True
        octopuse['power'] = 0
        self.nb_flashes += 1
        for index_1 in range(max(0, i - 1), min(10, i + 2)):
            for index_2 in range(max(0, j - 1), min(10, j + 2)):
                if index_1 == i and index_2 == j:
                    continue
                octopuse = self.octopuses[index_1][index_2]
                if octopuse.get('flash'):
                    continue
                power = octopuse.get('power') + 1
                octopuse['power'] = power
                if power > 9:
                    new_flashes.append((index_1, index_2))
        return new_flashes
        
