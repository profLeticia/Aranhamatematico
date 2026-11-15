import pygame


class Cidade:
    def __init__(self, tela, tema='dia'):
        self.tela = tela
        self.altura = tela.get_height()
        self.tema = None
        self.ceu = None
        self.predios = []          # cada camada: [imagem, fator de velocidade, deslocamento]
        self.trocar_tema(tema)

    def carregar(self, arquivo, transparente):
        imagem = pygame.image.load(arquivo)
        imagem = imagem.convert_alpha() if transparente else imagem.convert()
        return pygame.transform.scale(imagem, self.tela.get_size())

    def trocar_tema(self, tema):
        if tema == self.tema:
            return                                   # já está nesse tema: não faz nada
        self.tema = tema
        self.ceu = self.carregar(f'./assets/ceu_{tema}.png', False)

        # guarda onde cada camada estava, para os prédios não "pularem" na troca
        deslocamentos = [camada[2] for camada in self.predios] or [0.0, 0.0, 0.0]

        arquivos = (f'predios_longe_{tema}.png',
                    f'predio_perto_esq_{tema}.png',
                    f'predio_perto_dir_{tema}.png')
        fatores = (0.4, 1.0, 1.0)

        self.predios = []
        for arquivo, fator, deslocamento in zip(arquivos, fatores, deslocamentos):
            imagem = self.carregar(f'./assets/{arquivo}', True)
            self.predios.append([imagem, fator, deslocamento])

    def atualizar(self, velocidade):
        for camada in self.predios:
            camada[2] = (camada[2] + velocidade * camada[1]) % self.altura

    def desenhar(self):
        self.tela.blit(self.ceu, (0, 0))
        for imagem, fator, deslocamento in self.predios:
            y = int(deslocamento)
            self.tela.blit(imagem, (0, y - self.altura))
            self.tela.blit(imagem, (0, y))