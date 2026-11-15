import Link from "next/link";
import { notFound } from "next/navigation";
import HeroLoop from "@/components/HeroLoop";
import { dictionaries, isLocale } from "@/lib/i18n";

export default async function HomePage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  const t = dictionaries[lang];
  const soon = `/${lang}/coming-soon`;

  return (
    <>
      {/* Intro gate disconnected 14 Nov 2026 (plan v4.2: intro film dropped). components/IntroGate.tsx is kept. */}

      <header className="site-header" data-site-header>
        <Link href={`/${lang}`} className="site-name">
          {t.siteName}
        </Link>
        <Link href={t.langSwitch.href} className="lang-switch" hrefLang={lang === "en" ? "ar" : "en"}>
          {t.langSwitch.label}
        </Link>
      </header>

      <main id="main" tabIndex={-1}>
        {/* Hero v5 "The Orbit": 28 s glass-panel loop (16:9 + 9:16), poster first, no dust overlay. */}
        <section className="hero" aria-labelledby="hero-title">
          <HeroLoop alt={t.hero.imageAlt} />
          <div className="hero-copy">
            <h1 id="hero-title">{t.hero.title}</h1>
            <p>{t.hero.sub}</p>
            <div className="cta-row">
              <Link className="cta" href={soon}>
                {t.hero.ctaAdvertise}
              </Link>
              <Link className="cta secondary" href={soon}>
                {t.hero.ctaPartner}
              </Link>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}
