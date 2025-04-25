/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./helpers.js":
/*!********************!*\
  !*** ./helpers.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getMatches": () => (/* binding */ getMatches),
/* harmony export */   "hslToRGB": () => (/* binding */ hslToRGB),
/* harmony export */   "rgbToHSL": () => (/* binding */ rgbToHSL),
/* harmony export */   "rgbToHexString": () => (/* binding */ rgbToHexString),
/* harmony export */   "rgbToString": () => (/* binding */ rgbToString)
/* harmony export */ });
function rgbToHSL({
  r,
  g,
  b,
  a = 1
}) {
  r = r / 255;
  g = g / 255;
  b = b / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const c = max - min;
  const l = (max + min) / 2;

  if (c === 0) {
    return {
      h: 0,
      s: 0,
      l,
      a
    };
  }

  let h = (max === r ? (g - b) / c % 6 : max === g ? (b - r) / c + 2 : (r - g) / c + 4) * 60;

  if (h < 0) {
    h += 360;
  }

  const s = c / (1 - Math.abs(2 * l - 1));
  return {
    h,
    s,
    l,
    a
  };
}
function rgbToString(rgb) {
  const {
    r,
    g,
    b,
    a
  } = rgb;

  if (a != null && a < 1) {
    return `rgba(${toFixed(r)}, ${toFixed(g)}, ${toFixed(b)}, ${toFixed(a, 2)})`;
  }

  return `rgb(${toFixed(r)}, ${toFixed(g)}, ${toFixed(b)})`;
}
function rgbToHexString({
  r,
  g,
  b,
  a
}) {
  return `#${(a != null && a < 1 ? [r, g, b, Math.round(a * 255)] : [r, g, b]).map(x => {
    return `${x < 16 ? '0' : ''}${x.toString(16)}`;
  }).join('')}`;
}
function hslToRGB({
  h,
  s,
  l,
  a = 1
}) {
  if (s === 0) {
    const [r, b, g] = [l, l, l].map(x => Math.round(x * 255));
    return {
      r,
      g,
      b,
      a
    };
  }

  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(h / 60 % 2 - 1));
  const m = l - c / 2;
  const [r, g, b] = (h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x]).map(n => Math.round((n + m) * 255));
  return {
    r,
    g,
    b,
    a
  };
}
function getMatches(regex, input, group = 0) {
  const matches = [];
  let m;

  while (m = regex.exec(input)) {
    matches.push(m[group]);
  }

  return matches;
}

function toFixed(n, digits = 0) {
  const fixed = n.toFixed(digits);

  if (digits === 0) {
    return fixed;
  }

  const dot = fixed.indexOf('.');

  if (dot >= 0) {
    const zerosMatch = fixed.match(/0+$/);

    if (zerosMatch) {
      if (zerosMatch.index === dot + 1) {
        return fixed.substring(0, dot);
      }

      return fixed.substring(0, zerosMatch.index);
    }
  }

  return fixed;
}

/***/ }),

/***/ "./math.js":
/*!*****************!*\
  !*** ./math.js ***!
  \*****************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "applyColorMatrix": () => (/* binding */ applyColorMatrix),
/* harmony export */   "clamp": () => (/* binding */ clamp),
/* harmony export */   "createFilterMatrix": () => (/* binding */ createFilterMatrix),
/* harmony export */   "multiplyMatrices": () => (/* binding */ multiplyMatrices),
/* harmony export */   "scale": () => (/* binding */ scale)
/* harmony export */ });
const Matrix = {
  identity() {
    return [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]];
  },

  invertNHue() {
    return [[0.333, -0.667, -0.667, 0, 1], [-0.667, 0.333, -0.667, 0, 1], [-0.667, -0.667, 0.333, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]];
  },

  brightness(v) {
    return [[v, 0, 0, 0, 0], [0, v, 0, 0, 0], [0, 0, v, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]];
  },

  contrast(v) {
    const t = (1 - v) / 2;
    return [[v, 0, 0, 0, t], [0, v, 0, 0, t], [0, 0, v, 0, t], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]];
  },

  sepia(v) {
    return [[0.393 + 0.607 * (1 - v), 0.769 - 0.769 * (1 - v), 0.189 - 0.189 * (1 - v), 0, 0], [0.349 - 0.349 * (1 - v), 0.686 + 0.314 * (1 - v), 0.168 - 0.168 * (1 - v), 0, 0], [0.272 - 0.272 * (1 - v), 0.534 - 0.534 * (1 - v), 0.131 + 0.869 * (1 - v), 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]];
  },

  grayscale(v) {
    return [[0.2126 + 0.7874 * (1 - v), 0.7152 - 0.7152 * (1 - v), 0.0722 - 0.0722 * (1 - v), 0, 0], [0.2126 - 0.2126 * (1 - v), 0.7152 + 0.2848 * (1 - v), 0.0722 - 0.0722 * (1 - v), 0, 0], [0.2126 - 0.2126 * (1 - v), 0.7152 - 0.7152 * (1 - v), 0.0722 + 0.9278 * (1 - v), 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]];
  }

};
function scale(x, inLow, inHigh, outLow, outHigh) {
  return (x - inLow) * (outHigh - outLow) / (inHigh - inLow) + outLow;
}
function createFilterMatrix(config) {
  let m = Matrix.identity();

  if (config.sepia !== 0) {
    m = multiplyMatrices(m, Matrix.sepia(config.sepia / 100));
  }

  if (config.grayscale !== 0) {
    m = multiplyMatrices(m, Matrix.grayscale(config.grayscale / 100));
  }

  if (config.contrast !== 100) {
    m = multiplyMatrices(m, Matrix.contrast(config.contrast / 100));
  }

  if (config.brightness !== 100) {
    m = multiplyMatrices(m, Matrix.brightness(config.brightness / 100));
  }

  if (config.mode === 1) {
    m = multiplyMatrices(m, Matrix.invertNHue());
  }

  return m;
}
function multiplyMatrices(m1, m2) {
  const result = [];

  for (let i = 0; i < m1.length; i++) {
    result[i] = [];

    for (let j = 0; j < m2[0].length; j++) {
      let sum = 0;

      for (let k = 0; k < m1[0].length; k++) {
        sum += m1[i][k] * m2[k][j];
      }

      result[i][j] = sum;
    }
  }

  return result;
}
function applyColorMatrix([r, g, b], matrix) {
  const rgb = [[r / 255], [g / 255], [b / 255], [1], [1]];
  const result = multiplyMatrices(matrix, rgb);
  return [0, 1, 2].map(i => clamp(Math.round(result[i][0] * 255), 0, 255));
}
function clamp(x, min, max) {
  return Math.min(max, Math.max(min, x));
}

/***/ }),

/***/ "./modify.js":
/*!*******************!*\
  !*** ./modify.js ***!
  \*******************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "colorMatch": () => (/* binding */ colorMatch),
/* harmony export */   "findAndReplaceColor": () => (/* binding */ findAndReplaceColor),
/* harmony export */   "modifyBgHSL": () => (/* binding */ modifyBgHSL),
/* harmony export */   "modifyBorderHSL": () => (/* binding */ modifyBorderHSL),
/* harmony export */   "modifyColor": () => (/* binding */ modifyColor),
/* harmony export */   "modifyFgHSL": () => (/* binding */ modifyFgHSL)
/* harmony export */ });
/* harmony import */ var _math__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./math */ "./math.js");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./helpers */ "./helpers.js");
/* harmony import */ var _parsers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./parsers */ "./parsers.js");




