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
 * Media (company sales deck, media/source/products/SOURCE.md), chosen for look per kilobyte:
 *   Tom: real night photo (41 KB) · Jerry: studio render (6-18 KB) · Baloo: night render (21-52 KB)
 *   Jumbo: the only video (3D perfume campaign, 9.8 s, 545 KB MP4 / 573 KB WebM).
 * The Jumbo video downloads nothing until the card is first opened (preload="none", and its still is a lazy <img>
 * underneath instead of a poster attribute, which would load with the page). It plays only while its card is open
 * and the section is on screen; closing pauses it where it is, reopening resumes from that point, and it starts
 * over only when it reaches the end (loop). With reduced motion it never plays: the still stays.
 */
type Card = { name: string; tag: string; text: string; alt: string };
type Props = { title: string; sub: string; cta: string; all: string; href: string; cards: Card[] };

type Media = { src: string; srcSet?: string; position?: string; video?: { mp4: string; webm: string } };
const MEDIA: Media[] = [
  { src: "/media/products/tom-800.webp", position: "50% 30%" },
  // object-position keeps each product inside the narrow closed strip (measured on the deck images)
  { src: "/media/products/jerry-1600.webp", srcSet: "/media/products/jerry-800.webp 800w, /media/products/jerry-1600.webp 1600w" },
  {
    src: "/media/products/baloo-1600.webp",
    srcSet: "/media/products/baloo-800.webp 800w, /media/products/baloo-1600.webp 1600w",
    position: "55% 50%",
  },
  {
    src: "/media/products/jumbo-poster-1600.webp",
    srcSet: "/media/products/jumbo-poster-800.webp 800w, /media/products/jumbo-poster-1600.webp 1600w",
    position: "55% 50%",
    video: { mp4: "/media/products/jumbo.mp4", webm: "/media/products/jumbo.webm" },
  },
];

export default function ProductCards({ title, sub, cta, all, href, cards }: Props) {
  const [open, setOpen] = useState(0);
  const [inView, setInView] = useState(false);
  const [reduced, setReduced] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const uid = useId();
  const videoIndex = MEDIA.findIndex((m) => m.video);

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
    const v = videoRef.current;
    if (!v) return;
    if (open === videoIndex && inView && !reduced) v.play().catch(() => {});
    else v.pause();
  }, [open, inView, reduced, videoIndex]);

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
                  sizes={m.srcSet ? "(max-width: 767px) 100vw, 75vw" : undefined}
                  alt={c.alt}
                  loading="lazy"
                  decoding="async"
                  style={m.position ? { objectPosition: m.position } : undefined}
                />
                {m.video && (
                  <video
                    ref={videoRef}
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
                )}
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
