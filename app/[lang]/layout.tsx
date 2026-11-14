import type { Metadata, Viewport } from "next";
import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { INTRO_SEEN_KEY } from "@/lib/intro";
import { dictionaries, dir, isLocale, locales } from "@/lib/i18n";
import "../globals.css";

export function generateStaticParams() {
  return locales.map((lang) => ({ lang }));
}

export const viewport: Viewport = { themeColor: "#000000", width: "device-width", initialScale: 1 };

export async function generateMetadata({ params }: { params: Promise<{ lang: string }> }): Promise<Metadata> {
  const { lang } = await params;
  if (!isLocale(lang)) return {};
  const t = dictionaries[lang];
  return {
    title: t.meta.title,
    description: t.meta.description,
    alternates: { canonical: `/${lang}`, languages: { en: "/en", ar: "/ar", "x-default": "/en" } },
  };
}

// Runs before first paint: decides whether the intro gate shows, so there is no flash either way.
// Gate is skipped for returning visitors in this session and for prefers-reduced-motion.
const introScript = `(function(){try{var d=document.documentElement;var seen=sessionStorage.getItem(${JSON.stringify(
  INTRO_SEEN_KEY,
)});var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;d.dataset.intro=(seen||reduce)?"off":"on";}catch(e){document.documentElement.dataset.intro="on";}})();`;

void introScript; // kept for the archived intro gate, not injected

export default async function RootLayout({ children, params }: { children: ReactNode; params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  return (
    <html lang={lang} dir={dir(lang)} data-intro="off" suppressHydrationWarning>
      <head>
        {/* Intro gate disconnected (plan v4.2): the pre-paint script below is kept but not injected,
            so data-intro stays "off". Restore with a script tag using dangerouslySetInnerHTML and introScript. */}
      </head>
      <body>{children}</body>
    </html>
  );
}
