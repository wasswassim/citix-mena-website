"use client";

import { useEffect, useId, useRef, useState } from "react";

/**
 * Projects tunnel (Wassim, 17 Nov 2026): the idea of the bluesqx "experience" section (cards floating towards you
 * as you scroll), built on the 21st.dev "Perspective Tunnel Hero" by daiwiikharihar
 * (https://21st.dev/r/daiwiikharihar/perspective-tunnel-hero) and rebuilt here without framer-motion or Tailwind.
 * Kept from it: the golden-angle layout, the staggered fly-through from far Z to past the camera, the fade curve,
 * the pointer parallax and the depth rings. Changed: the page scrolls normally (a tall section with a sticky
 * stage drives the progress) instead of the component swallowing the mouse wheel, brand colours, and the cards
 * carry real projects from the company deck (media/source/projects/SOURCE.md).
 *
 * Without JavaScript or with reduced motion the cards stay a plain grid (the default CSS); the script adds
 * .is-3d only when the motion should play. All text is real HTML. The loop runs only while the section is on
 * screen and stops once the motion has settled.
 *
 * End (Wassim, 18 Nov 2026): instead of fading out, the heading becomes a camera target, as in the 21st.dev
 * "Glyph Portal" by Christian Katzmann (MIT): the camera dives into a letter near the middle of the phrase until
 * its white fills the screen, which then hands over to a plain white layer (the page continues on white).
 */
type Card = { place: string; title: string; text: string; alt: string };
type Props = { eyebrow: string; title: string; sub: string; hint: string; cards: Card[] };

const M = "/media/projects/";
// Must follow projects.cards in lib/i18n.ts (EN and AR, same order). A missing image falls back to the first.
const IMAGES = [
  "sharjah-skyline.webp",
  "jumbo.webp",
  "majaz-heera.webp",
  "saltanat-light.webp",
  "al-mamsha.webp",
  "baloo.webp",
  "06-mall.webp",
  "tom.webp",
  "chamber.webp",
];

const GOLDEN = 137.5 * (Math.PI / 180);
const SPAN = 0.55; // share of the scroll each card spends flying (21st.dev value)

type Layout = { cos: number; sin: number; rx: number; ry: number; rz: number };
const layout = (i: number): Layout => ({
  cos: Math.cos(i * GOLDEN),
  sin: Math.sin(i * GOLDEN),
  rx: 0.28 + (i % 3) * 0.08,
  ry: 0.26 + (i % 2) * 0.09,
  rz: (i % 2 === 0 ? 1 : -1) * (3 + (i % 5) * 2),
});

const clamp01 = (v: number) => (v < 0 ? 0 : v > 1 ? 1 : v);
// opacity over a card's own flight: in over the first 18 %, out over the last 18 % (21st.dev curve)
const fade = (t: number) => (t <= 0 ? 0 : t < 0.18 ? t / 0.18 : t <= 0.82 ? 1 : t < 0.98 ? 1 - (t - 0.82) / 0.16 : 0);
const smooth = (a: number, b: number, v: number) => {
  const t = clamp01((v - a) / (b - a));
  return t * t * (3 - 2 * t);
};
const easeInOutCubic = (t: number) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2);

// Scroll split (Wassim, 18 Nov 2026): the cards fly over the first 70 %, then the camera dives into one letter of
// the heading near its middle until that letter's white fills the screen, which becomes the white page.
const CARDS_END = 0.7;
const ZOOM_START = 0.72;
const ZOOM_END = 0.98; // HowWeWork's overlap (globals.css) is tuned to this split: keep them in step
const HEAD_SCALE_END = 1.15; // the heading's slow growth during the fly-through ends here

/**
 * Where to dive: the centre of the thickest patch of ink in a letter near the middle of the heading, in viewport
 * pixels, with the radius of the ink disk there. The largest-opaque-square scan is adapted from Glyph Portal
 * (© 2026 Christian Katzmann, MIT, https://21st.dev): here each word is drawn whole, so Arabic letters keep their
 * joined shapes, and each letter is searched only inside its own slice of the word.
 */
