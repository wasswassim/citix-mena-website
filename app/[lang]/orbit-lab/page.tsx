import type { Metadata } from "next";
import { notFound } from "next/navigation";
import OrbitLab from "@/components/OrbitLab";
import { isLocale } from "@/lib/i18n";

// Internal test page for the hero orbit (route 1: real 3D camera). Not part of the site.
export const metadata: Metadata = { title: "Orbit lab", robots: { index: false, follow: false } };

export default async function OrbitLabPage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  return <OrbitLab />;
}
