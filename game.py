# basic func imports
import numpy
import pandas
import random

import pygame
from pygame.locals import *
import cv2

# local imports
from graph import *

def drawArcCv2(surf, color, center, radius, width, end_angle):
    circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
    circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
        (radius-width//2, radius-width//2), 0, 90, end_angle + 90, (*color, 255), width, lineType=cv2.LINE_AA) 
    circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center = center))

textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3
def drawText(surface, text, color, rect, font, align=textAlignLeft, aa=True, bkg=None):

    lineSpacing = -2
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

    listOfWords = str(text).split(" ")
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

def endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije):
    channel1.fadeout(5)

    endcard = pygame.image.load('resources/endcard/endcard.jpg')
    tryagaina = pygame.image.load('resources/endcard/tryagaina.png')
    tryagainh = pygame.image.load('resources/endcard/tryagainh.png')
    closea = pygame.image.load('resources/endcard/exita.png')
    closeh = pygame.image.load('resources/endcard/exith.png')
    font = pygame.font.Font("resources/Rubik.ttf", 30)

    for i in range(0, len(opcije)):
            if opcije[i][1] == 'T':
                ti = i

    if (counterquestion <= 4):
        string = "Nažalost ste samo stigli do " + str(counterquestion) + ". pitanja, a tačan odgovor je bio \"" + str(opcije[ti][0]) + "\""
    elif (counterquestion <= 9):
        string = "Stigli ste do " + str(counterquestion) + ". pitanja, a tačan odgovor je bio \"" + str(opcije[ti][0]) + "\""
    elif (counterquestion <= 14):
        string = "Zamalo do pobede. Stigli ste do " + str(counterquestion) + ". pitanja."
    else:
        string = "Čestitamo na pobedi!"

    text = font.render(string, True, (184, 193, 209))
    text_rect = text.get_rect (center = (width // 2, 340))

    run = True
    while run:
        posm = pygame.mouse.get_pos()

        window.blit(endcard, (0, 0))
        window.blit(text, text_rect)
        if posm[0] > 534 and posm[0] < 745 and posm[1] > 481 and posm[1] < 512:
            window.blit(tryagainh, (534, 481))
        else: 
            window.blit(tryagaina, (534, 481))
        if posm[0] > 534 and posm[0] < 745 and posm[1] > 520 and posm[1] < 551:
            window.blit(closeh, (534, 520))
        else: 
            window.blit(closea, (534, 520))
        pygame.display.update()

        for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if posm[0] > 534 and posm[0] < 745 and posm[1] > 481 and posm[1] < 512:
                            run = False
                            game(window, width, height, clock)
                        if posm[0] > 534 and posm[0] < 745 and posm[1] > 520 and posm[1] < 551:
                            pygame.quit()
                            exit()

def game(window, width, height, clock):
    # resource load
    bg_music1 = pygame.mixer.Sound("resources/game/music/bg_music1.ogg")
    true1 = pygame.mixer.Sound("resources/game/music/true1.ogg")
    false1 = pygame.mixer.Sound("resources/game/music/false1.ogg")
    h1ogg = pygame.mixer.Sound("resources/game/music/asktheaudience.ogg")
    h2ogg = pygame.mixer.Sound("resources/game/music/50-50.ogg")
    h3ogg = pygame.mixer.Sound("resources/game/music/switcharoo.ogg")
    h4ogg = pygame.mixer.Sound("resources/game/music/doubletime.ogg")

    bg_img = pygame.image.load('resources/game/background.jpg')
    hover = pygame.image.load('resources/game/answer_hover/answer_hover.png')

    help1a = pygame.image.load('resources/game/help/asktheaudience/asktheaudience.png')
    help1h = pygame.image.load('resources/game/help/asktheaudience/asktheaudience_hover.png')
    help1c = pygame.image.load('resources/game/help/asktheaudience/asktheaudience_c.png')
    help2a = pygame.image.load('resources/game/help/50-50/50-50.png')
    help2h = pygame.image.load('resources/game/help/50-50/50-50_hover.png')
    help2c = pygame.image.load('resources/game/help/50-50/50-50_c.png')
    help3a = pygame.image.load('resources/game/help/switcharoo/switcharoo.png')
    help3h = pygame.image.load('resources/game/help/switcharoo/switcharoo_hover.png')
    help3c = pygame.image.load('resources/game/help/switcharoo/switcharoo_c.png')
    help4a = pygame.image.load('resources/game/help/doubletime/doubletime.png')
    help4h = pygame.image.load('resources/game/help/doubletime/doubletime_hover.png')
    help4c = pygame.image.load('resources/game/help/doubletime/doubletime_c.png')
        
    quita = pygame.image.load('resources/game/quit/quit.png')
    quith = pygame.image.load('resources/game/quit/quit_hover.png')

    currentq = [pygame.image.load('resources/game/currentq/currentq_1.png'),
        pygame.image.load('resources/game/currentq/currentq_2.png'),
        pygame.image.load('resources/game/currentq/currentq_3.png'),
        pygame.image.load('resources/game/currentq/currentq_4.png'),
        pygame.image.load('resources/game/currentq/currentq_5.png'),
        pygame.image.load('resources/game/currentq/currentq_6.png'),
        pygame.image.load('resources/game/currentq/currentq_7.png'),
        pygame.image.load('resources/game/currentq/currentq_8.png'),
        pygame.image.load('resources/game/currentq/currentq_9.png'),
        pygame.image.load('resources/game/currentq/currentq_10.png'),
        pygame.image.load('resources/game/currentq/currentq_11.png'),
        pygame.image.load('resources/game/currentq/currentq_12.png'),
        pygame.image.load('resources/game/currentq/currentq_13.png'),
        pygame.image.load('resources/game/currentq/currentq_14.png'),
        pygame.image.load('resources/game/currentq/currentq_15.png')]

    # font load
    timerfont = pygame.font.Font("resources/Rubik.ttf", 130)
    qafont = pygame.font.Font("resources/Rubik.ttf", 20)

    # timer setup
    counterclock = 30
    cc = 30
    text = timerfont.render(str(counterclock), True, (184, 193, 209))

    # question load
    qna1 = pandas.read_excel("resources/pitanja.xlsx", "11", usecols = "A,B,C,D,E")
    qnad1 = qna1.to_dict('index')
    qna3 = pandas.read_excel("resources/pitanja.xlsx", "6", usecols = "A,B,C,D,E")
    qnad3 = qna3.to_dict('index')
    qna6 = pandas.read_excel("resources/pitanja.xlsx", "3", usecols = "A,B,C,D,E")
    qnad6 = qna6.to_dict('index')
    qna11 = pandas.read_excel("resources/pitanja.xlsx", "1", usecols = "A,B,C,D,E")
    qnad11 = qna11.to_dict('index')
    random.shuffle(qnad1)
    random.shuffle(qnad3)
    random.shuffle(qnad6)
    random.shuffle(qnad11)


    # intro
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

    # audio channel init
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)
    channel3 = pygame.mixer.Channel(2)

    channel1.play(bg_music1, -1)

    # default temp values load
    counterquestion = 0
    dcao = 0
    graph = False
    running = True
    shuffle = True
    h1 = False
    h2 = False
    h3 = False
    h4 = False
    starttime = pygame.time.get_ticks()

    while running:
        posm = pygame.mouse.get_pos()
        counterclock = cc - (pygame.time.get_ticks()-starttime)/1000
        if int(counterclock) >= 0:
            text = timerfont.render(str(int(counterclock)), True, (184, 193, 209))
        else: endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije)

        window.blit(bg_img,(0,0))
        text_rect = text.get_rect (center = (width // 2, 200))
        window.blit(text, text_rect)
        if(counterclock > 0.1):
            drawArcCv2(window, (234, 138, 0), (640, 202), 116, 4, 360*counterclock/cc)
        if(counterquestion == 14):
            window.blit(currentq[14], (1107,51))
        elif(counterquestion < 14):
            window.blit(currentq[counterquestion], (1107,55))
        else: endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije)
        
        if(counterquestion == dcao):
            if(counterquestion <= 2):
                q = qnad1[counterquestion]["PITANJE"]
                opcije = [[qnad1[counterquestion]["OPCIJA1"],'T'], [qnad1[counterquestion]["OPCIJA2"],'F'], [qnad1[counterquestion]["OPCIJA3"],'F'], [qnad1[counterquestion]["OPCIJA4"],'F']]
            elif(counterquestion > 2 and counterquestion <= 5):
                q = qnad3[counterquestion]["PITANJE"]
                opcije = [[qnad3[counterquestion]["OPCIJA1"],'T'], [qnad3[counterquestion]["OPCIJA2"],'F'], [qnad3[counterquestion]["OPCIJA3"],'F'], [qnad3[counterquestion]["OPCIJA4"],'F']]
            elif(counterquestion > 5 and counterquestion <= 10):
                q = qnad6[counterquestion]["PITANJE"]
                opcije = [[qnad6[counterquestion]["OPCIJA1"],'T'], [qnad6[counterquestion]["OPCIJA2"],'F'], [qnad6[counterquestion]["OPCIJA3"],'F'], [qnad6[counterquestion]["OPCIJA4"],'F']]
            elif(counterquestion > 10 and counterquestion <= 14):
                q = qnad11[counterquestion]["PITANJE"]
                opcije = [[qnad11[counterquestion]["OPCIJA1"],'T'], [qnad11[counterquestion]["OPCIJA2"],'F'], [qnad11[counterquestion]["OPCIJA3"],'F'], [qnad11[counterquestion]["OPCIJA4"],'F']]
            dcao += 1
        if(shuffle):
            random.shuffle(opcije)
            shuffle = False

        q_rect = pygame.Rect(240, 430, 1045-240, 480-420)
        drawText(window, q, "white", q_rect, qafont, textAlignCenter, True)

        #o1 = qnad[r]["OPCIJA1"]
        o1_rect = pygame.Rect(224, 561, 594-224, 30)
        if posm[0] > 224 and posm[0] < 594 and posm[1] > 548 and posm[1] < 598 and opcije[0][0] != '':
            window.blit(hover, (200, 548))
            drawText(window, opcije[0][0], "black", o1_rect, qafont, textAlignCenter, True)
        else:
            drawText(window, opcije[0][0], "white", o1_rect, qafont, textAlignCenter, True)
        #o2 = qnad[r]["OPCIJA2"]
        o2_rect = pygame.Rect(224, 633, 594-224, 30)
        if posm[0] > 224 and posm[0] < 594 and posm[1] > 620 and posm[1] < 669 and opcije[2][0] != '':
            window.blit(hover, (200, 619))
            drawText(window, opcije[2][0], "black", o2_rect, qafont, textAlignCenter, True)
        else:
            drawText(window, opcije[2][0], "white", o2_rect, qafont, textAlignCenter, True)
        #o3 = qnad[r]["OPCIJA3"]
        o3_rect = pygame.Rect(690, 561, 594-224, 30)
        if posm[0] > 690 and posm[0] < 690+(594-224) and posm[1] > 548 and posm[1] < 598 and opcije[1][0] != '':
            window.blit(hover, (664, 548))
            drawText(window, opcije[1][0], "black", o3_rect, qafont, textAlignCenter, True)
        else:
            drawText(window, opcije[1][0], "white", o3_rect, qafont, textAlignCenter, True)
        #o4 = qnad[r]["OPCIJA4"]
        o4_rect = pygame.Rect(690, 633, 594-224, 30)
        if posm[0] > 690 and posm[0] < 690+(594-224) and posm[1] > 620 and posm[1] < 669 and opcije[3][0] != '':
            window.blit(hover, (664, 619))    
            drawText(window, opcije[3][0], "black", o4_rect, qafont, textAlignCenter, True)
        else:
            drawText(window, opcije[3][0], "white", o4_rect, qafont, textAlignCenter, True)
        
        if h1 == False:
            if posm[0] > 497 and posm[0] < 497+62 and posm[1] > 351 and posm[1] < 386:
                window.blit(help1h,(497,351))
            else: window.blit(help1a,(497,351))
        else: window.blit(help1c,(497,351))
        if h2 == False:
            if posm[0] > 573 and posm[0] < 573+62 and posm[1] > 351 and posm[1] < 386:
                window.blit(help2h,(573,351))
            else: window.blit(help2a,(573,351))
        else: window.blit(help2c,(573,351))
        if h3 == False:
            if posm[0] > 649 and posm[0] < 649+62 and posm[1] > 351 and posm[1] < 386:
                window.blit(help3h,(649,351))
            else: window.blit(help3a,(649,351))
        else: window.blit(help3c,(649,351))
        if h4 == False:
            if posm[0] > 724 and posm[0] < 724+62 and posm[1] > 351 and posm[1] < 386:
                window.blit(help4h,(724,351))
            else: window.blit(help4a,(724,351))
        else: window.blit(help4c,(724,351))

        if h1 == True and graph == True:
            window.blit(pygame.image.load('resources/figure.png'), (6,3))

        if posm[0] > 1106 and posm[0] < 1106+143 and posm[1] > 12 and posm[1] < 12 + 24:
                window.blit(quith,(1106,12))
        else: window.blit(quita,(1106,12))

        pygame.display.update()

        for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if posm[0] > 224 and posm[0] < 594 and posm[1] > 548 and posm[1] < 598 and opcije[0][0] != '':
                            shuffle = True
                            counterquestion = counterquestion + 1
                            starttime = pygame.time.get_ticks()
                            cc = 30
                            graph = False
                            channel1.pause()
                            if opcije[0][1] == 'F':
                                channel2.play(false1, 0)
                                endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije)
                            else:
                                channel2.play(true1, 0)
                                channel1.unpause()
                        if posm[0] > 224 and posm[0] < 594 and posm[1] > 620 and posm[1] < 669 and opcije[2][0] != '':
                            shuffle = True
                            counterquestion = counterquestion + 1
                            starttime = pygame.time.get_ticks()
                            cc = 30
                            graph = False
                            channel1.pause()
                            if opcije[2][1] == 'F':
                                channel2.play(false1, 0)
                                endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije)
                            else:
                                channel2.play(true1, 0)
                                channel1.unpause()
                        if posm[0] > 690 and posm[0] < 690+(594-224) and posm[1] > 548 and posm[1] < 598 and opcije[1][0] != '':
                            shuffle = True
                            counterquestion = counterquestion + 1
                            starttime = pygame.time.get_ticks()
                            cc = 30
                            graph = False
                            channel1.pause()
                            if opcije[1][1] == 'F':
                                channel2.play(false1, 0)
                                endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije)
                            else:
                                channel2.play(true1, 0)
                                channel1.unpause()
                        if posm[0] > 690 and posm[0] < 690+(594-224) and posm[1] > 620 and posm[1] < 669 and opcije[3][0] != '':
                            shuffle = True
                            counterquestion = counterquestion + 1
                            starttime = pygame.time.get_ticks()
                            cc = 30
                            graph = False
                            channel1.pause()
                            if opcije[3][1] == 'F':
                                channel2.play(false1, 0)
                                endcard(pygame, window, width, height, counterquestion, channel1, clock, opcije)
                            else:
                                channel2.play(true1, 0)
                                channel1.unpause()

                        if posm[0] > 497 and posm[0] < 497+62 and posm[1] > 351 and posm[1] < 386 and h1 == False:
                            channel3.play(h1ogg, 0)
                            graph = True
                            h1 = True
                            starttime = pygame.time.get_ticks()+1000 - (cc/2)*1000
                            makegraph(opcije)
                        if posm[0] > 573 and posm[0] < 573+62 and posm[1] > 351 and posm[1] < 386 and h2 == False:
                            channel3.play(h2ogg, 0)
                            h2 = True
                            rn = random.sample(opcije,2)
                            while rn[0][1]=='T' or rn[1][1]=='T':
                                rn = random.sample(opcije,2)
                            for i in range(0, len(opcije)):
                                if(rn[0] == opcije[i] or rn[1] == opcije[i]):
                                    opcije[i][0] = ''
                        if posm[0] > 649 and posm[0] < 649+62 and posm[1] > 351 and posm[1] < 386 and h3 == False:
                            channel3.play(h3ogg, 0)
                            cc = 30
                            h3 = True
                            graph = False
                            if(counterquestion <= 2):
                                pom = qnad1[counterquestion]
                                qnad1[counterquestion] = qnad1[15]
                                qnad1[15] = pom
                            elif(counterquestion > 2 and counterquestion <= 5):
                                pom = qnad3[counterquestion]
                                qnad3[counterquestion] = qnad3[15]
                                qnad3[15] = pom
                            elif(counterquestion > 5 and counterquestion <= 10):
                                pom = qnad6[counterquestion]
                                qnad6[counterquestion] = qnad6[15]
                                qnad6[15] = pom
                            elif(counterquestion > 10 and counterquestion <= 14):
                                pom = qnad11[counterquestion]
                                qnad11[counterquestion] = qnad11[15]
                                qnad11[15] = pom
                            dcao = counterquestion
                            shuffle = True
                            starttime = pygame.time.get_ticks()
                        if posm[0] > 724 and posm[0] < 724+62 and posm[1] > 351 and posm[1] < 386 and h4 == False:
                            channel3.play(h4ogg, 0)
                            h4 = True
                            cc = cc * 2 - (30 - counterclock)

                        if posm[0] > 1106 and posm[0] < 1106+143 and posm[1] > 12 and posm[1] < 12 + 24:
                            exit()
