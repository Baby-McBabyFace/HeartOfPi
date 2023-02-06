class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def delta(self, delta_x = 0, delta_y = 0):
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        
    def get_coords(self):
        return "{}, {}".format(self.x, self.y)
    