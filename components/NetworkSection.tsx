"use client";

import type { Marker } from "cobe";
import { useMemo, useState } from "react";
import { Globe } from "@/components/ui/globe";

/**
 * Our network (Wassim, 17 Nov 2026): where CITIX stands today, between About and Our Products. Dark section,
 * country list on one side and a globe on the other. Hovering, focusing or tapping a country turns the globe to it
 * and lights its cities in Pulse Red; the other cities stay small and grey. Facts: "Company facts" slide (sales deck
 * slide 4) and the company-facts screenshot ("No. 1 in Kazakhstan").
 */
type Country = { id: CountryId; name: string; cities: string; stat: string };
type Props = { eyebrow: string; title: string; sub: string; hint: string; globeLabel: string; countries: Country[] };
export type CountryId = "uae" | "oman" | "kz" | "tr";

// city coordinates [lat, lng]; the first city of each country is where the globe turns to
const PLACES: Record<CountryId, [number, number][]> = {
  uae: [
    [24.4539, 54.3773], // Abu Dhabi
    [25.2048, 55.2708], // Dubai
    [25.3463, 55.4209], // Sharjah
  ],
  oman: [[23.588, 58.3829]], // Muscat
  kz: [
    [43.222, 76.8512], // Almaty
    [51.1694, 71.4491], // Astana
  ],
  tr: [
    [41.0082, 28.9784], // Istanbul
    [39.9334, 32.8597], // Ankara
  ],
};

const RED: [number, number, number] = [253 / 255, 3 / 255, 50 / 255];
const MIST: [number, number, number] = [0.88, 0.88, 0.88];

export default function NetworkSection({ eyebrow, title, sub, hint, globeLabel, countries }: Props) {
  const [active, setActive] = useState<CountryId | null>(null);

  const markers = useMemo<Marker[]>(
    () =>
      (Object.keys(PLACES) as CountryId[]).flatMap((id) =>
        PLACES[id].map((location) => ({
          location,
          size: active === id ? 0.09 : active ? 0.035 : 0.05,
          color: active && active !== id ? MIST : RED,
        })),
      ),
    [active],
  );

  return (
    <section className="network" aria-labelledby="network-title">
      <div className="network-inner">
        <div className="network-text">
          <p className="network-eyebrow">{eyebrow}</p>
          <h2 id="network-title" className="network-title">
            {title}
          </h2>
          <p className="network-sub">{sub}</p>

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

        <div className="network-globe">
          <Globe
            markers={markers}
            focus={active ? PLACES[active][0] : null}
            label={globeLabel}
            baseColor={[0.16, 0.16, 0.16]}
            markerColor={RED}
            glowColor={[0.1, 0.1, 0.1]}
          />
        </div>
      </div>
    </section>
  );
}
