import pygame, random

class Bomba:
    def __init__(self):
        img = pygame.image.load("assets/bomba.png").convert_alpha()

        desired_w = 50
        scale = desired_w / img.get_width()
        new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
        self.img = pygame.transform.scale(img, new_size)

        self.reset()

    def reset(self):
        estrada_x = 120
        estrada_largura = 260
        min_x = estrada_x + 20
        max_x = estrada_x + estrada_largura - 20

        self.rect = self.img.get_rect(center=(random.randint(min_x, max_x), -50))
        self.y = float(self.rect.y)

    def mover(self, vel_bonus=0):
        self.y += 2 + vel_bonus
        self.rect.y = int(self.y)
        if self.rect.y > 650:
            self.reset()
            return True
        return False

    def desenhar(self, tela):
        tela.blit(self.img, self.rect)
