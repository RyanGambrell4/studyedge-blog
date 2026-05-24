# StudyEdge AI Blog

Astro blog hosted at **blog.getstudyedge.com**.

Light theme, matches the StudyEdge AI design tokens (`#F7F6F3` bg, `#3B61C4` accent, `#111111` text). Posts live in `src/content/posts/` as Markdown with frontmatter.

## Stack
- Astro 5 with Content Collections
- `@astrojs/mdx`, `@astrojs/sitemap`, `@astrojs/rss`
- Tailwind CSS (`@astrojs/tailwind`, base styles off)
- Hosted on Vercel

## First-time setup

```sh
npm install
```

Then verify it builds locally:

```sh
npm run dev      # http://localhost:4321
npm run build    # writes dist/
```

## Deploy to Vercel

This repo is configured for Vercel auto-detect via `vercel.json` (`framework: astro`).

1. Push this directory to its own GitHub repo, e.g. `studyedge-blog`.
2. In the Vercel dashboard, **Add New Project** and import `studyedge-blog`.
3. Build command: `npm run build` (auto-detected). Output: `dist/` (auto-detected).
4. Deploy.

## DNS — point `blog.getstudyedge.com` at this project

In your DNS provider for `getstudyedge.com`, add:

```
Type:   CNAME
Name:   blog
Value:  cname.vercel-dns.com
TTL:    Auto
```

Then in the Vercel project for `studyedge-blog`:
**Settings → Domains → Add → `blog.getstudyedge.com`**.

Vercel will provision the certificate automatically once DNS propagates.

## Writing a new post

Create `src/content/posts/<slug>.md`:

```md
---
title: "Your Title (also the H1)"
description: "150-160 char meta description used in og/twitter and listings."
pubDate: 2026-06-01
tag: "Exam Prep"   # one of: Exam Prep, GPA, Planning, Study Techniques, Pre-Med, Focus, ADHD
minutes: 9
---

## First H2

Body content. Use **bold** sparingly. No em dashes. No "leverage" / "utilize" / "delve into."

Internal links to the app:

- [Study planner](https://getstudyedge.com/study-planner-for-college-students)
- [Grade calculator](https://getstudyedge.com/grade-calculator)
- [Active recall app](https://getstudyedge.com/active-recall-app)
```

Schema validation lives in `src/content.config.ts`. The build will fail loudly if frontmatter is wrong.

## Writing rules (from AGENTS_SPEC.md)

- No em dashes anywhere. Use commas, colons, or restructure.
- No "leverage", "utilize", "delve into", "game-changer", "unlock your potential".
- Write like a smart upperclassman, not a marketing bot.
- 800-1,200 words per article. H1 = exact target keyword. H2s = related questions students Google.
- Every article includes one specific, actionable tip that StudyEdge AI does natively.
- Each article ends with a CTA to try StudyEdge AI free.
- Light theme only. Never link or include dark-themed assets.

## File layout

```
studyedge-blog/
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
├── vercel.json
├── package.json
├── public/
│   ├── favicon.png
│   ├── favicon.svg
│   └── robots.txt
└── src/
    ├── env.d.ts
    ├── content.config.ts
    ├── content/posts/*.md       # ← the articles
    ├── layouts/BaseLayout.astro
    ├── components/{Header,Footer,PostCard,CTA}.astro
    └── pages/
        ├── index.astro          # blog home
        ├── [...slug].astro      # post route
        └── rss.xml.js           # RSS feed at /rss.xml
```

Sitemap is generated automatically at `/sitemap-index.xml` by `@astrojs/sitemap`.

## What's left for the human

- [ ] Run `npm install` and confirm `npm run build` succeeds
- [ ] Create the GitHub repo and push
- [ ] Create the Vercel project from that repo
- [ ] Add the CNAME record for `blog.getstudyedge.com`
- [ ] Attach the domain in Vercel
- [ ] (Optional) Add the blog to Google Search Console as a new property
- [ ] (Optional) Add a link to `https://blog.getstudyedge.com` from the main app's footer
