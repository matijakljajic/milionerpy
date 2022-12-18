import pygame
from pygame.locals import *
import cv2
import numpy
import pandas
import random
import textwrap

pygame.init()
width = 1280
height = 720
window = pygame.display.set_mode((width,height))
pygame.display.toggle_fullscreen()

clock = pygame.time.Clock()
timerfont = pygame.font.Font("resources/Rubik.ttf", 130)
qafont = pygame.font.Font("resources/Rubik.ttf", 20)
counterclock = 30
text = timerfont.render(str(counterclock), True, (184, 193, 209))
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)

qna = pandas.read_excel("resources/Millionaire-Questions.xlsx", "sheet", usecols = "A,B,C,D,E")
qnad = qna.to_dict('index')

bg_img = pygame.image.load('resources/game/background.jpg')
hover = pygame.image.load('resources/game/answer_hover/answer_hover.png')

#textwrap

textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3

def drawText(surface, text, color, rect, font, align=textAlignLeft, aa=True, bkg=None):
    lineSpacing = -2
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

    listOfWords = text.split(" ")
    if bkg:
        imageList = [font.render(word, 1, color, bkg) for word in listOfWords]
        for image in imageList: image.set_colorkey(bkg)
    else:
        imageList = [font.render(word, aa, color) for word in listOfWords]

    maxLen = rect[2]
    lineLenList = [0]
    lineList = [[]]
    for image in imageList:
        width = image.get_width()
        lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
        if len(lineList[-1]) == 0 or lineLen <= maxLen:
            lineLenList[-1] += width
            lineList[-1].append(image)
        else:
            lineLenList.append(width)
            lineList.append([image])

    lineBottom = rect[1]
    lastLine = 0
    for lineLen, lineImages in zip(lineLenList, lineList):
        lineLeft = rect[0]
        if align == textAlignRight:
            lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages)-1)
        elif align == textAlignCenter:
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages)-1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            spaceWidth = (rect[2] - lineLen) // (len(lineImages)-1)
        if lineBottom + fontHeight > rect[1] + rect[3]:
            break
        lastLine += 1
        for i, image in enumerate(lineImages):
            x, y = lineLeft + i*spaceWidth, lineBottom
            surface.blit(image, (round(x), y))
            lineLeft += image.get_width() 
        lineBottom += fontHeight + lineSpacing

    if lastLine < len(lineList):
        drawWords = sum([len(lineList[i]) for i in range(lastLine)])
        remainingText = ""
        for text in listOfWords[drawWords:]: remainingText += text + " "
        return remainingText
    return ""



def drawArcCv2(surf, color, center, radius, width, end_angle):
    circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
    circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
        (radius-width//2, radius-width//2), 0, 90, end_angle + 90, (*color, 255), width, lineType=cv2.LINE_AA) 
    circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center = center))


counterquestion = 1
run = True
h1 = False
h2 = True
h3 = True 
h4 = True
while run:
    posm = pygame.mouse.get_pos()
    r = counterquestion #promeniti kasnije u random.randint(0, len(qnad))

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == timer_event:
            counterclock -= 1
            text = timerfont.render(str(counterclock), True, (184, 193, 209))
            if counterclock == 0:
                text = timerfont.render("0", True, (184, 193, 209))
                pygame.time.set_timer(timer_event, 0)                

    window.blit(bg_img,(0,0))
    text_rect = text.get_rect (center = (width // 2, 200))
    window.blit(text, text_rect)
    if(counterclock != 0):
        drawArcCv2(window, (234, 138, 0), (640, 202), 116, 4, 360*counterclock/30)
    currentq = pygame.image.load('resources/game/currentq/currentq_' + str(counterquestion) + ".png")
    if(counterquestion == 15):
        window.blit(currentq, (1107,75))
    else:
        window.blit(currentq, (1107,71))
    q = qnad[r]["PITANJE"]
    q_rect = pygame.Rect(387, 430, 895-387, 480-420)
    drawText(window, q, "white", q_rect, qafont, textAlignCenter, True)

    o1 = qnad[r]["OPCIJA1"]
    o1_rect = pygame.Rect(224, 561, 594-224, 30)
    if posm[0] > 224 and posm[0] < 594 and posm[1] > 561 and posm[1] < 591:
        window.blit(hover, (200, 548))
        drawText(window, o1, "black", o1_rect, qafont, textAlignCenter, True)
    else:
        drawText(window, o1, "white", o1_rect, qafont, textAlignCenter, True)
    o2 = qnad[r]["OPCIJA2"]
    o2_rect = pygame.Rect(224, 633, 594-224, 30)
    if posm[0] > 224 and posm[0] < 594 and posm[1] > 633 and posm[1] < 663:
        window.blit(hover, (200, 619))
        drawText(window, o2, "black", o2_rect, qafont, textAlignCenter, True)
    else:
        drawText(window, o2, "white", o2_rect, qafont, textAlignCenter, True)
    o3 = qnad[r]["OPCIJA3"]
    o3_rect = pygame.Rect(690, 561, 594-224, 30)
    if posm[0] > 690 and posm[0] < 690+(594-224) and posm[1] > 561 and posm[1] < 591:
        window.blit(hover, (664, 548))
        drawText(window, o3, "black", o3_rect, qafont, textAlignCenter, True)
    else:
        drawText(window, o3, "white", o3_rect, qafont, textAlignCenter, True)
    o4 = qnad[r]["OPCIJA4"]
    o4_rect = pygame.Rect(690, 633, 594-224, 30)
    if posm[0] > 690 and posm[0] < 690+(594-224) and posm[1] > 633 and posm[1] < 663:
        window.blit(hover, (664, 619))    
        drawText(window, o4, "black", o4_rect, qafont, textAlignCenter, True)
    else:
        drawText(window, o4, "white", o4_rect, qafont, textAlignCenter, True)


    pygame.display.update()


    for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if posm[0] > 224 and posm[0] < 594 and posm[1] > 561 and posm[1] < 591:
                        h1 = True
                    else: 
                        h1 = False


pygame.quit()
exit()