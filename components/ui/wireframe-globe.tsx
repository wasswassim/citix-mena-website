"use client";

import { geoGraticule10, geoOrthographic, geoPath, type GeoPermissibleObjects } from "d3-geo";
import { useEffect, useRef } from "react";
import { feature } from "topojson-client";
import type { GeometryCollection, Topology } from "topojson-specification";

/**
 * Wireframe globe (Wassim, 21 Nov 2026), rebuilt from the 21st.dev "Contact with globe" GlobeWireframe
 * (variant "wireframesolid": country outlines + sphere outline, d3 orthographic projection, world-atlas 110m).
 * Changes for this site:
 * - drawn on a <canvas> from a ref-driven loop (the original re-rendered the whole SVG through React state every frame)
 * - no Tailwind; styled by app/globals.css (.wglobe)
 * - map data from the world-atlas package, loaded as a separate chunk only when the globe nears the screen (no CDN)
 * - instead of a full spin it sways slowly around `center` (MENA), so the region never leaves the view
 * - `highlight` countries (ISO numeric ids) are tinted Pulse Red; `focus` glides the globe to a point
 * - `zoom`: the canvas is a window onto a sphere wider than it, so a region can fill the frame (canvas stays small)
 * - drag to turn (horizontal); the loop runs only while the globe is on screen
 * - reduced motion: no sway and no easing
 */
type LngLat = [number, number];
type Props = {
  center: LngLat; // [lng, lat] the globe faces at rest
  focus: LngLat | null; // [lng, lat] to glide to (a hovered country), or null to sway around center
  highlight: string[]; // ISO 3166 numeric ids, e.g. "784" for the UAE
  active: string | null; // the highlighted id drawn brighter
  markers: { location: LngLat; on: boolean }[];
  label: string;
  zoom?: number; // sphere diameter as a multiple of the canvas width (1 = the whole globe fits the width)
  top?: number; // gap above the sphere's top edge, in px
  className?: string;
};

type Shape = { id: string; geo: GeoPermissibleObjects };
type Atlas = Topology<{ countries: GeometryCollection<{ name: string }> }>;

const SWAY_DEG = 14; // amplitude either side of the center longitude
const SWAY_PERIOD = 48; // seconds for one full sway (the original turned ~27°/s; this peaks at ~1.8°/s)
const GLIDE_MS = 1400;

let atlasPromise: Promise<Shape[]> | null = null;
const loadAtlas = () =>
  (atlasPromise ??= import("world-atlas/countries-110m.json").then((m) => {
    const atlas = (m.default ?? m) as unknown as Atlas;
    const fc = feature(atlas, atlas.objects.countries);
    return fc.features.map((f) => ({ id: String(f.id), geo: f as GeoPermissibleObjects }));
  }));

const ease = (t: number) => (t < 0.5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2);

