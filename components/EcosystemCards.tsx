"use client";

import { useEffect, useState } from "react";

/**
 * CITIX Ecosystem glass cards (Wassim, 15 Nov 2026): 3 cards at a time, bottom-start of the hero; every few seconds
 * each card flips (one after the other) to show the other 3, in a loop. The flip squeezes the card to its edge and
 * opens it on the next card: a 2D transform, because a real 3D flip stops the frosted-glass blur in Chrome.
 * All 6 cards are in the HTML as a list for screen readers and crawlers; the animated cards are decorative copies.
 * Reduced motion: no flipping, the first 3 stay.
 */
type Card = { title: string; text: string };

const HOLD_MS = 4200; // time each set stays
const STAGGER_MS = 140; // delay between the 3 cards
const HALF_MS = 300; // half a flip: the content swaps at the edge-on moment

export default function EcosystemCards({ label, cards }: { label: string; cards: Card[] }) {
  const [sets, setSets] = useState([0, 0, 0]); // which set (0 or 1) each of the 3 slots shows
  const [flipping, setFlipping] = useState([false, false, false]);

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

  return (
    <div className="ecosystem">
      <ul className="eco-cards" aria-hidden="true">
        {[0, 1, 2].map((i) => {
          const c = cards[sets[i] * 3 + i];
          return (
            <li key={i} className={flipping[i] ? "eco-card is-flipping" : "eco-card"}>
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
