import pygame
from scripts.cenas import CenaMenu, CenaJogo

pygame.init()
tela = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Bob Pega Comidas")
clock = pygame.time.Clock()

jogo = CenaJogo(tela)
menu = CenaMenu(tela, jogo)  # passa a cena do jogo pro menu
cena_atual = "MENU"

rodando = True
while rodando:
    eventos = pygame.event.get()
    for e in eventos:
        if e.type == pygame.QUIT:
            rodando = False

    if cena_atual == "MENU":
        cena_atual = menu.atualizar(eventos)
        menu.desenhar()
    elif cena_atual == "JOGO":
        cena_atual = jogo.atualizar(eventos)
        jogo.desenhar()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
