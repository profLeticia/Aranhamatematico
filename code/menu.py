import pygame

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
          pygame.display.flip()

          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  quit()
      pass