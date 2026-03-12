#!/usr/bin/env python3
"""
SelectFunders Site Generator
Phase 1 MVP - Python + Cloudflare Pages
Mirrors FHFunding architecture with modular templates and SEO
"""

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# ============================================================================
# CONFIG
# ============================================================================

SITE_DOMAIN = "selectfunders.com"
SITE_TITLE = "SelectFunders - Sell Lottery Payments & Structured Settlements"
SITE_DESC = "Get cash now for your lottery winnings or structured settlement. Fast, fair quotes. 50+ states served."
BUILD_DIR = "./selectfunders-site"
CURRENT_YEAR = datetime.now().year

STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

# ============================================================================
# SHARED CSS (Cache-busted with MD5)
# ============================================================================

SHARED_CSS = """
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background: #f9fafb;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #0066cc 0%, #004aa3 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 400px;
  height: 400px;
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
  transform: translate(100px, -100px);
}

.hero-content {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 700;
  line-height: 1.2;
}

.hero p {
  font-size: 1.3rem;
  margin-bottom: 40px;
  opacity: 0.95;
}

.cta-button {
  display: inline-block;
  background: #ff6b35;
  color: white;
  padding: 16px 40px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.cta-button:hover {
  background: #ff5a1f;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 107, 53, 0.3);
}

/* Navigation */
nav {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

nav ul {
  list-style: none;
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  justify-content: center;
  flex-wrap: wrap;
}

nav li {
  margin: 0 20px;
}

nav a {
  display: block;
  padding: 15px 0;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
}

nav a:hover {
  color: #0066cc;
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-section {
  padding: 60px 20px;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #1a1a1a;
  text-align: center;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666;
  text-align: center;
  margin-bottom: 50px;
}

/* Value Props Grid */
.value-props {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin: 40px 0;
}

.value-prop {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.value-prop:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.value-prop h3 {
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: #0066cc;
}

.value-prop p {
  color: #666;
  line-height: 1.8;
}

/* Sidebar Form */
.sidebar-form {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  max-width: 400px;
  margin: 0 auto;
}

.sidebar-form h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.form-submit {
  width: 100%;
  background: #ff6b35;
  color: white;
  padding: 14px;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.form-submit:hover {
  background: #ff5a1f;
}

/* FAQ Section */
.faq-list {
  max-width: 800px;
  margin: 40px auto;
}

.faq-item {
  background: white;
  margin-bottom: 15px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.faq-question {
  padding: 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #0066cc;
  transition: background 0.3s ease;
}

.faq-question:hover {
  background: #f0f5ff;
}

.faq-answer {
  padding: 0 20px;
  max-height: 0;
  overflow: hidden;
  transition: all 0.3s ease;
  color: #666;
}

.faq-item.active .faq-answer {
  padding: 20px;
  max-height: 500px;
}

.faq-toggle {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.faq-item.active .faq-toggle {
  transform: rotate(180deg);
}

/* Trust Badges */
.trust-badges {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
  margin: 40px 0;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
}

.badge {
  text-align: center;
  color: #666;
  font-size: 0.95rem;
}

.badge-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

/* CTA Band */
.cta-band {
  background: linear-gradient(135deg, #0066cc 0%, #004aa3 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
  margin: 60px 0;
}

.cta-band h2 {
  font-size: 2.2rem;
  margin-bottom: 20px;
}

.cta-band p {
  font-size: 1.1rem;
  margin-bottom: 30px;
  opacity: 0.95;
}

/* Footer */
footer {
  background: #1a1a1a;
  color: white;
  padding: 40px 20px;
  margin-top: 80px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
}

.footer-section h4 {
  margin-bottom: 20px;
}

.footer-section ul {
  list-style: none;
}

.footer-section a {
  color: #aaa;
  text-decoration: none;
  transition: color 0.3s ease;
  display: block;
  margin-bottom: 10px;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid #333;
  margin-top: 30px;
  color: #aaa;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .hero p {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  nav ul {
    padding: 0 10px;
  }
  
  nav li {
    margin: 0 10px;
  }
  
  nav a {
    padding: 12px 0;
    font-size: 0.95rem;
  }
  
  .value-props {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .value-prop {
    padding: 25px;
  }
  
  .trust-badges {
    gap: 15px;
  }
  
  .cta-band h2 {
    font-size: 1.5rem;
  }
}
"""

