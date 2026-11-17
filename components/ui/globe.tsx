"use client";

import createGlobe, { type Globe as CobeGlobe, type Marker } from "cobe";
import { useEffect, useRef } from "react";

/**
 * Globe (from the 21st.dev "Globe" component, MIT, built on cobe), adapted for this site (17 Nov 2026):
 * - no Tailwind / shadcn: plain class names, styled in app/globals.css (.globe, .globe-canvas)
 * - cobe v2 API: our own animation loop drives globe.update(); the loop only runs while the globe is on screen
 * - `focus` turns the globe to a [lat, lng] (used when a country name is hovered); otherwise it spins slowly
 * - drag to spin, as in the original; reduced motion: no auto-spin and no easing, it jumps to the focus
 * - brand colours (dark graphite globe, Pulse Red markers) are passed in by the section
 */
type Props = {
  markers: Marker[];
  focus: [number, number] | null;
  label: string;
  className?: string;
  baseColor?: [number, number, number];
  markerColor?: [number, number, number];
  glowColor?: [number, number, number];
};

const TAU = Math.PI * 2;
// cobe's own "focus" maths: longitude -> phi, latitude -> theta
const toAngles = ([lat, lng]: [number, number]): [number, number] => [
  Math.PI - ((lng * Math.PI) / 180 - Math.PI / 2),
  (lat * Math.PI) / 180,
];
const shortest = (d: number) => ((((d + Math.PI) % TAU) + TAU) % TAU) - Math.PI;

export function Globe({
  markers,
  focus,
  label,
  className,
  baseColor = [0.16, 0.16, 0.16],
  markerColor = [253 / 255, 3 / 255, 50 / 255],
  glowColor = [0.12, 0.12, 0.12],
}: Props) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const markersRef = useRef(markers);
  const focusRef = useRef(focus);

  useEffect(() => {
    markersRef.current = markers;
    focusRef.current = focus;
  }, [markers, focus]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    if (!canvas || !wrap) return;

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    // start facing the Gulf
    let [phi, theta] = toAngles([28, 52]);
    theta = 0.3;
    let width = canvas.offsetWidth;
    let globe: CobeGlobe | null = null;
    let raf = 0;
    const drag = { active: false, x: 0, phi: 0 };

    const frame = () => {
      const f = focusRef.current;
      if (f && !drag.active) {
        const [tp, tt] = toAngles(f);
        const target = Math.min(0.75, Math.max(0.1, tt * 0.85));
        const ease = reduced ? 1 : 0.07;
        phi += shortest(tp - phi) * ease;
        theta += (target - theta) * ease;
      } else if (!drag.active) {
        if (!reduced) phi += 0.0025;
        theta += (0.3 - theta) * 0.03;
      }
      globe?.update({ phi, theta, width, height: width, markers: markersRef.current });
      raf = requestAnimationFrame(frame);
    };

    const start = () => {
      if (!globe) {
        width = canvas.offsetWidth;
        globe = createGlobe(canvas, {
          devicePixelRatio: dpr,
          width,
          height: width,
          phi,
          theta,
          dark: 1,
          diffuse: 1.2,
          mapSamples: 16000,
          mapBrightness: 5,
          baseColor,
          markerColor,
          glowColor,
          markers: markersRef.current,
          markerElevation: 0.01,
        });
        requestAnimationFrame(() => canvas.classList.add("is-ready"));
      }
      if (!raf) raf = requestAnimationFrame(frame);
    };
    const stop = () => {
      cancelAnimationFrame(raf);
      raf = 0;
    };

    // build the globe only near the viewport, and pause the loop when it leaves
    const io = new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop()), { rootMargin: "200px" });
    io.observe(wrap);

    const onResize = () => {
      width = canvas.offsetWidth;
    };
    window.addEventListener("resize", onResize);

    const down = (e: PointerEvent) => {
      drag.active = true;
      drag.x = e.clientX;
      drag.phi = phi;
      canvas.setPointerCapture(e.pointerId);
      canvas.style.cursor = "grabbing";
    };
    const move = (e: PointerEvent) => {
      if (drag.active) phi = drag.phi + (e.clientX - drag.x) / 200;
    };
    const up = () => {
      drag.active = false;
      canvas.style.cursor = "";
    };
    canvas.addEventListener("pointerdown", down);
    canvas.addEventListener("pointermove", move);
    canvas.addEventListener("pointerup", up);
    canvas.addEventListener("pointercancel", up);

    return () => {
      stop();
      io.disconnect();
      window.removeEventListener("resize", onResize);
      canvas.removeEventListener("pointerdown", down);
      canvas.removeEventListener("pointermove", move);
      canvas.removeEventListener("pointerup", up);
      canvas.removeEventListener("pointercancel", up);
      globe?.destroy();
    };
    // colours are fixed for the life of the globe
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div ref={wrapRef} className={className ? `globe ${className}` : "globe"} role="img" aria-label={label}>
      <canvas ref={canvasRef} className="globe-canvas" />
    </div>
  );
}
