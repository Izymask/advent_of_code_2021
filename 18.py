import json


class Homework:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.operations = [op.replace('\n', '') for op in f.readlines()]
            
    def do_work(self):
        result = self.operations.pop(0)
        while self.operations:
            next_operation = self.operations.pop(0)
            result = Pair([json.loads(str(result)), json.loads(next_operation)])
            result.reduce()
        result_pair = result
        return result_pair.get_magnitude()
        
    def get_max_magnitude(self):
        max_magnitude = 0
        for op1 in self.operations:
            for op2 in [op for op in self.operations if op != op1]:
                pair_to_test = Pair([json.loads(op1), json.loads(op2)])
                pair_to_test.reduce()
                pair_magnitude = pair_to_test.get_magnitude()
                if pair_magnitude > max_magnitude:
                    max_magnitude = pair_magnitude
        return max_magnitude


class Pair:
    def __init__(self, entry, parent=None):
        self.parent = parent
        self.depth = parent.depth + 1 if parent else 1
        self.left_value, self.right_value = entry
        if isinstance(self.left_value, list):
            self.left_value = Pair(self.left_value, parent=self)
        if isinstance(self.right_value, list):
            self.right_value = Pair(self.right_value, parent=self)
            
    def is_left(self):
        if self.parent and self.parent.left_value == self:
            return True
        return False
        
    def is_right(self):
        if self.parent and self.parent.right_value == self:
            return True
        return False
        
    def get_magnitude(self):
        if isinstance(self.left_value, int):
            left = self.left_value
        else:
            left = self.left_value.get_magnitude()
            
        if isinstance(self.right_value, int):
            right = self.right_value
        else:
            right = self.right_value.get_magnitude()
        
        return 3 * left  + 2 * right
    
    def reduce(self):
        # run explosions
        explosions = self.get_explosions()
        while explosions:
            pair_to_operate = explosions.pop(0).get('pair')
            pair_to_operate.explode()
        
        # run Splits
        splits = self.get_splits()
        if not splits:
            return
        split = splits[0]
        pair_to_operate = split.get('pair')
        pair_to_operate.split(field_to_split=split.get('field_to_split'))
        self.reduce()
        
    def get_explosions(self):
        explosions = []
        if self.depth > 4:
            explosions.append({'pair': self, 'action': 'E'})
        if isinstance(self.left_value, Pair):
            explosions.extend(self.left_value.get_explosions())
        if isinstance(self.right_value, Pair):
            explosions.extend(self.right_value.get_explosions())
        return explosions
        
    def get_splits(self):
        splits = []
        if isinstance(self.left_value, Pair):
            splits.extend(self.left_value.get_splits())
        elif self.left_value > 9:
            splits.append({'pair': self, 'action': 'S', 'field_to_split': 'left_value'})
        
        if isinstance(self.right_value, Pair):
            splits.extend(self.right_value.get_splits())
        elif self.right_value > 9:
            splits.append({'pair': self, 'action': 'S', 'field_to_split': 'right_value'})
        return splits
        
    def explode(self):
        # get direct left pair
        left_pair = self.get_direct_left_pair()
        if left_pair:
            if left_pair == self:
                self.parent.left_value += self.left_value
            elif isinstance(left_pair.right_value, Pair):
                left_pair.left_value += self.left_value
            else:
                left_pair.right_value += self.left_value
        
        # get direct right pair
        right_pair = self.get_direct_right_pair()
        if right_pair:
            if right_pair == self:
                self.parent.right_value += self.right_value
            elif isinstance(right_pair.left_value, Pair):
                right_pair.right_value += self.right_value
            else:
                right_pair.left_value += self.right_value
                         
        # replace actual with 0
        parent = self.parent
        if self.is_left():
            parent.left_value = 0
        elif self.is_right():
            parent.right_value = 0
            
    def get_direct_left_pair(self):
        left_pair = None
        if self.is_left():
            parent = self.parent
            while parent:
                if parent.is_right():
                   left_pair = parent.parent.left_value
                   if isinstance(left_pair, int):
                       left_pair = parent.parent
                       break
                   while isinstance(left_pair.right_value, Pair):
                       left_pair = left_pair.right_value
                   break
                parent = parent.parent              
        elif self.is_right():
            left_pair = self.parent.left_value
            if not isinstance(left_pair, Pair):
                left_pair = self
        return left_pair
        
    def get_direct_right_pair(self):
        right_pair = None
        if self.is_right():
            parent = self.parent
            while parent:
                if parent.is_left():
                   right_pair = parent.parent.right_value
                   if isinstance(right_pair, int):
                       right_pair = parent.parent
                       break
                   while isinstance(right_pair.left_value, Pair):
                       right_pair = right_pair.left_value
                   break
                parent = parent.parent              
        elif self.is_left():
            right_pair = self.parent.right_value
            if not isinstance(right_pair, Pair):
                right_pair = self
        return right_pair
            
    def split(self, field_to_split):
        value = getattr(self, field_to_split)
        new_left_value = value // 2
        new_right_value = value - new_left_value
        setattr(self, field_to_split, Pair([new_left_value, new_right_value], parent=self))
            
    def __str__(self):
        if isinstance(self.left_value, Pair):
            left_print = f'[{str(self.left_value)}'
        else:
            left_print = f'[{self.left_value}'
        if isinstance(self.right_value, Pair):
            right_print = f'{str(self.right_value)}]'
        else:
            right_print = f'{self.right_value}]'
        return f'{left_print}, {right_print}'