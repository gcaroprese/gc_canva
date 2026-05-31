"""
GC Canva - Sistema de recursos
Descarga imagenes de APIs gratuitas y renderiza iconos SVG del catalogo.
"""
import os
import io
import json
import hashlib
from PIL import Image, ImageDraw

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(PROJECT_ROOT, "static", "cache")
ICONS_CATALOG = os.path.join(PROJECT_ROOT, "static", "assets", "icons", "catalog.json")

os.makedirs(CACHE_DIR, exist_ok=True)

_catalog = None

def _load_catalog():
    global _catalog
    if _catalog is None:
        with open(ICONS_CATALOG, "r", encoding="utf-8") as f:
            _catalog = json.load(f)
    return _catalog


def get_icon_paths(icon_id, category=None):
    """Busca un icono por ID en el catalogo. Retorna (paths, is_stroke)."""
    cat = _load_catalog()
    for c in cat.get("categories", []):
        if category and c["id"] != category:
            continue
        for icon in c.get("icons", []):
            if icon["id"] == icon_id:
                return icon.get("paths", []), icon.get("stroke", False)
    return None, False


def render_icon_to_image(icon_id, size=200, color="#000000", category=None, padding=20):
    """Renderiza un icono SVG del catalogo como imagen PIL (RGBA).
    Usa una tecnica simple: dibuja los paths como lineas/formas basicas.
    Para iconos stroke-based, dibuja las curvas del SVG path.
    """
    paths, is_stroke = get_icon_paths(icon_id, category)
    if not paths:
        # Fallback: cuadrado con X
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([10, 10, size-10, size-10], outline=color, width=2)
        d.line([10, 10, size-10, size-10], fill=color, width=2)
        d.line([size-10, 10, 10, size-10], fill=color, width=2)
        return img

    # Usar cairosvg si esta disponible, sino hacer render basico
    try:
        import cairosvg
        svg_str = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">'
        for p in paths:
            if is_stroke:
                svg_str += f'<path d="{p}" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
            else:
                svg_str += f'<path d="{p}" fill="{color}"/>'
        svg_str += '</svg>'
        png_data = cairosvg.svg2png(bytestring=svg_str.encode(), output_width=size, output_height=size)
        return Image.open(io.BytesIO(png_data)).convert("RGBA")
    except ImportError:
        pass

    # Fallback sin cairosvg: render basico del icono como placeholder
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Dibujar un simbolo representativo basado en el ID
    from engine import parse_color
    col = parse_color(color)
    margin = padding
    inner = size - margin * 2

    # Iconos basicos hardcoded para los mas comunes
    basic_icons = {
        "star": lambda: _draw_star(d, size//2, size//2, inner//2, inner//4, 5, col),
        "heart": lambda: _draw_heart(d, margin, margin, inner, col),
        "home": lambda: _draw_home(d, margin, margin, inner, col),
        "coffee": lambda: _draw_coffee(d, margin, margin, inner, col),
        "paw": lambda: _draw_paw(d, size//2, size//2, inner//3, col),
    }
    if icon_id in basic_icons:
        basic_icons[icon_id]()
    else:
        # Generico: circulo con el primer caracter del ID
        d.ellipse([margin, margin, size-margin, size-margin], outline=col, width=max(2, size//30))
    return img


def _draw_star(d, cx, cy, outer, inner, points, color):
    import math
    pts = []
    for i in range(points*2):
        a = math.radians(-90 + 180*i/points)
        r = outer if i % 2 == 0 else inner
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    d.polygon(pts, fill=color)

def _draw_heart(d, x, y, s, color):
    d.ellipse([x+s//4, y, x+s//2+s//4, y+s//2], fill=color)
    d.ellipse([x+s//2-s//4, y, x+s, y+s//2], fill=color)
    d.polygon([(x, y+s//3), (x+s//2, y+s), (x+s, y+s//3)], fill=color)

def _draw_home(d, x, y, s, color):
    d.polygon([(x+s//2, y), (x, y+s//2), (x+s, y+s//2)], fill=color)
    d.rectangle([x+s//5, y+s//2, x+s*4//5, y+s], fill=color)

def _draw_coffee(d, x, y, s, color):
    d.rounded_rectangle([x+s//6, y+s//3, x+s*2//3, y+s], radius=s//10, fill=color)
    d.ellipse([x+s//6, y+s//4, x+s*2//3, y+s//2], fill=color)
    d.arc([x+s*2//3, y+s//3+s//6, x+s, y+s*2//3+s//6], -60, 60, fill=color, width=max(2, s//15))

def _draw_paw(d, cx, cy, r, color):
    d.ellipse([cx-r, cy-r//3, cx+r, cy+r+r//3], fill=color)
    offsets = [(-r*2//3, -r), (0, -r-r//4), (r*2//3, -r), (r, -r//3)]
    for ox, oy in offsets:
        pr = r//3
        d.ellipse([cx+ox-pr, cy+oy-pr, cx+ox+pr, cy+oy+pr], fill=color)


def download_stock_image(query, width=800, height=600):
    """Descarga una imagen stock gratuita de picsum.photos (no requiere API key).
    Retorna imagen PIL o None si falla.
    """
    import urllib.request

    # Cache basado en query+size
    cache_key = hashlib.md5(f"{query}_{width}_{height}".encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.jpg")

    if os.path.exists(cache_path):
        return Image.open(cache_path).convert("RGBA")

    try:
        # picsum.photos - imagenes random de alta calidad
        url = f"https://picsum.photos/{width}/{height}"
        req = urllib.request.Request(url, headers={"User-Agent": "GCCanva/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        with open(cache_path, "wb") as f:
            f.write(data)
        return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception as e:
        print(f"[resources] Error descargando imagen: {e}")
        return None


def list_cached_images():
    """Lista imagenes en cache."""
    if not os.path.isdir(CACHE_DIR):
        return []
    return [f for f in os.listdir(CACHE_DIR) if f.endswith(('.jpg', '.png', '.webp'))]


def list_icons():
    """Lista todos los iconos disponibles organizados por categoria."""
    cat = _load_catalog()
    result = {}
    for c in cat.get("categories", []):
        result[c["id"]] = {
            "name": c["name"],
            "icons": [ic["id"] for ic in c.get("icons", [])]
        }
    return result
