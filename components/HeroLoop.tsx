"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Hero v5 "The Orbit": the 28 s glass-panel loop (oasis, perfume, camel, SUV), muted, behind the hero copy.
 * - The poster is a plain <img> rendered on the server (the LCP element); the video fades in over it once playing.
 * - Desktop/landscape gets the 16:9 loop, portrait screens the 9:16 reframe (media/web/hero/timing.json).
 * - prefers-reduced-motion: no video at all, the poster stays.
 * - Paused while off-screen or while the tab is hidden.
 * No dust overlay (dropped by Wassim, 15 Nov 2026).
 */
const PORTRAIT = "(max-aspect-ratio: 4/5)";
const SRC = {
  wide: { mp4: "/media/hero/orbit_16x9.mp4", webm: "/media/hero/orbit_16x9.webm" },
  tall: { mp4: "/media/hero/orbit_9x16.mp4", webm: "/media/hero/orbit_9x16.webm" },
};

export default function HeroLoop({ alt }: { alt: string }) {
  const ref = useRef<HTMLVideoElement>(null);
  const [variant, setVariant] = useState<"wide" | "tall" | null>(null);
  const [playing, setPlaying] = useState(false);

  // Pick the variant on the client (and again if the screen flips between portrait and landscape).
  useEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    const portrait = window.matchMedia(PORTRAIT);
    const pick = () => setVariant(reduce.matches ? null : portrait.matches ? "tall" : "wide");
    pick();
    reduce.addEventListener("change", pick);
    portrait.addEventListener("change", pick);
    return () => {
      reduce.removeEventListener("change", pick);
      portrait.removeEventListener("change", pick);
    };
  }, []);

  // Play only while visible on screen and while the tab is in front.
  useEffect(() => {
    const v = ref.current;
    if (!v || !variant) return;
    setPlaying(false);
    v.load();
    let onScreen = true;
    const sync = () => {
      if (onScreen && !document.hidden) v.play().catch(() => {});
      else v.pause();
    };
    const io = new IntersectionObserver(([e]) => {
      onScreen = e.isIntersecting;
      sync();
    });
    io.observe(v);
    document.addEventListener("visibilitychange", sync);
    sync();
    return () => {
      io.disconnect();
      document.removeEventListener("visibilitychange", sync);
    };
  }, [variant]);

  return (
    <div className="hero-media">
      <picture>
        <source media={PORTRAIT} srcSet="/media/hero/orbit_9x16_poster.webp" />
        <img src="/media/hero/orbit_16x9_poster.webp" alt={alt} width={1280} height={720} fetchPriority="high" />
      </picture>
      {variant && (
        <video
          key={variant}
          ref={ref}
          className={playing ? "is-playing" : undefined}
          muted
          loop
          playsInline
          preload="auto"
          aria-hidden="true"
          tabIndex={-1}
          onPlaying={() => setPlaying(true)}
        >
          <source src={SRC[variant].webm} type="video/webm" />
          <source src={SRC[variant].mp4} type="video/mp4" />
        </video>
      )}
    </div>
  );
}
