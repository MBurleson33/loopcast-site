#!/usr/bin/env python3
"""Builds the LoopCast site: every page, sitemap.xml, robots.txt, 404.html and the web manifest.

Run from the repo root:  python3 tools/build.py
Edit page content in PAGES below (or tools/home.html for the homepage body), then rebuild and commit.
app/index.html is not built here; the LoopCast release workflow updates it.
"""
import json, os, datetime, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://loopcast.space'
TODAY = datetime.date.today().isoformat()
REL = 'https://github.com/MBurleson33/loopcast-site/releases/latest/download/'
DL_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>'

ORG = {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Treetop Business Solutions", "email": "hello@loopcast.space",
       "address": {"@type": "PostalAddress", "addressLocality": "Oklahoma City", "addressRegion": "OK", "addressCountry": "US"}}
APP = {"@type": "SoftwareApplication", "@id": f"{SITE}/#app", "name": "LoopCast",
       "url": f"{SITE}/", "image": f"{SITE}/assets/icon-512.png", "screenshot": f"{SITE}/assets/operator.webp",
       "applicationCategory": "MultimediaApplication", "applicationSubCategory": "Digital signage and presentation software",
       "operatingSystem": "Windows 10, Windows 11, macOS 12 or later, web browser",
       "description": "Offline looping media player for event screens. Plays a folder of images, PDFs and videos on a projector or TV, on repeat, without internet.",
       "featureList": ["Loops images, PDFs and video", "Folder-based playlists", "Projector output with live preview",
                       "Logo screen and fade to black", "Loop, repeat or stop per playlist", "Live HDMI capture inputs",
                       "Fullscreen on a single screen", "Works offline"],
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
       "publisher": {"@id": f"{SITE}/#org"}, "downloadUrl": f"{SITE}/#download"}

PAGES_NAV = [  # footer links: (path, label)
    ('/conferences/', 'Conferences'), ('/churches/', 'Churches'), ('/trade-shows/', 'Trade shows'),
    ('/digital-signage/', 'Lobbies and schools'), ('/guides/loop-powerpoint-pdf-on-projector/', 'Loop a PowerPoint or PDF'),
    ('/propresenter-alternative/', 'ProPresenter alternative'), ('/install/', 'Install help'), ('/faq/', 'FAQ'),
]

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, image=f"{SITE}/assets/og.jpg", image_alt="A conference ballroom with a full audience facing a large stage screen.", ld=None, noindex=False):
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
    links = ('<a href="#how">How it works</a><a href="#rooms">Rooms</a>' if home else '<a href="/#how">How it works</a><a href="/install/">Install help</a>') + '<a href="/faq/">FAQ</a>'
    return f'''<header class="wrap">
  <nav class="top" aria-label="Main">
    <a class="brand" href="/" aria-label="LoopCast home"><img src="/assets/mark.svg" width="32" height="27" alt=""><span>LoopCast</span></a>
    <div class="nav-r"><div class="nav-links">{links}</div><a class="btn solid sm" href="/app/" target="_blank" rel="noopener">Open in your browser</a></div>
  </nav>
</header>
'''

FOOTER = '''<footer>
  <div class="wrap"><div>
    <nav class="foot-links" aria-label="More about LoopCast">''' + ''.join(f'<a href="{p}">{l}</a>' for p, l in PAGES_NAV) + '''</nav>
    <div class="foot-row">
      <span class="b"><img src="/assets/mark.svg" width="24" height="20" alt=""><span><b>LoopCast</b>, for every space with a screen.</span></span>
      <span>Questions? <a href="mailto:hello@loopcast.space">hello@loopcast.space</a></span>
      <span>Made by Treetop Business Solutions in Oklahoma City. © 2026</span>
    </div>
  </div></div>
</footer>
'''

GET = f'''<section id="download" class="s wrap">
  <div class="get">
    <h2>Ready when the doors open.</h2>
    <div class="grid3">
      <a class="dl" href="{REL}LoopCast-Setup.exe"><b>Download for Windows</b><span>Windows 10 or 11</span></a>
      <a class="dl" href="{REL}LoopCast-Mac.dmg"><b>Download for Mac</b><span>macOS 12 or later, Apple silicon or Intel</span></a>
      <a class="dl alt" href="/app/" target="_blank" rel="noopener"><b>Open in your browser</b><span>Nothing to install</span></a>
    </div>
    <p><b>Expect a security warning the first time.</b> LoopCast isn’t signed with a paid developer certificate yet, so Windows and macOS can’t confirm who made it. On Windows choose More info, then Run anyway. On a Mac, go to System Settings › Privacy &amp; Security and choose Open Anyway. <a href="/install/">Here’s what that means</a>.</p>
    <p>Plays images, video and PDFs. Using PowerPoint or Keynote? Save your deck as a PDF first.</p>
  </div>
</section>
'''

