# Frame Math: free filmmaker calculators

A static site (no server, no database) that earns from affiliate links and sends traffic to the Etsy shop.

## Files
- `pages.py`: the content of every page. Agents add a tool by adding an entry here.
- `build.py`: generates the HTML, `sitemap.xml` and `robots.txt`. Run `python3 build.py`.
- `style.css`: shared styles (light and dark).
- `previews/`: screenshots of the site.

## Before going live (needs Thane, once)
1. A GitHub account and a new public repo, for example `frame-math`. Free hosting comes from GitHub Pages.
2. Amazon Associates sign-up. Put the tag in `AMZ_TAG` in `build.py`. Amazon closes accounts that make no sales in 180 days, so apply after launch.
3. Optional: a B&H affiliate account (through Impact), a custom domain (about $12 a year), and Google Search Console to get indexed faster.
4. Put the Etsy shop URL in `ETSY` and the site URL in `SITE` in `build.py`.

## Weekly agent routine (once live)
- Add 1 new calculator or guide page, picked from filmmaker search demand. Ideas: ND filter stops, shutter angle to shutter speed, crop factor and equivalent focal length, lighting distance (inverse square), drone flight time, a bitrate list by camera model, 180-degree rule for frame rates, and a wedding videography pricing guide.
- Rebuild, check every page for JavaScript errors and mobile overflow, then push.
- Monthly: check for broken affiliate links and check Search Console clicks, then rewrite titles on pages that get impressions but no clicks.
