import pygame
import math

class PlayerCar:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        #Advanced car control attributes
        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = 3
        self.friction = 0.05
        self.angle = 0

    def update(self, controls):
        self.move(controls)

    def move(self, controls):
        if controls.forward:
            self.speed += self.acceleration
        if controls.reverse:
            self.speed -= self.acceleration

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed / 2:
            self.speed = -self.max_speed / 2

        if self.speed > 0:
            self.speed -= self.friction
        if self.speed < 0:
            self.speed += self.friction
        if abs(self.speed) < self.friction:
            self.speed = 0

        
        if self.speed != 0:
            # Value of flip: 1 if forwards, -1 if reverse
            # So that controls when reversing are flipped to simulate real-life reverse
            flip = 1 if self.speed > 0 else -1
            if controls.left:
                self.angle += 0.03 * flip
            if controls.right:
                self.angle -= 0.03 * flip

        # Use trigonometry(unit circle formula) to calculate new position
        self.x -= math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        
        # self.y-=self.speed 

    def draw(self, screen):
        #create a car surface with a size matching the car's width and height
        #use pygame.SRCALPHA to create a surface with an alpha channel for transparency
        #fill the car surface with a transparent background by setting it to (0, 0, 0, 0)

        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        car_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))

        #rotate the car surface based on the current self.angle using pygame.transform.rotate
        #create a new rectangle new_rect for the rotated image, setting its center to (self.x, self.y)
        #draw the rotated car image on the screen using screen.blit

        rotated_image = pygame.transform.rotate(car_surface, math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect.topleft)

    # def draw(self, screen):
    #     pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
