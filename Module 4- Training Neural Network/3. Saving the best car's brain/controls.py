class Controls:
    def __init__(self, control_type):
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False
       
        if control_type=="TRAFFIC":
            self.forward=True

            
    
