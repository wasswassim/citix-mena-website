/** Loading screen switch (components/SiteLoader.tsx). Plain module so the server page can inline the script. */
// Runs before first paint: the loader plays on every page load (Wassim, 17 Nov 2026), never with reduced motion
// (no JS = never shown).
export const LOADER_SCRIPT = `(function(){try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.dataset.loader="on";}catch(e){}})();`;
