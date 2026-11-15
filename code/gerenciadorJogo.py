import pygame
from code.cidade import Cidade
from code.desafioMatematico import DesafioMatematico
from code.janela import Janela
from code.jogador import Jogador, CONTROLES_1, CONTROLES_2
from code.menu import MENU_OPTION
META = 30
TEMAS = ('dia', 'entardecer', 'noite')
NIVEIS_POR_TEMA = 2


class GerenciadorJogo:
    def __init__(self, tela, name, menu_option):
        self.tela = tela
        self.name = name
        self.menu_option = menu_option
        self.cidade = Cidade(tela)
        largura = tela.get_width()
        if menu_option == MENU_OPTION[1]:                    # NEW GAME 2P
            self.jogadores = [Jogador(tela, CONTROLES_1, 'heroi', largura * 0.35),
                              Jogador(tela, CONTROLES_2, 'heroi2', largura * 0.65)]
        else:                                                # NEW GAME 1P
            self.jogadores = [Jogador(tela)]

        for i, jogador in enumerate(self.jogadores):
            jogador.nome = f'JOG{i + 1}'
        self.fonte = pygame.font.SysFont('Arial', 28, bold=True)
        self.fonte_pequena = pygame.font.SysFont('Arial', 20, bold=True)
        self.level = 1
        self.mensagem = ''
        self.mensagem_tempo = 0
        self.nova_rodada()

    def run(self):
        pygame.mixer.music.load('./assets/Ramones - 10 - Track 10.mp3')
        pygame.mixer.music.play(-1)  # -1 = repete para sempre
        relogio = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return          # volta para o menu

            teclas = pygame.key.get_pressed()
            for jogador in self.jogadores:
                jogador.mover(teclas)
            self.atualizar_level()
            self.atualizar_tema()
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
            for jogador in self.jogadores:
                jogador.desenhar()
            self.desenhar_hud()
            pygame.display.flip()
            relogio.tick(60)

    def atualizar_level(self):
        self.level = 1 + self.pontos // 5

    def velocidade(self):
        return 3 + (self.level - 1) * 1

    def desenhar_hud(self):
        largura = self.tela.get_width()
        pygame.draw.rect(self.tela, (0, 0, 0), (0, 0, largura, 70))

        if len(self.jogadores) == 1:
            j = self.jogadores[0]
            titulo = self.fonte.render(self.desafio.enunciado, True, (255, 255, 255))
            self.tela.blit(titulo, titulo.get_rect(center=(largura // 2, 35)))
            nivel = self.fonte.render(f'LEVEL {self.level}', True, (255, 128, 0))
            self.tela.blit(nivel, (15, 8))
            pts = self.fonte.render(f'Pontos: {j.pontos}', True, (255, 255, 255))
            self.tela.blit(pts, (15, 38))
            for i in range(j.vidas):
                pygame.draw.circle(self.tela, (230, 40, 60), (largura - 30 - i * 34, 35), 12)
        else:
            j1, j2 = self.jogadores
            centro = self.fonte.render(f'LEVEL {self.level}  |  {self.desafio.enunciado}',
                                       True, (255, 255, 255))
            self.tela.blit(centro, centro.get_rect(center=(largura // 2, 35)))
            t1 = self.fonte_pequena.render(f'JOG1  Pontos: {j1.pontos}', True, (255, 255, 255))
            t2 = self.fonte_pequena.render(f'JOG2  Pontos: {j2.pontos}', True, (255, 255, 255))
            self.tela.blit(t1, (15, 6))
            self.tela.blit(t2, t2.get_rect(topright=(largura - 15, 6)))
            for i in range(j1.vidas):
                pygame.draw.circle(self.tela, (230, 40, 60), (27 + i * 30, 52), 10)
            for i in range(j2.vidas):
                pygame.draw.circle(self.tela, (60, 120, 255), (largura - 27 - i * 30, 52), 10)

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
        dois = len(self.jogadores) > 1
        rodada_acabou = False

        for janela in self.janelas:
            for jogador in self.jogadores:
                if janela.verificar_colisao(jogador.rect):
                    quem = f'{jogador.nome}: ' if dois else ''
                    if self.desafio.verificar_resposta(janela.resposta):
                        jogador.adicionar_pontos()
                        self.mensagem = f'{quem}Acertou! +1'
                    else:
                        jogador.remover_vida()
                        self.mensagem = f'{quem}Errou! Resposta: {self.desafio.resposta_correta}'
                    rodada_acabou = True
                    break
            if rodada_acabou:
                break

        if not rodada_acabou and all(j.saiu_da_tela() for j in self.janelas):
            if dois:
                self.mensagem = 'Ninguém acertou!'
            else:
                self.jogadores[0].remover_vida()
                self.mensagem = 'A resposta passou!'
            rodada_acabou = True

        if rodada_acabou:
            self.mensagem_tempo = 60
            self.nova_rodada()

    def remover_vida(self):
        self.vidas -= 1

    @property
    def pontos(self):                      # maior pontuação entre os jogadores
        return max(j.pontos for j in self.jogadores)

    def verificar_vitoria(self):
        return any(j.pontos >= META for j in self.jogadores)

    def verificar_derrota(self):
        return any(j.vidas <= 0 for j in self.jogadores)

    def tela_final(self, venceu):
        pygame.mixer.music.stop()
        novo_recorde = self.salvar_recorde()
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
            if novo_recorde:
                t4 = self.fonte.render('NOVO RECORDE!', True, (255, 215, 0))
                self.tela.blit(t4, t4.get_rect(center=(largura // 2, altura // 2 + 110)))

            pygame.display.flip()
            relogio.tick(60)

    @staticmethod
    def ler_recorde():
        try:
            with open('./recorde.txt', 'r') as arquivo:
                return int(arquivo.read())
        except (FileNotFoundError, ValueError):
            return 0                       # ainda não existe arquivo: recorde é 0

    def salvar_recorde(self):
        if self.pontos > self.ler_recorde():           # só grava se bateu o recorde
            with open('./recorde.txt', 'w') as arquivo:
                arquivo.write(str(self.pontos))
            return True                                # novo recorde!
        return False

    def atualizar_tema(self):
        posicao = (self.level - 1) // NIVEIS_POR_TEMA     # levels 1-2 -> 0, 3-4 -> 1, 5+ -> 2
        posicao = min(posicao, len(TEMAS) - 1)
        self.cidade.trocar_tema(TEMAS[posicao])