# SelectFunders Phase 1 MVP

## Overview

SelectFunders.com is a Cloudflare Pages + Python site generator for a lottery payment and structured settlement buyer. This project mirrors the FHFunding architecture for maintainability and scalability.

**Live URL:** selectfunders.pages.dev  
**DNS Target:** selectfunders.com (manual setup required)

---

## Architecture

### Technology Stack

- **Generator:** Python 3.12+ (single `build_site.py` script)
- **Hosting:** Cloudflare Pages
- **CI/CD:** GitHub Actions (auto-deploy on push to main)
- **Output:** Static HTML with cache-busted CSS/JS

### Code Organization

```
selectfunders/
├── build_site.py              # Main site generator (~47KB)
├── .github/
│   └── workflows/
│       └── deploy.yml         # Cloudflare Pages CI/CD
├── selectfunders-site/        # Build output (generated)
│   ├── index.html
│   ├── assets/
│   │   ├── styles.[hash].css
│   │   └── script.[hash].js
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── _headers               # Cloudflare security headers
│   └── _redirects             # Cloudflare redirects
├── README.md
└── Project.md                 # This file
```

### Build Process

1. Run `python3 build_site.py`
2. Generates all HTML pages in `selectfunders-site/`
3. Creates cache-busted CSS/JS with MD5 hashes
4. Generates sitemap.xml, robots.txt, _headers, _redirects
5. Output ready for Cloudflare Pages deployment

---

## Pages Generated (Phase 1)

### Core Pages (8)

| Page | URL | Purpose |
|------|-----|---------|
| Homepage | `/` | Hero, value props, trust badges, CTA |
| Apply | `/apply/` | Lead capture form |
| Lottery Payments | `/sell-lottery-payments/` | Service page 1 |
| Settlements | `/structured-settlements/` | Service page 2 |
| How It Works | `/how-it-works/` | 3-step process explanation |
| FAQ | `/faq/` | Toggle-based FAQ with schema |
| About | `/about/` | Team, mission, trust signals |
| Calculator | `/calculator/` | Rough estimate tool |

### State Pages (50)

- `/alabama/`, `/alaska/`, ... `/wyoming/`
- Template-generated with state-specific titles
- Optimized for local SEO

### Education Pages (3)

- `/education/lottery-101/` - Lottery Payments 101
- `/education/structured-settlements/` - Settlement Explained
- `/education/annuity-vs-lump-sum/` - Comparison guide

### Blog Posts (3)

- `/blog/post-1/`, `/blog/post-2/`, `/blog/post-3/`
- Placeholder content; expand in Phase 2

**Total Pages Generated:** 68 unique pages

---

## SEO Features

### Implemented in Phase 1

- ✅ **Meta Tags:** Title, description, canonical, OG, Twitter Card
- ✅ **Structured Data:**
  - FinancialService schema
  - FAQPage schema (with Q&A)
  - BreadcrumbList schema
- ✅ **Sitemap:** Auto-generated with priorities
- ✅ **Robots.txt:** Standard rules
- ✅ **Security Headers:** Via Cloudflare `_headers`
- ✅ **Mobile-Responsive CSS:** Mobile-first design
- ✅ **Cache Busting:** MD5 hash on CSS/JS for fresh assets

### Phase 2 Opportunities

- Blog expansion (30+ keyword-optimized posts)
- Local business schema for state pages
- FAQ expansion
- Internal linking optimization
- Performance metrics (Core Web Vitals)

---

## Credentials & Deployment

### GitHub Token

- Already authenticated via FHFunding project
- Used by `gh` CLI to create repos
- Same account: `esch8000`

### Cloudflare Setup

Required environment variables in GitHub Secrets:

```
CF_PAGES_DEPLOY_TOKEN    # Cloudflare API token (deploy scope)
CF_ACCOUNT_ID            # Cloudflare account ID
```

Obtain these from Cloudflare dashboard:
1. Account Settings → API Tokens
2. Create token with "Cloudflare Pages – Production" scope
3. Add to GitHub repo Secrets

**Build Command:** `python3 build_site.py`  
**Output Directory:** `./selectfunders-site/`  
**Project Name:** `selectfunders`

### DNS Configuration (Manual)

After deployment:

1. Point `selectfunders.com` to Cloudflare nameservers
2. Create CNAME: `www.selectfunders.com` → `selectfunders.pages.dev`
3. Cloudflare will handle routing to the Pages project

---

## Local Development

### Build Site Locally

```bash
python3 build_site.py
```

Output directory: `./selectfunders-site/`

### Preview Locally (Optional)

