import pygame
import math
import sensor
import utils
import network


class Car:
    def __init__(self, x, y, width, height, control_type, max_speed=3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image_traffic = pygame.image.load('traffic.png').convert_alpha()
        self.image_player = pygame.image.load('car.png').convert_alpha()
        self.image_damaged = pygame.image.load('damaged_car.png').convert_alpha()

        #Advanced car control attributes
        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = max_speed
        self.friction = 0.05
        self.angle = 0

        self.control_type = control_type

        self.use_brain=self.control_type=="PLAYER"

        if(control_type!="TRAFFIC"):
            self.sensor = sensor.Sensor(self)
            # print(f"Created sensor for car with sensor: {self.sensor}")
            #input layer of 5(sensor rays) neurons, hidden layer of 6 neurons,and output of 4(up,left,right,down)
            self.brain=network.NeuralNetwork([self.sensor.ray_count,6,4])
            # print(f"car has brain {self.brain}")

        self.damaged=False
        self.polygon = self.create_polygon()
      
        
    def update(self, controls, road_borders,traffics):
        if not self.damaged:
            self.move(controls)
            self.polygon = self.create_polygon()
            self.damaged = self.assess_damage(road_borders,traffics)
        if hasattr(self, 'sensor'):
            self.sensor.update(road_borders,traffics)
            #extract offsets from sensor readings and map them to 0 if null, otherwise 1 - offset
            offsets = [0 if reading is None else 1 - reading['offset'] for reading in self.sensor.readings]
            # offsets=[0 if s is None else 1-s.offset for s in self.sensor.readings]

            #check
            # print(s)
            # outputs = network.NeuralNetwork.feed_forward(offsets, self.brain)
            outputs = network.feed_forwarNeuralNetwork.d(offsets, self.brain)
            #for checking outputs in terminal
            # print(outputs)

            if self.use_brain:
                controls.forward = outputs[0]
                controls.left = outputs[1]
                controls.right = outputs[2]
                controls.reverse = outputs[3]

                # controls.forward = 1
                # controls.left = 0
                # controls.right = 1
                # controls.reverse = 0

    
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
        

    def draw(self, screen, camera_y, draw_sensor=False):
        if self.control_type == "PLAYER":
            if self.damaged:
                image_to_draw = self.image_damaged
            else:
                image_to_draw = self.image_player
            if self.sensor and draw_sensor:
                self.sensor.draw(screen, camera_y)
        else:
            image_to_draw = self.image_traffic

        small_car_surface = pygame.transform.scale(image_to_draw, (self.width, self.height))
        rotated_image = pygame.transform.rotate(small_car_surface, math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center=(self.x, self.y-camera_y))
        screen.blit(rotated_image, new_rect.topleft)

        