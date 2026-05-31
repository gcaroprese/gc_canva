/* ============================================================
   GC CANVA - Editor Principal
   ============================================================ */
'use strict';

/* ------------------------------------------------------------------ */
/* STATE                                                               */
/* ------------------------------------------------------------------ */
const S = {
  tool: 'select',
  canvasW: 800, canvasH: 600,
  zoom: 1,
  isDrawing: false, isPanning: false,
  drawStart: { x: 0, y: 0 },
  currentShape: null,
  clipboard: null,
  history: [], histIdx: -1,
  histMax: 60,
  showGrid: false, snapGrid: false, gridSize: 20,
  currentFill: '#7c6bf5',
  currentStroke: '',
  currentStrokeW: 0,
  catalog: null,
  iconCategory: 'general',
  selectedObj: null,
  filterTarget: null,
  lastPanX: 0, lastPanY: 0,
};

/* ------------------------------------------------------------------ */
/* CANVAS                                                               */
/* ------------------------------------------------------------------ */
const canvas = new fabric.Canvas('mainCanvas', {
  width: S.canvasW, height: S.canvasH,
  backgroundColor: '#ffffff',
  preserveObjectStacking: true,
  selection: true,
});

// Custom selection style
fabric.Object.prototype.set({
  borderColor: '#6366f1',
  cornerColor: '#6366f1',
  cornerStyle: 'circle',
  cornerSize: 8,
  transparentCorners: false,
  borderScaleFactor: 1.5,
});

/* ------------------------------------------------------------------ */
/* ZOOM & PAN                                                          */
/* ------------------------------------------------------------------ */
function setZoom(level) {
  level = Math.min(10, Math.max(0.05, level));
  S.zoom = level;
  canvas.setZoom(level);
  canvas.setWidth(S.canvasW * level);
  canvas.setHeight(S.canvasH * level);
  canvas.renderAll();
  document.getElementById('zoomDisplay').textContent = Math.round(level * 100) + '%';
}

function fitCanvas() {
  const wrap = document.getElementById('canvasWrapper');
  const mw = wrap.clientWidth  - 80;
  const mh = wrap.clientHeight - 80;
  const z = Math.min(mw / S.canvasW, mh / S.canvasH, 1);
  setZoom(z);
}

canvas.on('mouse:wheel', (opt) => {
  const delta = opt.e.deltaY;
  const z = Math.min(10, Math.max(0.05, canvas.getZoom() * (0.999 ** delta)));
  S.zoom = z;
  canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, z);
  canvas.setWidth(S.canvasW * z);
  canvas.setHeight(S.canvasH * z);
  document.getElementById('zoomDisplay').textContent = Math.round(z * 100) + '%';
  opt.e.preventDefault(); opt.e.stopPropagation();
});

// Pan with Alt+drag or middle mouse
canvas.on('mouse:down', (opt) => {
  if (opt.e.altKey || opt.e.button === 1) {
    S.isPanning = true;
    S.lastPanX = opt.e.clientX; S.lastPanY = opt.e.clientY;
    canvas.defaultCursor = 'grabbing';
    canvas.selection = false;
  }
});
canvas.on('mouse:move', (opt) => {
  if (!S.isPanning) return;
  const dx = opt.e.clientX - S.lastPanX;
  const dy = opt.e.clientY - S.lastPanY;
  const vpt = canvas.viewportTransform;
  vpt[4] += dx; vpt[5] += dy;
  canvas.requestRenderAll();
  S.lastPanX = opt.e.clientX; S.lastPanY = opt.e.clientY;
});
canvas.on('mouse:up', (opt) => {
  if (S.isPanning && opt.e.button !== 1) { /* keep if middle still held */ }
  S.isPanning = false;
  canvas.defaultCursor = 'default';
  canvas.selection = true;
});

document.getElementById('zoomInBtn').addEventListener('click', () => setZoom(S.zoom * 1.25));
document.getElementById('zoomOutBtn').addEventListener('click', () => setZoom(S.zoom / 1.25));
document.getElementById('zoomFitBtn').addEventListener('click', fitCanvas);
document.getElementById('zoomDisplay').addEventListener('click', () => {
  const v = prompt('Zoom (%):', Math.round(S.zoom * 100));
  if (v) setZoom(parseInt(v) / 100);
});

/* ------------------------------------------------------------------ */
/* GRID                                                                 */
/* ------------------------------------------------------------------ */
canvas.on('after:render', () => {
  if (!S.showGrid) return;
  const ctx = canvas.getContext('2d');
  const z = canvas.getZoom();
  const gs = S.gridSize * z;
  const vpt = canvas.viewportTransform;
  const ox = vpt[4] % gs, oy = vpt[5] % gs;
  ctx.save();
  ctx.strokeStyle = 'rgba(99,102,241,0.15)';
  ctx.lineWidth = 0.5;
  for (let x = ox; x < canvas.width; x += gs) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
  }
  for (let y = oy; y < canvas.height; y += gs) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }
  ctx.restore();
});

canvas.on('object:moving', (e) => {
  if (!S.snapGrid) return;
  const o = e.target, gs = S.gridSize;
  o.set({ left: Math.round(o.left / gs) * gs, top: Math.round(o.top / gs) * gs });
});

document.getElementById('gridBtn').addEventListener('click', function() {
  S.showGrid = !S.showGrid;
  this.classList.toggle('on', S.showGrid);
  canvas.renderAll();
});
document.getElementById('snapBtn').addEventListener('click', function() {
  S.snapGrid = !S.snapGrid;
  this.classList.toggle('on', S.snapGrid);
});

/* ------------------------------------------------------------------ */
/* HISTORY                                                              */
/* ------------------------------------------------------------------ */
function saveHistory() {
  const json = JSON.stringify(canvas.toJSON(['selectable', 'evented', 'lockMovementX', 'lockMovementY', 'id', 'clipPath']));
  S.history = S.history.slice(0, S.histIdx + 1);
  S.history.push({ state: json, bg: canvas.backgroundColor });
  if (S.history.length > S.histMax) S.history.shift();
  S.histIdx = S.history.length - 1;
  updateHistoryBtns();
}

function undo() {
  if (S.histIdx <= 0) return;
  S.histIdx--;
  restoreHistory(S.histIdx);
}

function redo() {
  if (S.histIdx >= S.history.length - 1) return;
  S.histIdx++;
  restoreHistory(S.histIdx);
}

function restoreHistory(idx) {
  const snap = S.history[idx];
  canvas.loadFromJSON(snap.state, () => {
    canvas.backgroundColor = snap.bg;
    canvas.renderAll();
    updateHistoryBtns();
  });
}

function updateHistoryBtns() {
  document.getElementById('undoBtn').style.opacity = S.histIdx > 0 ? '1' : '0.4';
  document.getElementById('redoBtn').style.opacity = S.histIdx < S.history.length - 1 ? '1' : '0.4';
}

canvas.on('object:modified', saveHistory);
canvas.on('object:added', saveHistory);
canvas.on('object:removed', saveHistory);

document.getElementById('undoBtn').addEventListener('click', undo);
document.getElementById('redoBtn').addEventListener('click', redo);

/* ------------------------------------------------------------------ */
/* TOOLS                                                                */
/* ------------------------------------------------------------------ */
function setTool(tool) {
  S.tool = tool;
  document.querySelectorAll('.tool-btn[data-tool]').forEach(b => {
    b.classList.toggle('active', b.dataset.tool === tool);
  });
  const isSelect = tool === 'select' || tool === 'text';
  canvas.isDrawingMode = false;
  canvas.selection = isSelect;
  canvas.defaultCursor = tool === 'text' ? 'text' : (isSelect ? 'default' : 'crosshair');
  canvas.forEachObject(o => { o.selectable = isSelect; o.evented = isSelect; });
}

document.querySelectorAll('.tool-btn[data-tool]').forEach(btn => {
  btn.addEventListener('click', () => setTool(btn.dataset.tool));
});

/* ------------------------------------------------------------------ */
/* DRAWING                                                              */
/* ------------------------------------------------------------------ */
canvas.on('mouse:down', (opt) => {
  if (S.isPanning || opt.e.altKey) return;
  if (S.tool === 'select') return;
  if (S.tool === 'text') { addText(opt); return; }

  const p = canvas.getPointer(opt.e);
  S.isDrawing = true;
  S.drawStart = { x: p.x, y: p.y };

  const fill = S.currentFill;
  const stroke = S.currentStroke;
  const sw = S.currentStrokeW;

  const defaults = { left: p.x, top: p.y, fill, stroke: stroke || undefined,
                     strokeWidth: sw || 0, originX: 'left', originY: 'top' };

  switch (S.tool) {
    case 'rect':
      S.currentShape = new fabric.Rect({ ...defaults, width: 0, height: 0, rx: 0, ry: 0 });
      break;
    case 'circle':
      S.currentShape = new fabric.Ellipse({ ...defaults, rx: 0, ry: 0 });
      break;
    case 'triangle':
      S.currentShape = new fabric.Triangle({ ...defaults, width: 0, height: 0 });
      break;
    case 'line':
      S.currentShape = new fabric.Line([p.x, p.y, p.x, p.y],
        { stroke: fill, strokeWidth: sw || 2, fill: 'transparent', strokeLineCap: 'round' });
      break;
    case 'arrow':
      S.currentShape = new fabric.Path(`M ${p.x} ${p.y} L ${p.x} ${p.y}`,
        { stroke: fill, strokeWidth: sw || 2, fill: 'transparent', strokeLineCap: 'round' });
      break;
    case 'star':
      S.currentShape = new fabric.Path('M 12 2 l 3 6.3 6.9 1 -5 4.9 1.2 6.9 -6.1-3.2 -6.1 3.2 1.2 -6.9 -5 -4.9 6.9 -1 z',
        { ...defaults, width: 0, height: 0, scaleX: 0, scaleY: 0 });
      break;
    case 'polygon':
      S.currentShape = new fabric.Path('M 12 2 L 21.5 8.9 L 18.6 20 L 5.4 20 L 2.5 8.9 Z',
        { ...defaults, width: 0, height: 0, scaleX: 0, scaleY: 0 });
      break;
    case 'diamond':
      S.currentShape = new fabric.Path('M 12 2 L 21 12 L 12 22 L 3 12 Z',
        { ...defaults, width: 0, height: 0, scaleX: 0, scaleY: 0 });
      break;
    default: return;
  }

  if (S.currentShape) {
    canvas.add(S.currentShape);
    canvas.renderAll();
  }
});

