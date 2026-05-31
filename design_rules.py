"""
Reglas de diseno y layouts predefinidos para composiciones de calidad.
Aplica principios: rule of thirds, jerarquia visual, espaciado consistente.
"""

def blog_og_layout(width=1200, height=675):
    """Layout estandar para blog OG image. Retorna posiciones."""
    margin = int(width * 0.05)
    return {
        "width": width, "height": height,
        "margin": margin,
        "title_x": margin, "title_y": int(height * 0.15),
        "subtitle_x": margin, "subtitle_y": int(height * 0.55),
        "brand_x": margin, "brand_y": int(height * 0.85),
        "image_x": int(width * 0.55), "image_y": 0,
        "image_w": int(width * 0.45), "image_h": height,
        "accent_line_y": int(height * 0.48),
    }


def social_square_layout(size=1080):
    """Layout para post cuadrado."""
    margin = int(size * 0.06)
    return {
        "width": size, "height": size,
        "margin": margin,
        "center_x": size // 2, "center_y": size // 2,
        "hero_x": int(size * 0.1), "hero_y": int(size * 0.05),
        "hero_w": int(size * 0.8), "hero_h": int(size * 0.55),
        "title_x": size // 2, "title_y": int(size * 0.68),
        "subtitle_x": size // 2, "subtitle_y": int(size * 0.82),
        "brand_x": size // 2, "brand_y": int(size * 0.94),
    }


def card_layout(width=1200, height=675):
    """Layout con card izquierda + hero derecha."""
    margin = int(width * 0.04)
    card_w = int(width * 0.42)
    return {
        "width": width, "height": height,
        "margin": margin,
        "card_x": margin, "card_y": margin,
        "card_w": card_w, "card_h": height - margin * 2,
        "hero_x": card_w + margin * 2,
        "hero_y": 0,
        "hero_w": width - card_w - margin * 3,
        "hero_h": height,
    }


def validate_composition(spec):
    """Valida que la composicion no tenga errores obvios."""
    issues = []
    w = spec.get("width", 800)
    h = spec.get("height", 600)

    for i, el in enumerate(spec.get("elements", [])):
        etype = el.get("type", "")
        ex = int(el.get("x", 0))
        ey = int(el.get("y", 0))

        # Verificar elementos fuera del canvas
        if etype in ("rect", "ellipse"):
            ew = int(el.get("w", 0))
            eh = int(el.get("h", 0))
            if ex > w or ey > h:
                issues.append(f"[{i}] {etype} completamente fuera del canvas ({ex},{ey})")
            if ex + ew > w * 1.2:
                issues.append(f"[{i}] {etype} se sale mucho del canvas (x+w={ex+ew}, canvas_w={w})")

        # Verificar texto (no deberia haber si se pide sin texto)
        # Se chequea externamente

        # Verificar assets de baja res
        if etype == "asset":
            name = el.get("name", "")
            target_w = int(el.get("w", 0))
            # Si se escala a mas del doble del original, se pixela
            # (esto lo valida el engine)

    return issues