```bash
cd selectfunders-site
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Directory Structure After Build

```
selectfunders-site/
├── index.html
├── apply/index.html
├── sell-lottery-payments/index.html
├── structured-settlements/index.html
├── how-it-works/index.html
├── faq/index.html
├── about/index.html
├── calculator/index.html
├── alabama/index.html           # ... 49 more states
├── education/
│   ├── lottery-101/index.html
│   ├── structured-settlements/index.html
│   └── annuity-vs-lump-sum/index.html
├── blog/
│   ├── post-1/index.html
│   ├── post-2/index.html
│   └── post-3/index.html
├── assets/
│   ├── styles.[hash].css
│   └── script.[hash].js
├── sitemap.xml
├── robots.txt
├── _headers
└── _redirects
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] Clone repo: `git clone github.com/esch8000/selectfunders`
- [ ] Run build: `python3 build_site.py`
- [ ] Verify output: Check `selectfunders-site/` has all pages
- [ ] Test locally (optional): `cd selectfunders-site && python3 -m http.server 8000`

### GitHub Actions Setup

- [ ] Add `CF_PAGES_DEPLOY_TOKEN` to GitHub repo secrets
- [ ] Add `CF_ACCOUNT_ID` to GitHub repo secrets
- [ ] Verify `.github/workflows/deploy.yml` exists

### Cloudflare Pages Setup

- [ ] Create Cloudflare Pages project: `selectfunders`
- [ ] Link to GitHub repo: `esch8000/selectfunders`
- [ ] Set build command: `python3 build_site.py`
- [ ] Set output directory: `./selectfunders-site/`

### DNS Configuration (After Pages Deployment)

- [ ] Add Cloudflare nameservers to domain registrar
- [ ] Wait for propagation (15 min - 24 hours)
- [ ] Verify site is live at `selectfunders.pages.dev`
- [ ] Create DNS record in Cloudflare for custom domain

### Verification

- [ ] Homepage loads: https://selectfunders.pages.dev/
- [ ] All 68 pages generated
- [ ] CSS/JS loading with cache-bust hashes
- [ ] Sitemap accessible: `/sitemap.xml`
- [ ] Robots.txt accessible: `/robots.txt`
- [ ] Mobile responsive

---

## Code Style & Standards

### FHFunding Mirror

This project follows FHFunding architecture:

- **Single-file generator** for simplicity
- **Modular template functions** (page_hero, sidebar_form, etc.)
- **Shared CSS/JS** at top of file
- **Escaped output** (escape_html, escape_attr) for security
- **Python 3.12+** f-strings
- **Loop-generated state pages** (not hardcoded)

### CSS

- Mobile-first responsive design
- BEM-style class naming (`.sidebar-form`, `.faq-item`, etc.)
- CSS-in-string for single bundle
- Cache-busted via MD5 hash

### JavaScript

- Vanilla (no jQuery/frameworks)
- Event listeners on DOM elements
- FAQ toggle, form validation, calculator logic
- No dependencies

### HTML

- Semantic structure
- Proper heading hierarchy
- Alt text (where applicable)
- ARIA labels (future enhancement)

---

## Customization & Expansion

### Content Updates

Edit `build_site.py`:

1. **Update site info:** `SITE_DOMAIN`, `SITE_TITLE`, `SITE_DESC`
2. **Modify templates:** Edit functions like `page_hero()`, `sidebar_form()`
3. **Add pages:** Create new generator functions and call them in `build_all()`
4. **Update FAQs:** Edit `faq_data` lists in page generators

### Phase 2 Roadmap

- [ ] Blog expansion (30+ posts, keyword research)
- [ ] CRM integration (lead form → database)
- [ ] Customer testimonials section
- [ ] Local schema for state pages
- [ ] Analytics integration (GA4)
- [ ] A/B testing variants
- [ ] Email capture workflow
- [ ] PDF guides & downloadables
- [ ] Video hosting (testimonials, how-to)
- [ ] Live chat integration

### Performance Optimization (Phase 2)

- Minify CSS/JS
- Image optimization (WebP, lazy loading)
- Preload critical resources
- Implement CDN caching strategy
- Monitor Core Web Vitals

---

## Troubleshooting

### Build fails

```bash
# Check Python version
python3 --version  # Should be 3.12+

# Run build with verbose output
python3 build_site.py 2>&1 | head -50
```

### Pages not deploying

1. Check GitHub Actions log: Repo → Actions tab
2. Verify Cloudflare API token in secrets (Settings → Secrets)
3. Ensure `CF_ACCOUNT_ID` is correct

### Site looks broken

1. Check browser console for 404s
2. Verify CSS/JS hashes match in HTML (e.g., `styles.abc12345.css`)
3. Ensure `selectfunders-site/` directory has all files

### Sitemap/robots.txt missing

- Run `python3 build_site.py` again locally
- Check `selectfunders-site/` directory contents
- Verify GitHub Actions completed successfully

---

## Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review `build_site.py` comments
3. Verify Cloudflare Pages documentation: https://developers.cloudflare.com/pages/
4. Check GitHub Actions logs for deployment errors

---

## License

SelectFunders Phase 1 MVP - Internal Project  
© 2024 SelectFunders. All rights reserved.

---

**Last Updated:** 2024-03-11  
**Status:** Phase 1 Complete  
**Next Milestone:** Phase 2 (Content Expansion & CRM Integration)