canvas.on('mouse:move', (opt) => {
  if (!S.isDrawing || !S.currentShape) return;
  const p = canvas.getPointer(opt.e);
  const dx = p.x - S.drawStart.x;
  const dy = p.y - S.drawStart.y;
  const w = Math.abs(dx), h = Math.abs(dy);
  const x = Math.min(p.x, S.drawStart.x), y = Math.min(p.y, S.drawStart.y);

  const t = S.tool;
  if (t === 'rect') { S.currentShape.set({ left: x, top: y, width: w, height: h }); }
  else if (t === 'circle') { S.currentShape.set({ left: x, top: y, rx: w / 2, ry: h / 2 }); }
  else if (t === 'triangle') { S.currentShape.set({ left: x, top: y, width: w, height: h }); }
  else if (t === 'line') { S.currentShape.set({ x2: p.x, y2: p.y }); }
  else if (t === 'arrow') {
    const ax = S.drawStart.x, ay = S.drawStart.y, bx = p.x, by = p.y;
    const angle = Math.atan2(by - ay, bx - ax);
    const ah = 16, aw = Math.PI / 7;
    const path = `M ${ax} ${ay} L ${bx} ${by} ` +
      `M ${bx} ${by} L ${bx - ah * Math.cos(angle - aw)} ${by - ah * Math.sin(angle - aw)} ` +
      `M ${bx} ${by} L ${bx - ah * Math.cos(angle + aw)} ${by - ah * Math.sin(angle + aw)}`;
    S.currentShape.set({ path: fabric.util.parsePath(path) });
  }
  else if (['star', 'polygon', 'diamond'].includes(t)) {
    const s = Math.max(w, h) / 24;
    S.currentShape.set({ left: x, top: y, scaleX: s, scaleY: s });
  }

  canvas.renderAll();
});

canvas.on('mouse:up', (opt) => {
  if (!S.isDrawing) return;
  S.isDrawing = false;
  if (S.currentShape) {
    const o = S.currentShape;
    // Remove if too small
    if ((o.width || 0) < 3 && (o.height || 0) < 3 && o.type !== 'line' && o.type !== 'path') {
      canvas.remove(o);
    } else {
      canvas.setActiveObject(o);
    }
    S.currentShape = null;
    canvas.renderAll();
  }
  setTool('select');
});

/* -- Add Text -- */
function addText(opt) {
  const p = canvas.getPointer(opt.e);
  const t = new fabric.IText('Texto', {
    left: p.x, top: p.y,
    fontSize: 36, fill: S.currentFill,
    fontFamily: 'Arial',
    fontWeight: 'normal',
    editable: true,
  });
  canvas.add(t);
  canvas.setActiveObject(t);
  t.enterEditing();
  t.selectAll();
  setTool('select');
}

/* ------------------------------------------------------------------ */
/* SELECTION → PROPERTIES PANEL                                        */
/* ------------------------------------------------------------------ */
canvas.on('selection:created', onSelect);
canvas.on('selection:updated', onSelect);
canvas.on('selection:cleared', () => {
  S.selectedObj = null;
  document.getElementById('propertiesPanel').innerHTML = `
    <div class="no-sel">
      <svg viewBox="0 0 24 24" width="40" height="40"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#4b5563"/></svg>
      <p>Selecciona un elemento para editar sus propiedades</p>
    </div>`;
  document.getElementById('alignBar').classList.add('hidden');
});

canvas.on('object:modified', (e) => {
  if (e.target) { onSelect({ selected: [e.target] }); }
});

function onSelect(e) {
  const objs = canvas.getActiveObjects();
  if (!objs.length) return;
  const obj = objs[0];
  S.selectedObj = obj;
  document.getElementById('alignBar').classList.remove('hidden');
  buildProps(obj, objs.length > 1);
}

