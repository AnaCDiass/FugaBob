import pygame
from scripts.jogador import Jogador
from scripts.comida import Comida
from scripts.bomba import Bomba
import random
import time

class CenaMenu:
    def __init__(self, tela, cena_jogo):
        self.tela = tela
        self.cena_jogo = cena_jogo
        self.font = pygame.font.SysFont(None, 60)
        self.btn_font = pygame.font.SysFont(None, 40)
        self.botao = pygame.Rect(150, 300, 200, 60)

        self.bolhas = [(random.randint(0, 500), random.randint(0, 600), random.randint(2, 6)) for _ in range(30)]

    def atualizar(self, eventos):
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.botao.collidepoint(e.pos):
                    self.cena_jogo.reset()
                    return "JOGO"
        return "MENU"

    def desenhar(self):
        self.tela.fill((64, 224, 208))

        for i, (x, y, r) in enumerate(self.bolhas):
            pygame.draw.circle(self.tela, (173, 216, 230), (x, y), r)
            self.bolhas[i] = (x, (y - 1) % 600, r)

        titulo_font = pygame.font.SysFont(None, 50)
        titulo = titulo_font.render("Bob na Fuga das Bombas", True, (255, 223, 0))
        titulo_rect = titulo.get_rect(center=(250, 150))
        self.tela.blit(titulo, titulo_rect)

        pygame.draw.rect(self.tela, (255, 223, 0), self.botao, border_radius=10)
        pygame.draw.rect(self.tela, (0, 128, 255), self.botao, width=4, border_radius=10)
        texto = self.btn_font.render("Iniciar", True, (0, 0, 128))
        self.tela.blit(texto, (self.botao.x + 50, self.botao.y + 10))


class CenaJogo:
    def __init__(self, tela):
        self.tela = tela
        self.font = pygame.font.SysFont(None, 40)
        self.fundo = pygame.image.load("assets/fundo.png").convert_alpha()
        self.fundo = pygame.transform.scale(self.fundo, (500, 600))
        self.jogador = Jogador()

        # high score começa em 0
        self.high_score = 0

        self.reset()

    def reset(self):
        # Atualiza high score ao morrer
        if hasattr(self, "pontos") and self.pontos > self.high_score:
            self.high_score = self.pontos

        self.pontos = 0
        self.fase = 1
        self.vel_bonus = 0
        self.mostrar_aviso = False
        self.tempo_aviso = 0

        self.comidas = [Comida("hamburguer") for _ in range(3)] + \
                        [Comida("refri") for _ in range(2)]
        self.bombas = [Bomba() for _ in range(2)]

        self.jogador.rect.center = (250, 500)

    def atualizar(self, eventos):
        teclas = pygame.key.get_pressed()
        self.jogador.mover(teclas)

        # ----- FASES (4 fases agora) -----
        if self.pontos >= 100:
            nova_fase = 4
        elif self.pontos >= 75:
            nova_fase = 3
        elif self.pontos >= 25:
            nova_fase = 2
        else:
            nova_fase = 1

        if nova_fase == 4 and self.fase != 4:
            self.mostrar_aviso = True
            self.tempo_aviso = time.time()

        self.fase = nova_fase

        # velocidade base das fases
        bases = {1: 0.5, 2: 1.5, 3: 4, 4: 5.5}

        base = bases[self.fase]

        self.vel_bonus = base + min(self.pontos * 0.008, 3)

        # comidas
        for c in self.comidas:
            if c.mover(self.vel_bonus):
                self.pontos += 1

            jogador_hitbox = self.jogador.rect.inflate(-10, -10)
            comida_hitbox = c.rect.inflate(-10, -10)

            if jogador_hitbox.colliderect(comida_hitbox):
                self.pontos += 1
                c.reset()

        # bombas
        for b in self.bombas:
            b.mover(self.vel_bonus)

            jogador_hitbox = self.jogador.rect.inflate(-10, -10)
            bomba_hitbox = b.rect.inflate(-10, -10)

            if jogador_hitbox.colliderect(bomba_hitbox):
                return "MENU"

        return "JOGO"

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        self.jogador.desenhar(self.tela)

        for c in self.comidas:
            c.desenhar(self.tela)

        for b in self.bombas:
            b.desenhar(self.tela)

        # pontos atuais
        txt = self.font.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        self.tela.blit(txt, (10, 10))

        # fase
        fase_txt = self.font.render(f"Fase: {self.fase}", True, (255, 255, 0))
        self.tela.blit(fase_txt, (10, 50))

        # ---- HIGH SCORE NA LATERAL DIREITA ----
        hs = self.font.render(f"Recorde: {self.high_score}", True, (0, 255, 0))
        hs_rect = hs.get_rect(topright=(490, 10))
        self.tela.blit(hs, hs_rect)
        # ---------------------------------------

        # aviso final
        if self.mostrar_aviso:
            if time.time() - self.tempo_aviso < 3:
                aviso_font = pygame.font.SysFont(None, 45)
                text = aviso_font.render("Parabéns! Última Fase!", True, (255, 255, 0))
                rect = text.get_rect(center=(250, 300))
                self.tela.blit(text, rect)
            else:
                self.mostrar_aviso = False