# ============================================================================
# SHARED JAVASCRIPT
# ============================================================================

SHARED_JS = """
document.addEventListener('DOMContentLoaded', function() {
  // FAQ Toggle
  document.querySelectorAll('.faq-question').forEach(function(question) {
    question.addEventListener('click', function() {
      const item = this.closest('.faq-item');
      item.classList.toggle('active');
    });
  });
  
  // Lead Form Handler
  const leadForm = document.getElementById('lead-form');
  if (leadForm) {
    leadForm.addEventListener('submit', function(e) {
      e.preventDefault();
      alert('Thank you! Our team will contact you shortly.');
      this.reset();
    });
  }
  
  // Calculator
  const calcType = document.getElementById('calc-type');
  const calcPayment = document.getElementById('calc-payment');
  const calcResult = document.getElementById('calc-result');
  
  if (calcType && calcPayment && calcResult) {
    function updateCalc() {
      const type = calcType.value;
      const payment = parseFloat(calcPayment.value) || 0;
      let estimate = 0;
      
      if (type === 'lottery') {
        estimate = Math.round(payment * 0.65);
      } else if (type === 'settlement') {
        estimate = Math.round(payment * 0.70);
      }
      
      calcResult.textContent = '$' + estimate.toLocaleString();
    }
    
    calcType.addEventListener('change', updateCalc);
    calcPayment.addEventListener('input', updateCalc);
  }
  
  // Mobile Nav Toggle (if needed)
  const navToggle = document.getElementById('nav-toggle');
  if (navToggle) {
    navToggle.addEventListener('click', function() {
      document.querySelector('nav ul').classList.toggle('active');
    });
  }
});
"""

# ============================================================================
# TEMPLATE FUNCTIONS
# ============================================================================

def get_css_hash():
    """Generate cache-busting hash for CSS"""
    return hashlib.md5(SHARED_CSS.encode()).hexdigest()[:8]

def get_js_hash():
    """Generate cache-busting hash for JS"""
    return hashlib.md5(SHARED_JS.encode()).hexdigest()[:8]

def page_head(title, description, og_image="", canonical=""):
    """Generate HTML head with SEO"""
    if not canonical:
        canonical = f"https://{SITE_DOMAIN}/"
    
    return f"""<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escape_attr(description)}">
  <meta name="theme-color" content="#0066cc">
  
  <!-- Open Graph -->
  <meta property="og:title" content="{escape_attr(title)}">
  <meta property="og:description" content="{escape_attr(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{escape_attr(canonical)}">
  {f'<meta property="og:image" content="{escape_attr(og_image)}">' if og_image else ''}
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape_attr(title)}">
  <meta name="twitter:description" content="{escape_attr(description)}">
  {f'<meta name="twitter:image" content="{escape_attr(og_image)}">' if og_image else ''}
  
  <!-- Canonical -->
  <link rel="canonical" href="{escape_attr(canonical)}">
  
  <!-- CSS -->
  <link rel="stylesheet" href="/assets/styles.{get_css_hash()}.css">
  
  <title>{escape_html(title)}</title>
</head>"""

def page_hero(title, subtitle="", cta_text="", cta_link=""):
    """Hero section template"""
    cta_html = ""
    if cta_text and cta_link:
        cta_html = f'<a href="{escape_attr(cta_link)}" class="cta-button">{escape_html(cta_text)}</a>'
    
    return f"""<section class="hero">
  <div class="hero-content">
    <h1>{escape_html(title)}</h1>
    {f'<p>{escape_html(subtitle)}</p>' if subtitle else ''}
    {cta_html}
  </div>
</section>"""

def sidebar_form(form_id="lead-form"):
    """Lead capture form"""
    return f"""<div class="sidebar-form">
  <h3>Get Your Quote</h3>
  <form id="{form_id}">
    <div class="form-group">
      <label for="name">Full Name</label>
      <input type="text" id="name" name="name" required>
    </div>
    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>
    </div>
    <div class="form-group">
      <label for="phone">Phone</label>
      <input type="tel" id="phone" name="phone">
    </div>
    <div class="form-group">
      <label for="type">Payment Type</label>
      <select id="type" name="type" required>
        <option value="">Select...</option>
        <option value="lottery">Lottery Winnings</option>
        <option value="settlement">Structured Settlement</option>
        <option value="annuity">Annuity</option>
      </select>
    </div>
    <div class="form-group">
      <label for="amount">Payment Amount</label>
      <input type="number" id="amount" name="amount" placeholder="$" required>
    </div>
    <button type="submit" class="form-submit">Get Free Quote</button>
  </form>
</div>"""

