"use client";

import { useEffect, useRef, useState } from "react";

/**
 * CITIX Ecosystem glass cards (Wassim, 15 Nov 2026): 3 cards at a time, bottom-start of the hero; every few seconds
 * each card (one after the other) changes to show the other 3, in a loop. The glass stays still: only the words
 * blur out, swap at the blurriest moment and sharpen back in (Wassim: blur instead of a flip).
 *
 * Apple-style glass that reacts to the scene: ~8 times a second the hero video frame is drawn into a tiny canvas,
 * and for each card the light around it gives --li (strength), --lx/--ly (direction) and --lc (colour), which move
 * the card's highlight, rim light and tint (app/globals.css). The real blur of the video stays underneath.
 *
 * All 6 cards are in the HTML as a list for screen readers and crawlers; the animated cards are decorative copies.
 * Reduced motion: no swapping and no light tracking (static glass).
 */
type Card = { title: string; text: string };

const HOLD_MS = 4200; // time each set stays
const STAGGER_MS = 160; // delay between the 3 cards
const HALF_MS = 450; // half the blur swap: the words change at the blurriest moment (CSS: 2 × HALF_MS)
const SAMPLE_MS = 125; // light sampling rate
const CW = 64; // sample canvas (16:9)
const CH = 36;

export default function EcosystemCards({ label, cards }: { label: string; cards: Card[] }) {
  const [sets, setSets] = useState([0, 0, 0]); // which set (0 or 1) each of the 3 slots shows
  const [flipping, setFlipping] = useState([false, false, false]);
  const cardRefs = useRef<(HTMLLIElement | null)[]>([]);

  // Flip loop
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const timers: number[] = [];
    const cycle = () => {
      if (document.hidden) return;
      for (let i = 0; i < 3; i++) {
        timers.push(
          window.setTimeout(() => setFlipping((f) => f.map((v, k) => (k === i ? true : v))), i * STAGGER_MS),
          window.setTimeout(() => setSets((s) => s.map((v, k) => (k === i ? 1 - v : v))), i * STAGGER_MS + HALF_MS),
          window.setTimeout(
            () => setFlipping((f) => f.map((v, k) => (k === i ? false : v))),
            i * STAGGER_MS + 2 * HALF_MS,
          ),
        );
      }
    };
    const id = window.setInterval(cycle, HOLD_MS);
    return () => {
      window.clearInterval(id);
      timers.forEach(clearTimeout);
    };
  }, []);

  // Light tracking from the hero video
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const canvas = document.createElement("canvas");
    canvas.width = CW;
    canvas.height = CH;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    if (!ctx) return;

    const sample = () => {
      const video = document.querySelector<HTMLVideoElement>(".hero-media video");
      if (!video || document.hidden || video.paused || video.readyState < 2 || !video.videoWidth) return;
      try {
        ctx.drawImage(video, 0, 0, CW, CH);
      } catch {
        return;
      }
      const px = ctx.getImageData(0, 0, CW, CH).data;
      // object-fit: cover mapping from the screen to the sample canvas
      const vr = video.getBoundingClientRect();
      const s = Math.max(vr.width / video.videoWidth, vr.height / video.videoHeight);
      const dw = video.videoWidth * s;
      const dh = video.videoHeight * s;
      const ox = vr.left + (vr.width - dw) / 2;
      const oy = vr.top + (vr.height - dh) / 2;

      cardRefs.current.forEach((card) => {
        if (!card) return;
        const r = card.getBoundingClientRect();
        // look at the card's area plus a margin around it: light near the glass still reaches it
        const m = r.width * 0.6;
        const x0 = Math.max(0, Math.floor(((r.left - m - ox) / dw) * CW));
        const x1 = Math.min(CW - 1, Math.ceil(((r.right + m - ox) / dw) * CW));
        const y0 = Math.max(0, Math.floor(((r.top - m - oy) / dh) * CH));
        const y1 = Math.min(CH - 1, Math.ceil(((r.bottom + m - oy) / dh) * CH));
        if (x1 <= x0 || y1 <= y0) return;
        const ccx = ((r.left + r.width / 2 - ox) / dw) * CW;
        const ccy = ((r.top + r.height / 2 - oy) / dh) * CH;
        let wSum = 0, lw = 0, rw = 0, gw = 0, bw = 0, xw = 0, yw = 0;
        for (let y = y0; y <= y1; y++) {
          for (let x = x0; x <= x1; x++) {
            const k = (y * CW + x) * 4;
            const L = 0.2126 * px[k] + 0.7152 * px[k + 1] + 0.0722 * px[k + 2];
            const w = L * L; // bright pixels dominate: they are the light sources
            wSum += w;
            lw += L * w;
            rw += px[k] * w;
            gw += px[k + 1] * w;
            bw += px[k + 2] * w;
            xw += (x - ccx) * w;
            yw += (y - ccy) * w;
          }
        }
        if (wSum < 1) {
          card.style.setProperty("--li", "0.12");
          return;
        }
        const light = lw / wSum; // brightness-weighted luminance, 0–255
        // calibrated on the hero loop: dark sand ≈ 15–25, lit water / headlights / petals ≈ 60–110
        const li = Math.min(1, Math.max(0.12, (light - 14) / 70));
        const half = ((x1 - x0) / 2) || 1;
        const halfY = ((y1 - y0) / 2) || 1;
        const lx = Math.min(100, Math.max(0, 50 + ((xw / wSum) / half) * 70));
        const ly = Math.min(100, Math.max(0, 50 + ((yw / wSum) / halfY) * 70));
        // light colour, lifted toward white so it tints rather than paints
        const lift = (c: number) => Math.round(Math.min(255, 150 + (c / wSum) * 0.6));
        card.style.setProperty("--li", li.toFixed(3));
        card.style.setProperty("--lx", `${lx.toFixed(1)}%`);
        card.style.setProperty("--ly", `${ly.toFixed(1)}%`);
        card.style.setProperty("--lc", `rgb(${lift(rw)} ${lift(gw)} ${lift(bw)})`);
      });
    };
    const id = window.setInterval(sample, SAMPLE_MS);
    return () => window.clearInterval(id);
  }, []);

  return (
    <div className="ecosystem">
      <ul className="eco-cards" aria-hidden="true">
        {[0, 1, 2].map((i) => {
          const c = cards[sets[i] * 3 + i];
          return (
            <li
              key={i}
              ref={(el) => {
                cardRefs.current[i] = el;
              }}
              className={flipping[i] ? "eco-card is-swapping" : "eco-card"}
            >
              <span className="eco-title">{c.title}</span>
              <span className="eco-dot" />
              <span className="eco-text">{c.text}</span>
            </li>
          );
        })}
      </ul>
      <ul className="sr-only">
        {cards.map((c) => (
          <li key={c.title}>
            {c.title}: {c.text}
          </li>
        ))}
      </ul>
      <p className="eco-label">{label}</p>
    </div>
  );
}
