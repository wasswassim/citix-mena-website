# CITIX MENA website — homepage pitch

Homepage pitch for the new CITIX MENA website (citixmena.com): a 15-second intro film gate (muted loop, Enter + Unmute), then the hero with the new Tom smartboard and a day/night switch. Other pages are "coming soon" placeholders until the homepage is approved.

Project rules, brand guardrails and products: see [`CLAUDE.md`](CLAUDE.md).
Shot list and step-by-step prompts: [`docs/planning/CITIX_intro_ClaudeCode_prompts.md`](docs/planning/CITIX_intro_ClaudeCode_prompts.md).

## Structure

| Path | Contents | In git? |
|---|---|---|
| `media/source/` | Original reference files (Tom refs 01–11, AQI widget UI, Baloo and Jumbo real footage) | No |
| `media/stock/` | Free Pexels stock clips, `review/` frames, `LICENSES.md` | No |
| `media/generated/` | Higgsfield outputs (drafts, finals) | No |
| `media/web/` | Compressed web deliverables (MP4 + WebM, posters, end frames) | Yes, later |
| `docs/planning/` | Copies of the planning docs from the claude.ai Project | Yes |
| `docs/higgsfield-map.md` | Local file → Higgsfield asset ID → intended use | Yes |
| `scripts/` | Helper scripts (Higgsfield API client, ffmpeg helpers) | Yes |

## Secrets

The Higgsfield credentials live only in `.env` (git-ignored). Copy `.env.example` to `.env` and fill the values. Never commit `.env`. `HIGGSFIELD_MAX_SPEND_USD` caps the cost of any single job.

## Requirements

git, Node.js LTS, Python 3, ffmpeg/ffprobe, GitHub CLI.
