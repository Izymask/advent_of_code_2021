class Map:
    def __init__(self, path):
        self.out_point_value = '.'
        self.enhancement_algorithm = ''
        self.image = []
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.replace('\n', '')
                if not line:
                    continue
                if len(self.enhancement_algorithm) < 512:
                    self.enhancement_algorithm += line
                    continue
                self.image.append(line)
                
    def count_lit_pixels(self, nb_enhance=0):
        for i in range(nb_enhance):
            self.enhance()
        return sum(line.count('#') for line in self.image)
                
    def enhance(self):
        new_image = []
        for i in range(-1, len(self.image) + 1):
            new_value = ''
            for j in range(-1, len(self.image[0]) + 1):
                new_value += self.get_point_enhanced_value(i, j)
            new_image.append(new_value)
        self.image = new_image
        # Modify value of point out of map if necessary
        self.out_point_value = self.enhancement_algorithm[0] if self.out_point_value == '.' else self.enhancement_algorithm[-1]
         
    def get_point_enhanced_value(self, index_1, index_2):
        value = ''
        for i in range(index_1 - 1, index_1 + 2):
            for j in range(index_2 - 1, index_2 + 2):
                value += self.get_point_value(i, j)
        # Binary
        value = value.replace('.', '0').replace('#', '1')
        return self.enhancement_algorithm[int(value, 2)]
                
    def get_point_value(self, index_1, index_2):
        if index_1 < 0 or index_1 > len(self.image) -1 or index_2 < 0 or index_2 > len(self.image[0]) -1:
            return self.out_point_value
        return self.image[index_1][index_2]