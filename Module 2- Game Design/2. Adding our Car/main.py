import pygame
import car 

pygame.init()

window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Self Driving Car")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# Create the PlayerCar object
player_car = car.PlayerCar(window_width // 2 - 25, window_height - 75, 50, 75, (255, 0, 0))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen (fill with a background color)
    screen.fill((255, 255, 255))  # White background

    #Draw the player car
    player_car.draw(screen)

    # Update the display
    pygame.display.update()

