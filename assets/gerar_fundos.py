"""Gera os fundos (PNG 800x600) do jogo. Requer: pip install pillow
Todas as camadas de prédios repetem a cada 600 px na vertical (rolagem sem emenda)."""
import os, random
from PIL import Image, ImageDraw, ImageFilter

W, H = 800, 600
SAIDA = os.path.dirname(os.path.abspath(__file__))

TEMAS = {
    "dia": dict(topo=(95, 170, 250), base=(215, 240, 255), astro=(255, 244, 170), astro_pos=(650, 120),
                estrelas=0, nuvens=True, longe=(125, 155, 195), longe_on=(210, 235, 255), longe_off=(95, 125, 168),
                perto=(160, 112, 98), perto_on=(175, 220, 255), perto_off=(88, 118, 150), borda=(110, 74, 66)),
    "entardecer": dict(topo=(50, 35, 105), base=(255, 150, 95), astro=(255, 205, 125), astro_pos=(170, 430),
                       estrelas=40, nuvens=False, longe=(95, 62, 125), longe_on=(255, 205, 120), longe_off=(60, 42, 90),
                       perto=(72, 46, 78), perto_on=(255, 190, 100), perto_off=(40, 30, 58), borda=(40, 26, 48)),
    "noite": dict(topo=(6, 8, 28), base=(38, 44, 96), astro=(240, 240, 255), astro_pos=(650, 110),
                  estrelas=130, nuvens=False, longe=(22, 27, 58), longe_on=(255, 232, 145), longe_off=(38, 44, 84),
                  perto=(30, 32, 44), perto_on=(255, 212, 95), perto_off=(46, 52, 72), borda=(18, 19, 28)),
}


def mistura(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def ceu(t, seed):
    rnd = random.Random(seed)
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=mistura(t["topo"], t["base"], y / H) + (255,))
    for _ in range(t["estrelas"]):
        x, y, r = rnd.randint(0, W), rnd.randint(0, int(H * .7)), rnd.choice([1, 1, 2])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, rnd.randint(120, 255)))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gx, gy = t["astro_pos"]
    ImageDraw.Draw(glow).ellipse((gx - 80, gy - 80, gx + 80, gy + 80), fill=t["astro"] + (110,))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(25)))
    d = ImageDraw.Draw(img)
    d.ellipse((gx - 38, gy - 38, gx + 38, gy + 38), fill=t["astro"] + (255,))
    if t["nuvens"]:
        for _ in range(7):
            cx, cy = rnd.randint(0, W), rnd.randint(40, 420)
            for k in range(5):
                ox, oy, r = rnd.randint(-45, 45), rnd.randint(-10, 10), rnd.randint(22, 40)
                d.ellipse((cx + ox - r, cy + oy - r * .6, cx + ox + r, cy + oy + r * .6), fill=(255, 255, 255, 215))
    return img


def janelas(d, x0, x1, passo, jw, jh, on, off, rnd, p_on, borda=None):
    colunas = max(1, (x1 - x0) // (jw + 14))
    esp = (x1 - x0) / colunas
    for c in range(colunas):
        for y in range(0, H, passo):
            cor = on if rnd.random() < p_on else off
            cx = x0 + esp * c + esp / 2
            box = (cx - jw / 2, y + (passo - jh) / 2, cx + jw / 2, y + (passo + jh) / 2)
            d.rectangle(box, fill=cor + (255,), outline=borda)
            if borda:  # peitoril
                d.rectangle((box[0] - 3, box[3], box[2] + 3, box[3] + 4), fill=borda + (255,))


def sombreia(img, x0, x1, claro=18):
    """Gradiente horizontal leve (mantém a repetição vertical)."""
    px = img.load()
    for x in range(x0, x1):
        k = int(claro * (1 - 2 * abs((x - x0) / max(1, x1 - x0 - 1) - .5)))
        for y in range(H):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (min(255, r + k), min(255, g + k), min(255, b + k), a)


def longe(t, seed):
    rnd = random.Random(seed)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = -20
    while x < W:
        larg = rnd.randint(70, 120)
        cor = mistura(t["longe"], (0, 0, 0), rnd.uniform(0, .18))
        d.rectangle((x, 0, x + larg, H), fill=cor + (255,))
        for y in range(0, H, 100):  # divisões de andar
            d.line([(x, y), (x + larg, y)], fill=mistura(cor, (0, 0, 0), .25) + (255,), width=2)
        janelas(d, x + 8, x + larg - 8, 30, 9, 14, t["longe_on"], t["longe_off"], rnd, .35)
        sombreia(img, max(0, x), min(W, x + larg), 14)
        x += larg + rnd.randint(25, 60)
    return img


def perto(t, lado, seed):
    rnd = random.Random(seed)
    larg = 150
    x0, x1 = (0, larg) if lado == "esq" else (W - larg, W)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((x0, 0, x1, H), fill=t["perto"] + (255,))
    for y in range(0, H, 100):  # cornijas
        d.rectangle((x0, y, x1, y + 8), fill=t["borda"] + (255,))
    janelas(d, x0 + 10, x1 - 10, 100, 40, 58, t["perto_on"], t["perto_off"], rnd, .4, t["borda"])
    borda_x = x1 if lado == "esq" else x0
    d.rectangle((borda_x - 4, 0, borda_x + 4, H), fill=t["borda"] + (255,))
    sombreia(img, x0, x1, 16)
    return img


if __name__ == "__main__":
    for i, (nome, t) in enumerate(TEMAS.items()):
        ceu(t, i).convert("RGB").save(os.path.join(SAIDA, f"ceu_{nome}.png"))
        longe(t, i + 10).save(os.path.join(SAIDA, f"predios_longe_{nome}.png"))
        perto(t, "esq", i + 20).save(os.path.join(SAIDA, f"predio_perto_esq_{nome}.png"))
        perto(t, "dir", i + 30).save(os.path.join(SAIDA, f"predio_perto_dir_{nome}.png"))
    print("Fundos gerados em", SAIDA)