def faq_section(faqs):
    """FAQ section with toggle functionality
    faqs: list of (question, answer) tuples
    """
    items = ""
    for q, a in faqs:
        items += f"""<div class="faq-item">
    <div class="faq-question">
      <span>{escape_html(q)}</span>
      <span class="faq-toggle">▼</span>
    </div>
    <div class="faq-answer">{escape_html(a)}</div>
  </div>
"""
    return f"""<section class="content-section">
  <h2 class="section-title">Frequently Asked Questions</h2>
  <div class="faq-list">
    {items}
  </div>
</section>"""

def cta_band(headline, subheadline="", button_text="", button_link=""):
    """Call-to-action band"""
    cta_html = ""
    if button_text and button_link:
        cta_html = f'<a href="{escape_attr(button_link)}" class="cta-button">{escape_html(button_text)}</a>'
    
    return f"""<section class="cta-band">
  <h2>{escape_html(headline)}</h2>
  {f'<p>{escape_html(subheadline)}</p>' if subheadline else ''}
  {cta_html}
</section>"""

def trust_badges():
    """Trust signals"""
    return """<div class="trust-badges">
  <div class="badge">
    <div class="badge-icon">🏆</div>
    <div>Fast & Fair Quotes</div>
  </div>
  <div class="badge">
    <div class="badge-icon">🔒</div>
    <div>Secure & Confidential</div>
  </div>
  <div class="badge">
    <div class="badge-icon">✓</div>
    <div>No Hidden Fees</div>
  </div>
  <div class="badge">
    <div class="badge-icon">📞</div>
    <div>Expert Guidance</div>
  </div>
</div>"""

def page_footer():
    """Site footer"""
    return f"""<footer>
  <div class="footer-content">
    <div class="footer-section">
      <h4>SelectFunders</h4>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/apply/">Apply Now</a></li>
        <li><a href="/how-it-works/">How It Works</a></li>
        <li><a href="/about/">About Us</a></li>
      </ul>
    </div>
    <div class="footer-section">
      <h4>Services</h4>
      <ul>
        <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
        <li><a href="/structured-settlements/">Structured Settlements</a></li>
        <li><a href="/calculator/">Calculator</a></li>
      </ul>
    </div>
    <div class="footer-section">
      <h4>Learn</h4>
      <ul>
        <li><a href="/education/lottery-101/">Lottery Payments 101</a></li>
        <li><a href="/education/settlements/">Settlement Explained</a></li>
        <li><a href="/faq/">FAQ</a></li>
      </ul>
    </div>
    <div class="footer-section">
      <h4>Legal</h4>
      <ul>
        <li><a href="/privacy/">Privacy Policy</a></li>
        <li><a href="/terms/">Terms of Service</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>&copy; {CURRENT_YEAR} SelectFunders. All rights reserved. | <a href="/sitemap.xml">Sitemap</a></p>
  </div>
</footer>"""

def schema_financial_service():
    """FinancialService schema"""
    return """{
  "@context": "https://schema.org/",
  "@type": "FinancialService",
  "name": "SelectFunders",
  "url": "https://selectfunders.com",
  "description": "Lottery payment and structured settlement buyer",
  "serviceName": ["Lottery Payment Purchase", "Structured Settlement Purchase"],
  "areaServed": "US",
  "telephone": "+1-800-xxx-xxxx",
  "sameAs": [
    "https://www.facebook.com/selectfunders",
    "https://www.linkedin.com/company/selectfunders"
  ]
}"""

def schema_faq(faqs):
    """FAQPage schema"""
    items = []
    for q, a in faqs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }
    return json.dumps(schema)

def schema_breadcrumb(path_list):
    """BreadcrumbList schema"""
    items = []
    url = f"https://{SITE_DOMAIN}"
    
    items.append({
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": url
    })
    
    for i, (name, slug) in enumerate(path_list, start=2):
        url += f"/{slug}/"
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    return json.dumps(schema)

def escape_html(text):
    """Escape HTML entities"""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))

def escape_attr(text):
    """Escape HTML attribute values"""
    return (text
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))

# ============================================================================
# PAGE GENERATORS
# ============================================================================

