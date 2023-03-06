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

    def start(self):
        scaler = self.scaler

        self.pygame.init()

        clock = self.pygame.time.Clock()
        self.keys = self.pygame.key.get_pressed()
        if self.isFullscreen:
            self.win = self.pygame.display.set_mode((self.width, self.height), self.pygame.FULLSCREEN)
        else:
            self.win = self.pygame.display.set_mode((self.width, self.height))

        while self.isRunning:
            self.pygame.display.set_caption(f'{clock.get_fps():.1f} fps')
            self.pygame.display.update()
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.isRunning = False
            self.keys = self.pygame.key.get_pressed()
            self.win.fill((0, 0, 0))
            self.pygame.draw.rect(self.win, (85, 123, 153), (self.windowBorder, self.windowBorder, self.width - 2 * self.windowBorder, self.height - 2 * self.windowBorder))

            # for entity in self.entities:
            #     print(entity)

            background = Entity(self.pygame, "assets/bg_street_city.png", 0, 0)
            self.drawEntity(background)
            driveway = Entity(self.pygame, "assets/bg_street_road_v2.png", 0, 0)
            self.drawEntity(driveway)


            if self.keys[self.pygame.K_ESCAPE]:
                self.isRunning = False

        self.pygame.quit()

