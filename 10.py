class Analizer:

    closing_characters = {
        ')': '(',
        '}': '{',
        ']': '[',
        '>': '<'
    }

    def __init__(self, path):
        with open(path, 'r') as f:
            self.data = [line.replace('\n', '') for line in f.readlines()]
        self.corrupted_chars = []
        self.missing_sequences = []
        for line in self.data:
            c_char, missing_sequence = self.get_corrupted_character_or_missing_sequence(line)
            if c_char:
                self.corrupted_chars.append(c_char)
            else:
                self.missing_sequences.append(missing_sequence)
        
    def get_missing_sequences_value(self):
        values = sorted([self.get_missing_sequence_value(missing) for missing in self.missing_sequences])
        return values[len(values) // 2]
            
    def get_corrupted_value(self):
        values = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }
        return sum(values.get(c) for c in self.corrupted_chars)
                
    def get_corrupted_character_or_missing_sequence(self, line):
        opening_characters = []
        corrupted_char = None
        for character in line:
            if character not in self.closing_characters.keys():
                opening_characters.append(character)
                continue
            if not opening_characters:
                corrupted_char = character
                break
            last_opening_char = opening_characters.pop(-1)
            if self.closing_characters[character] != last_opening_char:
                corrupted_char = character
                break
        
        if corrupted_char:
            return corrupted_char, None
        else:
            return None, self.get_missing_sequence(opening_characters)
            
    def get_missing_sequence(self, chars_to_match):
        correspondance = {v: k for k, v in self.closing_characters.items()}
        return [correspondance.get(c) for c in reversed(chars_to_match)]
                
    def get_missing_sequence_value(self, missing_sequence):
        values = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }
        result = 0
        for character in missing_sequence:
            result *= 5
            result += values.get(character)
        return result
                