function buildProps(obj, multi) {
  const panel = document.getElementById('propertiesPanel');
  const type = obj.type;
  const isLocked = obj.lockMovementX && obj.lockMovementY;

  let html = `
    <div class="prop-section">
      <div class="prop-title">Posicion y Tamaño</div>
      <div class="prop-row">
        <span class="prop-label">X</span>
        <input class="prop-input" id="pX" type="number" value="${Math.round(obj.left || 0)}">
        <span class="prop-label">Y</span>
        <input class="prop-input" id="pY" type="number" value="${Math.round(obj.top || 0)}">
      </div>
      <div class="prop-row">
        <span class="prop-label">W</span>
        <input class="prop-input" id="pW" type="number" value="${Math.round(obj.getScaledWidth() || 0)}">
        <span class="prop-label">H</span>
        <input class="prop-input" id="pH" type="number" value="${Math.round(obj.getScaledHeight() || 0)}">
      </div>
      <div class="prop-row">
        <span class="prop-label">&#8635;</span>
        <input class="prop-input" id="pRot" type="number" value="${Math.round(obj.angle || 0)}" min="-360" max="360">
        <span class="prop-label">°</span>
      </div>
    </div>

    <div class="prop-section">
      <div class="prop-title">Opacidad</div>
      <div class="prop-row">
        <input type="range" id="pOpacity" class="prop-range" min="0" max="100" value="${Math.round((obj.opacity || 1) * 100)}">
        <span class="prop-range-val" id="pOpacityV">${Math.round((obj.opacity || 1) * 100)}%</span>
      </div>
    </div>`;

  // Fill & stroke for non-text, non-image
  if (type !== 'image' && type !== 'i-text' && type !== 'text') {
    const fillColor = (typeof obj.fill === 'string' && obj.fill && obj.fill !== 'transparent') ? obj.fill : '#6366f1';
    html += `
      <div class="prop-section">
        <div class="prop-title">Relleno</div>
        <div class="prop-row">
          <input type="color" id="pFill" class="prop-color" value="${fillColor}">
          <button class="prop-btn" id="pFillNone" style="max-width:80px;font-size:10px">Sin relleno</button>
        </div>
        <div class="prop-title" style="margin-top:8px">Borde</div>
        <div class="prop-row">
          <input type="color" id="pStroke" class="prop-color" value="${obj.stroke || '#000000'}">
          <span class="prop-label">Grosor</span>
          <input class="prop-input" id="pSW" type="number" value="${obj.strokeWidth || 0}" min="0" max="50">
        </div>
        ${type === 'rect' ? `<div class="prop-row"><span class="prop-label">Radio</span>
          <input type="range" id="pRadius" class="prop-range" min="0" max="200" value="${obj.rx || 0}">
          <span class="prop-range-val" id="pRadiusV">${obj.rx || 0}px</span></div>` : ''}
      </div>`;
  }

  // Text properties
  if (type === 'i-text' || type === 'text') {
    const fontOpts = getFontOptions(obj.fontFamily || 'Arial');
    html += `
      <div class="prop-section">
        <div class="prop-title">Texto</div>
        <div class="prop-row">
          <select id="pFont" class="font-select">${fontOpts}</select>
        </div>
        <div class="prop-row">
          <span class="prop-label">Tam</span>
          <input class="prop-input" id="pFontSize" type="number" value="${obj.fontSize || 24}" min="6" max="400" style="width:60px">
          <input type="color" id="pTextColor" class="prop-color" value="${obj.fill || '#000000'}">
        </div>
        <div class="prop-row prop-btn-row">
          <button class="prop-btn ${obj.fontWeight === 'bold' ? 'active' : ''}" id="pBold"><strong>B</strong></button>
          <button class="prop-btn ${obj.fontStyle === 'italic' ? 'active' : ''}" id="pItalic"><em>I</em></button>
          <button class="prop-btn ${obj.underline ? 'active' : ''}" id="pUnderline"><u>U</u></button>
          <button class="prop-btn ${obj.linethrough ? 'active' : ''}" id="pStrikethrough"><s>S</s></button>
        </div>
        <div class="prop-row prop-btn-row">
          <button class="prop-btn ${obj.textAlign === 'left' ? 'active' : ''}" id="pAlignL">&#8592;</button>
          <button class="prop-btn ${(!obj.textAlign || obj.textAlign === 'center') ? 'active' : ''}" id="pAlignC">&#8596;</button>
          <button class="prop-btn ${obj.textAlign === 'right' ? 'active' : ''}" id="pAlignR">&#8594;</button>
          <button class="prop-btn ${obj.textAlign === 'justify' ? 'active' : ''}" id="pAlignJ">&#9644;</button>
        </div>
        <div class="prop-row">
          <span class="prop-label">Espaciado</span>
          <input class="prop-input" id="pLetterSpacing" type="number" value="${obj.charSpacing || 0}" min="-500" max="2000">
        </div>
        <div class="prop-row">
          <span class="prop-label">Altura</span>
          <input class="prop-input" id="pLineHeight" type="number" value="${obj.lineHeight || 1.16}" min="0.5" max="5" step="0.1">
        </div>
      </div>`;
  }

  // Image properties
  if (type === 'image') {
    html += `
      <div class="prop-section">
        <div class="prop-title">Imagen</div>
        <div class="prop-btn-row" style="gap:6px">
          <button class="prop-btn" id="pFilterBtn">&#127798; Ajustar</button>
          <button class="prop-btn" id="pRemoveBgBtn">&#127380; Quitar fondo</button>
        </div>
        <div class="prop-row prop-btn-row" style="margin-top:8px">
          <button class="prop-btn" id="pFlipH">&#8596; H</button>
          <button class="prop-btn" id="pFlipV">&#8597; V</button>
        </div>
      </div>`;
  }

  // Shadow for all
  const shadow = obj.shadow;
  html += `
    <div class="prop-section">
      <div class="prop-title">Sombra</div>
      <div class="prop-row">
        <input type="checkbox" id="pShadowOn" ${shadow ? 'checked' : ''}>
        <label for="pShadowOn" style="font-size:12px;color:var(--txt2)">Activar sombra</label>
      </div>
      ${shadow ? `
        <div class="prop-row">
          <span class="prop-label">Color</span>
          <input type="color" id="pShadowColor" class="prop-color" value="${shadow.color || '#000000'}">
          <span class="prop-label">X</span>
          <input class="prop-input" id="pShadowX" type="number" value="${shadow.offsetX || 4}" style="width:40px">
          <span class="prop-label">Y</span>
          <input class="prop-input" id="pShadowY" type="number" value="${shadow.offsetY || 4}" style="width:40px">
        </div>
        <div class="prop-row">
          <span class="prop-label">Blur</span>
          <input type="range" id="pShadowBlur" class="prop-range" min="0" max="50" value="${shadow.blur || 8}">
          <span class="prop-range-val" id="pShadowBlurV">${shadow.blur || 8}</span>
        </div>` : ''}
    </div>

    <div class="prop-section">
      <div class="prop-title">Capas</div>
      <div class="layer-btns">
        <button class="prop-btn" id="pFront">Al frente</button>
        <button class="prop-btn" id="pForward">Adelante</button>
        <button class="prop-btn" id="pBackward">Atras</button>
        <button class="prop-btn" id="pBack">Al fondo</button>
      </div>
      <div class="prop-row" style="margin-top:8px">
        <input type="checkbox" id="pLock" ${isLocked ? 'checked' : ''}>
        <label for="pLock" style="font-size:12px;color:var(--txt2)">&#128274; Bloquear elemento</label>
      </div>
    </div>`;

  panel.innerHTML = html;

  /* ---- Listeners ---- */
  function propInput(id, fn) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', fn);
  }
  function propClick(id, fn) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', fn);
  }
  function propChange(id, fn) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', fn);
  }

  propInput('pX', () => { obj.set('left', parseFloat(document.getElementById('pX').value) || 0); canvas.renderAll(); });
  propInput('pY', () => { obj.set('top', parseFloat(document.getElementById('pY').value) || 0); canvas.renderAll(); });
  propInput('pW', () => {
    const nw = parseFloat(document.getElementById('pW').value) || 1;
    const sx = nw / (obj.width || 1);
    obj.set('scaleX', sx); canvas.renderAll();
  });
  propInput('pH', () => {
    const nh = parseFloat(document.getElementById('pH').value) || 1;
    const sy = nh / (obj.height || 1);
    obj.set('scaleY', sy); canvas.renderAll();
  });
  propInput('pRot', () => { obj.set('angle', parseFloat(document.getElementById('pRot').value) || 0); canvas.renderAll(); });
  propInput('pOpacity', () => {
    const v = parseInt(document.getElementById('pOpacity').value);
    obj.set('opacity', v / 100); canvas.renderAll();
    document.getElementById('pOpacityV').textContent = v + '%';
  });

  if (type !== 'image' && type !== 'i-text' && type !== 'text') {
    propInput('pFill', () => { obj.set('fill', document.getElementById('pFill').value); canvas.renderAll(); });
    propClick('pFillNone', () => { obj.set('fill', 'transparent'); canvas.renderAll(); });
    propInput('pStroke', () => { obj.set('stroke', document.getElementById('pStroke').value); canvas.renderAll(); });
    propInput('pSW', () => { obj.set('strokeWidth', parseInt(document.getElementById('pSW').value) || 0); canvas.renderAll(); });
    if (type === 'rect') {
      propInput('pRadius', () => {
        const v = parseInt(document.getElementById('pRadius').value) || 0;
        obj.set({ rx: v, ry: v }); canvas.renderAll();
        document.getElementById('pRadiusV').textContent = v + 'px';
      });
    }
  }

  if (type === 'i-text' || type === 'text') {
    propChange('pFont', () => { obj.set('fontFamily', document.getElementById('pFont').value); canvas.renderAll(); });
    propInput('pFontSize', () => { obj.set('fontSize', parseInt(document.getElementById('pFontSize').value) || 24); canvas.renderAll(); });
    propInput('pTextColor', () => { obj.set('fill', document.getElementById('pTextColor').value); canvas.renderAll(); });
    propClick('pBold', () => {
      const bold = obj.fontWeight !== 'bold';
      obj.set('fontWeight', bold ? 'bold' : 'normal');
      document.getElementById('pBold').classList.toggle('active', bold);
      canvas.renderAll();
    });
    propClick('pItalic', () => {
      const italic = obj.fontStyle !== 'italic';
      obj.set('fontStyle', italic ? 'italic' : 'normal');
      document.getElementById('pItalic').classList.toggle('active', italic);
      canvas.renderAll();
    });
    propClick('pUnderline', () => {
      const v = !obj.underline;
      obj.set('underline', v);
      document.getElementById('pUnderline').classList.toggle('active', v);
      canvas.renderAll();
    });
    propClick('pStrikethrough', () => {
      const v = !obj.linethrough;
      obj.set('linethrough', v);
      document.getElementById('pStrikethrough').classList.toggle('active', v);
      canvas.renderAll();
    });
    ['L', 'C', 'R', 'J'].forEach(a => {
      const map = { L: 'left', C: 'center', R: 'right', J: 'justify' };
      propClick('pAlign' + a, () => {
        obj.set('textAlign', map[a]); canvas.renderAll();
        ['L','C','R','J'].forEach(x => document.getElementById('pAlign'+x)?.classList.toggle('active', x === a));
      });
    });
    propInput('pLetterSpacing', () => { obj.set('charSpacing', parseInt(document.getElementById('pLetterSpacing').value) || 0); canvas.renderAll(); });
    propInput('pLineHeight', () => { obj.set('lineHeight', parseFloat(document.getElementById('pLineHeight').value) || 1.16); canvas.renderAll(); });
  }

  if (type === 'image') {
    propClick('pFilterBtn', () => openFilterModal(obj));
    propClick('pRemoveBgBtn', () => removeBg(obj));
    propClick('pFlipH', () => { obj.set('flipX', !obj.flipX); canvas.renderAll(); saveHistory(); });
    propClick('pFlipV', () => { obj.set('flipY', !obj.flipY); canvas.renderAll(); saveHistory(); });
  }

  // Shadow
  propChange('pShadowOn', () => {
    if (document.getElementById('pShadowOn').checked) {
      obj.set('shadow', new fabric.Shadow({ color: '#00000060', offsetX: 4, offsetY: 4, blur: 8 }));
    } else {
      obj.set('shadow', null);
    }
    canvas.renderAll(); buildProps(obj, false);
  });
  propInput('pShadowColor', () => {
    if (obj.shadow) { obj.shadow.color = document.getElementById('pShadowColor').value; canvas.renderAll(); }
  });
  propInput('pShadowX', () => { if (obj.shadow) { obj.shadow.offsetX = parseInt(document.getElementById('pShadowX').value) || 0; canvas.renderAll(); } });
  propInput('pShadowY', () => { if (obj.shadow) { obj.shadow.offsetY = parseInt(document.getElementById('pShadowY').value) || 0; canvas.renderAll(); } });
  propInput('pShadowBlur', () => {
    if (obj.shadow) {
      const v = parseInt(document.getElementById('pShadowBlur').value) || 0;
      obj.shadow.blur = v; canvas.renderAll();
      document.getElementById('pShadowBlurV').textContent = v;
    }
  });

  // Layers
  propClick('pFront',   () => { canvas.bringToFront(obj);    canvas.renderAll(); saveHistory(); });
  propClick('pForward', () => { canvas.bringForward(obj);    canvas.renderAll(); saveHistory(); });
  propClick('pBackward',() => { canvas.sendBackwards(obj);   canvas.renderAll(); saveHistory(); });
  propClick('pBack',    () => { canvas.sendToBack(obj);      canvas.renderAll(); saveHistory(); });
  propChange('pLock',   () => {
    const lock = document.getElementById('pLock').checked;
    obj.set({ lockMovementX: lock, lockMovementY: lock, lockScalingX: lock, lockScalingY: lock, lockRotation: lock, hasControls: !lock });
    canvas.renderAll();
  });
}

/* ------------------------------------------------------------------ */
/* ALIGN BAR                                                            */
/* ------------------------------------------------------------------ */
document.querySelectorAll('#alignBar [data-align]').forEach(btn => {
  btn.addEventListener('click', () => {
    const objs = canvas.getActiveObjects();
    if (!objs.length) return;
    const cw = S.canvasW, ch = S.canvasH;
    objs.forEach(o => {
      const ow = o.getScaledWidth(), oh = o.getScaledHeight();
      switch (btn.dataset.align) {
        case 'left':    o.set('left', 0); break;
        case 'centerH': o.set('left', (cw - ow) / 2); break;
        case 'right':   o.set('left', cw - ow); break;
        case 'top':     o.set('top', 0); break;
        case 'centerV': o.set('top', (ch - oh) / 2); break;
        case 'bottom':  o.set('top', ch - oh); break;
      }
      o.setCoords();
    });
    canvas.renderAll(); saveHistory();
  });
});

