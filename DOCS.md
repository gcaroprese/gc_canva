# GC Canva - Documentacion

## Inicio rapido

```bash
# Ventana nativa (recomendado)
start.bat

# En browser
venv\Scripts\python app.py
# → http://localhost:5050
```

## Dos modos de uso

### 1. Editor Visual (Fabric.js)
Canvas interactivo con herramientas de dibujo, texto, formas, iconos.
Export client-side en WebP/PNG/JPG.

### 2. Claude JSON Mode (Pillow)
JSON spec compacto → imagen renderizada server-side con alta calidad.
Baja tokens. 84 fuentes. Sombras, gradientes, opacidades.

## JSON Spec - Referencia Completa

```json
{
  "width": 1200, "height": 630,
  "background": "#1a1a2e",
  "format": "webp", "quality": 92,
  "filename": "mi-diseno",
  "elements": [
    {"type":"gradient","x":0,"y":0,"w":1200,"h":630,"color1":"#6366f1","color2":"#1a1a2e","direction":"diagonal"},
    {"type":"rect","x":40,"y":40,"w":400,"h":300,"color":"#7c6bf5","opacity":0.08,"radius":20},
    {"type":"text","text":"Titulo","x":600,"y":280,"size":72,"color":"#fff","align":"center","bold":true,"font":"roboto slab","shadow":true,"shadow_blur":8}
  ]
}
```

### Elementos

| Tipo | Props principales |
|------|-------------------|
| rect | x,y,w,h,color,radius,opacity,stroke,stroke_width |
| circle | x,y,r,color,opacity |
| ellipse | x,y,w,h,color,opacity |
| triangle | x,y,w,h,color |
| polygon | x,y,r,sides,angle,color |
| star | x,y,r,inner_r,points,color |
| line | x1,y1,x2,y2,color,width |
| gradient | x,y,w,h,color1,color2,direction(horizontal/vertical/diagonal/radial) |
| text | x,y,text,size,color,font,bold,italic,align(left/center/right),valign(top/center/bottom),shadow,shadow_blur,text_stroke,max_width,spacing |
| image | src(data:base64),x,y,w,h |

### Fuentes (claves para `font`)

**Sans:** arial, calibri, mukta, segoe ui, tahoma, verdana, bahnschrift, candara, corbel, trebuchet ms
**Serif:** georgia, times, roboto slab, optimus princeps, rockwell
**Display:** impact, cooper black, moon bold, moon light, narnia, rakoon
**Mono:** consolas, courier new
**Decorativa:** gabriola, bananas

### Colores
`#ff0000`, `#f00`, `#ff000080` (hex+alpha), `rgb(255,0,0)`, `rgba(255,0,0,0.5)`

## API

| Ruta | Metodo | Uso |
|------|--------|-----|
| /api/preview | POST | Preview base64 desde JSON |
| /api/download | POST | Descarga imagen desde JSON |
| /api/qr | POST | Genera QR (text,size,color,bg_color) |
| /api/remove-bg | POST | Quita fondo (requiere rembg) |
| /api/filter | POST | Filtros: brightness,contrast,saturation,blur,grayscale,sepia |
| /api/fonts | GET | Lista fuentes |
| /api/presets | GET | Presets de canvas |

## Presets (32)

Social, Video, Presentacion, Web, Print, Etsy, Blog, Email

## Plantillas AI (12)

Social Elegante, YouTube Thumb, Blog Inforket, Blog Gabriel, Hatton Naturals, Pawsitive Brews, Etsy Perros, Etsy Remera, Iglesia Post, Real Estate, Banner Tech, Tarjeta Personal

## Shortcuts

V=Select, T=Texto, R=Rect, C=Circulo, L=Linea, Del=Borrar
Ctrl+Z/Y=Undo/Redo, Ctrl+C/V=Copy/Paste, Ctrl+D=Duplicar, Ctrl+G=Agrupar
Flechas=Mover 1px, Shift+Flechas=10px, Alt+Drag=Pan, Scroll=Zoom

## Performance

Promedio: 236ms generacion + 650ms export. WebP q92 ~47KB por imagen.
WebP es ~50% mas chico que PNG y ~40% mas chico que JPG con calidad identica.

## Instalacion

```bash
python -m venv venv
venv\Scripts\pip install flask pillow "qrcode[pil]" pywebview
```