def crumbs_ld(path, name):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "LoopCast", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

def related(current):
    picks = [(p, l) for p, l in PAGES_NAV if p != current][:3]
    blurbs = {'/conferences/': 'Walk-in loops, agendas and sponsors', '/churches/': 'Pre-service announcement loops',
              '/trade-shows/': 'All-day loops on the booth TV', '/digital-signage/': 'Lobby, hallway and office screens',
              '/guides/loop-powerpoint-pdf-on-projector/': 'Three ways, step by step', '/propresenter-alternative/': 'When you only need loops',
              '/install/': 'Why Windows and Mac warn you, and what to do', '/faq/': 'Projectors, files, installs'}
    return '<div class="related">' + ''.join(f'<a href="{p}"><b>{l}</b><span>{blurbs[p]}</span></a>' for p, l in picks) + '</div>'

def page(path, crumb, title, desc, h1, lede, body, image=None, image_alt=None, extra_ld=None):
    ld = [ORG, APP, crumbs_ld(path, crumb)] + (extra_ld or [])
    kw = {}
    if image: kw['image'] = image
    if image_alt: kw['image_alt'] = image_alt
    out = head(title, desc, path, ld=ld, **kw)
    out += header()
    out += f'''<main>
  <div class="wrap">
    <p class="crumbs"><a href="/">LoopCast</a> › {esc(crumb)}</p>
    <div class="page-hero">
      <h1>{h1}</h1>
      <p>{lede}</p>
      <div class="ctas"><a class="btn solid" href="#download">{DL_ICON}Download free</a><a class="btn ghost" href="/app/" target="_blank" rel="noopener">Open in your browser</a></div>
    </div>
    <div class="prose">
{body}
    </div>
    <div class="more"><div class="eyebrow">Keep reading</div>
    {related(path)}</div>
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
    ("Is LoopCast free?", "Yes. You can download LoopCast for Windows and Mac, or open it in your browser, at no cost."),
    ("Does it need internet?", "No. LoopCast runs on your computer and plays files from a folder on it. You only need internet to download it."),
    ("Will it work with our projector or TV?", "Yes, if your computer sees it as a second display: a projector, a TV, or an LED wall processor over HDMI, DisplayPort or USB-C. LoopCast opens the output fullscreen on it at its own resolution."),
    ("What if I only have one screen?", "Use Fullscreen here (the expand button, or the F key). LoopCast fills the screen it runs on, and Esc brings back the controls. If LoopCast only finds one display, Show on projector does this for you."),
    ("What kinds of files can I use?", "Images (JPG, PNG, GIF, WebP, SVG), PDFs, and video (MP4, WebM, MOV). Each page of a PDF becomes its own slide. MP4 with H.264 is the safest choice for video."),
    ("Can it play PowerPoint or Keynote files?", "Not directly. Save your deck as a PDF (in PowerPoint, File › Export › PDF; in Keynote, File › Export To › PDF) and put the PDF in the folder. If LoopCast finds a PowerPoint or Keynote file, it tells you how to export it."),
    ("Can I click through slides myself?", "Yes. Set a playlist’s Advance option to Manual and each slide stays up until you press next: the arrow keys, Page Up and Page Down, or a presentation clicker. Click any slide to jump straight to it. Videos play once and hold on their last frame."),
    ("Can I add or swap files during an event?", "Yes. Add or remove files in the folder and LoopCast picks up the changes the next time the playlist comes around, or right away if you press Rescan."),
    ("Can I show a presenter’s laptop or a camera?", "Yes. Plug it into a USB HDMI capture stick and it shows up under Inputs. Preview it, then put it on screen with one click. The playlist waits underneath, and Logo and Black still work."),
    ("Does it work on a Mac?", "Yes, on macOS 12 or later, on Apple silicon and Intel Macs. The first time you open it, go to System Settings › Privacy & Security and choose Open Anyway."),
    ("Can I use it without installing anything?", "Yes. Open in your browser runs the full player in any modern browser. The desktop app adds a few conveniences, like opening the projector window fullscreen on its own."),
    ("Why does my computer warn me when I install it?", "LoopCast isn’t signed with a paid developer certificate yet. Without one, Windows and macOS can’t confirm who made the app, so they ask you to confirm the first time. The warning is about an unverified publisher; it doesn’t mean the app was found to be harmful. Download it only from loopcast.space. The Installing LoopCast page explains each step. On Windows choose More info, then Run anyway. On a Mac, go to System Settings › Privacy & Security and choose Open Anyway."),
    ("How do I get help or send feedback?", "Email hello@loopcast.space. Include your version number (click the LoopCast logo in the app to see it) and whether you use Windows, Mac or the browser version."),
    ("How do I show a logo between sessions?", "Put an image named logo.png in the main media folder. Press Logo (or H) to cover the screen with it while the playlist keeps its place underneath. A playlist can also end on the logo by itself."),
]

def build():
    # ---------- homepage ----------
    home = open(os.path.join(ROOT, 'tools', 'home.html')).read().replace('{{GET}}', GET.strip())
    out = head('LoopCast: looping images, video and PDFs for every event space',
               'Free looping software for event screens. Play images, PDFs and video on a projector or TV, on repeat, offline. For conferences, churches, booths and lobbies.',
               '/', ld=[ORG, APP, {"@type": "WebSite", "@id": f"{SITE}/#site", "name": "LoopCast", "url": f"{SITE}/", "publisher": {"@id": f"{SITE}/#org"}}])
    out += header(home=True) + '\n' + home + FOOTER + '''