document.getElementById('flipHBtn').addEventListener('click', () => {
  canvas.getActiveObjects().forEach(o => { o.set('flipX', !o.flipX); });
  canvas.renderAll(); saveHistory();
});
document.getElementById('flipVBtn').addEventListener('click', () => {
  canvas.getActiveObjects().forEach(o => { o.set('flipY', !o.flipY); });
  canvas.renderAll(); saveHistory();
});
document.getElementById('groupBtn').addEventListener('click', () => {
  const sel = canvas.getActiveObjects();
  if (sel.length < 2) return;
  canvas.discardActiveObject();
  const group = new fabric.Group(sel);
  sel.forEach(o => canvas.remove(o));
  canvas.add(group);
  canvas.setActiveObject(group);
  canvas.renderAll(); saveHistory();
});
document.getElementById('ungroupBtn').addEventListener('click', () => {
  const obj = canvas.getActiveObject();
  if (!obj || obj.type !== 'group') return;
  obj.toActiveSelection();
  canvas.renderAll(); saveHistory();
});
document.getElementById('lockBtn').addEventListener('click', () => {
  canvas.getActiveObjects().forEach(o => {
    const l = !o.lockMovementX;
    o.set({ lockMovementX: l, lockMovementY: l, lockScalingX: l, lockScalingY: l, lockRotation: l, hasControls: !l });
  });
  canvas.renderAll();
});
document.getElementById('deleteBtn').addEventListener('click', () => {
  canvas.getActiveObjects().forEach(o => canvas.remove(o));
  canvas.discardActiveObject();
  canvas.renderAll(); saveHistory();
});

/* ------------------------------------------------------------------ */
/* COPY / PASTE / DUPLICATE                                            */
/* ------------------------------------------------------------------ */
function copySelection() {
  const obj = canvas.getActiveObject();
  if (!obj) return;
  obj.clone(cloned => { S.clipboard = cloned; S.clipboard._top = obj.top; S.clipboard._left = obj.left; });
}
function pasteSelection() {
  if (!S.clipboard) return;
  S.clipboard.clone(cloned => {
    cloned.set({ left: (S.clipboard._left || 0) + 20, top: (S.clipboard._top || 0) + 20 });
    if (cloned.type === 'activeSelection') {
      cloned.canvas = canvas;
      cloned.forEachObject(o => canvas.add(o));
      cloned.setCoords();
    } else {
      canvas.add(cloned);
    }
    canvas.setActiveObject(cloned);
    S.clipboard._left += 20; S.clipboard._top += 20;
    canvas.renderAll(); saveHistory();
  });
}

/* ------------------------------------------------------------------ */
/* BACKGROUND                                                           */
/* ------------------------------------------------------------------ */
document.getElementById('applyBgSolid').addEventListener('click', () => {
  const color = document.getElementById('bgSolidColor').value;
  canvas.setBackgroundColor(color, canvas.renderAll.bind(canvas));
  saveHistory();
});

document.getElementById('applyBgGrad').addEventListener('click', () => {
  const c1 = document.getElementById('gradC1').value;
  const c2 = document.getElementById('gradC2').value;
  const dir = document.getElementById('gradDir').value;
  const w = S.canvasW, h = S.canvasH;
  let coords;
  if (dir === 'horizontal') coords = { x1: 0, y1: 0, x2: w, y2: 0 };
  else if (dir === 'vertical') coords = { x1: 0, y1: 0, x2: 0, y2: h };
  else coords = { x1: 0, y1: 0, x2: w, y2: h };
  const gradient = new fabric.Gradient({
    type: 'linear', gradientUnits: 'pixels', coords,
    colorStops: [{ offset: 0, color: c1 }, { offset: 1, color: c2 }],
  });
  canvas.setBackgroundColor(gradient, canvas.renderAll.bind(canvas));
  saveHistory();
});

// Gradient presets
const GRAD_PRESETS = [
  ['#667eea', '#764ba2'], ['#f093fb', '#f5576c'], ['#4facfe', '#00f2fe'],
  ['#43e97b', '#38f9d7'], ['#fa709a', '#fee140'], ['#a18cd1', '#fbc2eb'],
  ['#ffecd2', '#fcb69f'], ['#ff9a9e', '#fecfef'],
  ['#1a1a2e', '#16213e'], ['#0f3460', '#533483'],
  ['#f7971e', '#ffd200'], ['#ee0979', '#ff6a00'],
  ['#11998e', '#38ef7d'], ['#c0392b', '#8e44ad'],
  ['#4568dc', '#b06ab3'], ['#2c3e50', '#4ca1af'],
];

function renderGradPresets() {
  const c = document.getElementById('gradPresets');
  c.innerHTML = GRAD_PRESETS.map((g, i) =>
    `<div class="grad-swatch" style="background:linear-gradient(135deg,${g[0]},${g[1]})" data-i="${i}" title="${g[0]} → ${g[1]}"></div>`
  ).join('');
  c.querySelectorAll('.grad-swatch').forEach(el => {
    el.addEventListener('click', () => {
      const [c1, c2] = GRAD_PRESETS[el.dataset.i];
      document.getElementById('gradC1').value = c1;
      document.getElementById('gradC2').value = c2;
    });
  });
}

// Quick background colors
const QUICK_BG_COLORS = [
  '#ffffff','#f8f9fa','#e9ecef','#dee2e6','#adb5bd','#6c757d','#343a40','#212529',
  '#0c0c14','#1a1a2e','#16213e','#0f3460','#1e1b4b','#2d1b69',
  '#fff8f0','#fdf2e9','#f5e6d3','#e8d5b7','#d4a574','#8b4513',
  '#f0fdf4','#dcfce7','#86efac','#22c55e','#166534','#052e16',
  '#eff6ff','#dbeafe','#93c5fd','#3b82f6','#1e40af','#172554',
  '#fef2f2','#fecaca','#f87171','#ef4444','#991b1b','#450a0a',
  '#fffbeb','#fef3c7','#fcd34d','#f59e0b','#92400e','#451a03',
  '#fdf4ff','#f5d0fe','#d946ef','#a855f7','#6b21a8','#3b0764',
];

function renderQuickBgColors() {
  const c = document.getElementById('quickBgColors');
  if (!c) return;
  c.innerHTML = QUICK_BG_COLORS.map(col =>
    `<div class="qc-swatch" style="background:${col}" data-color="${col}" title="${col}"></div>`
  ).join('');
  c.querySelectorAll('.qc-swatch').forEach(el => {
    el.addEventListener('click', () => {
      canvas.setBackgroundColor(el.dataset.color, canvas.renderAll.bind(canvas));
      document.getElementById('bgSolidColor').value = el.dataset.color;
      saveHistory();
    });
  });
}

// Pattern backgrounds
const PATTERNS = [
  { label: '⬝ Puntos', id: 'dots' },
  { label: '━ Rayas H', id: 'stripesH' },
  { label: '┃ Rayas V', id: 'stripesV' },
  { label: '▦ Cuadros', id: 'squares' },
  { label: '╱ Diag', id: 'diag' },
  { label: '▩ Cruce', id: 'cross' },
];

function createPatternCanvas(id, fg = '#333', bg = '#fff') {
  const pc = document.createElement('canvas');
  pc.width = 20; pc.height = 20;
  const ctx = pc.getContext('2d');
  ctx.fillStyle = bg; ctx.fillRect(0, 0, 20, 20);
  ctx.strokeStyle = fg; ctx.fillStyle = fg; ctx.lineWidth = 1;
  switch (id) {
    case 'dots':    ctx.beginPath(); ctx.arc(10,10,2,0,Math.PI*2); ctx.fill(); break;
    case 'stripesH': ctx.beginPath(); ctx.moveTo(0,10); ctx.lineTo(20,10); ctx.stroke(); break;
    case 'stripesV': ctx.beginPath(); ctx.moveTo(10,0); ctx.lineTo(10,20); ctx.stroke(); break;
    case 'squares': ctx.strokeRect(2,2,16,16); break;
    case 'diag':   ctx.beginPath(); ctx.moveTo(0,20); ctx.lineTo(20,0); ctx.stroke(); break;
    case 'cross':  ctx.beginPath(); ctx.moveTo(10,0); ctx.lineTo(10,20); ctx.moveTo(0,10); ctx.lineTo(20,10); ctx.stroke(); break;
  }
  return pc;
}

function renderPatternBtns() {
  const c = document.getElementById('patternBtns');
  c.innerHTML = PATTERNS.map(p => `<button class="pattern-btn" data-id="${p.id}">${p.label}</button>`).join('');
  c.querySelectorAll('.pattern-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const pc = createPatternCanvas(btn.dataset.id, '#aaa', '#fff');
      const pattern = new fabric.Pattern({ source: pc, repeat: 'repeat' });
      canvas.setBackgroundColor(pattern, canvas.renderAll.bind(canvas));
      saveHistory();
    });
  });
}

// Background image upload
document.getElementById('uploadBgBtn').addEventListener('click', () => document.getElementById('bgFileInput').click());
document.getElementById('bgFileInput').addEventListener('change', (e) => {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    fabric.Image.fromURL(ev.target.result, (img) => {
      img.scaleToWidth(S.canvasW);
      img.scaleToHeight(S.canvasH);
      canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
      saveHistory();
    });
  };
  reader.readAsDataURL(file);
  e.target.value = '';
});

