"""
Sistema de validacion de calidad para GC Canva.
Chequea assets y composiciones antes de usarlas.
"""
from PIL import Image
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "static", "assets", "images")
MIN_RESOLUTION = 400  # minimo aceptable en px
GOOD_RESOLUTION = 800  # ideal


def check_asset(name):
    """Valida un asset. Retorna (ok, issues)."""
    issues = []
    path = None
    for ext in [".webp", ".png", ".jpg"]:
        p = os.path.join(ASSETS_DIR, name + ext)
        if os.path.exists(p):
            path = p
            break
    if not path:
        return False, [f"Asset '{name}' no encontrado"]

    img = Image.open(path)
    w, h = img.size

    # Resolucion
    if w < MIN_RESOLUTION or h < MIN_RESOLUTION:
        issues.append(f"BAJA RESOLUCION: {w}x{h} (minimo {MIN_RESOLUTION}px)")
    elif w < GOOD_RESOLUTION or h < GOOD_RESOLUTION:
        issues.append(f"RESOLUCION MEDIA: {w}x{h} (ideal >={GOOD_RESOLUTION}px)")

    # Transparencia
    if img.mode == "RGBA":
        alpha = img.split()[3]
        extrema = alpha.getextrema()
        if extrema[0] > 250:
            issues.append("SIN TRANSPARENCIA REAL (alpha todo 255)")
        # Verificar bordes blancos
        pixels = list(alpha.getdata())
        border_pixels = []
        for y in range(h):
            for x in [0, 1, 2, w-3, w-2, w-1]:
                border_pixels.append(pixels[y * w + x])
        for x in range(w):
            for y in [0, 1, 2, h-3, h-2, h-1]:
                border_pixels.append(pixels[y * w + x])
        opaque_border = sum(1 for p in border_pixels if p > 200) / max(len(border_pixels), 1)
        if opaque_border > 0.3:
            issues.append(f"POSIBLE BORDE OPACO: {opaque_border:.0%} de bordes son opacos")

    # Tamano archivo
    file_size = os.path.getsize(path) / 1024
    if file_size < 2:
        issues.append(f"ARCHIVO MUY CHICO: {file_size:.1f}KB (posible corrupcion)")

    ok = not any("BAJA" in i or "SIN TRANS" in i for i in issues)
    return ok, issues


def check_composition(img, spec):
    """Valida una composicion generada."""
    issues = []
    w, h = img.size

    # Verificar que no hay elementos fuera del canvas
    for el in spec.get("elements", []):
        ex = int(el.get("x", 0))
        ey = int(el.get("y", 0))
        ew = int(el.get("w", el.get("r", 0)) * 2 if el.get("r") else el.get("w", 0))
        eh = int(el.get("h", el.get("r", 0)) * 2 if el.get("r") else el.get("h", 0))
        if ex + ew > w * 1.1 or ey + eh > h * 1.1:
            issues.append(f"FUERA DE CANVAS: {el.get('type')} en ({ex},{ey}) size ({ew},{eh})")

    # Verificar que no hay texto cuando se pide sin texto
    # (esto lo chequea el caller)

    return len(issues) == 0, issues


def audit_all_assets():
    """Audita todos los assets del proyecto."""
    print("=" * 60)
    print("  AUDITORIA DE ASSETS")
    print("=" * 60)
    good, bad = 0, 0
    for f in sorted(os.listdir(ASSETS_DIR)):
        if not f.endswith((".webp", ".png")):
            continue
        name = os.path.splitext(f)[0]
        ok, issues = check_asset(name)
        if ok and not issues:
            good += 1
        elif ok:
            print(f"  WARN {f}: {'; '.join(issues)}")
            good += 1
        else:
            print(f"  BAD  {f}: {'; '.join(issues)}")
            bad += 1
    print(f"---\nBuenos: {good} | Malos: {bad}")
    return bad == 0


if __name__ == "__main__":
    audit_all_assets()
