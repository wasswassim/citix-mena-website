"use client";

import { useId, useState, type FormEvent } from "react";
import Arrow from "@/components/Arrow";

/**
 * Call to action (Wassim, 18 Nov 2026): the contact form after How we work. Not connected to a backend yet, so a
 * submit only validates in the browser and then says plainly that nothing was sent (no fake "message received").
 */
type Props = {
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

export default function ContactCTA({ eyebrow, title, sub, slogan, fields, optional, interests, choose, submit, sentNote }: Props) {
  const id = useId();
  const [sent, setSent] = useState(false);
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSent(true);
  };
  const f = (k: string) => `${id}-${k}`;

  return (
    <section className="cta" id="contact" aria-labelledby={f("title")}>
      <div className="cta-grid">
        <div className="cta-head">
          <p className="cta-eyebrow">{eyebrow}</p>
          <h2 id={f("title")} className="cta-title">
            {title}
          </h2>
          <p className="cta-sub">{sub}</p>
          <p className="cta-slogan">{slogan}</p>
        </div>

        <form className="cta-form" onSubmit={onSubmit} onChange={() => sent && setSent(false)}>
          <div className="cta-field">
            <label htmlFor={f("name")}>{fields.name}</label>
            <input id={f("name")} name="name" autoComplete="name" required />
          </div>
          <div className="cta-field">
            <label htmlFor={f("company")}>{fields.company}</label>
            <input id={f("company")} name="company" autoComplete="organization" />
          </div>
          <div className="cta-field">
            <label htmlFor={f("email")}>{fields.email}</label>
            <input id={f("email")} name="email" type="email" autoComplete="email" required />
          </div>
          <div className="cta-field">
            <label htmlFor={f("phone")}>
              {fields.phone} <span className="cta-opt">({optional})</span>
            </label>
            <input id={f("phone")} name="phone" type="tel" autoComplete="tel" dir="ltr" />
          </div>
          <div className="cta-field cta-wide">
            <label htmlFor={f("interest")}>{fields.interest}</label>
            <select id={f("interest")} name="interest" defaultValue="" required>
              <option value="" disabled>
                {choose}
              </option>
              {interests.map((x) => (
                <option key={x}>{x}</option>
              ))}
            </select>
          </div>
          <div className="cta-field cta-wide">
            <label htmlFor={f("message")}>{fields.message}</label>
            <textarea id={f("message")} name="message" rows={4} />
          </div>
          <div className="cta-actions cta-wide">
            <button type="submit" className="btn-outline cta-submit">
              {submit}
              <Arrow />
            </button>
            <p className="cta-note" role="status">
              {sent ? sentNote : ""}
            </p>
          </div>
        </form>
      </div>
    </section>
  );
}