/* ------------------------------------------------------------------ */
/* IMAGE UPLOAD                                                         */
/* ------------------------------------------------------------------ */
document.getElementById('uploadImageBtn').addEventListener('click', () => document.getElementById('imageFileInput').click());
document.getElementById('imageFileInput').addEventListener('change', (e) => {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    fabric.Image.fromURL(ev.target.result, (img) => {
      const maxSz = Math.min(S.canvasW * 0.6, S.canvasH * 0.6, 400);
      if (img.width > maxSz || img.height > maxSz) img.scaleToWidth(Math.min(img.width, maxSz));
      img.set({ left: (S.canvasW - img.getScaledWidth()) / 2, top: (S.canvasH - img.getScaledHeight()) / 2 });
      canvas.add(img);
      canvas.setActiveObject(img);
      canvas.renderAll(); saveHistory();
    });
  };
  reader.readAsDataURL(file);
  e.target.value = '';
});

/* ------------------------------------------------------------------ */
/* ICON LIBRARY                                                         */
/* ------------------------------------------------------------------ */
async function loadCatalog() {
  try {
    const res = await fetch('/static/assets/icons/catalog.json');
    S.catalog = await res.json();
    renderCategoryBtns();
    renderIcons(S.iconCategory);
  } catch (e) { console.error('Error cargando catalogo:', e); }
}

function renderCategoryBtns() {
  if (!S.catalog) return;
  const c = document.getElementById('iconCategoryBtns');
  c.innerHTML = S.catalog.categories.map(cat =>
    `<button class="cat-btn ${cat.id === S.iconCategory ? 'active' : ''}" data-id="${cat.id}">${cat.name}</button>`
  ).join('');
  c.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      S.iconCategory = btn.dataset.id;
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.toggle('active', b.dataset.id === S.iconCategory));
      renderIcons(S.iconCategory);
    });
  });
}

function renderIcons(categoryId, filter = '') {
  if (!S.catalog) return;
  const cat = S.catalog.categories.find(c => c.id === categoryId);
  const icons = cat ? cat.icons.filter(ic => !filter || ic.name.toLowerCase().includes(filter.toLowerCase())) : [];
  const grid = document.getElementById('iconGrid');
  const color = document.getElementById('iconColorPicker').value;

  grid.innerHTML = icons.map(ic => {
    const paths = ic.paths.map(p => {
      if (ic.stroke) return `<path d="${p}" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`;
      return `<path d="${p}" fill="${color}"/>`;
    }).join('');
    return `<div class="icon-item" data-id="${ic.id}" data-cat="${categoryId}" title="${ic.name}">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">${paths}</svg>
    </div>`;
  }).join('');

  grid.querySelectorAll('.icon-item').forEach(el => {
    el.addEventListener('click', () => {
      const icon = icons.find(ic => ic.id === el.dataset.id);
      if (icon) addIconToCanvas(icon);
    });
  });
}

