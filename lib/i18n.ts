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
  hero: {
    title: string;
    sub: string;
    ctaAdvertise: string;
    ctaPartner: string;
    imageAlt: string;
    line1: string;
    line2: string;
    ctaSolutions: string;
    ctaProject: string;
    trusted: string;
    placeholderNote: string;
  };
  ecosystem: { label: string; lead: string; cards: { title: string; text: string }[] };
  facts: { title: string; items: { value: number; suffix: string; label: string }[] };
  about: { title: string; paragraphs: string[]; ctaLine: string; cta: string };
  network: {
    eyebrow: string;
    title: string;
    sub: string;
    hint: string;
    globeLabel: string;
    countries: { id: "uae" | "oman" | "kz" | "tr"; name: string; cities: string; stat: string }[];
  };
  products: {
    title: string;
    sub: string;
    cta: string;
    all: string;
    cards: { name: string; tag: string; text: string; alt: string }[];
  };
  projects: {
    eyebrow: string;
    title: string;
    sub: string;
    hint: string;
    cards: { place: string; title: string; text: string; alt: string }[];
  };
  how: {
    eyebrow: string;
    title: string;
    sub: string;
    steps: { title: string; text: string; rows: [string, string] }[];
  };
  cta: {
    eyebrow: string;
    title: string;
    sub: string;
    slogan: string;
    fields: { name: string; company: string; email: string; phone: string; interest: string; message: string };
    optional: string;
    interests: string[];
    choose: string;
    submit: string;
    sentNote: string;
  };
  footer: {
    tagline: string;
    groups: { title: string; links: string[] }[];
    rights: string;
    top: string;
    nav: string;
  };
  header: {
    nav: { solutions: string; smartboards: string; projects: string; about: string; insights: string; contact: string };
    getInTouch: string;
    menuOpen: string;
    menuClose: string;
    navLabel: string;
  };
  announcement: { text: string; cta: string; close: string };
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
      line1: "Smarter Cities.",
      line2: "Stronger Brands.",
      ctaSolutions: "Our Solutions",
      ctaProject: "Latest Project",
      trusted: "Global brands that trust us",
      placeholderNote: "logo placeholder",
    },
    // From the CITIX Ecosystem slide (company deck). "Propriety" on the slide corrected to "Proprietary".
    ecosystem: {
      label: "Ecosystem",
      lead: "All in one platform:", // hero word flip (Wassim, 17 Nov 2026): the card titles cycle after it
      cards: [
        { title: "Hardware", text: "Self-engineered smartboards and components" },
        { title: "Software", text: "Proprietary solutions" },
        { title: "AI engine", text: "Face detection, ML and computer vision" },
        { title: "Blockchain", text: "Content delivery" },
        { title: "VPN", text: "Content delivery tunnels" },
        { title: "Smart City", text: "Easy-to-integrate informational system" },
      ],
    },
    // Counters from the "Company facts" slide (company deck; employees added by Wassim). Left out on purpose: revenue and EBITDA (financials,
    // need the supervisor's OK before going public), countries and "No. 1 in Kazakhstan" (the network section).
    facts: {
      title: "CITIX MENA in numbers",
      items: [
        { value: 600, suffix: "+", label: "smartboards installed" },
        { value: 360, suffix: "", label: "brands partnered with us" },
        { value: 1000, suffix: "+", label: "marketing campaigns delivered" },
        { value: 50, suffix: "+", label: "smart-city cases" },
        { value: 150, suffix: "", label: "people on our team" },
      ],
    },
    // About statement (Wassim, 15 Nov 2026). Sources: sales deck "About CITIX", "Smart widget system", "Dynamic
    // creative optimization" and the eye-tracking slide (+53% conversion vs standard billboards), brand book mission.
    // Countries are left to the dedicated network section (Wassim); paragraph 2 is written for search and AI
    // answers: product names, what they do, and one sourced figure.
    about: {
      title: "About Us",
      paragraphs: [
        "We are a smart-city and digital out-of-home company that turns street advertising into a living network, where technology, creativity and design work for the city.",
        "Our smartboards and giant 3D screens pair live city widgets with dynamic creative optimization and campaign analytics, delivering 53% higher conversion than standard billboards in a real-traffic eye-tracking study.",
      ],
      ctaLine: "Let’s make tomorrow happen today.",
      cta: "Talk to us",
    },
    // Our network (Wassim, 17 Nov 2026). Sources: "Company facts" slide (sales deck slide 4: cities, smartboard
    // counts, giant screens, Oman Oil project, 12 global projects) and the company-facts screenshot ("No. 1 in
    // Kazakhstan"). Country order = west of the Gulf outwards; ids match components/NetworkSection.tsx.
    network: {
      eyebrow: "Our network",
      title: "Where we stand today",
      sub: "From the Gulf to Central Asia, CITIX smartboards and giant 3D screens already run in four countries, across 12 global projects.",
      hint: "Point at a country to find it on the globe.",
      globeLabel: "Globe marking CITIX cities in the UAE, Oman, Kazakhstan and Turkey",
      countries: [
        { id: "uae", name: "United Arab Emirates", cities: "Abu Dhabi · Dubai · Sharjah", stat: "40+ smartboards · 2 giant 3D screens" },
        { id: "oman", name: "Oman", cities: "Muscat", stat: "Project launched with Oman Oil" },
        { id: "kz", name: "Kazakhstan", cities: "Almaty · Astana", stat: "550+ smartboards · No. 1 in the country" },
        { id: "tr", name: "Turkey", cities: "Istanbul · Ankara", stat: "50+ smartboards" },
      ],
    },
    // Our Products (Wassim, 15 Nov 2026). Subtitle = deck slide 6 word for word; card text from the product slides
    // (Tom 13, Jerry 15, Baloo 17, Jumbo 19). Order (Wassim, 17 Nov): big screens first, then Tom and Jerry;
    // it must match MEDIA in components/ProductCards.tsx.
    products: {
      title: "Our Products",
      sub: "The first generation of innovative city gadgets is here to elevate the urban environment and modern advertising.",
      cta: "Discover",
      all: "All products",
      cards: [
        {
          name: "Jumbo",
          tag: "Largest 3D corner screen",
          text: "Around 400 m² of corner screen at a premium mall, built for immersive 3D campaigns that adapt in real time.",
          alt: "Jumbo corner screen on a shopping mall facade, with a 3D perfume bottle floating out of the screen",
        },
        {
          name: "Baloo",
          tag: "Giant 3D corner screen",
          text: "A 32 m² digital spire on the corner of Tejara 1, where 3D content wraps around the building’s edge.",
          alt: "Baloo corner screen on the Tejara 1 building by day, with a red SUV driving out of the screen in 3D",
        },
        {
          name: "Tom",
          tag: "Roadside smartboard",
          text: "A 7 × 2 m roadside totem. Live city widgets on top catch drivers’ eyes, and your ad sits right below.",
          alt: "Tom roadside smartboard against a sunlit wall, with an extreme heat alert above a cold drink ad",
        },
        {
          name: "Jerry",
          tag: "Pedestrian smartboard",
          text: "2.6 m tall and made for walkways, Jerry turns public space into a responsive media channel.",
          alt: "Jerry pedestrian smartboard in a concrete hall, with a weather widget above the ad",
        },
      ],
    },
    // Projects tunnel (17 Nov 2026). Facts from the sales deck (Sharjah network slides 23-27, Jumbo, Baloo, Cannes
    // Lions slide 56) and the project notes (Yas Island Tom). Order must match IMAGES in components/ProjectTunnel.tsx.
    projects: {
      eyebrow: "Our projects",
      title: "Already part of the city",
      sub: "From Sharjah’s waterfront to a Cannes Lions stage, CITIX screens are already on the street and already working for brands.",
      hint: "Scroll to fly through",
      cards: [
        {
          place: "Sharjah · UAE",
          title: "Sharjah network",
          text: "5 key areas and 14 landmarks: waterfront, heritage, education, family and retail destinations.",
          alt: "Sharjah waterfront skyline at dusk, with the Al Qasba wheel lit across the water",
        },
        {
          place: "Abu Dhabi · UAE",
          title: "Jumbo",
          text: "Our largest corner screen, about 400 m², at a premium mall surrounded by high-end brands.",
          alt: "Jumbo corner screen on a shopping mall facade, with a 3D perfume bottle floating out of the screen",
        },
        {
          place: "Sharjah · Network 1",
          title: "Majaz & Heera Beach",
          text: "Two locations linking the busy Majaz corridors with the coastal crowd of Heera Beach.",
          alt: "Map of the Majaz and Heera Beach network with the CITIX screen locations marked",
        },
        {
          place: "Kazakhstan · Cannes Lions 2025",
          title: "Saltanat Light",
          text: "CITIX Kazakhstan and GForce Grey won two Cannes Lions for an AI campaign that turns billboards into a live distress signal.",
          alt: "Saltanat Light campaign board: 22.3 million reach, 522,000 reactions",
        },
        {
          place: "Sharjah · Network 2",
          title: "Al Mamsha",
          text: "Two Tom smartboards connecting a growing residential community with its retail and leisure spots.",
          alt: "Map of the Al Mamsha network with the two Tom locations marked",
        },
        {
          place: "Tejara 1 · UAE",
          title: "Baloo",
          text: "Four 8 × 4 m screens wrapping the corner of the Tejara 1 building, right next to a busy highway.",
          alt: "Baloo corner screens on the Tejara 1 building at night, showing the CITIX X",
        },
        {
          place: "Sharjah · Network 3",
          title: "06 Mall",
          text: "Reaching shoppers, families and Al Jurainah residents on the way in and inside the mall.",
          alt: "Map of 06 Mall with its indoor screens and Jerry smartboard marked",
        },
        {
          place: "Abu Dhabi · UAE",
          title: "Tom at Yas Island",
          text: "The first two Tom smartboards stand at the entrances of Yas Island.",
          alt: "Tom roadside smartboard against a sunlit wall, with an extreme heat alert above a cold drink ad",
        },
        {
          place: "Sharjah · Network 4",
          title: "Chamber of Commerce",
          text: "Premium visibility for professionals, decision-makers and commuters on one of Sharjah’s busiest corridors.",
          alt: "Map of the Sharjah Chamber of Commerce network with the CITIX screen locations marked",
        },
      ],
    },
    // How we work (18 Nov 2026): from the sales deck (slides 9-10, 31, 33, 36, 39, 55) and the company profile
    // (p14, p25). Step 4's +53% is the deck's eye-tracking figure, still to be cleared for publication.
    how: {
      eyebrow: "How we work",
      title: "From the first brief to measurable impact",
      sub: "One team plans, creates, runs and measures your campaign on CITIX smartboards.",
      steps: [
        {
          title: "Plan",
          text: "We help you pick the right screen and placement for your goal: standard formats using 50% to 100% of the screen, or custom placements across our Sharjah and Abu Dhabi networks.",
          rows: ["50–100% of the screen", "Sharjah · Abu Dhabi"],
        },
        {
          title: "Create",
          text: "Our in-house creative team builds the concept with you, from cinematic video to 3D content made for each screen's shape.",
          rows: ["In-house creative team", "2D and 3D content"],
        },
        {
          title: "Sync",
          text: "Your ad runs alongside our smart widgets and adapts by itself to the weather, the time of day, the day of the week or public holidays, all managed from Citix OS.",
          rows: ["Weather · time of day", "Holidays · events"],
        },
        {
          title: "Measure",
          text: "Every campaign must deliver a measurable effect. Built-in cameras and sensors read the street, and an eye-tracking study in real traffic measured +53% conversion versus standard billboards.",
          rows: ["Eye-tracking study", "+53% vs billboards"],
        },
      ],
    },
    // Call to action (18 Nov 2026). The form is not connected to a backend yet: on submit it says so plainly.
    cta: {
      eyebrow: "Get in touch",
      title: "Put your brand where the city looks",
      sub: "Tell us about your campaign. Our team comes back with the right screens, placements and a plan.",
      slogan: "We make tomorrow happen today.",
      fields: { name: "Full name", company: "Company", email: "Work email", phone: "Phone", interest: "I’m interested in", message: "Tell us about your campaign" },
      optional: "optional",
      interests: ["Street smartboards", "Giant 3D screens", "Creative content", "Partnership"],
      choose: "Choose one",
      submit: "Send request",
      sentNote: "Thank you. This preview form is not connected yet, so nothing was sent.",
    },
    // Footer (18 Nov 2026): every page of the site; all of them are "coming soon" until the homepage is approved.
    footer: {
      tagline: "Smarter cities. Stronger brands.",
      groups: [
        { title: "Solutions", links: ["Hardware", "Software", "AI engine", "Smart City"] },
        { title: "Smartboards", links: ["Tom", "Jerry", "Smart Pillar", "Baloo", "Simba", "Jumbo", "Citix OS"] },
        { title: "Projects", links: ["Sharjah network", "Jumbo", "Tom at Yas Island", "Saltanat Light"] },
        { title: "Company", links: ["About", "Insights", "Contact", "Get a quote"] },
      ],
      rights: "All rights reserved.",
      top: "Back to top",
      nav: "Footer",
    },
    header: {
      nav: {
        solutions: "Solutions",
        smartboards: "Smartboards",
        projects: "Projects",
        about: "About",
        insights: "Insights",
        contact: "Contact",
      },
      getInTouch: "Get a quote",
      menuOpen: "Open menu",
      menuClose: "Close menu",
      navLabel: "Main",
    },
    announcement: { text: "Stay inspired: subscribe for CITIX MENA updates", cta: "Subscribe", close: "Close" },
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
      line1: "مدن أذكى.",
      line2: "علامات أقوى.",
      ctaSolutions: "حلولنا",
      ctaProject: "أحدث مشاريعنا",
      trusted: "علامات عالمية تثق بنا",
      placeholderNote: "شعار مؤقت",
    },
    ecosystem: {
      label: "المنظومة",
      lead: "منصّة واحدة متكاملة:",
      cards: [
        { title: "الأجهزة", text: "لوحات ذكية ومكوّنات من تصميمنا" },
        { title: "البرمجيات", text: "حلول خاصة بنا" },
        { title: "محرّك الذكاء الاصطناعي", text: "التعرّف على الوجوه، التعلّم الآلي والرؤية الحاسوبية" },
        { title: "بلوك تشين", text: "توصيل المحتوى" },
        { title: "VPN", text: "قنوات آمنة لتوصيل المحتوى" },
        { title: "المدينة الذكية", text: "نظام معلوماتي سهل الدمج" },
      ],
    },
    facts: {
      title: "CITIX MENA بالأرقام",
      items: [
        { value: 600, suffix: "+", label: "لوحة ذكية مثبّتة" },
        { value: 360, suffix: "", label: "علامة تجارية شريكة" },
        { value: 1000, suffix: "+", label: "حملة تسويقية منفّذة" },
        { value: 50, suffix: "+", label: "حالة استخدام للمدن الذكية" },
        { value: 150, suffix: "", label: "موظفاً في فريقنا" },
      ],
    },
    about: {
      title: "من نحن",
      paragraphs: [
        "نحن شركة متخصصة في المدن الذكية والإعلانات الرقمية الخارجية، تحوّل إعلانات الشوارع إلى شبكة رقمية حيّة تجتمع فيها التقنية والإبداع والتصميم لخدمة المدينة.",
        "تجمع لوحاتنا الذكية وشاشاتنا العملاقة ثلاثية الأبعاد بين معلومات المدينة الحيّة والتحسين الديناميكي للمحتوى الإعلاني وتحليلات الحملات، لتحقق معدل تحويل أعلى بنسبة 53% مقارنة باللوحات الإعلانية التقليدية، وفق دراسة لتتبّع حركة العين في حركة مرور حقيقية.",
      ],
      ctaLine: "لنصنع الغد اليوم.",
      cta: "تحدث إلينا",
    },
    network: {
      eyebrow: "شبكتنا",
      title: "أين نقف اليوم",
      sub: "من الخليج إلى آسيا الوسطى، تعمل لوحات CITIX الذكية وشاشاتها العملاقة ثلاثية الأبعاد في أربع دول، ضمن 12 مشروعاً عالمياً.",
      hint: "مرّر المؤشر على دولة لتجدها على الكرة الأرضية.",
      globeLabel: "كرة أرضية تُظهر مدن CITIX في الإمارات وعُمان وكازاخستان وتركيا",
      countries: [
        { id: "uae", name: "الإمارات العربية المتحدة", cities: "أبوظبي · دبي · الشارقة", stat: "أكثر من 40 لوحة ذكية · شاشتان عملاقتان ثلاثيتا الأبعاد" },
        { id: "oman", name: "عُمان", cities: "مسقط", stat: "مشروع أُطلق مع شركة النفط العُمانية" },
        { id: "kz", name: "كازاخستان", cities: "ألماتي · أستانا", stat: "أكثر من 550 لوحة ذكية · الأولى في البلاد" },
        { id: "tr", name: "تركيا", cities: "إسطنبول · أنقرة", stat: "أكثر من 50 لوحة ذكية" },
      ],
    },
    products: {
      title: "منتجاتنا",
      sub: "الجيل الأول من أدوات المدينة المبتكرة وصل ليرتقي بالبيئة الحضرية والإعلان الحديث.",
      cta: "اكتشف",
      all: "جميع المنتجات",
      cards: [
        {
          name: "Jumbo",
          tag: "أكبر شاشة زاوية ثلاثية الأبعاد",
          text: "نحو 400 م² من الشاشات على زاوية مركز تسوق راقٍ، مصممة لحملات ثلاثية الأبعاد غامرة تتكيّف في الوقت الحقيقي.",
          alt: "شاشة Jumbo على واجهة مركز تسوق مع زجاجة عطر ثلاثية الأبعاد تخرج من الشاشة",
        },
        {
          name: "Baloo",
          tag: "شاشة زاوية عملاقة ثلاثية الأبعاد",
          text: "برج رقمي بمساحة 32 م² على زاوية مبنى تجارة 1، يلتف فيه المحتوى ثلاثي الأبعاد حول حافة المبنى.",
          alt: "شاشة Baloo على زاوية مبنى تجارة 1 نهاراً، مع سيارة SUV حمراء تخرج من الشاشة بتقنية ثلاثية الأبعاد",
        },
        {
          name: "Tom",
          tag: "لوحة ذكية على الطرق",
          text: "لوحة طرقية بمقاس 7 × 2 م. معلومات المدينة الحيّة في الأعلى تلفت أنظار السائقين، وإعلانك أسفلها مباشرة.",
          alt: "لوحة Tom الذكية أمام جدار مشمس، مع تنبيه من الحر الشديد فوق إعلان مشروب بارد",
        },
        {
          name: "Jerry",
          tag: "لوحة ذكية للمشاة",
          text: "بارتفاع 2.6 م ومصممة لممرات المشاة، تحوّل Jerry المساحات العامة إلى قناة إعلامية تتفاعل مع محيطها.",
          alt: "لوحة Jerry الذكية للمشاة في قاعة خرسانية، مع معلومات الطقس فوق الإعلان",
        },
      ],
    },
    projects: {
      eyebrow: "مشاريعنا",
      title: "جزء من المدينة اليوم",
      sub: "من واجهة الشارقة البحرية إلى منصة مهرجان كان ليونز، شاشات CITIX موجودة في الشارع وتعمل للعلامات التجارية الآن.",
      hint: "مرّر للتنقّل",
      cards: [
        {
          place: "الشارقة · الإمارات",
          title: "شبكة الشارقة",
          text: "5 مناطق رئيسية و14 معلمًا: الواجهة البحرية والتراث والتعليم والعائلات ووجهات التسوق.",
          alt: "أفق الشارقة البحري عند الغروب مع عجلة القصباء المضاءة فوق الماء",
        },
        {
          place: "أبوظبي · الإمارات",
          title: "Jumbo",
          text: "أكبر شاشاتنا الزاوية، بمساحة 400 م² تقريبًا، في مركز تسوق فاخر تحيط به العلامات الراقية.",
          alt: "شاشة جمبو الزاوية على واجهة مركز تسوق، تخرج منها زجاجة عطر ثلاثية الأبعاد",
        },
        {
          place: "الشارقة · الشبكة 1",
          title: "المجاز وشاطئ الحيرة",
          text: "موقعان يربطان ممرات المجاز المزدحمة بجمهور شاطئ الحيرة الساحلي.",
          alt: "خريطة شبكة المجاز وشاطئ الحيرة مع مواقع شاشات CITIX",
        },
        {
          place: "كازاخستان · كان ليونز 2025",
          title: "سلطنات لايت",
          text: "فازت CITIX كازاخستان مع GForce Grey بجائزتين في كان ليونز عن حملة بالذكاء الاصطناعي تحوّل اللوحات إلى إشارة استغاثة حيّة.",
          alt: "لوحة حملة سلطنات لايت: وصول 22.3 مليون و522 ألف تفاعل",
        },
        {
          place: "الشارقة · الشبكة 2",
          title: "الممشى",
          text: "لوحتا Tom ذكيتان تربطان مجتمعًا سكنيًا متناميًا بوجهات التسوق والترفيه.",
          alt: "خريطة شبكة الممشى مع موقعي Tom",
        },
        {
          place: "تجارة 1 · الإمارات",
          title: "Baloo",
          text: "أربع شاشات بمقاس 8 × 4 م تلتف حول زاوية مبنى تجارة 1، بجوار طريق سريع مزدحم.",
          alt: "شاشات Baloo الزاوية على مبنى تجارة 1 ليلًا، تعرض علامة X من CITIX",
        },
        {
          place: "الشارقة · الشبكة 3",
          title: "06 مول",
          text: "تصل إلى المتسوقين والعائلات وسكان الجرينة عند الوصول وداخل المول.",
          alt: "خريطة 06 مول مع شاشاته الداخلية ولوحة Jerry",
        },
        {
          place: "أبوظبي · الإمارات",
          title: "Tom في جزيرة ياس",
          text: "أول لوحتين من Tom تقفان عند مداخل جزيرة ياس.",
          alt: "لوحة Tom الذكية على جانب الطريق أمام جدار مشمس، مع تنبيه حرارة شديدة فوق إعلان مشروب بارد",
        },
        {
          place: "الشارقة · الشبكة 4",
          title: "غرفة التجارة",
          text: "حضور مميز أمام المهنيين وصنّاع القرار والمتنقلين على أحد أكثر ممرات الشارقة حركة.",
          alt: "خريطة شبكة غرفة تجارة وصناعة الشارقة مع مواقع شاشات CITIX",
        },
      ],
    },
    how: {
      eyebrow: "كيف نعمل",
      title: "من الفكرة الأولى إلى أثر قابل للقياس",
      sub: "فريق واحد يخطط لحملتك ويبدعها ويشغّلها ويقيس نتائجها على لوحات CITIX الذكية.",
      steps: [
        {
          title: "التخطيط",
          text: "نساعدك على اختيار الشاشة والموقع الأنسب لهدفك: صيغ قياسية تشغل من 50% إلى 100% من الشاشة، أو مواقع مخصّصة عبر شبكاتنا في الشارقة وأبوظبي.",
          rows: ["من 50% إلى 100% من الشاشة", "الشارقة · أبوظبي"],
        },
        {
          title: "الإبداع",
          text: "يبني فريقنا الإبداعي الداخلي الفكرة معك، من الفيديو السينمائي إلى المحتوى ثلاثي الأبعاد المصمّم لشكل كل شاشة.",
          rows: ["فريق إبداعي داخلي", "محتوى ثنائي وثلاثي الأبعاد"],
        },
        {
          title: "المزامنة",
          text: "يُعرض إعلانك إلى جانب أدواتنا الذكية ويتكيّف تلقائياً مع الطقس ووقت اليوم ويوم الأسبوع والعطلات الرسمية، وكل ذلك يُدار من Citix OS.",
          rows: ["الطقس · وقت اليوم", "العطلات · الفعاليات"],
        },
        {
          title: "القياس",
          text: "يجب أن تحقق كل حملة أثراً قابلاً للقياس. تقرأ الكاميرات وأجهزة الاستشعار المدمجة حركة الشارع، وقاست دراسة لتتبّع العين في حركة مرور حقيقية زيادة بنسبة 53% في التحويل مقارنة باللوحات الإعلانية التقليدية.",
          rows: ["دراسة تتبّع العين", "+53% مقارنة باللوحات"],
        },
      ],
    },
    cta: {
      eyebrow: "تواصل معنا",
      title: "ضع علامتك حيث تنظر المدينة",
      sub: "أخبرنا عن حملتك، وسيعود إليك فريقنا بالشاشات والمواقع المناسبة وخطة واضحة.",
      slogan: "نصنع الغد اليوم.",
      fields: { name: "الاسم الكامل", company: "الشركة", email: "البريد الإلكتروني للعمل", phone: "الهاتف", interest: "أهتم بـ", message: "أخبرنا عن حملتك" },
      optional: "اختياري",
      interests: ["لوحات الشوارع الذكية", "الشاشات العملاقة ثلاثية الأبعاد", "المحتوى الإبداعي", "الشراكة"],
      choose: "اختر واحدًا",
      submit: "أرسل الطلب",
      sentNote: "شكرًا لك. هذا النموذج تجريبي وغير متصل بعد، لذلك لم يُرسل شيء.",
    },
    footer: {
      tagline: "مدن أذكى. علامات تجارية أقوى.",
      groups: [
        { title: "الحلول", links: ["الأجهزة", "البرمجيات", "محرك الذكاء الاصطناعي", "المدينة الذكية"] },
        { title: "اللوحات الذكية", links: ["Tom", "Jerry", "Smart Pillar", "Baloo", "Simba", "Jumbo", "Citix OS"] },
        { title: "المشاريع", links: ["شبكة الشارقة", "Jumbo", "Tom في جزيرة ياس", "Saltanat Light"] },
        { title: "الشركة", links: ["من نحن", "رؤى", "تواصل", "اطلب عرض سعر"] },
      ],
      rights: "جميع الحقوق محفوظة.",
      top: "العودة إلى الأعلى",
      nav: "تذييل الموقع",
    },
    header: {
      nav: {
        solutions: "الحلول",
        smartboards: "اللوحات الذكية",
        projects: "المشاريع",
        about: "من نحن",
        insights: "رؤى",
        contact: "تواصل",
      },
      getInTouch: "اطلب عرض سعر",
      menuOpen: "فتح القائمة",
      menuClose: "إغلاق القائمة",
      navLabel: "الرئيسية",
    },
    announcement: { text: "ابقَ على اطلاع: اشترك لتصلك أخبار CITIX MENA", cta: "اشترك", close: "إغلاق" },
    comingSoon: { title: "قريباً", body: "هذه الصفحة قيد الإعداد.", back: "العودة إلى الصفحة الرئيسية" },
    langSwitch: { label: "English", href: "/en" },
  },
};
