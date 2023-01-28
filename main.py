# local imports
from game import *

# pygame init & other pygame properties
pygame.init()
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN])
width = 1280
height = 720
flags = FULLSCREEN | DOUBLEBUF | HWSURFACE
window = pygame.display.set_mode((width,height), flags, 16)
clock = pygame.time.Clock()

# call
game(window, width, height, clock)