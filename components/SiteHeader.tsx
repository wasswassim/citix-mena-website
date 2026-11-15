"use client";

import Link from "next/link";
import { useEffect, useId, useRef, useState } from "react";
import Arrow from "@/components/Arrow";
import { SHOW_ANNOUNCEMENT } from "@/lib/flags";
import type { Locale } from "@/lib/i18n";

/**
 * Fixed, transparent header over the hero (runbook v5 P5, bluesqx layout rebuilt in our stack).
 * Desktop: wordmark left, nav centred, "Get in touch" + EN/AR right. Mobile: wordmark, "Get in touch", "+" menu.
 * Optional announcement bar on top, behind SHOW_ANNOUNCEMENT (preview with ?bar=1); closing it is remembered.
 */
const BAR_KEY = "citix-announcement-closed";

type Props = {
  lang: Locale;
  siteName: string;
  nav: { href: string; label: string }[];
  getInTouch: { href: string; label: string };
  langSwitch: { href: string; label: string; hrefLang: string };
  menuOpen: string;
  menuClose: string;
  navLabel: string;
  announcement: { text: string; cta: string; close: string; href: string };
};

export default function SiteHeader(p: Props) {
  const [open, setOpen] = useState(false);
  const [bar, setBar] = useState(false);
  const menuId = useId();

  useEffect(() => {
    let closed = false;
    try {
      closed = localStorage.getItem(BAR_KEY) === "1";
    } catch {}
    const forced = new URLSearchParams(location.search).get("bar") === "1";
    setBar((SHOW_ANNOUNCEMENT || forced) && !closed);
  }, []);

  // Header tone and frosting (Wassim, 15 Nov 2026, like the reference): the tone follows the section 25 px below the
  // top of the screen (light sections are marked data-header-theme="light"; everything else is dark), and after
  // 96 px of scroll the header turns into frosted glass of that tone (app/globals.css). Transparent at the very top.
  const topRef = useRef<HTMLDivElement>(null);
  const [light, setLight] = useState(false);
  const [frosted, setFrosted] = useState(false);
  useEffect(() => {
    let raf = 0;
    const TONE_LINE = 25;
    const FROST_AFTER = 96;
    const check = () => {
      raf = 0;
      const onLight = [...document.querySelectorAll<HTMLElement>('[data-header-theme="light"]')].some((el) => {
        const b = el.getBoundingClientRect();
        return b.top <= TONE_LINE && b.bottom > TONE_LINE;
      });
      setLight(onLight);
      setFrosted(window.scrollY > FROST_AFTER);
    };
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(check);
    };
    check();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  const closeBar = () => {
    setBar(false);
    try {
      localStorage.setItem(BAR_KEY, "1");
    } catch {}
  };

  return (
    <div ref={topRef} className="site-top" data-open={open || undefined} data-theme={light ? "light" : undefined}
      data-frosted={frosted || undefined}
    >
      {bar && (
        <div className="announce">
          <p>{p.announcement.text}</p>
          <Link className="announce-cta" href={p.announcement.href}>
            {p.announcement.cta}
            <Arrow />
          </Link>
          <button type="button" className="announce-close" onClick={closeBar} aria-label={p.announcement.close}>
            <svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true">
              <path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" strokeWidth="1.4" />
            </svg>
          </button>
        </div>
      )}
      <header className="site-header">
        {/* Official CITIX › MENA logo from citixmena.com (media/brand/_download_2026-11-15/SOURCE.md).
            Brand rules: never stretched (height set, width follows), never bottom-right, clear space = the X. */}
        <Link href={`/${p.lang}`} className="site-name">
          <img className="logo-light" src="/media/brand/citix-logo-white.png" alt={p.siteName} width={934} height={280} />
          {/* Brand book "black / red" version for light sections: made from the official file by turning only its
              white pixels black (red X and chevron untouched). */}
          <img
            className="logo-dark"
            src="/media/brand/citix-logo-black.png"
            alt=""
            aria-hidden="true"
            width={934}
            height={280}
          />
        </Link>
        <nav className="site-nav" aria-label={p.navLabel}>
          <ul>
            {p.nav.map((n) => (
              <li key={n.label}>
                <Link href={n.href}>{n.label}</Link>
              </li>
            ))}
          </ul>
        </nav>
        <div className="header-actions">
          <Link className="btn-outline" href={p.getInTouch.href}>
            {p.getInTouch.label}
            <Arrow />
          </Link>
          <Link className="lang-switch" href={p.langSwitch.href} hrefLang={p.langSwitch.hrefLang}>
            {p.langSwitch.label}
          </Link>
          <button
            type="button"
            className="menu-btn"
            aria-expanded={open}
            aria-controls={menuId}
            aria-label={open ? p.menuClose : p.menuOpen}
            onClick={() => setOpen((o) => !o)}
          >
            <svg viewBox="0 0 14 14" width="14" height="14" aria-hidden="true">
              <path d="M7 1v12M1 7h12" stroke="currentColor" strokeWidth="1.5" />
            </svg>
          </button>
        </div>
      </header>
      <div id={menuId} className="mobile-menu" hidden={!open}>
        <ul>
          {p.nav.map((n) => (
            <li key={n.label}>
              <Link href={n.href} onClick={() => setOpen(false)}>
                {n.label}
              </Link>
            </li>
          ))}
          <li>
            <Link href={p.langSwitch.href} hrefLang={p.langSwitch.hrefLang}>
              {p.langSwitch.label}
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
}
