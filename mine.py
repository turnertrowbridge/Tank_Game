import pygame


class Mine:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (0, 0, 0)
        self.exploded = False
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer % 10 == 0:
            if self.color == (0, 0, 0):
                self.color = (255, 0, 0)
            else:
                self.color = (0, 0, 0)
        if self.timer >= 100:
            self.exploded = True

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
