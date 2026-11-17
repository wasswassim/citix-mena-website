/** Loading screen switch (components/SiteLoader.tsx). Plain module so the server page can inline the script. */
export const LOADER_KEY = "citix-loader-seen";
// Runs before first paint: the loader plays once per session, never with reduced motion (no JS = never shown).
export const LOADER_SCRIPT = `(function(){try{var d=document.documentElement;if(!sessionStorage.getItem("${LOADER_KEY}")&&!matchMedia("(prefers-reduced-motion: reduce)").matches)d.dataset.loader="on";}catch(e){}})();`;
