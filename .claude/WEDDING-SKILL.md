# Wedding Site Skill (v2)

## Component library + swappable theme packs — not one fixed style

---

## WHY THIS CHANGED FROM v1

The original version of this skill hard-baked a single visual language (Cormorant Garamond + Jost, near-monochrome, editorial/typography-forward, Cordially.io-inspired) as _the_ wedding site look. That's now **one theme pack, not the whole skill**.

We're deliberately styling each build differently — 8 layout paradigms are in rotation (asymmetric editorial, full-bleed cinematic scroll, scrapbook/collage grid, magazine two-column, bento-box modular grid, split-screen duo, minimalist single-column storytelling, zine-style overlapping type & image — see the Dribbble Inspiration Stash), so the portfolio shows range instead of the same template re-skinned per couple.

What stays constant across every build is the **component library**: the functional sections (hero, story, schedule, tidbits, gifts, FAQ, faith, footer, RSVP, etc.) and their behavior. What changes per build is the **theme pack**: fonts, color tokens, layout treatment, and motion style that skin those components to match the chosen paradigm.

**When building a site:** first confirm which layout paradigm + reference link is assigned to this couple (see the Claude Code Starter prompt), then apply the matching theme pack below. If no theme pack exists yet for that paradigm, use "Theme A: Editorial Minimalist" structure as the component reference and design new tokens to fit the paradigm — then add the result back here as a new theme pack.

---

## PART 1 — COMPONENT LIBRARY (shared across all themes)

These are the functional sections. Their markup/behavior is theme-agnostic; only their visual skin changes.

### Hero

- Full viewport height (`100svh`)
- Content: eyebrow label → couple names → date → quote/scripture (optional) → scroll cue
- No hero photo required by default — themes should work image-light, though image-heavy paradigms (full-bleed cinematic scroll, scrapbook/collage) may lean on photography instead of typography as the hero device

### Our Story

- Eyebrow sentence intro (lowercase or theme-appropriate case)
- Narrative content — chaptered if long, single block if short
- Image-light themes: use pull-quotes / dividers between chapters instead of photos
- Image-heavy themes: chapters can pair with photography per the paradigm

### Schedule

- Date, countdown timer, venue name + address + map link, event cards per ceremony

### Tidbits / Details

- Card grid, 2–3 col desktop / 1 col mobile, arbitrary short-form info blocks

### Gifts

- "Your presence is the greatest gift" style opening line
- Payment details block (MoMo + bank), account numbers with copy-to-clipboard

### FAQ / Q&A

- Accordion, question/answer pairs

### Faith / Gospel (optional)

- Soft, non-intrusive section, expandable prayer/reflection text

### RSVP / Guest Management (Add-on package only)

- Reminders, meal selection, plus-ones, attendance list, CSV export

### Footer

- Closing line/quote, couple names + date, minimal — no heavy footer bar

### Analytics (every build, no exceptions)

- Wire up **Vercel Analytics** (or the equivalent on the deploy target) by default on every site.
- Zero extra cost, minimal setup — gives traction data per site (page views, which sections get scrolled to, RSVP conversion) without a per-build "should we track this" decision.
- Add to `<head>` per Vercel's standard snippet, or `@vercel/analytics` package if the build is React/Next-based.

---

## PART 2 — THEME PACKS (swap per build, based on assigned layout paradigm)

### Theme A: Editorial Minimalist _(default / fallback — matches "Minimalist single-column storytelling")_

Inspired by Cordially.io — editorial, image-light, typography-forward. Use when a couple's build is assigned the minimalist single-column storytelling paradigm, or as the fallback if no paradigm has been picked yet.

**Design philosophy:** typography as the hero, generous whitespace, lowercase editorial voice, restrained near-monochrome palette, full-width sections with centered ~720–900px containers, story-first structure.

**Fonts:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap"
  rel="stylesheet"