def generate_homepage():
    """Generate homepage"""
    title = "SelectFunders - Sell Your Lottery Winnings & Structured Settlements Fast"
    desc = "Get immediate cash for your lottery payments or structured settlement. Fair quotes, no hidden fees. Apply today."
    
    breadcrumb = schema_breadcrumb([])
    faq_data = [
        ("How does SelectFunders work?", "We evaluate your payment plan and provide a fair quote for your remaining payments. Quick, transparent process."),
        ("What payments do you buy?", "Lottery winnings, structured settlements, annuities, and other future payment streams."),
        ("How much can I get?", "It depends on your payment amount, timeline, and terms. Get a free quote in minutes."),
        ("Is it confidential?", "Yes, we keep all information secure and confidential."),
    ]
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Turn Your Future Payments Into Cash Today",
    "Get fair quotes for lottery winnings, structured settlements, and annuities.",
    "Get Free Quote",
    "/apply/"
  )}
  
  <section class="content-section">
    <div class="container">
      <h2 class="section-title">Why Choose SelectFunders?</h2>
      <div class="value-props">
        <div class="value-prop">
          <h3>💰 Best Rates</h3>
          <p>Competitive cash offers for your future payments. Transparent pricing, no surprises.</p>
        </div>
        <div class="value-prop">
          <h3>⚡ Fast Process</h3>
          <p>From quote to approval in days. Get your cash when you need it.</p>
        </div>
        <div class="value-prop">
          <h3>🔒 100% Secure</h3>
          <p>Your information is safe with us. Confidential process from start to finish.</p>
        </div>
      </div>
      {trust_badges()}
    </div>
  </section>
  
  {cta_band(
    "Ready to Get Cash for Your Payments?",
    "We're here to help. Get a free quote in minutes.",
    "Get Started",
    "/apply/"
  )}
  
  {faq_section(faq_data)}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script type="application/ld+json">{schema_faq(faq_data)}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  
  {page_footer()}
