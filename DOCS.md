# GC Canva v4.6

## Quick Start
```bash
start.bat              # ventana nativa
venv\Scripts\python app.py  # browser http://localhost:5050
```

## Templates (6 pro templates)
```python
from templates_lib import blog_dark_split
spec = blog_dark_split(title="Mi Titulo", accent="#7c6bf5", brand="misite.com")
```
| Template | Params | Size |
|----------|--------|------|
| blog_dark_split | title, subtitle, accent, bg_photo, brand | 1200x675 |
| blog_photo_hero | title, subtitle, accent, photo, brand | 1200x675 |
| dashboard_card | accent | 1200x675 |
| product_showcase | product_image, accent, bg_tint | 1200x675 |
| church_post | verse, reference, church_name, accent, bg_photo | 1080x1080 |
| etsy_listing | title_lines, price, accent, product_image | 2000x2000 |

## API
| Ruta | Metodo | Uso |
|------|--------|-----|
| /api/preview | POST | Preview JSON spec |
| /api/download | POST | Download JSON spec |
| /api/template/\<id\> | POST | Generate from template |
| /api/templates | GET | List templates |
| /api/assets | GET | List transparent assets (47) |
| /api/qr | POST | QR code |
| /api/filter | POST | Image filters |
| /api/remove-bg | POST | Background removal (rembg) |
| /api/fonts | GET | Available fonts (84) |
| /api/presets | GET | Canvas size presets (32) |

## JSON Spec
```json
{
  "width": 1200, "height": 675,
  "background": "dark", "antialias": 2,
  "post": {"vignette": true, "tint": "#7c6bf5", "grain": true},
  "elements": [
    {"type": "gradient", ...},
    {"type": "text", "text": "Title", "text_gradient": {"color1": "#fff", "color2": "#aaa"}},
    {"type": "asset", "name": "green_tea_nobg", "x": 100, "y": 100, "w": 400},
    {"type": "contact_shadow", "x": 200, "y": 500, "w": 300, "h": 20, "blur": 15}
  ]
}
```

## Elements (17)
rect, circle, ellipse, triangle, polygon, star, line, gradient, pill, divider, text, image, asset, arc, ring, grid, repeat, contact_shadow

## Post-processing
vignette, tint (color grading), grain (film noise), blur (depth of field), antialias (2x supersampling)

## Quality tools
- `python quality_check.py` — audit all assets
- `python tests/full_test.py` — generate and verify all templates
- Assets auto-validated on load (warns <300px)

## Install
```bash
python -m venv venv
venv\Scripts\pip install flask pillow "qrcode[pil]" pywebview "rembg[cpu]"
python setup_fonts.py
```
