# LoopCast website

Product page for [LoopCast](https://loopcast.space/), an offline looping media player for conference and event screens.

- **Pages are generated.** Edit `tools/build.py` (page content, titles, descriptions, FAQ) or `tools/home.html` (the homepage body), then run `python3 tools/build.py` and commit the output. It writes every page, `404.html`, `sitemap.xml`, `robots.txt` and `site.webmanifest`.
- Shared styles are in `assets/site.css`; images, font and icons are in `assets/`.
- `app/index.html` is the browser version of LoopCast itself, opened by the page's "Open in your browser" button. The release workflow replaces it with the new build on every release; don't edit it here.
- Downloads come from this repo's **Releases**. The LoopCast release workflow (in the private app repo) publishes each new version here as `LoopCast-Setup.exe`, `LoopCast-Mac.dmg` and `LoopCast.html`, so the page's download links always point at the latest release.
- Hosted with GitHub Pages from the `main` branch at **loopcast.space** (the `CNAME` file sets the custom domain).

The Archivo font is used under the SIL Open Font License (`assets/ARCHIVO-OFL.txt`).

© 2026 Treetop Business Solutions
