import random


class DesafioMatematico:
    def __init__(self, maximo=12):
        self.maximo = maximo
        self.enunciado = None
        self.resposta_correta = None
        self.alternativas = []
        self.gerar_desafio()

    def gerar_desafio(self):
        raiz = random.randint(2, self.maximo)        # a resposta: 2 a 12
        self.resposta_correta = raiz
        self.enunciado = f'√{raiz * raiz} = ?'       # 7 * 7 = 49 -> "√49 = ?"

        erradas = set()                              # set não aceita números repetidos
        while len(erradas) < 2:
            candidata = raiz + random.choice([-3, -2, -1, 1, 2, 3])
            if candidata > 0 and candidata != raiz:
                erradas.add(candidata)

        self.alternativas = [raiz] + list(erradas)   # certa + 2 erradas
        random.shuffle(self.alternativas)            # embaralha as posições

    def verificar_resposta(self, valor):
        return valor == self.resposta_correta


if __name__ == '__main__':          # só roda se você executar ESTE arquivo direto
    for _ in range(5):
        d = DesafioMatematico()
        print(d.enunciado, d.alternativas, 'certa:', d.resposta_correta)