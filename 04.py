class Joueur:
    
    partie_gagnee = False

    def __init__(self, lines):
        grille = []
        for line in lines:
            numbers = [n for n in line.replace('\n', '').split(' ') if n]
            grille.append([{"value": int(n), "check": False} for n in numbers])
        self.grille = grille
        
    def ajouter_nombre(self, nombre):
        for line in self.grille:
           for item in line:
               if item.get('value') == nombre:
                   item['check'] = True
                   
    def is_done(self):
        # Lines
        for lines in self.grille:
            if all(item.get('check') for item in lines):
                return True
        # Column
        import numpy as np
        transposed = np.transpose(self.grille)
        for lines in transposed:
            if all(item.get('check') for item in lines):
                return True
        return False
        
    def get_unmarked_numbers(self):
        unmarked_numbers = []
        for line in self.grille:
            unmarked_numbers.extend(item.get('value') for item in line if not item.get('check'))
        return unmarked_numbers
        
    def reset_joueur(self):
        self.partie_gagnee = False
        for line in self.grille:
            for item in line:
                item['check'] = False
       
        
class Bingo:
 
    last_number = 0
    winner = None

    def __init__(self, path):
        self.numbers = []
        self.joueurs = []
        grid_lines = []
        with open(path, 'r') as f:
            for line in f.readlines():
                if not self.numbers:
                   self.numbers = [int(n) for n in line.replace('\n', '').split(',')]
                   continue
                if not line.replace('\n', ''):
                    if grid_lines:
                        self.joueurs.append(Joueur(grid_lines))
                        grid_lines = []
                    continue
                grid_lines.append(line)
            else:
                if grid_lines:
                    self.joueurs.append(Joueur(grid_lines))
                    
    def play(self, first_winner=True):
        self.reset_partie()
        nb_gagnants = 0
        for nombre in self.numbers:
            for joueur in self.joueurs:
                if joueur.partie_gagnee:
                    continue
                joueur.ajouter_nombre(nombre)
                if joueur.is_done():
                    nb_gagnants += 1
                    joueur.partie_gagnee = True
                    self.last_number = nombre
                    self.winner = joueur
                    if first_winner:
                        break
                    # Mode: Dernier gagnant, on stoppe s'il ne reste qu'un joueur, sinon, on remove
                    if nb_gagnants == len(self.joueurs):
                        break
                    else:
                        self.winner = None
            if self.winner:
                break
        return sum(self.winner.get_unmarked_numbers()) * self.last_number
        
    def reset_partie(self):
        self.last_number = 0
        self.winner = None
        for joueur in self.joueurs:
            joueur.reset_joueur()
            