import { loadFont } from '@remotion/fonts';
import { brand } from './linkeddy.config';

// Los archivos se importan como módulos para que funcionen igual en el
// render de Remotion (webpack) y en el Motion Studio (Vite).
import display400 from './fonts/familjen-grotesk-latin-400-normal.woff2';
import display500 from './fonts/familjen-grotesk-latin-500-normal.woff2';
import display600 from './fonts/familjen-grotesk-latin-600-normal.woff2';
import display700 from './fonts/familjen-grotesk-latin-700-normal.woff2';
import serif400 from './fonts/instrument-serif-latin-400-normal.woff2';
import serif400i from './fonts/instrument-serif-latin-400-italic.woff2';
import mono400 from './fonts/dm-mono-latin-400-normal.woff2';
import mono500 from './fonts/dm-mono-latin-500-normal.woff2';

const faces = [
  { family: brand.fonts.display, url: display400, weight: '400' },
  { family: brand.fonts.display, url: display500, weight: '500' },
  { family: brand.fonts.display, url: display600, weight: '600' },
  { family: brand.fonts.display, url: display700, weight: '700' },
  { family: brand.fonts.serif, url: serif400, weight: '400' },
  { family: brand.fonts.serif, url: serif400i, weight: '400', style: 'italic' },
  { family: brand.fonts.mono, url: mono400, weight: '400' },
  { family: brand.fonts.mono, url: mono500, weight: '500' },
];

let started = false;
export const loadBrandFonts = () => {
  if (started) return;
  started = true;
  for (const f of faces) {
    loadFont({ ...f, format: 'woff2' }).catch((err) => {
      console.error(`No se pudo cargar ${f.family} ${f.weight}`, err);
    });
  }
};
