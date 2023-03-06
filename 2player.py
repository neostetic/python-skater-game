import random
import pygame
import pyautogui

pygame.init()

windowWidth = pyautogui.size().width
windowHeight = pyautogui.size().height
# windowWidth = 1024
# windowHeight = 768
windowBorder = 0

win = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
# win = pygame.display.set_mode((windowWidth, windowHeight))

scaler = 5
gameBackground = (85, 123, 153)
playerWidth = 11 * scaler
playerHeight = 14 * scaler
playerVel = 8
player1Vel = playerVel
player2Vel = playerVel
player1x = windowWidth // 2 - playerWidth
player1y = windowHeight // 2
player2x = windowWidth // 2 + playerWidth
player2y = windowHeight // 2
player1points = 0
player2points = 0
player1flip = False
player2flip = False
goalWidth = 5*scaler
goalHeight = goalWidth
goalToWin = 15
run = True
isWinner = False
timing = 0

clock = pygame.time.Clock()


def getVelocity1():
    return player1Vel


def getVelocity2():
    return player2Vel


def getGoalX():
    return random.randrange(0, (windowWidth - goalWidth))


def getGoalY():
    return random.randrange(0, (windowHeight - goalHeight))


goalX = getGoalX()
goalY = getGoalY()

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

    timing = timing + 1
    player1img = pygame.image.load("player_1_f1.png").convert_alpha()
    player2img = pygame.image.load("player_2_f1.png").convert_alpha()
    if 20 >= timing >= 10:
        player1img = pygame.image.load("player_1_f2.png").convert_alpha()
        player2img = pygame.image.load("player_2_f2.png").convert_alpha()
    elif timing >= 20:
        timing = 0

    player1img = pygame.transform.flip(player1img, player1flip, False)
    player2img = pygame.transform.flip(player2img, player2flip, False)

    if not isWinner:
        if keys[pygame.K_a] and player1x > 0:
            player1x -= getVelocity1()
            player1flip = True
        if keys[pygame.K_d] and player1x < windowWidth - playerWidth:
            player1x += getVelocity1()
            player1flip = False
        if keys[pygame.K_w] and player1y > 0:
            player1y -= getVelocity1()
        if keys[pygame.K_s] and player1y < windowHeight - playerHeight:
            player1y += getVelocity1()
        if keys[pygame.K_LEFT] and player2x > 0:
            player2x -= getVelocity2()
            player2flip = True
        if keys[pygame.K_RIGHT] and player2x < windowWidth - playerWidth:
            player2x += getVelocity2()
            player2flip = False
        if keys[pygame.K_UP] and player2y > 0:
            player2y -= getVelocity2()
        if keys[pygame.K_DOWN] and player2y < windowHeight - playerHeight:
            player2y += getVelocity2()

    if keys[pygame.K_RETURN]:
        player1points = 0
        player2points = 0
        isWinner = 0
        player1x = windowWidth // 2 - playerWidth
        player1y = windowHeight // 2
        player2x = windowWidth // 2 + playerWidth
        player2y = windowHeight // 2
        goalX = getGoalX()
        goalY = getGoalY()
    if keys[pygame.K_RCTRL]:
        goalX = getGoalX()
        goalY = getGoalY()

    pygame.mouse.set_visible(False)

    win.fill((255, 0, 0))
    border = pygame.draw.rect(win, gameBackground, (
        windowBorder, windowBorder, windowWidth - 2 * windowBorder, windowHeight - 2 * windowBorder))

    if not isWinner:
        pokeballImg = pygame.image.load("pokeball.png").convert_alpha()
        pokeballImg = pygame.transform.scale(pokeballImg, (goalWidth, goalHeight))
        pokeball = pygame.draw.rect(win, gameBackground, (goalX, goalY, goalWidth, goalHeight))
        player1 = pygame.draw.rect(win, gameBackground, (player1x, player1y, playerWidth, playerHeight))
        player2 = pygame.draw.rect(win, gameBackground, (player2x, player2y, playerWidth, playerHeight))
        player1img = pygame.transform.scale(player1img, (playerWidth, playerHeight))
        player2img = pygame.transform.scale(player2img, (playerWidth, playerHeight))
        win.blit(pokeballImg, (goalX, goalY))
        win.blit(player1img, (player1x, player1y))
        win.blit(player2img, (player2x, player2y))
        if player1.colliderect(pokeball):
            goalX = getGoalX()
            goalY = getGoalY()
            player1points = player1points + 1
        if player2.colliderect(pokeball):
            goalX = getGoalX()
            goalY = getGoalY()
            player2points = player2points + 1

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    my_font2 = pygame.font.SysFont('Comic Sans MS', 64)
    img = pygame.image.load("mouse.png").convert_alpha()
    img = pygame.transform.scale(img, (16*scaler/2, 16*scaler/2))
    text_player1 = my_font.render(f'Player1: {player1points}', False, (255, 0, 0))
    text_player2 = my_font.render(f'Player2: {player2points}', False, (0, 0, 255))
    text_info = my_font.render("press 'Enter' to restart", True, (64, 64, 64))
    text_win_rect = text_info.get_rect(center=((windowWidth / 2), (windowHeight - 100)))
    win.blit(text_player1, (25, 25))
    win.blit(text_player2, (windowWidth - 170, 25))
    win.blit(text_info, text_win_rect)
    win.blit(img, (pyautogui.position().x, pyautogui.position().y))

    if player1points >= goalToWin or player2points >= goalToWin:
        if player1points > player2points:
            text_win = my_font2.render("Player1 wins!", True, (255, 0, 0))
            text_win_rect = text_win.get_rect(center=(windowWidth / 2, windowHeight / 2))
            win.blit(text_win, text_win_rect)
        else:
            text_win = my_font2.render("Player2 wins!", True, (0, 0, 255))
            text_win_rect = text_win.get_rect(center=(windowWidth / 2, windowHeight / 2))
            win.blit(text_win, text_win_rect)
        isWinner = True
    pygame.display.update()

pygame.quit()