</body>
</html>
'''
    open(os.path.join(ROOT, 'index.html'), 'w').write(out)

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
      <h3>Breakout rooms too</h3>
      <p>Put LoopCast on each room’s laptop with that room’s session details. If a room only has one screen, Fullscreen here fills it, and Esc gets you back to the controls.</p>''',
         image=f"{SITE}/assets/og.jpg")

    # ---------- churches ----------
    page('/churches/', 'Churches',
         'Church announcement loop software | LoopCast',
         'Loop church announcements, welcome slides and countdown videos before the service. Free, offline, and simple enough for any volunteer.',
         'Pre-service announcement loops for churches.',
         'Welcome slides, announcements and countdown videos on the sanctuary and lobby screens, looping until the service starts. Simple enough for any volunteer.',
         f'''      <h2>The announcement loop, without tying up the presentation computer</h2>
      <p>Most churches loop announcements before the service and between services. LoopCast does that one job well: point it at a folder of announcement slides and it plays them on repeat, fullscreen on the sanctuary projector or the lobby TV.</p>
      <ul>
        <li><strong>Volunteer-friendly.</strong> Choose the folder, click Show on projector, press play. Nothing to configure.</li>
        <li><strong>Announcements as a PDF.</strong> Export this week’s slides from Canva, PowerPoint or Keynote as a PDF and drop it in. Each page becomes a slide.</li>
        <li><strong>Countdown video at the end.</strong> Set the pre-service playlist to stop on its last item, or end on your church logo.</li>
        <li><strong>Lobby and kids’ check-in screens.</strong> Run a separate copy on each screen’s computer, each with its own folder.</li>
      </ul>
      {fig('use-church.webp', 'A church welcome slide: coffee in the lobby, service starts at 10:30.', 'A pre-service welcome slide.', 960, 540)}
      <h2>Update it in seconds</h2>
      <p>Replace last week’s files with this week’s and LoopCast picks them up the next time the loop comes around. Want a version for the second service without one announcement? Duplicate the playlist and hide that slide. The original stays as it was.</p>
      <h3>Works alongside your worship software</h3>
      <p>LoopCast doesn’t replace lyric and sermon software. It’s for the loops around the service, on the same projector before worship starts or on a different screen entirely.</p>''',
         image=f"{SITE}/assets/use-church.webp", image_alt="A church welcome slide shown by LoopCast.")

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
      <p>Plug a demo laptop or camera into a USB HDMI capture stick and it appears under Inputs. Cut to the live demo, then press play to go back to the loop.</p>''',
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
      {fig('use-school.webp', 'A school hallway slide: Spirit Week, Friday is blue and gold.', 'A hallway announcement for Spirit Week.', 960, 540)}''',
         image=f"{SITE}/assets/use-lobby.webp", image_alt="A lobby digital sign shown by LoopCast.")

    # ---------- guide ----------
    page('/guides/loop-powerpoint-pdf-on-projector/', 'Loop a PowerPoint or PDF',
         'How to loop a PowerPoint or PDF on a projector | LoopCast',
         'Three ways to make a PowerPoint, Keynote, Google Slides or PDF slideshow loop continuously on a projector or TV, with step-by-step instructions.',
         'How to loop a PowerPoint or PDF on a projector.',
         'Three ways to keep a slideshow repeating on a projector or TV, from the setting already in your presentation app to a dedicated looping player.',
         f'''      <h2>1. In PowerPoint</h2>
      <ol>
        <li>On the <strong>Transitions</strong> tab, check <strong>After</strong> and set how many seconds each slide stays up. Click <strong>Apply To All</strong>.</li>
        <li>On the <strong>Slide Show</strong> tab, choose <strong>Set Up Slide Show</strong> and check <strong>Loop continuously until ‘Esc’</strong>.</li>
        <li>Start the slide show. It repeats until you press Esc.</li>
      </ol>
      <h2>2. In Keynote or Google Slides</h2>
      <p><strong>Keynote:</strong> in the Document inspector, set the presentation type to <strong>Self-Playing</strong>, choose a delay, and check <strong>Loop slideshow</strong>.</p>
      <p><strong>Google Slides:</strong> start the presentation, open the options menu in the presenter toolbar, choose <strong>Auto-play</strong>, pick a speed and check <strong>Loop</strong>.</p>
      <p>These work for a single deck. They get awkward when you need video in the loop, more than one loop for different parts of the day, a logo screen, or a preview of what the room sees.</p>
      <h2>3. With LoopCast</h2>
      <p>LoopCast is a free player built for this job. It loops images, PDFs and video, and gives you separate playlists, a live preview and one-key logo and black screens.</p>
      <ol>
        <li><strong>Export your deck as a PDF.</strong> PowerPoint: File › Export › PDF. Keynote: File › Export To › PDF. Google Slides: File › Download › PDF.</li>
        <li><strong>Put the PDF in a folder</strong>, along with any videos or images you want in the same loop. Each page of the PDF becomes a slide.</li>
        <li><strong>Open LoopCast and choose the folder.</strong> Click <strong>Show on projector</strong>, then play. Use <strong>Fullscreen here</strong> if there’s only one screen.</li>
      </ol>
      {fig('operator.webp', 'LoopCast’s control window with a live preview of the slide on the projector and a filmstrip of the playlist.', 'LoopCast’s controls, with a live preview of what the room sees.', 2880, 1720)}
      <h3>Tips for a slideshow that reads well from the back of the room</h3>
      <ul>
        <li>Use a 16:9 slide size to match most projectors and TVs.</li>
        <li>Keep text large and short. Eight to ten seconds per slide is a good starting point.</li>
        <li>For video, export MP4 (H.264). It plays everywhere.</li>
      </ul>''',
         image=f"{SITE}/assets/operator.webp", image_alt="LoopCast’s control window.")

    # ---------- alternative ----------
    page('/propresenter-alternative/', 'ProPresenter alternative',
         'Simple ProPresenter alternative for looping slides | LoopCast',
         'Only need to loop announcements, slides and video? LoopCast is a free, simple alternative to full presentation suites for looping on a projector.',
         'A simple alternative for when you only need loops.',
         'Full presentation suites do a lot. If what you need is announcements, slides and video looping on a screen, LoopCast does that one thing simply, for free.',
         '''      <h2>Different tools for different jobs</h2>
      <p>ProPresenter is professional presentation software for worship and live production, with lyrics, stage displays, multiple screens and much more. If you run services or productions with all of that, it’s built for you.</p>
      <p>Plenty of screens only need a loop: a conference walk-in, a lobby TV, a booth display, a pre-service announcement loop on a second computer. For those, LoopCast is lighter and quicker to learn.</p>
      <h2>What LoopCast does</h2>
      <ul>
        <li>Loops images, PDFs and video from folders, one folder per playlist.</li>
        <li>Shows a live preview of the projector, with the current and next item marked.</li>
        <li>Logo screen and fade to black on one key.</li>
        <li>Per-playlist endings (loop, stop or end on the logo), per-item repeat, and a manual mode to click through slides with the keyboard or a clicker.</li>
        <li>Live inputs from a USB HDMI capture stick.</li>
        <li>Runs offline on Windows and Mac, or in any modern browser.</li>
      </ul>
      <h2>What it doesn’t do</h2>
      <p>LoopCast isn’t a lyric or sermon presenter. It has no song library, stage display, timeline cues or video switching between multiple outputs. If you need those, a full presentation suite is the right tool, and LoopCast can still run the loops on a separate screen.</p>
      <p class="crumbs" style="margin-top:32px">ProPresenter is a trademark of Renewed Vision. LoopCast is not affiliated with or endorsed by Renewed Vision.</p>''')

    # ---------- FAQ ----------
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    body = '      <div class="faq-list">\n' + '\n'.join(f'        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQS) + '\n      </div>'
    page('/faq/', 'FAQ', 'LoopCast FAQ: projectors, files, PDFs, PowerPoint and installs',
         'Answers about LoopCast: projectors and TVs, single-screen use, supported files, PDFs and PowerPoint, live inputs, Mac support and install warnings.',
         'Questions, answered.', 'Everything people usually ask before their first event with LoopCast.', body, extra_ld=[faq_ld])

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
    urls = ['/'] + [p for p, _ in PAGES_NAV]
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