type Ink = { x: number; y: number; r: number };
const SS = 2; // supersampling of the scan
function findInk(title: HTMLElement): Ink | null {
  const node = title.firstChild;
  if (!(node instanceof Text)) return null;
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  if (!ctx) return null;
  const cs = getComputedStyle(title);
  const font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
  const range = document.createRange();
  const box = title.getBoundingClientRect();
  const found: Ink[] = [];
  const pad = 6;
  for (const m of node.data.matchAll(/\S+/g)) {
    const i0 = m.index ?? 0;
    range.setStart(node, i0);
    range.setEnd(node, i0 + m[0].length);
    const wr = range.getClientRects()[0];
    if (!wr || !wr.width) continue;
    canvas.width = Math.ceil(wr.width * SS) + pad * 2;
    canvas.height = Math.ceil(wr.height * SS) + pad * 2;
    const { width, height } = canvas;
    ctx.font = font;
    ctx.direction = cs.direction === "rtl" ? "rtl" : "ltr";
    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";
    if ("letterSpacing" in ctx) ctx.letterSpacing = cs.letterSpacing === "normal" ? "0px" : cs.letterSpacing;
    const fm = ctx.measureText(m[0]);
    const asc = fm.fontBoundingBoxAscent;
    const baseline = (wr.height - (asc + fm.fontBoundingBoxDescent)) / 2 + asc;
    // stretch to the DOM word width, so the drawing matches the letter columns even where canvas letterSpacing
    // is unsupported
    const fit = fm.width > 0 ? wr.width / fm.width : 1;
    ctx.setTransform(SS * (fit > 0.8 && fit < 1.25 ? fit : 1), 0, 0, SS, pad, pad);
    ctx.fillText(m[0], 0, baseline);
    // which letter each canvas column belongs to
    const owner = new Int16Array(width).fill(-1);
    const letters = m[0].length;
    for (let k = 0; k < letters; k++) {
      range.setStart(node, i0 + k);
      range.setEnd(node, i0 + k + 1);
      const cr = range.getBoundingClientRect();
      if (cr.width < 1) continue; // joining marks and the like own no column
      const a = Math.max(0, Math.floor((cr.left - wr.left) * SS + pad));
      const b = Math.min(width, Math.ceil((cr.right - wr.left) * SS + pad));
      for (let x = a; x < b; x++) owner[x] = k;
    }
    const px = ctx.getImageData(0, 0, width, height).data;
    const rows = new Uint16Array(width + 1);
    const best = Array.from({ length: letters }, () => ({ s: 0, x: 0, y: 0 }));
    for (let y = 0; y < height; y++) {
      let diag = 0;
      for (let x = 0; x < width; x++) {
        const above = rows[x + 1];
        rows[x + 1] = px[(y * width + x) * 4 + 3] > 245 ? Math.min(above, rows[x], diag) + 1 : 0;
        diag = above;
        const s = rows[x + 1];
        if (s < 3) continue;
        const k = owner[Math.floor(x + 1 - s / 2)];
        if (k >= 0 && s > best[k].s) best[k] = { s, x, y };
      }
    }
    for (const q of best) {
      if (q.s < 2 * SS * 2 + 2) continue; // ink thinner than about 4 px is not worth diving into
      found.push({
        x: wr.left + (q.x + 1 - q.s / 2 - pad) / SS,
        y: wr.top + (q.y + 1 - q.s / 2 - pad) / SS,
        r: (q.s / 2 - 1) / SS,
      });
    }
  }
  if (!found.length) return null;
  // among the letters with thick enough ink, the one closest to the middle of the heading
  const maxR = Math.max(...found.map((f) => f.r));
  const cx = box.left + box.width / 2;
  const cy = box.top + box.height / 2;
  return found
    .filter((f) => f.r >= maxR * 0.6)
    .sort((a, b) => Math.hypot(a.x - cx, a.y - cy) - Math.hypot(b.x - cx, b.y - cy))[0];
}

