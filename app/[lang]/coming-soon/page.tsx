import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { dictionaries, isLocale } from "@/lib/i18n";

export const metadata: Metadata = { robots: { index: false } };

export default async function ComingSoon({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  const t = dictionaries[lang].comingSoon;
  return (
    <main className="coming-soon">
      <h1>{t.title}</h1>
      <p>{t.body}</p>
      <p>
        <Link href={`/${lang}`}>{t.back}</Link>
      </p>
    </main>
  );
}
