import pygame

class Road:
    def __init__(self, width, lane_count=3, window_width=800, window_height=600):
        self.width = width
        self.lane_count = lane_count
        self.window_width = window_width
        self.window_height = window_height

        # road position (lets make it center for now)
        self.x = (window_width - width) / 2 
    
    def get_lane_center(self, lane_index):
        lane_width = self.width / self.lane_count
        return self.x + lane_width * lane_index + lane_width / 2

    def draw(self, screen):
        road_color = (128, 128, 128)  
        lane_color = (255, 255, 0)
        border_color = (255, 255, 0)
        border_width = 5

        lane_width = self.width / self.lane_count

        # Fill the road area with the road color
        pygame.draw.rect(screen, road_color, (self.x, 0, self.width, self.window_height))

        for i in range(self.lane_count + 1):  # Draw one more lane for the rightmost lane
            x = self.x + lane_width * i
            pygame.draw.rect(screen, lane_color, (x - 5 // 2, 0, 5, self.window_height))

