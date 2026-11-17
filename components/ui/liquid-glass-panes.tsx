"use client";

import { type RefObject, useEffect, useRef } from "react";
import { DARK_GLASS, GLSL_COMMON } from "@/lib/liquid-glass";

/**
 * Liquid glass panes (Wassim, 17 Nov 2026): the hero's Ecosystem cards made of the same glass as the loading screen.
 * One small WebGL2 canvas sits behind the cards (above the hero's 50% overlay) and, for each card, draws a
 * superellipse tile of glass that refracts the live hero video: the same rounded-edge Snell refraction, colour
 * dispersion, rim light, specular and sheen as components/ui/liquid-glass-logo-reveal.tsx (shared GLSL in
 * lib/liquid-glass.ts). The face is frosted (blurred video) so the white text stays readable.
 *
 * Source: the hero <video> while it plays, else the poster <img> (reduced motion keeps the poster: drawn once).
 * Runs only while the hero is on screen and the tab is visible. `onReady(true)` fires after the first frame,
 * so the CSS glass stays as the fallback when WebGL2 is missing or anything fails.
 */
const MAX_CARDS = 3;
const MARGIN = 28;
const CARD_N = 8.8; // CSS px around the cards for the drop shadow

const VERT = `#version 300 es
in vec2 aPos;
void main() { gl_Position = vec4(aPos, 0.0, 1.0); }`;

