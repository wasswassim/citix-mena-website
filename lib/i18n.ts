export const locales = ["en", "ar"] as const;
export type Locale = (typeof locales)[number];

export function isLocale(value: string): value is Locale {
  return (locales as readonly string[]).includes(value);
}

export const dir = (locale: Locale) => (locale === "ar" ? "rtl" : "ltr");

/** Overlay lines of the intro film, timed to the shots (seconds). */
export const introTimings = [
  { key: "line1", from: 0, to: 2.5 },
  { key: "line2", from: 5, to: 8 },
  { key: "line3", from: 10.5, to: 15 },
] as const;

type Dictionary = {
  siteName: string;
  meta: { title: string; description: string };
  gate: {
    label: string;
    line1: string;
    line2: string;
    line3: string;
    enter: string;
    skip: string;
    unmute: string;
    mute: string;
    soundUnavailable: string;
  };
  hero: { title: string; sub: string; ctaAdvertise: string; ctaPartner: string; imageAlt: string };
  comingSoon: { title: string; body: string; back: string };
  langSwitch: { label: string; href: string };
};

// NOTE: the Arabic copy is a first draft and must be reviewed by a native speaker before launch.
export const dictionaries: Record<Locale, Dictionary> = {
  en: {
    siteName: "CITIX MENA",
    meta: {
      title: "CITIX MENA | Smarter cities. Stronger brands.",
      description:
        "CITIX MENA builds smart street boards and giant 3D screens that give cities live information and give brands attention where people actually are.",
    },
    gate: {
      label: "CITIX MENA intro film",
      line1: "Smarter cities.",
      line2: "Stronger brands.",
      line3: "We make tomorrow happen today",
      enter: "Enter",
      skip: "Skip intro",
      unmute: "Unmute",
      mute: "Mute",
      soundUnavailable: "Sound is not available yet",
    },
    hero: {
      title: "We make tomorrow happen today",
      sub: "Smart street boards and giant 3D screens across the UAE. Live city information on top, your brand below.",
      ctaAdvertise: "Advertise with us",
      ctaPartner: "Partner with us",
      imageAlt:
        "A frameless glass screen standing on moonlit desert dunes; an oasis, a perfume bottle, a camel and an SUV come out of the glass in turn",
    },
    comingSoon: { title: "Coming soon", body: "This page is on its way.", back: "Back to the homepage" },
    langSwitch: { label: "العربية", href: "/ar" },
  },
  ar: {
    siteName: "CITIX MENA",
    meta: {
      title: "CITIX MENA | مدن أذكى. علامات أقوى.",
      description:
        "تبني CITIX MENA لوحات ذكية في الشوارع وشاشات ثلاثية الأبعاد عملاقة تمنح المدن معلومات حيّة وتمنح العلامات التجارية حضوراً حيث يوجد الناس.",
    },
    gate: {
      label: "الفيلم التعريفي لـ CITIX MENA",
      line1: "مدن أذكى.",
      line2: "علامات أقوى.",
      line3: "نصنع الغد اليوم",
      enter: "ادخل",
      skip: "تخطَّ المقدمة",
      unmute: "تشغيل الصوت",
      mute: "كتم الصوت",
      soundUnavailable: "الصوت غير متوفر بعد",
    },
    hero: {
      title: "نصنع الغد اليوم",
      sub: "لوحات ذكية في الشوارع وشاشات ثلاثية الأبعاد عملاقة في أنحاء الإمارات. معلومات المدينة الحيّة في الأعلى، وعلامتك في الأسفل.",
      ctaAdvertise: "أعلن معنا",
      ctaPartner: "كن شريكاً",
      imageAlt: "شاشة زجاجية بلا إطار على كثبان صحراوية تحت ضوء القمر، تخرج منها بالتتابع واحة وزجاجة عطر وجمل وسيارة دفع رباعي",
    },
    comingSoon: { title: "قريباً", body: "هذه الصفحة قيد الإعداد.", back: "العودة إلى الصفحة الرئيسية" },
    langSwitch: { label: "English", href: "/en" },
  },
};
