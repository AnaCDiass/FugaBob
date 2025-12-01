import pygame
from scripts.jogador import Jogador
from scripts.comida import Comida
from scripts.bomba import Bomba
import random

class CenaMenu:
    def __init__(self, tela, cena_jogo):
        self.tela = tela
        self.cena_jogo = cena_jogo  # referência para resetar o jogo
        self.font = pygame.font.SysFont(None, 60)
        self.btn_font = pygame.font.SysFont(None, 40)
        self.botao = pygame.Rect(150, 300, 200, 60)

        # efeito de bolhas no fundo
        self.bolhas = [(random.randint(0, 500), random.randint(0, 600), random.randint(2, 6)) for _ in range(30)]

    def atualizar(self, eventos):
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.botao.collidepoint(e.pos):
                    self.cena_jogo.reset()  # reseta o jogo antes de iniciar
                    return "JOGO"
        return "MENU"

    def desenhar(self):
        # fundo azul água
        self.tela.fill((64, 224, 208))  # aquamarine

        # desenhar bolhas
        for i, (x, y, r) in enumerate(self.bolhas):
            pygame.draw.circle(self.tela, (173, 216, 230), (x, y), r)  # lightblue
            self.bolhas[i] = (x, (y - 1) % 600, r)

       # título em amarelo com fonte menor e centralizado
        titulo_font = pygame.font.SysFont(None, 50)  # menor que 60
        titulo = titulo_font.render("Bob na Fuga das Bombas", True, (255, 223, 0))
        titulo_rect = titulo.get_rect(center=(250, 150))  # centraliza horizontalmente
        self.tela.blit(titulo, titulo_rect)

        # botão com amarelo e contorno azul
        pygame.draw.rect(self.tela, (255, 223, 0), self.botao, border_radius=10)
        pygame.draw.rect(self.tela, (0, 128, 255), self.botao, width=4, border_radius=10)

        # texto do botão em azul escuro
        texto = self.btn_font.render("Iniciar", True, (0, 0, 128))
        self.tela.blit(texto, (self.botao.x + 50, self.botao.y + 10))


class CenaJogo:
    def __init__(self, tela):
        self.tela = tela
        self.font = pygame.font.SysFont(None, 40)
        self.fundo = pygame.image.load("assets/fundo.png").convert_alpha()
        self.fundo = pygame.transform.scale(self.fundo, (500, 600))
        self.jogador = Jogador()
        self.reset()

    def reset(self):
        self.pontos = 0
        self.vel_bonus = 0
        # recria comidas e bombas
        self.comidas = [Comida("hamburguer") for _ in range(3)] + [Comida("refri") for _ in range(2)]
        self.bombas = [Bomba() for _ in range(2)]
        # opcional: reseta posição do jogador
        self.jogador.rect.center = (250, 500)

    def atualizar(self, eventos):
        teclas = pygame.key.get_pressed()
        self.jogador.mover(teclas)

        # aumenta gradualmente, mas com limite
        self.vel_bonus = min(self.pontos * 0.03, 4)

        for c in self.comidas:
            if c.mover(self.vel_bonus):
                self.pontos += 1
            jogador_hitbox = self.jogador.rect.inflate(-10, -10)
            comida_hitbox = c.rect.inflate(-10, -10)
            if jogador_hitbox.colliderect(comida_hitbox):
                self.pontos += 1
                c.reset()

        for b in self.bombas:
            b.mover(self.vel_bonus)
            jogador_hitbox = self.jogador.rect.inflate(-10, -10)
            bomba_hitbox = b.rect.inflate(-10, -10)
            if jogador_hitbox.colliderect(bomba_hitbox):
                return "MENU"  # morreu

        return "JOGO"

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        self.jogador.desenhar(self.tela)
        for c in self.comidas:
            c.desenhar(self.tela)
        for b in self.bombas:
            b.desenhar(self.tela)
        txt = self.font.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        self.tela.blit(txt, (10, 10))
