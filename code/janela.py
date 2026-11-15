import pygame


class Janela:
    def __init__(self, tela, x, y, resposta):
        self.tela = tela
        self.resposta = resposta
        self.y = float(y)                            # float: aceita velocidades como 2.5
        self.rect = pygame.Rect(0, 0, 90, 90)
        self.rect.center = (x, int(y))
        self.fonte = pygame.font.SysFont('Arial', 40, bold=True)

    def atualizar(self, velocidade):
        self.y += velocidade                         # igual ao "mude y por" do Scratch
        self.rect.centery = int(self.y)

    def desenhar(self):
        pygame.draw.rect(self.tela, (255, 215, 110), self.rect, border_radius=8)    # amarelo
        pygame.draw.rect(self.tela, (90, 60, 30), self.rect, 5, border_radius=8)    # moldura
        texto = self.fonte.render(str(self.resposta), True, (40, 30, 20))
        self.tela.blit(texto, texto.get_rect(center=self.rect.center))

    def verificar_colisao(self, rect_jogador):
        return self.rect.colliderect(rect_jogador)   # True se os retângulos se tocam

    def saiu_da_tela(self):
        return self.rect.top > self.tela.get_height()