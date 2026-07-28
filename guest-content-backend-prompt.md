# Prompt: CF Weddings shared guest-content backend

Hand this whole file to a fresh Claude Code session as the opening prompt for a **new, separate project/repo**. It is not part of any individual wedding site's codebase.

---

## Context

CF Weddings hand-builds bespoke wedding websites — one static, dependency-free HTML/CSS/JS repo per couple (no framework, no build step, no server), deployed to Vercel or GitHub Pages, images served off GitHub via jsDelivr. Each site reuses a shared **component library** (documented in each site's `.claude/WEDDING-SKILL.md`) but gets its own visual theme so the portfolio shows range.

Two components that keep showing up need a backend, and it doesn't make sense to build a one-off for each couple:

1. **Guest Wishes Wall** — guests leave a name + relationship + written wish, and it should appear on a wall that *every* visitor to that couple's site sees (not just the device that submitted it).
2. **Guest Photo Sharing** — guests upload photos from their phones during/after the wedding, and those photos should show up in a shared gallery on that couple's site.

The first real site built against this need is **`dagandgayle`** (repo: `dabick14/thejosiahs`, live wedding 8 Aug 2026). Its frontend currently has both features implemented as **frontend-only stubs**:

- Wishes persist to `localStorage` only, seeded with 2 sample entries.
- Photo sharing just previews picked files locally via `URL.createObjectURL` — nothing is uploaded anywhere.

Both stubs have a single clearly-marked seam in `index.html`'s inline `<script>`:
- `submitWish({ name, relation, text })` — currently reads/writes `localStorage`, flagged `// TODO(backend): replace localStorage persistence with a POST to the shared guest-content service`.
- A `change` handler on the photo `<input type="file" multiple>` — currently just local-previews, flagged similarly.

Your job: build the shared backend, then update the integration contract below so a follow-up pass on `dagandgayle` (and every future couple's site) is close to a drop-in swap.

## Non-negotiable constraints (inherited from how these sites are built)

- **No build step on the wedding-site side.** Every site is plain HTML/CSS/vanilla JS loaded straight in a browser — no npm, no bundler, no framework. Whatever you build must be callable from a `<script>` tag with `fetch()`, nothing more. A small vanilla-JS snippet file the couple sites can `<script src>` is ideal.
- **Multi-tenant from day one.** This backend serves *every* couple, not just `dagandgayle`. Every table/API call must be scoped by a wedding identifier (e.g. a slug like `dagandgayle`) with strict data isolation — one couple's wishes/photos must never be visible to another couple's site.
- **No guest login.** Wedding guests will not create accounts or authenticate. Submission should be frictionless (name + text, or name + photo) — but see abuse-prevention below.
- **Cheap.** Every other piece of this stack is free-tier (GitHub Pages/Vercel hosting, jsDelivr for images, Vercel Analytics). This backend should comfortably run on a free/near-free tier for the volumes involved (dozens to low hundreds of guests per wedding, not internet-scale).
- **Fast on weak mobile connections.** The brief for `dagandgayle` specifically calls out Ghanaian mobile networks; assume similar for future couples. Keep payloads small — resize/compress photos client-side before upload if practical, keep API responses light, avoid chatty polling if you can.
- **CORS-friendly for static origins.** Each couple's site lives on its own Vercel/GitHub Pages domain (and eventually a custom domain). The API needs permissive-but-scoped CORS — allow-list per registered wedding, not a global wildcard if avoidable.

## Recommended stack (default — deviate if you have a good reason)

**Supabase** (Postgres + Storage + Row Level Security) is the natural fit here: generous free tier, RLS gives you multi-tenant isolation without hand-rolling an API server, Storage handles guest photo uploads directly from the browser, and it's directly callable from vanilla JS via `@supabase/supabase-js` (or even raw REST calls, avoiding any bundler requirement). A `supabase` skill is available in this environment if you need reference docs on RLS/Storage/schema best practices — use it.

If you land on something else (e.g. Cloudflare Workers + D1 + R2), that's fine as long as the constraints above hold — just document why in the new repo's README.

## Functional requirements

### Wishes
- Create a wish: `{ wedding_slug, name, relation, text }` → stored, timestamped.
- List wishes for a wedding: newest-first (or let the frontend choose), paginated/limited (don't return unbounded history).
- Reasonable field limits (e.g. name ≤ 80 chars, text ≤ 500 chars) enforced server-side, not just client-side.

### Guest photos
- Upload one or more photos scoped to a wedding: accept common image types, cap file size (reject or auto-downscale oversized uploads — don't let a guest's 12MB HEIC photo blow the budget).
- List/serve photos for a wedding's shared gallery, newest-first.
- Store at a resolution reasonable for web display (you don't need to keep full-res originals — this is a guest-facing wall, not archival storage).

### Multi-tenant admin basics
- A way to register a new wedding (slug, allowed origin(s) for CORS) when onboarding each new couple — doesn't need a UI, a script or a row insert is fine for now.
- A way to hide/delete an individual wish or photo (spam, inappropriate content) without taking down the whole wall — a Supabase table edit is an acceptable "admin panel" for v1, but make the schema support a `hidden`/`approved` flag so a real admin UI can be added later without a migration.

### Abuse prevention (lightweight, not enterprise-grade)
- Basic rate limiting per IP per wedding (e.g. N submissions per minute) — RLS + a simple counter/policy, or Supabase Edge Function, whichever is simpler in your chosen stack.
- A honeypot field or similar cheap spam deterrent on the submission form contract.
- Server-side validation of field lengths/file types — never trust the client.

## Integration contract (what the wedding sites will call)

Design the actual API surface, but make sure it can support a JS module shaped roughly like this (the wedding-site side, no build step, plain `<script type="module">` or a plain global):

```js
// Conceptual shape — adjust to your actual endpoint/SDK, but keep it this simple to call.
await CFWGuestContent.submitWish({
  weddingSlug: 'dagandgayle',
  name: 'Auntie Efua',
  relation: 'Family',
  text: 'So happy for you both!',
});

const wishes = await CFWGuestContent.listWishes({ weddingSlug: 'dagandgayle' });

await CFWGuestContent.uploadPhoto({ weddingSlug: 'dagandgayle', file /* a File object */ });

const photos = await CFWGuestContent.listPhotos({ weddingSlug: 'dagandgayle' });
```

Ship this as a small, dependency-free (or single-CDN-script) JS file that any couple's static site can include, so retrofitting `dagandgayle` and building new sites both become "drop in this script + call these four functions" rather than a bespoke integration each time.

## Deliverables

1. New repo/project with the backend (schema + RLS policies + any edge functions, or equivalent for your chosen stack).
2. The drop-in frontend JS snippet described above.
3. A short README: how to onboard a new couple (register a wedding slug + allowed origin), how the abuse limits work, how to hide a submission, and — critically — the exact two seams to edit in `dagandgayle/index.html` (`submitWish()` and the photo-input `change` handler) to wire this backend in for real, replacing the `localStorage`/local-preview stubs.
4. Cost estimate / free-tier ceiling so CF Weddings knows when they'd need to upgrade a plan.

## Explicitly out of scope for v1

- Guest accounts/login.
- Real-time push updates (polling on page load / a manual refresh button is fine — this is a wedding wall, not a chat app).
- A polished admin dashboard (a documented path to build one later is enough).
