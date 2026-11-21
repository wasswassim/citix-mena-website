"use client";

import { useMemo, useState } from "react";
import { WireframeGlobe } from "@/components/ui/wireframe-globe";

/**
 * Our network (Wassim, 17 Nov 2026; globe replaced 21 Nov 2026): where CITIX MENA stands today, between About and Our
 * Products. Heading and country list on top, a large wireframe globe at the bottom middle, zoomed on the MENA region
 * and swaying slowly. Hovering, focusing or tapping a country turns the globe to it, brightens it and its cities.
 * Facts: "Company facts" slide (sales deck slide 4). CITIX MENA only: the UAE and Oman.
 */
type Country = { id: CountryId; name: string; cities: string; stat: string };
type Props = { eyebrow: string; title: string; sub: string; hint: string; globeLabel: string; countries: Country[] };
export type CountryId = "uae" | "oman";

// ISO 3166 numeric id (world-atlas) and city coordinates [lng, lat]; the first city is where the globe turns to
const PLACES: Record<CountryId, { iso: string; cities: [number, number][] }> = {
  uae: {
    iso: "784",
    cities: [
      [54.3773, 24.4539], // Abu Dhabi
      [55.2708, 25.2048], // Dubai
      [55.4209, 25.3463], // Sharjah
    ],
  },
  oman: { iso: "512", cities: [[58.3829, 23.588]] }, // Muscat
};
const ISO = Object.values(PLACES).map((p) => p.iso);
// rest view: the globe is tipped back so the Arabian Peninsula sits in the middle of the window (the canvas shows
// only the top arc of a sphere ZOOM times its width); a hovered country is shown at the same height
const CENTER: [number, number] = [50, -27];
const TILT = 51; // degrees between the view center and the latitude shown mid-window
const ZOOM = 1.55;

export default function NetworkSection({ eyebrow, title, sub, hint, globeLabel, countries }: Props) {
  const [active, setActive] = useState<CountryId | null>(null);

  const markers = useMemo(
    () =>
      (Object.keys(PLACES) as CountryId[]).flatMap((id) =>
        PLACES[id].cities.map((location) => ({ location, on: active === id })),
      ),
    [active],
  );
  const focus = active ? PLACES[active].cities[0] : null;

  return (
    <section className="network" aria-labelledby="network-title">
      <div className="network-inner">
        <div className="network-text">
          <p className="network-eyebrow">{eyebrow}</p>
          <h2 id="network-title" className="network-title">
            {title}
          </h2>
          <p className="network-sub">{sub}</p>
        </div>

        <div className="network-side">
          <ul className="network-list" onMouseLeave={() => setActive(null)}>
            {countries.map((c) => (
              <li key={c.id}>
                <button
                  type="button"
                  className="network-country"
                  data-active={active === c.id || undefined}
                  aria-pressed={active === c.id}
                  onMouseEnter={() => setActive(c.id)}
                  onFocus={() => setActive(c.id)}
                  onBlur={() => setActive(null)}
                  onClick={() => setActive((a) => (a === c.id ? null : c.id))}
                >
                  <span className="network-name">{c.name}</span>
                  <span className="network-cities">{c.cities}</span>
                  <span className="network-stat">{c.stat}</span>
                </button>
              </li>
            ))}
          </ul>
          <p className="network-hint">{hint}</p>
        </div>
      </div>

      <div className="network-globe">
        <WireframeGlobe
          center={CENTER}
          focus={focus ? [focus[0], focus[1] - TILT] : null}
          highlight={ISO}
          active={active ? PLACES[active].iso : null}
          markers={markers}
          label={globeLabel}
          zoom={ZOOM}
          top={24}
        />
      </div>
    </section>
  );
}
