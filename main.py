import pygame  # Import the pygame library for game development
from game import Game  # Import the custom Game class
import tkinter as tk  # Import tkinter for screen resolution retrieval

# Grab the resolution of the screen
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Initialize pygame
pygame.init()

# Set display mode
# Create the game window with the retrieved resolution
screen = pygame.display.set_mode((screen_width, screen_height))
# (800, 600)/(1280, 720)/(1024x768) res for testing

# Create a Clock object to control frame rate
clock = pygame.time.Clock()

# Define the center of the screen
window_size = pygame.Vector2(screen.get_width(), screen.get_height())

# Set the caption of the screen
pygame.display.set_caption("World Conquest")

# Create an instance of the Game class
game = Game(screen, clock, window_size)
# Run the game loop
game.run()

# Update the display
pygame.display.flip()

# Quit pygame
pygame.quit()

# Finished
