import pygame
import math
import os
import sensor
import utils


class Car:
    def __init__(self, x, y, width, height, control_type, max_speed=4):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        #Advanced car control attributes
        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = max_speed
        self.friction = 0.05
        self.angle = 0

        self.control_type = control_type

        if(control_type=="PLAYER"):
            self.sensor = sensor.Sensor(self)

        self.damaged=False
        self.polygon = self.create_polygon()
      
        
    def update(self, controls, road_borders,traffics):
        if not self.damaged:
            self.move(controls)
            self.polygon = self.create_polygon()
            self.damaged = self.assess_damage(road_borders,traffics)
        if hasattr(self, 'sensor'):
            self.sensor.update(road_borders,traffics)


    
    def create_polygon(self):
        points = []
        rad = math.hypot(self.width, self.height) / 2
        alpha = math.atan2(self.width, self.height)
        points.append({
            'x': self.x - math.sin(self.angle - alpha) * rad,
            'y': self.y - math.cos(self.angle - alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(self.angle + alpha) * rad,
            'y': self.y - math.cos(self.angle + alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(math.pi + self.angle - alpha) * rad,
            'y': self.y - math.cos(math.pi + self.angle - alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(math.pi + self.angle + alpha) * rad,
            'y': self.y - math.cos(math.pi + self.angle + alpha) * rad
        })
        return points


    def assess_damage(self, road_borders,traffics):
        for border in road_borders:
            if utils.polys_intersect(self.polygon, border):
                return True
            
        for traffic in traffics:
            if utils.polys_intersect(self.polygon, traffic.polygon):
                return True
        return False


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
        if self.control_type == "PLAYER":
            if self.damaged:
                #load the damaged car image from the file "./damaged_car.png" using pygame.image.load
                current_dir = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.join(current_dir, "damaged_car.png")
                car_surface = pygame.image.load(image_path).convert_alpha()
            else:
                #load the original car image from the file "./car.png" using pygame.image.load
                current_dir = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.join(current_dir, "car.png")
                car_surface = pygame.image.load(image_path).convert_alpha()
                

            small_car_surface = pygame.transform.scale(car_surface, (self.width, self.height))
            rotated_image = pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
            new_rect = rotated_image.get_rect(center=(self.x, self.y-camera_y))
            screen.blit(rotated_image, new_rect.topleft)

            if self.sensor:
                self.sensor.draw(screen, camera_y)
        
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "traffic.png")
            car_surface = pygame.image.load(image_path).convert_alpha()

            small_car_surface = pygame.transform.scale(car_surface, (self.width, self.height))
            rotated_image = pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
            new_rect = rotated_image.get_rect(center=(self.x, self.y - camera_y))
            screen.blit(rotated_image, new_rect.topleft)