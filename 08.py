class Display:
    
    patterns = {
        'abcefg': '0',
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9'
    }

    def __init__(self, path):
        self.entries = []
        with open(path, 'r') as f:
            for line in f.readlines():
                self.entries.append(line.replace('\n', ''))
        
    def get_result(self):
        return sum(self.get_value(entry) for entry in self.entries)

    def get_value(self, entry):
        entree, valeurs = entry.split(' | ')  
        correspondance = {v: k for k, v in self.decode_entry(entree).items()}
        valeurs = valeurs.split(' ')
        value = ''
        for v in valeurs:
            lettres = ''.join(sorted(correspondance.get(lettre) for lettre in v))
            value += self.patterns.get(lettres)
        return int(value)       
    
    def decode_entry(self, entry):
        data = entry.split(' ')
        actual_values = dict.fromkeys(range(9), '')
        correspondance = dict.fromkeys(['a', 'b', 'c', 'd', 'e', 'f', 'g'], '')
        for d in data:
            if len(d) == 2:
                actual_values[1] = d
            elif len(d) == 3:
                actual_values[7] = d
            elif len(d) == 4:
                actual_values[4] = d
            elif len(d) == 7:
                actual_values[8] = d
        correspondance['a'] = self.get_a(actual_values[1], actual_values[7])
        actual_values[9] = self.get_9([d for d in data if len(d) == 6], correspondance['a'], actual_values[4])
        correspondance['e'] = self.get_e(actual_values[8], actual_values[9])
        lettre_c, lettre_d, zero, six = self.get_c_d_0_6([d for d in data if len(d) == 6 and d != actual_values[9]], actual_values[1])
        correspondance['c'] = lettre_c
        correspondance['d'] = lettre_d
        actual_values[0] = zero
        actual_values[6] = six
        deux, trois, cinq = self.get_2_3_5([d for d in data if len(d) == 5], correspondance)
        actual_values[2] = deux
        actual_values[3] = trois
        actual_values[5] = cinq
        correspondance['b'] = self.get_b(actual_values[3], actual_values[9])
        correspondance['g'] = self.get_g(correspondance, actual_values[1])
        correspondance['f'] = self.get_f(correspondance)
        return correspondance
        
    def get_a(self, entry_1, entry_7):
        return list(set(entry_7) - set(entry_1))[0]
        
    def get_9(self, data, value_a, entry_4):
        # data = 0, 6 ou 9 
        # 9 => contient a + lettres de 4
        return [d for d in data if all(lettre in d for lettre in entry_4 + value_a)][0]
        
    def get_e(self, entry_8, entry_9):
        return list(set(entry_8) - set(entry_9))[0]
        
    def get_c_d_0_6(self, data, entry_1):
        # data = 0, 6
        # 0 => all(entry1)
        zero = [d for d in data if all(lettre in d for lettre in entry_1)][0]
        six = [d for d in data if d != zero][0]
        lettre_c = list(set(zero) - set(six))[0]
        lettre_d = list(set(six) - set(zero))[0]
        return lettre_c, lettre_d, zero, six
        
    def get_2_3_5(self, data, correspondance):
        # data = 2, 3 , 5
        # 2 => all (a,c, d,e)
        lettre_a = correspondance['a']
        lettre_c = correspondance['c']
        lettre_d = correspondance['d']
        lettre_e = correspondance['e']
        deux = [d for d in data if all(lettre in d for lettre in [lettre_a, lettre_c, lettre_d, lettre_e])][0]
        trois = [d for d in data if d != deux and len(set(d) - set(deux)) == 1][0]
        cinq = [d for d in data if d != deux and d != trois][0]
        return deux, trois, cinq
     
    def get_b(self, entry_3, entry_9):
        return list(set(entry_9) - set(entry_3))[0]
        
    def get_g(self, correspondance, entry_1):
        # g =  correspondances à trouver non dans 1
        not_in = ''.join([lettre for lettre in correspondance.values() if lettre]) + entry_1
        return [lettre for lettre in correspondance.keys() if lettre not in not_in][0]
        
    def get_f(self, correspondance):
        # la dernière 
        not_in = [lettre for lettre in correspondance.values() if lettre]
        return [lettre for lettre in correspondance.keys() if lettre not in not_in][0]