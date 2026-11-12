"""Higgsfield API client for the CITIX MENA project (Python 3.8+, standard library only).

Sources (read before writing this, 2026-11-12):
  - https://docs.higgsfield.ai/docs/authentication        Authorization: Key KEY_ID:KEY_SECRET
  - https://docs.higgsfield.ai/docs/concepts/file-uploads POST /files/generate-upload-url -> PUT upload_url
  - https://docs.higgsfield.ai/docs/concepts/requests     POST /{model_id} -> request_id, status_url
  - https://docs.higgsfield.ai/docs/concepts/billing-and-retention  POST /estimate/{model_id} -> {"usd": "..."}
  - Model IDs: marketing-studio/image, kling-video/v4.0/image-to-video,
    bytedance/seedance-2.0/image-to-video (open.higgsfield.ai model pages)

Hard rules enforced here:
  - Credentials are read from .env only and are never printed or logged.
  - generate() always gets a quote first, refuses jobs above HIGGSFIELD_MAX_SPEND_USD,
    and refuses to submit unless confirm=True (CLI: --yes) after Wassim's OK.
  - 12_AQI_widget_ui.png is never uploaded.

CLI:
  python scripts/higgsfield.py test
  python scripts/higgsfield.py upload media/source/01_tom_day_photo.jpg [...]
  python scripts/higgsfield.py estimate MODEL_ID params.json
  python scripts/higgsfield.py generate MODEL_ID params.json [--yes]
  python scripts/higgsfield.py wait REQUEST_ID
  python scripts/higgsfield.py download REQUEST_ID DEST_DIR
"""
from __future__ import annotations

import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.higgsfield.ai"
ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
UPLOAD_CACHE = ROOT / "media" / "generated" / "uploads.json"  # git-ignored
NEVER_UPLOAD = {"12_AQI_widget_ui.png"}
UPLOAD_TTL = timedelta(days=6)  # Higgsfield deletes uploads within 7 days; re-upload after 6
TERMINAL = {"completed", "failed", "nsfw", "canceled", "cancelled"}
CONTENT_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".webp": "image/webp", ".gif": "image/gif", ".mp4": "video/mp4", ".wav": "audio/wav",
}


class HiggsfieldError(RuntimeError):
    pass


# ---------------------------------------------------------------- config

def _env() -> dict:
    if not ENV_FILE.exists():
        raise HiggsfieldError(".env not found at repo root (copy .env.example and fill it)")
    out = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    for k in ("HF_API_KEY_ID", "HF_API_KEY_SECRET"):
        if not out.get(k):
            raise HiggsfieldError(f"{k} is missing or empty in .env")
    return out


def _auth() -> str:
    e = _env()
    return f"Key {e['HF_API_KEY_ID']}:{e['HF_API_KEY_SECRET']}"


def max_spend() -> float:
    return float(_env().get("HIGGSFIELD_MAX_SPEND_USD", "0") or 0)


# ---------------------------------------------------------------- http

def _request(method: str, url: str, body: dict | None = None, extra: dict | None = None,
             auth: bool = True) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "citix-mena-pipeline/1.0"}
    if auth:
        headers["Authorization"] = _auth()
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    headers.update(extra or {})
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        # Only status + response body; request headers (credentials) are never included.
        detail = e.read().decode("utf-8", "replace")[:500]
        raise HiggsfieldError(f"HTTP {e.code} on {method} {url.split('?')[0]}: {detail}") from None
    except urllib.error.URLError as e:
        raise HiggsfieldError(f"Network error on {method} {url.split('?')[0]}: {e.reason}") from None


# ---------------------------------------------------------------- uploads

def _load_cache() -> dict:
    if UPLOAD_CACHE.exists():
        return json.loads(UPLOAD_CACHE.read_text(encoding="utf-8"))
    return {}


def _save_cache(cache: dict) -> None:
    UPLOAD_CACHE.parent.mkdir(parents=True, exist_ok=True)
    UPLOAD_CACHE.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def upload(path: str | Path, force: bool = False) -> str:
    """Upload a local file to Higgsfield storage and return its public URL.

    Higgsfield has no permanent asset IDs: uploads are deleted within 7 days, so the
    public URL is cached with its upload time and refreshed automatically after 6 days.
    """
    p = Path(path).resolve()
    if p.name in NEVER_UPLOAD:
        raise HiggsfieldError(f"{p.name} is code-only and must never be uploaded")
    if not p.is_file():
        raise HiggsfieldError(f"File not found: {p}")
    ctype = CONTENT_TYPES.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0]
    if ctype not in CONTENT_TYPES.values():
        raise HiggsfieldError(f"Unsupported content type for upload: {p.name}")

    cache = _load_cache()
    key = p.name
    hit = cache.get(key)
    if hit and not force:
        age = datetime.now(timezone.utc) - datetime.fromisoformat(hit["uploaded_at"])
        if age < UPLOAD_TTL and hit.get("size") == p.stat().st_size:
            return hit["public_url"]

    meta = _request("POST", f"{API}/files/generate-upload-url", {"content_type": ctype})
    put = urllib.request.Request(meta["upload_url"], data=p.read_bytes(), method="PUT",
                                 headers=dict(meta.get("upload_headers") or {"Content-Type": ctype}))
    try:
        with urllib.request.urlopen(put, timeout=300) as r:  # no Higgsfield credentials here
            if r.status not in (200, 201, 204):
                raise HiggsfieldError(f"Upload PUT returned {r.status} for {p.name}")
    except urllib.error.HTTPError as e:
        raise HiggsfieldError(f"Upload PUT failed for {p.name}: HTTP {e.code}") from None

    now = datetime.now(timezone.utc)
    cache[key] = {
        "public_url": meta["public_url"],
        "content_type": ctype,
        "size": p.stat().st_size,
        "uploaded_at": now.isoformat(timespec="seconds"),
        "expires_by": (now + timedelta(days=7)).isoformat(timespec="seconds"),
    }
    _save_cache(cache)
    return meta["public_url"]


