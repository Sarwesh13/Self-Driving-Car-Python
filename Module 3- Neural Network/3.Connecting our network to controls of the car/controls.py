import pygame

class Controls:
    def __init__(self, control_type):
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False
        self.control_type=control_type

    def update(self, event):
        if self.control_type=="PLAYER":
            self.keyboard_listeners(event)
        else:
            self.forward=True
            
    
    def keyboard_listeners(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
            elif event.key == pygame.K_RIGHT:
                self.right = True
            elif event.key == pygame.K_UP:
                self.forward = True
            elif event.key == pygame.K_DOWN:
                self.reverse = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False
            elif event.key == pygame.K_UP:
                self.forward = False
            elif event.key == pygame.K_DOWN:
                self.reverse = False