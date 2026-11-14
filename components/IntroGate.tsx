"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import styles from "./IntroGate.module.css";

import { INTRO_SEEN_KEY } from "@/lib/intro";

type Line = { text: string; from: number; to: number };

type Props = {
  label: string;
  siteName: string;
  lines: Line[];
  enterLabel: string;
  skipLabel: string;
  unmuteLabel: string;
  muteLabel: string;
  soundUnavailableLabel: string;
  /** Audio-only music track, fetched only after the visitor clicks Unmute. Omit until a track is chosen. */
  audioSrc?: string;
  /** Element that receives focus when the gate closes (the page's main landmark). */
  returnFocusId: string;
};

const MEDIA = {
  desktop: { mp4: "/media/intro-desktop.mp4", webm: "/media/intro-desktop.webm", poster: "/media/poster.jpg" },
  mobile: { mp4: "/media/intro-mobile.mp4", webm: "/media/intro-mobile.webm", poster: "/media/poster-mobile.jpg" },
};

/**
 * Full-screen intro film over the real homepage. The homepage stays in the DOM (crawlable);
 * a tiny inline script in the layout sets <html data-intro="on|off"> before first paint, so
 * returning visitors (sessionStorage) and reduced-motion users never see the gate.
 */
export default function IntroGate(props: Props) {
  const [open, setOpen] = useState(false);
  const [leaving, setLeaving] = useState(false);
  const [variant, setVariant] = useState<"desktop" | "mobile" | null>(null);
  const [activeLine, setActiveLine] = useState(-1);
  const [soundOn, setSoundOn] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const enterRef = useRef<HTMLButtonElement>(null);

  // Decide on the client whether the gate runs, then load the right film.
  useEffect(() => {
    if (document.documentElement.dataset.intro !== "on") return;
    const portrait = window.matchMedia("(max-aspect-ratio: 4/5)").matches;
    setVariant(portrait ? "mobile" : "desktop");
    setOpen(true);
  }, []);

  const close = useCallback(
    (fade: boolean) => {
      try {
        sessionStorage.setItem(INTRO_SEEN_KEY, "1");
      } catch {
        /* storage blocked: the gate simply shows again next time */
      }
      audioRef.current?.pause();
      const finish = () => {
        document.documentElement.dataset.intro = "off";
        setOpen(false);
        setLeaving(false);
        // after React has removed the gate and lifted `inert`, hand focus to the page
        window.setTimeout(() => document.getElementById(props.returnFocusId)?.focus({ preventScroll: true }), 60);
      };
      if (fade) {
        setLeaving(true);
        window.setTimeout(finish, 700);
      } else {
        finish();
      }
    },
    [props.returnFocusId],
  );

  // While open: lock scroll, make the page behind inert, trap focus, Escape skips.
  useEffect(() => {
    if (!open) return;
    const main = document.getElementById(props.returnFocusId);
    const header = document.querySelector<HTMLElement>("[data-site-header]");
    main?.setAttribute("inert", "");
    header?.setAttribute("inert", "");
    document.body.style.overflow = "hidden";
    enterRef.current?.focus();

    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        close(false);
        return;
      }
      if (e.key !== "Tab" || !rootRef.current) return;
      const items = rootRef.current.querySelectorAll<HTMLElement>("button:not([disabled]), a[href]");
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("keydown", onKey);
      main?.removeAttribute("inert");
      header?.removeAttribute("inert");
      document.body.style.overflow = "";
    };
  }, [open, close, props.returnFocusId]);

  // Overlay lines follow the film's clock; the film pauses when the tab is hidden.
  useEffect(() => {
    const video = videoRef.current;
    if (!open || !video) return;
    const onTime = () => {
      const t = video.currentTime;
      setActiveLine(props.lines.findIndex((l) => t >= l.from && t < l.to));
    };
    const onVisibility = () => {
      if (document.hidden) video.pause();
      else void video.play().catch(() => undefined);
    };
    video.addEventListener("timeupdate", onTime);
    document.addEventListener("visibilitychange", onVisibility);
    void video.play().catch(() => undefined);
    return () => {
      video.removeEventListener("timeupdate", onTime);
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, [open, variant, props.lines]);

  const toggleSound = () => {
    if (!props.audioSrc) return;
    if (!audioRef.current) {
      const audio = new Audio(props.audioSrc); // fetched only now, after an explicit click
      audio.loop = true;
      audioRef.current = audio;
    }
    if (soundOn) {
      audioRef.current.pause();
      setSoundOn(false);
    } else {
      void audioRef.current.play().then(() => setSoundOn(true)).catch(() => setSoundOn(false));
    }
  };

  if (!open || !variant) return null;
  const media = MEDIA[variant];
  const soundLabel = !props.audioSrc ? props.soundUnavailableLabel : soundOn ? props.muteLabel : props.unmuteLabel;

  return (
    <div
      ref={rootRef}
      className={`${styles.gate} ${leaving ? styles.leaving : ""}`}
      role="dialog"
      aria-modal="true"
      aria-label={props.label}
    >
      <video
        ref={videoRef}
        className={styles.video}
        poster={media.poster}
        muted
        loop
        playsInline
        autoPlay
        preload="auto"
        aria-hidden="true"
        tabIndex={-1}
      >
        <source src={media.webm} type="video/webm" />
        <source src={media.mp4} type="video/mp4" />
      </video>
      <div className={styles.shade} aria-hidden="true" />

      <p className={styles.brand}>{props.siteName}</p>

      {/* Real HTML text, timed to the shots. aria-live is off: the lines are decorative repeats of the page copy. */}
      <div className={styles.lines} aria-hidden="true">
        {props.lines.map((line, i) => (
          <p key={line.text} className={`${styles.line} ${i === activeLine ? styles.lineOn : ""}`}>
            {line.text}
          </p>
        ))}
      </div>

      <div className={styles.controls}>
        <button ref={enterRef} type="button" className={styles.enter} onClick={() => close(true)}>
          {props.enterLabel}
        </button>
        <button
          type="button"
          className={styles.ghost}
          onClick={toggleSound}
          disabled={!props.audioSrc}
          aria-pressed={props.audioSrc ? soundOn : undefined}
          title={!props.audioSrc ? props.soundUnavailableLabel : undefined}
        >
          {soundLabel}
        </button>
        <button type="button" className={styles.ghost} onClick={() => close(false)}>
          {props.skipLabel}
        </button>
      </div>
    </div>
  );
}