</body>
</html>"""

def generate_apply():
    """Generate apply page"""
    title = "Apply for a Quote - SelectFunders"
    desc = "Apply for a free quote for your lottery winnings or structured settlement. Simple form, fast response."
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/apply/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Apply for Your Quote",
    "Get a fair offer for your lottery winnings or structured settlement.",
  )}
  
  <section class="content-section">
    <div class="container" style="max-width: 500px;">
      {sidebar_form("lead-form")}
    </div>
  </section>
  
  {cta_band(
    "Questions?",
    "Check out our FAQ or contact our team for help.",
    "View FAQ",
    "/faq/"
  )}
  
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_sell_lottery():
    """Generate lottery payments page"""
    title = "Sell Your Lottery Payments Fast - SelectFunders"
    desc = "Immediate cash for your lottery winnings. Fair quotes on annuities and lump sum settlements."
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/sell-lottery-payments/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Sell Your Lottery Payments",
    "Won the lottery? Get cash now instead of waiting years for payments.",
    "Get Quote",
    "/apply/"
  )}
  
  <section class="content-section">
    <div class="container">
      <h2 class="section-title">How It Works</h2>
      <div class="value-props">
        <div class="value-prop">
          <h3>1. Contact Us</h3>
          <p>Tell us about your lottery winnings and payment structure.</p>
        </div>
        <div class="value-prop">
          <h3>2. Get Quote</h3>
          <p>We analyze your payments and provide a fair cash offer.</p>
        </div>
        <div class="value-prop">
          <h3>3. Receive Cash</h3>
          <p>Accept the offer and receive your cash quickly.</p>
        </div>
      </div>
    </div>
  </section>
  
  {trust_badges()}
  
  {cta_band(
    "Ready to Sell Your Lottery Payments?",
    "Get a free quote today. No obligation.",
    "Apply Now",
    "/apply/"
  )}
  
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_structured_settlements():
    """Generate structured settlements page"""
    title = "Sell Structured Settlement Payments - SelectFunders"
    desc = "Convert structured settlement payments into cash now. Fair quotes guaranteed."
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/structured-settlements/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Sell Your Structured Settlement",
    "Need cash now? Convert your settlement payments into immediate funds.",
    "Get Quote",
    "/apply/"
  )}
  
  <section class="content-section">
    <div class="container">
      <h2 class="section-title">Structured Settlement Payments</h2>
      <p style="text-align: center; max-width: 700px; margin: 0 auto 40px;">
        Whether you received a settlement from an injury, lawsuit, or other claim,
        SelectFunders can help you convert those future payments into cash today.
      </p>
      
      <div class="value-props">
        <div class="value-prop">
          <h3>Lawsuit Settlements</h3>
          <p>Convert personal injury settlement payments into cash now.</p>
        </div>
        <div class="value-prop">
          <h3>Workers' Compensation</h3>
          <p>Get cash for structured workers' comp payments.</p>
        </div>
        <div class="value-prop">
          <h3>Annuities</h3>
          <p>Liquidate annuity payments on your timeline.</p>
        </div>
      </div>
    </div>
  </section>
  
  {trust_badges()}
  
  {cta_band(
    "Convert Your Payments to Cash",
    "Fair quotes, fast process, transparent pricing.",
    "Get Started",
    "/apply/"
  )}
  
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_how_it_works():
    """Generate how it works page"""
    title = "How SelectFunders Works - The Simple Process"
    desc = "3 simple steps to turn your future payments into cash. Apply, quote, receive. Fast and transparent."
    
    breadcrumb = schema_breadcrumb([("How It Works", "how-it-works")])
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/how-it-works/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Our Simple Process",
    "From application to cash in just a few days.",
  )}
  
  <section class="content-section">
    <div class="container">
      <div class="value-props">
        <div class="value-prop">
          <h3>📋 Step 1: Apply</h3>
          <p>Fill out our quick application with details about your payments. Takes just 5 minutes.</p>
        </div>
        <div class="value-prop">
          <h3>📊 Step 2: Get Quote</h3>
          <p>Our experts review your information and provide a fair cash offer within 24 hours.</p>
        </div>
        <div class="value-prop">
          <h3>💰 Step 3: Receive Cash</h3>
          <p>Accept your quote and receive funds quickly. Most approvals within 3-5 business days.</p>
        </div>
      </div>
    </div>
  </section>
  
  {cta_band(
    "Ready to Get Started?",
    "Apply now and receive your quote today.",
    "Apply Now",
    "/apply/"
  )}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_faq():
    """Generate FAQ page"""
    title = "FAQ - SelectFunders"
    desc = "Answers to common questions about selling lottery payments and structured settlements."
    
    faq_data = [
        ("What is SelectFunders?", "SelectFunders is a company that purchases future payment streams like lottery winnings, structured settlements, and annuities, giving you cash now."),
        ("What payments do you buy?", "We purchase lottery payments, structured settlements, annuities, workers' compensation payments, and other future payment obligations."),
        ("How much can I get?", "The amount depends on your payment structure, the remaining term, and current rates. We provide a customized quote."),
        ("How long does it take?", "From application to funding typically takes 3-7 business days. We provide a quote within 24 hours of receiving your information."),
        ("Is this legitimate?", "Yes, we are a licensed buyer of future payments. The sale of structured settlements is regulated by state laws."),
        ("Will I lose money?", "Yes, you'll receive less than the full remaining value of your payments, similar to how banks discount future payments. We provide fair market rates."),
        ("What are the fees?", "Our fees are included in the price we quote. No hidden charges or surprise fees."),
        ("Is this confidential?", "Completely. We maintain strict confidentiality throughout the process."),
        ("Can I only sell part of my payments?", "Yes, many customers sell a portion of their payments while keeping others."),
        ("What states do you serve?", "We serve all 50 states. Contact us for specific details about your location."),
    ]
    
    breadcrumb = schema_breadcrumb([("FAQ", "faq")])
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/faq/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Frequently Asked Questions",
    "Find answers to your questions about SelectFunders.",
  )}
  
  {faq_section(faq_data)}
  
  {cta_band(
    "Still Have Questions?",
    "Contact our team directly. We're here to help.",
    "Contact Us",
    "/apply/"
  )}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script type="application/ld+json">{schema_faq(faq_data)}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_about():
    """Generate about page"""
    title = "About SelectFunders"
    desc = "Learn about SelectFunders' mission to help people access their money when they need it most."
    
    breadcrumb = schema_breadcrumb([("About", "about")])
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/about/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "About SelectFunders",
    "Our mission is to help people access their funds when they need them most.",
  )}
  
  <section class="content-section">
    <div class="container" style="max-width: 800px;">
      <h2 class="section-title">Who We Are</h2>
      <p style="margin-bottom: 20px;">
        SelectFunders was founded with a simple mission: to help people turn their future
        payments into immediate cash. Whether you won the lottery, settled a lawsuit, or
        received an annuity, we believe you should have access to your money when you need it.
      </p>
      <p style="margin-bottom: 40px;">
        We combine industry expertise with transparent practices to deliver fair quotes and
        exceptional service. Our team has decades of experience in structured payments and
        financial services.
      </p>
      
      <h2 class="section-title">Why Trust Us?</h2>
      <div class="value-props">
        <div class="value-prop">
          <h3>Licensed & Regulated</h3>
          <p>We are licensed and compliant with state structured settlement regulations.</p>
        </div>
        <div class="value-prop">
          <h3>Fair Pricing</h3>
          <p>Competitive rates based on current market conditions and your specific circumstances.</p>
        </div>
        <div class="value-prop">
          <h3>Expert Team</h3>
          <p>Our professionals bring years of experience and genuine care for your situation.</p>
        </div>
      </div>
    </div>
  </section>
  
  {trust_badges()}
  
  {cta_band(
    "Ready to Work With Us?",
    "Get started today with a free, no-obligation quote.",
    "Apply Now",
    "/apply/"
  )}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_state_page(state):
    """Generate state-specific page"""
    slug = state.lower().replace(" ", "-")
    title = f"{state} Lottery Payment Buyer - SelectFunders"
    desc = f"Sell your lottery payments or structured settlement in {state}. Fast quotes, fair prices, no hidden fees."
    canonical = f"https://selectfunders.com/{slug}/"
    
    breadcrumb = schema_breadcrumb([(state, slug)])
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical=canonical)}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    f"Sell Your Lottery Payments in {state}",
    f"Get cash now for your {state} lottery winnings or structured settlement.",
    "Get Free Quote",
    "/apply/"
  )}
  
  <section class="content-section">
    <div class="container">
      <h2 class="section-title">Lottery Payments & Settlements in {state}</h2>
      <p style="text-align: center; max-width: 700px; margin: 0 auto 40px;">
        Won the {state} Lottery or received a structured settlement? SelectFunders can help you
        convert those future payments into cash today. We serve all residents of {state}.
      </p>
      
      <div class="value-props">
        <div class="value-prop">
          <h3>Local Expertise</h3>
          <p>We understand {state} regulations and can help you navigate the process smoothly.</p>
        </div>
        <div class="value-prop">
          <h3>Fast Process</h3>
          <p>Get a quote quickly and receive your cash within days of approval.</p>
        </div>
        <div class="value-prop">
          <h3>Fair Rates</h3>
          <p>Competitive pricing based on current market rates and your specific situation.</p>
        </div>
      </div>
    </div>
  </section>
  
  {trust_badges()}
  
  {cta_band(
    f"Ready to Sell Your Payments in {state}?",
    "Apply now for a free quote.",
    "Get Started",
    "/apply/"
  )}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_education_page(slug, title, content):
    """Generate education/blog page"""
    full_title = f"{title} - SelectFunders"
    canonical = f"https://selectfunders.com/{slug}/"
    breadcrumb = schema_breadcrumb([("Learn", "education"), (title, slug)])
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(full_title, content[:150], canonical=canonical)}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(title, f"Learn about {title.lower()}")}
  
  <section class="content-section">
    <div class="container" style="max-width: 800px;">
      {content}
    </div>
  </section>
  
  {cta_band(
    "Ready to Sell Your Payments?",
    "Get a free quote today.",
    "Apply Now",
    "/apply/"
  )}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

def generate_calculator():
    """Generate calculator page"""
    title = "Lottery Payment & Settlement Calculator - SelectFunders"
    desc = "Estimate how much cash you can receive for your lottery payments or structured settlement."
    
    breadcrumb = schema_breadcrumb([("Tools", "tools"), ("Calculator", "calculator")])
    
    return f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc, canonical="https://selectfunders.com/calculator/")}
<body>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/apply/">Apply</a></li>
      <li><a href="/sell-lottery-payments/">Lottery Payments</a></li>
      <li><a href="/structured-settlements/">Settlements</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/faq/">FAQ</a></li>
    </ul>
  </nav>
  
  {page_hero(
    "Payment Calculator",
    "Get a rough estimate of how much cash you could receive.",
  )}
  
  <section class="content-section">
    <div class="container" style="max-width: 500px;">
      <div class="sidebar-form">
        <h3>Estimate Your Cash Value</h3>
        <div class="form-group">
          <label for="calc-type">Payment Type</label>
          <select id="calc-type">
            <option value="">Select...</option>
            <option value="lottery">Lottery Winnings</option>
            <option value="settlement">Structured Settlement</option>
          </select>
        </div>
        <div class="form-group">
          <label for="calc-payment">Annual Payment Amount</label>
          <input type="number" id="calc-payment" placeholder="$" value="0">
        </div>
        <div style="background: #f0f5ff; padding: 20px; border-radius: 6px; margin-top: 20px;">
          <p style="font-size: 0.9rem; color: #666; margin-bottom: 10px;">Estimated Cash Value:</p>
          <p id="calc-result" style="font-size: 2rem; color: #0066cc; font-weight: 700;">$0</p>
          <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
            <em>This is a rough estimate. Your actual offer may vary.</em>
          </p>
        </div>
        <a href="/apply/" class="cta-button" style="display: block; text-align: center; margin-top: 20px;">Get Real Quote</a>
      </div>
    </div>
  </section>
  
  {cta_band(
    "Ready for a Real Quote?",
    "Apply now for an accurate offer.",
    "Apply Now",
    "/apply/"
  )}
  
  <script type="application/ld+json">{breadcrumb}</script>
  <script src="/assets/script.{get_js_hash()}.js"></script>
  {page_footer()}
</body>
</html>"""

