import Link from "next/link";
import { notFound } from "next/navigation";
import IntroGate from "@/components/IntroGate";
import { dictionaries, introTimings, isLocale } from "@/lib/i18n";

export default async function HomePage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  const t = dictionaries[lang];
  const soon = `/${lang}/coming-soon`;

  return (
    <>
      <IntroGate
        label={t.gate.label}
        siteName={t.siteName}
        lines={introTimings.map((l) => ({ text: t.gate[l.key], from: l.from, to: l.to }))}
        enterLabel={t.gate.enter}
        skipLabel={t.gate.skip}
        unmuteLabel={t.gate.unmute}
        muteLabel={t.gate.mute}
        soundUnavailableLabel={t.gate.soundUnavailable}
        returnFocusId="main"
        /* audioSrc="/media/intro-music.mp3"  -> add once Wassim has chosen the track */
      />

      <header className="site-header" data-site-header>
        <Link href={`/${lang}`} className="site-name">
          {t.siteName}
        </Link>
        <Link href={t.langSwitch.href} className="lang-switch" hrefLang={lang === "en" ? "ar" : "en"}>
          {t.langSwitch.label}
        </Link>
      </header>

      <main id="main" tabIndex={-1}>
        {/* Hero night state. Placeholder still until Prompt 4 builds the coded day/night hero;
            it is the film's last frame, so Enter fades the gate into it without a cut. */}
        <section className="hero" aria-labelledby="hero-title">
          <picture className="hero-media">
            <source media="(max-aspect-ratio: 4/5)" srcSet="/media/end-mobile.jpg" />
            <img src="/media/end.jpg" alt={t.hero.imageAlt} width={1920} height={1080} fetchPriority="high" />
          </picture>
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
