"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

/**
 * Route 1 test (14 Nov 2026): the orbit as REAL 3D, so the geometry is exact by construction.
 *  - Tom is a real box at the centre of a circle.
 *  - The camera is a point on that circle (fixed radius, fixed height), always looking at the centre,
 *    travelling at one constant angular speed.
 *  - Black dune hills stand on the camera's path: they wipe the lens to black as the camera passes.
 * Content: the falcon is a generated video plate on black (keyed in the shader); the sand stream is particles.
 * Both leave the lower screen while the orbit runs.
 *
 * URL params:  ?t=3.5  freeze at 3.5 s (for measurements)   ?speed=8  degrees per second   ?debug=1  show numbers
 */

const LOOP = 8; // seconds per rotation
const R = 26; // camera circle radius (m)
const CAM_H = 1.5; // camera height (m)
const LOOK_Y = 3.6; // the camera always aims at this point on Tom's axis
const TOM = { w: 2, h: 5.9, d: 0.24, plinthH: 1.1, plinthW: 1.2 };
const START_DEG = 82; // angle from the screen's normal at t = 0 (almost edge-on, on the red-strip side)

export default function OrbitLab() {
  const mountRef = useRef<HTMLDivElement>(null);
  const hudRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;
    const params = new URLSearchParams(window.location.search);
    const frozen = params.has("t") ? Number(params.get("t")) : null;
    const speedDeg = Number(params.get("speed")) || 8.5; // inspiration: about 65 degrees in 8 s
    const debug = params.has("debug") || frozen !== null;

    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x020306);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    // The drawing buffer is sized in device pixels; the element itself must always fit the window,
    // otherwise the picture is cropped on screens with display scaling (125 %, 150 %, ...).
    Object.assign(renderer.domElement.style, { display: "block", width: "100%", height: "100%" });
    mount.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x020306, 0.02);
    const camera = new THREE.PerspectiveCamera(31, 16 / 9, 0.1, 400);

    // ---------- ground: dark sand, only visible where the screen lights it
    const sandCanvas = document.createElement("canvas");
    sandCanvas.width = sandCanvas.height = 512;
    const sctx = sandCanvas.getContext("2d")!;
    const img = sctx.createImageData(512, 512);
    for (let i = 0; i < 512 * 512; i++) {
      const x = i % 512;
      const y = (i / 512) | 0;
      const ripple = Math.sin((x + Math.sin(y / 23) * 14) / 5.5) * 0.5 + 0.5;
      const v = 105 + ripple * 60 + Math.random() * 55;
      img.data.set([v, v, v, 255], i * 4);
    }
    sctx.putImageData(img, 0, 0);
    const sandTex = new THREE.CanvasTexture(sandCanvas);
    sandTex.wrapS = sandTex.wrapT = THREE.RepeatWrapping;
    sandTex.repeat.set(60, 60);
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(400, 400),
      new THREE.MeshStandardMaterial({ color: 0x8f97a6, map: sandTex, bumpMap: sandTex, bumpScale: 0.6, roughness: 1 }),
    );
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    // ---------- Tom (old Tom): body box, front texture from the real cut-out, plinth, red side strip
    const tom = new THREE.Group();
    scene.add(tom);
    const black = new THREE.MeshStandardMaterial({ color: 0x08090b, roughness: 0.55, metalness: 0.3 });
    const body = new THREE.Mesh(new THREE.BoxGeometry(TOM.w, TOM.h, TOM.d), black);
    body.position.y = TOM.plinthH + TOM.h / 2;
    tom.add(body);
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(TOM.plinthW, TOM.plinthH, TOM.d * 0.9), black);
    plinth.position.set(TOM.w / 2 - TOM.plinthW / 2, TOM.plinthH / 2, 0);
    tom.add(plinth);
    const frontTex = new THREE.TextureLoader().load("/media/lab/tom_front.png");
    frontTex.colorSpace = THREE.SRGBColorSpace;
    const front = new THREE.Mesh(
      new THREE.PlaneGeometry(TOM.w, TOM.h),
      new THREE.MeshBasicMaterial({ map: frontTex, transparent: true, alphaTest: 0.5, toneMapped: false, fog: false, color: 0xdfe9ff }),
    );
    front.position.set(0, TOM.plinthH + TOM.h / 2, TOM.d / 2 + 0.005);
    tom.add(front);
    const strip = new THREE.Mesh(
      new THREE.BoxGeometry(0.02, TOM.h + TOM.plinthH - 0.1, 0.05),
      new THREE.MeshBasicMaterial({ color: 0xfd0332, toneMapped: false, fog: false }),
    );
    strip.position.set(TOM.w / 2 + 0.011, (TOM.h + TOM.plinthH) / 2, 0.04);
    tom.add(strip);

    // ---------- light from the screens: pool on the sand + a faint volumetric shaft
    const spot = new THREE.SpotLight(0xcfe0ff, 420, 34, 1.05, 1, 1.9);
    spot.position.set(0, 4.4, 0.5);
    spot.target.position.set(0, 0, 5.5);
    scene.add(spot, spot.target);
    scene.add(new THREE.HemisphereLight(0x2b4070, 0x000000, 0.1)); // faint moon rim on the sand
    const rim = new THREE.DirectionalLight(0x8fb0ff, 0.55); // cool moon edge light so the black body reads
    rim.position.set(-14, 9, -6);
    scene.add(rim);
    const shaftCanvas = document.createElement("canvas");
    shaftCanvas.width = shaftCanvas.height = 256;
    const g = shaftCanvas.getContext("2d")!;
    const shaftImg = g.createImageData(256, 256);
    for (let i = 0; i < 256 * 256; i++) {
      const u = (i % 256) / 255;
      const v = ((i / 256) | 0) / 255; // 0 at the screen, 1 far out on the sand
      const edge = Math.pow(Math.sin(u * Math.PI), 1.6); // soft sides
      const alpha = edge * Math.pow(1 - v, 1.8) * 0.2;
      shaftImg.data.set([190, 215, 255, alpha * 255], i * 4);
    }
    g.putImageData(shaftImg, 0, 0);
    const shaftMat = new THREE.MeshBasicMaterial({
      map: new THREE.CanvasTexture(shaftCanvas),
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      side: THREE.DoubleSide,
      fog: false,
    });
    // two crossed soft beams read as a volume from any orbit angle
    for (const tilt of [0.36, 0.2]) {
      const shaft = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 10), shaftMat);
      shaft.position.set(0, 2.6 - tilt * 2.4, 5.1);
      shaft.rotation.x = -Math.PI / 2 + tilt;
      scene.add(shaft);
    }

    // ---------- black dunes on the camera's circle: they pass the lens and wipe to black
    const duneMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
    const duneAt = (deg: number) => {
      const a = THREE.MathUtils.degToRad(deg);
      const dune = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), duneMat);
      dune.scale.set(5.5, 3.4, 2.2);
      dune.position.set(Math.sin(a) * (R - 3.2), 0, Math.cos(a) * (R - 3.2));
      dune.rotation.y = a;
      scene.add(dune);
    };
    duneAt(START_DEG + 1.5); // the shot starts behind this one
    duneAt(START_DEG - speedDeg * LOOP - 1.5); // and ends behind this one

    // ---------- content: falcon sprite + sand stream leaving the lower screen
    // Falcon = generated plate on pure black (scripts/orbit_plates.py), keyed by luminance in the shader.
    const falconVideo = document.createElement("video");
    falconVideo.src = "/media/lab/falcon_plate.mp4";
    falconVideo.muted = true;
    falconVideo.loop = true;
    falconVideo.playsInline = true;
    falconVideo.preload = "auto";
    const falconTex = new THREE.VideoTexture(falconVideo);
    falconTex.colorSpace = THREE.SRGBColorSpace;
    const falconMat = new THREE.ShaderMaterial({
      uniforms: { map: { value: falconTex }, opacity: { value: 0 } },
      transparent: true,
      depthWrite: false,
      toneMapped: false,
      vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
      fragmentShader: [
        "uniform sampler2D map; uniform float opacity; varying vec2 vUv;",
        "void main(){",
        "  vec4 c = texture2D(map, vUv);",
        "  float key = smoothstep(0.012, 0.06, max(c.r, max(c.g, c.b)));", // black -> transparent (values are linear)
        "  float edge = smoothstep(0.0, 0.04, vUv.x) * smoothstep(1.0, 0.96, vUv.x);", // hide wingtips touching the plate edge
        "  gl_FragColor = vec4(c.rgb * vec3(0.66, 0.76, 0.94), key * edge * opacity);", // lit by the cool screen behind it
        "  #include <colorspace_fragment>",
        "}",
      ].join("\n"),
    });
    const falcon = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 5.2 * (1080 / 1912)), falconMat);
    scene.add(falcon);
    if (frozen === null) void falconVideo.play().catch(() => undefined);
    const screenOrigin = new THREE.Vector3(0, TOM.plinthH + TOM.h * 0.27, TOM.d / 2 + 0.05); // lower screen centre

    const N = 2600;
    const pos = new Float32Array(N * 3);
    const seed = new Float32Array(N * 4);
    for (let i = 0; i < N; i++) seed.set([Math.random(), Math.random(), Math.random(), Math.random()], i * 4);
    const sandGeo = new THREE.BufferGeometry();
    sandGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const sand = new THREE.Points(
      sandGeo,
      new THREE.PointsMaterial({ color: 0xb9c8e6, size: 0.07, fog: false, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending }),
    );
    sand.frustumCulled = false;
    scene.add(sand);

    const ease = (x: number) => x * x * (3 - 2 * x);
    const T0 = 1.6; // content starts leaving the screen at this time, while the orbit runs
    const update = (t: number) => {
      // camera: a point on the circle, constant angular speed, always aimed at Tom's axis
      const a = THREE.MathUtils.degToRad(START_DEG - speedDeg * t);
      camera.position.set(Math.sin(a) * R, CAM_H, Math.cos(a) * R);
      camera.lookAt(0, LOOK_Y, 0);

      // falcon: out of the lower screen, forward and up, then past the camera's side
      const k = THREE.MathUtils.clamp((t - T0) / 4.6, 0, 1);
      const out = ease(k);
      falcon.position.set(screenOrigin.x - 1.2 * out - 9 * out * out, screenOrigin.y + 0.4 * out + 1.6 * out * out, screenOrigin.z + 0.2 + 19 * out);
      const grow = THREE.MathUtils.clamp(k * 5, 0.02, 1);
      falcon.scale.set(grow, grow, 1);
      falcon.lookAt(camera.position);
      falconMat.uniforms.opacity.value = k <= 0 ? 0 : THREE.MathUtils.clamp((1 - k) * 6, 0, 1);
      if (frozen !== null && falconVideo.readyState >= 1) {
        const want = ((((t - T0) % 4) + 4) % 4);
        if (Math.abs(falconVideo.currentTime - want) > 0.02) falconVideo.currentTime = want; // freeze mode: seek the plate
      }

      // sand stream: pours out of the lower screen and fans across the ground toward +z
      for (let i = 0; i < N; i++) {
        const [s1, s2, s3, s4] = [seed[i * 4], seed[i * 4 + 1], seed[i * 4 + 2], seed[i * 4 + 3]];
        const life = 2.6;
        const age = (((t - T0) / life + s1) % 1) * life;
        const born = t - age;
        const on = born >= T0 - 0.2 && t >= T0 ? 1 : 0;
        const vx = (s2 - 0.5) * 1.6;
        const vz = 2.2 + s3 * 3.2;
        const y = screenOrigin.y - 0.9 + (s4 - 0.5) * 1.6 - 1.9 * age * age + 0.3 * age;
        pos[i * 3] = on ? screenOrigin.x + (s2 - 0.5) * 1.2 + vx * age : 0;
        pos[i * 3 + 1] = on ? Math.max(0.03, y) : -5;
        pos[i * 3 + 2] = on ? screenOrigin.z + vz * age : 0;
      }
      sandGeo.attributes.position.needsUpdate = true;
    };

    const resize = () => {
      const w = mount.clientWidth;
      const h = mount.clientHeight;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      // lens shift: Tom sits about two-thirds across the frame (centred on portrait screens), camera still aims at him
      const shift = w > h ? -0.17 : 0;
      camera.setViewOffset(w, h, shift * w, 0, w, h);
      camera.updateProjectionMatrix();
    };
    resize();
    window.addEventListener("resize", resize);

    // numbers for verification: Tom's projected position and height on screen
    const top = new THREE.Vector3();
    const base = new THREE.Vector3();
    const measure = (t: number) => {
      top.set(0, TOM.plinthH + TOM.h, 0).project(camera);
      base.set(0, 0, 0).project(camera);
      const m = {
        t: +t.toFixed(2),
        angleDeg: +(START_DEG - speedDeg * t).toFixed(2),
        radius: +camera.position.distanceTo(new THREE.Vector3(0, CAM_H, 0)).toFixed(3),
        tomX: +(((top.x + base.x) / 4 + 0.5) * 100).toFixed(2), // % of frame width
        tomHeight: +(((top.y - base.y) / 2) * 100).toFixed(2), // % of frame height
      };
      (window as unknown as { __orbit: unknown }).__orbit = m;
      return m;
    };
    (window as unknown as { __orbitAt: (t: number) => unknown }).__orbitAt = (t: number) => {
      update(t);
      camera.updateMatrixWorld();
      renderer.render(scene, camera);
      return measure(t);
    };

    let raf = 0;
    let running = true;
    const start = performance.now();
    const tick = () => {
      if (!running) return;
      const t = frozen ?? ((performance.now() - start) / 1000) % LOOP;
      update(t);
      renderer.render(scene, camera);
      const m = measure(t);
      if (debug && hudRef.current) hudRef.current.textContent = JSON.stringify(m);
      raf = requestAnimationFrame(tick);
    };
    const onVis = () => {
      running = !document.hidden;
      if (running) raf = requestAnimationFrame(tick);
    };
    document.addEventListener("visibilitychange", onVis);
    raf = requestAnimationFrame(tick);

    return () => {
      running = false;
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      document.removeEventListener("visibilitychange", onVis);
      falconVideo.pause();
      falconVideo.removeAttribute("src");
      renderer.dispose();
      mount.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div style={{ position: "fixed", inset: 0, background: "#000" }}>
      <div ref={mountRef} style={{ position: "absolute", inset: 0 }} />
      <pre ref={hudRef} style={{ position: "absolute", left: 12, bottom: 8, margin: 0, color: "#9fb4d8", font: "12px monospace" }} />
    </div>
  );
}
