import pygame
from game import Game

pygame.init()

screen_info = pygame.display.Info()
w = screen_info.current_w
h = screen_info.current_h

# Set display mode
screen = pygame.display.set_mode((w, h))  # (800, 600)/(1280, 720)/(1024, 768) res for testing

clock = pygame.time.Clock()

# Define the center of the screen
window_size = pygame.Vector2(screen.get_width(), screen.get_height())

# Set the caption of the screen
pygame.display.set_caption("World Conquest")

game = Game(screen, clock, window_size)
game.run()

pygame.display.flip()

pygame.quit()
