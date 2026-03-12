# SelectFunders

**Sell Your Lottery Payments & Structured Settlements Fast**

SelectFunders is a modern web platform for buying lottery payments and structured settlements. This is the **Phase 1 MVP** built with Python + Cloudflare Pages.

🔗 **Live:** [selectfunders.pages.dev](https://selectfunders.pages.dev)  
📊 **Repository:** [github.com/esch8000/selectfunders](https://github.com/esch8000/selectfunders)  
📋 **Documentation:** [Project.md](./Project.md)

---

## Quick Start

### Build Locally

```bash
git clone https://github.com/esch8000/selectfunders.git
cd selectfunders

python3 build_site.py
```

This generates a fully static site in `selectfunders-site/`.

### Preview

```bash
cd selectfunders-site
python3 -m http.server 8000
# Open http://localhost:8000
```

### Deploy

Push to `main` branch:

```bash
git add .
git commit -m "Build updates"
git push origin main
```

GitHub Actions automatically builds and deploys to Cloudflare Pages.

---

## What's Included (Phase 1)

### ✅ Implemented

- **8 Core Pages:** Home, Apply, Services (2), How-It Works, FAQ, About, Calculator
- **50 State Pages:** Location-specific landing pages for SEO
- **3 Education Pages:** Lottery 101, Settlement Explained, Annuity Comparison
- **3 Blog Posts:** Placeholder for expansion
- **Full SEO:** Meta tags, sitemap, robots.txt, structured data (FAQPage, FinancialService, BreadcrumbList)
- **Mobile Responsive:** Mobile-first CSS design
- **Trust Signals:** Badges, testimonials framework, security headers
- **Lead Capture Form:** Contact form with form validation
- **Payment Calculator:** Rough estimate tool
- **Security:** Cloudflare headers, no hidden forms

### 📈 Next Phase (Phase 2)

- Blog expansion (30+ posts, keyword research)
- CRM integration (lead form to database)
- Customer testimonials
- Video hosting
- Analytics integration
- Email workflow

---

## Tech Stack

- **Generator:** Python 3.12+ (`build_site.py` - 47KB)
- **Hosting:** Cloudflare Pages
- **CI/CD:** GitHub Actions
- **Output:** Static HTML + Cache-busted CSS/JS
- **Format:** Responsive, semantic HTML5

### No Dependencies

- Pure Python (no external libs needed)
- Vanilla JavaScript (no frameworks)
- No build tools or npm required

---

## File Structure

```
selectfunders/
├── build_site.py              # Site generator (47KB, all-in-one)
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions → Cloudflare
├── selectfunders-site/        # Output (generated)
├── Project.md                 # Full documentation
└── README.md                  # This file
```

---

## Features

### 🎨 Design

- **Hero Sections:** Eye-catching banners with CTAs
- **Value Props Grid:** Responsive 3-column layout
- **Sidebar Forms:** Lead capture with client-side validation
- **FAQ Toggle:** Smooth expand/collapse with FAQ schema
- **Trust Badges:** Visual credibility signals
- **CTA Bands:** Compelling call-to-action sections
- **Footer:** Organized with links and legal

### 🔍 SEO

- Meta tags (title, description, canonical, OG, Twitter)
- Structured data (FinancialService, FAQPage, BreadcrumbList)
- Auto-generated sitemap.xml (with priorities)
- robots.txt
- Mobile-responsive (mobile-first CSS)
- Cache-busting CSS/JS (MD5 hashes)

### 📱 Mobile

- Responsive grid layouts
- Flexible navigation
- Touch-friendly forms
- Readable font sizes

### 🔒 Security

- HTML escaping (prevent XSS)
- Cloudflare security headers
- No external dependencies
- No third-party scripts

---

## How to Customize

### Change Site Title/Description

Edit `build_site.py` (top section):

```python
SITE_DOMAIN = "selectfunders.com"
SITE_TITLE = "SelectFunders - Your New Title"
SITE_DESC = "Your new description"
```

### Modify Templates

Edit template functions (e.g., `page_hero()`, `sidebar_form()`) in `build_site.py`.

### Add New Pages

1. Create a generator function: `def generate_my_page(): ...`
2. Call it in `build_all()`: `write_page("/my-page/", generate_my_page())`
3. Rebuild: `python3 build_site.py`

### Update Content

Edit FAQ data, value props, education content directly in `build_site.py`.

---

## Deployment

### 1. GitHub Setup

Already done! Repo created at `github.com/esch8000/selectfunders`.

### 2. Cloudflare Pages Setup

1. Go to Cloudflare Pages
2. Create project: `selectfunders`
3. Link to GitHub repo
4. Build command: `python3 build_site.py`
5. Output: `./selectfunders-site/`

### 3. Environment Variables

Add to GitHub Secrets:

- `CF_PAGES_DEPLOY_TOKEN` - Cloudflare API token
- `CF_ACCOUNT_ID` - Your Cloudflare account ID

### 4. DNS (Manual)

Point `selectfunders.com` to Cloudflare nameservers. Cloudflare will route it to Pages.

---

## Performance

- **Build Time:** ~1-2 seconds (local) / ~5-10 seconds (CI)
- **Total Pages:** 68 (8 core + 50 states + 3 education + 3 blog)
- **Site Size:** ~2-3 MB (all HTML + CSS + JS)
- **Cache Strategy:** 1-year immutable for assets (MD5 hashes)

---

## Statistics

| Metric | Phase 1 |
|--------|---------|
| Pages | 68 |
| Core Pages | 8 |
| State Pages | 50 |
| Education Pages | 3 |
| Blog Posts | 3 |
| Total Build Time | ~2s |
| Site Output | ~3 MB |

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile: iOS 14+, Android 10+

---

## FAQs

**Q: Do I need Node.js?**  
A: No. Python 3.12+ only.

**Q: Can I edit pages without rebuilding?**  
A: No. All pages are generated from `build_site.py`. Edit the generator, then rebuild.

**Q: What's in Phase 2?**  
A: Blog expansion, CRM integration, testimonials, video, analytics.

**Q: Is it SEO-friendly?**  
A: Yes! Sitemap, robots.txt, structured data, meta tags, mobile-responsive.

**Q: Can I use a custom domain?**  
A: Yes. Point your domain to Cloudflare, then set it in Pages settings.

---

## Support

See [Project.md](./Project.md) for full documentation, troubleshooting, and deployment instructions.

---

## License

Internal project. © 2024 SelectFunders.

---

**Status:** Phase 1 MVP Complete ✅  
**Next:** Phase 2 (Content & CRM)  
**Built with:** Python + Cloudflare Pages + GitHub Actions

