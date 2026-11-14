#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.menu import Menu

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((600, 480))
        pygame.display.set_caption("Aranha Matemática")
        self.relogio = pygame.time.Clock()

    def executar(self):
        menu = Menu(self.tela)
        rodando = True



        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
            menu.run()
            pygame.display.flip()
            self.relogio.tick(60)
        pygame.quit()

