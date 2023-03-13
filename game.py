from entity.entity import Entity


class Game:
    def __init__(self, pygame, scaler, width, height, isFullscreen):
        self.pygame = pygame
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
        img = self.pygame.transform.scale(entity.image, (entity.width * self.scaler, entity.height * self.scaler))
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

    def drawText(self, string, font, color, x, y):
        self.pygame.font.init()
        entity = font.render(string, False, color)
        self.win.blit(entity, (x, y))

    def start(self):
        self.pygame.init()

        self.keys = self.pygame.key.get_pressed()
        if self.isFullscreen:
            self.win = self.pygame.display.set_mode((self.width, self.height), self.pygame.FULLSCREEN)
        else:
            self.win = self.pygame.display.set_mode((self.width, self.height))
        skater = Entity(self.pygame, "assets/p1_default.png", 0, 0)
        driveway = Entity(self.pygame, "assets/bg_street_road_v2.png", self.scaler, 0)
        driveway.y = self.height - driveway.height * self.scaler
        drivewaySecond = Entity(self.pygame, "assets/bg_street_road_v2.png", 0, 0)
        drivewaySecond.y = self.height - driveway.height * self.scaler
        background = Entity(self.pygame, "assets/bg_street_city.png", self.scaler, 0)
        backgroundSecond = Entity(self.pygame, "assets/bg_street_city.png", 0, 0)
        background.y = self.height - driveway.height * self.scaler - background.height * self.scaler
        backgroundSecond.y = self.height - driveway.height * self.scaler - background.height * self.scaler

        speed = 1
        distance = 0
        my_font = self.pygame.font.SysFont('Berlin Sans FB', 24)
        clock = self.pygame.time.Clock()

        while self.isRunning:
            clock.tick(60)
            self.pygame.display.set_caption(f'{clock.get_fps() :.1f} fps')
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.isRunning = False
            self.keys = self.pygame.key.get_pressed()
            self.win.fill((0, 0, 0))
            self.pygame.draw.rect(self.win, (85, 123, 153), (
                self.windowBorder, self.windowBorder, self.width - 2 * self.windowBorder,
                self.height - 2 * self.windowBorder))

            # for entity in self.entities:
            #     print(entity)

            speed = speed * 1.002
            distance = distance + speed
            self.drawEntity(background)
            self.moveEntity(driveway, -speed * self.scaler, -driveway.width * self.scaler, 0)
            self.moveEntity(drivewaySecond, -speed * self.scaler, 0, driveway.width * self.scaler)
            self.moveEntity(background, -speed * self.scaler, -background.width * self.scaler, 0)
            self.moveEntity(backgroundSecond, -speed * self.scaler, 0, backgroundSecond.width * self.scaler)

            self.drawEntity(skater)

            self.drawText("Speed: " + str(round(speed, 2)).__str__(), my_font, (0, 0, 0), 24, 24)
            self.drawText("Distance: " + distance.__trunc__().__str__(), my_font, (0, 0, 0), 24, 24*2)
            self.drawText("Coins: null", my_font, (0, 0, 0), 24, 24*3)

            if self.keys[self.pygame.K_ESCAPE]:
                self.isRunning = False
            if self.keys[self.pygame.K_UP]:
                speed += .1
            if self.keys[self.pygame.K_DOWN]:
                speed -= .1
            self.pygame.display.update()

        self.pygame.quit()
