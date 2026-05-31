"""
Genera assets reutilizables con transparencia (RGBA).
Tazas, huellas, formas organicas que se componen en imagenes.
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), "static", "assets", "images")
os.makedirs(OUT, exist_ok=True)


def save(img, name):
    img.save(os.path.join(OUT, f"{name}.webp"), "WEBP", quality=95, lossless=True)
    print(f"  {name}.webp ({img.width}x{img.height})")


# ═══════════════════════════════════════════════════════
# COFFEE CUP - Taza de cafe con detalles
# ═══════════════════════════════════════════════════════
def make_coffee_cup(size=600, cup_color="#c8956c", coffee_color="#3d1e0a"):
    # Render a 2x para anti-aliasing
    ss = 2
    rsize = size * ss
    img = Image.new("RGBA", (rsize, rsize), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2 + 30
    cw, ch = int(size * 0.45), int(size * 0.42)

    # Sombra debajo
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([cx - cw - 20, cy + ch - 10, cx + cw + 50, cy + ch + 30], fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    img.paste(shadow, (0, 0), shadow)
    d = ImageDraw.Draw(img)

    # Cuerpo de la taza (trapecio redondeado)
    taper = 15  # la base es mas angosta
    body_pts = [
        (cx - cw, cy - ch // 2),          # top-left
        (cx + cw, cy - ch // 2),           # top-right
        (cx + cw - taper, cy + ch),        # bottom-right
        (cx - cw + taper, cy + ch),        # bottom-left
    ]
    d.polygon(body_pts, fill=cup_color)

    # Redondear bordes con circulos en esquinas inferiores
    br = 20
    d.ellipse([cx - cw + taper - br, cy + ch - br, cx - cw + taper + br, cy + ch + br], fill=cup_color)
    d.ellipse([cx + cw - taper - br, cy + ch - br, cx + cw - taper + br, cy + ch + br], fill=cup_color)

    # Borde superior (elipse)
    rim_h = 20
    d.ellipse([cx - cw - 5, cy - ch // 2 - rim_h, cx + cw + 5, cy - ch // 2 + rim_h], fill=cup_color)

    # Cafe adentro (elipse oscura)
    d.ellipse([cx - cw + 8, cy - ch // 2 - rim_h + 6, cx + cw - 8, cy - ch // 2 + rim_h - 2], fill=coffee_color)

    # Reflejo en el cafe
    d.ellipse([cx - cw // 3, cy - ch // 2 - 4, cx, cy - ch // 2 + 6], fill=(139, 80, 48, 120))

    # Highlight en la taza (reflejo de luz)
    highlight = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(highlight)
    hd.rounded_rectangle([cx - cw + 20, cy - ch // 2 + 20, cx - cw + 50, cy + ch - 40],
                          radius=10, fill=(255, 255, 255, 30))
    img.paste(highlight, (0, 0), highlight)

    # Handle (asa) - con doble arco
    d = ImageDraw.Draw(img)
    handle_x = cx + cw
    handle_y = cy
    d.arc([handle_x - 10, handle_y - 50, handle_x + 60, handle_y + 50],
          -70, 70, fill=cup_color, width=16)
    d.arc([handle_x - 10, handle_y - 50, handle_x + 60, handle_y + 50],
          -70, 70, fill=(0, 0, 0, 30), width=4)

    # Vapor (3 curvas con blur)
    steam = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(steam)
    for i, (sx, sw) in enumerate([(cx - 40, 25), (cx, 30), (cx + 40, 22)]):
        opacity = 90 - i * 20
        sy = cy - ch // 2 - 40
        sd.arc([sx - sw, sy - 80, sx + sw, sy], 180, 360, fill=(255, 255, 255, opacity), width=3)
        sd.arc([sx - sw + 5, sy - 140, sx + sw - 5, sy - 70], 0, 180, fill=(255, 255, 255, opacity - 20), width=2)
    steam = steam.filter(ImageFilter.GaussianBlur(3))
    img.paste(steam, (0, 0), steam)

    # Plato
    d = ImageDraw.Draw(img)
    d.ellipse([cx - cw - 30, cy + ch + 5, cx + cw + 60, cy + ch + 30], fill=(160, 112, 80, 180))

    return img


# ═══════════════════════════════════════════════════════
# PAW PRINT - Huella de perro
# ═══════════════════════════════════════════════════════
def make_paw(size=400, color="#d4a574"):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2 + size // 8

    from engine import parse_color
    col = parse_color(color)

    # Pad principal (elipse grande)
    pw, ph = size // 3, size // 4
    d.ellipse([cx - pw, cy - ph, cx + pw, cy + ph], fill=col)

    # 4 dedos (ellipses)
    toes = [
        (cx - pw + 10, cy - ph - size // 5, size // 6, size // 5),       # izq exterior
        (cx - pw // 2 + 5, cy - ph - size // 4 - 10, size // 6, size // 5),  # izq interior
        (cx + pw // 2 - 5, cy - ph - size // 4 - 10, size // 6, size // 5),  # der interior
        (cx + pw - 10, cy - ph - size // 5, size // 6, size // 5),       # der exterior
    ]
    for tx, ty, tw, th in toes:
        d.ellipse([tx - tw, ty - th, tx + tw, ty + th], fill=col)

    return img


# ═══════════════════════════════════════════════════════
# COFFEE BEAN - Grano de cafe
# ═══════════════════════════════════════════════════════
def make_coffee_bean(size=200, color="#3d1e0a"):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    from engine import parse_color
    col = parse_color(color)

    cx, cy = size // 2, size // 2
    rw, rh = size // 3, size * 2 // 5

    # Forma del grano (elipse)
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=col)

    # Linea central (surco del grano)
    lighter = (col[0] + 30, col[1] + 15, col[2] + 5, col[3])
    d.arc([cx - rw + 10, cy - rh + 15, cx + rw - 10, cy + rh - 15], 170, 370, fill=lighter, width=3)

    # Highlight sutil
    d.ellipse([cx - rw + 15, cy - rh + 20, cx - 5, cy - 10], fill=(255, 255, 255, 20))

    return img


# ═══════════════════════════════════════════════════════
# DOG BONE - Hueso de perro
# ═══════════════════════════════════════════════════════
def make_bone(size=400, color="#f0e0d0"):
    img = Image.new("RGBA", (size, size // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    from engine import parse_color
    col = parse_color(color)

    w, h = size, size // 2
    cx, cy = w // 2, h // 2
    # Barra central
    bar_h = h // 3
    d.rounded_rectangle([w // 5, cy - bar_h // 2, w * 4 // 5, cy + bar_h // 2], radius=bar_h // 2, fill=col)
    # Extremos (4 circulos)
    knob = h // 3
    d.ellipse([10, 5, 10 + knob * 2, 5 + knob * 2], fill=col)
    d.ellipse([10, h - 5 - knob * 2, 10 + knob * 2, h - 5], fill=col)
    d.ellipse([w - 10 - knob * 2, 5, w - 10, 5 + knob * 2], fill=col)
    d.ellipse([w - 10 - knob * 2, h - 5 - knob * 2, w - 10, h - 5], fill=col)

    return img


# ═══════════════════════════════════════════════════════
# CHART BARS - Icono de barras de grafico
# ═══════════════════════════════════════════════════════
def make_chart_bars(size=400, color="#7c6bf5"):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    from engine import parse_color
    col = parse_color(color)

    margin = size // 8
    n_bars = 5
    bar_w = (size - margin * 2) // (n_bars * 2)
    heights = [0.3, 0.5, 0.4, 0.7, 1.0]
    max_h = size - margin * 2

    for i, h_pct in enumerate(heights):
        bx = margin + i * bar_w * 2
        bh = int(max_h * h_pct)
        by = size - margin - bh
        alpha = int(100 + 155 * h_pct)
        bar_col = col[:3] + (alpha,)
        d.rounded_rectangle([bx, by, bx + bar_w, size - margin], radius=bar_w // 3, fill=bar_col)

    return img


# ═══════════════════════════════════════════════════════
# GENERAR TODOS
# ═══════════════════════════════════════════════════════
print("Generando assets...")
save(make_coffee_cup(600), "coffee_cup")
save(make_coffee_cup(600, "#ffffff", "#6b8a5e"), "coffee_cup_white")
save(make_paw(400, "#d4a574"), "paw_beige")
save(make_paw(400, "#ffffff"), "paw_white")
save(make_paw(400, "#7c6bf5"), "paw_accent")
save(make_coffee_bean(200, "#3d1e0a"), "bean_dark")
save(make_coffee_bean(200, "#6b3a1a"), "bean_medium")
save(make_bone(400, "#f0e0d0"), "bone_white")
save(make_bone(400, "#d4a574"), "bone_beige")
save(make_chart_bars(400, "#7c6bf5"), "chart_accent")
save(make_chart_bars(400, "#22c55e"), "chart_green")
print("OK")