function addIconToCanvas(icon) {
  const color = document.getElementById('iconColorPicker').value;
  const paths = icon.paths.map(p => {
    if (icon.stroke) return `<path d="${p}" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`;
    return `<path d="${p}" fill="${color}"/>`;
  }).join('');
  const svgStr = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="120" height="120">${paths}</svg>`;
  fabric.loadSVGFromString(svgStr, (objects, options) => {
    const obj = fabric.util.groupSVGElements(objects, options);
    obj.scaleToWidth(120);
    obj.set({ left: (S.canvasW - obj.getScaledWidth()) / 2, top: (S.canvasH - obj.getScaledHeight()) / 2 });
    canvas.add(obj);
    canvas.setActiveObject(obj);
    canvas.renderAll(); saveHistory();
  });
}

document.getElementById('iconColorPicker').addEventListener('input', () => renderIcons(S.iconCategory, document.getElementById('iconSearchInput').value));
document.getElementById('iconSearchInput').addEventListener('input', (e) => {
  const q = e.target.value;
  if (q) {
    // Search all categories
    if (!S.catalog) return;
    const grid = document.getElementById('iconGrid');
    const color = document.getElementById('iconColorPicker').value;
    const allIcons = S.catalog.categories.flatMap(c => c.icons.map(ic => ({ ...ic, isStroke: ic.stroke, catId: c.id })));
    const filtered = allIcons.filter(ic => ic.name.toLowerCase().includes(q.toLowerCase()));
    grid.innerHTML = filtered.map(ic => {
      const paths = ic.paths.map(p => ic.stroke
        ? `<path d="${p}" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`
        : `<path d="${p}" fill="${color}"/>`).join('');
      return `<div class="icon-item" data-id="${ic.id}" data-cat="${ic.catId}" title="${ic.name}">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">${paths}</svg>
      </div>`;
    }).join('');
    grid.querySelectorAll('.icon-item').forEach(el => {
      el.addEventListener('click', () => {
        const icon = allIcons.find(ic => ic.id === el.dataset.id && ic.catId === el.dataset.cat);
        if (icon) addIconToCanvas(icon);
      });
    });
  } else {
    renderIcons(S.iconCategory);
  }
});

/* ------------------------------------------------------------------ */
/* QR CODE                                                              */
/* ------------------------------------------------------------------ */
document.getElementById('qrBtn').addEventListener('click', () => openModal('qrModal'));
document.getElementById('generateQrBtn').addEventListener('click', async () => {
  const text = document.getElementById('qrText').value.trim();
  if (!text) return alert('Ingresa texto o URL para el QR');
  const size = parseInt(document.getElementById('qrSize').value) || 300;
  const color = document.getElementById('qrFgColor').value;
  const bgColor = document.getElementById('qrBgColor').value;
  try {
    const res = await fetch('/api/qr', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, size, color, bg_color: bgColor }),
    });
    const data = await res.json();
    if (data.error) return alert('Error: ' + data.error);
    const url = `data:${data.mime};base64,${data.image}`;
    fabric.Image.fromURL(url, (img) => {
      img.set({ left: (S.canvasW - img.width) / 2, top: (S.canvasH - img.height) / 2 });
      canvas.add(img); canvas.setActiveObject(img); canvas.renderAll(); saveHistory();
    });
    closeModal('qrModal');
  } catch (e) { alert('Error generando QR: ' + e.message); }
});

/* ------------------------------------------------------------------ */
/* IMAGE FILTERS MODAL                                                  */
/* ------------------------------------------------------------------ */
function openFilterModal(obj) {
  S.filterTarget = obj;
  openModal('filterModal');
}

['Bright', 'Contrast', 'Sat', 'Sharp', 'Blur'].forEach(id => {
  const el = document.getElementById('f' + id);
  const vEl = document.getElementById(id.toLowerCase() + 'Val') || document.getElementById(id + 'Val');
  if (el) el.addEventListener('input', () => {
    if (vEl) vEl.textContent = el.value;
  });
});

document.querySelectorAll('#filterModal [data-preset]').forEach(btn => {
  btn.addEventListener('click', () => {
    const p = btn.dataset.preset;
    const presets = {
      normal:   { bright: 100, contrast: 100, sat: 100, sharp: 100, blur: 0 },
      grayscale:{ bright: 100, contrast: 100, sat: 0,   sharp: 100, blur: 0 },
      sepia:    { bright: 110, contrast: 90,  sat: 50,  sharp: 100, blur: 0 },
      vivid:    { bright: 110, contrast: 130, sat: 160, sharp: 120, blur: 0 },
      matte:    { bright: 95,  contrast: 85,  sat: 80,  sharp: 80,  blur: 0 },
      cold:     { bright: 100, contrast: 105, sat: 110, sharp: 100, blur: 0 },
      warm:     { bright: 105, contrast: 100, sat: 130, sharp: 100, blur: 0 },
      faded:    { bright: 120, contrast: 75,  sat: 70,  sharp: 80,  blur: 0 },
    };
    const v = presets[p]; if (!v) return;
    document.getElementById('fBright').value = v.bright;
    document.getElementById('fContrast').value = v.contrast;
    document.getElementById('fSat').value = v.sat;
    document.getElementById('fSharp').value = v.sharp;
    document.getElementById('fBlur').value = v.blur;
    document.getElementById('brightVal').textContent = v.bright;
    document.getElementById('contrastVal').textContent = v.contrast;
    document.getElementById('satVal').textContent = v.sat;
    document.getElementById('sharpVal').textContent = v.sharp;
    document.getElementById('blurVal').textContent = v.blur;
  });
});

document.getElementById('applyFilterBtn').addEventListener('click', async () => {
  const obj = S.filterTarget;
  if (!obj || obj.type !== 'image') return;

  const filters = {
    brightness: parseInt(document.getElementById('fBright').value) / 100,
    contrast:   parseInt(document.getElementById('fContrast').value) / 100,
    saturation: parseInt(document.getElementById('fSat').value) / 100,
    sharpness:  parseInt(document.getElementById('fSharp').value) / 100,
    blur:       parseInt(document.getElementById('fBlur').value),
    grayscale:  parseInt(document.getElementById('fSat').value) === 0,
  };

  // Get image data URL from the fabric object
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = obj.width; tempCanvas.height = obj.height;
  const ctx = tempCanvas.getContext('2d');
  ctx.drawImage(obj.getElement(), 0, 0);
  const dataURL = tempCanvas.toDataURL('image/png');

  try {
    const res = await fetch('/api/filter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: dataURL, filters }),
    });
    const data = await res.json();
    if (data.error) return alert('Error: ' + data.error);
    const url = `data:${data.mime};base64,${data.image}`;
    const prevLeft = obj.left, prevTop = obj.top, prevSX = obj.scaleX, prevSY = obj.scaleY;
    canvas.remove(obj);
    fabric.Image.fromURL(url, (newImg) => {
      newImg.set({ left: prevLeft, top: prevTop, scaleX: prevSX, scaleY: prevSY });
      canvas.add(newImg); canvas.setActiveObject(newImg); canvas.renderAll(); saveHistory();
    });
    closeModal('filterModal');
  } catch (e) { alert('Error aplicando filtro: ' + e.message); }
});

/* ------------------------------------------------------------------ */
/* BACKGROUND REMOVAL                                                   */
/* ------------------------------------------------------------------ */
async function removeBg(obj) {
  if (!obj || obj.type !== 'image') return;
  const confirm = window.confirm('Esto requiere rembg instalado. ¿Continuar?');
  if (!confirm) return;

  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = obj.width; tempCanvas.height = obj.height;
  const ctx = tempCanvas.getContext('2d');
  ctx.drawImage(obj.getElement(), 0, 0);

  tempCanvas.toBlob(async (blob) => {
    const fd = new FormData();
    fd.append('image', blob, 'img.png');
    try {
      const res = await fetch('/api/remove-bg', { method: 'POST', body: fd });
      const data = await res.json();
      if (data.error) return alert('Error: ' + data.error);
      const url = `data:${data.mime};base64,${data.image}`;
      const prevLeft = obj.left, prevTop = obj.top, prevSX = obj.scaleX, prevSY = obj.scaleY;
      canvas.remove(obj);
      fabric.Image.fromURL(url, (newImg) => {
        newImg.set({ left: prevLeft, top: prevTop, scaleX: prevSX, scaleY: prevSY });
        canvas.add(newImg); canvas.setActiveObject(newImg); canvas.renderAll(); saveHistory();
      });
    } catch (e) { alert('Error: ' + e.message); }
  }, 'image/png');
}

/* ------------------------------------------------------------------ */
/* EXPORT                                                               */
/* ------------------------------------------------------------------ */
document.getElementById('downloadBtn').addEventListener('click', downloadDesign);
document.getElementById('exportQuality').addEventListener('input', function() {
  document.getElementById('qualityLabel').textContent = this.value;
});

function downloadDesign() {
  const fmt = document.getElementById('exportFormat').value;
  const quality = parseInt(document.getElementById('exportQuality').value) / 100;
  const scale = parseFloat(document.getElementById('exportScale').value) || 2;
  const multiplier = scale / S.zoom;
  const name = document.getElementById('designName').value || 'diseno';

  const mime = fmt === 'png' ? 'image/png' : fmt === 'jpg' ? 'image/jpeg' : 'image/webp';

  const wasSel = canvas.getActiveObject();
  canvas.discardActiveObject();
  canvas.renderAll();

  const dataURL = canvas.toDataURL({
    format: fmt,
    quality: quality,
    multiplier: multiplier,
    enableRetinaScaling: false,
  });

  if (wasSel) { canvas.setActiveObject(wasSel); canvas.renderAll(); }

  const a = document.createElement('a');
  a.href = dataURL;
  a.download = `${name}.${fmt}`;
  a.click();
}

/* ------------------------------------------------------------------ */
/* SAVE / LOAD PROJECT                                                  */
/* ------------------------------------------------------------------ */
document.getElementById('saveProjectBtn').addEventListener('click', () => {
  const project = {
    version: '1.0',
    name: document.getElementById('designName').value,
    canvasW: S.canvasW, canvasH: S.canvasH,
    fabric: canvas.toJSON(['selectable', 'evented', 'lockMovementX', 'lockMovementY']),
    bg: typeof canvas.backgroundColor === 'string' ? canvas.backgroundColor : '#ffffff',
  };
  const blob = new Blob([JSON.stringify(project, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (project.name || 'diseno') + '.gccanva.json';
  a.click();
});

document.getElementById('loadProjectBtn').addEventListener('click', () => document.getElementById('projectFileInput').click());
document.getElementById('projectFileInput').addEventListener('change', (e) => {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const project = JSON.parse(ev.target.result);
      if (project.name) document.getElementById('designName').value = project.name;
      resizeCanvas(project.canvasW || 800, project.canvasH || 600);
      canvas.loadFromJSON(project.fabric, () => {
        if (project.bg) canvas.setBackgroundColor(project.bg, () => {});
        canvas.renderAll(); saveHistory();
      });
    } catch (err) { alert('Error cargando proyecto: ' + err.message); }
  };
  reader.readAsText(file);
  e.target.value = '';
});

/* ------------------------------------------------------------------ */
/* CANVAS SIZE & MAGIC RESIZE                                          */
/* ------------------------------------------------------------------ */
async function loadPresets() {
  try {
    const res = await fetch('/api/presets');
    const presets = await res.json();
    const sel = document.getElementById('canvasPresetSelect');
    // Group by category
    const cats = {};
    presets.forEach(p => {
      const c = p.cat || 'Otros';
      if (!cats[c]) cats[c] = [];
      cats[c].push(p);
    });
    sel.innerHTML = '<option value="">Seleccionar preset...</option>';
    Object.entries(cats).forEach(([cat, items]) => {
      if (cat) {
        const og = document.createElement('optgroup'); og.label = cat;
        items.forEach(p => {
          const o = document.createElement('option');
          o.value = `${p.w}x${p.h}`;
          o.textContent = `${p.name} (${p.w}x${p.h})`;
          og.appendChild(o);
        });
        sel.appendChild(og);
      }
    });
    sel.addEventListener('change', () => {
      const v = sel.value;
      if (!v) return;
      const [w, h] = v.split('x').map(Number);
      document.getElementById('cwInput').value = w;
      document.getElementById('chInput').value = h;
      resizeCanvas(w, h);
    });

    // Magic Resize modal list
    const list = document.getElementById('magicResizeList');
    list.innerHTML = presets.filter(p => p.name !== 'Personalizado').map(p =>
      `<div class="mr-item" data-w="${p.w}" data-h="${p.h}">
        <div class="mr-cat">${p.cat || ''}</div>
        <div class="mr-name">${p.name}</div>
        <div class="mr-size">${p.w} × ${p.h}</div>
      </div>`).join('');
    list.querySelectorAll('.mr-item').forEach(el => {
      el.addEventListener('click', () => {
        magicResize(parseInt(el.dataset.w), parseInt(el.dataset.h));
        closeModal('magicResizeModal');
      });
    });
  } catch (e) { console.error('Error cargando presets:', e); }
}

function resizeCanvas(w, h) {
  const oldW = S.canvasW, oldH = S.canvasH;
  S.canvasW = w; S.canvasH = h;
  canvas.setWidth(w * S.zoom); canvas.setHeight(h * S.zoom);
  canvas.setDimensions({ width: w, height: h }, { backstoreOnly: true });
  canvas.renderAll();
  fitCanvas();
}

function magicResize(newW, newH) {
  const scaleX = newW / S.canvasW, scaleY = newH / S.canvasH;
  canvas.forEachObject(o => {
    o.set({
      left: (o.left || 0) * scaleX,
      top:  (o.top  || 0) * scaleY,
      scaleX: (o.scaleX || 1) * scaleX,
      scaleY: (o.scaleY || 1) * scaleY,
    });
    o.setCoords();
  });
  // Scale text size
  canvas.forEachObject(o => {
    if (o.type === 'i-text' || o.type === 'text') {
      o.set('fontSize', Math.round((o.fontSize || 24) * Math.min(scaleX, scaleY)));
    }
  });
  resizeCanvas(newW, newH);
  canvas.renderAll(); saveHistory();
}

document.getElementById('applySizeBtn').addEventListener('click', () => {
  const w = parseInt(document.getElementById('cwInput').value) || S.canvasW;
  const h = parseInt(document.getElementById('chInput').value) || S.canvasH;
  if (w > 0 && h > 0) resizeCanvas(w, h);
});

document.getElementById('magicResizeBtn').addEventListener('click', () => openModal('magicResizeModal'));
document.getElementById('mrCustomBtn').addEventListener('click', () => {
  const w = parseInt(document.getElementById('mrCustomW').value);
  const h = parseInt(document.getElementById('mrCustomH').value);
  if (w > 0 && h > 0) { magicResize(w, h); closeModal('magicResizeModal'); }
});

/* ------------------------------------------------------------------ */
/* CLAUDE / AI MODE                                                     */
/* ------------------------------------------------------------------ */
// ─── Font Loader ────────────────────────────────────────────
async function loadProjectFonts() {
  try {
    const res = await fetch('/api/fonts');
    const fonts = await res.json();
    // Update font selector options (built into buildProps dynamically)
    S.availableFonts = fonts.map(f => f.name);
    console.log(`Fuentes cargadas: ${fonts.length}`);
  } catch(e) { S.availableFonts = []; }
}

// Full font list for selectors
function getFontOptions(currentFont) {
  const allFonts = [
    'Arial','Arial Black','Bahnschrift','Calibri','Cambria','Candara',
    'Comic Sans MS','Consolas','Cooper Black','Corbel','Courier New',
    'Franklin Gothic','Gabriola','Georgia','Impact','Moon Bold','Moon Light',
    'Mukta','Narnia','Optimus Princeps','Rakoon',
    'Roboto Slab','Rockwell','Segoe UI','Tahoma',
    'Times New Roman','Trebuchet MS','Verdana',
  ];
  return allFonts.map(f => `<option ${currentFont === f ? 'selected' : ''}>${f}</option>`).join('');
}

// ─── Quick Templates ─────────────────────────────────────────
const QUICK_TEMPLATES = [
  // Social / General
  { name: 'Social Elegante', spec: {
    width:1080,height:1080,background:'#1a1a2e',format:'webp',quality:92,
    elements:[
      {type:'gradient',x:0,y:0,w:1080,h:1080,color1:'#16213e',color2:'#0f3460',direction:'diagonal'},
      {type:'rect',x:60,y:60,w:960,h:960,color:'#e94560',opacity:0.06,radius:30},
      {type:'text',text:'Tu Marca',x:540,y:440,size:96,color:'#ffffff',align:'center',bold:true,shadow:true,font:'Mukta'},
      {type:'text',text:'Subtitulo aquí',x:540,y:570,size:36,color:'#9898c0',align:'center'},
    ]}},

  // YouTube
  { name: 'YouTube Thumb', spec: {
    width:1280,height:720,background:'#0f0f0f',format:'webp',quality:92,
    elements:[
      {type:'gradient',x:0,y:0,w:1280,h:720,color1:'#1a1a2e',color2:'#0f0f0f',direction:'horizontal'},
      {type:'rect',x:0,y:0,w:8,h:720,color:'#ff0000'},
      {type:'text',text:'TÍTULO DEL VIDEO',x:50,y:240,size:100,color:'#ffffff',bold:true,shadow:true,font:'Impact'},
      {type:'text',text:'Subtítulo descriptivo aquí',x:50,y:390,size:42,color:'#ff6666',font:'Mukta'},
    ]}},

  // Blog / OG - Inforket / Digital Marketing
  { name: 'Blog Inforket', spec: {
    width:1200,height:630,background:'#0a0a14',format:'webp',quality:92,
    filename:'blog-inforket',
    elements:[
      {type:'gradient',x:0,y:0,w:1200,h:630,color1:'#0d0d20',color2:'#1a0a2e',direction:'diagonal'},
      {type:'rect',x:0,y:0,w:1200,h:5,color:'#6366f1'},
      {type:'rect',x:0,y:625,w:1200,h:5,color:'#6366f1'},
      {type:'text',text:'MARKETING DIGITAL',x:60,y:80,size:18,color:'#6366f1',font:'Consolas',bold:true},
      {type:'text',text:'Titulo del\nArticulo',x:60,y:140,size:90,color:'#ffffff',bold:true,font:'Mukta',shadow:true,shadow_color:'#6366f160',shadow_x:3,shadow_y:3,shadow_blur:8},
      {type:'text',text:'inforket.com',x:60,y:530,size:22,color:'#5a5a80',font:'Segoe UI'},
    ]}},

  // Blog - Gabriel Caroprese Personal Brand
  { name: 'Blog Gabriel', spec: {
    width:1200,height:630,background:'#ffffff',format:'webp',quality:92,
    filename:'blog-gabriel',
    elements:[
      {type:'rect',x:0,y:0,w:420,h:630,color:'#1e1e2e'},
      {type:'rect',x:420,y:0,w:6,h:630,color:'#f59e0b'},
      {type:'gradient',x:0,y:0,w:420,h:630,color1:'#1e1e2e',color2:'#0f0f1a',direction:'vertical'},
      {type:'text',text:'Gabriel\nCaroprese',x:40,y:180,size:52,color:'#ffffff',bold:true,font:'Roboto Slab'},
      {type:'text',text:'gabrielcaroprese.com',x:40,y:420,size:18,color:'#f59e0b',font:'Segoe UI'},
      {type:'text',text:'Titulo del Post',x:460,y:200,size:62,color:'#1e1e2e',bold:true,font:'Roboto Slab'},
      {type:'text',text:'Subtitulo o descripcion breve',x:460,y:310,size:28,color:'#6b7280',font:'Segoe UI'},
    ]}},

  // Hatton Naturals - Natural / Health Products
  { name: 'Hatton Naturals', spec: {
    width:1080,height:1080,background:'#f5f0e8',format:'webp',quality:92,
    filename:'hatton-naturals',
    elements:[
      {type:'gradient',x:0,y:0,w:1080,h:1080,color1:'#fdf8f0',color2:'#e8dcc8',direction:'diagonal'},
      {type:'ellipse',x:140,y:140,w:800,h:800,color:'#8fbc8f',opacity:0.12},
      {type:'rect',x:80,y:80,w:920,h:920,color:'#5d8a5e',opacity:0.06,radius:40},
      {type:'text',text:'HATTON\nNATURALS',x:540,y:200,size:80,color:'#2d5a2e',align:'center',bold:true,font:'Optimus Princeps',shadow:true,shadow_color:'#2d5a2e30',shadow_blur:10},
      {type:'text',text:'Puro · Natural · Auténtico',x:540,y:420,size:32,color:'#5d8a5e',align:'center',font:'Gabriola'},
      {type:'rect',x:340,y:500,w:400,h:2,color:'#8fbc8f'},
      {type:'text',text:'Nombre del Producto',x:540,y:550,size:44,color:'#3d6b3e',align:'center',bold:true,font:'Roboto Slab'},
      {type:'text',text:'hattonnaturals.com',x:540,y:800,size:22,color:'#8a9e6a',align:'center',font:'Segoe UI'},
    ]}},

  // Pawsitive Brews - Café para perros / Pet products
  { name: 'Pawsitive Brews', spec: {
    width:1080,height:1080,background:'#2c1810',format:'webp',quality:92,
    filename:'pawsitive-brews',
    elements:[
      {type:'gradient',x:0,y:0,w:1080,h:1080,color1:'#3d2314',color2:'#1a0a08',direction:'vertical'},
      {type:'ellipse',x:190,y:190,w:700,h:700,color:'#8b4513',opacity:0.2},
      {type:'text',text:'PAWSITIVE',x:540,y:250,size:88,color:'#d4a574',align:'center',bold:true,font:'Cooper Black',shadow:true,shadow_color:'#00000080',shadow_blur:12},
      {type:'text',text:'BREWS',x:540,y:370,size:88,color:'#ff9a3c',align:'center',bold:true,font:'Cooper Black'},
      {type:'text',text:'☕ 🐾',x:540,y:520,size:64,align:'center'},
      {type:'rect',x:240,y:640,w:600,h:2,color:'#8b4513'},
      {type:'text',text:'Café Artesanal para Amantes\nde los Perros',x:540,y:680,size:30,color:'#c8956c',align:'center',font:'Rockwell'},
      {type:'text',text:'pawsitivebrews.com',x:540,y:900,size:20,color:'#8b6040',align:'center',font:'Segoe UI'},
    ]}},

  // Etsy Product - T-Shirt / Dog merch
  { name: 'Etsy Perros', spec: {
    width:2000,height:2000,background:'#fafafa',format:'webp',quality:92,
    filename:'etsy-perros',
    elements:[
      {type:'gradient',x:0,y:0,w:2000,h:2000,color1:'#fff9f0',color2:'#f5ece0',direction:'diagonal'},
      {type:'ellipse',x:400,y:400,w:1200,h:1200,color:'#d4956a',opacity:0.08},
      {type:'text',text:'DOG',x:1000,y:500,size:260,color:'#3d2314',align:'center',bold:true,font:'Impact',shadow:true,shadow_color:'#d4956a60',shadow_blur:20},
      {type:'text',text:'MOM',x:1000,y:780,size:260,color:'#8b4513',align:'center',bold:true,font:'Impact'},
      {type:'star',x:1000,y:1100,r:40,inner_r:16,points:5,color:'#d4956a'},
      {type:'text',text:'Proudly Obsessed',x:1000,y:1200,size:60,color:'#6b4423',align:'center',font:'Gabriola'},
      {type:'text',text:'Est. Always',x:1000,y:1310,size:40,color:'#a06030',align:'center',font:'Bahnschrift'},
    ]}},

  // Etsy - Remera / Apparel listing
  { name: 'Etsy Remera', spec: {
    width:2000,height:2000,background:'#1a1a1a',format:'webp',quality:92,
    filename:'etsy-remera',
    elements:[
      {type:'gradient',x:0,y:0,w:2000,h:2000,color1:'#1a1a2e',color2:'#0d0d0d',direction:'radial'},
      {type:'text',text:'STREET\nWEAR',x:1000,y:540,size:200,color:'#ffffff',align:'center',bold:true,font:'Impact',shadow:true,shadow_color:'#6366f180',shadow_blur:30},
      {type:'rect',x:300,y:1000,w:1400,h:4,color:'#6366f1'},
      {type:'text',text:'LIMITED EDITION',x:1000,y:1050,size:50,color:'#6366f1',align:'center',bold:true,font:'Bahnschrift'},
      {type:'text',text:'Unisex · Premium Quality',x:1000,y:1160,size:40,color:'#6b6b9b',align:'center',font:'Segoe UI'},
    ]}},

  // Iglesia / Church
  { name: 'Iglesia Post', spec: {
    width:1080,height:1080,background:'#0a0a14',format:'webp',quality:92,
    filename:'iglesia-post',
    elements:[
      {type:'gradient',x:0,y:0,w:1080,h:1080,color1:'#1a1200',color2:'#0a0a0a',direction:'radial'},
      {type:'ellipse',x:240,y:240,w:600,h:600,color:'#ffd700',opacity:0.06},
      {type:'text',text:'†',x:540,y:160,size:120,color:'#ffd700',align:'center'},
      {type:'text',text:'DOMINGO',x:540,y:320,size:24,color:'#ffd700',align:'center',bold:true,font:'Bahnschrift'},
      {type:'text',text:'10:00 AM',x:540,y:360,size:18,color:'#a08030',align:'center',font:'Segoe UI'},
      {type:'text',text:'"La fe\nmueve montañas"',x:540,y:450,size:68,color:'#ffffff',align:'center',font:'Optimus Princeps',shadow:true,shadow_blur:15},
      {type:'text',text:'Mateo 17:20',x:540,y:680,size:28,color:'#ffd700',align:'center',font:'Gabriola'},
      {type:'text',text:'Nombre de la Iglesia',x:540,y:860,size:30,color:'#8a7040',align:'center',bold:true,font:'Roboto Slab'},
      {type:'text',text:'Todos son bienvenidos',x:540,y:920,size:22,color:'#5a5040',align:'center'},
    ]}},

  // Real Estate
  { name: 'Real Estate', spec: {
    width:1200,height:630,background:'#0f1923',format:'webp',quality:92,
    filename:'real-estate',
    elements:[
      {type:'gradient',x:0,y:0,w:1200,h:630,color1:'#0f1923',color2:'#1a2535',direction:'diagonal'},
      {type:'rect',x:0,y:0,w:6,h:630,color:'#c9a227'},
      {type:'rect',x:0,y:620,w:1200,h:10,color:'#c9a227'},
      {type:'text',text:'EXCLUSIVO',x:60,y:60,size:18,color:'#c9a227',bold:true,font:'Bahnschrift'},
      {type:'text',text:'Casa en Venta',x:60,y:110,size:80,color:'#ffffff',bold:true,font:'Roboto Slab',shadow:true,shadow_blur:10},
      {type:'text',text:'4 Hab · 3 Baños · 300 m²',x:60,y:240,size:32,color:'#8090a0',font:'Segoe UI'},
      {type:'rect',x:60,y:300,w:200,h:3,color:'#c9a227'},
      {type:'text',text:'USD 285,000',x:60,y:340,size:56,color:'#c9a227',bold:true,font:'Roboto Slab'},
      {type:'text',text:'Tu Inmobiliaria',x:900,y:560,size:24,color:'#6b7a8d',align:'right'},
    ]}},

  // Tech Banner
  { name: 'Banner Tech', spec: {
    width:1200,height:630,background:'#0a0a0f',format:'webp',quality:92,
    elements:[
      {type:'gradient',x:0,y:0,w:1200,h:630,color1:'#1e1b4b',color2:'#0a0a0f',direction:'diagonal'},
      {type:'rect',x:0,y:0,w:4,h:630,color:'#6366f1'},
      {type:'text',text:'{ code }',x:60,y:180,size:28,color:'#6366f1',font:'Consolas'},
      {type:'text',text:'Soluciones Tech',x:60,y:240,size:80,color:'#ffffff',bold:true,font:'Mukta'},
      {type:'text',text:'Innovacion · Calidad · Resultados',x:60,y:360,size:28,color:'#8b8ba8',font:'Segoe UI'},
    ]}},

  // Tarjeta personal
  { name: 'Tarjeta Personal', spec: {
    width:1050,height:600,background:'#ffffff',format:'webp',quality:92,
    elements:[
      {type:'rect',x:0,y:0,w:300,h:600,color:'#1e1e2e'},
      {type:'rect',x:300,y:0,w:8,h:600,color:'#6366f1'},
      {type:'gradient',x:0,y:0,w:300,h:600,color1:'#1e1e2e',color2:'#0f0f1a',direction:'vertical'},
      {type:'text',text:'Juan',x:150,y:200,size:38,color:'#ffffff',align:'center',bold:true,font:'Roboto Slab'},
      {type:'text',text:'García',x:150,y:255,size:38,color:'#6366f1',align:'center',bold:true,font:'Roboto Slab'},
      {type:'text',text:'Director',x:150,y:320,size:18,color:'#9898c0',align:'center'},
      {type:'text',text:'Mi Empresa',x:680,y:160,size:48,color:'#1e1e2e',bold:true,font:'Roboto Slab'},
      {type:'text',text:'contacto@empresa.com',x:680,y:270,size:22,color:'#6366f1'},
      {type:'text',text:'+54 11 1234-5678',x:680,y:330,size:22,color:'#6060a0'},
      {type:'text',text:'www.empresa.com',x:680,y:390,size:22,color:'#6060a0'},
    ]}},
];

function renderQuickTemplates() {
  const c = document.getElementById('quickTemplates');
  c.innerHTML = QUICK_TEMPLATES.map((t, i) =>
    `<button class="qtpl-btn" data-i="${i}">${t.name}</button>`
  ).join('');
  c.querySelectorAll('.qtpl-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const spec = JSON.stringify(QUICK_TEMPLATES[btn.dataset.i].spec, null, 2);
      document.getElementById('claudeJsonInput').value = spec;
    });
  });
}

document.getElementById('aiPreviewBtn').addEventListener('click', async () => {
  const raw = document.getElementById('claudeJsonInput').value.trim();
  if (!raw) return;
  try {
    const spec = JSON.parse(raw);
    const res = await fetch('/api/preview', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: raw,
    });
    const data = await res.json();
    if (data.error) return alert('Error: ' + data.error);
    const wrap = document.getElementById('aiPreviewWrap');
    wrap.innerHTML = `<img src="data:${data.mime};base64,${data.image}" alt="Preview">`;
  } catch (e) { alert('JSON invalido: ' + e.message); }
});

document.getElementById('aiDownloadBtn').addEventListener('click', async () => {
  const raw = document.getElementById('claudeJsonInput').value.trim();
  if (!raw) return;
  try {
    const spec = JSON.parse(raw);
    const res = await fetch('/api/download', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: raw,
    });
    const blob = await res.blob();
    const ext = (spec.format || 'webp');
    const name = spec.filename || 'diseno';
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${name}.${ext}`;
    a.click();
  } catch (e) { alert('Error: ' + e.message); }
});

