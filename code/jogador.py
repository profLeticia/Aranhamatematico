import pygame


class Jogador:
    def __init__(self, tela):
        self.tela = tela
        self.velocidade = 6

        # carrega as 5 poses de uma vez (dicionário: nome -> imagem)
        self.sprites = {}
        for nome in ('parado', 'subindo', 'descendo', 'esq', 'dir'):
            imagem = pygame.image.load(f'./assets/heroi_{nome}.png').convert_alpha()
            self.sprites[nome] = pygame.transform.smoothscale(imagem, (60, 82))

        self.pose = 'parado'
        self.surf = self.sprites[self.pose]
        self.rect = self.surf.get_rect(midbottom=(tela.get_width() // 2, tela.get_height() - 40))

        # área onde o herói pode andar (a tela inteira; depois dá para limitar mais)
        self.limites = tela.get_rect()

    def mover(self, teclas):
        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade

        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(self.limites)      # não deixa sair da tela

        # escolhe a imagem de acordo com o movimento
        if dx > 0:
            self.pose = 'dir'
        elif dx < 0:
            self.pose = 'esq'
        elif dy < 0:
            self.pose = 'subindo'
        elif dy > 0:
            self.pose = 'descendo'
        else:
            self.pose = 'parado'
        self.surf = self.sprites[self.pose]

    def lancar_teia(self):
        pygame.draw.line(self.tela, (230, 230, 230),(self.rect.centerx, 0), (self.rect.centerx, self.rect.top + 10), 2)

    def desenhar(self):
        self.lancar_teia()
        self.tela.blit(self.surf, self.rect)