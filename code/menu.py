import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface


class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.surf = pygame.image.load('./assets/ceu_noite.png').convert()
        self.surf = pygame.transform.scale(self.surf, self.tela.get_size())
        self.rect = self.surf.get_rect(left=0, top=0)


    def run(self):

      pygame.mixer_music.load('./assets/Pitty - Equalize.mp3')
      pygame.mixer_music.play(-1)
      while True:
          self.tela.blit(source=self.surf, dest=self.rect)
          self.menu_text(100, "Aranha", (255,128,0), (self.tela.get_width() // 2, 120))
          self.menu_text(100, "Matemática", (255, 128, 0), (self.tela.get_width() // 2, 240))
          pygame.display.flip()

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