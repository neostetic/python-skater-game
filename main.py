import time

import pygame
import pyautogui

pygame.init()

# windowWidth = pyautogui.size().width
# windowHeight = pyautogui.size().height
windowWidth = 1024
windowHeight = 768
windowBorder = 0

win = pygame.display.set_mode((windowWidth, windowHeight))

scaler = 2.5
player1img = pygame.image.load("assets/p1_default.png").convert_alpha()
player1DefaultImg = pygame.image.load("assets/p1_default.png").convert_alpha()
player1JumpImg = pygame.image.load("assets/p1_jump.png").convert_alpha()
playerWidth = player1img.get_width() * scaler
playerHeight = player1img.get_height() * scaler
skateImg0 = pygame.image.load("assets/sk_default.png").convert_alpha()
skateImg = skateImg0
skateImg1 = pygame.image.load("assets/sk_kickflip_1.png").convert_alpha()
skateImg2 = pygame.image.load("assets/sk_kickflip_2.png").convert_alpha()
skateImg3 = pygame.image.load("assets/sk_kickflip_3.png").convert_alpha()
skateImg4 = pygame.image.load("assets/sk_kickflip_4.png").convert_alpha()
skateImg5 = pygame.image.load("assets/sk_kickflip_5.png").convert_alpha()
skateImg6 = pygame.image.load("assets/sk_kickflip_6.png").convert_alpha()
skateWidth = skateImg.get_width() * scaler
skateHeight = skateImg.get_height() * scaler
streetDrivewayImg = pygame.image.load("assets/bg_street_road_v2.png").convert_alpha()
streetDrivewayWidth = streetDrivewayImg.get_width() * scaler
streetDrivewayHeight = streetDrivewayImg.get_height() * scaler
streetCityImg = pygame.image.load("assets/bg_street_city.png").convert_alpha()
streetCityWidth = streetCityImg.get_width() * scaler
streetCityHeight = streetCityImg.get_height() * scaler
streetBackgroundImg = pygame.image.load("assets/bg_street_background_1.png").convert_alpha()
streetBackgroundWidth = streetBackgroundImg.get_width() * scaler
streetBackgroundHeight = streetBackgroundImg.get_height() * scaler
coneImg = pygame.image.load("assets/en_cone.png").convert_alpha()
coneWidth = coneImg.get_width() * scaler
coneHeight = coneImg.get_height() * scaler
streetDrivewayScrollX = 0
streetCityScrollX = 0
streetBackground1ScrollX = 0
scrollVelocity = 1 * scaler
scrollVelocityMultiplier = 1
gameBackground = (85, 123, 153)
playerVel = 1 * scaler
player1x = windowWidth // 2 - playerWidth // 2
player1y = windowHeight - streetDrivewayHeight
playerXVel = 0
playerYVel = 0
counter = 0
isPlayer1Jumping = False
run = True

clock = pygame.time.Clock()


def getVelocity():
    return playerVel


def getGameVelocity(multiplier):
    return scrollVelocity * multiplier


def getPlayerJumpPosition():
    if isPlayer1Jumping:
        return player1y + (-4 * scaler)
    else:
        return player1y


def getPlayerSkatePosition():
    if isPlayer1Jumping:
        return player1y + (20 * scaler)
    else:
        return player1y + (22 * scaler)


