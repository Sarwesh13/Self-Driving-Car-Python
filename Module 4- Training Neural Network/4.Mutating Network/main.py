import pygame
import pickle


import network
import car
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
        player_cars.append(car.Car(road.get_lane_center(1), 10000, 30, 45, "PLAYER"))
    return player_cars

N = 20
player_cars = generate_cars(N)
try:
    with open('brain.txt', 'rb') as b:
        for i in range(len(player_cars)):
            player_cars[i].brain = pickle.load(b)
            if i != 0:
                network.NeuralNetwork.mutate(player_cars[i].brain,amount=0.1)
except FileNotFoundError:
    print('no file')
except Exception as e:
    print('error ', e)

def save_brain():
    best_brain = best_car.brain
    with open('brain.txt','wb') as f:
        for _ in range(N):
            pickle.dump(best_brain,f)

#array of traffic cars
traffics = [
    car.Car(road.get_lane_center(1), 9800, 30, 45,"TRAFFIC",2),
    car.Car(road.get_lane_center(0), 9600, 30, 45,"TRAFFIC",2),
    car.Car(road.get_lane_center(2), 9600, 30, 45,"TRAFFIC",2),
    car.Car(road.get_lane_center(1), 9400, 30, 45,"TRAFFIC",2),
    car.Car(road.get_lane_center(0), 9400, 30, 45,"TRAFFIC",2),
    car.Car(road.get_lane_center(0), 9200, 30, 45,"TRAFFIC",2),
    car.Car(road.get_lane_center(2), 9200, 30, 45,"TRAFFIC",2)
]
# Camera offset to follow the car on the y-axis
camera_y_offset = 450

#button properties
save_button = pygame.Rect(640, 10, 150, 50)
button_font = pygame.font.Font(None, 36)
button_colors = {
    "idle": (0, 0, 0),
    "hover": (128, 128, 128),
    "click": (0, 255, 0),
}
save_button_state="idle"

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if save_button.collidepoint(event.pos):
                save_button_state = "hover"
            else:
                save_button_state = "idle"
                
        elif event.type == pygame.MOUSEBUTTONDOWN:               
            if save_button.collidepoint(event.pos):
                save_button_state="click"
                save_brain()

    #best car with least y-value
    best_car = min(player_cars, key=lambda c: c.y)

    # Calculate the camera's y-coordinate based on the car's position
    camera_y = best_car.y - camera_y_offset

    screen.fill((255, 255, 255)) #white

    # Draw the road with camera_y offset
    road.draw(screen, camera_y)

    #update and draw player car
    # for i in range(len(player_cars)):
    for i,player_car in enumerate(player_cars):
        player_car.update(road.get_borders(), traffics)
        # print(f"car {i} has brain: ", player_car.brain.to_string())
        if player_car == best_car:
            player_car.draw(screen, camera_y, draw_sensor=True)
        else:
            player_car.draw(screen, camera_y)


    #update and draw the traffic cars
    for traffic_car in traffics:
        traffic_car.update([], [])
        traffic_car.draw(screen, camera_y)

    #save brain button 
    save_button_color = button_colors[save_button_state]
    pygame.draw.rect(screen, save_button_color, save_button)
    save_text = button_font.render("Save Brain", True, (255, 255, 255))
    screen.blit(save_text, (650, 20))

    pygame.display.update()

pygame.quit()
