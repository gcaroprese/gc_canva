# GC Canva - Documentacion v4.4

## Inicio rapido
```bash
start.bat              # ventana nativa
venv\Scripts\python app.py  # browser → http://localhost:5050
```

## Templates reutilizables (templates_lib.py)

```python
from templates_lib import blog_dark_split, product_showcase, dashboard_card
spec = blog_dark_split(title="Mi Titulo", accent="#7c6bf5", brand="misite.com")
```

| Template | Uso | Parametros |
|----------|-----|------------|
| blog_dark_split | Blog OG con split foto/texto | title, subtitle, accent, bg_photo, brand |
| blog_photo_hero | Foto fullscreen + texto centrado | title, subtitle, accent, photo, brand |
| dashboard_card | Analytics sin texto | accent |
| product_showcase | Producto centrado con glow | product_image, accent, bg_tint |

## JSON Spec

```json
{
  "width": 1200, "height": 675,
  "background": "dark",
  "antialias": 2,
  "post": {"vignette": true, "tint": "#7c6bf5", "tint_strength": 0.03, "grain": true},
  "elements": [...]
}
```

## Elementos (16 tipos)
rect, circle, ellipse, triangle, polygon, star, line, gradient, pill, divider, text, image, asset, arc, ring, grid, repeat

## Post-processing
- **vignette**: oscurece bordes (vignette_strength 0-1)
- **tint**: unifica color (tint + tint_strength)
- **grain**: textura fotografica (grain_strength)
- **blur**: profundidad de campo en imagenes (blur en el elemento)
- **antialias**: render global a Nx (2 = 2x supersampling + LANCZOS)

## Features clave
- Shadow universal, gradient text, multi-stop gradients, angle gradients
- letter_spacing, uppercase, max_width, bg_color, valign
- Image clip (circle/rounded/ellipse), rotate, blur
- Grid layout, repeat patterns
- Pills anti-aliased con centrado vertical
- 22 named colors, 84 fuentes

## Assets (static/assets/images/)
47 assets con transparencia. Correr `python quality_check.py` para auditar.

## API
POST /api/preview, /api/download, /api/qr, /api/filter, /api/remove-bg
GET /api/fonts, /api/presets

## Shortcuts
V=Select T=Texto R=Rect C=Circulo L=Linea Del=Borrar
Ctrl+Z/Y Ctrl+C/V/D/G/A | Flechas=1px Shift+10px | Alt+Drag=Pan Scroll=Zoom
