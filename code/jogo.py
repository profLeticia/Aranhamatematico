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
                if menu_return == MENU_OPTION[0]:
                    GerenciadorJogo(self.tela, 'JOG1', menu_return).run()
                elif menu_return == MENU_OPTION[1]:
                    GerenciadorJogo(self.tela, 'JOG2', menu_return).run()
                elif menu_return == MENU_OPTION[3]:
                    pygame.quit()
                    quit()

        pygame.quit()

