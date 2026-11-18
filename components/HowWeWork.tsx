"use client";

import { useEffect, useId, useRef, useState, type CSSProperties } from "react";

/**
 * How we work (Wassim, 18 Nov 2026, v2): the four steps from the company documents (sales deck and company profile,
 * see lib/i18n.ts) as a stack of CITIX widget cards. Motion idea taken from the 21st.dev "Stacking Cards" pattern
 * (cards pin and the ones underneath shrink back as the next lands), rebuilt here without its code.
 *
 * Desktop: the heading and a step index sit pinned on the start side; the cards pile up on the end side. Each card is
 * a smartboard widget (dark screen, graphite tiles, Pulse Red chevron discs) carrying the full step copy as real HTML.
 * Mobile: one column, the cards still stack. Reduced motion: the cards simply follow each other, nothing pins.
 */
type Step = { title: string; text: string; rows: [string, string] };
type Props = { eyebrow: string; title: string; sub: string; steps: Step[]; rtl: boolean };

type Icon = "pin" | "cube" | "sun" | "eye";
const ICONS: Icon[] = ["pin", "cube", "sun", "eye"];

function StepIcon({ name }: { name: Icon }) {
  const line = { fill: "none", stroke: "currentColor", strokeWidth: 1.6, strokeLinecap: "round", strokeLinejoin: "round" } as const;
  return (
    <svg className="how-icon" viewBox="0 0 48 48" aria-hidden="true">
      {name === "pin" && (
        <>
          <path {...line} d="M24 43s-13-13.4-13-23a13 13 0 0 1 26 0c0 9.6-13 23-13 23z" />
          <circle cx="24" cy="20" r="4.6" fill="var(--pulse)" />
        </>
      )}
      {name === "cube" && (
        <>
          <path d="M24 6l15 8-15 8-15-8z" fill="var(--pulse)" />
          <path {...line} d="M9 14v18l15 9 15-9V14M24 22v19" />
        </>
      )}
      {name === "sun" && (
        <>
          <circle cx="24" cy="24" r="7.5" fill="var(--pulse)" />
          <path {...line} d="M24 6v6M24 36v6M6 24h6M36 24h6M11.3 11.3l4.2 4.2M32.5 32.5l4.2 4.2M11.3 36.7l4.2-4.2M32.5 15.5l4.2-4.2" />
        </>
      )}
      {name === "eye" && (
        <>
          <path {...line} d="M4 24s7.3-12 20-12 20 12 20 12-7.3 12-20 12S4 24 4 24z" />
          <circle cx="24" cy="24" r="6.5" fill="var(--pulse)" />
        </>
      )}
    </svg>
  );
}

function Chevron() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M6 15l6-6 6 6" fill="none" stroke="currentColor" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

const pad = (n: number) => String(n).padStart(2, "0");

export default function HowWeWork({ eyebrow, title, sub, steps, rtl }: Props) {
  const titleId = useId();
  const sectionRef = useRef<HTMLElement>(null);
  const cardRefs = useRef<(HTMLLIElement | null)[]>([]);
  const [active, setActive] = useState(0);

  // Reveal: in motion mode the section is pulled up over the end of the projects tunnel (CSS margin) so that it
  // reaches the top of the screen just as the dive turns white; it stays hidden until then. Scrolling back up hides
  // it again so the dive can replay.
  const [revealed, setRevealed] = useState(false);
  useEffect(() => {
    const el = sectionRef.current;
    const tunnel = el?.previousElementSibling;
    if (!el || !(tunnel instanceof HTMLElement) || !tunnel.classList.contains("tunnel")) {
      setRevealed(true);
      return;
    }
    const check = () => {
      if (document.documentElement.dataset.motion !== "ok") return setRevealed(true);
      setRevealed(el.getBoundingClientRect().top <= 2);
    };
    check();
    window.addEventListener("scroll", check, { passive: true });
    window.addEventListener("resize", check);
    return () => {
      window.removeEventListener("scroll", check);
      window.removeEventListener("resize", check);
    };
  }, []);

  // Stacking: while card j slides over card i, card i shrinks and dims a little (depth adds up as more cards land).
  // One rAF-batched pass per scroll; with reduced motion no depth is set (CSS also turns the pinning off).
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    let raf = 0;
    const run = () => {
      raf = 0;
      const cards = cardRefs.current.filter((c): c is HTMLLIElement => !!c);
      if (!cards.length) return;
      const rects = cards.map((c) => c.getBoundingClientRect());
      const tops = cards.map((c) => parseFloat(getComputedStyle(c).top) || 0);
      let current = 0;
      cards.forEach((card, i) => {
        // a card counts as the current step once it covers most of the one below
        if (rects[i].top <= tops[i] + rects[i].height * 0.4) current = i;
        if (mq.matches) {
          card.style.removeProperty("--depth");
          return;
        }
        const h = rects[i].height || 1;
        let depth = 0;
        for (let j = i + 1; j < cards.length; j++) depth += Math.min(1, Math.max(0, (tops[i] + h - rects[j].top) / h));
        card.style.setProperty("--depth", depth.toFixed(3));
      });
      setActive(current);
    };
    const queue = () => {
      if (!raf) raf = requestAnimationFrame(run);
    };
    queue();
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue);
    mq.addEventListener("change", queue);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", queue);
      window.removeEventListener("resize", queue);
      mq.removeEventListener("change", queue);
    };
  }, []);

  return (
    <section ref={sectionRef} className={revealed ? "how is-revealed" : "how"} aria-labelledby={titleId}>
      <div className="how-grid">
        <div className="how-head">
          <p className="how-eyebrow">{eyebrow}</p>
          <h2 id={titleId} className="how-title">
            {title}
          </h2>
          <p className="how-sub">{sub}</p>

          {/* step index: follows the card on top of the stack */}
          <ol className="how-index" aria-hidden="true">
            {steps.map((s, i) => (
              <li key={s.title} className={i === active ? "is-active" : i < active ? "is-done" : undefined}>
                <span className="how-index-n">{pad(i + 1)}</span>
                <span className="how-index-t">{s.title}</span>
              </li>
            ))}
          </ol>
        </div>

        <ol className="how-stack" style={{ "--n": steps.length } as CSSProperties}>
          {steps.map((s, i) => (
            <li
              key={s.title}
              ref={(el) => {
                cardRefs.current[i] = el;
              }}
              className="how-card"
              style={{ "--i": i } as CSSProperties}
              aria-current={i === active ? "step" : undefined}
            >
              <article className="how-screen" dir={rtl ? "rtl" : "ltr"}>
                <div className="how-tile how-tile-main">
                  <div className="how-tile-top">
                    <span className="how-num">{pad(i + 1)}</span>
                    <span className="how-disc how-disc-white">
                      <Chevron />
                    </span>
                  </div>
                  <StepIcon name={ICONS[i % ICONS.length]} />
                  <h3 className="how-card-title">{s.title}</h3>
                  <p className="how-card-text">{s.text}</p>
                </div>
                <ul className="how-rows">
                  {s.rows.map((r) => (
                    <li key={r} className="how-tile how-row">
                      <span>{r}</span>
                      <span className="how-disc">
                        <Chevron />
                      </span>
                    </li>
                  ))}
                </ul>
              </article>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
