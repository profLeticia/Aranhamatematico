import pygame
from code.cidade import Cidade


class GerenciadorJogo:
    def __init__(self, tela, name, menu_option):
        self.tela = tela
        self.name = name
        self.menu_option = menu_option
        self.cidade = Cidade(tela)

    def run(self):
        relogio = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return          # volta para o menu

            self.cidade.desenhar()
            pygame.display.flip()
            self.cidade.atualizar(3)  # 3 = velocidade da descida (teste 1, 3, 6...)
            self.cidade.desenhar()
            pygame.display.flip()
            relogio.tick(60) # limita o jogo a 60 quadros por segundo.