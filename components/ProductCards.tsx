"use client";

import Link from "next/link";
import { useEffect, useId, useRef, useState } from "react";
import Arrow from "@/components/Arrow";

/**
 * Our Products (Wassim, 15 Nov 2026): the layout and motion of the bluesqx product accordion, rebuilt in our own
 * code. A row of tall cards: one is open, the others are narrow strips with the product name written vertically.
 * Clicking a strip opens it (1 s ease-out) while the open one closes; its text fades up after the card has grown.
 * Phones: the cards stack and open downwards.
 *
 * Media: every card is a short muted video from the company files (media/source/products/SOURCE.md), 0.3-0.8 MB
 * each. A video downloads nothing until its card is open (preload="none", and its still is a lazy <img>
 * underneath instead of a poster attribute, which would load with the page). It plays only while its card is open
 * and the section is on screen; closing pauses it where it is, reopening resumes from that point, and it starts
 * over only when it reaches the end (loop). With reduced motion it never plays: the still stays.
 */
type Card = { name: string; tag: string; text: string; alt: string };
type Props = { title: string; sub: string; cta: string; all: string; href: string; cards: Card[] };

type Media = { src: string; srcSet: string; position?: string; video: { mp4: string; webm: string } };
const P = "/media/products/";
const clip = (n: string, poster: [string, string], position?: string): Media => ({
  src: P + poster[1],
  srcSet: `${P}${poster[0]} 600w, ${P}${poster[1]} 1200w`,
  position,
  video: { mp4: `${P}${n}.mp4`, webm: `${P}${n}.webm` },
});
// Every card is a video (Wassim, 15 Nov 2026); the still underneath is its first frame.
const MEDIA: Media[] = [
  clip("tom-daynight", ["tom-poster-600.webp", "tom-poster-1200.webp"]), // day then night, one clip (9.6 s)
  clip("jerry", ["jerry-poster-600.webp", "jerry-poster-1200.webp"]),
  clip("baloo", ["baloo-poster-600.webp", "baloo-poster-1200.webp"]),
  {
    ...clip("jumbo", ["jumbo-poster-800.webp", "jumbo-poster-1600.webp"], "55% 50%"),
    srcSet: `${P}jumbo-poster-800.webp 800w, ${P}jumbo-poster-1600.webp 1600w`,
  },
];

export default function ProductCards({ title, sub, cta, all, href, cards }: Props) {
  const [open, setOpen] = useState(0);
  const [inView, setInView] = useState(false);
  const [reduced, setReduced] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);
  const videoRefs = useRef<(HTMLVideoElement | null)[]>([]);
  const uid = useId();

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const sync = () => setReduced(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    const io = new IntersectionObserver(([e]) => setInView(e.isIntersecting), { threshold: 0.15 });
    if (sectionRef.current) io.observe(sectionRef.current);
    return () => {
      mq.removeEventListener("change", sync);
      io.disconnect();
    };
  }, []);

  // Play only while open + on screen; pausing keeps the current time, so reopening resumes from there.
  useEffect(() => {
    videoRefs.current.forEach((v, i) => {
      if (!v) return;
      if (i === open && inView && !reduced) v.play().catch(() => {});
      else v.pause();
    });
  }, [open, inView, reduced]);

  return (
    <section ref={sectionRef} className="products" data-header-theme="light" aria-labelledby="products-title">
      <div className="products-head">
        <h2 id="products-title" className="products-title">
          {title}
        </h2>
        <p className="products-sub">{sub}</p>
      </div>

      <ul className="prod-row">
        {cards.map((c, i) => {
          const m = MEDIA[i];
          const isOpen = open === i;
          const contentId = `${uid}-p${i}`;
          return (
            <li key={c.name} className="prod-card" data-open={isOpen || undefined}>
              <div className="prod-media">
                <img
                  src={m.src}
                  srcSet={m.srcSet}
                  sizes="(max-width: 767px) 100vw, 70vw"
                  alt={c.alt}
                  loading="lazy"
                  decoding="async"
                  style={m.position ? { objectPosition: m.position } : undefined}
                />
                <video
                  ref={(el) => {
                    videoRefs.current[i] = el;
                  }}
                  muted
                  loop
                  playsInline
                  preload="none"
                  aria-hidden="true"
                  style={m.position ? { objectPosition: m.position } : undefined}
                >
                  <source src={m.video.mp4} type="video/mp4" />
                  <source src={m.video.webm} type="video/webm" />
                </video>
              </div>
              <div className="prod-shade" aria-hidden="true" />

              <button
                type="button"
                className="prod-toggle"
                aria-expanded={isOpen}
                aria-controls={contentId}
                onClick={() => setOpen(i)}
              >
                <span className="prod-preview">{c.name}</span>
              </button>

              <div id={contentId} className="prod-content" inert={!isOpen}>
                <div className="prod-top">
                  <p className="prod-tag">{c.tag}</p>
                  <h3 className="prod-name">{c.name}</h3>
                  <p className="prod-text">{c.text}</p>
                </div>
                <div className="prod-bottom">
                  <Link className="btn-outline" href={href}>
                    {cta}
                    <Arrow />
                  </Link>
                </div>
              </div>
            </li>
          );
        })}
      </ul>

      <div className="products-more">
        <Link className="btn-outline" href={href}>
          {all}
          <Arrow />
        </Link>
      </div>
    </section>
  );
}
