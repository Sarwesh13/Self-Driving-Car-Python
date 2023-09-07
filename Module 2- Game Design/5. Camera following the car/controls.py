import pygame

class Controls:
    def __init__(self):
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False

    def update(self, event):
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
