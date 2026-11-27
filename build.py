# Generates the static site. Agents edit TOOLS and re-run this.
import json, datetime
SITE="https://infoneverplay-arch.github.io/Tess"  # GitHub Pages URL; change if a custom domain is added
ETSY="https://www.etsy.com/shop/YOURSHOP"  # replace after shop opens
AMZ_TAG="YOURTAG-20"  # Amazon Associates tag, after approval
def amz(q):
    u=f"https://www.amazon.com/s?k={q.replace(' ','+')}"
    return u if AMZ_TAG.startswith("YOUR") else u+f"&tag={AMZ_TAG}"
NAV=[("index.html","Home"),("recording-time-calculator.html","Storage"),("depth-of-field-calculator.html","Depth of Field"),("aspect-ratio-crop-calculator.html","Aspect Ratio"),("timelapse-calculator.html","Timelapse")]
def page(fn,title,desc,h1,lead,tool,js,article,gear,cta):
    nav="".join(f'<a href="{h}">{t}</a>' for h,t in NAV[1:])
    g="" if not gear else '<section class="gear"><h2>Gear that helps</h2><ul>'+"".join(f'<li><a href="{amz(q)}" rel="sponsored nofollow" target="_blank">{t}</a></li>' for t,q in gear)+'</ul>'+('' if AMZ_TAG.startswith('YOUR') else '<p style="font-size:13px;color:var(--muted)">As an Amazon Associate we earn from qualifying purchases.</p>')+'</section>'
    if "YOURSHOP" in ETSY: cta=None  # hide shop promo until the Etsy shop is live
    c=f'<section class="cta"><h2>{cta[0]}</h2><p>{cta[1]}</p><a href="{ETSY}" target="_blank">See the templates &rarr;</a></section>' if cta else ""
    ld=json.dumps({"@context":"https://schema.org","@type":"WebApplication","name":h1,"url":f"{SITE}/{fn}","applicationCategory":"MultimediaApplication","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}})
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE}/{fn}"><link rel="stylesheet" href="style.css">
<script type="application/ld+json">{ld}</script></head><body><header><nav class="nav"><a class="brand" href="index.html">Frame Math</a>{nav}</nav></header>
<main><h1>{h1}</h1><p class="lead">{lead}</p>{tool}{c}<article>{article}</article>{g}</main>
<footer>Free tools for filmmakers. Results are estimates; always check your camera's manual. Some links are affiliate links, which support this site at no cost to you. &copy; {datetime.date.today().year} Frame Math</footer>
<script>{js}</script></body></html>'''
    open(fn,"w").write(html)
from pages import PAGES
for p in PAGES: page(**p)
urls="".join(f"<url><loc>{SITE}/{p['fn']}</loc></url>" for p in PAGES)
open("sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built",len(PAGES),"pages")
