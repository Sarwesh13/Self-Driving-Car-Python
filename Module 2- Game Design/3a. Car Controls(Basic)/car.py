import pygame

class PlayerCar:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self, controls):
        if controls.forward:
            self.y -= 1
        if controls.reverse:
            self.y += 1
        if controls.left:
            self.x -= 1
        if controls.right:
            self.x += 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
