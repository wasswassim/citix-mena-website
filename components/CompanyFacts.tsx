"use client";

import { useEffect, useRef } from "react";

/**
 * Company facts strip between the hero and the About statement (Wassim, 15 Nov 2026): a compact row of counters,
 * laid out like his reference (numbers side by side, a short line under each, thin dividers), on a light section.
 *
 * The final numbers are rendered on the server (crawlable, read normally by screen readers, shown as is without JS
 * or with reduced motion). With motion allowed, each cell rises in and its number counts up from 0 the first time
 * the strip enters the screen, one cell after another. Columns have fixed widths and the digits are tabular, so the
 * counting moves nothing else on the page.
 */
const DURATION_MS = 1800;
const STAGGER_MS = 140;
const ease = (t: number) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t)); // fast start, long soft landing

type Fact = { value: number; suffix: string; label: string };
type Props = { title: string; facts: Fact[] };

const fmt = (n: number) => n.toLocaleString("en-US");

export default function CompanyFacts({ title, facts }: Props) {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    // Already scrolled past (e.g. a reload halfway down the page): leave the final numbers in place.
    if (section.getBoundingClientRect().bottom < 0) return;

    const nums = [...section.querySelectorAll<HTMLElement>("[data-count]")];
    const targets = nums.map((el) => Number(el.dataset.count));
    nums.forEach((el) => (el.textContent = "0"));
    section.dataset.anim = "";

    let raf = 0;
    let start = 0;
    const tick = (now: number) => {
      if (!start) start = now;
      let running = false;
      nums.forEach((el, i) => {
        const t = Math.max(0, (now - start - i * STAGGER_MS) / DURATION_MS);
        if (t < 1) running = true;
        el.textContent = fmt(Math.round(targets[i] * ease(t)));
      });
      raf = running ? requestAnimationFrame(tick) : 0;
    };

    const io = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        io.disconnect();
        section.classList.add("is-in");
        raf = requestAnimationFrame(tick);
      },
      { threshold: 0.35 },
    );
    io.observe(section);

    return () => {
      io.disconnect();
      if (raf) cancelAnimationFrame(raf);
      nums.forEach((el, i) => (el.textContent = fmt(targets[i])));
      delete section.dataset.anim;
      section.classList.remove("is-in");
    };
  }, []);

  return (
    <section ref={sectionRef} className="facts" data-header-theme="light" aria-labelledby="facts-title">
      <h2 id="facts-title" className="sr-only">
        {title}
      </h2>
      <ul className="facts-list">
        {facts.map((f, i) => (
          <li key={f.label} className="fact" style={{ "--i": i } as React.CSSProperties}>
            <p className="fact-num">
              <span data-count={f.value}>{fmt(f.value)}</span>
              {f.suffix}
            </p>
            <p className="fact-label">{f.label}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
