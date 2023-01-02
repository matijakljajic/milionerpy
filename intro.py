# basic func imports
import pygame
from pygame.locals import *
import cv2

def intro(window, clock):
    
    audio = pygame.mixer.Sound("resources/game/intro/intro.ogg")
    video = cv2.VideoCapture("resources/game/intro/intro.mp4")

    channel = pygame.mixer.Channel(2)

    success, camera_image = video.read()
    channel.play(audio)

    run = success
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    run = False
                    channel.stop()
        
        success, camera_image = video.read()
        if success:
            camera_surf = pygame.image.frombuffer(camera_image.tobytes(), camera_image.shape[1::-1], "BGR")
        else:
            run = False
        window.blit(camera_surf, (0, 0))
        pygame.display.update()