/>
```

| Role                 | Font               | Weight  | Style                      |
| -------------------- | ------------------ | ------- | -------------------------- |
| Hero names / display | Cormorant Garamond | 300–400 | Normal or italic           |
| Chapter headings     | Cormorant Garamond | 400     | Italic                     |
| Body / story text    | Cormorant Garamond | 300     | Normal                     |
| Nav, labels, badges  | Jost               | 300–400 | Uppercase or lowercase     |
| Eyebrow labels       | Jost               | 300     | Uppercase, ~0.2em tracking |
| Countdown, dates     | Jost               | 300     | Normal                     |
| Buttons              | Jost               | 400     | Normal, slight tracking    |

**Type scale:**

```css
:root {
  --text-hero: clamp(3.5rem, 10vw, 8rem);
  --text-display: clamp(2rem, 5vw, 3.5rem);
  --text-chapter: clamp(1.4rem, 3vw, 2rem);
  --text-body: clamp(1rem, 1.5vw, 1.15rem);
  --text-label: 0.75rem;
  --text-button: 0.85rem;
  --leading-tight: 1.1;
  --leading-body: 1.8;
  --leading-display: 1.2;
  --tracking-wide: 0.15em;
  --tracking-hero: -0.02em;
}
```

**Color palette:**

```css
:root {
  --color-bg: #faf8f5;
  --color-bg-alt: #f2ede6;
  --color-surface: #ffffff;
  --color-text-primary: #1c1a18;
  --color-text-body: #3d3a36;
  --color-text-muted: #9a9189;
  --color-accent: #b5936a; /* swap per couple: sage #8FA68E, dusty rose #C4A0A0, slate blue #7A8FA6 */
  --color-border: #e2ddd6;
}
```

**Layout tokens:**

```css
:root {
  --container-max: 860px;
  --container-wide: 1100px;
  --section-padding-y: clamp(5rem, 10vw, 9rem);
  --section-padding-x: clamp(1.5rem, 5vw, 3rem);
  --gap-sm: 1rem;
  --gap-md: 2rem;
  --gap-lg: 4rem;
}
```

**Image-light strategies:** large italic pull-quotes, thin decorative rules, oversized low-opacity initials/date as background type, inline SVG botanical dividers, alternating `--color-bg`/`--color-bg-alt` for rhythm.

**Motion:** scroll-reveal fade-up via IntersectionObserver, nav hides on scroll down / shows on scroll up, accordion via `max-height` transition, no JS animation libraries.

**Copy conventions:** lowercase eyebrows and nav (`our story`, `june 18, 2027`), dates written out, sentence-case CTAs, one warm sentence per section intro.

**Checklist:**

- [ ] Google Fonts link (Cormorant Garamond + Jost)
- [ ] All tokens in `:root`
- [ ] Nav lowercase, hide-on-scroll
- [ ] Mobile hamburger menu
- [ ] No `font-weight: 700` anywhere
- [ ] Countdown wired up
- [ ] Copy-to-clipboard on account numbers
- [ ] `.reveal` scroll animation wired
- [ ] Analytics wired (see Part 1)

---

### Theme B: Modern Editorial _(matches "Asymmetric editorial layout" / "Magazine two-column")_

For builds assigned a more contemporary, off-center editorial paradigm rather than the classical-serif minimalist look — e.g. asymmetric layouts, magazine-style two-column spreads.

**Fonts (free equivalents to Aeonik + PP Editorial New):**

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<!-- Fraunces via Google Fonts -->
<link
  href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,400&display=swap"
  rel="stylesheet"
/>
<!-- Satoshi or General Sans via Fontshare -->
<link
  href="https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500&display=swap"
  rel="stylesheet"
/>
```

| Role                 | Font                      | Weight  | Style                                                        |
| -------------------- | ------------------------- | ------- | ------------------------------------------------------------ |
| Hero names / display | Fraunces                  | 300–400 | Normal or italic (soft-curve editorial serif)                |
| Body / UI / labels   | Satoshi (or General Sans) | 300–500 | Normal (geometric, warm sans — closest free match to Aeonik) |

Use the same type-scale / color-token / layout-token structure as Theme A, but swap the font-family values and lean into wider asymmetric grids, off-center hero text, and oversized cropped imagery rather than Theme A's centered whitespace approach.

**Note:** this theme pack is a starting point, not fully specified yet — flesh out layout/motion tokens the first time it's used on a live build, then update this section.

---

### Theme packs still to be written

Add a section here each time a new paradigm gets its first real build, so the tokens are captured instead of re-derived from scratch next time:

- [ ] Full-bleed cinematic scroll
- [ ] Scrapbook / collage grid
- [ ] Bento-box modular grid
- [ ] Split-screen duo layout
- [ ] Zine-style overlapping type & image

---

## BEFORE OUTPUT — UNIVERSAL CHECKLIST (any theme)

- [ ] Correct theme pack applied for this couple's assigned layout paradigm (not defaulted to Theme A out of habit)
- [ ] Component library sections match the couple's package (Essential vs Stress-Free vs add-ons)
- [ ] All design tokens in `:root`, no hardcoded values in component CSS
- [ ] Mobile-first, fast on low-bandwidth mobile networks
- [ ] Analytics wired (Vercel Analytics or deploy-target equivalent)
- [ ] Copy-to-clipboard on account numbers
- [ ] Countdown timer wired up
- [ ] Scroll-reveal / motion treatment matches the theme's motion style, not copy-pasted from a different theme
- [ ] README with domain setup + deploy steps
