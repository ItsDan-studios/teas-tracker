---
name: cloning-website-template
description: Analyzes any website or local project folder as a template, breaks down its key components, then clones and rebrands it for a new client company. Triggers when the user says "clone this for [company]", "create a website for [company]", "use this as a template", "rebrand for", or "new client website". Reads and maps every component of the source template, collects client intake info, copies the folder, substitutes all brand-specific content (name, tagline, colors, services, contact info, images), installs dependencies, and runs locally for preview.
---

# Cloning a Website Template for a New Client

## When to use this skill
- User says "clone this for [company]" or "use [folder] as a template"
- User wants a new client website based on an existing local project
- User provides a company name, services, or brand info to substitute into a base site
- User says "rebrand", "new folder for", or "same layout but for [company]"

---

## Pre-flight Checklist

- [ ] Template source folder identified (ask user if not specified)
- [ ] Template has been fully read and broken down (Step 1 — do this first)
- [ ] Client intake info collected — see [resources/client-intake.md](resources/client-intake.md)
- [ ] New folder name decided (e.g., `gb-hardscapes`, `peck-landscaping`)
- [ ] Client images available or placeholders confirmed
- [ ] Brand color known or derivable from logo

---

## Workflow

### Step 1 — Break down the template (ALWAYS first)

Before copying or editing anything, fully read and map the source template. This is the foundation of the entire clone.

**Read every source file** in the template folder:
- Root config files (`index.html`, `package.json`, any CSS entry point)
- All components (navbar, footer, any shared UI)
- All pages (every route/view)
- Any global style or theme file

**For each file, identify:**

| Question | Why it matters |
|---|---|
| What sections/components does it contain? | Defines the page structure to clone |
| What text is client-specific? | Names, taglines, services, locations, contact info |
| What is layout/structural (reusable)? | Do not change — it's the template's value |
| What images are used and from where? | Image paths to update |
| What color/token system is used? | CSS variables, Tailwind theme, or inline styles |
| What routing/navigation exists? | Pages to replicate in new folder |

**Produce a breakdown like this before proceeding:**

```
TEMPLATE: [folder name]
Stack: [React/Next/HTML/etc]
Pages: [list all routes]
Components: [Navbar, Footer, etc — one line each describing what they contain]
Color system: [CSS vars / Tailwind config / inline — list token names and roles]
Images: [list all image references and where each is used]
Brand-specific strings: [company name occurrences, phone, email, address, tagline]
Reusable (do not change): [layout classes, animation logic, routing, utilities]
```

Only proceed to Step 2 once this map is complete.

---

### Step 2 — Collect client info

Try fetching the client's existing website first:
```
WebFetch the client URL — extract: company name, tagline, services, contact info, testimonials, service areas
```

If the site is JS-rendered or unavailable, use the intake form:

| Field | Required | Placeholder if unknown |
|---|---|---|
| Company name | Yes | — |
| Sub-brand / division | No | omit |
| Tagline | Yes | `[TAGLINE]` |
| Services (3 featured + full list) | Yes | `[SERVICE]` |
| Primary brand color (hex) | No | derive from logo or use neutral |
| Phone | No | `[PHONE]` |
| Email | No | `[EMAIL]` |
| Address | No | `[ADDRESS]` |
| Hours | No | `[HOURS]` |
| Service area | Yes | `[SERVICE AREA]` |
| New folder name | Yes | — |
| Image source | No | use template defaults |

Any missing field gets a `[PLACEHOLDER]` — never block on missing info.

---

### Step 3 — Copy the template

```bash
cp -r "<template-folder>" "<new-folder-name>"
rm -rf "<new-folder-name>/node_modules"
```

Verify:
```bash
ls "<new-folder-name>/src"
```

---

### Step 4 — Read all files in the new folder before editing

The editor requires every file to be read before it can be written. Read all source files in the new folder before making any changes.

---

### Step 5 — Apply substitutions

Use the breakdown from Step 1 as your guide. Work file by file:

#### Global branding (do first — cascades everywhere)

**Color/theme file** (e.g., `index.css`, `tailwind.config`, `theme.ts`):
- Replace all brand color tokens to match the client's palette
- Derive a full scale (dark → light) from their primary color if only one is given
- For dark/charcoal brands: use a charcoal + warm neutral accent scale
- For vibrant brands: derive from logo primary, build supporting shades

**Entry HTML** (e.g., `index.html`):
- `<title>` → company name
- `og:title`, `og:description` → company name + tagline
- `og:url` → client domain
- `og:image` → client hero image full URL

#### Shared components

**Navbar:**
- Company name + sub-brand
- Phone `href` on all CTA buttons (desktop + mobile)
- Swap or remove any industry-specific icon (e.g., `<TreePine>` → `<Hammer>`)

**Footer:**
- Company name + sub-brand
- Short brand description sentence
- Services column list
- Contact info block (address, phone, email)
- Copyright line
- Remove irrelevant social icons

#### Pages — substitute all client-specific content

For each page, use the breakdown map to locate and replace:
- All headings, subtext, badge/label text
- All data arrays (services, testimonials, portfolio projects, values/stats)
- All contact details
- All image paths
- All service area references
- Form `<select>` options (match client's service list)

Use `[PLACEHOLDER]` for any unknown values — never invent contact info.

---

### Step 6 — Handle images

Images typically live in `public/images/` or `assets/`.

- **Client has images:** copy them into the new folder's image directory
  ```bash
  cp "<source>/public/images/<file>.jpg" "<new-folder>/public/images/<file>.jpg"
  ```
- **No images yet:** leave template defaults — they work as placeholders
- **Hero image:** check how many places it's referenced (often 2–3: hero section, CTA background, OG meta tag) — update all of them

---

### Step 7 — Install and run locally

```bash
cd "<new-folder>"
npm install
npm run dev
```

Report the localhost URL to the user. Vite auto-selects an available port.

---

### Step 8 — Verify before handing off

- [ ] Company name correct in navbar and browser tab
- [ ] Brand colors applied (no leftover template colors)
- [ ] All pages/routes load without errors
- [ ] No visible `[PLACEHOLDER]` in hero, navbar, or footer
- [ ] Images load (no broken img tags)
- [ ] Contact form options match client's services

---

## Key principles

- **Understand before you clone.** Step 1 is non-negotiable — reading the template first prevents blind find-and-replace errors.
- **Separate structure from content.** Layout, animations, routing, and utility classes are the template's value — never touch them. Only substitute content and colors.
- **Placeholders over guessing.** Use `[FIELD]` for any unknown info. Never invent phone numbers, addresses, or testimonials.
- **One template can serve many clients.** The same base site can be reused indefinitely — each clone lives in its own folder with its own identity.

---

## Resources
- [resources/client-intake.md](resources/client-intake.md) — blank intake form to fill out before cloning