export default function ProjectTunnel({ eyebrow, title, sub, hint, cards }: Props) {
  const sectionRef = useRef<HTMLElement>(null);
  const titleRef = useRef<HTMLDivElement>(null);
  const hintRef = useRef<HTMLParagraphElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const stickyRef = useRef<HTMLDivElement>(null);
  const whiteRef = useRef<HTMLDivElement>(null);
  const cardRefs = useRef<(HTMLLIElement | null)[]>([]);
  const [is3d, setIs3d] = useState(false);
  const titleId = useId();

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    // the 3D layout itself is switched on before paint by html[data-motion="ok"] (lib/loader.ts), so the tall
    // section never jumps in after hydration; this keeps the flag in step if the setting changes later
    const sync = () => {
      setIs3d(!mq.matches);
      if (mq.matches) delete document.documentElement.dataset.motion;
      else document.documentElement.dataset.motion = "ok";
    };
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);

  useEffect(() => {
    const section = sectionRef.current;
    if (!is3d || !section) return;
    const total = cards.length;
    const L = cards.map((_, i) => layout(i));

    let target = 0;
    let prog = 0;
    let px = 0,
      py = 0,
      tx = 0,
      ty = 0;
    let w = window.innerWidth,
      h = window.innerHeight;
    let raf = 0;
    let last = 0;
    let onScreen = false;

    const measure = () => {
      const r = section.getBoundingClientRect();
      const run = r.height - h;
      target = run > 0 ? clamp01(-r.top / run) : 0;
    };

    // Geometry for the dive, in the sticky stage's own pixels, measured with the heading untransformed.
    let geo: { hx: number; hy: number; hw: number; hh: number; ink: Ink | null; sw: number; sh: number } | null =
      null;
    const measureInk = () => {
      const head = titleRef.current;
      const heading = headingRef.current;
      const stage = stickyRef.current;
      if (!head || !heading || !stage) return;
      const saved = head.style.transform;
      head.style.transform = "none";
      const s = stage.getBoundingClientRect();
      const hr = head.getBoundingClientRect();
      const ink = findInk(heading);
      head.style.transform = saved;
      geo = {
        hx: hr.left - s.left,
        hy: hr.top - s.top,
        hw: hr.width,
        hh: hr.height,
        ink: ink && { x: ink.x - s.left, y: ink.y - s.top, r: ink.r },
        sw: stage.clientWidth,
        sh: stage.clientHeight,
      };
    };

    const renderHead = () => {
      const head = titleRef.current;
      if (!head) return;
      const cp = clamp01(prog / CARDS_END);
      // the heading grows slowly as you travel and stays readable behind the cards
      const base = cp < 0.5 ? 0.82 + cp * 0.36 : 1 + (cp - 0.5) * 0.3;
      const zt = clamp01((prog - ZOOM_START) / (ZOOM_END - ZOOM_START));
      // eyebrow and sub fade out, and the heading's gradient turns solid white, so the letter is pure #fff
      head.style.setProperty("--tz", smooth(0, 0.25, zt).toFixed(3));
      const ink = geo?.ink;
      if (!geo || !ink || zt <= 0) {
        head.style.transform = `scale(${base.toFixed(4)})`;
        head.style.opacity = "";
        if (whiteRef.current) whiteRef.current.style.opacity = !ink && zt > 0 ? zt.toFixed(3) : "0";
        return;
      }
      // Camera dive (after Glyph Portal): the scale grows on a log curve from the end of the fly-through to the
      // point where the ink disk round the focus covers the screen diagonal, while the focus slides to the centre.
      const e = easeInOutCubic(zt);
      const s0 = HEAD_SCALE_END;
      const s1 = Math.min(600, Math.max(s0, Math.hypot(geo.sw, geo.sh) / (ink.r * 1.2)));
      const s = s0 * Math.pow(s1 / s0, e);
      const blend = s1 === s0 ? 1 : (1 / s - 1 / s0) / (1 / s1 - 1 / s0);
      const cx = geo.hx + geo.hw / 2;
      const cy = geo.hy + geo.hh / 2;
      // where the focus sits at the end of the fly-through (scale s0 round the heading's centre)
      const bx = cx + s0 * (ink.x - cx);
      const by = cy + s0 * (ink.y - cy);
      const px2 = bx + (geo.sw / 2 - bx) * blend;
      const py2 = by + (geo.sh / 2 - by) * blend;
      const tx2 = px2 - cx - s * (ink.x - cx);
      const ty2 = py2 - cy - s * (ink.y - cy);
      const done = zt >= 1;
      head.style.transform = `translate(${tx2.toFixed(2)}px, ${ty2.toFixed(2)}px) scale(${s.toFixed(4)})`;
      // once the letter fills the screen it is swapped for a plain white layer (same colour, nothing moves)
      head.style.opacity = done ? "0" : "";
      if (whiteRef.current) whiteRef.current.style.opacity = done ? "1" : "0";
    };

    const render = () => {
      const mobile = w < 768;
      const far = mobile ? -1200 : -1700;
      const near = mobile ? 350 : 500;
      const pan = mobile ? 20 : 45;
      const cp = clamp01(prog / CARDS_END);
      for (let i = 0; i < total; i++) {
        const el = cardRefs.current[i];
        if (!el) continue;
        const start = (i / total) * (1 - SPAN);
        const t = clamp01((cp - start) / SPAN);
        const o = fade(t);
        const c = L[i];
        if (o <= 0) {
          // opacity only (no visibility: hidden), so screen readers still reach every card
          el.style.opacity = "0";
          el.style.pointerEvents = "none";
          continue;
        }
        const x = c.cos * w * c.rx - px * pan;
        const y = c.sin * h * c.ry - py * pan;
        const z = far + (near - far) * t;
        el.style.pointerEvents = "";
        el.style.opacity = o.toFixed(3);
        el.style.transform = `translate3d(calc(-50% + ${x.toFixed(1)}px), calc(-50% + ${y.toFixed(1)}px), ${z.toFixed(1)}px) rotateZ(${c.rz}deg)`;
      }
      renderHead();
      if (hintRef.current) hintRef.current.style.opacity = (1 - clamp01(cp / 0.1)).toFixed(3);
    };

    const frame = (now: number) => {
      const dt = last ? Math.min(0.05, (now - last) / 1000) : 1 / 60;
      last = now;
      const k = 1 - Math.exp(-dt * 7); // critically damped feel, close to the original spring
      const kp = 1 - Math.exp(-dt * 5);
      prog += (target - prog) * k;
      px += (tx - px) * kp;
      py += (ty - py) * kp;
      render();
      const settled = Math.abs(target - prog) < 0.0002 && Math.abs(tx - px) < 0.001 && Math.abs(ty - py) < 0.001;
      if (settled || !onScreen) {
        prog = target;
        raf = 0;
        last = 0;
        render();
        return;
      }
      raf = requestAnimationFrame(frame);
    };
    const kick = () => {
      if (!raf && onScreen) raf = requestAnimationFrame(frame);
    };

    const onScroll = () => {
      measure();
      kick();
    };
    // Re-scan the letters only when the width changes (mobile address bars fire height-only resizes while
    // scrolling), at most once per frame.
    let inkRaf = 0;
    const onResize = () => {
      const widthChanged = window.innerWidth !== w;
      w = window.innerWidth;
      h = window.innerHeight;
      if (widthChanged && !inkRaf) {
        inkRaf = requestAnimationFrame(() => {
          inkRaf = 0;
          measureInk();
          render();
        });
      }
      onScroll();
    };
    const fine = window.matchMedia("(pointer: fine)").matches;
    const onPointer = (e: PointerEvent) => {
      tx = (e.clientX / w - 0.5) * 2;
      ty = (e.clientY / h - 0.5) * 2;
      kick();
    };

    const io = new IntersectionObserver(([e]) => {
      onScreen = e.isIntersecting;
      if (onScreen) onScroll();
    });
    io.observe(section);
    measure();
    measureInk();
    prog = target;
    render();
    // the letter shapes depend on the web font: measure again once it has loaded
    let alive = true;
    document.fonts?.ready.then(() => {
      if (!alive) return;
      measureInk();
      render();
    });
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize);
    if (fine) window.addEventListener("pointermove", onPointer, { passive: true });
    return () => {
      alive = false;
      cancelAnimationFrame(inkRaf);
      io.disconnect();
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onResize);
      window.removeEventListener("pointermove", onPointer);
      for (const el of cardRefs.current) el?.removeAttribute("style");
      titleRef.current?.removeAttribute("style");
      hintRef.current?.removeAttribute("style");
      whiteRef.current?.removeAttribute("style");
    };
  }, [is3d, cards.length]);

  return (
    <section
      ref={sectionRef}
      className={is3d ? "tunnel is-3d" : "tunnel"}
      aria-labelledby={titleId}
    >
      <div className="tunnel-sticky" ref={stickyRef}>
        <div className="tunnel-bg" aria-hidden="true">
          <div className="tunnel-dots" />
          <div className="tunnel-glow" />
          <div className="tunnel-ring tunnel-ring-1" />
          <div className="tunnel-ring tunnel-ring-2" />
        </div>

        <div className="tunnel-head" ref={titleRef}>
          <p className="tunnel-eyebrow">{eyebrow}</p>
          <h2 id={titleId} className="tunnel-title" ref={headingRef}>
            {title}
          </h2>
          <p className="tunnel-sub">{sub}</p>
        </div>

        <p className="tunnel-hint" ref={hintRef} aria-hidden="true">
          <span>{hint}</span>
          <span className="tunnel-hint-line" />
        </p>

        <ul className="tunnel-stage">
          {cards.map((c, i) => (
            <li
              key={c.title}
              className="tunnel-card"
              ref={(el) => {
                cardRefs.current[i] = el;
              }}
            >
              <article className="tunnel-card-in">
                <img
                  src={M + (IMAGES[i] ?? IMAGES[0])}
                  alt={c.alt}
                  width={640}
                  height={800}
                  loading="lazy"
                  decoding="async"
                  draggable={false}
                />
                <div className="tunnel-card-text">
                  <p className="tunnel-card-place">{c.place}</p>
                  <h3 className="tunnel-card-title">{c.title}</h3>
                  <p className="tunnel-card-body">{c.text}</p>
                </div>
              </article>
            </li>
          ))}
        </ul>

        {/* the white the camera lands in at the end of the dive (3D mode only) */}
        <div className="tunnel-white" ref={whiteRef} aria-hidden="true" />
      </div>
    </section>
  );
}
