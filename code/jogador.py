import pygame

# dicionário: "ação" -> tecla correspondente
CONTROLES_1 = {'esq': pygame.K_LEFT, 'dir': pygame.K_RIGHT,
               'cima': pygame.K_UP, 'baixo': pygame.K_DOWN}
CONTROLES_2 = {'esq': pygame.K_a, 'dir': pygame.K_d,
               'cima': pygame.K_w, 'baixo': pygame.K_s}


class Jogador:
    def __init__(self, tela, controles=CONTROLES_1, prefixo='heroi', x_inicial=None):
        self.tela = tela
        self.velocidade = 6
        self.controles = controles
        self.pontos = 0
        self.vidas = 3
        # as teclas deste jogador

        # prefixo escolhe a cor: 'heroi' (vermelho) ou 'heroi2' (azul)
        self.sprites = {}
        for nome in ('parado', 'subindo', 'descendo', 'esq', 'dir'):
            imagem = pygame.image.load(f'./assets/{prefixo}_{nome}.png').convert_alpha()
            self.sprites[nome] = pygame.transform.smoothscale(imagem, (60, 82))

        self.pose = 'parado'
        self.surf = self.sprites[self.pose]

        if x_inicial is None:
            x_inicial = tela.get_width() // 2      # sem valor: começa no meio
        self.rect = self.surf.get_rect(midbottom=(int(x_inicial), tela.get_height() - 40))
        self.limites = tela.get_rect()

    def mover(self, teclas):
        dx = 0
        dy = 0
        if teclas[self.controles['esq']]:
            dx = -self.velocidade
        if teclas[self.controles['dir']]:
            dx = self.velocidade
        if teclas[self.controles['cima']]:
            dy = -self.velocidade
        if teclas[self.controles['baixo']]:
            dy = self.velocidade

        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(self.limites)

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
        pygame.draw.line(self.tela, (230, 230, 230),
                         (self.rect.centerx, 0), (self.rect.centerx, self.rect.top + 10), 2)

    def desenhar(self):
        self.lancar_teia()
        self.tela.blit(self.surf, self.rect)

    def adicionar_pontos(self):
        self.pontos += 1

    def remover_vida(self):
        self.vidas -= 1