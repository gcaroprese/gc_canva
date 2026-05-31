# GC Canva

Editor de imagenes tipo Canva con Python. Dos modos de uso:

1. **Editor Visual** - Canvas interactivo con Fabric.js (browser/ventana nativa)
2. **JSON Mode** - Genera imagenes server-side con Pillow desde un JSON compacto (ideal para AI/Claude, bajo consumo de tokens)

## Quick Start

```bash
# Clonar
git clone https://github.com/gcaroprese/gc_canva.git
cd gc_canva

# Setup
python -m venv venv
venv\Scripts\pip install flask pillow "qrcode[pil]" pywebview
python setup_fonts.py  # copiar fuentes de Windows

# Correr
start.bat              # ventana nativa
# o: venv\Scripts\python app.py  ->  http://localhost:5050
```

## JSON Mode - Ejemplo

```json
{
  "width": 1200, "height": 630,
  "background": "dark",
  "elements": [
    {"type": "gradient", "x": 0, "y": 0, "w": 1200, "h": 630,
     "stops": [[0,"#0a0518"],[0.5,"#1e1b4b"],[1,"#0a0518"]], "angle": 135},
    {"type": "pill", "x": 60, "y": 60, "text": "NUEVO", "color": "accent"},
    {"type": "text", "text": "Titulo", "x": 600, "y": 280, "size": 72,
     "color": "white", "align": "center", "bold": true, "font": "mukta",
     "shadow": true, "shadow_blur": 10}
  ]
}
```

## Features

**Engine (Pillow)**
- 14 tipos de elementos: rect, circle, ellipse, triangle, polygon, star, line, gradient, pill, divider, text, image, grid, repeat
- Gradientes: multi-stop (2+ colores), angulo libre (0-360), horizontal/vertical/diagonal/radial
- Texto: gradient fill, shadow blur, outline, bg_color highlight, auto-wrap (max_width), valign
- Shadow universal en todas las formas (drop shadow + glow)
- Image clip (circle, rounded, ellipse)
- Rotacion, opacidad, anti-aliasing 2x
- 84 fuentes (custom + Windows), 22 colores con nombre
- Grid layout y repeat para patrones
- ~250ms promedio, ~43KB WebP

**Editor (Fabric.js)**
- 10 herramientas de dibujo
- Panel de propiedades completo
- 80+ iconos SVG en 8 categorias
- 48 colores rapidos, 16 gradientes preset
- 32 presets de canvas (Social, Video, Print, Etsy, Blog...)
- 12 plantillas AI listas para usar
- Undo/redo, copy/paste, align, layers, zoom, grid
- Export WebP/PNG/JPG con escala 1-4x
- QR code generator, image filters, background removal (rembg)

## API

```
POST /api/preview   - Preview base64 desde JSON
POST /api/download  - Descarga imagen desde JSON
POST /api/qr        - Genera QR code
POST /api/filter    - Aplica filtros (brightness, contrast, blur, sepia...)
GET  /api/fonts     - Lista fuentes disponibles
GET  /api/presets   - Lista presets de canvas
```

## Docs

Ver [DOCS.md](DOCS.md) para referencia completa de la JSON spec.

## Stack

Python 3.12 | Flask | Pillow | Fabric.js v5 | pywebview
