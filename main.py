# local imports
from game import *

# pygame init & other pygame properties
pygame.init()
width = 1280
height = 720
window = pygame.display.set_mode((width,height))
pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()

# call
game(window, width, height, clock)