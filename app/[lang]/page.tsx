import Link from "next/link";
import { notFound } from "next/navigation";
import AboutStatement from "@/components/AboutStatement";
import Arrow from "@/components/Arrow";
import CompanyFacts from "@/components/CompanyFacts";
import EcosystemCards from "@/components/EcosystemCards";
import HeroLoop from "@/components/HeroLoop";
import SiteHeader from "@/components/SiteHeader";
import { logoStyle, trustedBrands } from "@/lib/brands";
import { dictionaries, isLocale } from "@/lib/i18n";

export default async function HomePage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  const t = dictionaries[lang];
  const soon = `/${lang}/coming-soon`;
  const n = t.header.nav;

  return (
    <>
      {/* Intro gate disconnected 14 Nov 2026 (plan v4.2: intro film dropped). components/IntroGate.tsx is kept. */}
      <SiteHeader
        lang={lang}
        siteName={t.siteName}
        nav={[n.solutions, n.smartboards, n.projects, n.about, n.insights, n.contact].map((label) => ({
          label,
          href: soon,
        }))}
        getInTouch={{ label: t.header.getInTouch, href: soon }}
        langSwitch={{ ...t.langSwitch, hrefLang: lang === "en" ? "ar" : "en" }}
        menuOpen={t.header.menuOpen}
        menuClose={t.header.menuClose}
        navLabel={t.header.navLabel}
        announcement={{ ...t.announcement, href: soon }}
      />

      <main id="main" tabIndex={-1}>
        {/* Hero v5 "The Orbit" in the bluesqx hero layout (runbook v5 P5): loop + flat 50% overlay, H1 top-start,
            CTAs bottom-end, trusted-by marquee at the bottom. No dust overlay (dropped 15 Nov 2026). */}
        <section className="hero" aria-labelledby="hero-title">
          <HeroLoop alt={t.hero.imageAlt} />
          <div className="hero-overlay" aria-hidden="true" />

          <div className="hero-title-wrap">
            <h1 id="hero-title" className="hero-title">
              <span className="hero-line">{t.hero.line1}</span> <span className="hero-line">{t.hero.line2}</span>
            </h1>
          </div>

          <EcosystemCards label={t.ecosystem.label} cards={t.ecosystem.cards} />

          <div className="hero-ctas">
            <Link className="btn-outline" href={soon}>
              {t.hero.ctaSolutions}
              <Arrow />
            </Link>
            <Link className="btn-outline" href={soon}>
              {t.hero.ctaProject}
              <Arrow />
            </Link>
          </div>

          <div className="trusted">
            <p className="trusted-label">{t.hero.trusted}</p>
            <div className="marquee">
              {[0, 1].map((copy) => (
                <ul className="marquee-track" key={copy} aria-hidden={copy === 1 || undefined}>
                  {trustedBrands.map((b) => (
                    <li key={b.name} className="logo" role="img" aria-label={b.name} style={logoStyle(b.box)} />
                  ))}
                </ul>
              ))}
            </div>
          </div>
        </section>

        <CompanyFacts title={t.facts.title} facts={t.facts.items} />

        <AboutStatement
          title={t.about.title}
          paragraphs={t.about.paragraphs}
          ctaLine={t.about.ctaLine}
          cta={t.about.cta}
          href={soon}
        />
      </main>
    </>
  );
}
