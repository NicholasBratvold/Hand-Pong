class PlayerController():

    def __init__(self, object):
        self.object = object
        self.up_event = 24
        self.down_event = 25
        self.stop_event = 26
    
    def handle_event(self, event):
        if event == self.up_event:
            self.object.vely = -self.object.speed
        elif event == self.down_event:
            self.object.vely = self.object.speed
        elif event == self.stop_event:
            self.object.vely = 0





        
    