while run:
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps() :.1f} fps')
    #    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    if (keys[pygame.K_SPACE]) and 0 < player1x < windowWidth - playerWidth and windowHeight - streetDrivewayHeight - playerHeight + skateHeight // 2 < player1y < windowHeight - playerHeight - skateHeight // 2:
        counter += 0.25
        isPlayer1Jumping = True
        isPlayer1PerformingATrick = True
        player1img = player1JumpImg
        player1x = player1x + playerXVel
        player1y = player1y + playerYVel
        if counter % 7 == 0:
            skateImg = skateImg0
        elif counter % 7 == 1:
            skateImg = skateImg1
        elif counter % 7 == 2:
            skateImg = skateImg2
        elif counter % 7 == 3:
            skateImg = skateImg3
        elif counter % 7 == 4:
            skateImg = skateImg4
        elif counter % 7 == 5:
            skateImg = skateImg5
        elif counter % 7 == 6:
            skateImg = skateImg6
    else:
        counter = 0
        skateImg = skateImg0
        isPlayer1PerformingATrick = False
        if keys[pygame.K_a] and player1x > 0:
            player1x -= getVelocity() * 1.5
            playerXVel = -getVelocity() * 1.5
        elif keys[pygame.K_d] and player1x < windowWidth - playerWidth:
            player1x += getVelocity()
            playerXVel = getVelocity()
        else:
            playerXVel = 0
        if keys[pygame.K_w] and player1y > windowHeight - streetDrivewayHeight - playerHeight + skateHeight // 2:
            player1y -= getVelocity()
            playerYVel = -getVelocity()
        elif keys[pygame.K_s] and player1y < windowHeight - playerHeight - skateHeight // 2:
            player1y += getVelocity()
            playerYVel = getVelocity()
        else:
            playerYVel = 0
        isPlayer1Jumping = False
        player1img = player1DefaultImg

    win.fill((255, 0, 0))
    border = pygame.draw.rect(win, gameBackground, (
        windowBorder, windowBorder, windowWidth - 2 * windowBorder, windowHeight - 2 * windowBorder))

    streetDrivewayScrollX -= getGameVelocity(scrollVelocityMultiplier)
    if -streetDrivewayScrollX == streetDrivewayWidth:
        streetDrivewayScrollX = 0

    streetCityScrollX -= getGameVelocity(scrollVelocityMultiplier)
    if -streetCityScrollX == streetCityWidth:
        streetCityScrollX = 0

    streetDriveway = pygame.draw.rect(win, (255, 0, 255), (
        0, windowHeight - streetDrivewayHeight, streetDrivewayWidth, streetDrivewayHeight))
    streetDrivewayImg = pygame.transform.scale(streetDrivewayImg, (streetDrivewayWidth, streetDrivewayHeight))
    streetDrivewayImgSecond = pygame.transform.scale(streetDrivewayImg, (streetDrivewayWidth, streetDrivewayHeight))

    streetCity = pygame.draw.rect(win, gameBackground, (
        0, windowHeight - streetCityHeight - streetDrivewayHeight, streetCityWidth, streetCityHeight))
    streetCityImg = pygame.transform.scale(streetCityImg, (streetCityWidth, streetCityHeight))
    streetCityImgSecond = pygame.transform.scale(streetCityImg, (streetCityWidth, streetCityHeight))

    player1 = pygame.draw.rect(win, gameBackground, (player1x, player1y, playerWidth, playerHeight))
    player1img = pygame.transform.scale(player1img, (playerWidth, playerHeight))
    player1skate = pygame.draw.rect(win, (255, 255, 0), (player1x, player1y + (22 * scaler), skateWidth, skateHeight))
    skateImg = pygame.transform.scale(skateImg, (skateWidth, skateHeight))

    textString = "PlayerX: " + player1x.__str__() + "; PlayerY: " + player1y.__str__()
    pygame.font.init()
    my_font = pygame.font.SysFont('Monospace', 12)
    text_surface = my_font.render(textString, False, (0, 0, 0))

    # rendered
    win.blit(streetCityImg, (streetCityScrollX, streetCity.y))
    win.blit(streetCityImgSecond, (streetCityScrollX + streetCityWidth, streetCity.y))
    win.blit(streetDrivewayImg, (streetDrivewayScrollX, streetDriveway.y))
    win.blit(streetDrivewayImgSecond, (streetDrivewayScrollX + streetDrivewayWidth, streetDriveway.y))
    win.blit(skateImg, (player1skate.x, getPlayerSkatePosition()))
    win.blit(player1img, (player1x, getPlayerJumpPosition()))
    win.blit(text_surface, (0, 0))

    cone = pygame.draw.rect(win, (255, 0, 0), (500, 500, coneWidth, coneHeight * .3))
    coneImg = pygame.transform.scale(coneImg, (coneWidth, coneHeight))
    win.blit(coneImg, (cone.x, cone.y - coneHeight * .7))

    pygame.display.update()

pygame.quit()