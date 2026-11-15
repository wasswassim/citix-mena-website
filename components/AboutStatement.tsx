"use client";

import Link from "next/link";
import { Fragment, useEffect, useRef } from "react";
import Arrow from "@/components/Arrow";

/**
 * About statement right after the hero (Wassim, 15 Nov 2026): the layout and scroll motion of the bluesqx intro
 * statement, rebuilt in our own code (no GSAP or SplitType needed for this one effect). White section, a title in
 * place of their animated logo, a large two-paragraph statement, then a short line and a "Talk to us" button.
 *
 * Motion (measured on the reference): every word starts at 25% opacity and turns solid one after another as you
 * scroll. The reveal runs from the moment the section's top reaches the middle of the screen until its bottom
 * reaches the middle (phones: top at 35%, bottom at 60%), with a smoothed follow so it eases behind the scroll.
 * Each word takes 0.5 units to fill, starting 0.1 after the previous one (ease-out).
 *
 * The words are real text rendered on the server (crawlable, read normally by screen readers). Without JS or with
 * reduced motion they stay fully solid.
 */
const DIM = 0.25;
const STAGGER = 0.1;
const DUR = 0.5;
const SMOOTH_S = 0.45; // follow time constant: ~95% caught up after ~1.4 s

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));

type Props = { title: string; paragraphs: string[]; ctaLine: string; cta: string; href: string };

export default function AboutStatement({ title, paragraphs, ctaLine, cta, href }: Props) {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const words = [...section.querySelectorAll<HTMLElement>(".about-word")];
    if (!words.length) return;
    const total = STAGGER * (words.length - 1) + DUR;
    const shown = new Array<string>(words.length).fill("");

    // Progress in page-scroll terms. While this is the last section, its bottom can never reach the end line, so
    // the end is capped at the bottom of the page: the statement is always complete when you reach the end.
    const target = () => {
      const r = section.getBoundingClientRect();
      const vh = window.innerHeight;
      const mobile = window.innerWidth <= 767;
      const startLine = vh * (mobile ? 0.35 : 0.5);
      const endLine = vh * (mobile ? 0.6 : 0.5);
      const y = window.scrollY;
      const top = r.top + y;
      const startY = top - startLine;
      const maxY = document.documentElement.scrollHeight - vh;
      const endY = Math.min(top + r.height - endLine, maxY - 1);
      return endY > startY ? clamp01((y - startY) / (endY - startY)) : 1;
    };

    const paint = (p: number) => {
      const t = p * total;
      for (let i = 0; i < words.length; i++) {
        const x = clamp01((t - i * STAGGER) / DUR);
        const o = (DIM + (1 - DIM) * (1 - (1 - x) * (1 - x))).toFixed(3);
        if (o !== shown[i]) {
          words[i].style.opacity = o;
          shown[i] = o;
        }
      }
    };

    let current = target();
    paint(current);
    let raf = 0;
    let last = 0;
    const tick = (now: number) => {
      const dt = last ? (now - last) / 1000 : 0.016;
      last = now;
      const goal = target();
      current += (goal - current) * (1 - Math.exp(-dt / SMOOTH_S));
      if (Math.abs(goal - current) < 0.0005) current = goal;
      paint(current);
      raf = current === goal ? 0 : requestAnimationFrame(tick);
      if (!raf) last = 0;
    };
    const wake = () => {
      if (!raf) raf = requestAnimationFrame(tick);
    };

    window.addEventListener("scroll", wake, { passive: true });
    window.addEventListener("resize", wake);
    return () => {
      window.removeEventListener("scroll", wake);
      window.removeEventListener("resize", wake);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <section ref={sectionRef} className="about" data-header-theme="light" aria-labelledby="about-title">
      <h2 id="about-title" className="about-title">
        {title}
      </h2>
      <div className="about-text">
        {paragraphs.map((para, pi) => (
          <p key={pi}>
            {para.split(" ").map((w, i) => (
              <Fragment key={i}>
                {i > 0 && " "}
                <span className="about-word">{w}</span>
              </Fragment>
            ))}
          </p>
        ))}
      </div>
      <div className="about-cta">
        <p>{ctaLine}</p>
        <Link className="btn-outline" href={href}>
          {cta}
          <Arrow />
        </Link>
      </div>
    </section>
  );
}
