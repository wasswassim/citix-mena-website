import Link from "next/link";

/**
 * Large footer (Wassim, 18 Nov 2026): the wordmark and tagline, every page of the site in four groups (all "coming
 * soon" until the homepage is approved), then the legal line, and the CITIX X from the loading screen
 * (media/brand/citix-x-1024.png on the same dark tile) in the bottom corner, as Wassim asked.
 */
type Props = {
  lang: string;
  siteName: string;
  tagline: string;
  groups: { title: string; links: string[] }[];
  rights: string;
  top: string;
  nav: string;
  href: string;
  langSwitch: { label: string; href: string; hrefLang: string };
};

export default function SiteFooter({ lang, siteName, tagline, groups, rights, top, nav, href, langSwitch }: Props) {
  return (
    <footer className="site-footer">
      <div className="footer-top">
        <div className="footer-brand">
          <Link href={`/${lang}`} className="footer-logo" aria-label={siteName}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/media/brand/citix-logo-white.png" alt="" width={934} height={280} loading="lazy" />
          </Link>
          <p className="footer-tagline">{tagline}</p>
        </div>

        <nav className="footer-nav" aria-label={nav}>
          {groups.map((g) => (
            <div key={g.title} className="footer-group">
              <h2 className="footer-group-title">{g.title}</h2>
              <ul>
                {g.links.map((l) => (
                  <li key={l}>
                    <Link href={href}>{l}</Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </div>

      <div className="footer-bottom">
        <div className="footer-legal">
          <p>
            © {new Date().getFullYear()} {siteName}. {rights}
          </p>
          <div className="footer-utils">
            <Link href={langSwitch.href} hrefLang={langSwitch.hrefLang}>
              {langSwitch.label}
            </Link>
            <a href="#main">{top}</a>
          </div>
        </div>
        <div className="footer-x" aria-hidden="true">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/media/brand/citix-x-1024.png" alt="" width={1152} height={1144} loading="lazy" />
        </div>
      </div>
    </footer>
  );
}
