import pygame

def gera_fundo(caminho, width=500, height=600):
    pygame.init()
    
    # criar superfície
    surf = pygame.Surface((width, height))

    # céu
    surf.fill((135, 206, 235))  # azul claro

    # chão
    pygame.draw.rect(surf, (34, 139, 34), (0, height - 100, width, 100))  # verde

    # faixa de jogo central (onde o Bob vai pegar comidas)
    faixa_x = 100
    faixa_largura = 300
    pygame.draw.rect(surf, (210, 180, 140), (faixa_x, 0, faixa_largura, height))  # marrom clarinho

    # salvar
    pygame.image.save(surf, caminho)
    print(f"Fundo salvo em {caminho}")

if __name__ == "__main__":
    gera_fundo("assets/fundo.png")
