class Population:
    def __init__(self, path):
        self.fishes = dict.fromkeys(range(9), 0)
        with open(path, 'r') as f:
            data = [int(i) for i in f.read().split(',')]
            for d in data:
                self.fishes[d] += 1
           
    def run(self, nb_days):
        for i in range(nb_days):
            self.next_day()
        return self.count_fishes()
            
    def next_day(self):
        nb_new_fishes = self.fishes[0]
        for i in range(8):
            self.fishes[i] = self.fishes[i + 1]
        self.fishes[6] += nb_new_fishes
        self.fishes[8] = nb_new_fishes
            
    def count_fishes(self):
        return sum(self.fishes.values())