# ---------------------------------------------------------------- cost + generation

def estimate(model: str, params: dict) -> float:
    """Free quote for a request: POST /estimate/{model_id} with the same params."""
    res = _request("POST", f"{API}/estimate/{model.strip('/')}", params)
    if "usd" in res:
        return float(res["usd"])
    # Some video models (e.g. Kling 4.0) return a per-second rate table instead:
    # {"type": "description", "pricing_description": "... 720p: $0.1257; 1080p: $0.1879. ..."}
    desc = res.get("pricing_description", "")
    if "per video second" in desc:
        import re
        rates = {k.lower(): float(v) for k, v in re.findall(r"(\d{3,4}p|4k|2k|1k)\s*:\s*\$(\d+(?:\.\d+)?)", desc, re.I)}
        res_key = str(params.get("resolution", "")).lower()
        if res_key in rates and params.get("duration"):
            return rates[res_key] * float(params["duration"])
    raise HiggsfieldError(f"Could not compute a price for {model}; refusing to proceed. Raw: {json.dumps(res)[:300]}")


def generate(model: str, params: dict, confirm: bool = False) -> dict:
    """Quote, enforce the spend cap, then submit. Returns the submission response."""
    usd = estimate(model, params)
    cap = max_spend()
    print(f"Quote for {model}: ${usd:.4f} (cap ${cap:.2f})")
    if cap <= 0 or usd > cap:
        raise HiggsfieldError(f"Refused: ${usd:.4f} is above HIGGSFIELD_MAX_SPEND_USD (${cap:.2f})")
    if not confirm:
        raise HiggsfieldError("Not submitted: re-run with confirm=True / --yes after Wassim approves the quote")
    return _request("POST", f"{API}/{model.strip('/')}", params,
                    extra={"Idempotency-Key": str(uuid.uuid4())})


def status(request_id: str) -> dict:
    return _request("GET", f"{API}/requests/{request_id}/status")


def wait(request_id: str, timeout_s: int = 1800) -> dict:
    """Poll with backoff until a terminal status (docs: concepts/polling)."""
    delay, start = 3.0, time.time()
    while True:
        res = status(request_id)
        st = res.get("status")
        if st in TERMINAL:
            return res
        if time.time() - start > timeout_s:
            raise HiggsfieldError(f"Timed out waiting for {request_id} (last status: {st})")
        time.sleep(delay)
        delay = min(delay * 1.5, 20.0)


def result_urls(res: dict) -> list[str]:
    urls = [i["url"] for i in res.get("images") or [] if i.get("url")]
    for k in ("video", "audio"):
        v = res.get(k)
        if isinstance(v, dict) and v.get("url"):
            urls.append(v["url"])
        elif isinstance(v, list):
            urls += [i["url"] for i in v if i.get("url")]
    return urls


def download(res: dict, dest_dir: str | Path, prefix: str | None = None) -> list[Path]:
    """Download every output of a completed request (outputs expire after 7 days)."""
    if res.get("status") != "completed":
        raise HiggsfieldError(f"Request is not completed (status: {res.get('status')})")
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    prefix = prefix or res.get("request_id", "hf")
    saved = []
    for n, url in enumerate(result_urls(res), 1):
        ext = Path(url.split("?")[0]).suffix or ".bin"
        out = dest / f"{prefix}_{n}{ext}"
        with urllib.request.urlopen(url, timeout=300) as r:
            out.write_bytes(r.read())
        saved.append(out)
    return saved


# ---------------------------------------------------------------- connection test

def test_connection() -> str:
    """Read-only check: an unknown request ID returns 404 with valid credentials, 401 without."""
    try:
        status("00000000-0000-0000-0000-000000000000")
        return "OK (unexpected 200 for dummy request)"
    except HiggsfieldError as e:
        msg = str(e)
        if "HTTP 401" in msg or "HTTP 403" in msg:
            raise HiggsfieldError("Authentication failed: credentials rejected (401/403)") from None
        if "HTTP 404" in msg or "HTTP 422" in msg or "HTTP 400" in msg:
            return f"OK: credentials accepted ({msg.split(':')[0]} for a dummy request, as expected)"
        raise


# ---------------------------------------------------------------- CLI

def _main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == "test":
            print(test_connection())
        elif cmd == "upload":
            for f in args:
                print(f"{Path(f).name}\t{upload(f, force='--force' in args)}") if f != "--force" else None
        elif cmd == "estimate":
            print(f"${estimate(args[0], json.loads(Path(args[1]).read_text(encoding='utf-8'))):.4f}")
        elif cmd == "generate":
            res = generate(args[0], json.loads(Path(args[1]).read_text(encoding="utf-8")),
                           confirm="--yes" in args)
            print(json.dumps({k: res.get(k) for k in ("request_id", "status")}))
        elif cmd == "wait":
            res = wait(args[0])
            print(json.dumps({"status": res.get("status"), "outputs": len(result_urls(res))}))
        elif cmd == "download":
            for p in download(wait(args[0]), args[1]):
                print(p)
        else:
            print(f"Unknown command: {cmd}")
            return 1
    except HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
