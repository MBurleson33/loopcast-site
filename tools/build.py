#!/usr/bin/env python3
"""Builds the LoopCast site: every page, sitemap.xml, robots.txt, 404.html and the web manifest.

Run from the repo root:  python3 tools/build.py
Edit page content in PAGES below (or tools/home.html for the homepage body), then rebuild and commit.
app/index.html is not built here; the LoopCast release workflow updates it.
"""
import json, os, sys, datetime, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guides

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://loopcast.space'
TODAY = datetime.date.today().isoformat()
REL = 'https://github.com/MBurleson33/loopcast-site/releases/latest/download/'
DL_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>'

ORG = {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Treetop Business Solutions", "email": "hello@loopcast.space", "telephone": "+1-405-486-0215",
       "address": {"@type": "PostalAddress", "addressLocality": "Oklahoma City", "addressRegion": "OK", "addressCountry": "US"}}
APP = {"@type": "SoftwareApplication", "@id": f"{SITE}/#app", "name": "LoopCast",
       "url": f"{SITE}/", "image": f"{SITE}/assets/icon-512.png", "screenshot": f"{SITE}/assets/operator.webp",
       "applicationCategory": "MultimediaApplication", "applicationSubCategory": "Digital signage and presentation software",
       "operatingSystem": "Windows 10, Windows 11, macOS 12 or later, web browser",
       "description": "Offline looping media player for event screens. Plays a folder of images, PDFs and videos on a projector or TV, on repeat, without internet.",
       "featureList": ["Loops images, PDFs and video", "Folder-based playlists", "Projector output with live preview",
                       "Logo screen and fade to black", "Loop, repeat or stop per playlist", "Manual mode for presentation clickers",
                       "Countdown timer to a time or for minutes", "On-screen clock and message bar", "QR code overlay",
                       "Picture in picture camera", "Streaming window for OBS, vMix and Ecamm", "Phone remote control over Wi-Fi",
                       "Live web pages", "Send photos from a phone", "Live HDMI capture inputs", "Playlist schedule by time of day",
                       "Starts automatically for unattended screens", "Works offline"],
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
       "publisher": {"@id": f"{SITE}/#org"}, "downloadUrl": f"{SITE}/#download"}

GUIDES = [  # (path, title, one-line summary, group) for the /guides/ hub, related links and the sitemap
    ('/guides/loop-slideshow-on-tv/', 'How to loop a slideshow on a TV', 'Connect a laptop, extend the display, and keep pictures repeating all day.', 'How-to'),
    ('/guides/lobby-tv-slideshow-from-laptop/', 'Put a slideshow on a lobby TV from a laptop', 'Cables, sleep settings, and a screen that starts by itself.', 'How-to'),
    ('/guides/church-announcement-loop/', 'Set up a church announcement loop', 'A weekly routine any volunteer can run before the service.', 'How-to'),
    ('/guides/loop-powerpoint-pdf-on-projector/', 'How to loop a PowerPoint or PDF on a projector', 'Three ways, from PowerPoint’s own setting to a dedicated player.', 'How-to'),
    ('/guides/free-digital-signage-windows-mac/', 'Free digital signage for Windows and Mac', 'Five free ways to run a looping sign, and when each one fits.', 'How-to'),
    ('/guides/free-countdown-timer-event-screen/', 'A free countdown timer for event screens', 'Count down to a time, show a clock or a quick message.', 'Features'),
    ('/guides/qr-code-on-projector-screen/', 'Show a QR code on a projector or TV', 'Giving, registration or a survey, in a corner over your slides.', 'Features'),
    ('/guides/phone-remote-for-slideshow/', 'Run the slideshow from your phone', 'Next, logo, messages and countdowns from anywhere in the room.', 'Features'),
    ('/guides/picture-in-picture-slides-camera/', 'Show a camera over your slides', 'Picture in picture with fixed corners, shapes and borders.', 'Features'),
    ('/guides/obs-streaming-window/', 'Put looping slides into OBS, vMix or Ecamm', 'The streaming window for your livestream.', 'Features'),
    ('/guides/free-propresenter-alternatives/', 'The best free ProPresenter alternatives', 'FreeShow, OpenLP, LoopCast and PowerPoint, honestly compared.', 'Compare'),
    ('/guides/powerpoint-kiosk-mode/', 'PowerPoint kiosk mode, and when to use something else', 'Set it up, fix it, and know its limits.', 'Compare'),
    ('/guides/free-yodeck-screencloud-alternatives/', 'Free alternatives to Yodeck and ScreenCloud', 'What cloud signage costs per screen, and when free is enough.', 'Compare'),
]


PAGES_NAV = [  # footer links: (path, label)
    ('/features/', 'Features'), ('/uses/', 'Uses'),
    ('/conferences/', 'Conferences'), ('/churches/', 'Churches'), ('/trade-shows/', 'Trade shows'),
    ('/digital-signage/', 'Lobbies and schools'), ('/guides/', 'Guides'),
    ('/propresenter-alternative/', 'ProPresenter alternative'), ('/install/', 'Install help'), ('/faq/', 'FAQ'),
]

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, image=f"{SITE}/assets/og-logo.jpg", image_alt="The LoopCast logo on a black background.", ld=None, noindex=False):
    url = SITE + path
    graph = ld or []
    tags = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'}
