#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.gerenciadorJogo import GerenciadorJogo
from code.menu import Menu, MENU_OPTION


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((600, 480))
        pygame.display.set_caption("Aranha Matemática")

    def executar(self):
        menu = Menu(self.tela)
        rodando = True



        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
            menu = Menu(self.tela)
            while True:
                menu_return = menu.run()
                pygame.mixer.music.stop()  # ou fadeout(800) se quiser suavizar
                if menu_return == MENU_OPTION[0]:
                    GerenciadorJogo(self.tela, 'JOG1', menu_return).run()
                elif menu_return == MENU_OPTION[1]:
                    GerenciadorJogo(self.tela, 'JOG2', menu_return).run()
                elif menu_return == MENU_OPTION[2]:
                    self.tela_score()
                elif menu_return == MENU_OPTION[3]:
                    pygame.quit()
                    quit()




        pygame.quit()

    def tela_score(self):
        fundo = pygame.image.load('./assets/ceu_noite.png').convert()
        fundo = pygame.transform.scale(fundo, self.tela.get_size())
        fonte_g = pygame.font.SysFont('Arial', 64, bold=True)
        fonte = pygame.font.SysFont('Arial', 32, bold=True)
        largura, altura = self.tela.get_size()
        recorde = GerenciadorJogo.ler_recorde()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return

            self.tela.blit(fundo, (0, 0))
            t1 = fonte_g.render('RECORDE', True, (255, 128, 0))
            t2 = fonte_g.render(f'{recorde} pontos', True, (255, 255, 255))
            t3 = fonte.render('ENTER para voltar', True, (255, 255, 255))
            self.tela.blit(t1, t1.get_rect(center=(largura // 2, altura // 2 - 80)))
            self.tela.blit(t2, t2.get_rect(center=(largura // 2, altura // 2)))
            self.tela.blit(t3, t3.get_rect(center=(largura // 2, altura // 2 + 90)))
            pygame.display.flip()