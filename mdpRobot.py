class Robot:
    def __init__(self, x=0, y=0, orientation=720):
        self.x = x
        self.y = y
        self.orientation = orientation
        
        # 0 -> top
        # 90 -> left
        # 180 -> bottom
        # 270 -> right
    
    def delta(self, delta_x = 0, delta_y = 0):
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        
    def get_coords(self):
        return "ROBOT/{}/{}/{}".format(self.x, self.y, (self.orientation % 360))
    
    def update_delta_straight(self, movement, distance):
        if(movement == 1):
            if(self.orientation % 360 == 0):
                self.delta(delta_y=(distance/10))
            elif(self.orientation % 360 == 90):
                self.delta(delta_x=(-distance/10))
            elif(self.orientation % 360 == 180):
                self.delta(delta_y=(-distance/10))
            elif(self.orientation % 360 == 270):
                self.delta(delta_x=(distance/10))
        elif(movement == 2):
            if(self.orientation % 360 == 0):
                self.delta(delta_y=(-distance/10))
            elif(self.orientation % 360 == 90):
                self.delta(delta_x=(distance/10))
            elif(self.orientation % 360 == 180):
                self.delta(delta_y=(distance/10))
            elif(self.orientation % 360 == 270):
                self.delta(delta_x=(-distance/10))

    def update_delta_turn(self, movement, angle):
        if(movement == 3): # LEFT
            if(self.orientation % 360 == 0):
                self.delta(delta_x=-3, delta_y=3)
            elif(self.orientation % 360 == 90):
                self.delta(delta_x=-3, delta_y=-3)
            elif(self.orientation % 360 == 180):
                self.delta(delta_x=3, delta_y=-3)
            elif(self.orientation % 360 == 270):
                self.delta(delta_x=3, delta_y=3)                
            self.orientation -= angle
        elif(movement == 4): # RIGHT
            if(self.orientation % 360 == 0):
                self.delta(delta_x=3, delta_y=3)
            elif(self.orientation % 360 == 90):
                self.delta(delta_x=-3, delta_y=3)
            elif(self.orientation % 360 == 180):
                self.delta(delta_x=-3, delta_y=-3)
            elif(self.orientation % 360 == 270):
                self.delta(delta_x=3, delta_y=-3)
            self.orientation += angle
        elif(movement == 5): # R LEFT
            if(self.orientation % 360 == 0):
                self.delta(delta_x=-3, delta_y=-3)
            elif(self.orientation % 360 == 90):
                self.delta(delta_x=3, delta_y=-3)
            elif(self.orientation % 360 == 180):
                self.delta(delta_x=3, delta_y=3)
            elif(self.orientation % 360 == 270):
                self.delta(delta_x=-3, delta_y=3)
            self.orientation += angle
        elif(movement == 6): # R RIGHT
            if(self.orientation % 360 == 0):
                self.delta(delta_x=3, delta_y=-3)
            elif(self.orientation % 360 == 90):
                self.delta(delta_x=3, delta_y=3)
            elif(self.orientation % 360 == 180):
                self.delta(delta_x=-3, delta_y=3)
            elif(self.orientation % 360 == 270):
                self.delta(delta_x=-3, delta_y=-3)
            self.orientation -= angle
