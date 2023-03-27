from entity.entity import Entity

import pygame


class Game:
    pygame = pygame

    def __init__(self, scaler, width, height, isFullscreen):
        self.win = None
        self.scaler = scaler
        self.width = width
        self.height = height
        self.isFullscreen = isFullscreen
        self.isRunning = True
        self.keys = None
        self.entities = None
        self.windowBorder = 0

    def setWindowBorder(self, number):
        self.windowBorder = number

    def drawEntity(self, entity):
        img = Game.pygame.transform.scale(entity.image, (entity.width * self.scaler, entity.height * self.scaler))
        self.win.blit(img, (entity.x, entity.y))

    def moveEntity(self, entity, speed, threshold, reset):
        entity.x = entity.x + speed
        if speed < 0:
            if entity.x < threshold:
                entity.x = reset
        else:
            if entity.x > threshold:
                entity.x = reset
        self.drawEntity(entity)

    def isCollision(self, rect1, rect2):
        x1 = rect1.x < rect2.x + rect2.width * self.scaler
        x2 = rect1.x + rect1.width * self.scaler > rect2.x
        y1 = rect1.y < rect2.y + rect2.height * self.scaler
        y2 = rect1.height * self.scaler + rect1.y > rect2.y
        if x1 and x2 and y1 and y2:
            return True
        else:
            return False

    def drawCollision(self, entity):
        return pygame.draw.rect(self.win, (255, 0, 0),
                                (entity.x, entity.y, entity.width * self.scaler, entity.height * self.scaler))

    def drawText(self, string, font, color, x, y):
        Game.pygame.font.init()
        entity = font.render(string, False, color)
        self.win.blit(entity, (x, y))

    def keyhandlerMoveEntity(self, entity, velocity, threshold_entity):
        velocity = velocity * self.scaler
        if self.keys[Game.pygame.K_a] and entity.x > 0:
            entity.x -= velocity * 1.5
        elif self.keys[Game.pygame.K_d] and entity.x < self.width - entity.width * self.scaler:
            entity.x += velocity
        if self.keys[
            Game.pygame.K_w] and entity.y > self.height - threshold_entity.height * self.scaler - entity.height * self.scaler * .75:
            entity.y -= velocity
        elif self.keys[Game.pygame.K_s] and entity.y < self.height - entity.height * self.scaler:
            entity.y += velocity

    def start(self):
        Game.pygame.init()

        self.keys = Game.pygame.key.get_pressed()
        if self.isFullscreen:
            self.win = Game.pygame.display.set_mode((self.width, self.height), Game.pygame.FULLSCREEN, vsync=1)
        else:
            self.win = Game.pygame.display.set_mode((self.width, self.height), vsync=1)
        skater = Entity(Game.pygame, "assets/p1_default.png", 0, 0)
        skater.x = skater.width * self.scaler
        skater.y = self.height - skater.height * self.scaler * 2
        skate = Entity(Game.pygame, "assets/sk_default.png", 0, 0)
        driveway = Entity(Game.pygame, "assets/bg_street_road_v2.png", self.scaler, 0)
        driveway.y = self.height - driveway.height * self.scaler
        drivewaySecond = Entity(Game.pygame, "assets/bg_street_road_v2.png", 0, 0)
        drivewaySecond.y = self.height - driveway.height * self.scaler
        invisibleCoin = Entity(Game.pygame, "assets/en_coin_1.png", 0, -99999)
        coinEntities = [
            Entity(Game.pygame, "assets/en_coin_1.png", 0, 0),
            Entity(Game.pygame, "assets/en_coin_2.png", 0, 0),
            Entity(Game.pygame, "assets/en_coin_3.png", 0, 0),
            Entity(Game.pygame, "assets/en_coin_4.png", 0, 0)
        ]
        background = Entity(Game.pygame, "assets/bg_street_city.png", self.scaler, 0)
        backgroundSecond = Entity(Game.pygame, "assets/bg_street_city.png", 0, 0)
        background.y = self.height - driveway.height * self.scaler - background.height * self.scaler + self.scaler * 2
        backgroundSecond.y = self.height - driveway.height * self.scaler - background.height * self.scaler + self.scaler * 2

        speed = 1
        distance = 0
        coins = 0
        my_font = Game.pygame.font.Font('./assets/joystix.otf', 32)
        clock = Game.pygame.time.Clock()

        timer = 0
        timerTickrate = 0
        timerThreshold = 12

        while self.isRunning:
            clock.tick(60)
            Game.pygame.display.set_caption(f'{clock.get_fps() :.1f} fps')
            for event in Game.pygame.event.get():
                if event.type == Game.pygame.QUIT:
                    self.isRunning = False
            self.keys = Game.pygame.key.get_pressed()
            self.win.fill((0, 0, 0))
            Game.pygame.draw.rect(self.win, (85, 123, 153), (
                self.windowBorder, self.windowBorder, self.width - 2 * self.windowBorder,
                self.height - 2 * self.windowBorder))

            timerTickrate = timerTickrate + 1
            if timerTickrate >= timerThreshold:
                timer = timer + 1
                timerTickrate = 0

            # for entity in self.entities:
            #     print(entity)

            speed = speed * 1.001
            distance = distance + speed

            self.moveEntity(invisibleCoin, -speed * self.scaler, 0, self.width)

            self.drawEntity(background)
            self.moveEntity(driveway, -speed * self.scaler, -driveway.width * self.scaler, 0)
            self.moveEntity(drivewaySecond, -speed * self.scaler, 0, driveway.width * self.scaler)
            self.moveEntity(background, -speed * self.scaler, -background.width * self.scaler, 0)
            self.moveEntity(backgroundSecond, -speed * self.scaler, 0, backgroundSecond.width * self.scaler)

            skate.x = skater.x
            skate.y = skater.y + skater.height * self.scaler * 0.9
            self.drawEntity(skate)
            self.drawEntity(skater)
            self.keyhandlerMoveEntity(skater, 2, driveway)

            coin = coinEntities[timer % len(coinEntities)]
            for coinOne in coinEntities:
                coinOne.x = invisibleCoin.x

            if invisibleCoin.x <= 50:
                for coinOne in coinEntities:
                    coinOne.y = 650

            if self.isCollision(skate, coin):
                for coinOne in coinEntities:
                    coinOne.y = self.height
                coins = coins + 1

            self.drawEntity(coin)

            self.drawText("Speed: " + str(round(speed, 2)).__str__(), my_font, (0, 0, 0), 16, 16)
            self.drawText("Distance: " + distance.__trunc__().__str__(), my_font, (0, 0, 0), 16, 16 + 32)
            self.drawText("Coins: " + coins.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 2)
            self.drawText("Player_X: " + skater.x.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 5)
            self.drawText("Player_Y: " + skater.y.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 6)
            self.drawText("Coin_invisible_x: " + invisibleCoin.x.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 7)
            self.drawText("Coin_invisible_y: " + invisibleCoin.y.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 8)
            self.drawText("Coin_X: " + coin.x.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 9)
            self.drawText("Coin_Y: " + coin.y.__str__(), my_font, (0, 0, 0), 16, 16 + 32 * 10)

            if self.keys[Game.pygame.K_ESCAPE]:
                self.isRunning = False
            if self.keys[Game.pygame.K_UP]:
                speed *= 1.1
            if self.keys[Game.pygame.K_DOWN]:
                speed *= .9
            if speed <= 0:
                speed = 0
            Game.pygame.display.update()

        Game.pygame.quit()