export function WireframeGlobe({ center, focus, highlight, active, markers, label, className, zoom = 1, top = 2 }: Props) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  // everything the draw loop reads lives in a ref, so prop changes never restart the loop
  const live = useRef({ center, focus, highlight, active, markers, zoom, top });
  live.current = { center, focus, highlight, active, markers, zoom, top };

  useEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!wrap || !canvas || !ctx) return;

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    const css = getComputedStyle(wrap);
    const color = (name: string, fallback: string) => css.getPropertyValue(name).trim() || fallback;
    const C = {
      line: color("--wglobe-line", "rgba(255,255,255,0.34)"),
      grid: color("--wglobe-grid", "rgba(255,255,255,0.07)"),
      rim: color("--wglobe-rim", "rgba(255,255,255,0.5)"),
      tint: color("--wglobe-tint", "rgba(253,3,50,0.22)"),
      tintOn: color("--wglobe-tint-on", "rgba(253,3,50,0.5)"),
      red: color("--wglobe-red", "#fd0332"),
    };

    const projection = geoOrthographic().precision(0.3);
    const path = geoPath(projection, ctx);
    const graticule = geoGraticule10();
    let shapes: Shape[] = [];
    let w = 0;
    let h = 0;
    let dpr = 1;

    // rotation state, in degrees: lng offset from the sway, and the glide between rest and focus
    let lng = -live.current.center[0];
    let lat = -live.current.center[1];
    let swayT0 = performance.now();
    let dragLng = 0;
    let glide: { from: LngLat; to: LngLat; t0: number } | null = null;
    let lastFocus: LngLat | null = null;

    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = wrap.clientWidth;
      h = wrap.clientHeight || w;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      // the canvas is only a window onto the sphere: with zoom > 1 its top arc fills the width
      const r = (w / 2) * live.current.zoom - 1;
      projection.translate([w / 2, live.current.top + r]).scale(r).clipExtent([[0, 0], [w, h]]);
    };

    const draw = () => {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      projection.rotate([lng + dragLng, lat]);
      const { highlight: hl, active: on, markers: mk } = live.current;

      ctx.beginPath();
      path(graticule);
      ctx.strokeStyle = C.grid;
      ctx.lineWidth = 1;
      ctx.stroke();

      for (const s of shapes) {
        if (!hl.includes(s.id)) continue;
        ctx.beginPath();
        path(s.geo);
        ctx.fillStyle = s.id === on ? C.tintOn : C.tint;
        ctx.fill();
      }

      ctx.beginPath();
      for (const s of shapes) path(s.geo);
      ctx.strokeStyle = C.line;
      ctx.lineWidth = 0.6;
      ctx.stroke();

      ctx.beginPath();
      path({ type: "Sphere" });
      ctx.strokeStyle = C.rim;
      ctx.lineWidth = 1.2;
      ctx.stroke();

      const [rl, rp] = projection.rotate();
      for (const m of mk) {
        // skip points on the far side (angular distance from the view center > 90°)
        const d = Math.acos(
          Math.sin((-rp * Math.PI) / 180) * Math.sin((m.location[1] * Math.PI) / 180) +
            Math.cos((-rp * Math.PI) / 180) *
              Math.cos((m.location[1] * Math.PI) / 180) *
              Math.cos(((m.location[0] + rl) * Math.PI) / 180),
        );
        if (d > Math.PI / 2) continue;
        const p = projection(m.location);
        if (!p) continue;
        const r = (m.on ? 5 : 3.2) * Math.min(1.4, live.current.zoom);
        ctx.beginPath();
        ctx.arc(p[0], p[1], r * 2.4, 0, Math.PI * 2);
        ctx.fillStyle = C.tint;
        ctx.fill();
        ctx.beginPath();
        ctx.arc(p[0], p[1], r, 0, Math.PI * 2);
        ctx.fillStyle = C.red;
        ctx.fill();
      }
    };

    let raf = 0;
    let visible = false;
    const frame = (now: number) => {
      raf = 0;
      const { center: c, focus: f } = live.current;
      const rest: LngLat = [-c[0], -c[1]];

      // a new focus (or its release) starts a glide from wherever the globe is now
      const key = f ? `${f[0]},${f[1]}` : null;
      const lastKey = lastFocus ? `${lastFocus[0]},${lastFocus[1]}` : null;
      if (key !== lastKey) {
        lastFocus = f;
        const target: LngLat = f ? [-f[0], -f[1]] : rest;
        glide = { from: [lng + dragLng, lat], to: target, t0: now };
        dragLng = 0;
      }

      if (glide) {
        const t = reduce.matches ? 1 : Math.min(1, (now - glide.t0) / GLIDE_MS);
        const e = ease(t);
        lng = glide.from[0] + (glide.to[0] - glide.from[0]) * e;
        lat = glide.from[1] + (glide.to[1] - glide.from[1]) * e;
        if (t >= 1) {
          glide = null;
          // the sway restarts from its middle so it continues smoothly from the rest position
          swayT0 = now;
        }
      } else if (!f && !reduce.matches && !dragging) {
        const s = Math.sin(((now - swayT0) / 1000 / SWAY_PERIOD) * Math.PI * 2);
        lng = rest[0] + s * SWAY_DEG;
        lat = rest[1];
      }

      draw();
      const moving = !!glide || (!f && !reduce.matches) || dragging;
      if (visible && moving) raf = requestAnimationFrame(frame);
    };
    const kick = () => {
      if (!raf && visible) raf = requestAnimationFrame(frame);
    };

    // drag to turn
    let dragging = false;
    let dragX = 0;
    let dragBase = 0;
    const down = (e: PointerEvent) => {
      dragging = true;
      dragX = e.clientX;
      dragBase = dragLng;
      canvas.setPointerCapture(e.pointerId);
      kick();
    };
    const move = (e: PointerEvent) => {
      if (!dragging) return;
      dragLng = dragBase + ((e.clientX - dragX) / w) * (180 / live.current.zoom);
      kick();
    };
    const up = () => {
      if (!dragging) return;
      dragging = false;
      // let go: glide back to the rest view (or the focused country)
      const f = live.current.focus;
      const c = live.current.center;
      glide = { from: [lng + dragLng, lat], to: f ? [-f[0], -f[1]] : [-c[0], -c[1]], t0: performance.now() };
      dragLng = 0;
      kick();
    };
    canvas.addEventListener("pointerdown", down);
    canvas.addEventListener("pointermove", move);
    canvas.addEventListener("pointerup", up);
    canvas.addEventListener("pointercancel", up);

    const ro = new ResizeObserver(() => {
      resize();
      draw();
    });
    ro.observe(wrap);
    resize();

    // load the map once the globe is within one screen of the viewport; animate only while it is on screen
    let loading = false;
    const io = new IntersectionObserver(
      ([entry]) => {
        const near = entry.isIntersecting;
        if (near && !loading) {
          loading = true;
          loadAtlas()
            .then((s) => {
              shapes = s;
              canvas.classList.add("is-ready");
              draw();
              kick();
            })
            .catch(() => canvas.classList.add("is-ready"));
        }
        visible = near;
        if (visible) kick();
        else if (raf) {
          cancelAnimationFrame(raf);
          raf = 0;
        }
      },
      { rootMargin: "100% 0px", threshold: [0, 0.01] },
    );
    io.observe(wrap);

    const onReduce = () => kick();
    reduce.addEventListener("change", onReduce);
    const props = () => kick();
    wrap.addEventListener("wglobe:update", props);

    return () => {
      cancelAnimationFrame(raf);
      io.disconnect();
      ro.disconnect();
      reduce.removeEventListener("change", onReduce);
      wrap.removeEventListener("wglobe:update", props);
      canvas.removeEventListener("pointerdown", down);
      canvas.removeEventListener("pointermove", move);
      canvas.removeEventListener("pointerup", up);
      canvas.removeEventListener("pointercancel", up);
    };
  }, []);

  // a prop change (hover) wakes the loop, which may be idle in reduced motion
  useEffect(() => {
    wrapRef.current?.dispatchEvent(new Event("wglobe:update"));
  }, [focus, active, markers]);

  return (
    <div ref={wrapRef} className={className ? `wglobe ${className}` : "wglobe"}>
      <canvas ref={canvasRef} className="wglobe-canvas" role="img" aria-label={label} />
    </div>
  );
}
