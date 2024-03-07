import pygame
from game import Game
import tkinter as tk

#Grab the resolution of the screen
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pygame.init()

# Set display mode
screen = pygame.display.set_mode((screen_width, screen_height))  # (800, 600)/(1280, 720)/(1024x768) res for testing

clock = pygame.time.Clock()

# Define the center of the screen
window_size = pygame.Vector2(screen.get_width(), screen.get_height())

# Set the caption of the screen
pygame.display.set_caption("World Conquest")

game = Game(screen, clock, window_size)
game.run()

pygame.display.flip()

pygame.quit()
