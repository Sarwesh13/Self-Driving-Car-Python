# ----------------------pip install pygame ----------------------

import pygame

#Initialize Pygame
pygame.init()

# Define window dimensions
window_width = 800
window_height = 600

# Create the game window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Self Driving Car") #changing default title of "pygame window"
icon = pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon) #changing default pygame icon

#Game loop
running = True
clock = pygame.time.Clock()  #Create a clock object to track time  

#Add a running variable to control the game loop
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  #Set running to False to exit the game loop

    #fill with a background color
    screen.fill((255, 255, 255))  #White background - RGB color model
    #Update the display
    pygame.display.update()


