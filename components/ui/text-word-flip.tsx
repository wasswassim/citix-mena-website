"use client";

import { type CSSProperties, useEffect, useRef, useState } from "react";

/**
 * Text Word Flip, after the 21st.dev component by wensity (https://21st.dev/@wensity/components/text-word-flip),
 * rebuilt for this site (17 Nov 2026) without framer-motion or Tailwind: the same motion in CSS (app/globals.css,
 * .word-flip). Each word's letters blur in one after another and rise into place; after a hold the word leaves
 * up and outward, blurring and growing, while the next one comes in.
 *
 * Arabic letters join, so Arabic words are never split into letters: they come in word by word instead.
 * The exit leans toward the reading direction (mirrored in RTL). The cycle pauses while off screen or in a
 * hidden tab; reduced motion shows the first word, still. Decorative: the parent provides the readable text.
 */
type Props = {
  words: string[];
  /** Hold time per word, ms */
  duration?: number;
  /** Stagger between letters, s */
  letterDelay?: number;
  /** Stagger between words inside a phrase, s */
  wordDelay?: number;
  className?: string;
};

const EXIT_MS = 700;
const ARABIC = /[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/;

function Word({ text, letterDelay, wordDelay }: { text: string; letterDelay: number; wordDelay: number }) {
  const parts = text.split(" ").filter(Boolean);
  const joined = ARABIC.test(text);
  return (
    <>
      {parts.map((w, wi) => (
        <span key={wi} className="word-flip-part">
          {joined ? (
            <span className="word-flip-ch" style={{ "--d": `${wi * wordDelay}s` } as CSSProperties}>
              {w}
            </span>
          ) : (
            Array.from(w).map((ch, ci) => (
              <span
                key={ci}
                className="word-flip-ch"
                style={{ "--d": `${wi * wordDelay + ci * letterDelay}s` } as CSSProperties}
              >
                {ch}
              </span>
            ))
          )}
          {wi < parts.length - 1 ? " " : null}
        </span>
      ))}
    </>
  );
}

export function TextWordFlip({ words, duration = 2200, letterDelay = 0.05, wordDelay = 0.3, className }: Props) {
  const [index, setIndex] = useState(0);
  const [leaving, setLeaving] = useState<{ i: number; key: number } | null>(null);
  const [still, setStill] = useState(false);
  const rootRef = useRef<HTMLSpanElement>(null);
  const tick = useRef(0);
  const indexRef = useRef(0);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const sync = () => setStill(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);

  useEffect(() => {
    if (still || words.length < 2) return;
    let onScreen = true;
    const io = new IntersectionObserver(([e]) => (onScreen = e.isIntersecting));
    if (rootRef.current) io.observe(rootRef.current);
    let clear = 0;
    const id = window.setInterval(() => {
      if (!onScreen || document.hidden) return;
      const cur = indexRef.current;
      const next = (cur + 1) % words.length;
      indexRef.current = next;
      tick.current += 1;
      setLeaving({ i: cur, key: tick.current });
      setIndex(next);
      window.clearTimeout(clear);
      clear = window.setTimeout(() => setLeaving(null), EXIT_MS);
    }, Math.max(900, duration));
    return () => {
      io.disconnect();
      window.clearInterval(id);
      window.clearTimeout(clear);
    };
  }, [still, words.length, duration]);

  const cls = className ? `word-flip ${className}` : "word-flip";
  if (still) {
    return (
      <span ref={rootRef} className={cls} aria-hidden="true">
        <span className="word-flip-word is-still">{words[0]}</span>
      </span>
    );
  }
  return (
    <span ref={rootRef} className={cls} aria-hidden="true">
      {leaving && (
        <span key={`out-${leaving.key}`} className="word-flip-word is-out">
          {words[leaving.i]}
        </span>
      )}
      <span key={`in-${index}-${tick.current}`} className="word-flip-word is-in">
        <Word text={words[index]} letterDelay={letterDelay} wordDelay={wordDelay} />
      </span>
    </span>
  );
}

export default TextWordFlip;
