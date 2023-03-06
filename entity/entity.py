class Entity:
    def __init__(self, pygame, image, x, y):
        self.pygame = pygame
        self.image = self.pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()