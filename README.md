# Dag & Gayle — Wedding Site

Static, dependency-free HTML/CSS/JS (no build step) for Dag Josiah & Gayle Hughes' wedding, 8th August 2026.

**Layout paradigm:** Minimalist single-column storytelling (per `.claude/WEDDING-SKILL.md`, Theme A structure), themed to this couple's **chrome & white** palette with a **Fraunces + Satoshi** primary font pairing (falls back to Cormorant Garamond + Jost — see [Fonts](#fonts)).

**Package:** Essential + Photo Gallery (Pro) + Guest Photo Sharing add-ons. Hero feature: guided-prompt Guest Wishes Wall.

## Structure

```
index.html          — main site (hero, wishes+photos memory card, story, schedule, teasers, tidbits, faq, gifts, footer)
programme.html      — order of service / officiating ministers / order of photography
gallery.html        — Photo Gallery (Pro) add-on, static grid + lightbox
memories.html       — full wish wall + full guest photo gallery, paginated from the guest-content backend
cfw-guest-content.js — vendored client for the shared CF Weddings guest-content backend (Guest Wishes Wall + Guest Photo Sharing)
pictures/           — all site images (WebP, -sm/-lg srcset pairs) + qr-code.png/.svg + invitation-preview.webp
  _originals/       — full-res camera JPGs the couple supplied (gitignored — reference only, never shipped)
dag-and-gayle-invitation.pdf — downloadable invitation placeholder
```

No npm, no framework, no build step. Every page is a single self-contained HTML file (styles + script inline), matching the pattern used across CF Weddings builds.

## Running locally

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Deploying

Any static host works. Two easy options:

**Vercel** (recommended — gives you the Analytics dashboard for free):
```bash
npx vercel --prod
```
No config needed; it's a static site. Vercel Web Analytics is already wired via the `<script defer src="https://cdn.vercel-insights.com/v1/script.js">` tag on every page — it activates automatically once the site is deployed on Vercel. No package install or extra setup required.

**GitHub Pages:**
1. Push this repo to GitHub (already has `origin` set to `dabick14/thejosiahs`).
2. Settings → Pages → Deploy from branch → `main` → `/ (root)`.
3. Site will be live at `https://dabick14.github.io/thejosiahs/`.

Note: Vercel Analytics only collects data when served from a Vercel deployment. If you deploy to GitHub Pages instead, swap the analytics script for GitHub Pages' equivalent or drop in Plausible/Umami — the `<script>` tag is the only thing that needs to change.

## Custom domain

The site currently uses a **placeholder domain** (`dagandgayle.com`) in:
- `pictures/qr-code.png` / `qr-code.svg` (regenerate once the real domain is live — see below)
- `dag-and-gayle-invitation.pdf` (regenerate the same way)
- Open Graph / meta text mentions in `index.html`

