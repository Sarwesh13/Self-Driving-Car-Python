import pygame
import math
import os
import sensor


class PlayerCar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        #Advanced car control attributes
        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = 3
        self.friction = 0.05
        self.angle = 0

        self.sensor = sensor.Sensor(self)

        self.damaged=False
        

    def update(self, controls, road_borders):
        if not self.damaged:
            self.move(controls)
            self.damaged = self.assess_damage(road_borders)

        self.sensor.update(road_borders)

    def assess_damage(self, road_borders):
        for border in road_borders:
            if self.intersect(border):
                return True
        return False

    def intersect(self, border):
        car_left, car_right, car_top, car_bottom = self.get_bounds()
        border_left, border_right, border_top, border_bottom = self.get_border_bounds(border)

        #check for collision by comparing boundaries
        if (car_right >= border_left and car_left <= border_right and
            car_bottom >= border_top and car_top <= border_bottom):
            return True

        return False
    #calculate the boundaries of the car
    def get_bounds(self):
        car_left = self.x - self.width / 2
        car_right = self.x + self.width / 2
        car_top = self.y - self.height / 2
        car_bottom = self.y + self.height / 2

        return car_left, car_right, car_top, car_bottom

    #calculate the boundaries of road borders
    def get_border_bounds(self, border):
        border_left = border[0]['x']
        border_right = border[1]['x']
        border_top = border[0]['y']
        border_bottom = border[1]['y']

        return border_left, border_right, border_top, border_bottom


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
        if self.damaged:
            # Load the damaged car image from the file "./damaged_car.png" using pygame.image.load
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "damaged_car.png")
            car_surface = pygame.image.load(image_path)
        else:
            # Load the original car image from the file "./car.png" using pygame.image.load
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