/* ------------------------------------------------------------------ */
/* TABS                                                                 */
/* ------------------------------------------------------------------ */
document.querySelectorAll('.ptab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.ptab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
});

/* ------------------------------------------------------------------ */
/* MODALS                                                               */
/* ------------------------------------------------------------------ */
function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

document.querySelectorAll('.modal-close').forEach(btn => {
  btn.addEventListener('click', () => {
    const modalId = btn.dataset.modal || btn.closest('.modal')?.id;
    if (modalId) closeModal(modalId);
  });
});
document.querySelectorAll('.modal').forEach(m => {
  m.addEventListener('click', (e) => { if (e.target === m) closeModal(m.id); });
});

/* ------------------------------------------------------------------ */
/* KEYBOARD SHORTCUTS                                                    */
/* ------------------------------------------------------------------ */
document.addEventListener('keydown', (e) => {
  const tag = document.activeElement.tagName;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(tag)) return;

  const ctrl = e.ctrlKey || e.metaKey;
  if (ctrl && e.key === 'z') { e.preventDefault(); undo(); }
  else if (ctrl && (e.key === 'y' || (e.shiftKey && e.key === 'z'))) { e.preventDefault(); redo(); }
  else if (ctrl && e.key === 'c') { e.preventDefault(); copySelection(); }
  else if (ctrl && e.key === 'v') { e.preventDefault(); pasteSelection(); }
  else if (ctrl && e.key === 'd') {
    e.preventDefault();
    copySelection(); pasteSelection();
  }
  else if (ctrl && e.key === 'a') {
    e.preventDefault();
    const sel = new fabric.ActiveSelection(canvas.getObjects(), { canvas });
    canvas.setActiveObject(sel); canvas.requestRenderAll();
  }
  else if (ctrl && e.key === 'g') { e.preventDefault(); document.getElementById('groupBtn').click(); }
  else if (e.key === 'Delete' || e.key === 'Backspace') {
    e.preventDefault();
    canvas.getActiveObjects().forEach(o => canvas.remove(o));
    canvas.discardActiveObject(); canvas.renderAll(); saveHistory();
  }
  else if (e.key === 'v') setTool('select');
  else if (e.key === 't') setTool('text');
  else if (e.key === 'r') setTool('rect');
  else if (e.key === 'c') setTool('circle');
  else if (e.key === 'l') setTool('line');
  else if (e.key === 'Escape') {
    canvas.discardActiveObject(); canvas.renderAll();
    setTool('select');
  }
  // Arrow keys for nudging
  else if (['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) {
    const obj = canvas.getActiveObject(); if (!obj) return;
    const step = e.shiftKey ? 10 : 1;
    const d = { ArrowLeft: [-step,0], ArrowRight: [step,0], ArrowUp: [0,-step], ArrowDown: [0,step] };
    const [dx, dy] = d[e.key];
    obj.set({ left: (obj.left || 0) + dx, top: (obj.top || 0) + dy });
    obj.setCoords(); canvas.renderAll();
  }
});

