"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { GlassIconReveal } from "@/components/ui/liquid-glass-logo-reveal";
import { DARK_GLASS } from "@/lib/liquid-glass";

/**
 * Loading screen (Wassim, 17 Nov 2026): the CITIX X (cut from the official logo, media/web/brand/citix-x.png)
 * lands as a drop of liquid glass, spreads into a tile, bends into colour and lets go, then the screen slides
 * up to reveal the hero. Same glass maths as the hero cards (lib/liquid-glass.ts).
 *
 * Shown on every page load (Wassim, 17 Nov 2026), never with reduced motion, never without JavaScript: a pre-paint script in
 * app/[lang]/page.tsx (LOADER_SCRIPT, lib/loader.ts) sets <html data-loader="on"> only when it should play; CSS hides the
 * screen otherwise and also slides it away on its own after a few seconds if this component never runs.
 * Click, tap or any key skips it.
 */
const FADE_MS = 900; // the slide-up exit in app/globals.css

export default function SiteLoader({ label }: { label: string }) {
  const [active, setActive] = useState(false);
  const [out, setOut] = useState(false);
  const doneRef = useRef(false);

  useEffect(() => {
    if (document.documentElement.dataset.loader === "on") setActive(true);
  }, []);

  const finish = useCallback(() => {
    if (doneRef.current) return;
    doneRef.current = true;
    setOut(true);
    window.setTimeout(() => {
      document.documentElement.dataset.loader = "off";
      setActive(false);
    }, FADE_MS);
  }, []);

  useEffect(() => {
    if (!active) return;
    const skip = () => finish();
    window.addEventListener("keydown", skip);
    // hold the page still under the loader without hiding the scrollbar (hiding it shifted the layout)
    const hold = (e: Event) => e.preventDefault();
    window.addEventListener("wheel", hold, { passive: false });
    window.addEventListener("touchmove", hold, { passive: false });
    // a safety net: never hold the page for more than 6 s, whatever happens to the animation
    const id = window.setTimeout(finish, 6000);
    return () => {
      window.removeEventListener("keydown", skip);
      window.removeEventListener("wheel", hold);
      window.removeEventListener("touchmove", hold);
      window.clearTimeout(id);
    };
  }, [active, finish]);

  return (
    <div className={out ? "site-loader is-out" : "site-loader"} aria-hidden="true" onClick={finish}>
      {active && (
        <GlassIconReveal
          className="site-loader-glass"
          // the component sets position: relative inline, so the full-screen size must be inline too
          style={{ position: "absolute", inset: 0 }}
          logo="/media/brand/citix-x-1024.png"
          look="dark"
          originalColors
          loop={false}
          replayOnClick={false}
          speed={1.15}
          tileSize={240}
          tuning={DARK_GLASS}
          label={label}
          onDone={finish}
        />
      )}
    </div>
  );
}
