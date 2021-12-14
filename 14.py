class Polymer:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.transmuts = {}
            for line in f.readlines():
                line = line.replace('\n', '')
                if not line:
                    continue
                if '->' in line:
                    couple, new_p = line.split(' -> ')
                    self.transmuts[couple] = new_p
                else:
                    self.template = line
            self.elements = set(self.transmuts.values())
            self.couples = {}
            for index, element in enumerate(self.template[:-1]):
                first_e, second_e = element, self.template[index + 1]
                couple = f'{first_e}{second_e}'
                self.couples[couple] = self.couples.get(couple, 0) + 1
                    
    def run(self, nb_cycle=1):
        for i in range(nb_cycle):
            self.run_cycle()
        result = dict.fromkeys(self.elements, 0)
        for element in self.elements:
            start = end = 0
            for couple, nb_c in self.couples.items():
                if couple.startswith(element):
                    start += nb_c
                if couple.endswith(element):
                    end += nb_c
                result[element] = max(start, end)
        return max(result.values()) - min(result.values())
    
    def run_cycle(self):
        new_couples = self.couples.copy()
        for couple, nb in self.couples.items():
            if nb == 0:
                continue
            new_element = self.transmuts.get(couple)
            new_couple_1 = f'{couple[0]}{new_element}'
            new_couple_2 = f'{new_element}{couple[1]}'
            new_couples[new_couple_1] = new_couples.get(new_couple_1, 0) + nb
            new_couples[new_couple_2] = new_couples.get(new_couple_2, 0) + nb
            new_couples[couple] = new_couples.get(couple, 0) - nb
        self.couples = new_couples
            
     