<meta property="og:site_name" content="LoopCast">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{image}">
<meta name="theme-color" content="#0c0d10">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icon-512.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
'''
    if graph:
        tags += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>\n'
    return tags + '</head>\n<body>\n'

def header(home=False):
    links = '<a href="/features/">Features</a><a href="/uses/">Uses</a><a href="/faq/">FAQ</a>'
    return f'''<a class="promo" href="{'#download' if home else '/#download'}"><span class="promo-t"><b><span class="dot pulse"></span>Free during our launch.</b> <span>Download LoopCast now while it’s free.</span></span><span class="promo-go">Get it →</span></a>
<header class="wrap">
  <nav class="top" aria-label="Main">
    <a class="brand" href="/" aria-label="LoopCast home"><img src="/assets/mark.svg" width="32" height="27" alt=""><span>LoopCast</span></a>
    <div class="nav-r"><div class="nav-links">{links}</div><a class="btn ghost sm kofi-nav" href="https://ko-fi.com/loopcast" target="_blank" rel="noopener"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V9z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 3.5c0 1 1 1 1 2M12 3.5c0 1 1 1 1 2"/></svg><span>Support</span></a><a class="btn solid sm" href="/app/" target="_blank" rel="noopener">Open in your browser</a></div>
  </nav>
</header>
'''

# ---- Tracking (both stay off until filled in) ----
# GoatCounter: your site code, e.g. 'loopcast' for https://loopcast.goatcounter.com
GOATCOUNTER = 'loopcast'
# Optional email box after a download: the form's POST address and its email field name.
#   Kit:        action 'https://app.kit.com/forms/<FORM_ID>/subscriptions', field 'email_address'
#   Buttondown: action 'https://buttondown.com/api/emails/embed-subscribe/<USERNAME>', field 'email'
EMAIL_FORM = {'action': 'https://app.kit.com/forms/10131096/subscriptions', 'field': 'email_address'}

def tracking_tags():
    cfg = json.dumps({'gc': bool(GOATCOUNTER), 'form': EMAIL_FORM if EMAIL_FORM['action'] else None})
    tags = f'<script>window.LC_CFG={cfg}</script>\n<script src="/assets/track.js" defer></script>\n'
    if GOATCOUNTER:
        tags += f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
    return tags

FOOTER = '''<footer>
  <div class="wrap"><div>
    <nav class="foot-links" aria-label="More about LoopCast">''' + ''.join(f'<a href="{p}">{l}</a>' for p, l in PAGES_NAV) + '''</nav>
    <div class="foot-row">
      <span class="b"><img src="/assets/mark.svg" width="24" height="20" alt=""><span><b>LoopCast</b>, for every space with a screen.</span></span>
      <span>Questions? <a href="mailto:hello@loopcast.space">hello@loopcast.space</a> · <a href="tel:+14054860215">405-486-0215</a></span>
      <span><a href="https://ko-fi.com/loopcast" target="_blank" rel="noopener">Support LoopCast on Ko-fi</a></span>
      <span>Made by Treetop Business Solutions in Oklahoma City. © 2026</span>
    </div>
  </div></div>
</footer>
''' + tracking_tags()

GET = f'''<section id="download" class="s wrap">
  <div class="get">
    <h2>Ready when the doors open.</h2>
    <div class="grid3">
      <a class="dl" href="{REL}LoopCast-Setup.exe"><b>Download for Windows</b><span>Windows 10 or 11</span></a>
      <a class="dl" href="{REL}LoopCast-Mac.dmg"><b>Download for Mac</b><span>macOS 12 or later, Apple silicon or Intel</span></a>
      <a class="dl alt" href="/app/" target="_blank" rel="noopener"><b>Open in your browser</b><span>Nothing to install</span></a>
    </div>
    <p>Your computer will show a security warning the first time you open it. That’s expected. <a href="/install/">Here’s why, and what to click</a>.</p>
  </div>
