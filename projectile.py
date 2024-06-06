import pygame
import math


class Projectile:
    def __init__(self, x, y, angle, color, speed=5):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.rect = pygame.Rect(x, y, 10, 7)
        self.surf = pygame.Surface((10, 7), pygame.SRCALPHA)
        pygame.draw.rect(self.surf, color, (0, 0, 10, 7))
        self.surf = pygame.transform.rotate(self.surf, angle)

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
