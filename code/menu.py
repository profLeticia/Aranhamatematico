import pygame
from pygame.examples.grid import WINDOW_WIDTH
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

MENU_OPTION = ('NEW GAME 1P',
               'NEW GAME 2P',
               'SCORE')

class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.surf = pygame.image.load('./assets/ceu_noite.png').convert()
        self.surf = pygame.transform.scale(self.surf, self.tela.get_size())
        self.rect = self.surf.get_rect(left=0, top=0)


    def run(self):

            pygame.mixer.music.load('./assets/Pitty - Equalize.mp3')
            pygame.mixer.music.play(-1)
            while True:
                self.tela.blit(source=self.surf, dest=self.rect)
                self.menu_text(80, "ARANHA", (255, 128, 0), (self.tela.get_width() // 2, 70))
                self.menu_text(80, "MATEMÁTICA", (255, 128, 0), (self.tela.get_width() // 2, 150))

                for i in range(len(MENU_OPTION)):
                    self.menu_text(20, MENU_OPTION[i], (255, 255, 255),
                                   (self.tela.get_width() // 2, 260 + 35 * i))

                pygame.display.flip()  # por último

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
    pass

    def menu_text (self, text_size:int, text:str, text_color:tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont('Arial', size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.tela.blit(text_surf, text_rect)