let vanta = VANTA.FOG({
  el: "#background",
  mouseControls: false,
  touchControls: false,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  highlightColor: 0x2c2c2c,
  midtoneColor: 0x272727,
  lowlightColor: 0x151515,
  baseColor: 0x1a1a1a,
  blurFactor: 0.90,
  speed: 4,
  zoom: 0.50
})


const configs = {
  error: {
    highlightColor: 0x382424,
    midtoneColor: 0x422323,
    lowlightColor: 0x452d2d,
    baseColor: 0x1a0808
  },

  main: {
    highlightColor: 0x2c2c2c,
    midtoneColor:   0x272727,
    lowlightColor:  0x151515,
    baseColor:      0x1a1a1a
  },

  waiting: {
    highlightColor: 0x59503a,
    midtoneColor: 0x453713,
    lowlightColor: 0x362e18,
    baseColor: 0x151515
  }
};


// ——— Утилиты ———
let _vantaColorAnim = { raf: null, cancel: false };

function toHexInt(c) {
  if (typeof c === 'number') return c >>> 0;
  if (typeof c === 'string') {
    let s = c.trim();
    if (s[0] === '#') s = s.slice(1);
    return parseInt(s, 16) >>> 0;
  }
  if (typeof c === 'object' && c !== null) {
    // THREE.Color or {r,g,b} (0..1 or 0..255?)
    if (typeof c.r === 'number' && typeof c.g === 'number' && typeof c.b === 'number') {
      // если компоненты от 0..1 — приводим
      let r = c.r <= 1 ? Math.round(c.r * 255) : Math.round(c.r);
      let g = c.g <= 1 ? Math.round(c.g * 255) : Math.round(c.g);
      let b = c.b <= 1 ? Math.round(c.b * 255) : Math.round(c.b);
      return ((r & 0xff) << 16) | ((g & 0xff) << 8) | (b & 0xff);
    }
  }
  return 0;
}

function padHex(n) {
  return n.toString(16).padStart(6, '0');
}

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// ——— Основная функция: возвращает Promise, который резолвится по завершении ———
function changeConfigById(id, duration = 2000) {
  const targetConfig = configs[id];
  if (!targetConfig) {
    console.warn(`Config with id ${id} not found`);
    return Promise.resolve();
  }

  // отменяем предыдущую анимацию
  if (_vantaColorAnim.raf) {
    _vantaColorAnim.cancel = true;
    cancelAnimationFrame(_vantaColorAnim.raf);
    _vantaColorAnim = { raf: null, cancel: false };
  }

  // пытаемся достать текущие цвета из vanta (варианты возможны)
  const startConfig = {
    highlightColor: toHexInt(vanta.highlightColor ?? vanta.options?.highlightColor ?? configs.main.highlightColor),
    midtoneColor: toHexInt(vanta.midtoneColor ?? vanta.options?.midtoneColor ?? configs.main.midtoneColor),
    lowlightColor: toHexInt(vanta.lowlightColor ?? vanta.options?.lowlightColor ?? configs.main.lowlightColor),
    baseColor: toHexInt(vanta.baseColor ?? vanta.options?.baseColor ?? configs.main.baseColor)
  };

  const targetHex = {
    highlightColor: toHexInt(targetConfig.highlightColor),
    midtoneColor: toHexInt(targetConfig.midtoneColor),
    lowlightColor: toHexInt(targetConfig.lowlightColor),
    baseColor: toHexInt(targetConfig.baseColor)
  };

  return new Promise((resolve) => {
    let startTime = null;
    _vantaColorAnim.cancel = false;

    function lerpInts(aInt, bInt, t) {
      // Если THREE есть — используем его (лучше для цвета)
      if (window.THREE && typeof THREE.Color === 'function') {
        const a = new THREE.Color('#' + padHex(aInt));
        const b = new THREE.Color('#' + padHex(bInt));
        const c = a.clone().lerp(b, t);
        return ((Math.round(c.r * 255) & 0xff) << 16) | ((Math.round(c.g * 255) & 0xff) << 8) | (Math.round(c.b * 255) & 0xff);
      } else {
        // fallback: линейно интерполируем по каналам
        const ar = (aInt >> 16) & 0xff;
        const ag = (aInt >> 8) & 0xff;
        const ab = aInt & 0xff;

        const br = (bInt >> 16) & 0xff;
        const bg = (bInt >> 8) & 0xff;
        const bb = bInt & 0xff;

        const rr = Math.round(ar + (br - ar) * t);
        const rg = Math.round(ag + (bg - ag) * t);
        const rb = Math.round(ab + (bb - ab) * t);

        return ((rr & 0xff) << 16) | ((rg & 0xff) << 8) | (rb & 0xff);
      }
    }

    function frame(time) {
      if (_vantaColorAnim.cancel) {
        _vantaColorAnim.raf = null;
        return resolve(); // отменено
      }
      if (!startTime) startTime = time;
      let t = (time - startTime) / duration;
      if (t >= 1) t = 1;
      t = easeInOutCubic(t);

      vanta.setOptions({
        highlightColor: lerpInts(startConfig.highlightColor, targetHex.highlightColor, t),
        midtoneColor:  lerpInts(startConfig.midtoneColor, targetHex.midtoneColor, t),
        lowlightColor: lerpInts(startConfig.lowlightColor, targetHex.lowlightColor, t),
        baseColor:     lerpInts(startConfig.baseColor, targetHex.baseColor, t)
      });

      if (t < 1) {
        _vantaColorAnim.raf = requestAnimationFrame(frame);
      } else {
        _vantaColorAnim.raf = null;
        resolve();
      }
    }

    _vantaColorAnim.raf = requestAnimationFrame(frame);
  });
}