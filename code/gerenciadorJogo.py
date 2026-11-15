import pygame
from code.cidade import Cidade
from code.jogador import Jogador
from code.desafioMatematico import DesafioMatematico
from code.janela import Janela
META = 30


class GerenciadorJogo:
    def __init__(self, tela, name, menu_option):
        self.tela = tela
        self.name = name
        self.menu_option = menu_option
        self.cidade = Cidade(tela)
        self.jogador = Jogador(tela)
        self.fonte = pygame.font.SysFont('Arial', 28, bold=True)  # criada UMA vez só
        self.level = 1
        self.pontos = 0
        self.vidas = 3
        self.mensagem = ''
        self.mensagem_tempo = 0
        self.nova_rodada()

    def run(self):
        pygame.mixer.music.load('./assets/Ramones - 10 - Track 10.mp3')  # troque pelo nome do seu arquivo
        pygame.mixer.music.play(-1)  # -1 = repete para sempre
        relogio = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return          # volta para o menu

            self.jogador.mover(pygame.key.get_pressed())
            self.atualizar_level()
            velocidade = self.velocidade()
            self.cidade.atualizar(velocidade)
            for janela in self.janelas:
                janela.atualizar(velocidade)
            self.verificar_janelas()
            if self.verificar_vitoria():
                self.tela_final(True)
                return  # encerra a partida e volta ao menu
            if self.verificar_derrota():
                self.tela_final(False)
                return

            self.cidade.desenhar()
            for janela in self.janelas:
                janela.desenhar()
            self.jogador.desenhar()
            self.desenhar_hud()
            pygame.display.flip()
            relogio.tick(60)

    def atualizar_level(self):
        self.level = 1 + self.pontos // 5

    def velocidade(self):
        return 3 + (self.level - 1) * 1

    def desenhar_hud(self):
        largura = self.tela.get_width()
        pygame.draw.rect(self.tela, (0, 0, 0), (0, 0, largura, 70))  # barra preta
        titulo = self.fonte.render(self.desafio.enunciado, True, (255, 255, 255))
        self.tela.blit(titulo, titulo.get_rect(center=(largura // 2, 35)))  # a pergunta
        nivel = self.fonte.render(f'LEVEL {self.level}', True, (255, 128, 0))
        self.tela.blit(nivel, (15, 8))
        pts = self.fonte.render(f'Pontos: {self.pontos}', True, (255, 255, 255))
        self.tela.blit(pts, (15, 38))
        for i in range(self.vidas):  # uma bolinha por vida
            pygame.draw.circle(self.tela, (230, 40, 60), (largura - 30 - i * 34, 35), 12)
        if self.mensagem_tempo > 0:
            self.mensagem_tempo -= 1
            msg = self.fonte.render(self.mensagem, True, (255, 255, 120))
            self.tela.blit(msg, msg.get_rect(center=(largura // 2, 105)))

    def nova_rodada(self):
        self.desafio = DesafioMatematico()
        largura = self.tela.get_width()
        xs = [int(largura * f) for f in (0.3, 0.5, 0.7)]  # 3 colunas: 30%, 50%, 70%
        self.janelas = [Janela(self.tela, x, -60, valor)
                        for x, valor in zip(xs, self.desafio.alternativas)]

    def verificar_janelas(self):
        rodada_acabou = False

        for janela in self.janelas:
            if janela.verificar_colisao(self.jogador.rect):
                if self.desafio.verificar_resposta(janela.resposta):
                    self.adicionar_pontos()
                    self.mensagem = 'Acertou! +1'
                else:
                    self.vidas -= 1
                    self.mensagem = f'Errou! Resposta: {self.desafio.resposta_correta}'
                rodada_acabou = True
                break

        # nenhuma janela foi pega e todas saíram pela parte de baixo

        if not rodada_acabou and all(j.saiu_da_tela() for j in self.janelas):
            self.vidas -= 1
            self.mensagem = 'A resposta passou!'
            rodada_acabou = True

        if rodada_acabou:
            self.mensagem_tempo = 60  # 60 quadros = 1 segundo
            self.nova_rodada()

    def adicionar_pontos(self):
        self.pontos += 1

    def remover_vida(self):
        self.vidas -= 1

    def verificar_vitoria(self):
        return self.pontos >= META

    def verificar_derrota(self):
        return self.vidas <= 0

    def tela_final(self, venceu):
        pygame.mixer.music.stop()
        largura, altura = self.tela.get_size()
        fonte_grande = pygame.font.SysFont('Arial', 64, bold=True)
        relogio = pygame.time.Clock()

        if venceu:
            titulo, cor = 'VOCÊ VENCEU!', (120, 255, 140)
        else:
            titulo, cor = 'GAME OVER', (255, 90, 90)

        veu = pygame.Surface((largura, altura), pygame.SRCALPHA)  # camada transparente
        veu.fill((0, 0, 0, 170))  # preto com transparência

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return  # sai da tela final

            self.cidade.desenhar()
            self.tela.blit(veu, (0, 0))
            t1 = fonte_grande.render(titulo, True, cor)
            t2 = self.fonte.render(f'Pontos: {self.pontos}', True, (255, 255, 255))
            t3 = self.fonte.render('ENTER para voltar ao menu', True, (255, 255, 255))
            self.tela.blit(t1, t1.get_rect(center=(largura // 2, altura // 2 - 60)))
            self.tela.blit(t2, t2.get_rect(center=(largura // 2, altura // 2 + 10)))
            self.tela.blit(t3, t3.get_rect(center=(largura // 2, altura // 2 + 60)))
            pygame.display.flip()
            relogio.tick(60)