Once you've registered the real domain:
1. **Vercel:** Project → Settings → Domains → add the domain → follow the DNS records Vercel gives you (usually an `A` record to `76.76.21.21` and a `CNAME` for `www`).
2. **GitHub Pages:** add a `CNAME` file at the repo root containing the domain, then point your registrar's DNS at GitHub's IPs (see GitHub's "Managing a custom domain" docs) or a `CNAME` record to `dabick14.github.io`.
3. Regenerate the QR code and invitation PDF with the real URL:
   ```bash
   python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
   .venv/bin/python scripts/gen_qr.py https://your-real-domain.com
   .venv/bin/python scripts/gen_invitation.py
   ```

## Images

All 10 supplied photos are processed into WebP `-sm` (800px long edge) and `-lg` (1600px long edge) pairs, EXIF-stripped (no GPS/camera metadata shipped), served via jsDelivr once pushed to GitHub:

```
https://cdn.jsdelivr.net/gh/dabick14/thejosiahs@main/pictures/hero-01-lg.webp
```

Swap `src`/`srcset` in `index.html` and `gallery.html` to point at jsDelivr once the repo is pushed (currently relative paths, which also work fine on Vercel/GitHub Pages directly — jsDelivr is an optional extra CDN layer for edge caching, not required for the site to function).

Current allocation (10 photos total, deliberately not front-loaded into hero/story since this is a typography-led paradigm):
- **Hero:** 1 (subtle background wash, low-opacity)
- **Our Story:** 2
- **Gallery (Pro add-on):** 5
- **Guest Photo Sharing seed wall:** 2

To add more photos later (e.g. real wedding-day shots for the gallery), drop the full-res files into `pictures/_originals/`, add an entry to `scripts/process_photos.py`, and run it — it strips EXIF and produces the `-lg`/`-sm` WebP pair automatically.

## Guest Wishes Wall & Guest Photo Sharing — read before launch

Both features are merged into a single "Leave Dag & Gayle a memory" card (`#wishes` section in `index.html`) and backed by the shared CF Weddings guest-content service (`cfw-guest-content.js`, a vendored copy of the client from the `guest-content` backend repo). The card's "send" button calls `CFWGuestContent.submitWish()` and/or `.uploadPhoto()` depending on what the guest filled in; two capped, swipeable strips below it hydrate from `.listWishes()` / `.listPhotos()` on page load.

`CFWGuestContent.configure({ baseUrl })` currently points at the **production** Cloud Functions URL (`https://us-central1-cfweddingslive.cloudfunctions.net`). Before guests can actually use this on a live deployment, that deployment's real origin (Vercel domain, custom domain when set) must be registered against the backend via `node scripts/add-wedding.js dagandgayle <origin>` in the `guest-content` repo — the API enforces a per-wedding CORS allow-list and will 403 any unregistered origin.

For local development against the Firebase emulator instead of production, see the `guest-content` repo's README ("Local development" section) and temporarily point the `configure({ baseUrl })` call at `http://127.0.0.1:5001/demo-cfw-guest-content/us-central1`.

The "See the full wall →" / "Open the gallery →" links on the two preview strips point at `memories.html`, which paginates through every wish/photo via `listWishes`/`listPhotos`' `nextCursor` ("load more" buttons, `PAGE_SIZE = 12` per click) — no unbounded fetch, matches the backend's own page-size cap.

## Placeholder content — replace before go-live

Everything the couple hasn't finalized yet is marked `[Placeholder]` in the copy or flagged with an HTML comment:
- Our Story (both chapters + pull-quote)
- Couple Q&A answers
- Venue name (map link is real: the White Wedding ceremony pin)
- Style guide copy
- FAQ answers (plus-one, kids, contact names)
- MoMo number, bank name/account/sort code
- Officiating ministers, hymn titles, scripture readers (`programme.html`)
- Footer closing line/scripture
- Custom domain (see above)

Search for `[Placeholder` across the repo to find every instance.

## Fonts

Primary: **Fraunces** (display) + **Satoshi** (body/UI), loaded via Google Fonts + Fontshare. Fallback chain: **Cormorant Garamond + Jost** (also loaded), then system serif/sans — so if Fontshare is slow or unreachable on a guest's mobile connection, the page still lands on a real, already-loading webfont pairing instead of dropping straight to a system font.

## Analytics

Vercel Web Analytics is wired on all three pages via the standard `<script defer src="https://cdn.vercel-insights.com/v1/script.js">` snippet — zero package install, activates automatically on a Vercel deployment. Gives page views and visitor counts per page (including which of the three pages guests actually reach) at no extra cost.

## Accessibility / performance notes

- Hero content (couple names/date) is visible by default via CSS, not JS — it degrades gracefully if JS is slow or blocked.
- `prefers-reduced-motion: reduce` disables all animation/transition duration site-wide.
- All below-the-fold images use `loading="lazy"`; only the hero background is eager.
- All photos ship as WebP with `srcset` for two pixel densities/widths.
