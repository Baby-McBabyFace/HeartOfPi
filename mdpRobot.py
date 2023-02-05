class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def delta_x(self, delta):
        self.x = self.x + delta
    
    def delta_y(self, delta):
        self.y = self.y + delta
    
    def get_coords(self):
        return self.x, self.y
    