# ============================================================================
# BUILD PROCESS
# ============================================================================

def create_directory():
    """Create build directory"""
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(f"{BUILD_DIR}/assets", exist_ok=True)

def write_assets():
    """Write CSS and JS files with cache-busting"""
    css_file = f"{BUILD_DIR}/assets/styles.{get_css_hash()}.css"
    js_file = f"{BUILD_DIR}/assets/script.{get_js_hash()}.js"
    
    with open(css_file, "w") as f:
        f.write(SHARED_CSS)
    
    with open(js_file, "w") as f:
        f.write(SHARED_JS)

def write_page(slug, content):
    """Write HTML page to file"""
    if slug == "/":
        path = f"{BUILD_DIR}/index.html"
    else:
        path = f"{BUILD_DIR}/{slug.strip('/')}/index.html"
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def generate_sitemap():
    """Generate sitemap.xml"""
    now = datetime.now().isoformat()
    
    urls = [
        ("/", "1.0", now),
        ("/apply/", "0.9", now),
        ("/sell-lottery-payments/", "0.9", now),
        ("/structured-settlements/", "0.9", now),
        ("/how-it-works/", "0.8", now),
        ("/faq/", "0.8", now),
        ("/about/", "0.7", now),
        ("/education/lottery-101/", "0.7", now),
        ("/education/structured-settlements/", "0.7", now),
        ("/education/annuity-vs-lump-sum/", "0.7", now),
        ("/calculator/", "0.7", now),
    ]
    
    # Add state pages
    for state in STATES:
        slug = state.lower().replace(" ", "-")
        urls.append((f"/{slug}/", "0.8", now))
    
    # Add blog posts
    for i in range(1, 4):
        urls.append((f"/blog/post-{i}/", "0.6", now))
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for path, priority, date in urls:
        xml += f"""  <url>
    <loc>https://{SITE_DOMAIN}{path}</loc>
    <lastmod>{date}</lastmod>
    <priority>{priority}</priority>
  </url>
"""
    
    xml += '</urlset>'
    
    with open(f"{BUILD_DIR}/sitemap.xml", "w") as f:
        f.write(xml)

