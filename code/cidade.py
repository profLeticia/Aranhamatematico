import pygame


class Cidade:
    def __init__(self, tela):
        self.tela = tela
        self.altura = tela.get_height()

        # céu: fica parado no fundo
        self.ceu = pygame.image.load('./assets/ceu_noite.png').convert()
        self.ceu = pygame.transform.scale(self.ceu, tela.get_size())

        # prédios: cada camada tem [imagem, fator de velocidade, deslocamento]
        self.predios = []
        self.adicionar_camada('./assets/predios_longe_noite.png', 0.4)      # longe: devagar
        self.adicionar_camada('./assets/predio_perto_esq_noite.png', 1.0)   # perto: rápido
        self.adicionar_camada('./assets/predio_perto_dir_noite.png', 1.0)

    def adicionar_camada(self, arquivo, fator):
        imagem = pygame.image.load(arquivo).convert_alpha()   # alpha = parte transparente
        imagem = pygame.transform.scale(imagem, self.tela.get_size())
        self.predios.append([imagem, fator, 0.0])

    def atualizar(self, velocidade):
        for camada in self.predios:
            camada[2] = (camada[2] + velocidade * camada[1]) % self.altura

    def desenhar(self):
        self.tela.blit(self.ceu, (0, 0))                      # 1º o céu
        for imagem, fator, deslocamento in self.predios:      # 2º os prédios por cima
            y = int(deslocamento)
            self.tela.blit(imagem, (0, y - self.altura))      # cópia de cima
            self.tela.blit(imagem, (0, y))                    # cópia de baixo - o blit é para colocar uma tela sobre a outra.