/* ------------------------------------------------------------------ */
/* UX: Auto-select number inputs on focus                               */
/* ------------------------------------------------------------------ */
document.addEventListener('focus', (e) => {
  if (e.target.matches('#propertiesPanel input[type="number"], .size-row input[type="number"], .modal input[type="number"]')) {
    setTimeout(() => e.target.select(), 0);
  }
}, true);

/* ------------------------------------------------------------------ */
/* INIT                                                                 */
/* ------------------------------------------------------------------ */
async function init() {
  // Set initial canvas
  document.getElementById('cwInput').value = S.canvasW;
  document.getElementById('chInput').value = S.canvasH;

  // Load async resources
  await Promise.all([loadPresets(), loadCatalog(), loadProjectFonts()]);

  renderGradPresets();
  renderQuickBgColors();
  renderPatternBtns();
  renderQuickTemplates();

  // Fit canvas to screen
  fitCanvas();

  // Save initial history
  saveHistory();

  // Update quality label
  document.getElementById('qualityLabel').textContent = document.getElementById('exportQuality').value;

  // Export format change: toggle quality visibility
  document.getElementById('exportFormat').addEventListener('change', function() {
    document.querySelector('.quality-wrap').style.opacity = this.value === 'png' ? '0.3' : '1';
  });

  // Resize observer for canvas area
  const observer = new ResizeObserver(() => fitCanvas());
  observer.observe(document.getElementById('canvasWrapper'));

  console.log('%cGC Canva listo ✓', 'color:#6366f1;font-weight:bold;font-size:14px');
}

init();
