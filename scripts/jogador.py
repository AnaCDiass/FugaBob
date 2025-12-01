import pygame

class Jogador:
    def __init__(self):
        img = pygame.image.load("assets/bob.png").convert_alpha()

        # aumenta um pouco e suaviza
        desired_w = 70  # antes era 60
        scale = desired_w / img.get_width()
        new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
        self.img = pygame.transform.smoothscale(img, new_size)

        self.rect = self.img.get_rect(center=(250, 500))
        self.vel = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.vel

        # limites da estrada, chegando quase nas bordas
        estrada_x = 120
        estrada_largura = 260
        min_x = estrada_x
        max_x = estrada_x + estrada_largura - self.rect.width

        if self.rect.x < min_x:
            self.rect.x = min_x
        if self.rect.x > max_x:
            self.rect.x = max_x

    def desenhar(self, tela):
        tela.blit(self.img, self.rect)
