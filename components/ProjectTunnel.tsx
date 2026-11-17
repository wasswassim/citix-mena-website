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

export default function ProjectTunnel({ eyebrow, title, sub, hint, cards }: Props) {
  const sectionRef = useRef<HTMLElement>(null);
  const titleRef = useRef<HTMLDivElement>(null);
  const hintRef = useRef<HTMLParagraphElement>(null);
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

    const render = () => {
      const mobile = w < 768;
      const far = mobile ? -1200 : -1700;
      const near = mobile ? 350 : 500;
      const pan = mobile ? 20 : 45;
      for (let i = 0; i < total; i++) {
        const el = cardRefs.current[i];
        if (!el) continue;
        const start = (i / total) * (1 - SPAN);
        const t = clamp01((prog - start) / SPAN);
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
      if (titleRef.current) {
        // the heading grows slowly as you travel and stays readable behind the cards
        const s = prog < 0.5 ? 0.82 + prog * 0.36 : 1 + (prog - 0.5) * 0.3;
        titleRef.current.style.transform = `scale(${s.toFixed(4)})`;
        titleRef.current.style.opacity = (prog > 0.9 ? 1 - (prog - 0.9) * 6 : 1).toFixed(3);
      }
      if (hintRef.current) hintRef.current.style.opacity = (1 - clamp01(prog / 0.1)).toFixed(3);
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
    const onResize = () => {
      w = window.innerWidth;
      h = window.innerHeight;
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
    prog = target;
    render();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize);
    if (fine) window.addEventListener("pointermove", onPointer, { passive: true });
    return () => {
      io.disconnect();
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onResize);
      window.removeEventListener("pointermove", onPointer);
      for (const el of cardRefs.current) el?.removeAttribute("style");
      titleRef.current?.removeAttribute("style");
      hintRef.current?.removeAttribute("style");
    };
  }, [is3d, cards.length]);

  return (
    <section
      ref={sectionRef}
      className={is3d ? "tunnel is-3d" : "tunnel"}
      aria-labelledby={titleId}
    >
      <div className="tunnel-sticky">
        <div className="tunnel-bg" aria-hidden="true">
          <div className="tunnel-dots" />
          <div className="tunnel-glow" />
          <div className="tunnel-ring tunnel-ring-1" />
          <div className="tunnel-ring tunnel-ring-2" />
        </div>

        <div className="tunnel-head" ref={titleRef}>
          <p className="tunnel-eyebrow">{eyebrow}</p>
          <h2 id={titleId} className="tunnel-title">
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
      </div>
    </section>
  );
}