const FRAG = `#version 300 es
precision highp float;
out vec4 outColor;

uniform sampler2D uScene;
uniform vec2 uRes;          // canvas size, device px
uniform vec2 uVidOff;       // where the cover-fitted video's top-left sits, canvas device px (y down)
uniform vec2 uVidSize;      // its drawn size, device px
uniform float uShade;       // the hero overlay: the scene is seen at this brightness
uniform int uCount;
uniform vec4 uCards[${MAX_CARDS}];  // centre x, centre y (y down), side, sweep position
uniform float uSlab;
uniform float uOptics;
uniform float uShapeN;
uniform float uBevelW;
uniform float uCornerPull;
uniform float uCornerWidth;
uniform float uDisp;
uniform float uStreak;
uniform float uDouble;
uniform float uSpec;
uniform float uSheen;
uniform float uFrostLod;

float px;
${GLSL_COMMON}

vec3 sceneAt(vec2 q, vec2 c, float side, float lod) {
  // plate units -> canvas px (y down) -> video uv
  vec2 pos = c + vec2(q.x, -q.y) * side * 0.5;
  vec2 uv = (pos - uVidOff) / uVidSize;
  return textureLod(uScene, clamp(uv, 0.001, 0.999), lod).rgb * uShade;
}

void main() {
  vec2 frag = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y);
  vec4 col = vec4(0.0);
  float shadow = 0.0;

  for (int k = 0; k < ${MAX_CARDS}; k++) {
    if (k >= uCount) break;
    vec4 cd = uCards[k];
    vec2 c = cd.xy;
    float side = cd.z;
    px = 2.0 / side;
    vec2 p = (frag - c) * px;
    p.y = -p.y;

    vec2 nOut, dg; float g;
    float sd = shape(p, 1.0, uShapeN, nOut, g, dg);

    // soft drop shadow below the tile
    vec2 ps = p - vec2(0.0, -0.12);
    vec2 sn, sdg; float sg;
    float ssd = shape(ps, 1.04, uShapeN, sn, sg, sdg);
    shadow = max(shadow, 0.42 * exp(-max(ssd, 0.0) / 0.16));

    if (sd > px) continue;

    float s = -sd;
    float bw = uBevelW;
    float x = clamp(s / bw, 0.0, 1.0);
    float R = contourRadius(p, 1.0, uShapeN);
    vec2 pq = p * p;
    float diag = 4.0 * pq.x * pq.y / max((pq.x + pq.y) * (pq.x + pq.y), 1e-6);
    vec2 dirOut = normalize(mix(nOut, p / max(length(p), 1e-4), 0.2));
    float cornerness = max(smoothstep(0.1, 0.9, 4.0 * nOut.x * nOut.x * nOut.y * nOut.y), smoothstep(0.15, 0.75, diag));
    float offMul = 1.0 + 0.4 * max(uCornerPull - 1.0, 0.0) * cornerness;
    float bwF = bw * (1.0 + uCornerWidth * cornerness);
    float xf = clamp(s / bwF, 0.0, 1.0);

    // rounded-edge normal (same profile as the reveal)
    float y1 = 1.0 - x;
    const float K = 2.6;
    float base1 = max(1.0 - pow(y1, K), 1e-4);
    float db = min(pow(y1, K - 1.0) * pow(base1, 1.0 / K - 1.0), 25.0);
    float s1 = bw * 0.62;
    float w2 = bw * 0.22;
    float t2 = clamp((s - s1) / w2, -1.0, 1.0);
    float dh2 = uDouble * bw * 0.16;
    float dd = dh2 * 0.5 * cos(t2 * 1.5707963) * 1.5707963 / w2 * step(abs(t2), 0.999);
    vec2 grad = -(db + dd) * nOut;

    // frosted face, sharper toward the rim where the refraction shows
    float lod = mix(uFrostLod * 0.45, uFrostLod, smoothstep(0.0, 1.0, xf));
    float streak = 0.35 * uStreak * bw * mix(0.15, 1.0, cornerness) * pow(1.0 - xf, 1.5);
    vec2 tangent = vec2(-nOut.y, nOut.x);
    vec3 acc = vec3(0.0), wsum = vec3(0.0);
    for (int i = 0; i < 10; i++) {
      float lam = (float(i) + 0.5) / 10.0;
      float cc = uDisp * (1.0 - 2.0 * lam);
      vec2 along = tangent * (streak * 2.0 * (fract(float(i) * 0.618034 + 0.31) - 0.5));
      vec2 sp = refractSample(xf, bwF, 1.5 + 0.06 * cc, R, dirOut, p + along, 0.0, offMul);
      vec3 w = spectrum(lam);
      acc += sceneAt(sp, c, side, lod) * w;
      wsum += w;
    }
    vec3 trans = acc / wsum;
    // the glass body: a touch brighter and clearer than the shaded scene around it (keeps text legible)
    trans = trans * 1.18 + vec3(0.035);
    // light caught in the body from the top-left, like the old CSS glass gradient
    trans += vec3(0.07) * clamp(0.5 + 0.5 * dot(p, normalize(vec2(-0.6, 0.8))), 0.0, 1.0) * x;

    vec3 Nl = normalize(vec3(-grad, 1.0));
    float edge = 1.0 - Nl.z;
    vec2 ldir = normalize(vec2(-0.62, 0.78));
    float side2 = dot(nOut, ldir);
    float fres = pow(edge, 1.5);
    vec3 rimCol = vec3(0.80, 0.87, 0.97);
    vec3 rim = rimCol * fres * (0.35 + 0.65 * max(side2, -side2 * 0.8)) * 0.65;
    vec3 Hv = normalize(normalize(vec3(-0.45, 0.6, 0.66)) + vec3(0.0, 0.0, 1.0));
    float spc = pow(max(dot(Nl, Hv), 0.0), 140.0) * 0.8 * smoothstep(0.0, 0.25, y1);
    float edgeLine = gauss(s, 0.012, 0.008);
    vec3 glass = trans * (1.0 - 0.25 * fres) + (rim + vec3(spc)) * uSpec + rimCol * 0.22 * edgeLine * (0.4 + 0.6 * max(side2, 0.0));

    float sweepD = dot(p, normalize(vec2(0.8, 0.6))) - cd.w;
    float sheen = uSheen * exp(-sweepD * sweepD / 0.03) * (0.55 + 0.45 * (1.0 - x));
    glass = mix(glass, vec3(1.0), sheen * 0.22);

    float cov = clamp(0.5 - sd / px, 0.0, 1.0);
    col = vec4(glass, 1.0) * cov + col * (1.0 - cov);
  }

  // shadow under the glass (premultiplied black)
  float a = col.a + shadow * (1.0 - col.a);
  outColor = vec4(col.rgb, a);
}`;

