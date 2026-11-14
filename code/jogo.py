#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.menu import Menu


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode(size=(600, 480))

    def iniciar(self, ):
        pass

    def executar(self):
        print('Setup Start')

        print('Setup End')

        print('Loop Start')
        while True:

            menu = Menu(self.tela)
            menu.Run()
            pass

           # for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
             #       pygame.quit()
              #      quit()

    def atualizar(self, ):
        pass

    def desenhar(self, ):
        pass

    def verificar_fim(self, ):
        pass
