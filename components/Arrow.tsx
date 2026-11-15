/** The small square arrow box on the right of each outline button (header + hero CTAs). */
export default function Arrow() {
  return (
    <span className="btn-arrow" aria-hidden="true">
      <svg viewBox="0 0 12 12" width="12" height="12">
        <path d="M3 9 9 3M4 3h5v5" fill="none" stroke="currentColor" strokeWidth="1.3" />
      </svg>
    </span>
  );
}
