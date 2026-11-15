/**
 * "Trusted by" marquee: exactly the 35 brands listed on citixmena.com (CLAUDE.md), with their official logos.
 * Source: the official citixmena.com logo grid `Logos.svg` (1046 × 447, 7 × 5, same order as below), downloaded
 * 15 Nov 2026 (see media/brand/_download_2026-11-15/SOURCE.md) and served as /media/brand/trusted-logos.svg.
 * Each logo is shown through a CSS window onto that file: `box` = [x, y, width, height] of the logo in SVG units,
 * measured from the file. Nothing is traced or redrawn. Do NOT add Porsche, Ferrari or Mercedes.
 */
export const LOGO_SPRITE = { src: "/media/brand/trusted-logos.svg", width: 1046, height: 447 } as const;

export const trustedBrands: { name: string; box: [number, number, number, number] }[] = [
  { name: "Sony", box: [8.5, 16, 81.5, 15] },
  { name: "Kia", box: [170, 15, 74, 17] },
  { name: "Panasonic", box: [314, 16, 99.5, 15.5] },
  { name: "Yokohama", box: [469.5, 16, 105.5, 15] },
  { name: "Apple", box: [663, 4, 33, 39] },
  { name: "L'Oréal", box: [792, 15, 90.5, 17] },
  { name: "Rolex", box: [959.5, 3.5, 70.5, 40] },
  { name: "McDonald's", box: [23, 99.5, 53, 46] },
  { name: "Tiffany & Co.", box: [151, 115.5, 112, 14] },
  { name: "Coca-Cola", box: [326, 109.5, 77, 25.5] },
  { name: "Lenovo", box: [476.5, 113, 91, 19] },
  { name: "Lexus", box: [633.5, 114.5, 92, 16] },
  { name: "Lufthansa", box: [780, 112.5, 114.5, 20] },
  { name: "Bridgestone", box: [944, 116, 101.5, 13] },
  { name: "Ülker", box: [9, 209, 81, 25] },
  { name: "Mondelēz International", box: [159.5, 210, 94.5, 23] },
  { name: "BMW", box: [339.5, 196.5, 50, 50] },
  { name: "Red Bull", box: [488, 202, 68, 39.5] },
  { name: "Kinder", box: [641, 209.5, 77.5, 24.5] },
  { name: "Michelin", box: [796.5, 200.5, 81.5, 37] },
  { name: "Volvo", box: [945, 214.5, 99.5, 14] },
  { name: "H&M", box: [21.5, 302, 55.5, 37] },
  { name: "Kenzo", box: [168.5, 311.5, 76.5, 18.5] },
  { name: "Sprite", box: [326.5, 293.5, 76, 54.5] },
  { name: "Audi", box: [488, 308.5, 68.5, 24.5] },
  { name: "Hyundai", box: [630, 314, 99.5, 13] },
  { name: "Samsung", box: [791, 305, 92.5, 31] },
  { name: "Xiaomi", box: [972.5, 298.5, 44, 44] },
  { name: "Bosch", box: [0, 408.5, 99, 22] },
  { name: "Pandora", box: [155.5, 409, 102.5, 21.5] },
  { name: "KFC", box: [324.5, 407, 78.5, 25] },
  { name: "Unilever", box: [498, 393, 48, 53.5] },
  { name: "Lancôme", box: [628.5, 407, 102, 25] },
  { name: "Visa", box: [807, 408, 69.5, 23] },
  { name: "P&G", box: [968, 408, 53.5, 23.5] },
];

/** CSS for one logo cell of `cellW` × `cellH` px: the logo scaled to fit (with a small margin) and centred. */
export function logoStyle([x, y, w, h]: [number, number, number, number], cellW = 90, cellH = 40) {
  const s = Math.min(cellW / w, cellH / h) * 0.9;
  const px = (n: number) => `${Math.round(n * 100) / 100}px`;
  return {
    backgroundImage: `url(${LOGO_SPRITE.src})`,
    backgroundSize: `${px(LOGO_SPRITE.width * s)} ${px(LOGO_SPRITE.height * s)}`,
    backgroundPosition: `${px((cellW - w * s) / 2 - x * s)} ${px((cellH - h * s) / 2 - y * s)}`,
  };
}