</section>
'''

def crumbs_ld(path, name):
    items = [("LoopCast", SITE + "/")]
    if path.startswith('/guides/') and path != '/guides/':
        items.append(("Guides", SITE + "/guides/"))
    items.append((name, SITE + path))
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

BLURBS = {'/guides/': 'Step-by-step how-tos', '/features/': 'Everything LoopCast can do', '/uses/': 'Conferences, churches, booths, lobbies', '/conferences/': 'Walk-in loops, agendas and sponsors', '/churches/': 'Pre-service announcement loops',
          '/trade-shows/': 'All-day loops on the booth TV', '/digital-signage/': 'Lobby, hallway and office screens', '/propresenter-alternative/': 'An honest comparison',
          '/install/': 'Why Windows and Mac warn you, and what to do', '/faq/': 'Projectors, files, installs'}
TITLES = dict(PAGES_NAV)
TITLES['/propresenter-alternative/'] = 'LoopCast vs ProPresenter'
for _p, _t, _d, _g in GUIDES:
    TITLES[_p], BLURBS[_p] = _t, _d

def related(current, picks=None):
    picks = [p for p in (picks or []) if p != current] or [p for p, _ in PAGES_NAV if p != current][:3]
    return '<div class="related">' + ''.join(f'<a href="{p}"><b>{TITLES[p]}</b><span>{BLURBS[p]}</span></a>' for p in picks[:3]) + '</div>'

def page(path, crumb, title, desc, h1, lede, body, image=None, image_alt=None, extra_ld=None, wide=False, rel=None):
    ld = [ORG, APP, crumbs_ld(path, crumb)] + (extra_ld or [])
    kw = {}  # every page shares the logo preview image
    out = head(title, desc, path, ld=ld, **kw)
    out += header()
    out += f'''<main>
  <div class="wrap">
    <p class="crumbs"><a href="/">LoopCast</a> › {'<a href="/guides/">Guides</a> › ' if path.startswith('/guides/') and path != '/guides/' else ''}{esc(crumb)}</p>
    <div class="page-hero">
      <h1>{h1}</h1>
      <p>{lede}</p>
      <div class="ctas"><a class="btn solid" href="#download">{DL_ICON}Download free</a><a class="btn ghost" href="/app/" target="_blank" rel="noopener">Open in your browser</a></div>
    </div>
    {body if wide else '<div class="prose">' + chr(10) + body + chr(10) + '    </div>'}
    <div class="more"><div class="eyebrow">Keep reading</div>
    {related(path, rel)}</div>
  </div>
  {GET}
</main>
{FOOTER}</body>
</html>
'''
    dest = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w').write(out)

def fig(src, alt, caption, w=1600, h=900):
    return f'<figure class="figure"><img src="/assets/{src}" width="{w}" height="{h}" loading="lazy" alt="{esc(alt)}"><figcaption>{caption}</figcaption></figure>'

FAQS = [
    ("Is LoopCast free?", "Yes, LoopCast is free during our launch. You can download it for Windows and Mac, or open it in your browser, at no cost."),
    ("Does it need internet?", "No. LoopCast runs on your computer and plays files from a folder on it. You only need internet to download it."),
    ("Will it work with our projector or TV?", "Yes, if your computer sees it as a second display: a projector, a TV, or an LED wall processor over HDMI, DisplayPort or USB-C. LoopCast opens the output fullscreen on it at its own resolution."),
    ("Can I send LoopCast to a livestream, like OBS?", "Yes. In Settings › Projector, choose a Streaming window (1920×1080 or 1280×720) and press Open streaming window. The show opens in its own window: add it to OBS, vMix or Ecamm as a Window Capture source and pick LoopCast Stream. Web pages, the clock and messages show up in the stream just like on the projector, and it keeps playing behind other windows (just don’t minimize it). This is a Pro feature, free while LoopCast is in its launch."),
    ("What if I only have one screen?", "Use Fullscreen here (the expand button, or the F key). LoopCast fills the screen it runs on, and Esc brings back the controls. If LoopCast only finds one display, Show on projector does this for you."),
    ("What kinds of files can I use?", "Images (JPG, PNG, GIF, WebP, SVG), PDFs, and video (MP4, WebM, MOV). Each page of a PDF becomes its own slide. MP4 with H.264 is the safest choice for video."),
    ("Can it play PowerPoint or Keynote files?", "Not directly. Save your deck as a PDF (in PowerPoint, File › Export › PDF; in Keynote, File › Export To › PDF) and put the PDF in the folder. If LoopCast finds a PowerPoint or Keynote file, it tells you how to export it."),
    ("Can I click through slides myself?", "Yes. Set a playlist’s Advance option to Manual and each slide stays up until you press next: the arrow keys, Page Up and Page Down, or a presentation clicker. Click any slide to jump straight to it. Videos play once and hold on their last frame."),
    ("Can I add or swap files during an event?", "Yes. Add or remove files in the folder and LoopCast picks up the changes the next time the playlist comes around, or right away if you press Rescan."),
    ("Can I show a countdown or a quick message?", "Yes. Press T (or Timer) for a countdown that covers the screen, like “We’ll be back in 10:00,” and returns to the slides at zero. Type a time instead of minutes, like 9:30 AM, to count down to it. Press M (or Message) to show a bar of text over whatever is playing, and C to show the time in a corner."),
    ("Can it switch playlists by itself at certain times?", "Yes. In Settings › Schedule, add times and the playlist for each, like Walk-in at 8:30 and Lunch at 12:00. For lobby TVs, LoopCast can also start the show automatically when it opens and open when the computer starts."),
    ("Can I show a live web page?", "Yes, in the desktop app. Open a playlist, choose Add web page, and paste the address. The page plays live like any other item: polls, social walls, schedules or dashboards. When the playlist is set to Manual, or the page is on repeat, you can click, scroll and type on it from the preview. Web pages need an internet connection."),
    ("Can I show a QR code on screen?", "Yes. Press QR (or Q), paste a link for giving, registration or a survey, and add a few words to go under it. LoopCast shows the code in a corner over whatever is playing until you press Q again. Pick the corner and size in Settings › QR code."),
    ("Can I control LoopCast from my phone?", "Yes, in the desktop app. Click From phone, choose Remote control and scan the code with a phone on the same Wi-Fi. The remote opens in the phone’s browser: next and back, Black, Logo, messages, countdowns, the clock, the QR code, picture in picture and switching playlists. This is a Pro feature, free while LoopCast is in its launch."),
    ("Can I show a camera in the corner of the slides?", "Yes, in the desktop app. Picture in picture puts a webcam or USB HDMI capture device in a corner of the screen while the slides keep changing behind it. Choose the camera, corner, size, shape and border in Settings › Picture in picture, then press PiP (or P). This is a Pro feature, free while LoopCast is in its launch."),
    ("Can I send photos from my phone?", "Yes, in the desktop app. Click From phone and LoopCast shows a QR code. Scan it with a phone on the same Wi-Fi, pick photos, videos or a PDF, and they arrive in a Phone uploads playlist within seconds. Nothing goes on screen until you choose Show now. Some guest and venue networks block devices from reaching each other; if the phone can’t connect, try another network."),
    ("Can I show a presenter’s laptop or a camera?", "Yes. Plug it into a USB HDMI capture stick and it shows up under Inputs. Preview it, then put it on screen with one click. The playlist waits underneath, and Logo and Black still work."),
    ("Does it work on a Mac?", "Yes, on macOS 12 or later, on Apple silicon and Intel Macs. The first time you open it, go to System Settings › Privacy & Security and choose Open Anyway."),
    ("Can I use it without installing anything?", "Yes. Open in your browser runs the full player in any modern browser. The desktop app adds a few conveniences, like opening the projector window fullscreen on its own."),
    ("Why does my computer warn me when I install it?", "LoopCast isn’t signed with a paid developer certificate yet. Without one, Windows and macOS can’t confirm who made the app, so they ask you to confirm the first time. The warning is about an unverified publisher; it doesn’t mean the app was found to be harmful. Download it only from loopcast.space. The Installing LoopCast page explains each step. On Windows choose More info, then Run anyway. On a Mac, go to System Settings › Privacy & Security and choose Open Anyway."),
    ("How do I get help or send feedback?", "Email hello@loopcast.space or call 405-486-0215. When you email, include your version number (click the LoopCast logo in the app to see it) and whether you use Windows, Mac or the browser version."),
    ("How do I show a logo between sessions?", "Put an image named logo.png in the main media folder. Press Logo (or H) to cover the screen with it while the playlist keeps its place underneath. A playlist can also end on the logo by itself."),
]

def build():
    # ---------- homepage ----------
    KOFI_CARD = '''    <div class="kofi-card">
      <span class="kofi-ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V9z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 3.5c0 1 1 1 1 2M12 3.5c0 1 1 1 1 2"/></svg></span>
      <div><b>LoopCast is free during our launch.</b><span>If it helps your event, a coffee helps keep it growing.</span></div>
      <a class="btn kofi-btn" href="https://ko-fi.com/loopcast" target="_blank" rel="noopener">Buy us a coffee</a>
    </div>
