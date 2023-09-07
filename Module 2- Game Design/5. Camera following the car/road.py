import pygame

class Road:
    def __init__(self, width, total_height, lane_count=3, window_width=800, window_height=600):
        self.width = width
        self.total_height = total_height  # Set the total height of the road
        self.lane_count = lane_count
        self.window_width = window_width
        self.window_height = window_height

        # Calculate the road position to center it both above and below the screen
        self.x = (window_width - width) / 2
        self.y = (total_height - window_height) / 2 

    def get_lane_center(self, lane_index):
        lane_width = self.width / self.lane_count
        return self.x + lane_width * lane_index + lane_width / 2

    def draw(self, screen, camera_y):
        road_color = (128, 128, 128)
        lane_color = (255, 255, 255)
        border_color = (255, 255, 0)
        border_width = 5

        lane_width = self.width / self.lane_count

        # Fill the road area with the road color
        pygame.draw.rect(screen, road_color, (self.x, self.y-camera_y, self.width, self.total_height))

        # Draw road borders (excluding lane markers)
        pygame.draw.rect(screen, border_color, (self.x, self.y-camera_y, border_width, self.total_height))
        pygame.draw.rect(screen, border_color, (self.x + self.width - border_width, self.y-camera_y, border_width, self.total_height))

        # Draw dashed lines for inner lanes
        dash_length = 20
        for i in range(1, self.lane_count):
            x = self.x + lane_width * i
            for y in range(0, self.total_height, dash_length * 2):
                pygame.draw.rect(screen, lane_color, (x - 5 // 2, y+self.y-camera_y, 5, dash_length))
