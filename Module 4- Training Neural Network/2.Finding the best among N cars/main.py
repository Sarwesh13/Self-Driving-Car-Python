import pygame
import car
import controls
import road

pygame.init()

window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Self Driving Car")
icon = pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon)

# Create the Road object
road_width = 200 
road_height=10000
road = road.Road(road_width, road_height, lane_count=3, window_width=window_width, window_height=window_height)


def generate_cars(N):
    player_cars = []
    for _ in range(N):
        car_instance = car.Car(road.get_lane_center(1), 10000, 30, 45, "PLAYER")
        player_cars.append(car_instance)
    return player_cars

N = 20
player_cars = generate_cars(N)

#array of traffic cars
traffics = [
    car.Car(road.get_lane_center(1), 9800, 30, 45,"TRAFFIC",2)
    # car.Car(road.get_lane_center(0), 9600, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(2), 9600, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(1), 9400, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(0), 9400, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(0), 9200, 30, 45,"TRAFFIC",2),
    # car.Car(road.get_lane_center(2), 9200, 30, 45,"TRAFFIC",2)
]
# Camera offset to follow the car on the y-axis
camera_y_offset = 450


# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #best car with least y-value
    best_car = min(player_cars, key=lambda c: c.y)
    
    # Calculate the camera's y-coordinate based on the car's position
    camera_y = best_car.y - camera_y_offset

    screen.fill((255, 255, 255)) #white

    # Draw the road with camera_y offset
    road.draw(screen, camera_y)

    #update and draw player car
    for p in player_cars: 
        p.update(road.get_borders(), traffics)
        if p == best_car:
            p.draw(screen, camera_y, draw_sensor=True)
        else:
            p.draw(screen, camera_y)

    #update and draw the traffic cars
    for traffic_car in traffics:
        traffic_car.update(road.get_borders(),[])
        traffic_car.draw(screen, camera_y)

    # Update the display
    pygame.display.update()

pygame.quit()
