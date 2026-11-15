import pygame
from code.cidade import Cidade
from code.jogador import Jogador


class GerenciadorJogo:
    def __init__(self, tela, name, menu_option):
        self.tela = tela
        self.name = name
        self.menu_option = menu_option
        self.cidade = Cidade(tela)
        self.jogador = Jogador(tela)
        self.fonte = pygame.font.SysFont('Arial', 28, bold=True)  # criada UMA vez só
        self.level = 1
        self.pontos = 0

    def run(self):
        pygame.mixer.music.load('./assets/Ramones - 10 - Track 10.mp3')  # troque pelo nome do seu arquivo
        pygame.mixer.music.play(-1)  # -1 = repete para sempre
        relogio = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return          # volta para o menu

            self.jogador.mover(pygame.key.get_pressed())
            self.atualizar_level()
            self.cidade.atualizar(self.velocidade())  # 3 = velocidade da descida (teste 1, 3, 6...)
            self.cidade.desenhar()
            self.jogador.desenhar()  # ← o herói por cima da cidade
            self.desenhar_hud()
            pygame.display.flip()
            relogio.tick(60) # limita o jogo a 60 quadros por segundo.

    def atualizar_level(self):
        self.level = 1 + self.pontos // 5

    def velocidade(self):
        return 3 + (self.level - 1) * 1

    def desenhar_hud(self):
        texto = self.fonte.render(f'LEVEL {self.level}', True, (255, 255, 255))
        self.tela.blit(texto, (15, 15))