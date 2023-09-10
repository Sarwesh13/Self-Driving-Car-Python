import pygame
import math
import os
import sensor


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

        self.sensor = sensor.Sensor(self)
        

    def update(self, controls, road_borders):
        self.move(controls)

        self.sensor.update(road_borders)

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

    def draw(self, screen, camera_y):
        #load the car image from the file "./car.png" using pygame.image.load
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_surface = pygame.image.load(image_path)

        # Draw the car image on the screen of size (self.width, self.height) at position (self.x, self.y)
        # screen.blit(car_surface, (self.x, self.y))
        #rotate the car surface based on the current self.angle using pygame.transform.rotate
        #create a new rectangle new_rect for the rotated image, setting its center to (self.x, self.y)
        #draw the rotated car image on the screen using screen.blit

        small_car_surface = pygame.transform.scale(car_surface, (self.width, self.height))
        rotated_image = pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center=(self.x, self.y-camera_y))
        screen.blit(rotated_image, new_rect.topleft)

        self.sensor.draw(screen, camera_y)