'''
    get_home = GET.replace('  </div>\n</section>', KOFI_CARD + '  </div>\n</section>')
    home = open(os.path.join(ROOT, 'tools', 'home.html')).read().replace('{{GET}}', get_home.strip())
    out = head('LoopCast: free app to loop pictures, videos and PDFs on a projector or TV',
               'LoopCast is a free app that plays your pictures, videos and PDFs on a projector or TV, on repeat. For conferences, churches, trade show booths and lobby TVs. Windows, Mac or browser.',
               '/', ld=[ORG, APP, {"@type": "WebSite", "@id": f"{SITE}/#site", "name": "LoopCast", "url": f"{SITE}/", "publisher": {"@id": f"{SITE}/#org"}}])
    out += header(home=True) + '\n' + home + FOOTER.replace('</footer>\n', '</footer>\n<script src="/assets/testimonials.js" defer></script>\n') + '''
</body>
</html>
'''
    open(os.path.join(ROOT, 'index.html'), 'w').write(out)

    # ---------- features / uses ----------
    page('/features/', 'Features', 'LoopCast features: countdowns, QR codes, phone remote, OBS, logo and black',
         'Everything LoopCast does: loop images, PDFs and video; one-key logo and black; countdowns, a clock and messages; QR codes; picture in picture; a phone remote; and a streaming window for OBS.',
         'Everything it can do.', 'Simple on the surface, with the controls you want when the room is full.',
         open(os.path.join(ROOT, 'tools', 'features.html')).read(), wide=True)
    page('/uses/', 'Uses', 'Where to use LoopCast: conferences, churches, trade shows and lobbies',
         'LoopCast puts looping pictures, videos and PDFs on screens at conferences, churches, trade show booths, meeting rooms, lobbies and schools.',
         'Made for every room.', 'From the ballroom stage to the lobby TV, anywhere a screen should keep showing something useful.',
         open(os.path.join(ROOT, 'tools', 'uses.html')).read(), wide=True)

    # ---------- conferences ----------
    page('/conferences/', 'Conferences',
         'Conference walk-in loop and event screen software | LoopCast',
         'Run walk-in loops, agendas, sponsor slides and break screens on every conference screen. LoopCast is free, works offline, and plays images, PDFs and video.',
         'Walk-in loops and event screens for conferences.',
         'Welcome slides, the day’s agenda, sponsor thank-yous and break timers, looping on the big screen while you run the rest of the event.',
         f'''      <h2>Everything a conference screen needs to show</h2>
      <p>Between sessions, the stage screen is the most-read sign in the building. LoopCast keeps it useful: a <strong>walk-in loop</strong> as doors open, <strong>sponsor slides</strong> at breaks, a <strong>“back in 15 minutes”</strong> screen, and your <strong>event logo</strong> whenever the stage is dark.</p>
      <ul>
        <li><strong>One folder per moment.</strong> Walk-in, Sponsors, Break, Lunch. Each folder is a playlist you can switch to in one click.</li>
        <li><strong>Sponsor decks as PDFs.</strong> Every page becomes a slide, rendered sharply at the projector’s resolution.</li>
        <li><strong>Agenda changes at the last minute.</strong> Drop the new slide into the folder and it shows up the next time around.</li>
        <li><strong>Logo and black on one key</strong> for the moment a speaker takes the stage.</li>
      </ul>
      {fig('photo-hero-wide.webp', 'A conference ballroom with a full audience facing a large stage screen showing a welcome message and the day’s schedule.', 'A walk-in loop with the welcome and the day’s schedule.', 1920, 800)}
      <h2>Built for the AV table</h2>
      <p>Your laptop shows a live preview of what the room sees, outlined red when it’s on screen, with the next item marked. The projector output opens fullscreen on the second display. If the venue has a presenter laptop or camera feed, a USB HDMI capture stick turns it into a live input you can cut to and back.</p>
      <h3>No Wi-Fi required</h3>
      <p>Hotel and convention-center networks are unpredictable. LoopCast plays from files on your computer, so the loop keeps going whether or not the internet does.</p>
      <h2>On the day</h2>
      <ul>
        <li><strong>Break timers and start times:</strong> press T for a full-screen countdown, in minutes or to a time. <a href="/guides/free-countdown-timer-event-screen/">Countdowns, clocks and messages</a>.</li>
        <li><strong>Session feedback and the event app:</strong> a QR code in the corner, over every slide. <a href="/guides/qr-code-on-projector-screen/">QR codes on screen</a>.</li>
        <li><strong>Run it from the floor:</strong> next, logo, messages and timers from your phone. <a href="/guides/phone-remote-for-slideshow/">The phone remote</a>.</li>
        <li><strong>The speaker on the big screen:</strong> a camera in the corner while the slides keep going. <a href="/guides/picture-in-picture-slides-camera/">Picture in picture</a>.</li>
        <li><strong>Hybrid events:</strong> the same walk-in loop and countdowns on the livestream. <a href="/guides/obs-streaming-window/">Slides into OBS</a>.</li>
      </ul>
      <h3>Breakout rooms too</h3>
      <p>Put LoopCast on each room’s laptop with that room’s session details. If a room only has one screen, Fullscreen here fills it, and Esc gets you back to the controls.</p>''',
         image=f"{SITE}/assets/og.jpg")

    # ---------- trade shows ----------
    page('/trade-shows/', 'Trade shows',
         'Trade show booth TV loop software | LoopCast',
         'Keep a product video and slides looping on your trade show booth TV all day, with no internet. Free for Windows and Mac. Plays images, PDFs and MP4 video.',
         'A booth loop that runs all day.',
         'Product videos, demo times and slides on the booth TV, looping from setup to teardown, even when the show-floor Wi-Fi doesn’t.',
         f'''      <h2>Set it up once, then work the booth</h2>
      <p>A booth TV should catch eyes from the aisle without anyone babysitting it. Put your product video, demo schedule and a couple of slides in a folder, and LoopCast loops them fullscreen on the TV for as long as the show runs.</p>
      <ul>
        <li><strong>Video and slides together.</strong> MP4 sizzle reels, PNG or JPG slides, and PDF one-pagers in the same loop.</li>
        <li><strong>No internet needed.</strong> Show-floor Wi-Fi is slow and crowded. LoopCast plays from your laptop.</li>
        <li><strong>Keeps the screen awake</strong> so the laptop doesn’t sleep in the middle of the afternoon.</li>
        <li><strong>One screen is fine.</strong> If the TV is the only display, Fullscreen here fills it, and Esc brings the controls back.</li>
      </ul>
      {fig('use-booth.webp', 'A trade-show booth slide: demos every half hour.', 'A demo-schedule slide in the booth loop.', 960, 540)}
      <h2>Live demos on the big screen</h2>
      <p>Plug a demo laptop or camera into a USB HDMI capture stick and it appears under Inputs. Cut to the live demo, then press play to go back to the loop. Or keep the loop going and put the camera in a corner with <a href="/guides/picture-in-picture-slides-camera/">picture in picture</a>.</p>
      <h2>Collect leads from the aisle</h2>
      <p>Press Q and paste your demo booking or brochure link, and a QR code sits in the corner of every slide. <a href="/guides/qr-code-on-projector-screen/">QR codes on screen</a>.</p>
      <h2>Already using PowerPoint?</h2>
      <p>PowerPoint’s kiosk mode can loop one deck, but changing it means stopping the show in front of visitors. <a href="/guides/powerpoint-kiosk-mode/">PowerPoint kiosk mode vs a looping player</a>.</p>''',
         image=f"{SITE}/assets/use-booth.webp", image_alt="A trade-show booth slide shown by LoopCast.")

    # ---------- digital signage ----------
    page('/digital-signage/', 'Lobbies and schools',
         'Free digital signage for lobby and school TVs | LoopCast',
         'Turn any TV into a looping digital sign for lobbies, offices, schools and waiting rooms. Free, offline, no subscription.',
         'Simple digital signage for lobbies, offices and schools.',
         'Today’s events, welcome messages, menus and announcements on a lobby or hallway TV. Point LoopCast at a folder and it loops, with no subscription and no cloud account.',
         f'''      <h2>Any computer and any TV</h2>
      <p>Digital signage doesn’t need special players or monthly fees. Connect a computer to the TV, open LoopCast, choose a folder, and it loops your images, PDFs and videos fullscreen. If the TV is the only screen, set Settings › Projector to <strong>This screen</strong> and LoopCast fills it every time.</p>
      <ul>
        <li><strong>Schools:</strong> hallway and cafeteria screens with this week’s news, schedules and spirit days.</li>
        <li><strong>Offices and lobbies:</strong> today’s meetings and rooms, visitor welcome messages, wayfinding.</li>
        <li><strong>Waiting rooms and front desks:</strong> services, hours and reminders.</li>
        <li><strong>Restaurants and cafés:</strong> menu boards and specials as images or a PDF.</li>
      </ul>
      {fig('use-lobby.webp', 'A lobby display listing today’s events and rooms.', 'A “today in the building” slide.', 960, 540)}
      <h2>Update it from the folder</h2>
      <p>LoopCast checks the folder every time a playlist comes around, so changing the sign is as simple as replacing a file. Put the folder in a shared drive or a synced cloud folder and anyone on your team can update it.</p>
      {fig('use-school.webp', 'A school hallway slide: Spirit Week, Friday is blue and gold.', 'A hallway announcement for Spirit Week.', 960, 540)}
      <h2>Runs by itself</h2>
      <p>Turn on <strong>Start the show automatically</strong> and <strong>Open LoopCast when this computer starts</strong>, and the screen comes back by itself after a restart or power cut. <strong>Settings › Schedule</strong> switches playlists by time of day: the breakfast menu until 10:30, lunch until 2:00. <a href="/guides/lobby-tv-slideshow-from-laptop/">Set up a lobby TV, step by step</a>.</p>
      <h2>Compared with cloud signage</h2>
      <p>Services like Yodeck and ScreenCloud manage many screens from a web dashboard and charge per screen. For one or a few screens in one place, a free offline player is often enough. <a href="/guides/free-yodeck-screencloud-alternatives/">An honest comparison</a>.</p>''',
         image=f"{SITE}/assets/use-lobby.webp", image_alt="A lobby digital sign shown by LoopCast.")

    # ---------- FAQ ----------
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    body = ('      <div class="faq-layout">\n        <div class="faq-list">\n' + '\n'.join(f'          <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQS) + '\n        </div>\n'
            '''        <aside class="faq-aside">
          <div class="card">
            <h3>Still have a question?</h3>
            <p>Email or call, and a real person will get back to you.</p>
            <a class="btn solid sm" href="mailto:hello@loopcast.space">hello@loopcast.space</a>
            <a class="btn ghost sm" href="tel:+14054860215" style="margin-top:8px">Call 405-486-0215</a>
          </div>
          <div class="card">
            <h3>Helpful pages</h3>
            <nav class="aside-links"><a href="/install/">Install help and the security warning</a><a href="/guides/">Step-by-step guides</a><a href="/features/">Everything LoopCast can do</a></nav>
          </div>
        </aside>
      </div>''')
    page('/faq/', 'FAQ', 'LoopCast FAQ: projectors, files, PDFs, PowerPoint and installs',
         'Answers about LoopCast: projectors and TVs, single-screen use, supported files, PDFs and PowerPoint, live inputs, Mac support and install warnings.',
         'Questions, answered.', 'Everything people usually ask before their first event with LoopCast.', body, extra_ld=[faq_ld], wide=True)

    # ---------- install / security warning ----------
    page('/install/', 'Installing LoopCast', 'Installing LoopCast: the Windows and Mac security warning, explained',
         'Why Windows SmartScreen and macOS warn you when you open LoopCast, what that means, and step-by-step instructions to install it safely.',
         'About the security warning.',
         'Windows and macOS will warn you the first time you open LoopCast. Here’s why, what it does and doesn’t mean, and how to get past it.',
         '''      <div class="callout">
        <p><strong>The short version:</strong> LoopCast isn’t signed with a paid developer certificate yet, so your computer can’t confirm who made it. That’s why you see a warning. It doesn’t mean the app was checked and found to be harmful. If you’d rather not install anything, <a href="/app/" target="_blank" rel="noopener">open LoopCast in your browser</a> instead.</p>
      </div>
      <h2>Why the warning appears</h2>
      <p>Microsoft and Apple let developers “sign” their apps with a certificate that proves who published them. Certificates cost a yearly fee and require identity checks. LoopCast doesn’t have one yet.</p>
      <p>When an app isn’t signed, Windows and macOS can’t confirm the publisher, so they stop and ask you before it runs the first time. That’s a reasonable default: it protects people from apps they didn’t mean to install. After you’ve allowed LoopCast once, it opens normally.</p>
      <h2>What it does and doesn’t mean</h2>
      <ul>
        <li><strong>It means</strong> your computer doesn’t know who published the app.</li>
        <li><strong>It doesn’t mean</strong> Windows or macOS scanned LoopCast and found a problem. Your antivirus and your computer’s built-in malware protection still check it like any other app.</li>
        <li><strong>It doesn’t change</strong> how LoopCast works once it’s open.</li>
      </ul>
      <h2>What LoopCast does on your computer</h2>
      <ul>
        <li>It plays files from the folder you choose. It doesn’t read files anywhere else.</li>
        <li>It works offline. It doesn’t upload your files or send anything about you anywhere.</li>
        <li>It only turns on a camera or capture device when you choose Find inputs. On a Mac, macOS asks your permission first.</li>
        <li>On Windows it installs for your user account only and doesn’t need administrator rights.</li>
      </ul>
      <h2>Stay safe</h2>
      <ul>
        <li><strong>Only download LoopCast from loopcast.space.</strong> The files are named LoopCast-Setup.exe (Windows) and LoopCast-Mac.dmg (Mac).</li>
        <li>If you get LoopCast from anywhere else, like an email attachment or another website, don’t open it.</li>
        <li>If your organization manages your computer, ask your IT team before installing. They can allow it, or you can use the browser version.</li>
      </ul>
      <h2>Installing on Windows</h2>
      <ol>
        <li>Download LoopCast-Setup.exe. If your browser says the file isn’t commonly downloaded, choose <strong>Keep</strong> (in Edge, open the … menu next to the download, choose Keep, then Keep anyway).</li>
        <li>Open the file. If a blue window says <strong>“Windows protected your PC,”</strong> choose <strong>More info</strong>, then <strong>Run anyway</strong>.</li>
        <li>Follow the installer. LoopCast opens when it’s done and appears in your Start menu.</li>
      </ol>
      <p>To uninstall, go to Settings › Apps › Installed apps, find LoopCast and choose Uninstall.</p>
      <h2>Installing on a Mac</h2>
      <ol>
        <li>Download LoopCast-Mac.dmg, open it, and drag LoopCast into your Applications folder.</li>
        <li>Open LoopCast from Applications. macOS will say it can’t verify the app. Choose <strong>Done</strong> (or <strong>OK</strong>).</li>
        <li>Open <strong>System Settings › Privacy &amp; Security</strong>, scroll down to the Security section, and choose <strong>Open Anyway</strong> next to the message about LoopCast. Enter your password if asked.</li>
        <li>Choose <strong>Open</strong> to confirm. From then on, LoopCast opens like any other app.</li>
      </ol>
      <p>On macOS 14 or earlier you can also Control-click LoopCast in Applications, choose Open, then choose Open again.</p>
      <p>To uninstall, drag LoopCast from Applications to the Trash.</p>
      <h2>Prefer not to install?</h2>
      <p>The browser version is the same player and needs no install or security prompts. The desktop app adds a few conveniences, like opening the projector window fullscreen on its own. <a href="/app/" target="_blank" rel="noopener">Open LoopCast in your browser</a>.</p>''')


    # ---------- guides hub ----------
    groups = [('How-to', 'Step by step'), ('Features', 'Using LoopCast’s tools'), ('Compare', 'Comparisons')]
    hub = ''.join(f'      <h2 style="margin:56px 0 18px;font-size:clamp(24px,2.4vw,32px)">{label}</h2>\n      <div class="related" style="margin-top:0">' +
                  ''.join(f'<a href="{p}"><b>{t}</b><span>{d}</span></a>' for p, t, d, g in GUIDES if g == key) + '</div>\n' for key, label in groups)
    hub += '      <h2 style="margin:56px 0 18px;font-size:clamp(24px,2.4vw,32px)">By place</h2>\n      <div class="related" style="margin-top:0">' + ''.join(
        f'<a href="{p}"><b>{TITLES[p]}</b><span>{BLURBS[p]}</span></a>' for p in ['/conferences/', '/churches/', '/trade-shows/', '/digital-signage/', '/propresenter-alternative/']) + '</div>'
    page('/guides/', 'Guides', 'Guides: looping slideshows, countdowns, QR codes and signage | LoopCast',
         'Step-by-step guides for looping slideshows and announcements on a projector or TV, countdowns, QR codes, phone remotes and OBS, plus honest comparisons with PowerPoint, ProPresenter and cloud signage.',
         'Guides.', 'Plain, step-by-step help for getting pictures, videos and PDFs onto a screen and keeping them there.',
         hub, wide=True)

    # ---------- guides, comparisons and the churches page (tools/guides.py) ----------
    guides.build(page, fig)

    # ---------- private links page (not linked, not in the sitemap, not indexed, not counted) ----------
    ADMIN_SLUG = 'hq-1b2312f2f8'
    links = [
      ('Interest', [
        ('Visitor stats', 'GoatCounter: visits, referrers, download clicks', 'https://loopcast.goatcounter.com'),
        ('Email signups', 'Kit: subscribers from the download box', 'https://app.kit.com/subscribers'),
        ('Downloads dashboard', 'GitHub download counts per release (ask Claude to refresh)', 'https://claude.ai/artifact/Y5xetPB7GeUdXHnu9BS2Ze'),
        ('Release downloads (raw)', 'Every release and its files on GitHub', 'https://github.com/MBurleson33/loopcast-site/releases'),
      ]),
      ('Search', [
        ('Google Search Console', 'Indexing and the searches that find you', 'https://search.google.com/search-console'),
        ('Bing Webmaster Tools', 'Bing indexing and searches', 'https://www.bing.com/webmasters'),
        ('Bing notifications', 'The automatic IndexNow runs', 'https://github.com/MBurleson33/loopcast-site/actions/workflows/indexnow.yml'),
      ]),
      ('Build and release', [
        ('Run a release', 'Actions → Release → Run workflow', 'https://github.com/MBurleson33/loopcast/actions'),
        ('App code', 'MBurleson33/loopcast', 'https://github.com/MBurleson33/loopcast'),
        ('Website code', 'MBurleson33/loopcast-site', 'https://github.com/MBurleson33/loopcast-site'),
        ('GitHub Pages settings', 'Domain and HTTPS', 'https://github.com/MBurleson33/loopcast-site/settings/pages'),
      ]),
      ('Listings and domain', [
        ('AlternativeTo', 'Your LoopCast listing', 'https://alternativeto.net/software/loopcast/about/'),
        ('Product Hunt', 'Your products', 'https://www.producthunt.com/my/products'),
        ('Namecheap', 'loopcast.space DNS and email forwarding', 'https://ap.www.namecheap.com/domains/list/'),
      ]),
    ]
    groups = ''.join('<section class="s" style="padding-top:48px"><div class="eyebrow">' + esc(g) + '</div><div class="related" style="margin-top:16px">' +
                     ''.join(f'<a href="{u}" target="_blank" rel="noopener noreferrer"><b>{esc(t)}</b><span>{esc(d)}</span></a>' for t, d, u in items) + '</div></section>' for g, items in links)
    out = head('LoopCast HQ', 'Private links.', '/' + ADMIN_SLUG + '/', noindex=True).replace('</head>', '<meta name="referrer" content="no-referrer">\n</head>')
    out += header() + '<main><div class="wrap"><div class="page-hero" style="padding-top:48px"><h1>LoopCast HQ.</h1><p>Your private shortcuts. This page isn’t linked anywhere or shown to search engines; keep the address to yourself.</p></div>' + groups + '</div></main>'
    out += FOOTER.split(tracking_tags())[0] + '</body>\n</html>\n'
    os.makedirs(os.path.join(ROOT, ADMIN_SLUG), exist_ok=True)
    open(os.path.join(ROOT, ADMIN_SLUG, 'index.html'), 'w').write(out)

    # ---------- 404 ----------
    out = head('Page not found | LoopCast', 'This page doesn’t exist.', '/404.html', noindex=True) + header() + '''<main>
  <div class="wrap hero" style="padding-bottom:clamp(64px,8vw,120px)">
    <span class="pill"><span class="dot"></span>No signal</span>
    <h1>This page isn’t on the loop.</h1>
    <p class="lede">The link may be old or mistyped.</p>
    <div class="ctas"><a class="btn solid" href="/">Go to the homepage</a><a class="btn ghost" href="/faq/">Read the FAQ</a></div>
  </div>
</main>
''' + FOOTER + '</body>\n</html>\n'
    open(os.path.join(ROOT, '404.html'), 'w').write(out)

    # ---------- sitemap, robots, manifest ----------
    urls = ['/'] + [p for p, _ in PAGES_NAV] + [p for p, _, _, _ in GUIDES]
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n# The in-browser app is a tool, not a page to index.\nDisallow: /app/\n\nSitemap: {SITE}/sitemap.xml\n')
    json.dump({"name": "LoopCast", "short_name": "LoopCast", "description": "Looping images, video and PDFs for every event space.",
               "start_url": "/", "display": "standalone", "background_color": "#121316", "theme_color": "#121316",
               "icons": [{"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]},
              open(os.path.join(ROOT, 'site.webmanifest'), 'w'), indent=2)
    print('built', len(urls), 'pages + 404, sitemap.xml, robots.txt, site.webmanifest')

if __name__ == '__main__':
    build()