type Props = {
  /** The card elements to put glass behind (same order every frame) */
  cards: RefObject<(HTMLElement | null)[]>;
  /** The element the canvas covers (the cards' row) */
  frame: RefObject<HTMLElement | null>;
  /** Called with true once the glass draws, false if it stops (so the CSS glass can come back) */
  onReady: (ok: boolean) => void;
  /** Sheen: performance.now() / 1000 when a light should start sweeping across card i */
  sweepAt?: RefObject<number[]>;
};

export function LiquidGlassPanes({ cards, frame, onReady, sweepAt }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const readyRef = useRef(onReady);
  useEffect(() => {
    readyRef.current = onReady;
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    const box = frame.current;
    const hero = canvas?.closest(".hero");
    if (!canvas || !box || !hero) return;
    const gl = canvas.getContext("webgl2", { antialias: false, premultipliedAlpha: true, alpha: true });
    if (!gl) return;

    let prog: WebGLProgram;
    try {
      const compile = (type: number, src: string) => {
        const sh = gl.createShader(type)!;
        gl.shaderSource(sh, src);
        gl.compileShader(sh);
        if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh) || "shader");
        return sh;
      };
      prog = gl.createProgram()!;
      gl.attachShader(prog, compile(gl.VERTEX_SHADER, VERT));
      gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FRAG));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog) || "program");
    } catch (err) {
      console.error(err);
      return;
    }
    gl.useProgram(prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const aPos = gl.getAttribLocation(prog, "aPos");
    gl.enableVertexAttribArray(aPos);
    gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
    const U = (n: string) => gl.getUniformLocation(prog, n);

    const G = DARK_GLASS;
    gl.uniform1f(U("uSlab"), 0.3 * G.opticalDepth);
    gl.uniform1f(U("uOptics"), 1);
    // the cards' original corner curve (Wassim, 17 Nov 2026): CSS border-radius 13% of the side. A superellipse of
    // power 8.8 passes through the same corner point (2^(-1/n) = 1 - r + r/sqrt(2), r = 0.26 in half-side units)
    gl.uniform1f(U("uShapeN"), CARD_N);
    gl.uniform1f(U("uBevelW"), G.bevelWidth);
    gl.uniform1f(U("uCornerPull"), G.cornerPull);
    gl.uniform1f(U("uCornerWidth"), G.cornerWidth);
    gl.uniform1f(U("uDisp"), G.dispersion);
    gl.uniform1f(U("uStreak"), G.edgeSmear);
    gl.uniform1f(U("uDouble"), G.doubleBevel);
    gl.uniform1f(U("uSpec"), G.specular);
    gl.uniform1f(U("uSheen"), G.sheen);
    gl.uniform1f(U("uShade"), 0.5); // .hero-overlay is rgb(0 0 0 / 0.5)
    gl.uniform1i(U("uScene"), 0);
    const uRes = U("uRes");
    const uVidOff = U("uVidOff");
    const uVidSize = U("uVidSize");
    const uCount = U("uCount");
    const uCards = U("uCards");
    const uFrostLod = U("uFrostLod");

    const tex = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

    let srcW = 0;
    let srcH = 0;
    let lastImg: HTMLImageElement | null = null;
    let lastVideoTime = -1;
    let visible = false;
    let raf = 0;
    let drawn = false;
    let lost = false;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const upload = (): boolean => {
      const video = hero.querySelector<HTMLVideoElement>(".hero-media video.is-playing");
      if (video && video.readyState >= 2 && video.videoWidth) {
        if (video.currentTime === lastVideoTime) return true;
        lastVideoTime = video.currentTime;
        try {
          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, video);
        } catch {
          return false;
        }
        srcW = video.videoWidth;
        srcH = video.videoHeight;
        lastImg = null;
        gl.generateMipmap(gl.TEXTURE_2D);
        return true;
      }
      const img = hero.querySelector<HTMLImageElement>(".hero-media img");
      if (img && img.complete && img.naturalWidth) {
        if (img === lastImg) return true;
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, img);
        gl.generateMipmap(gl.TEXTURE_2D);
        srcW = img.naturalWidth;
        srcH = img.naturalHeight;
        lastImg = img;
        lastVideoTime = -1;
        return true;
      }
      return false;
    };

    const cardData = new Float32Array(MAX_CARDS * 4);
    const draw = (now: number) => {
      if (lost || !upload()) return false;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const cr = canvas.getBoundingClientRect();
      const w = Math.max(1, Math.round(cr.width * dpr));
      const h = Math.max(1, Math.round(cr.height * dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
      // cover fit of the scene inside the hero media box
      const media = hero.querySelector<HTMLElement>(".hero-media") ?? hero;
      const mr = media.getBoundingClientRect();
      const s = Math.max(mr.width / srcW, mr.height / srcH);
      const dw = srcW * s;
      const dh = srcH * s;
      const ox = mr.left + (mr.width - dw) / 2 - cr.left;
      const oy = mr.top + (mr.height - dh) / 2 - cr.top;

      const list = cards.current ?? [];
      let n = 0;
      let side = 0;
      const t = now / 1000;
      for (const el of list) {
        if (!el || n >= MAX_CARDS) continue;
        const r = el.getBoundingClientRect();
        side = r.width * dpr;
        cardData[n * 4] = (r.left + r.width / 2 - cr.left) * dpr;
        cardData[n * 4 + 1] = (r.top + r.height / 2 - cr.top) * dpr;
        cardData[n * 4 + 2] = side;
        // sheen: a light passes across each card after its words change (sweepAt holds the trigger times)
        const t0 = sweepAt?.current?.[n] ?? -10;
        const k = Math.min(1, Math.max(0, (t - t0) / 1.4));
        const ease = k * k * (3 - 2 * k);
        cardData[n * 4 + 3] = reduced ? -3 : -1.8 + 3.6 * ease;
        n++;
      }
      gl.viewport(0, 0, w, h);
      gl.uniform2f(uRes, w, h);
      gl.uniform2f(uVidOff, ox * dpr, oy * dpr);
      gl.uniform2f(uVidSize, dw * dpr, dh * dpr);
      gl.uniform1i(uCount, n);
      gl.uniform4fv(uCards, cardData);
      // frost ≈ the old 22 px CSS blur, in texture mip levels: texels per device px decide the base level
      const texelsPerPx = srcW / (dw * dpr);
      gl.uniform1f(uFrostLod, Math.log2(Math.max(1, (22 * dpr) * texelsPerPx)) + 0.3);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      return true;
    };

    const tick = (now: number) => {
      raf = 0;
      const ok = draw(now);
      if (ok && !drawn) {
        drawn = true;
        readyRef.current(true);
      }
      // reduced motion: the poster never changes, so one good frame is enough (resizes redraw it)
      if (visible && !document.hidden && (!reduced || !ok)) raf = requestAnimationFrame(tick);
    };
    const kick = () => {
      if (!raf && visible && !document.hidden) raf = requestAnimationFrame(tick);
    };

    const io = new IntersectionObserver(([e]) => {
      visible = e.isIntersecting;
      if (visible) kick();
      else if (raf) {
        cancelAnimationFrame(raf);
        raf = 0;
      }
    });
    io.observe(hero);
    const ro = new ResizeObserver(kick);
    ro.observe(box);
    const onVis = () => kick();
    document.addEventListener("visibilitychange", onVis);
    const onLost = (e: Event) => {
      e.preventDefault();
      lost = true;
      drawn = false;
      readyRef.current(false);
    };
    canvas.addEventListener("webglcontextlost", onLost);

    return () => {
      if (raf) cancelAnimationFrame(raf);
      io.disconnect();
      ro.disconnect();
      document.removeEventListener("visibilitychange", onVis);
      canvas.removeEventListener("webglcontextlost", onLost);
      readyRef.current(false);
      gl.getExtension("WEBGL_lose_context")?.loseContext();
    };
  }, [cards, frame, sweepAt]);

  return <canvas ref={canvasRef} className="eco-glass" aria-hidden="true" style={{ inset: -MARGIN }} />;
}

export default LiquidGlassPanes;
