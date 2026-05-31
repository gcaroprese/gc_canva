"""Auto-review: analiza calidad visual de las imagenes generadas."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageStat

OUT = os.path.join(os.path.dirname(__file__), "output", "final")

def analyze(path):
    """Analiza una imagen y retorna metricas de calidad."""
    img = Image.open(path).convert("RGB")
    stat = ImageStat.Stat(img)
    w, h = img.size
    avg_brightness = sum(stat.mean) / 3
    contrast = sum(stat.stddev) / 3
    file_kb = os.path.getsize(path) / 1024

    issues = []
    # Brillo
    if avg_brightness < 10:
        issues.append("MUY OSCURA")
    elif avg_brightness > 220:
        issues.append("MUY CLARA")

    # Contraste
    if contrast < 15:
        issues.append("BAJO CONTRASTE")

    # Tamaño archivo
    if file_kb < 10:
        issues.append("ARCHIVO MUY CHICO")
    elif file_kb > 500:
        issues.append("ARCHIVO GRANDE (optimizar)")

    # Resolucion
    if w < 800 or h < 400:
        issues.append(f"BAJA RES ({w}x{h})")

    score = 10
    if issues:
        score -= len(issues) * 2

    return {
        "size": f"{w}x{h}",
        "brightness": round(avg_brightness, 1),
        "contrast": round(contrast, 1),
        "file_kb": round(file_kb, 1),
        "score": max(0, score),
        "issues": issues,
    }

if __name__ == "__main__":
    print("=" * 70)
    print(f"  {'Imagen':30s} {'Size':>10s} {'Bright':>7s} {'Contr':>7s} {'KB':>6s} {'Score':>5s}")
    print("-" * 70)
    total_score = 0
    count = 0
    for f in sorted(os.listdir(OUT)):
        if not f.endswith(".webp"):
            continue
        path = os.path.join(OUT, f)
        r = analyze(path)
        status = " ".join(r["issues"]) if r["issues"] else "OK"
        print(f"  {f:30s} {r['size']:>10s} {r['brightness']:>7.1f} {r['contrast']:>7.1f} {r['file_kb']:>6.1f} {r['score']:>5d}  {status}")
        total_score += r["score"]
        count += 1
    print("-" * 70)
    avg = total_score / max(count, 1)
    print(f"  Score promedio: {avg:.1f}/10 ({count} imagenes)")
    print("=" * 70)
