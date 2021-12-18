class Probe:
    def __init__(self, path):
        self.x = 0
        self.y = 0
        self.x_velocity = 0
        self.y_velocity = 0
        with open(path, 'r') as f:
            data = f.read().replace('\n', '').replace('target area:', '')
        data_x, data_y = data.split(',')
        x_min, x_max = data_x.replace('x=', '').split('..')    
        y_min, y_max = data_y.replace('y=', '').split('..')    
        self.target_x_min = int(x_min.strip())
        self.target_x_max = int(x_max.strip())
        self.target_y_min = int(y_min.strip())
        self.target_y_max = int(y_max.strip())
   
    def reset_position(self):
        self.x = 0
        self.y = 0
        
    def get_result(self):
        max_y = 0
        max_velocity = (0, 0)
        nb_ok = 0
        for i in range(self.target_x_max + 1):
            for j in range(self.target_y_min, abs(self.target_y_min)):  # Arbitrary value, can obviously do better ;<
                launch_result, hauteur = self.launch(i, j)
                if launch_result == 'OK':
                    nb_ok += 1
                    if hauteur > max_y:
                        max_y = hauteur
                        max_velocity = (i, j)
        return nb_ok, max_velocity, max_y
        
    def launch(self, x_velocity, y_velocity):
        max_high = 0
        self.reset_position()
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        while True:
            self.x, self.y = self.next_position()
            if self.y > max_high:
                max_high = self.y
            self.update_velocity()
            if self.is_out():
                return 'KO', max_high
            if self.is_in_target():
                return 'OK', max_high
                
    def next_position(self):
        return self.x + self.x_velocity, self.y + self.y_velocity
        
    def update_velocity(self):
        if self.x_velocity < 0:
            self.x_velocity += 1
        elif self.x_velocity > 0:
            self.x_velocity -= 1       
        self.y_velocity -= 1
            
    def is_in_target(self):
        return self.target_x_min <= self.x <= self.target_x_max and self.target_y_min <= self.y <= self.target_y_max
        
    def is_out(self):
        return self.x > self.target_x_max or self.y < self.target_y_min
        