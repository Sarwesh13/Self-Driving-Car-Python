import pygame
import car
import controls

pygame.init()

window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Driving Game")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# Create the PlayerCar object
player_car = car.PlayerCar(window_width/2-25, window_height-75,50,75,(255,0,0))

# Create a controls instance
controls = controls.Controls()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Update controls based on keyboard events
        controls.update(event)

    
    screen.fill((255,255,255))  

    # Update the player car's position based on controls
    player_car.update(controls)

    #Draw the player car
    player_car.draw(screen)

    # Update the display
    pygame.display.update()

