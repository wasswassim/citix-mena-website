/**
 * Button icon (Wassim, 17 Nov 2026, icon style A): the chevron of the CITIX logo ("CITIX › MENA"), replacing the
 * bluesqx-style diagonal arrow in a square box. A plain chevron, no box; it slides forward on hover and points
 * left in Arabic (app/globals.css, .btn-arrow).
 */
export default function Arrow() {
  return (
    <span className="btn-arrow" aria-hidden="true">
      <svg viewBox="0 0 10 12" width="10" height="12">
        <path d="M3 1.5 7.5 6 3 10.5" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinejoin="miter" />
      </svg>
    </span>
  );
}