def generate_robots():
    """Generate robots.txt"""
    robots = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Sitemap: https://{SITE_DOMAIN}/sitemap.xml
"""
    with open(f"{BUILD_DIR}/robots.txt", "w") as f:
        f.write(robots)

def generate_headers():
    """Generate _headers for Cloudflare Pages"""
    headers = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable
"""
    with open(f"{BUILD_DIR}/_headers", "w") as f:
        f.write(headers)

def generate_redirects():
    """Generate _redirects for Cloudflare Pages"""
    redirects = ""
    with open(f"{BUILD_DIR}/_redirects", "w") as f:
        f.write(redirects)

def build_all():
    """Build entire site"""
    print("🏗️  SelectFunders Site Generator Started...")
    
    # Setup
    create_directory()
    write_assets()
    
    # Core pages
    print("📄 Building core pages...")
    write_page("/", generate_homepage())
    write_page("/apply/", generate_apply())
    write_page("/sell-lottery-payments/", generate_sell_lottery())
    write_page("/structured-settlements/", generate_structured_settlements())
    write_page("/how-it-works/", generate_how_it_works())
    write_page("/faq/", generate_faq())
    write_page("/about/", generate_about())
    write_page("/calculator/", generate_calculator())
    
    # Education pages
    print("📚 Building education pages...")
    lottery_101 = """
    <h2>Understanding Lottery Payments</h2>
    <p>When you win the lottery, you typically have two choices: receive your winnings as an annuity
    (payments over time) or as a lump sum. Many winners choose the annuity for stability, but life changes
    can happen. If you need cash now, SelectFunders can help.</p>
    <p>Most lottery winners don't realize they can sell their future payments. This is a legitimate financial
    option that allows you to access your money today instead of waiting 20+ years.</p>
    """
    write_page("/education/lottery-101/", 
               generate_education_page("education/lottery-101", "Lottery Payments 101", lottery_101))
    
    settlement_explained = """
    <h2>What Are Structured Settlements?</h2>
    <p>A structured settlement is an agreement where a defendant pays the plaintiff periodic payments
    rather than a single lump sum. These are common in personal injury, lawsuit settlements, and
    workers' compensation cases.</p>
    <p>If you have a structured settlement but need cash now for medical bills, debt, or life changes,
    you can sell your future payments to SelectFunders.</p>
    """
    write_page("/education/structured-settlements/",
               generate_education_page("education/structured-settlements", "Structured Settlements Explained", settlement_explained))
    
    annuity_comparison = """
    <h2>Annuity vs Lump Sum: Which Is Right for You?</h2>
    <p>When you win the lottery or receive a settlement, the annuity vs lump sum decision is critical.
    Each has pros and cons depending on your situation.</p>
    <p><strong>Annuity:</strong> Steady payments over time, less temptation to overspend, tax advantages.
    But you need to wait for your money.</p>
    <p><strong>Lump Sum:</strong> Instant access to most of your money, but taxes are higher and there's
    risk of overspending.</p>
    <p>If you chose the annuity but now need cash, SelectFunders offers a third option: sell some or all
    of your future payments today.</p>
    """
    write_page("/education/annuity-vs-lump-sum/",
               generate_education_page("education/annuity-vs-lump-sum", "Annuity vs Lump Sum Comparison", annuity_comparison))
    
    # State pages
    print(f"🗺️  Building {len(STATES)} state pages...")
    for state in STATES:
        slug = state.lower().replace(" ", "-")
        write_page(f"/{slug}/", generate_state_page(state))
    
    # Blog posts (minimal for Phase 1)
    print("📰 Building blog posts...")
    for i in range(1, 4):
        blog_content = f"""
        <h2>Blog Post {i}</h2>
        <p><em>Published {datetime.now().strftime('%B %d, %Y')}</em></p>
        <p>This is a sample blog post. In Phase 2, we'll expand the blog with keyword-optimized,
        long-form content for better SEO performance.</p>
        <p>Topics we'll cover include:</p>
        <ul style="margin: 20px 0; padding-left: 20px;">
          <li>Tax implications of selling structured settlements</li>
          <li>How to maximize your cash offer</li>
          <li>Common mistakes lottery winners make</li>
          <li>Your rights as a settlement payment owner</li>
        </ul>
        """
        write_page(f"/blog/post-{i}/",
                  generate_education_page(f"blog/post-{i}", f"Blog Post {i}", blog_content))
    
    # SEO files
    print("🔍 Generating SEO files...")
    generate_sitemap()
    generate_robots()
    generate_headers()
    generate_redirects()
    
    print(f"\n✅ Build complete!")
    print(f"📁 Output: {BUILD_DIR}/")
    print(f"🎯 Total pages: ~{8 + len(STATES) + 6}")
    print(f"⚡ Assets: styles.{get_css_hash()}.css, script.{get_js_hash()}.js")
    print(f"\nNext steps:")
    print(f"1. Push to GitHub: git push origin main")
    print(f"2. GitHub Actions will auto-deploy to Cloudflare Pages")
    print(f"3. Site available at: selectfunders.pages.dev")
    print(f"4. Point DNS selectfunders.com → Cloudflare nameservers (manual)")

if __name__ == "__main__":
    build_all()