let filter = {
  mode: 0,
  brightness: 100,
  contrast: 100,
  grayscale: 0,
  sepia: 0,
  useFont: false,
  fontFamily: "Hiragino Kaku Gothic Pro",
  textStroke: 0,
  stylesheet: ""
};
const colorMatch = /(#(?:[0-9a-f]{2}){2,4}|(#[0-9a-f]{3})|(rgb|hsl)a?\((-?\d+%?[,\s]+){2,3}\s*[\d\.]+%?\)|black|silver|gray|whitesmoke|maroon|red|purple|fuchsia|green|lime|olivedrab|yellow|navy|blue|teal|aquamarine|orange|aliceblue|antiquewhite|aqua|azure|beige|bisque|blanchedalmond|blueviolet|brown|burlywood|cadetblue|chartreuse|chocolate|coral|cornflowerblue|cornsilk|crimson|darkblue|darkcyan|darkgoldenrod|darkgray|darkgreen|darkgrey|darkkhaki|darkmagenta|darkolivegreen|darkorange|darkorchid|darkred|darksalmon|darkseagreen|darkslateblue|darkslategray|darkslategrey|darkturquoise|darkviolet|deeppink|deepskyblue|dimgray|dimgrey|dodgerblue|firebrick|floralwhite|forestgreen|gainsboro|ghostwhite|goldenrod|gold|greenyellow|grey|honeydew|hotpink|indianred|indigo|ivory|khaki|lavenderblush|lavender|lawngreen|lemonchiffon|lightblue|lightcoral|lightcyan|lightgoldenrodyellow|lightgray|lightgreen|lightgrey|lightpink|lightsalmon|lightseagreen|lightskyblue|lightslategray|lightslategrey|lightsteelblue|lightyellow|limegreen|linen|mediumaquamarine|mediumblue|mediumorchid|mediumpurple|mediumseagreen|mediumslateblue|mediumspringgreen|mediumturquoise|mediumvioletred|midnightblue|mintcream|mistyrose|moccasin|navajowhite|oldlace|olive|orangered|orchid|palegoldenrod|palegreen|paleturquoise|palevioletred|papayawhip|peachpuff|peru|pink|plum|powderblue|rosybrown|royalblue|saddlebrown|salmon|sandybrown|seagreen|seashell|sienna|skyblue|slateblue|slategray|slategrey|snow|springgreen|steelblue|tan|thistle|tomato|turquoise|violet|wheat|white|yellowgreen|rebeccapurple)/gi;
function modifyBgHSL({
  h,
  s,
  l,
  a
}) {
  const lMin = 0.22;
  const lMaxS0 = 0.25;
  const lMaxS1 = 0.4;
  const sNeutralLim = 0.12;
  const lNeutralLight = 0.8;
  const sColored = 0.05;
  const hColored = 205;
  const hBlue0 = 200;
  const hBlue1 = 280;

  if (a < 0.1 && a > 0) {
    a = 0.3;
    return {
      h: h,
      s: s,
      l: l,
      a
    };
  }

  const lMax = (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(s, 0, 1, lMaxS0, lMaxS1);
  const lx = l < lMax ? l : l < 0.5 ? lMax : (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(l, 0.5, 1, lMax, lMin);
  const isNeutral = l >= lNeutralLight && h > hBlue0 && h < hBlue1 || s < sNeutralLim;
  let hx = h;
  let sx = s;

  if (isNeutral) {
    sx = sColored;
    hx = hColored;
  }

  return {
    h: hx,
    s: sx,
    l: lx,
    a
  };
}
function modifyFgHSL({
  h,
  s,
  l,
  a
}) {
  const lMax = 0.9;
  const lMinS0 = 0.9;
  const lMinS1 = 0.6;
  const sNeutralLim = 0.24;
  const lNeutralDark = 0.2;
  const sColored = 0.20;
  const hColored = 40;
  const hBlue0 = 205;
  const hBlue1 = 245;
  const hBlueMax = 220;
  const lBlueMin = 0.7;
  const isBlue = h > hBlue0 && h <= hBlue1;
  const lMin = (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(s, 0, 1, isBlue ? (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(h, hBlue0, hBlue1, lMinS0, lBlueMin) : lMinS0, lMinS1);
  const lx = l < 0.5 ? (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(l, 0, 0.5, lMax, lMin) : l < lMin ? lMin : l;
  let hx = h;
  let sx = s;

  if (isBlue) {
    hx = (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(hx, hBlue0, hBlue1, hBlue0, hBlueMax);
  }

  const isNeutral = l < lNeutralDark || s < sNeutralLim;

  if (isNeutral) {
    sx = sColored;
    hx = hColored;
  }

  return {
    h: hx,
    s: sx,
    l: lx,
    a
  };
}
function modifyBorderHSL({
  h,
  s,
  l,
  a
}) {
  const lMinS0 = 0.3;
  const lMinS1 = 0.4;
  const lMaxS0 = 0.4;
  const lMaxS1 = 0.5;
  const lMin = (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(s, 0, 1, lMinS0, lMinS1);
  const lMax = (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(s, 0, 1, lMaxS0, lMaxS1);
  const lx = (0,_math__WEBPACK_IMPORTED_MODULE_0__.scale)(l, 0, 1, lMax, lMin);
  return {
    h,
    s,
    l: lx,
    a
  };
}
function modifyColor(rgb, modifyHSL) {
  if (rgb == '0px' || rgb == '0px 0px' || rgb == '0 0' || rgb == 'none') {
    return rgb;
  }

  let hsl = (0,_helpers__WEBPACK_IMPORTED_MODULE_1__.rgbToHSL)(rgb);
  let modified = modifyHSL(hsl);
  let {
    r,
    g,
    b,
    a
  } = (0,_helpers__WEBPACK_IMPORTED_MODULE_1__.hslToRGB)(modified);
  let matrix = (0,_math__WEBPACK_IMPORTED_MODULE_0__.createFilterMatrix)(filter);
  let [rf, gf, bf] = (0,_math__WEBPACK_IMPORTED_MODULE_0__.applyColorMatrix)([r, g, b], matrix);
  let color = a === 1 ? (0,_helpers__WEBPACK_IMPORTED_MODULE_1__.rgbToHexString)({
    r: rf,
    g: gf,
    b: bf
  }) : (0,_helpers__WEBPACK_IMPORTED_MODULE_1__.rgbToString)({
    r: rf,
    g: gf,
    b: bf,
    a
  });
  return color.trim();
}

function clearTrash(value, modifier) {
  let colors = value.replace(/url\(.*?\)/g, '').match(colorMatch);

  if (colors) {
    Array.from(colors).forEach(color => {
      let rgb = (0,_parsers__WEBPACK_IMPORTED_MODULE_2__.parse)(color);
      let modifyCol = modifyColor(rgb, modifier);
      value = value.replace(color, modifyCol);
    });
  }

  return value;
}

function findAndReplaceColor(value, modifier) {
  try {
    if (value == '0px' || value == '0px 0px' || value == '0 0' || value == 'none') {
      return value;
    }

    let matchess = value.match(/var\(.*?\)/g);

    if (matchess) {
      let matcher = value.match(/--(.+?)(?=\)|,)/g).reverse();

      for (var prop in matcher) {
        let match = matcher[prop];
        let cssVar = match.trim();

        if (cssVar) {
          let valCss = (0,_parsers__WEBPACK_IMPORTED_MODULE_2__.getValFromCache)(cssVar);

          if (valCss) {
            valCss = valCss.trim();
            let rrr = new RegExp('var\\([^var\\(]*?' + cssVar + '[^\\)]*\\)', 'g');
            let newValCss = value.replace(rrr, valCss);
            newValCss = clearTrash(newValCss, modifier);
            let one = (newValCss.match(/\)/g) || []).length;
            let two = (newValCss.match(/\(/g) || []).length;

            if (one != two) {
              return valCss;
            }

            setTimeout(function () {
              let style = getComputedStyle(document.body);
              let valCss = style.getPropertyValue(cssVar);

              if (valCss) {
                (0,_parsers__WEBPACK_IMPORTED_MODULE_2__.setValToCache)(cssVar, valCss);
              }
            }, 6000);

            if (value == 'var(--steel_gray_60)') {
              console.log('TEST', match, valCss, newValCss);
            }

            return newValCss;
          } else {
            try {
              let style = getComputedStyle(document.body);
              let valCss = style.getPropertyValue(cssVar);

              if (valCss) {
                (0,_parsers__WEBPACK_IMPORTED_MODULE_2__.setValToCache)(cssVar, valCss);
              } else {
                if (modifier.name == 'modifyBgHSL') {
                  valCss = "rgba(53,57,59,0.7)";
                  return valCss;
                } else if (modifier.name == 'modifyFgHSL') {
                  valCss = "#bab5ab";
                  return valCss;
                }

                throw "Error2";
              }

              valCss = valCss.trim();
              let rrr = new RegExp('var\\([^var\\(]*?' + cssVar + '[^\\)]*\\)', 'g');
              let newValCss = value.replace(rrr, valCss);
              newValCss = clearTrash(newValCss, modifier);
              return newValCss;
            } catch (e) {
              setTimeout(function () {
                let style = getComputedStyle(document.body);
                let valCss = style.getPropertyValue(cssVar);

                if (valCss) {
                  (0,_parsers__WEBPACK_IMPORTED_MODULE_2__.setValToCache)(cssVar, valCss);
                }

                valCss = valCss.trim();
                let rrr = new RegExp('var\\([^var\\(]*?' + cssVar + '[^\\)]*\\)', 'g');
                let newValCss = value.replace(rrr, valCss);
                newValCss = clearTrash(newValCss, modifier);
                return newValCss;
              }, 8000);
            }
          }
        }
      }
    } else {
      value = clearTrash(value, modifier);
      return value;
    }
  } catch (e) {
    let modifyCol = modifyColor(value, modifier);
    return modifyCol;
  }
}

/***/ }),

/***/ "./parsers.js":
/*!********************!*\
  !*** ./parsers.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getColorFromVar": () => (/* binding */ getColorFromVar),
/* harmony export */   "getValFromCache": () => (/* binding */ getValFromCache),
/* harmony export */   "parse": () => (/* binding */ parse),
/* harmony export */   "setValToCache": () => (/* binding */ setValToCache)
/* harmony export */ });
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./helpers */ "./helpers.js");

const rgbMatch = /^rgba?\([^\(\)]+\)$/;
const hslMatch = /^hsla?\([^\(\)]+\)$/;
const hexMatch = /^#[0-9a-f]+$/i;
const hslSplitter = /hsla?|\(|\)|\/|,|\s/ig;
const hslRange = [360, 1, 1, 1];
const hslUnits = {
  '%': 100,
  'deg': 360,
  'rad': 2 * Math.PI,
  'turn': 1
};
const rgbSplitter = /rgba?|\(|\)|\/|,|\s/ig;
const rgbRange = [255, 255, 255, 1];
const rgbUnits = {
  '%': 100
};
const knownColors = new Map(Object.entries({
  aliceblue: 0xf0f8ff,
  antiquewhite: 0xfaebd7,
  aqua: 0x00ffff,
  aquamarine: 0x7fffd4,
  azure: 0xf0ffff,
  beige: 0xf5f5dc,
  bisque: 0xffe4c4,
  black: 0x000000,
  blanchedalmond: 0xffebcd,
  blue: 0x0000ff,
  blueviolet: 0x8a2be2,
  brown: 0xa52a2a,
  burlywood: 0xdeb887,
  cadetblue: 0x5f9ea0,
  chartreuse: 0x7fff00,
  chocolate: 0xd2691e,
  coral: 0xff7f50,
  cornflowerblue: 0x6495ed,
  cornsilk: 0xfff8dc,
  crimson: 0xdc143c,
  cyan: 0x00ffff,
  darkblue: 0x00008b,
  darkcyan: 0x008b8b,
  darkgoldenrod: 0xb8860b,
  darkgray: 0xa9a9a9,
  darkgrey: 0xa9a9a9,
  darkgreen: 0x006400,
  darkkhaki: 0xbdb76b,
  darkmagenta: 0x8b008b,
  darkolivegreen: 0x556b2f,
  darkorange: 0xff8c00,
  darkorchid: 0x9932cc,
  darkred: 0x8b0000,
  darksalmon: 0xe9967a,
  darkseagreen: 0x8fbc8f,
  darkslateblue: 0x483d8b,
  darkslategray: 0x2f4f4f,
  darkslategrey: 0x2f4f4f,
  darkturquoise: 0x00ced1,
  darkviolet: 0x9400d3,
  deeppink: 0xff1493,
  deepskyblue: 0x00bfff,
  dimgray: 0x696969,
  dimgrey: 0x696969,
  dodgerblue: 0x1e90ff,
  firebrick: 0xb22222,
  floralwhite: 0xfffaf0,
  forestgreen: 0x228b22,
  fuchsia: 0xff00ff,
  gainsboro: 0xdcdcdc,
  ghostwhite: 0xf8f8ff,
  gold: 0xffd700,
  goldenrod: 0xdaa520,
  gray: 0x808080,
  grey: 0x808080,
  green: 0x008000,
  greenyellow: 0xadff2f,
  honeydew: 0xf0fff0,
  hotpink: 0xff69b4,
  indianred: 0xcd5c5c,
  indigo: 0x4b0082,
  ivory: 0xfffff0,
  khaki: 0xf0e68c,
  lavender: 0xe6e6fa,
  lavenderblush: 0xfff0f5,
  lawngreen: 0x7cfc00,
  lemonchiffon: 0xfffacd,
  lightblue: 0xadd8e6,
  lightcoral: 0xf08080,
  lightcyan: 0xe0ffff,
  lightgoldenrodyellow: 0xfafad2,
  lightgray: 0xd3d3d3,
  lightgrey: 0xd3d3d3,
  lightgreen: 0x90ee90,
  lightpink: 0xffb6c1,
  lightsalmon: 0xffa07a,
  lightseagreen: 0x20b2aa,
  lightskyblue: 0x87cefa,
  lightslategray: 0x778899,
  lightslategrey: 0x778899,
  lightsteelblue: 0xb0c4de,
  lightyellow: 0xffffe0,
  lime: 0x00ff00,
  limegreen: 0x32cd32,
  linen: 0xfaf0e6,
  magenta: 0xff00ff,
  maroon: 0x800000,
  mediumaquamarine: 0x66cdaa,
  mediumblue: 0x0000cd,
  mediumorchid: 0xba55d3,
  mediumpurple: 0x9370db,
  mediumseagreen: 0x3cb371,
  mediumslateblue: 0x7b68ee,
  mediumspringgreen: 0x00fa9a,
  mediumturquoise: 0x48d1cc,
  mediumvioletred: 0xc71585,
  midnightblue: 0x191970,
  mintcream: 0xf5fffa,
  mistyrose: 0xffe4e1,
  moccasin: 0xffe4b5,
  navajowhite: 0xffdead,
  navy: 0x000080,
  oldlace: 0xfdf5e6,
  olive: 0x808000,
  olivedrab: 0x6b8e23,
  orange: 0xffa500,
  orangered: 0xff4500,
  orchid: 0xda70d6,
  palegoldenrod: 0xeee8aa,
  palegreen: 0x98fb98,
  paleturquoise: 0xafeeee,
  palevioletred: 0xdb7093,
  papayawhip: 0xffefd5,
  peachpuff: 0xffdab9,
  peru: 0xcd853f,
  pink: 0xffc0cb,
  plum: 0xdda0dd,
  powderblue: 0xb0e0e6,
  purple: 0x800080,
  rebeccapurple: 0x663399,
  red: 0xff0000,
  rosybrown: 0xbc8f8f,
  royalblue: 0x4169e1,
  saddlebrown: 0x8b4513,
  salmon: 0xfa8072,
  sandybrown: 0xf4a460,
  seagreen: 0x2e8b57,
  seashell: 0xfff5ee,
  sienna: 0xa0522d,
  silver: 0xc0c0c0,
  skyblue: 0x87ceeb,
  slateblue: 0x6a5acd,
  slategray: 0x708090,
  slategrey: 0x708090,
  snow: 0xfffafa,
  springgreen: 0x00ff7f,
  steelblue: 0x4682b4,
  tan: 0xd2b48c,
  teal: 0x008080,
  thistle: 0xd8bfd8,
  tomato: 0xff6347,
  turquoise: 0x40e0d0,
  violet: 0xee82ee,
  wheat: 0xf5deb3,
  white: 0xffffff,
  whitesmoke: 0xf5f5f5,
  yellow: 0xffff00,
  yellowgreen: 0x9acd32
}));
const systemColors = new Map(Object.entries({
  ActiveBorder: 0x3b99fc,
  ActiveCaption: 0x000000,
  AppWorkspace: 0xaaaaaa,
  Background: 0x6363ce,
  ButtonFace: 0xffffff,
  ButtonHighlight: 0xe9e9e9,
  ButtonShadow: 0x9fa09f,
  ButtonText: 0x000000,
  CaptionText: 0x000000,
  GrayText: 0x7f7f7f,
  Highlight: 0xb2d7ff,
  HighlightText: 0x000000,
  InactiveBorder: 0xffffff,
  InactiveCaption: 0xffffff,
  InactiveCaptionText: 0x000000,
  InfoBackground: 0xfbfcc5,
  InfoText: 0x000000,
  Menu: 0xf6f6f6,
  MenuText: 0xffffff,
  Scrollbar: 0xaaaaaa,
  ThreeDDarkShadow: 0x000000,
  ThreeDFace: 0xc0c0c0,
  ThreeDHighlight: 0xffffff,
  ThreeDLightShadow: 0xffffff,
  ThreeDShadow: 0x000000,
  Window: 0xececec,
  WindowFrame: 0xaaaaaa,
  WindowText: 0x000000,
  '-webkit-focus-ring-color': 0xe59700
}).map(([key, value]) => [key.toLowerCase(), value]));
const colorMatch = /(#(?:[0-9a-f]{2}){2,4}|(#[0-9a-f]{3})|(rgb|hsl)a?\((-?\d+%?[,\s]+){2,3}\s*[\d\.]+%?\)|black|silver|gray|whitesmoke|maroon|red|purple|fuchsia|green|lime|olivedrab|yellow|navy|blue|teal|aquamarine|orange|aliceblue|antiquewhite|aqua|azure|beige|bisque|blanchedalmond|blueviolet|brown|burlywood|cadetblue|chartreuse|chocolate|coral|cornflowerblue|cornsilk|crimson|darkblue|darkcyan|darkgoldenrod|darkgray|darkgreen|darkgrey|darkkhaki|darkmagenta|darkolivegreen|darkorange|darkorchid|darkred|darksalmon|darkseagreen|darkslateblue|darkslategray|darkslategrey|darkturquoise|darkviolet|deeppink|deepskyblue|dimgray|dimgrey|dodgerblue|firebrick|floralwhite|forestgreen|gainsboro|ghostwhite|goldenrod|gold|greenyellow|grey|honeydew|hotpink|indianred|indigo|ivory|khaki|lavenderblush|lavender|lawngreen|lemonchiffon|lightblue|lightcoral|lightcyan|lightgoldenrodyellow|lightgray|lightgreen|lightgrey|lightpink|lightsalmon|lightseagreen|lightskyblue|lightslategray|lightslategrey|lightsteelblue|lightyellow|limegreen|linen|mediumaquamarine|mediumblue|mediumorchid|mediumpurple|mediumseagreen|mediumslateblue|mediumspringgreen|mediumturquoise|mediumvioletred|midnightblue|mintcream|mistyrose|moccasin|navajowhite|oldlace|olive|orangered|orchid|palegoldenrod|palegreen|paleturquoise|palevioletred|papayawhip|peachpuff|peru|pink|plum|powderblue|rosybrown|royalblue|saddlebrown|salmon|sandybrown|seagreen|seashell|sienna|skyblue|slateblue|slategray|slategrey|snow|springgreen|steelblue|tan|thistle|tomato|turquoise|violet|wheat|white|yellowgreen|rebeccapurple)/gi;

function parseRGB($rgb) {
  const [r, g, b, a = 1] = getNumbersFromString($rgb, rgbSplitter, rgbRange, rgbUnits);
  return {
    r,
    g,
    b,
    a
  };
}

function parseHSL($hsl) {
  const [h, s, l, a = 1] = getNumbersFromString($hsl, hslSplitter, hslRange, hslUnits);
  return (0,_helpers__WEBPACK_IMPORTED_MODULE_0__.hslToRGB)({
    h,
    s,
    l,
    a
  });
}

function parseHex($hex) {
  const h = $hex.substring(1);

  switch (h.length) {
    case 3:
    case 4:
      {
        const [r, g, b] = [0, 1, 2].map(i => parseInt(`${h[i]}${h[i]}`, 16));
        const a = h.length === 3 ? 1 : parseInt(`${h[3]}${h[3]}`, 16) / 255;
        return {
          r,
          g,
          b,
          a
        };
      }

    case 6:
    case 8:
      {
        const [r, g, b] = [0, 2, 4].map(i => parseInt(h.substring(i, i + 2), 16));
        const a = h.length === 6 ? 1 : parseInt(h.substring(6, 8), 16) / 255;
        return {
          r,
          g,
          b,
          a
        };
      }
  }

  throw new Error(`Unable to parse ${$hex}`);
}

function getNumbersFromString(str, splitter, range, units) {
  const raw = str.split(splitter).filter(x => x);
  const unitsList = Object.entries(units);
  const numbers = raw.map(r => r.trim()).map((r, i) => {
    let n;
    const unit = unitsList.find(([u]) => r.endsWith(u));

    if (unit) {
      n = parseFloat(r.substring(0, r.length - unit[0].length)) / unit[1] * range[i];
    } else {
      n = parseFloat(r);
    }

    if (range[i] > 1) {
      return Math.round(n);
    }

    return n;
  });
  return numbers;
}

function getColorByName($color) {
  const n = knownColors.get($color);
  return {
    r: n >> 16 & 255,
    g: n >> 8 & 255,
    b: n >> 0 & 255,
    a: 1
  };
}

function getSystemColor($color) {
  const n = systemColors.get($color);
  return {
    r: n >> 16 & 255,
    g: n >> 8 & 255,
    b: n >> 0 & 255,
    a: 1
  };
}

function getColorFromVar(string, stringVar) {
  let cssVar = stringVar.trim();

  try {
    let style = getComputedStyle(document.body);
    let prop = style.getPropertyValue(cssVar); //let color = string.replace(/var\(.*?\)/, prop).replace(' ', '');

    return prop;
  } catch (e) {
    setTimeout(function () {
      let style = getComputedStyle(document.body);
      let prop = style.getPropertyValue(cssVar);

      if (valCss) {
        setValToCache(newMatch[0], valCss);
        value = valCss;
      }

      console.log(cssVar, prop);
    }, 2000);
    return stringVar;
  }
}
function parse($color) {
  const c = $color.trim().toLowerCase();
  return parseColor(c);
}

function parseColor(c) {
  if (c.match(rgbMatch)) {
    return parseRGB(c);
  }

  if (c.match(hslMatch)) {
    return parseHSL(c);
  }

  if (c.match(hexMatch)) {
    return parseHex(c);
  }

  if (knownColors.has(c)) {
    return getColorByName(c);
  }

  if (systemColors.has(c)) {
    return getSystemColor(c);
  }

  return c;
}

function getValFromCache(cssVar) {
  return localStorage[cssVar] ? JSON.parse(localStorage[cssVar]) : localStorage[cssVar];
}
function setValToCache(cssVar, valCss) {
  localStorage[cssVar] = JSON.stringify(valCss);
}

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
/*!*****************!*\
  !*** ./dark.js ***!
  \*****************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _modify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./modify */ "./modify.js");
/* harmony import */ var _parsers__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./parsers */ "./parsers.js");


chrome.storage.local.get().then(res => {
  const win = window;

  if (win === win.self && win === win.top) {
    let dark = res['dark'];
    let domains = res['domains'];
    let url = new URL(window.location.href);
    let domain = url.hostname;

    if (domains) {
      domains = JSON.parse(domains);
    } else {
      domains = {};
    }

    if (domains[domain]) {
      localStorage.activeDarkGoogle = false;
    } else if (dark) {
      localStorage.activeDarkGoogle = dark;
    } else {
      localStorage.activeDarkGoogle = false;
    }
  }
});
var nn = document.getElementById('dark-theme');

if (!nn) {
  activateDark();
}

function activateDark() {
  var currentLoadedStyles = [];
  var styleDark = Object;
  var firstTemporaryStyle = Object;
  var arr = [];
  var mutationObserver = null;
  var inlineStyle = '';
  var stylenodes = ["STYLE", "LINK"];
  var stringStyle = ' html, body, table, thead, input, textarea, select {color: #bab5ab!important; background: #35393b;} input[type="text"], textarea, select {color: #bab5ab!important; background: #35393b;} [data-darksite-inline-background-image-gradient] {background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5))!important; -webkit-background-size: cover!important; -moz-background-size: cover!important; -o-background-size: cover!important; background-size: cover!important;} [data-darksite-force-inline-background] * {background-color: rgba(0,0,0,0.7)!important;} [data-darksite-inline-background] {background-color: rgba(0,0,0,0.7)!important;} [data-darksite-inline-color] {color: #fff!important;} [data-darksite-inline-background-image] {background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3))!important} .ytp-gradient-bottom{display: none!important}';
  var cssImportRegex = /@import (url\()?(('.+?')|(".+?")|([^\)]*?))\)?;?/g;
  var unparsableColors = ["inherit", "transparent", "initial", "currentcolor", "none"];

  window.onbeforeunload = function () {
    if (mutationObserver) {
      mutationObserver.disconnect();
    }
  };

  document.addEventListener("visibilitychange", function (evt) {
    if (document.visibilityState === 'visible' && window.self == window.top) {
      chrome.runtime.sendMessage({
        context: localStorage.activeDarkGoogle === 'true'
      }, function () {});
    }

    if (mutationObserver) {
      if (document.visibilityState === 'visible') {
        mutationObserver.observe(document.documentElement, {
          childList: true,
          subtree: true
        });
        load();
      } else {
        mutationObserver.disconnect();
      }
    }
  });

  if (window.self == window.top) {
    chrome.runtime.sendMessage({
      context: localStorage.activeDarkGoogle == 'true'
    });
  }

  createTemporaryStyle();

  var mmm = function mmm(mutations) {
    if (localStorage.activeDarkGoogle === 'true') {
      for (var j = 0; j < mutations.length; ++j) {
        var mutation = mutations[j];
        var styles = [];
        var node = mutation.target;

        if (node && node.nodeType == 1) {
          if ((styles = node.querySelectorAll('[style]')).length) {
            styles = Array.from(styles);
            styles.push(node);

            for (var prop in styles) {
              var _node = styles[prop];

              if (_node.style.cssText.indexOf('background-color') !== -1 && _node.style.cssText.indexOf('rgba(') == -1 && _node.style.cssText.indexOf('hsla(') == -1) {
                var backgroundColor = _node.style.backgroundColor;

                if (backgroundColor) {
                  var currentStyle = (0,_parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(backgroundColor);
                  var finishStyle = (0,_modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(currentStyle, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);
                  var stringFinishStyle = finishStyle.replace(/[^\dA-Za-z]/g, '');
                  var st = "data-darksite-inline-background-color" + stringFinishStyle;
                  var iL = addStyle(finishStyle + "!important", "background-color", "[" + st + "]");

                  if (iL) {
                    inlineStyle = inlineStyle + iL;
                    firstTemporaryStyle.innerText = firstTemporaryStyle.innerText + iL;
                  }

                  _node.setAttribute(st, "");
                }
              } else if (_node.style.cssText.indexOf('background-image') !== -1) {
                var backgroundImage = _node.style.backgroundImage;

                if (backgroundImage.indexOf('url(') !== -1 && backgroundImage.indexOf('linear-gradient(') == -1) {
                  _node.style.backgroundImage = backgroundImage; // node.style.backgroundBlendMode = 'multiply';

                  _node.style.filter = 'brightness(78%)';
                }
              } else if (_node.style.cssText.indexOf('background') !== -1 && _node.style.cssText.indexOf('rgba(') == -1 && _node.style.cssText.indexOf('hsla(') == -1) {
                var background = _node.style.background;

                if (background) {
                  var _currentStyle = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(background);

                  var _finishStyle = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(_currentStyle, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);

                  var _stringFinishStyle = _finishStyle.replace(/[^\dA-Za-z]/g, '');

                  var _st = "data-darksite-inline-background" + _stringFinishStyle;

                  var _iL = addStyle(_finishStyle + "!important", "background", "[" + _st + "]");

                  if (_iL) {
                    inlineStyle = inlineStyle + _iL;
                    firstTemporaryStyle.innerText = firstTemporaryStyle.innerText + _iL;
                  }

                  _node.setAttribute(_st, "");
                }
              }

              if (_node.style.cssText.indexOf('linear-gradient(') !== -1 && _node.style.cssText.indexOf('url(') == -1) {
                _node.setAttribute("data-darksite-inline-background-image", "");
              }

              if (_node.style.color) {
                var color = _node.style.color;

                if (color) {
                  var _currentStyle2 = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(color);

                  var _finishStyle2 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(_currentStyle2, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyFgHSL);

                  var _stringFinishStyle2 = _finishStyle2.replace(/[^\dA-Za-z]/g, '');

                  var _st2 = "data-darksite-inline-color" + _stringFinishStyle2;

                  var _iL2 = addStyle(_finishStyle2 + "!important", "color", "[" + _st2 + "]");

                  if (_iL2) {
                    inlineStyle = inlineStyle + _iL2;
                    firstTemporaryStyle.innerText = firstTemporaryStyle.innerText + _iL2;
                  }

                  _node.setAttribute(_st2, "");
                }
              }
            }
          }

          var _loop = function _loop(kk) {
            var node = mutation.addedNodes[kk];

            if (node && node.nodeType == 1) {
              var nodeName = node.nodeName.toUpperCase();

              if (stylenodes.indexOf(nodeName) !== -1) {
                try {
                  if (node.sheet && node.sheet.cssRules && currentLoadedStyles.indexOf(node.sheet) == -1 && node.id != 'dark-theme' && node.id != 'temporary-dark-theme') {
                    pushCurrentLoadedStyles(node.sheet);
                    var styleDarkText = interval(node.sheet.cssRules); //перебор всех стилей

                    styleDark = document.createElement('style');
                    styleDark.id = 'dark-theme';
                    styleDark.innerText = styleDarkText;
                    document.body.appendChild(styleDark);

                    if (node instanceof HTMLStyleElement) {
                      subscribeToSheetChanges(node.sheet, styleDark);
                    }
                  } else if (currentLoadedStyles.indexOf(node.sheet) == -1 && node.id != 'dark-theme' && node.id != 'temporary-dark-theme') {
                    node.addEventListener('load', function () {
                      try {
                        if (node.sheet && node.sheet.cssRules && currentLoadedStyles.indexOf(node.sheet) == -1) {
                          pushCurrentLoadedStyles(node.sheet);

                          var _styleDarkText = interval(node.sheet.cssRules); //загрузка и перебор всех стилей


                          styleDark = document.createElement('style');
                          styleDark.id = 'dark-theme';
                          styleDark.innerText = _styleDarkText;
                          document.body.appendChild(styleDark);
                        }
                      } catch (e) {
                        if (node.sheet.href && currentLoadedStyles.indexOf(node.sheet) == -1) {
                          pushCurrentLoadedStyles(node.sheet);
                          loadCssFile(node.sheet.href, node);
                        }
                      }
                    });
                  }
                } catch (e) {
                  if (node.sheet.href && currentLoadedStyles.indexOf(node.sheet) == -1 && node.id != 'dark-theme' && node.id != 'temporary-dark-theme') {
                    pushCurrentLoadedStyles(node.sheet);
                    loadCssFile(node.sheet.href, node);
                  }
                }
              }

              if (['SVG'].indexOf(nodeName) !== -1) {
                var fills = document.querySelectorAll("[fill]");

                for (var i = 0; i < fills.length; i++) {
                  var fill = fills[i].getAttribute("fill");

                  if (fill && fill.nodeName == 'text') {
                    var _currentStyle3 = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(fill);

                    var _finishStyle3 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(_currentStyle3, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyFgHSL);

                    fills[i].setAttribute("fill", _finishStyle3);
                  } else {
                    var _currentStyle4 = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(fill);

                    var _finishStyle4 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(_currentStyle4, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);

                    fills[i].setAttribute("fill", _finishStyle4);
                  }
                }

                var strokes = document.querySelectorAll("[stroke]");

                for (var _i = 0; _i < strokes.length; _i++) {
                  var stroke = strokes[_i].getAttribute("stroke");

                  if (stroke) {
                    var _currentStyle5 = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(stroke);

                    var _finishStyle5 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(_currentStyle5, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyFgHSL);

                    strokes[_i].setAttribute("stroke", _finishStyle5);
                  }
                }
              }
            }
          };

          for (var kk in mutation.addedNodes) {
            _loop(kk);
          }
        }
      }

      ;
    }
  };

  document.addEventListener("DOMContentLoaded", function () {
    var links = document.querySelectorAll('link[rel="stylesheet"]');
    var styles = document.getElementsByTagName('style');
    var sum = links.length + styles.length;

    if (localStorage.activeDarkGoogle === 'true') {
      var ii = setInterval(function () {
        if (document.body && !document.getElementById("temporary-dark-theme")) {
          firstTemporaryStyle = document.createElement('style');
          firstTemporaryStyle.id = 'temporary-dark-theme';
          firstTemporaryStyle.innerText = stringStyle;
          document.body.appendChild(firstTemporaryStyle);
          clearInterval(ii);
        }
      });
      setTimeout(function () {
        if (localStorage.activeDarkGoogle == undefined || localStorage.activeDarkGoogle === 'false') {
          if (mutationObserver) {
            mutationObserver.disconnect();
          }

          if (firstTemporaryStyle && firstTemporaryStyle.remove) {
            firstTemporaryStyle.remove();
          }
        }

        clearInterval(ii);
      }, 1500);

      for (var j = 0; j < document.styleSheets.length; ++j) {
        handlerSheet(document.styleSheets[j]);
      }

      loadImport();
      additionaLoad(document);
      mutationObserver = new MutationObserver(mmm);
      mutationObserver.observe(document.documentElement, {
        childList: true,
        subtree: true
      });
      var allNodes = document.getElementsByTagName('*');

      for (var i = 0; i < allNodes.length; i++) {
        if (allNodes[i].shadowRoot) {
          allNodes[i].style.background = "#35393b";
          allNodes[i].style.color = "#bab5ab";
        }
      }

      var cc = currentLoadedStyles.length;
      var aa = setInterval(function () {
        if (cc == currentLoadedStyles.length && currentLoadedStyles.length >= sum) {
          clearInterval(aa);
          firstTemporaryStyle.innerText = stringStyle + inlineStyle;
        }

        cc = currentLoadedStyles.length;
      }, 300);
      setTimeout(function () {
        firstTemporaryStyle.innerText = stringStyle + inlineStyle;
        clearInterval(aa);
      }, 3500);
    }

    setTimeout(function () {
      if (firstTemporaryStyle && firstTemporaryStyle.remove) {
        if (localStorage.activeDarkGoogle === 'false') {
          firstTemporaryStyle.remove();
          const boxes = document.querySelectorAll('#dark-theme');
          boxes.forEach(box => {
            box.remove();
          });
        }
      }
    }, 2000);

    if (window.self == window.top) {
      window.onmessage = function (e) {
        if (e.data == 'active') {
          if (localStorage.activeDarkGoogle === 'true') {
            e.source.postMessage('activeDarkSiteTrue', '*');
          } else {
            e.source.postMessage('activeDarkSiteFalse', '*');
          }
        }
      };
    } else {
      window.top.postMessage('active', '*');

      window.onmessage = function (e) {
        if (e.data == 'activeDarkSiteTrue') {
          localStorage.activeDarkGoogle = true;
        } else if (e.data == 'activeDarkSiteFalse') {
          localStorage.activeDarkGoogle = false;
        }
      };

      window.onbeforeunload = function () {
        window.top.postMessage('active', '*');
      };
    }
  });
  window.addEventListener("load", load);

  function load() {
    if (localStorage.activeDarkGoogle == 'true') {
      for (var j = 0; j < document.styleSheets.length; ++j) {
        handlerSheet(document.styleSheets[j]);
      }

      loadImport();
      additionaLoad(document);
    }
  }

  function handlerSheet(sheet) {
    try {
      if (sheet.cssRules && sheet.cssRules.length > 0 && currentLoadedStyles.indexOf(sheet) == -1 && sheet.ownerNode.id != 'dark-theme' && sheet.ownerNode.id != 'temporary-dark-theme') {
        pushCurrentLoadedStyles(sheet);
        var styleDarkText = interval(sheet.cssRules);
        styleDark = document.createElement('style');
        styleDark.id = 'dark-theme';
        styleDark.innerText = styleDarkText;
        document.body.appendChild(styleDark);

        if (sheet.ownerNode instanceof HTMLStyleElement) {
          subscribeToSheetChanges(sheet, styleDark);
        }
      }
    } catch (e) {
      if (sheet.href && currentLoadedStyles.indexOf(sheet) == -1) {
        pushCurrentLoadedStyles(sheet);
        loadCssFile(sheet.href, sheet.ownerNode);
      }
    }
  }

  function interval(rules) {
    // по всем правилам
    var finalString = '';

    if (rules && rules.length) {
      for (var k = 0; k < rules.length; k++) {
        if (rules[k] instanceof CSSMediaRule && rules[k].type == 4 && rules[k].conditionText == 'not all') {} else {
          try {
            if (rules[k] instanceof CSSImportRule && rules[k].styleSheet && rules[k].styleSheet.cssRules) {
              finalString = finalString + interval(rules[k].styleSheet.cssRules);
            } else {
              finalString = finalString + addNewRule(rules[k]);
            }
          } catch (e) {
            console.log(e);
          }
        }
      }
    }

    return finalString;
  }

  function subscribeToSheetChanges(element, styleDark) {
    var length = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 1;

    var callb = function callb() {
      if (element.cssRules.length != length) {
        var cssText = styleDark.innerText;

        for (var k = length - 1; k < element.cssRules.length - 1; k++) {
          cssText = cssText + addNewRule(element.cssRules[k]);
        }

        length = element.cssRules.length;
        styleDark.innerText = cssText;
      }

      requestAnimationFrame(callb);
    };

    callb();
  }

  function loadImport() {
    var docs = document.querySelectorAll('link[rel="import"]');
    var finalString = '';
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
      for (var _iterator = docs[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
        var i = _step.value;
        var doc = i.import;

        for (var j = 0; j < doc.styleSheets.length; ++j) {
          try {
            if (doc.styleSheets[j].cssRules && doc.styleSheets[j].cssRules.length > 0 && currentLoadedStyles.indexOf(doc.styleSheets[j]) == -1 && doc.styleSheets[j].ownerNode.id != 'dark-theme' && doc.styleSheets[j].ownerNode.id != 'temporary-dark-theme') {
              pushCurrentLoadedStyles(doc.styleSheets[j]);

              for (var k = 0; k < doc.styleSheets[j].cssRules.length; k++) {
                finalString = finalString + addNewRule(doc.styleSheets[j].cssRules[k]);
              }

              styleDark = document.createElement('style');
              styleDark.id = 'dark-theme';
              styleDark.innerText = finalString;
              document.body.appendChild(styleDark);
            }
          } catch (e) {
            if (doc.styleSheets[j].href && currentLoadedStyles.indexOf(doc.styleSheets[j]) == -1) {
              pushCurrentLoadedStyles(doc.styleSheets[j]);
              loadCssFile(doc.styleSheets[j].href, doc);
            }
          }
        }
      }
    } catch (err) {
      _didIteratorError = true;
      _iteratorError = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion && _iterator.return) {
          _iterator.return();
        }
      } finally {
        if (_didIteratorError) {
          throw _iteratorError;
        }
      }
    }
  }

  function additionaLoad(dom) {
    if (document.body && localStorage.activeDarkGoogle === 'true') {
      var bgcolors = dom.querySelectorAll("[bgcolor]");

      for (var i = 0; i < bgcolors.length; i++) {
        var bgcolor = bgcolors[i].getAttribute("bgcolor");

        if (bgcolor) {
          var currentStyle = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(bgcolor);
          var finishStyle = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(currentStyle, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);
          bgcolors[i].setAttribute("bgcolor", finishStyle);
        }
      }

      var colors = dom.querySelectorAll("[color]");

      for (var _i2 = 0; _i2 < colors.length; _i2++) {
        var color = colors[_i2].getAttribute("color");

        if (color) {
          var _currentStyle6 = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(color);

          var _finishStyle6 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(_currentStyle6, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyFgHSL);

          colors[_i2].setAttribute("color", _finishStyle6);
        }
      }

      var styles = dom.querySelectorAll("[style]");

      for (var _i3 = 0; _i3 < styles.length; _i3++) {
        addNewStyle(styles[_i3].style, styles[_i3]);
      }

      var images = dom.querySelectorAll("img");

      for (var _i4 = 0; _i4 < images.length; _i4++) {
        var img = images[_i4];
        var screenWidth = window.screen.width / 3;

        if (img) {
          if (img.offsetWidth > screenWidth) {
            img.style.filter = 'brightness(83%)';
          }
        }
      }
    }
  }

  function addNewStyle(sty, st) {
    var endString = '';

    if (sty && sty.cssText.indexOf('background') !== -1) {
      if (sty.backgroundImage && sty.backgroundImage.indexOf('data:image/png') == -1 && sty.backgroundImage.indexOf('data:image/svg+xml') == -1) {
        if (sty.backgroundRepeatX == 'repeat' || sty.backgroundRepeatY == 'repeat' || sty.backgroundRepeat == 'repeat') {
          if (sty.backgroundImage.match(_modify__WEBPACK_IMPORTED_MODULE_0__.colorMatch)) {
            var start = sty.backgroundImage.trim();
            var finish = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(start, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);

            if (start != finish) {
              if (sty.getPropertyPriority('background-image') || sty.background) {
                endString = endString + addStyle(finish + '!important', 'background-image', st);
              } else {
                endString = endString + addStyle(finish, 'background-image', st);
              }
            }
          } else {
            endString = endString + addStyle('rgba(53,57,59,0.5)', 'background', st);
          }
        } else {
          var _start = sty.backgroundImage.trim();

          if (_start.indexOf('url(') !== -1 && _start.indexOf('linear-gradient(') == -1 && _start.indexOf('.svg') == -1 && _start.indexOf('.png') == -1) {
            endString = endString + addStyle(_start, 'background-image', st); // endString = endString + addStyle('rgb(0, 0, 0, 0.5)', 'background-color', st);

            endString = endString + addStyle('brightness(83%)', 'filter', st);
          } else {
            var _finish = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);

            if (_start != _finish) {
              if (sty.getPropertyPriority('background-image') || sty.background) {
                endString = endString + addStyle(_finish + '!important', 'background-image', st);
              } else {
                endString = endString + addStyle(_finish, 'background-image', st);
              }
            } else if (_finish == 'none') {
              endString = endString + addStyle(_finish, 'background-image', st);
            } else if (sty.backgroundImage.indexOf('.gif') !== -1) {
              endString = endString + addStyle('none', 'background-image', st);
            }
          }
        }
      }

      if (sty.backgroundColor) {
        var _start2 = sty.backgroundColor.trim();

        if (_start2) {
          var _finish2 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start2, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);

          if (_finish2 == '(' || _finish2 == ')' || _finish2 == '') {
            endString = endString + addStyle('rgba(53,57,59,0.5)', 'background-color', st);
          } else if (_start2 != _finish2) {
            if (sty.backgroundImage && sty.backgroundImage.indexOf('url(') !== -1 && sty.backgroundImage.indexOf('.png') == -1 && sty.backgroundImage.indexOf('data:image/png') == -1 && sty.backgroundImage.indexOf('data:image/svg+xml') == -1) {
              if (sty.getPropertyPriority('background-color') || sty.background) {
                endString = endString + addStyle(_finish2 + '!important', 'background', st);
              } else {
                endString = endString + addStyle(_finish2, 'background', st);
              }
            } else if (sty.getPropertyPriority('background-color') || sty.background) {
              endString = endString + addStyle(_finish2 + '!important', 'background-color', st);
            } else {
              endString = endString + addStyle(_finish2, 'background-color', st);
            }

            if (sty.backgroundImage) {
              // endString = endString + addStyle('rgb(0, 0, 0, 0.5)', 'background-color', st);
              endString = endString + addStyle('multiply', 'background-blend-mode', st);
            }
          }
        }
      }

      if (sty.background && (sty.backgroundImage == '' || sty.backgroundImage == 'initial') && (sty.backgroundColor == '' || sty.backgroundColor == 'initial')) {
        if (sty.background.indexOf('url(') !== -1) {
          if (sty.background.indexOf('data:image/svg+xml') == -1) {} else {
            var sed = sty.background.match(_modify__WEBPACK_IMPORTED_MODULE_0__.colorMatch);

            if (sed) {
              var col = (0, _parsers__WEBPACK_IMPORTED_MODULE_1__.parse)(sed[0]);
              var color = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyColor)(col, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);
              endString = endString + addStyle(color + '!important', 'background', st);
            }
          }
        } else {
          var _start3 = sty.background.trim();

          if (_start3) {
            var _finish3 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start3, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL, st);

            if (_finish3 == '(' || _finish3 == ')' || _finish3 == '') {
              endString = endString + addStyle('rgba(53,57,59,0.5)', 'background', st);
            } else if (_start3 != _finish3) {
              if (sty.getPropertyPriority('background')) {
                endString = endString + addStyle(_finish3 + '!important', 'background', st);
              } else {
                endString = endString + addStyle(_finish3, 'background', st);
              }
            }
          }
        }
      } else {
        var _start4 = sty.background.trim();

        if (_start4) {
          var _finish4 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start4, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBgHSL);

          if (_start4 != _finish4) {
            if (sty.getPropertyPriority('background')) {
              endString = endString + addStyle(_finish4 + '!important', 'background', st);
            } else {
              endString = endString + addStyle(_finish4, 'background-color', st);
            }
          }
        }
      }
    }

    if (sty && sty.cssText.indexOf('border') !== -1) {
      if (sty.borderColor && unparsableColors.indexOf(sty.borderColor) == -1) {
        var _start5 = sty.borderColor.trim();

        if (_start5) {
          var _finish5 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start5, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

          if (_start5 != _finish5) {
            if (sty.getPropertyPriority('border-color')) {
              endString = endString + addStyle(_finish5 + '!important', 'border-color', st);
            } else {
              endString = endString + addStyle(_finish5, 'border-color', st);
            }
          }
        }
      }

      if (sty.border && unparsableColors.indexOf(sty.border) == -1) {
        var _start6 = sty.border.trim();

        if (_start6) {
          var _finish6 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start6, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

          if (_start6 != _finish6) {
            if (sty.getPropertyPriority('border')) {
              endString = endString + addStyle(_finish6 + '!important', 'border', st);
            } else {
              endString = endString + addStyle(_finish6, 'border', st);
            }
          }
        }
      }

      if (sty.borderBottom && unparsableColors.indexOf(sty.borderBottom) == -1) {
        var _start7 = sty.borderBottom.trim();

        if (_start7) {
          var _finish7 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start7, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

          if (_start7 != _finish7) {
            if (sty.getPropertyPriority('border-bottom')) {
              endString = endString + addStyle(_finish7 + '!important', 'border-bottom', st);
            } else {
              endString = endString + addStyle(_finish7, 'border-bottom', st);
            }
          }
        }
      }

      if (sty.borderTop && unparsableColors.indexOf(sty.borderTop) == -1) {
        var _start8 = sty.borderTop.trim();

        if (_start8) {
          var _finish8 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start8, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

          if (_start8 != _finish8) {
            if (sty.getPropertyPriority('border-top')) {
              endString = endString + addStyle(_finish8 + '!important', 'border-top', st);
            } else {
              endString = endString + addStyle(_finish8, 'border-top', st);
            }
          }
        }
      }

      if (sty.borderLeft && unparsableColors.indexOf(sty.borderLeft) == -1) {
        var _start9 = sty.borderLeft.trim();

        if (_start9) {
          var _finish9 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start9, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

          if (_start9 != _finish9) {
            if (sty.getPropertyPriority('border-left')) {
              endString = endString + addStyle(_finish9 + '!important', 'border-left', st);
            } else {
              endString = endString + addStyle(_finish9, 'border-left', st);
            }
          }
        }
      }

      if (sty.borderRight && unparsableColors.indexOf(sty.borderRight) == -1) {
        var _start10 = sty.borderRight.trim();

        if (_start10) {
          var _finish10 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start10, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

          if (_start10 != _finish10) {
            if (sty.getPropertyPriority('border-right')) {
              endString = endString + addStyle(_finish10 + '!important', 'border-right', st);
            } else {
              endString = endString + addStyle(_finish10, 'border-right', st);
            }
          }
        }
      }
    }

    if (sty && sty.outline && unparsableColors.indexOf(sty.outline) == -1) {
      var _start11 = sty.outline.trim();

      if (_start11) {
        var _finish11 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start11, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

        if (_start11 != _finish11) {
          if (sty.getPropertyPriority('outline')) {
            endString = endString + addStyle(_finish11 + '!important', 'outline', st);
          } else {
            endString = endString + addStyle(_finish11, 'outline', st);
          }
        }
      }
    }

    if (sty && sty.boxShadow && unparsableColors.indexOf(sty.boxShadow) == -1) {
      var _start12 = sty.boxShadow.trim();

      if (_start12) {
        var _finish12 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start12, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

        if (_start12 != _finish12) {
          if (sty.getPropertyPriority('box-shadow')) {
            endString = endString + addStyle(_finish12 + '!important', 'box-shadow', st);
          } else {
            endString = endString + addStyle(_finish12, 'box-shadow', st);
          }
        }
      }
    }

    if (sty && sty.textShadow && unparsableColors.indexOf(sty.textShadow) == -1) {
      var _start13 = sty.textShadow.trim();

      if (_start13) {
        var _finish13 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start13, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyBorderHSL);

        if (_start13 != _finish13) {
          if (sty.getPropertyPriority('text-shadow')) {
            endString = endString + addStyle(_finish13 + '!important', 'text-shadow', st);
          } else {
            endString = endString + addStyle(_finish13, 'text-shadow', st);
          }
        }
      }
    }

    if (sty && sty.color && unparsableColors.indexOf(sty.color) == -1) {
      var _start14 = sty.color.trim();

      if (_start14 && st != '*, ::before, ::after') {
        var _finish14 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start14, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyFgHSL);

        if (_finish14 == '(' || _finish14 == ')' || _finish14 == '') {
          endString = endString + addStyle('#bab5ab', 'color', st);
        } else if (_start14 != _finish14) {
          if (sty.getPropertyPriority('color')) {
            endString = endString + addStyle(_finish14 + '!important', 'color', st);
          } else {
            endString = endString + addStyle(_finish14, 'color', st);
          }
        }
      }
    }

    if (sty && sty.fill && unparsableColors.indexOf(sty.fill) == -1) {
      var _start15 = sty.fill.trim();

      var _finish15 = (0, _modify__WEBPACK_IMPORTED_MODULE_0__.findAndReplaceColor)(_start15, _modify__WEBPACK_IMPORTED_MODULE_0__.modifyFgHSL);

      if (_start15 != _finish15) {
        if (sty.getPropertyPriority('fill')) {
          endString = endString + addStyle(_finish15 + '!important', 'fill', st);
        } else {
          endString = endString + addStyle(_finish15, 'fill', st);
        }
      }
    }

    return endString;
  }

  function addNewRule(rule) {
    if (rule && rule.selectorText == undefined && rule.cssRules) {
      var lll = '';

      for (var kk = 0; kk < rule.cssRules.length; kk++) {
        var sty = rule.cssRules[kk].style;
        var st = rule.cssRules[kk].selectorText;
        var ttt = addNewStyle(sty, st);

        if (ttt != undefined) {
          lll = lll + ttt;
        }
      }

      return lll;
    } else if (rule) {
      var _lll = '';
      var _sty = rule.style;
      var _st3 = rule.selectorText;

      var _ttt = addNewStyle(_sty, _st3);

      if (_ttt != undefined) {
        _lll = _ttt;
      }

      return _lll;
    }
  }

  function addStyle(finishStyle, styleName, st) {
    if (typeof st === 'string') {
      var str = ' ' + st + ' {' + styleName + ':' + finishStyle + ';}';

      if (arr[str] == undefined) {
        arr[str] = ' ';
        return str;
      }
    } else if (st) {
      st.style[styleName] = finishStyle;
    }

    return '';
  }

  function createTemporaryStyle() {
    var stringStyle = 'html, body, input, textarea, select, body *, html *, table *, thead *, div, *:before, *:after, *:active {color: #bab5ab!important; background: #35393b!important; background-color: #35393b!important;} input[type="text"], textarea, select {color: #bab5ab!important; background: #35393b;}';

    if (localStorage.activeDarkGoogle === 'true') {
      if (!document.getElementById("temporary-dark-theme")) {
        firstTemporaryStyle = document.createElement('style');
        firstTemporaryStyle.id = 'temporary-dark-theme';
        firstTemporaryStyle.innerText = stringStyle;
        document.documentElement.appendChild(firstTemporaryStyle);
      }

      var ii = setInterval(function () {
        if (document.body && !document.body.querySelector("#temporary-dark-theme")) {
          document.body.appendChild(firstTemporaryStyle);
          clearInterval(ii);
        }
      });
      setTimeout(function () {
        clearInterval(ii);
      }, 1000);
    }
  }

  function loadCssFile(href, node) {
    if (href && node) {
      var data = {
        url: href,
        responseType: "text",
        mimeType: "text/css",
        origin: window.location.origin
      };
      chrome.runtime.sendMessage({
        type: "fetch",
        data: data
      });
    }
  }

  chrome.runtime.onMessage.addListener(function (_ref, sender, sendResponse) {
    var type = _ref.type,
        response = _ref.response,
        href = _ref.href;

    if (type === "fetch-response") {
      var data = response.trim().replace(cssImportRegex, '');
      var newStyleSync = createCssSync(href);
      newStyleSync.textContent = data;
      var styleDarkText = interval(newStyleSync.sheet.cssRules); //загрузка и перебор всех стилей

      styleDark = document.createElement('style');
      styleDark.id = 'dark-theme';
      styleDark.innerText = styleDarkText;
      document.body.appendChild(styleDark);

      try {
        newStyleSync.remove();
      } catch (e) {
        console.log('Error load', e);
      }
    }

    sendResponse();
  });

  function pushCurrentLoadedStyles(item) {
    currentLoadedStyles.push(item);
  }

  function createCssSync(href) {
    var styleSync = document.createElement('style');
    styleSync.id = href;
    document.head.appendChild(styleSync);
    return styleSync;
  }
}
})();

/******/ })()
;
//# sourceMappingURL=dark.js.map