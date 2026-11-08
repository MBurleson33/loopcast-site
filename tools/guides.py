"""Guides, comparisons and the longer landing pages for the LoopCast site.

build.py calls build(page, fig) after the rest of the site. Each page here is plain HTML in a Python string.
Facts about other products (prices, plans) carry a "Checked" month and a source link: re-check them before
changing the month.
"""
import html, json

CHECKED = 'November 2026'


def esc(s): return html.escape(s, quote=True)


def faq(items):
    """Visible questions plus the matching FAQPage data. Returns (html, ld)."""
    body = ('      <h2>Questions</h2>\n      <div class="faq-list">\n' +
            '\n'.join(f'        <details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in items) +
            '\n      </div>')
    strip = lambda s: html.unescape(__import__('re').sub(r'<[^>]+>', '', s))
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}
    return body, ld


def article_ld(path, headline, desc, image):
    return {"@type": "Article", "headline": headline, "description": desc, "image": f"https://loopcast.space/assets/{image}",
            "dateModified": __import__('datetime').date.today().isoformat(), "mainEntityOfPage": f"https://loopcast.space{path}",
            "author": {"@id": "https://loopcast.space/#org"}, "publisher": {"@id": "https://loopcast.space/#org"}}


def table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'      <div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


DL = '<a href="/#download">Download LoopCast</a> (free) for Windows or Mac'
PRO = 'It’s a Pro feature, free for everyone while LoopCast is in its launch.'


def build(page, fig):
    def guide(path, crumb, title, desc, h1, lede, body, faqs, image, rel):
        fq, ld = faq(faqs)
        page(path, crumb, title, desc, h1, lede, body + '\n' + fq,
             extra_ld=[ld, article_ld(path, h1.rstrip('.'), desc, image)], rel=rel)

    # =====================================================================
    # New feature guides
    # =====================================================================

    guide('/guides/obs-streaming-window/', 'Slides in OBS',
          'How to add looping slides to OBS, vMix or Ecamm (free) | LoopCast',
          'Send a looping slideshow, countdown, clock and messages into OBS, vMix or Ecamm with LoopCast’s streaming window. Step by step, with settings that look sharp.',
          'How to put looping slides into OBS, vMix or Ecamm.',
          'Your livestream needs the same walk-in loop, countdown and announcements the room sees. LoopCast’s streaming window gives your streaming software a clean, fixed-size picture of the show to capture.',
          f'''      <p>Most people run their pre-service or pre-event loop on the projector and then try to get the same slides onto the stream by screen-sharing a laptop, pointing a camera at the screen, or rebuilding the loop as a video file. All three are fiddly. A <strong>streaming window</strong> is simpler: LoopCast opens the show in its own window at exactly 1920×1080 or 1280×720, and your streaming software captures that window like any other source.</p>
      <h2>What you need</h2>
      <ul>
        <li>The LoopCast desktop app for Windows or Mac. {DL}. The browser version can’t open a streaming window.</li>
        <li>Streaming software that can capture a window: OBS Studio (free), vMix, Ecamm Live, Streamlabs and most others can.</li>
        <li>Your slides, videos and PDFs in a folder, one folder per playlist.</li>
      </ul>
      <h2>1. Choose the streaming window</h2>
      <ol>
        <li>Open LoopCast and choose your folder.</li>
        <li>Open <strong>Settings</strong> (the sliders icon, top right) and find <strong>Projector</strong>.</li>
        <li>In the menu, under <strong>For streaming</strong>, pick <strong>Streaming window, 1920×1080</strong> or <strong>Streaming window, 1280×720</strong>. Match your stream’s output resolution; 1080 is right for most.</li>
        <li>Close Settings and press <strong>Open streaming window</strong> where Show on projector used to be.</li>
      </ol>
      {fig('shot-stream-settings.webp', 'LoopCast Settings with Projector set to Streaming window, 1920×1080, and a note explaining how to add it to OBS as a Window Capture source.', 'Settings › Projector, with the streaming window chosen.', 720, 660).replace('class="figure"', 'class="figure mid"')}
      <h2>2. Add it to OBS</h2>
      <ol>
        <li>In OBS, under <strong>Sources</strong>, press <strong>+</strong> and choose <strong>Window Capture</strong> (on a Mac, <strong>macOS Screen Capture</strong> with the method set to Window Capture also works).</li>
        <li>Pick the window named <strong>LoopCast Stream</strong>.</li>
        <li>If the source doesn’t fill the canvas, right-click it and choose <strong>Transform › Fit to screen</strong>. Because the window is exactly the size you picked, there’s nothing to crop.</li>
      </ol>
      <p><strong>vMix:</strong> Add Input › Desktop Capture, then pick the LoopCast Stream window. <strong>Ecamm Live:</strong> add a Window Capture source and choose LoopCast Stream. Other apps work the same way: look for window capture, not display capture.</p>
      {fig('shot-stream-window.webp', 'The LoopCast streaming window showing a welcome slide at 1920 by 1080, ready to capture.', 'The streaming window: just the show, nothing else.', 1600, 900)}
      <h2>3. Run the show as usual</h2>
      <p>Everything you do in LoopCast’s controls shows up in the stream: switching playlists, Logo and Black, the countdown, the message bar, the clock, the QR code and picture in picture. Live web pages play in the stream too. You keep the control window on your screen and the stream sees only the show.</p>
      <ul>
        <li><strong>Walk-in:</strong> loop welcome slides and announcements before the stream goes live.</li>
        <li><strong>Countdown:</strong> press T and type a time, like 10:00 AM, so online viewers see “Starting in…” counting down. <a href="/guides/free-countdown-timer-event-screen/">More about countdowns</a>.</li>
        <li><strong>Lower-third style notes:</strong> press M for a one-line message along the bottom or top of the picture.</li>
        <li><strong>Giving or sign-up link:</strong> press Q to put a QR code in a corner. <a href="/guides/qr-code-on-projector-screen/">More about QR codes</a>.</li>
      </ul>
      <h2>Tips for a clean capture</h2>
      <ul>
        <li><strong>Don’t minimize the window.</strong> It keeps playing behind other windows, so you can cover it, but most systems stop drawing a minimized window and the capture freezes.</li>
        <li><strong>Pick the size before you go live.</strong> If you switch between 1920×1080 and 1280×720, re-check the source’s transform in your streaming software.</li>
        <li><strong>Use window capture, not display capture.</strong> Display capture grabs the whole screen, menus and all.</li>
        <li><strong>Audio:</strong> video sound plays through the computer as normal. Capture it in your streaming software as desktop or application audio, the same as any other app.</li>
        <li><strong>One output at a time.</strong> The streaming window is one of the choices in the Projector menu, so LoopCast sends the show either to a display or to the streaming window. If the room and the stream need the same picture, feed the projector from your switcher or streaming software’s output.</li>
      </ul>
      <p>The streaming window is a Pro feature in the desktop app. {PRO}</p>''',
          [
              ("Can I use LoopCast with OBS?", "Yes. In Settings › Projector, choose Streaming window (1920×1080 or 1280×720), press Open streaming window, and add it to OBS as a Window Capture source named LoopCast Stream."),
              ("Does the browser version have a streaming window?", "No. The streaming window is in the LoopCast desktop app for Windows and Mac. In a browser you could capture the browser tab, but the size and edges are harder to control."),
              ("Will countdowns, messages and the clock show in the stream?", "Yes. Everything that shows on the projector shows in the streaming window: Logo, Black, the countdown, the message bar, the clock, QR codes, picture in picture and live web pages."),
              ("Why did my OBS source freeze?", "The LoopCast Stream window was probably minimized. Restore it; it can sit behind other windows and keep playing, but minimized windows usually stop drawing."),
              ("Which size should I pick?", "Match your stream’s output resolution. Most streams are 1920×1080; pick 1280×720 if you stream at 720p and want to save processing power."),
              ("Does it cost anything?", "The streaming window is a Pro feature. It’s free for everyone while LoopCast is in its launch."),
          ], 'shot-stream-window.webp',
          ['/guides/free-countdown-timer-event-screen/', '/guides/picture-in-picture-slides-camera/', '/guides/phone-remote-for-slideshow/'])

    guide('/guides/qr-code-on-projector-screen/', 'QR code on screen',
          'How to show a QR code on a projector or TV screen | LoopCast',
          'Put a scannable QR code for giving, registration or a survey in the corner of your projector or TV, over your slides, without editing a single slide.',
          'How to show a QR code on a projector or TV.',
          'A QR code on the big screen is the fastest way to get a room to a giving page, a sign-up form or a survey. LoopCast puts one in a corner, over whatever is playing, and takes it away with one key.',
          f'''      <p>The usual way to show a QR code is to make a slide for it. That works until the link changes, or you want the code up during the announcements and the walk-in loop, or you need it on for five minutes and then gone. LoopCast treats the QR code as an overlay instead: it sits in a corner on top of every slide, video and web page until you hide it.</p>
      <h2>Show a QR code in three steps</h2>
      <ol>
        <li><strong>Start your loop.</strong> {DL}, or <a href="/app/" target="_blank" rel="noopener">open it in your browser</a>. Choose your folder and press Show on projector.</li>
        <li><strong>Press QR</strong> (or the Q key). Paste the link people should open, like <code>https://example.org/give</code>, and add a few words to go under it, like “Scan to give” or “Scan to register”.</li>
        <li><strong>Press Show QR code.</strong> It appears in the corner of the projector and the preview. Press QR or Q again to hide it.</li>
      </ol>
      {fig('shot-qr.webp', 'A conference welcome slide with a white QR code card in the bottom-right corner reading Scan to register.', 'A QR code card in the corner, over the welcome slide.', 1568, 882)}
      <p>LoopCast remembers the last link and caption, so next time you press QR they’re already filled in.</p>
      <h2>Pick the corner and size</h2>
      <p>In <strong>Settings › QR code</strong>, choose any of the four corners and Small, Medium or Large. Large is easiest to scan from the back of a big room; Small is enough for a lobby TV people walk right past. If the clock is in the same corner, the code sits neatly inside it. If picture in picture is in the same corner, LoopCast tells you so you can move one of them.</p>
      {fig('shot-qr-app.webp', 'LoopCast’s control window with the QR code showing in the live preview and the QR button lit.', 'The QR button sits with Timer, Message and Clock under the preview.', 1600, 956)}
      <h2>Ideas for what to link</h2>
      <ul>
        <li><strong>Churches:</strong> online giving, a connection card, next week’s sign-ups, the sermon notes.</li>
        <li><strong>Conferences:</strong> the event app, session feedback, the sponsor raffle, slides for the talk that just ended.</li>
        <li><strong>Trade show booths:</strong> book a demo, download the brochure, join the mailing list.</li>
        <li><strong>Lobbies and schools:</strong> the Wi-Fi details page, a volunteer form, the lunch menu.</li>
      </ul>
      <h2>Make it easy to scan</h2>
      <ul>
        <li><strong>Size for the room.</strong> As a rough guide, people can scan a code from about ten times its width. On a big projector, Medium or Large reaches most rows.</li>
        <li><strong>Shorter links make simpler codes.</strong> A long link with tracking tags makes a denser pattern that’s harder to scan from far away. Use a short page address where you can.</li>
        <li><strong>Tell people what they’ll get.</strong> “Scan to give” or “Scan for the schedule” works better than “Scan me”.</li>
        <li><strong>Leave it up long enough.</strong> Thirty seconds is short for a room of people finding their phones. Put it on during the announcement and leave it through the next few slides.</li>
        <li><strong>Test it from the back row</strong> before the doors open.</li>
      </ul>
      <h2>Over web pages and in the stream</h2>
      <p>In the desktop app, the QR code also shows over live web pages in your playlist, and in the <a href="/guides/obs-streaming-window/">streaming window</a> for OBS, so online viewers can scan it from their screens too. You can turn it on and off from your phone with the <a href="/guides/phone-remote-for-slideshow/">phone remote</a>.</p>''',
          [
              ("Do I need to put the QR code on a slide?", "No. LoopCast draws the QR code itself, in a corner over whatever is playing, so you don’t need to edit any slides. Press QR (or Q), paste the link, and it appears."),
              ("Can I change where the QR code shows?", "Yes. In Settings › QR code, pick any corner and Small, Medium or Large."),
              ("Does it work in the browser version?", "Yes. The QR code works in the browser version and the desktop app. Showing it over live web pages is in the desktop app, since web pages are."),
              ("Does LoopCast track who scans the code?", "No. LoopCast just turns your link into a code. If you want scan counts, use a link from a service that counts visits, or add tracking tags to your own page."),
              ("What happens if I have no internet?", "Making the code doesn’t need internet; LoopCast draws it on your computer. People who scan it need internet on their phones to open the link."),
          ], 'shot-qr.webp',
          ['/guides/free-countdown-timer-event-screen/', '/guides/church-announcement-loop/', '/guides/phone-remote-for-slideshow/'])

    guide('/guides/free-countdown-timer-event-screen/', 'Countdown timer',
          'Free countdown timer for church and event screens | LoopCast',
          'Show a full-screen countdown on a projector or TV: “We’ll be back in 10:00” or “Starting in” to a set time, plus an on-screen clock and message bar. Free for Windows, Mac and browser.',
          'A free countdown timer for church and event screens.',
          'A big countdown tells a room exactly when things start. LoopCast shows one full screen in two keystrokes, counts to a number of minutes or to a time of day, and goes back to your slides when it reaches zero.',
          f'''      <p>Countdown videos are popular, but they’re a fixed length: if the service starts at 10:30 you have to press play at exactly 10:25. A countdown <em>to a time</em> doesn’t care when you start it. LoopCast does both kinds, and it doesn’t interrupt your playlist: the slides keep their place underneath and come back when the countdown ends.</p>
      <h2>Start a countdown</h2>
      <ol>
        <li>Open LoopCast and start your loop. {DL}, or <a href="/app/" target="_blank" rel="noopener">open it in your browser</a>; the countdown works in both.</li>
        <li>Press <strong>Timer</strong> (or T).</li>
        <li>Type <strong>minutes</strong>, like <code>10</code>, or a <strong>time of day</strong>, like <code>9:30 AM</code> or <code>14:00</code>.</li>
        <li>Change the words above the timer if you like, then press <strong>Start countdown</strong>.</li>
      </ol>
      {fig('shot-countdown-dialog.webp', 'LoopCast’s Show a countdown box, with 10 minutes typed in and the words We’ll be back in above the timer.', 'Type minutes or a time, and the words to show above the timer.', 1600, 956)}
      <p>The countdown covers the screen. At zero it shows “Starting now” for a moment and then the slides come back. Press T again to stop it early.</p>
      {fig('shot-countdown.webp', 'A full-screen countdown reading We’ll be back in 9:57.', 'What the room sees.', 1568, 882)}
      <h2>Minutes or a time of day?</h2>
      <ul>
        <li><strong>Minutes</strong> for breaks: “We’ll be back in 15:00”.</li>
        <li><strong>A time</strong> for start times: type <code>10:30</code> and LoopCast counts down to the next 10:30, so you can start it whenever you’re ready. If you leave the words as “We’ll be back in”, LoopCast changes them to “Starting in”, which reads better for a start time.</li>
      </ul>
      <p>LoopCast remembers what you typed last, so a weekly service countdown is the same two keystrokes every Sunday.</p>
      <h2>A clock in the corner</h2>
      <p>Sometimes you don’t need a countdown, just the time. Press <strong>Clock</strong> (or C) to put the current time in a corner over everything that plays. In <strong>Settings › Clock</strong>, pick the corner, size, font (Clean, Bold, Classic or Digital), color, background, 24-hour time and seconds. It’s handy for speakers keeping to time, breakout rooms and lobby screens.</p>
      <h2>A message bar for quick notes</h2>
      <p>Press <strong>Message</strong> (or M) and type a line, like “Session 2 starts at 10:30 in Ballroom B”. It slides in along the bottom of the screen over whatever is playing, and pressing M again clears it. In <strong>Settings › Message bar</strong> you can put it at the top instead and change its size, font, text color and background.</p>
      {fig('shot-clock-message.webp', 'An agenda slide with the time, 1:52 PM, in the top-right corner and a message bar along the bottom reading Session 2 starts at 10:30 in Ballroom B.', 'The clock and the message bar, over an agenda slide.', 1568, 882)}
      <h2>Where it helps</h2>
      <ul>
        <li><strong>Churches:</strong> a countdown to the service start on the sanctuary screen and the stream, after the announcement loop.</li>
        <li><strong>Conferences:</strong> break timers, “Doors open at 8:30”, and a clock for speakers in breakout rooms.</li>
        <li><strong>Schools:</strong> a countdown to the assembly, or a clock on the cafeteria screen.</li>
        <li><strong>Workshops:</strong> timed exercises: press T, type 5, and everyone can see the time left.</li>
      </ul>
      <h2>Run it from your phone</h2>
      <p>With the <a href="/guides/phone-remote-for-slideshow/">phone remote</a>, you can start a countdown, show a message or turn the clock on from your phone while you’re away from the computer. Countdowns, the clock and messages also appear in the <a href="/guides/obs-streaming-window/">streaming window</a> for your livestream.</p>''',
          [
              ("Is the countdown timer free?", "Yes. The countdown, clock and message bar are part of LoopCast, which is free during our launch, on Windows, Mac and in the browser."),
              ("Can it count down to a specific time?", "Yes. Type a time like 9:30 AM or 14:00 instead of minutes, and LoopCast counts down to the next time it’s that time."),
              ("What happens at zero?", "It shows “Starting now” for a moment, then your slides come back. The playlist keeps its place underneath the whole time."),
              ("Can I change the words above the timer?", "Yes. LoopCast asks for them each time you start a countdown, and remembers what you used last."),
              ("Can I show the time instead of a countdown?", "Yes. Press Clock (or C) to show the time in a corner. Settings › Clock has the corner, size, font, color, background, 24-hour time and seconds."),
              ("Does it work with a countdown video?", "Yes. Put the video in a playlist like any other file. Set that playlist to stop on its last item so it doesn’t loop back to the start."),
          ], 'shot-countdown.webp',
          ['/guides/church-announcement-loop/', '/guides/obs-streaming-window/', '/guides/qr-code-on-projector-screen/'])

    guide('/guides/phone-remote-for-slideshow/', 'Phone remote',
          'Control a slideshow from your phone over Wi-Fi | LoopCast',
          'Use your phone as a remote for the projector: next and back, Black, Logo, messages, countdowns, the clock, QR codes and switching playlists. No app to install.',
          'Run the slideshow from your phone.',
          'Walk the room, stand by the stage, or step out to the lobby, and still run the screens. LoopCast’s phone remote works in your phone’s browser over Wi-Fi, with nothing to install.',
          f'''      <p>Clickers are great for next and back, but an event screen needs more than that: a logo between speakers, a quick “Lunch is in the Grand Ballroom” message, a countdown at the end of the break. The phone remote puts all of those on your phone, along with what’s playing now and what’s next.</p>
      <h2>Turn on the remote</h2>
      <ol>
        <li>Open the LoopCast desktop app on the computer connected to the screen. {DL}.</li>
        <li>Click <strong>From phone</strong> in the top bar, then choose the <strong>Remote control</strong> tab and press <strong>Turn on the remote</strong>.</li>
        <li>Connect your phone to the <strong>same Wi-Fi</strong> as the computer.</li>
        <li>Point the phone’s camera at the code on screen and tap the link. Keep that page open; it’s your remote.</li>
      </ol>
      {fig('shot-remote-dialog.webp', 'LoopCast’s Your phone box on the Remote control tab, showing a QR code and three steps to connect a phone on the same Wi-Fi.', 'Scan the code with your phone to open the remote.', 1120, 896).replace('class="figure"', 'class="figure mid"')}
      <h2>What you can do from the phone</h2>
      <ul>
        <li>See the playlist, the item on screen now, and the next one.</li>
        <li>Previous, play or pause, and next.</li>
        <li><strong>Black</strong> and <strong>Logo</strong>, for the moment a speaker walks up.</li>
        <li>Turn the <strong>clock</strong>, <strong>QR code</strong> and <strong>picture in picture</strong> on or off.</li>
        <li>Type a <strong>message</strong> for the message bar, and clear it again.</li>
        <li>Start a <strong>countdown</strong>, in minutes or to a time.</li>
        <li>Switch to another <strong>playlist</strong>.</li>
      </ul>
      {fig('shot-remote-phone.webp', 'The LoopCast remote on a phone: what is playing and next, previous, pause and next buttons, Black, Logo, Clock, QR code and PiP buttons, a message box, a countdown box and a playlist menu.', 'The remote in a phone’s browser.', 585, 1266).replace('class="figure"', 'class="figure narrow"')}
      <h2>Good to know</h2>
      <ul>
        <li><strong>Same network.</strong> The phone talks straight to the computer over your Wi-Fi; nothing goes through the internet. Some guest and venue networks block devices from reaching each other. If the phone can’t connect, try another network, a phone hotspot that both devices join, or a small travel router.</li>
        <li><strong>The link is the key.</strong> Anyone with the link can run the screens, so only share it with your team. Press <strong>Turn off the remote</strong> and the link stops working; turning it on again makes a new one.</li>
        <li><strong>More than one phone.</strong> A producer and a stage manager can both open the same link.</li>
        <li><strong>Keep the page open.</strong> If your phone locks, unlock it and the remote reconnects.</li>
      </ul>
      <h2>Phone remote or a clicker?</h2>
      <p>Use both. A presentation clicker is perfect for a speaker clicking through slides in a playlist set to Manual: LoopCast responds to arrow keys and Page Up and Page Down, which is what clickers send. The phone remote is for the person running the room: switching playlists, logos, messages and timers from wherever they’re standing.</p>
      <h2>Also on the phone: send photos</h2>
      <p>The other tab in the From phone box, <strong>Send photos and videos</strong>, lets anyone on the Wi-Fi send pictures from their phone into a Phone uploads playlist. Nothing shows on screen until you choose it. It’s a quick way to get a photo from today’s session onto the screen at the next break.</p>
      <p>The phone remote is a Pro feature in the desktop app. {PRO}</p>''',
          [
              ("Do I need to install an app on my phone?", "No. The remote opens in your phone’s web browser after you scan the code. It works on iPhone and Android."),
              ("Does the phone remote need internet?", "No. The phone and the computer need to be on the same Wi-Fi network, but nothing goes over the internet."),
              ("Why can’t my phone connect?", "Make sure the phone is on the same Wi-Fi as the computer. Some guest and venue networks stop devices from reaching each other; try another network or a hotspot both devices join."),
              ("Is it secure?", "The remote uses a long private link that changes each time you turn it on. Anyone with the link on the same network can control the screens, so share it only with your team, and turn the remote off when you’re done."),
              ("Can I use a presentation clicker too?", "Yes. Clickers send arrow or Page Up and Page Down keys, which LoopCast uses for previous and next."),
              ("Does it work in the browser version of LoopCast?", "No. The phone remote is in the desktop app for Windows and Mac."),
          ], 'shot-remote-phone.webp',
          ['/guides/qr-code-on-projector-screen/', '/guides/free-countdown-timer-event-screen/', '/conferences/'])

    guide('/guides/picture-in-picture-slides-camera/', 'Picture in picture',
          'Show a camera over your slides (picture in picture) | LoopCast',
          'Put a live camera or HDMI feed in a corner of the projector while your slides keep changing behind it. Fixed corners, sizes, shapes and borders. For Windows and Mac.',
          'Show a camera over your slides with picture in picture.',
          'Put the speaker, the band or the worship leader in a corner of the screen while the slides keep looping behind them. LoopCast’s picture in picture uses any webcam or USB HDMI capture device.',
          f'''      <p>In a big room, the people at the back can’t see the speaker’s face. In an overflow room, they can’t see them at all. Picture in picture solves both: a live camera in a corner of the screen, with the agenda, sponsor slides or lyrics images still changing behind it.</p>
      <h2>What you need</h2>
      <ul>
        <li>The LoopCast desktop app for Windows or Mac. {DL}.</li>
        <li>A camera LoopCast can see: a USB webcam, or a camera with HDMI out plugged into a <strong>USB HDMI capture</strong> stick. Inexpensive capture sticks work well. A presenter’s laptop through a capture stick works too.</li>
      </ul>
      <h2>Turn it on</h2>
      <ol>
        <li>Plug in the camera or capture stick.</li>
        <li>Open <strong>Settings › Picture in picture</strong> and choose the camera. On a Mac, macOS asks your permission the first time.</li>
        <li>Pick a <strong>corner</strong>, a <strong>size</strong> (Small, Medium or Large), a <strong>shape</strong> (square corners, rounded or a circle) and a <strong>border</strong> (none, white, cream or red). Turn on <strong>Mirror</strong> for a webcam facing the presenter.</li>
        <li>Press <strong>PiP</strong> (or P) under the preview to show it, and again to hide it.</li>
      </ol>
      {fig('shot-pip.webp', 'A conference welcome slide with a live camera picture of a presenter in a rounded box with a white border in the bottom-right corner.', 'A camera in the corner, rounded with a white border.', 1568, 882)}
      <h2>The slides keep going underneath</h2>
      <p>Picture in picture doesn’t pause anything. The playlist keeps advancing behind the camera, so a walk-in loop or sponsor slides carry on as normal. You can switch playlists, show the logo or a countdown, and the camera stays in its corner until you turn it off. It shows over live web pages too, and in the <a href="/guides/obs-streaming-window/">streaming window</a> for your livestream.</p>
      {fig('shot-pip-app.webp', 'LoopCast’s control window with the camera in the corner of the live preview and the PiP button lit among Timer, Message, QR, Clock, Logo and Black.', 'The PiP button lights up while the camera is on screen.', 1600, 956)}
      <h2>Why fixed corners?</h2>
      <p>The picture snaps to one of four corners at three sizes instead of being dragged around. That keeps it in the same place every time you turn it on, lines it up neatly with the clock or QR code if they share a corner, and means a volunteer can’t accidentally drop it in the middle of a slide. If the QR code is set to the same corner, Settings tells you so you can move one of them.</p>
      <h2>Ideas</h2>
      <ul>
        <li><strong>Conferences:</strong> the speaker in the corner of the agenda or sponsor loop; a remote speaker’s laptop through a capture stick.</li>
        <li><strong>Churches:</strong> the worship leader or pastor on the lobby and overflow screens, over the announcement slides.</li>
        <li><strong>Trade shows:</strong> a live product demo camera over the booth loop.</li>
        <li><strong>Schools:</strong> the stage camera over the program slides at an assembly.</li>
      </ul>
      <h2>Full screen instead?</h2>
      <p>To show a camera or laptop full screen rather than in a corner, use <strong>Inputs</strong> in the sidebar: preview the input, then put it on screen with one click. The playlist waits underneath, and Logo and Black still work.</p>
      <p>Picture in picture is a Pro feature in the desktop app. {PRO}</p>''',
          [
              ("What cameras work with picture in picture?", "Any camera your computer sees as a webcam: built-in and USB webcams, and HDMI cameras through a USB HDMI capture stick."),
              ("Do the slides keep changing behind the camera?", "Yes. The playlist keeps playing underneath, and you can switch playlists, show the logo or start a countdown while the camera stays in its corner."),
              ("Can I drag the picture anywhere?", "No, on purpose. It snaps to one of four corners at three sizes, so it’s always in the same place and can’t end up over the middle of a slide."),
              ("Can I make it round?", "Yes. Settings › Picture in picture has square corners, rounded and circle shapes, and a choice of border."),
              ("Does it work in the browser version?", "No. Picture in picture is in the desktop app for Windows and Mac."),
              ("Does it show in the livestream?", "Yes. If you use the streaming window for OBS, vMix or Ecamm, the camera shows there too."),
          ], 'shot-pip.webp',
          ['/guides/obs-streaming-window/', '/guides/phone-remote-for-slideshow/', '/conferences/'])

    # =====================================================================
    # Expanded existing guides
    # =====================================================================

    guide('/guides/loop-slideshow-on-tv/', 'Loop a slideshow on a TV',
          'How to loop a slideshow on a TV from a laptop (free) | LoopCast',
          'Step-by-step: connect a laptop to a TV, extend the display, and loop pictures, videos and PDFs full screen all day for free, with fixes for black bars, sleep and sound.',
          'How to loop a slideshow on a TV.',
          'All you need is a laptop, an HDMI cable and a folder of pictures. Here’s how to get them repeating on the TV, full screen, for as long as you like, and how to fix the things that usually go wrong.',
          f"""      <h2>What you need</h2>
      <ul>
        <li>A Windows laptop or a Mac.</li>
        <li>A cable from the laptop to the TV, usually HDMI. Many newer laptops only have USB-C, so you may need a USB-C to HDMI adapter.</li>
        <li>Your pictures, videos or PDFs in one folder.</li>
        <li>A power cable for the laptop. A slideshow that runs all day will drain a battery.</li>
      </ul>
      <h2>1. Connect the TV</h2>
      <p>Plug the cable into the laptop and the TV, then switch the TV to that HDMI input with its remote (often a button called Input or Source). If the TV shows “No signal”, unplug and replug the cable with the laptop awake, or try another HDMI port on the TV.</p>
      <h2>2. Set the TV as a second screen</h2>
      <p><strong>Windows:</strong> press the Windows key and P together, then choose <strong>Extend</strong>. <strong>Mac:</strong> open System Settings › Displays and make sure the TV is set as an extended display, not a mirror.</p>
      <p>Extending matters: the TV shows the slideshow while your laptop keeps the controls, so you can change things without the room seeing. Mirroring shows your whole desktop on the TV, including every notification.</p>
      <h2>3. Start the loop</h2>
      <ol>
        <li>{DL}, or <a href="/app/" target="_blank" rel="noopener">open it in your browser</a>.</li>
        <li>Choose your folder. Each folder inside it becomes a playlist.</li>
        <li>Press <strong>Show on projector</strong>. LoopCast opens full screen on the TV.</li>
        <li>Press play. It repeats until you stop it.</li>
      </ol>
      {fig('operator.webp', 'LoopCast’s control window with a live preview of the agenda slide on the TV and a filmstrip of the playlist.', 'Your laptop shows the controls and a live preview; the TV shows only the slides.', 2880, 1720)}
      <h2>4. Set the timing</h2>
      <p>Pictures stay up for the time set in LoopCast’s settings; videos play to the end and then move on. Eight to ten seconds per picture is a good start for a TV people walk past; give slides with more text longer. Want one item to play again before moving on? Press R while it’s on screen to repeat it.</p>
      <h2>Tips for a slideshow people actually read</h2>
      <ul>
        <li>Make slides 16:9 (1920×1080) so they fill the TV with no black bars.</li>
        <li>Keep text big and short: a headline and one line under it. If you can’t read it from across the room on your laptop at arm’s length, it’s too small.</li>
        <li>Use MP4 (H.264) for video. It plays everywhere.</li>
        <li>Mix in a photo or two between text slides to catch the eye.</li>
        <li>Put your logo between messages: name an image <code>logo.png</code> and press H to show it.</li>
      </ul>
      <h2>Fixing common problems</h2>
      <ul>
        <li><strong>Black bars around the picture:</strong> the slide isn’t 16:9, or the TV is set to a different shape. Re-export at 1920×1080, and set the TV’s picture size to “Fit”, “Just scan” or “Screen fit” to stop it cropping the edges.</li>
        <li><strong>The TV goes dark after a while:</strong> the LoopCast desktop app keeps the computer awake while it plays. In a browser, set the computer’s sleep to never. Turn off the TV’s own eco or sleep timer.</li>
        <li><strong>No sound from videos:</strong> on Windows, click the speaker icon and choose the TV as the output; on a Mac, choose it in System Settings › Sound.</li>
        <li><strong>The slideshow opened on the laptop:</strong> make sure the display is extended, then in LoopCast press Find displays in Settings › Projector, or pick the TV there.</li>
      </ul>
      <h2>Only one screen?</h2>
      <p>If the laptop is the screen, or it’s plugged into the TV and closed, press the F key in LoopCast to fill the screen. Esc brings the controls back. For a TV that should run every day, set Settings › Projector to <strong>This screen</strong> and turn on <strong>Start the show automatically</strong>.</p>""",
          [
              ("Can I loop a slideshow on a TV without a laptop?", "Many TVs can play photos from a USB stick, but usually without PDFs, mixed video or control over timing. A laptop, mini PC or old desktop with LoopCast gives you all of that."),
              ("Why is there a black border around my slideshow?", "The slides aren’t the same shape as the TV, or the TV is zooming. Export slides at 1920×1080 and set the TV’s picture size to Fit or Just scan."),
              ("Will the laptop go to sleep?", "Not while the LoopCast desktop app is playing. In the browser version, set the computer’s sleep to never while the slideshow runs."),
              ("Can I change the slides without stopping the slideshow?", "Yes. Add or remove files in the folder; LoopCast picks up the change the next time the loop comes around."),
              ("Does it need Wi-Fi?", "No. LoopCast plays files from your computer and works offline."),
          ], 'operator.webp',
          ['/guides/lobby-tv-slideshow-from-laptop/', '/guides/loop-powerpoint-pdf-on-projector/', '/guides/free-digital-signage-windows-mac/'])

    guide('/guides/lobby-tv-slideshow-from-laptop/', 'Lobby TV slideshow',
          'How to put a slideshow on a lobby TV from a laptop | LoopCast',
          'Run a looping slideshow on a lobby, office or school TV from a laptop or mini PC: cables, display settings, stopping sleep, starting by itself every morning, and updating it remotely.',
          'Put a slideshow on a lobby TV from a laptop.',
          'A lobby TV should show something useful all day without anyone babysitting it. A spare laptop or a small PC and a free app are enough, with no subscription and no cloud account.',
          f"""      <h2>The setup</h2>
      <ol>
        <li><strong>Place the computer near the TV</strong> and connect it with HDMI (or a USB-C to HDMI adapter). Plug it into power.</li>
        <li><strong>Choose how the TV is used.</strong> If the computer also has its own screen, extend the display (Windows + P, then Extend; on a Mac, System Settings › Displays). If the TV is the only screen, that’s fine too.</li>
        <li><strong>Make a folder</strong> called something like “Lobby” and put your pictures, videos and PDFs in it.</li>
        <li><strong>Open LoopCast</strong>, choose the folder, press Show on projector, then press play.</li>
      </ol>
      {fig('use-lobby.webp', 'A lobby display listing today’s events and rooms.', 'A “today in the building” slide.', 960, 540).replace('class="figure"', 'class="figure mid"')}
      <h2>Make it start by itself</h2>
      <p>A lobby sign should come back on its own after a power cut or a Monday-morning restart. In the LoopCast desktop app:</p>
      <ol>
        <li>Set <strong>Settings › Projector</strong> to the TV, or to <strong>This screen</strong> if the TV is the only display.</li>
        <li>Turn on <strong>Start the show automatically</strong>. LoopCast opens the projector and plays the last playlist as soon as it opens.</li>
        <li>Turn on <strong>Open LoopCast when this computer starts</strong>.</li>
      </ol>
      <p>Together, the screen recovers by itself after a restart. If the computer asks for a password at startup, set it to sign in automatically (only on a computer that stays in a safe place) or the sign will wait at the login screen.</p>
      <h2>Change it by time of day</h2>
      <p>In <strong>Settings › Schedule</strong>, add times and a playlist for each: a Morning playlist at 7:30 with today’s events, Lunch at 11:30 with the menu, Evening at 5:00 with tomorrow’s schedule. LoopCast switches by itself using the computer’s clock.</p>
      <h2>Keep it running all day</h2>
      <ul>
        <li>The desktop app keeps the computer awake while it plays. In a browser, set the computer’s sleep to never.</li>
        <li>Turn off notifications during opening hours (Focus on Windows and Mac) so pop-ups don’t appear on the TV if it’s the only screen.</li>
        <li>Schedule system updates for after hours so the computer doesn’t restart at noon.</li>
        <li>Turn off the TV’s own sleep or eco timer. Many TVs switch off when they don’t see a remote press for a few hours.</li>
      </ul>
      <h2>Update it without interrupting</h2>
      <p>Drop new files into the folder, or delete old ones. LoopCast picks up the changes the next time the loop comes around, so the screen never goes blank while you edit.</p>
      <p><strong>Update it from your desk:</strong> make the Lobby folder a synced cloud folder, like OneDrive, Google Drive or Dropbox, on the lobby computer. Anyone with access can add this week’s slides from their own computer, and they appear on the TV once the folder syncs. LoopCast itself still plays from the computer, so the sign keeps running if the internet drops.</p>
      <h2>What to show</h2>
      <ul>
        <li>Today’s events and rooms, the Wi-Fi name and password, and a welcome message.</li>
        <li>Upcoming dates, staff photos or a short video about your organization.</li>
        <li>A live web page, like a calendar or dashboard, in the desktop app (web pages need internet).</li>
        <li>Your logo between messages. Name an image logo.png and press H to show it any time.</li>
        <li>The time in a corner: press C, or turn on the clock in Settings.</li>
      </ul>
      <h2>Which computer?</h2>
      <p>Any Windows 10 or 11 computer or Mac running macOS 12 or later will do. An old laptop with its lid open works. For a neat install behind the TV, a small mini PC is tidy and quiet. Use a wired network connection if you want the folder to sync reliably.</p>
      <p>More ideas for lobbies, offices and schools are on the <a href="/digital-signage/">digital signage page</a>.</p>""",
          [
              ("Can the lobby TV start the slideshow by itself in the morning?", "Yes. In the desktop app, turn on Start the show automatically and Open LoopCast when this computer starts. When the computer starts, LoopCast opens and plays the last playlist on the TV."),
              ("Can I update the lobby TV from another computer?", "Yes. Make the folder LoopCast plays a synced cloud folder (OneDrive, Google Drive, Dropbox). New files appear on the TV after they sync."),
              ("Can it show different slides in the morning and afternoon?", "Yes. In Settings › Schedule, add times and the playlist for each. LoopCast switches by itself."),
              ("Do I need a subscription?", "No. LoopCast is free during our launch and doesn’t need an account or a cloud service."),
              ("What if the TV is the only screen?", "Set Settings › Projector to This screen and LoopCast fills it every time."),
          ], 'use-lobby.webp',
          ['/digital-signage/', '/guides/free-digital-signage-windows-mac/', '/guides/free-yodeck-screencloud-alternatives/'])

    guide('/guides/church-announcement-loop/', 'Church announcement loop',
          'How to set up a church announcement loop (free) | LoopCast',
          'A weekly routine for looping church announcements, welcome slides and a countdown before the service, with a QR code for giving, using free software any volunteer can run.',
          'Set up a church announcement loop.',
          'A weekly routine for pre-service announcements that takes ten minutes to prepare and one click on Sunday, run by whoever is on the rota that week.',
          f"""      <h2>During the week: make the slides</h2>
      <ol>
        <li>Design this week’s announcements in Canva, PowerPoint, Keynote or Google Slides at 16:9 (1920×1080).</li>
        <li>Export them as a <strong>PDF</strong>, or as images. Each page of a PDF becomes its own slide in LoopCast.</li>
        <li>Put the file in a folder called <strong>Announcements</strong>. Add a short video or two if you have them.</li>
      </ol>
      <p>Keep each slide to one announcement: a headline, a date and one line of detail. If people need more, add a QR code (see below) instead of more words.</p>
      {fig('use-church.webp', 'A church welcome slide: coffee in the lobby, service starts at 10:30.', 'A pre-service welcome slide.', 960, 540).replace('class="figure"', 'class="figure mid"')}
      <h2>Organize by moment</h2>
      <p>Make one folder per moment, and each becomes a playlist you can switch between with a click:</p>
      <ul>
        <li><strong>Welcome</strong>: the loop people see as they walk in: a welcome, coffee and kids’ check-in.</li>
        <li><strong>Announcements</strong>: this week’s slides.</li>
        <li><strong>Countdown</strong>: a countdown video, set to stop when it ends, if you use one.</li>
        <li><strong>After</strong>: a goodbye loop with next week’s events.</li>
      </ul>
      <p>Need a version for the second service without one announcement? Duplicate the playlist and hide that slide. The original stays the same.</p>
      <h2>On Sunday: one click</h2>
      <ol>
        <li>Open LoopCast on the computer connected to the projector or lobby TV.</li>
        <li>Press <strong>Show on projector</strong>, then play the Welcome playlist.</li>
        <li>Five minutes out, press <strong>Timer</strong> (T) and type the start time, like <code>10:30</code>, for a full-screen “Starting in” countdown. It goes back to the slides at zero.</li>
        <li>When the service starts, press <strong>Logo</strong> (H) to cover the screen with your church logo, or <strong>Black</strong> (B).</li>
      </ol>
      <h2>Add a QR code for giving or sign-ups</h2>
      <p>Press <strong>QR</strong> (Q), paste your giving page or connection card link, and type “Scan to give”. The code sits in a corner over every slide until you press Q again, so you don’t need to put it on any slides. <a href="/guides/qr-code-on-projector-screen/">More about QR codes on screen</a>.</p>
      <h2>A quick message during the service</h2>
      <p>A car with its lights on, a parent needed in the nursery: press <strong>Message</strong> (M), type a line, and it shows along the bottom of the screen over whatever is up. Press M again to clear it. For a discreet nursery call, a short code like “Nursery: 214” works well.</p>
      <h2>The lobby and kids’ check-in screens</h2>
      <p>Run a copy of LoopCast on each screen’s computer, each with its own folder. A lobby TV can open LoopCast and start the loop by itself every Sunday morning: turn on <strong>Start the show automatically</strong> and <strong>Open LoopCast when this computer starts</strong> in Settings, then use <strong>Settings › Schedule</strong> to switch playlists at set times.</p>
      <h2>On the livestream too</h2>
      <p>If you stream your service, the desktop app’s <a href="/guides/obs-streaming-window/">streaming window</a> sends the same announcement loop and countdown into OBS, vMix or Ecamm, so online viewers see what the room sees before the service starts.</p>
      <h2>Next week</h2>
      <p>Replace last week’s PDF with this week’s. LoopCast picks it up the next time the loop comes around, so there’s nothing to rebuild. If your team shares a cloud folder, whoever makes the slides can drop them straight into the Announcements folder from home.</p>
      <h2>Make it volunteer-proof</h2>
      <ul>
        <li>Tape a card by the computer: “Open LoopCast › Show on projector › play Welcome. T for countdown. H for logo.”</li>
        <li>Name folders by what they’re for, not by date.</li>
        <li>Keep a <code>logo.png</code> in the main folder so H always has something to show.</li>
        <li>Use the <a href="/guides/phone-remote-for-slideshow/">phone remote</a> if the computer is in the booth and the volunteer is down front.</li>
      </ul>
      <p>More about using LoopCast at church is on the <a href="/churches/">churches page</a>.</p>""",
          [
              ("What’s the easiest way to loop church announcements?", "Export your slides as a PDF, put it in a folder, open LoopCast, choose the folder, press Show on projector and play. It loops until you stop it."),
              ("Can I add a countdown before the service?", "Yes. Press T and type the start time, like 10:30, for a full-screen countdown that goes back to the slides at zero. A countdown video works too."),
              ("Will it replace ProPresenter or our worship software?", "No. LoopCast is for the loops around the service: announcements, welcome slides and lobby screens. Keep your lyric software for worship. <a href=\"/propresenter-alternative/\">How they compare</a>."),
              ("Can I show a giving QR code?", "Yes. Press Q, paste the link and add “Scan to give”. It shows in a corner over every slide until you hide it."),
              ("Is it free for churches?", "Yes. LoopCast is free during our launch, for churches and everyone else."),
          ], 'use-church.webp',
          ['/churches/', '/guides/free-countdown-timer-event-screen/', '/guides/free-propresenter-alternatives/'])

    guide('/guides/free-digital-signage-windows-mac/', 'Free digital signage',
          'Free digital signage software for Windows and Mac | LoopCast',
          'Five free ways to run looping digital signage on a TV from a Windows PC or Mac, from built-in slideshows to free plans of cloud signage, with the honest trade-offs of each.',
          'Free digital signage for Windows and Mac.',
          'You don’t need a subscription to put a looping sign on a TV. Here are five free options, what each one is good at, and where each one runs out.',
          f"""      <p class="updated">Prices checked {CHECKED}.</p>
      <h2>1. Your computer’s photo slideshow</h2>
      <p>Windows Photos and macOS Photos can both play a folder of pictures as a slideshow. It’s fine for a handful of photos at home, but it isn’t built for signs: no PDFs, limited control over timing, and it doesn’t keep a second screen separate from your controls.</p>
      <h2>2. PowerPoint or Keynote on repeat</h2>
      <p>Both can loop a presentation by itself. In PowerPoint, set slide timings, then Slide Show › Set Up Slide Show › Browsed at a kiosk. In Keynote, set the presentation to Self-Playing and turn on Loop slideshow. Good when the content already lives in one deck; harder when you want to mix in videos from elsewhere, swap content during the day or switch between several loops. <a href="/guides/powerpoint-kiosk-mode/">PowerPoint kiosk mode, step by step</a>.</p>
      <h2>3. The TV’s USB slideshow</h2>
      <p>Many smart TVs play photos from a USB stick. It costs nothing and needs no computer, but it usually means images only, little control over timing, and walking to the TV with a stick every time something changes.</p>
      <h2>4. Free plans of cloud signage services</h2>
      <p>Hosted signage platforms manage screens from a web dashboard, usually with a small media player at each TV. Some have a free tier: Yodeck, for example, offers one screen free. They suit chains and campuses with many screens to manage from one place; most charge per screen once you grow, and need internet to manage content. <a href="/guides/free-yodeck-screencloud-alternatives/">How they compare with free options</a>.</p>
      <h2>5. A dedicated looping player: LoopCast</h2>
      <p>LoopCast is free during our launch and made for one or a few screens run from a computer you already have:</p>
      <ul>
        <li>Plays pictures, videos and PDFs from a folder, on repeat, full screen on the TV.</li>
        <li>Works offline. Nothing is uploaded and there’s no account.</li>
        <li>Each folder is a playlist; switch between them with a click, or on a schedule.</li>
        <li>Drop in new files and they join the loop without stopping it.</li>
        <li>Logo and black screens on one key, plus a clock, a message bar, a countdown and QR codes.</li>
        <li>Starts by itself when the computer starts, for unattended screens.</li>
      </ul>
      {fig('use-school.webp', 'A school hallway slide: Spirit Week, Friday is blue and gold.', 'A hallway announcement for Spirit Week.', 960, 540).replace('class="figure"', 'class="figure mid"')}
      <h2>Side by side</h2>
""" + table(['', 'Photo slideshow', 'PowerPoint / Keynote', 'Cloud signage free tier', 'LoopCast'], [
              ['Cost', 'Free', 'Free if you own it', 'Free for limited screens, then per screen', 'Free during launch'],
              ['Pictures, video, PDFs', 'Pictures, some video', 'Inside one deck', 'Yes', 'Yes, mixed in one loop'],
              ['Works offline', 'Yes', 'Yes', 'Plays cached content; managing needs internet', 'Yes'],
              ['Several loops', 'No', 'Separate decks', 'Yes', 'Yes, one per folder'],
              ['Schedule by time', 'No', 'No', 'Yes', 'Yes'],
              ['Manage many sites remotely', 'No', 'No', 'Yes', 'Through a synced folder'],
              ['Extra hardware', 'No', 'No', 'Often a player per TV', 'No, any Windows PC or Mac'],
          ]) + f"""
      <h2>Which should you use?</h2>
      <ul>
        <li><strong>A few photos at home:</strong> your computer’s photo slideshow.</li>
        <li><strong>Everything is already in one deck:</strong> PowerPoint or Keynote on repeat.</li>
        <li><strong>Dozens of screens across sites, managed centrally:</strong> a cloud signage service.</li>
        <li><strong>One or a few screens, mixed media, no internet needed:</strong> <a href="/#download">LoopCast</a>.</li>
      </ul>
      <h2>Getting the most from a free sign</h2>
      <ul>
        <li>Design at 1920×1080 so slides fill the TV.</li>
        <li>Fewer words: a sign gets a few seconds of attention.</li>
        <li>Change it often. A sign that never changes stops being read.</li>
        <li>Put the folder somewhere others can reach, like a synced cloud folder, so updating isn’t one person’s job.</li>
      </ul>
      <p class="sources">Sources: <a href="https://www.yodeck.com/pricing" rel="nofollow noopener" target="_blank">Yodeck pricing</a>, <a href="https://support.microsoft.com/en-us/office/create-a-self-running-presentation-57fc41ae-f36a-4fb5-94a3-52d5bc466037" rel="nofollow noopener" target="_blank">Microsoft: Create a self-running presentation</a>.</p>""",
          [
              ("Is there free digital signage software for Windows?", "Yes. LoopCast is free during our launch for Windows and Mac. PowerPoint’s kiosk mode and your computer’s photo slideshow are free too, with fewer features for signs."),
              ("Do I need a special player for digital signage?", "No. Any Windows 10 or 11 computer or Mac with macOS 12 or later, connected to the TV, can run LoopCast."),
              ("Does free signage software need internet?", "LoopCast doesn’t. It plays files from your computer. Cloud services need internet to manage content."),
              ("Can I schedule different content at different times?", "Yes. LoopCast’s Settings › Schedule switches playlists at the times you set."),
              ("What file types can I use?", "Images (JPG, PNG, GIF, WebP, SVG), PDFs and video (MP4, WebM, MOV). Each PDF page becomes a slide."),
          ], 'use-school.webp',
          ['/guides/free-yodeck-screencloud-alternatives/', '/guides/powerpoint-kiosk-mode/', '/guides/lobby-tv-slideshow-from-laptop/'])

    guide('/guides/loop-powerpoint-pdf-on-projector/', 'Loop a PowerPoint or PDF',
          'How to loop a PowerPoint or PDF on a projector | LoopCast',
          'Three ways to make a PowerPoint, Keynote, Google Slides or PDF slideshow loop continuously on a projector or TV, with step-by-step instructions and fixes when it won’t loop.',
          'How to loop a PowerPoint or PDF on a projector.',
          'Three ways to keep a slideshow repeating on a projector or TV, from the setting already in your presentation app to a dedicated looping player, and what to do when it stops.',
          f'''      <h2>1. In PowerPoint</h2>
      <ol>
        <li>On the <strong>Transitions</strong> tab, check <strong>After</strong> and set how many seconds each slide stays up. Click <strong>Apply To All</strong>.</li>
        <li>On the <strong>Slide Show</strong> tab, choose <strong>Set Up Slide Show</strong>. Under Show type, choose <strong>Browsed at a kiosk (full screen)</strong>, which also turns on <strong>Loop continuously until ‘Esc’</strong>. Under Advance slides, choose <strong>Using timings, if present</strong>.</li>
        <li>Start the slide show. It repeats until you press Esc.</li>
      </ol>
      <p>If it stops on a slide, that slide has no timing: check its Transitions tab. Videos inside the deck need to be set to start automatically. <a href="/guides/powerpoint-kiosk-mode/">More on PowerPoint kiosk mode</a>.</p>
      <h2>2. In Keynote or Google Slides</h2>
      <p><strong>Keynote:</strong> in the Document inspector, set the presentation type to <strong>Self-Playing</strong>, choose a delay, and check <strong>Loop slideshow</strong>.</p>
      <p><strong>Google Slides:</strong> start the presentation, open the options menu in the presenter toolbar, choose <strong>Auto-play</strong>, pick a speed and check <strong>Loop</strong>. Google Slides needs internet unless you’ve set it up for offline use.</p>
      <p>These work for a single deck. They get awkward when you need video from elsewhere in the loop, more than one loop for different parts of the day, a logo screen, a countdown, or a preview of what the room sees.</p>
      <h2>3. With LoopCast</h2>
      <p>LoopCast is a free player built for this job. It loops images, PDFs and video, and gives you separate playlists, a live preview and one-key logo and black screens.</p>
      <ol>
        <li><strong>Export your deck as a PDF.</strong> PowerPoint: File › Export › PDF. Keynote: File › Export To › PDF. Google Slides: File › Download › PDF. Canva: Share › Download › PDF.</li>
        <li><strong>Put the PDF in a folder</strong>, along with any videos or images you want in the same loop. Each page of the PDF becomes a slide, drawn sharply at the projector’s resolution.</li>
        <li><strong>Open LoopCast and choose the folder.</strong> Click <strong>Show on projector</strong>, then play. Use <strong>Fullscreen here</strong> if there’s only one screen.</li>
      </ol>
      {fig('operator.webp', 'LoopCast’s control window with a live preview of the slide on the projector and a filmstrip of the playlist.', 'LoopCast’s controls, with a live preview of what the room sees.', 2880, 1720)}
      <h3>Why a PDF instead of the PowerPoint file?</h3>
      <p>A PDF looks the same on every computer: no missing fonts, no “update links” prompts, no version differences between the office and the venue laptop. You lose animations and transitions inside slides, which rarely matter in a loop. If you need a video, put the video file in the folder next to the PDF instead of inside the deck.</p>
      <h3>Click through instead of auto-advance</h3>
      <p>Set a playlist’s <strong>Advance</strong> to <strong>Manual</strong> and each slide stays up until you press next: arrow keys, Page Up and Page Down, or a presentation clicker. Click any slide in the filmstrip to jump to it.</p>
      <h2>Compared</h2>
''' + table(['', 'PowerPoint kiosk', 'Keynote / Google Slides', 'LoopCast'], [
              ['Loops by itself', 'Yes', 'Yes', 'Yes'],
              ['Video from other files', 'Embedded in the deck', 'Embedded in the deck', 'Any MP4, WebM or MOV in the folder'],
              ['Several loops', 'Separate files', 'Separate files', 'One per folder, switch with a click'],
              ['Live preview of the room', 'Presenter view', 'Presenter view', 'Yes, with next item marked'],
              ['Logo / black on one key', 'B for black, W for white', 'Varies', 'H for logo, B for black'],
              ['Countdown, clock, messages', 'No', 'No', 'Yes'],
              ['Change slides mid-loop', 'Stop and restart', 'Stop and restart', 'Drop files in; they join next time around'],
          ]) + f'''
      <h3>Tips for a slideshow that reads well from the back of the room</h3>
      <ul>
        <li>Use a 16:9 slide size to match most projectors and TVs.</li>
        <li>Keep text large and short. Eight to ten seconds per slide is a good starting point.</li>
        <li>Dark backgrounds with light text often look better on projectors, which struggle with true black-on-white contrast in a lit room.</li>
        <li>For video, export MP4 (H.264). It plays everywhere.</li>
      </ul>
      <p class="sources">Source: <a href="https://support.microsoft.com/en-us/office/create-a-self-running-presentation-57fc41ae-f36a-4fb5-94a3-52d5bc466037" rel="nofollow noopener" target="_blank">Microsoft: Create a self-running presentation</a>.</p>''',
          [
              ("How do I make a PowerPoint loop continuously?", "Set slide timings on the Transitions tab, then Slide Show › Set Up Slide Show › Browsed at a kiosk (full screen), with Advance slides set to Using timings, if present. It loops until you press Esc."),
              ("Why does my PowerPoint stop instead of looping?", "Usually a slide has no timing, or Show type isn’t set to kiosk or Loop continuously. Check each slide’s After time on the Transitions tab."),
              ("Can LoopCast open PowerPoint files?", "Not directly. Export the deck as a PDF and put it in the folder; each page becomes a slide. If LoopCast finds a PowerPoint or Keynote file, it tells you how to export it."),
              ("Can I loop a PDF?", "Yes. Put the PDF in a folder and choose it in LoopCast. Every page becomes a slide and the playlist repeats."),
              ("Can I mix a PDF with videos?", "Yes. Put the PDF and the video files in the same folder; LoopCast plays them in one loop."),
          ], 'operator.webp',
          ['/guides/powerpoint-kiosk-mode/', '/guides/loop-slideshow-on-tv/', '/guides/church-announcement-loop/'])

    # =====================================================================
    # Comparisons
    # =====================================================================

    pp_src = '<a href="https://support.renewedvision.com/hc/en-us/articles/35579747176083-Renewed-Vision-Pricing-and-Renewal-Process" rel="nofollow noopener" target="_blank">Renewed Vision: pricing and renewal</a>'
    fq, ld = faq([
        ("Is LoopCast a replacement for ProPresenter?", "Only for loops. LoopCast plays announcements, slides and video on repeat. It doesn’t do lyrics, scripture, stage displays or multi-screen production, so churches that need those should keep ProPresenter or another worship app."),
        ("How much does ProPresenter cost?", f"As of {CHECKED}, Renewed Vision lists ProPresenter at $29 a month or $289 a year for one seat, with discounts for additional annual seats. New users can only buy it as a subscription."),
        ("Can I use LoopCast and ProPresenter together?", "Yes. Many churches run ProPresenter for worship and LoopCast on a second computer for the lobby, kids’ check-in or pre-service screens, so the main operator isn’t tied up with announcements."),
        ("Is LoopCast free?", "Yes, LoopCast is free during our launch, on Windows, Mac and in the browser."),
        ("Does LoopCast work offline like ProPresenter?", "Yes. LoopCast plays files from your computer and needs no internet."),
    ])
    page('/propresenter-alternative/', 'ProPresenter alternative',
         'LoopCast vs ProPresenter: a free alternative for looping slides',
         'An honest comparison of LoopCast and ProPresenter: price, features and when each fits. If you only need to loop announcements, slides and video, LoopCast is free and simpler.',
         'LoopCast vs ProPresenter.',
         'ProPresenter is a full production suite. LoopCast does one job: keeping announcements, slides and video looping on a screen. Here’s an honest look at when each one is the right tool.',
         f'''      <p class="updated">Prices checked {CHECKED}.</p>
      <h2>The short answer</h2>
      <p><strong>If you run worship with lyrics, scripture, stage displays and multiple outputs, use ProPresenter</strong> (or another worship app). It’s built for that and LoopCast isn’t.</p>
      <p><strong>If a screen only needs to loop</strong>, like a lobby TV, a pre-service announcement loop, a kids’ check-in screen, a conference walk-in or a booth display, LoopCast is free, quicker to learn, and doesn’t need a subscription seat for every computer.</p>
      <h2>Side by side</h2>
''' + table(['', 'ProPresenter', 'LoopCast'], [
             ['Made for', 'Worship, live events and broadcast production', 'Looping slides, video and PDFs on event and lobby screens'],
             ['Price', '$29/month or $289/year per seat; extra annual seats discounted', 'Free during launch'],
             ['Buying', 'Subscription only for new users', 'Download, no account'],
             ['Lyrics and Bible verses', 'Yes, with song libraries and scripture', 'No'],
             ['Stage display / confidence monitor', 'Yes', 'No'],
             ['Multiple outputs and screens', 'Yes', 'One output per computer'],
             ['Loop a folder of slides, video and PDFs', 'Yes, by building a playlist', 'Yes: point it at a folder'],
             ['Countdown, clock, message bar', 'Yes', 'Yes'],
             ['QR code overlay', 'Through its own slides and props', 'Yes, one key'],
             ['Picture in picture camera', 'Yes', 'Yes (Pro, free during launch)'],
             ['Send to OBS', 'Yes, with NDI and more', 'Streaming window for window capture (Pro, free during launch)'],
             ['Phone remote', 'Yes, with its own apps', 'Yes, in the phone’s browser (Pro, free during launch)'],
             ['Learning curve', 'Deep; most churches train operators', 'Minutes'],
             ['Platforms', 'Windows and Mac', 'Windows, Mac and any modern browser'],
         ]) + f'''
      <h2>What ProPresenter does that LoopCast doesn’t</h2>
      <p>ProPresenter is professional presentation software for worship and live production. It handles song lyrics and scripture, stage displays for musicians and speakers, multiple screens with different content, timeline cues, and broadcast integrations. If your Sunday depends on those, it’s the right tool, and plenty of churches consider it the standard.</p>
      <h2>What LoopCast does well</h2>
      <ul>
        <li>Loops images, PDFs and video from folders, one folder per playlist. Update the folder and the loop updates.</li>
        <li>A live preview of the screen, with the current and next item marked.</li>
        <li>Logo screen and fade to black on one key.</li>
        <li>Per-playlist endings (loop, stop or end on the logo), per-item repeat, and a manual mode for clickers.</li>
        <li>Countdown to a time, a clock, a message bar and a QR code overlay.</li>
        <li>Schedules that switch playlists at set times, and starting by itself when the computer starts, for unattended screens.</li>
        <li>Runs offline on Windows and Mac, or in any modern browser.</li>
      </ul>
      {fig('operator.webp', 'LoopCast’s control window with a live preview and a filmstrip of the playlist.', 'LoopCast’s whole interface: playlists, a preview and the controls you need.', 2880, 1720)}
      <h2>Using both</h2>
      <p>The two work well side by side. Keep ProPresenter on the main sanctuary computer for worship, and put LoopCast on a second computer for the lobby TV, the kids’ check-in screen and the overflow room. The volunteers who run those screens get one simple app, and your ProPresenter operator isn’t also managing announcements.</p>
      <h2>Cost over a year</h2>
      <p>For one computer, ProPresenter’s listed annual price is $289. A church with a sanctuary computer plus two lobby or classroom screens would need three seats for ProPresenter; LoopCast on the two extra screens costs nothing during our launch. Check Renewed Vision’s current pricing for your situation; volume and legacy pricing differ.</p>
      <h2>Free alternatives with lyrics</h2>
      <p>If you need lyrics and scripture but not the price, look at free, open-source worship apps like FreeShow and OpenLP. We compare them in <a href="/guides/free-propresenter-alternatives/">free ProPresenter alternatives</a>.</p>
{fq}
      <p class="sources">Sources: {pp_src}. ProPresenter is a trademark of Renewed Vision. LoopCast is not affiliated with or endorsed by Renewed Vision.</p>''',
         extra_ld=[ld, article_ld('/propresenter-alternative/', 'LoopCast vs ProPresenter', 'An honest comparison of LoopCast and ProPresenter.', 'operator.webp')],
         rel=['/guides/free-propresenter-alternatives/', '/churches/', '/guides/church-announcement-loop/'])

    guide('/guides/free-propresenter-alternatives/', 'Free ProPresenter alternatives',
          'Best free ProPresenter alternatives for churches | LoopCast',
          'Free alternatives to ProPresenter, compared honestly: FreeShow and OpenLP for lyrics and scripture, LoopCast for announcement loops and lobby screens, and PowerPoint for simple decks.',
          'The best free ProPresenter alternatives.',
          'ProPresenter is excellent, and it’s a subscription for every computer. If your budget is tight, these free tools cover most of what a small church or event needs. We make one of them, so we’ll be clear about what each is for.',
          f'''      <p class="updated">Checked {CHECKED}.</p>
      <h2>First, what do you actually need?</h2>
      <ul>
        <li><strong>Lyrics and Bible verses during worship?</strong> You want a worship presentation app: FreeShow or OpenLP.</li>
        <li><strong>Announcement loops, a lobby TV, a kids’ check-in screen, or a walk-in loop?</strong> You want a looping player: LoopCast.</li>
        <li><strong>One sermon deck with a few slides?</strong> PowerPoint, Keynote or Google Slides may be enough.</li>
      </ul>
      <p>Many churches end up with two: a worship app on the sanctuary computer, and a looping player for every other screen.</p>
      <h2>FreeShow</h2>
      <p>FreeShow is a free, open-source presentation app built for churches and live events. It shows lyrics, scripture and media, with stage display and remote control, and runs on Windows, Mac and Linux. It’s the closest free match to what most churches use ProPresenter for. Some reviewers note it has fewer advanced features than paid suites, and it takes a little time to learn.</p>
      <p><strong>Best for:</strong> churches that want lyrics and scripture for free. <a href="https://freeshow.app" rel="nofollow noopener" target="_blank">freeshow.app</a></p>
      <h2>OpenLP</h2>
      <p>OpenLP is free, open-source worship presentation software that has been around for years. It displays songs, Bible verses, presentations and images, runs on Windows, Mac and Linux, and has Android and iOS remotes. On Windows it can control PowerPoint presentations. Reviewers sometimes find the Mac version less polished than the Windows one.</p>
      <p><strong>Best for:</strong> churches that want a mature, free lyrics app, especially on Windows. <a href="https://openlp.org" rel="nofollow noopener" target="_blank">openlp.org</a></p>
      <h2>LoopCast</h2>
      <p>LoopCast is our app. It isn’t a lyrics app. It loops announcements, welcome slides and video from folders, with a live preview, a countdown to the service start, a QR code for giving, a message bar, and logo and black on one key. It’s simple enough for any volunteer, works offline, and is free during our launch on Windows, Mac and in the browser.</p>
      <p><strong>Best for:</strong> pre-service announcement loops, lobby and kids’ screens, and events. <a href="/#download">Download LoopCast</a></p>
      {fig('use-church.webp', 'A church welcome slide: coffee in the lobby, service starts at 10:30.', 'A pre-service welcome slide looping in LoopCast.', 960, 540).replace('class="figure"', 'class="figure mid"')}
      <h2>PowerPoint, Keynote or Google Slides</h2>
      <p>If you already have one of these, it can loop a single deck (<a href="/guides/powerpoint-kiosk-mode/">here’s how in PowerPoint</a>) and show sermon slides. They aren’t built for lyrics libraries or for switching between several loops, but for a small church with one screen they may be all you need.</p>
      <h2>Compared</h2>
''' + table(['', 'FreeShow', 'OpenLP', 'LoopCast', 'PowerPoint kiosk'], [
              ['Price', 'Free, open source', 'Free, open source', 'Free during launch', 'Included with Microsoft 365'],
              ['Lyrics and scripture', 'Yes', 'Yes', 'No', 'Typed onto slides'],
              ['Announcement loops', 'Yes', 'Yes', 'Yes, from folders', 'One deck'],
              ['Stage display', 'Yes', 'Yes', 'No', 'Presenter view'],
              ['QR code overlay', 'Through slides', 'Through slides', 'Yes, one key', 'Through slides'],
              ['Learning curve', 'Moderate', 'Moderate', 'Minutes', 'Familiar'],
              ['Platforms', 'Windows, Mac, Linux', 'Windows, Mac, Linux', 'Windows, Mac, browser', 'Windows, Mac'],
          ]) + f'''
      <p>Features change often in open-source projects; check each app’s site for the latest.</p>
      <h2>When ProPresenter is still worth it</h2>
      <p>For multi-screen productions, broadcast integration, large song libraries shared across campuses and 7-day support, ProPresenter remains a strong choice. As of {CHECKED}, Renewed Vision lists it at $29 a month or $289 a year per seat. <a href="/propresenter-alternative/">LoopCast vs ProPresenter</a> goes into detail.</p>
      <h2>A setup that costs nothing</h2>
      <ol>
        <li>Sanctuary computer: FreeShow or OpenLP for lyrics and scripture.</li>
        <li>Before the service on the same projector, or on the lobby TV all morning: LoopCast looping the announcements, with a countdown to the start time.</li>
        <li>Kids’ check-in and hallway screens: a LoopCast copy on each, starting by itself when the computer starts.</li>
      </ol>
      <p class="sources">Sources: <a href="https://freeshow.app" rel="nofollow noopener" target="_blank">FreeShow</a>, <a href="https://openlp.org" rel="nofollow noopener" target="_blank">OpenLP</a>, {pp_src}. ProPresenter is a trademark of Renewed Vision. LoopCast is not affiliated with Renewed Vision, FreeShow or OpenLP.</p>''',
          [
              ("What is the best free alternative to ProPresenter?", "For lyrics and scripture, FreeShow and OpenLP are the best-known free, open-source options. For announcement loops and lobby screens, LoopCast is free and simpler."),
              ("Is there a free version of ProPresenter?", "Renewed Vision sells ProPresenter as a subscription for new users. Its pricing page describes watermarked editor seats, not a free version for live output."),
              ("Can LoopCast show song lyrics?", "Not as a lyrics app. You could export lyric slides as a PDF and loop them, but for live worship with song libraries use FreeShow, OpenLP or ProPresenter."),
              ("Can I use FreeShow and LoopCast together?", "Yes. Use FreeShow for worship and LoopCast for the pre-service loop or other screens."),
              ("Do these free apps work on a Mac?", "FreeShow, OpenLP and LoopCast all have Mac versions. LoopCast also runs in any modern browser."),
          ], 'use-church.webp',
          ['/propresenter-alternative/', '/guides/church-announcement-loop/', '/churches/'])

    ms_src = '<a href="https://support.microsoft.com/en-us/office/create-a-self-running-presentation-57fc41ae-f36a-4fb5-94a3-52d5bc466037" rel="nofollow noopener" target="_blank">Microsoft: Create a self-running presentation</a>'
    guide('/guides/powerpoint-kiosk-mode/', 'PowerPoint kiosk mode',
          'PowerPoint kiosk mode: how to set it up, and when to use something else',
          'How to use PowerPoint’s Browsed at a kiosk mode to loop a slideshow unattended, why it sometimes won’t advance, and how it compares with a dedicated looping player.',
          'PowerPoint kiosk mode, and when to use something else.',
          'PowerPoint can loop a slideshow on its own for a booth or lobby screen. Here’s how to set it up properly, the problems people hit, and when a dedicated looping player is less hassle.',
          f'''      <h2>Set up kiosk mode</h2>
      <ol>
        <li><strong>Give every slide a timing.</strong> On the <strong>Transitions</strong> tab, check <strong>After</strong>, set the seconds, and press <strong>Apply To All</strong>. (Or use <strong>Slide Show › Rehearse Timings</strong> to set each one as you go.)</li>
        <li><strong>Open Slide Show › Set Up Slide Show.</strong></li>
        <li>Under <strong>Show type</strong>, choose <strong>Browsed at a kiosk (full screen)</strong>. This turns on <strong>Loop continuously until ‘Esc’</strong> for you.</li>
        <li>Under <strong>Advance slides</strong>, choose <strong>Using timings, if present</strong>.</li>
        <li>If a second screen is connected, pick it under <strong>Multiple monitors</strong>.</li>
        <li>Press <strong>OK</strong>, then start the slide show from the beginning.</li>
      </ol>
      <p>In kiosk mode, clicks don’t advance slides, which stops passers-by from skipping ahead. Press <strong>Esc</strong> to stop.</p>
      <h2>Why kiosk mode won’t advance or loop</h2>
      <ul>
        <li><strong>A slide has no timing.</strong> Kiosk mode ignores clicks, so a slide without an After time waits forever. Check each slide on the Transitions tab.</li>
        <li><strong>Advance slides is set to Manually.</strong> Change it to Using timings, if present.</li>
        <li><strong>A video doesn’t play.</strong> Select the video and, on the Playback tab, set Start to Automatically. Make sure the slide’s timing is at least as long as the video.</li>
        <li><strong>Linked media is missing.</strong> If the deck links to a video on another computer’s drive, it won’t play at the venue. Embed it, or keep the files with the deck.</li>
        <li><strong>The screen sleeps.</strong> Set the computer’s sleep to never for the day, and turn off the TV’s eco timer.</li>
      </ul>
      <h2>Where kiosk mode gets awkward</h2>
      <p>Kiosk mode is fine for one deck that doesn’t change all day. It gets harder when:</p>
      <ul>
        <li><strong>Content changes during the event.</strong> Editing means stopping the show, changing the deck and restarting it, in front of the room.</li>
        <li><strong>You need several loops.</strong> Walk-in, sponsors, lunch and the afternoon all mean separate files and stopping and starting between them.</li>
        <li><strong>You want to see what the room sees</strong> without the audience seeing your controls.</li>
        <li><strong>You need a logo between sessions, a countdown or a quick message.</strong></li>
        <li><strong>The deck came from someone else.</strong> Missing fonts and different PowerPoint versions change how slides look on the venue laptop.</li>
      </ul>
      <h2>The alternative: a looping player</h2>
      <p>LoopCast plays a folder instead of a deck. Export your PowerPoint as a PDF (File › Export › PDF), put it in a folder with any videos and images, and LoopCast loops it, each PDF page as a slide.</p>
      <ul>
        <li>Drop new files into the folder and they join the loop without stopping it.</li>
        <li>One folder per playlist; switch between them with a click, or by schedule.</li>
        <li>A live preview on your laptop while the screen shows only the slides.</li>
        <li>Logo (H) and black (B) on one key; countdown (T), message (M), clock (C) and QR code (Q).</li>
        <li>A PDF looks the same on every computer, so fonts can’t go missing.</li>
      </ul>
      {fig('operator.webp', 'LoopCast’s control window with a live preview and a filmstrip of the playlist.', 'LoopCast: a preview of the screen, with the playlist below.', 2880, 1720)}
      <h2>PowerPoint kiosk mode vs LoopCast</h2>
''' + table(['', 'PowerPoint kiosk mode', 'LoopCast'], [
              ['Price', 'Included with PowerPoint', 'Free during launch'],
              ['Loops unattended', 'Yes', 'Yes'],
              ['Content', 'One deck', 'Folders of images, PDFs and video'],
              ['Change content while it runs', 'Stop, edit, restart', 'Drop files in the folder'],
              ['Several loops', 'Separate decks', 'One playlist per folder'],
              ['Schedule by time of day', 'No', 'Yes'],
              ['Preview without the room seeing', 'Presenter view (not in kiosk mode)', 'Yes'],
              ['Logo, countdown, message, clock, QR', 'No', 'Yes'],
              ['Animations and transitions', 'Yes', 'Fades between slides; no in-slide animation'],
              ['Starts by itself after a restart', 'No', 'Yes, with two settings'],
          ]) + f'''
      <h2>Which should you use?</h2>
      <ul>
        <li><strong>One deck, set once, shown all day:</strong> PowerPoint kiosk mode is fine.</li>
        <li><strong>Animations matter:</strong> stay with PowerPoint; a PDF won’t keep them.</li>
        <li><strong>Several loops, changes during the day, a logo or countdown, or a screen that should run by itself:</strong> <a href="/#download">try LoopCast</a>.</li>
      </ul>
      <p class="sources">Source: {ms_src}. PowerPoint is a trademark of Microsoft. LoopCast is not affiliated with Microsoft.</p>''',
          [
              ("What is PowerPoint kiosk mode?", "It’s the Browsed at a kiosk (full screen) option in Set Up Slide Show. The presentation loops until someone presses Esc, and clicks don’t advance slides."),
              ("Why won’t my kiosk-mode PowerPoint advance?", "Kiosk mode ignores clicks, so every slide needs a timing. Set After on the Transitions tab and choose Using timings, if present in Set Up Slide Show."),
              ("Can I update a PowerPoint kiosk without stopping it?", "No, you need to stop the show, edit and restart. LoopCast plays a folder instead, so new files join the loop without stopping it."),
              ("Does PowerPoint kiosk mode work on a Mac?", "Yes. PowerPoint for Mac has the same Browsed at a kiosk option in Set Up Slide Show."),
              ("Will my PowerPoint animations work in LoopCast?", "No. LoopCast plays PDFs, images and video. Export the deck as a PDF, which keeps each slide’s look but not its animations."),
          ], 'operator.webp',
          ['/guides/loop-powerpoint-pdf-on-projector/', '/trade-shows/', '/guides/free-digital-signage-windows-mac/'])

    yo_src = '<a href="https://www.yodeck.com/pricing" rel="nofollow noopener" target="_blank">Yodeck pricing</a>'
    sc_src = '<a href="https://screencloud.com/pricing" rel="nofollow noopener" target="_blank">ScreenCloud pricing</a>'
    guide('/guides/free-yodeck-screencloud-alternatives/', 'Yodeck and ScreenCloud alternatives',
          'Free alternatives to Yodeck and ScreenCloud for a few screens | LoopCast',
          'An honest look at free alternatives to Yodeck and ScreenCloud for one or a few screens: what the cloud services cost per screen, and when a free offline player is enough.',
          'Free alternatives to Yodeck and ScreenCloud.',
          'Cloud signage services are great at managing many screens from one dashboard, and they charge per screen. If you have one or a few screens, here’s what they cost and when a free option does the job.',
          f'''      <p class="updated">Prices checked {CHECKED}. They change; check each site before you decide.</p>
      <h2>What Yodeck and ScreenCloud cost</h2>
      <p><strong>Yodeck</strong> charges per screen per month. Its pricing page lists a free plan for one screen, then Basic at $8, Premium at $12 and Enterprise at $16 per screen per month. Annual plans include a Yodeck player device for each screen. Yodeck says its players keep playing locally stored content for weeks if the internet goes down.</p>
      <p><strong>ScreenCloud</strong> lists Core from $20 and Pro from $30 per screen per month, billed annually, with Enterprise by quote. It offers a 14-day free trial; its pricing page doesn’t list a free plan.</p>
      <p>Both are built for organizations managing screens across rooms or sites from a web dashboard, with apps, templates, user permissions and remote device management. If that’s you, they’re worth the money.</p>
''' + table(['', 'Yodeck', 'ScreenCloud', 'LoopCast'], [
              ['Price', 'Free for 1 screen; $8–$16 per screen/month after', 'From $20–$30 per screen/month, billed annually', 'Free during launch'],
              ['Free option', 'One screen', '14-day trial', 'Free for any number of screens'],
              ['Hardware', 'Player included on annual plans, or your own device', 'Supported players or your own device', 'Any Windows PC or Mac you already have'],
              ['Managed from', 'Web dashboard', 'Web dashboard', 'The computer by the screen, or a synced folder'],
              ['Internet', 'Needed to manage; plays cached content offline', 'Needed to manage', 'Not needed'],
              ['Apps and integrations', 'Many', 'Many', 'Live web pages, phone uploads'],
              ['Templates and design tools', 'Yes', 'Yes', 'No; bring your own slides'],
              ['Best for', 'Small to large fleets', 'Corporate fleets and dashboards', 'One or a few screens, events'],
          ]) + f'''
      <h2>A year of three screens</h2>
      <p>Say a small office, school or church has three screens. At list prices, Yodeck Basic is one free screen plus two at $8 a month, about $192 a year. ScreenCloud Core at $20 a screen is about $720 a year. LoopCast on three computers you already have costs nothing during our launch. That’s the honest trade: you give up the central dashboard, templates and app integrations.</p>
      <h2>Free alternatives</h2>
      <h3>LoopCast</h3>
      <p>Our app. Point it at a folder of images, PDFs and videos and it loops them full screen on the TV, offline. It has playlists per folder, a schedule that switches playlists by time of day, starting by itself when the computer starts, a clock, a message bar, a countdown, QR codes and live web pages (in the desktop app). To update screens from elsewhere, make each screen’s folder a synced cloud folder.</p>
      {fig('use-lobby.webp', 'A lobby display listing today’s events and rooms.', 'A lobby screen run by LoopCast on a small PC behind the TV.', 960, 540).replace('class="figure"', 'class="figure mid"')}
      <h3>Yodeck’s free screen</h3>
      <p>If you only have one screen and like the idea of a web dashboard, Yodeck’s free single-screen plan is a genuine option. You’ll need a device for the TV, since the free player comes with annual paid plans.</p>
      <h3>PowerPoint or the TV’s USB slideshow</h3>
      <p>For one deck that rarely changes, PowerPoint’s <a href="/guides/powerpoint-kiosk-mode/">kiosk mode</a> or a USB stick in the TV works at no cost, with fewer features.</p>
      <h2>When to pay for cloud signage</h2>
      <ul>
        <li>You manage screens in different buildings or cities.</li>
        <li>Several people need logins with different permissions.</li>
        <li>You want built-in apps: weather, social feeds, dashboards, calendars.</li>
        <li>You need audit logs, single sign-on or a support contract.</li>
      </ul>
      <h2>When a free player is enough</h2>
      <ul>
        <li>One to a handful of screens in one place.</li>
        <li>Your content is slides, posters, PDFs and videos you already make.</li>
        <li>You want it to keep working when the internet doesn’t.</li>
        <li>You’d rather not add a monthly bill for every TV.</li>
      </ul>
      <p class="sources">Sources: {yo_src}, {sc_src}. Yodeck and ScreenCloud are trademarks of their owners. LoopCast is not affiliated with either.</p>''',
          [
              ("Is there a free alternative to Yodeck?", "Yes. LoopCast is free during our launch and loops images, PDFs and video on any number of screens from a Windows PC or Mac, offline. Yodeck itself is free for one screen."),
              ("How much does ScreenCloud cost?", f"As of {CHECKED}, ScreenCloud lists Core from $20 and Pro from $30 per screen per month, billed annually, with a 14-day free trial."),
              ("How much does Yodeck cost?", f"As of {CHECKED}, Yodeck lists a free plan for one screen, then $8, $12 or $16 per screen per month for Basic, Premium and Enterprise."),
              ("Can LoopCast manage screens in different buildings?", "Not from a central dashboard. Each screen runs LoopCast on its own computer. You can update them remotely by making each screen’s folder a synced cloud folder."),
              ("Does LoopCast need a special player box?", "No. It runs on a Windows 10 or 11 computer or a Mac with macOS 12 or later, connected to the TV."),
          ], 'use-lobby.webp',
          ['/digital-signage/', '/guides/free-digital-signage-windows-mac/', '/guides/lobby-tv-slideshow-from-laptop/'])

    # =====================================================================
    # Churches (expanded)
    # =====================================================================
    fq, ld = faq([
        ("Is LoopCast free for churches?", "Yes. LoopCast is free during our launch, on Windows, Mac and in the browser."),
        ("Does it replace ProPresenter or our lyrics software?", "No. LoopCast is for the loops around the service. Keep your worship software for lyrics and scripture, and use LoopCast for announcements, the lobby and kids’ screens."),
        ("Can a volunteer run it?", "Yes. Choose the folder, press Show on projector and play. H shows the logo, B goes to black and T starts a countdown."),
        ("Can we show a countdown to the service?", "Yes. Press T and type the start time, like 10:30. The countdown covers the screen and goes back to the slides at zero."),
        ("Can it show a QR code for online giving?", "Yes. Press Q, paste the giving link and add “Scan to give”. It sits in a corner over every slide until you hide it."),
        ("Can it run the lobby TV by itself?", "Yes. In the desktop app, turn on Start the show automatically and Open LoopCast when this computer starts, and use Settings › Schedule to switch playlists at set times."),
    ])
    page('/churches/', 'Churches',
         'Church announcement loop software, free | LoopCast',
         'Loop church announcements, welcome slides and a countdown before the service, show a giving QR code, and run lobby and kids’ screens. Free, offline, and simple enough for any volunteer.',
         'Pre-service announcement loops for churches.',
         'Welcome slides, announcements and a countdown on the sanctuary and lobby screens, looping until the service starts. Simple enough for any volunteer, and free.',
         f'''      <h2>The announcement loop, without tying up the presentation computer</h2>
      <p>Most churches loop announcements before the service and between services. LoopCast does that one job well: point it at a folder of announcement slides and it plays them on repeat, fullscreen on the sanctuary projector or the lobby TV.</p>
      <ul>
        <li><strong>Volunteer-friendly.</strong> Choose the folder, click Show on projector, press play. Nothing to configure.</li>
        <li><strong>Announcements as a PDF.</strong> Export this week’s slides from Canva, PowerPoint or Keynote as a PDF and drop it in. Each page becomes a slide.</li>
        <li><strong>A countdown to the start time.</strong> Press T, type 10:30, and the screen counts down, then goes back to the slides at zero. Countdown videos work too.</li>
        <li><strong>Lobby and kids’ check-in screens.</strong> Run a separate copy on each screen’s computer, each with its own folder.</li>
      </ul>
      {fig('use-church.webp', 'A church welcome slide: coffee in the lobby, service starts at 10:30.', 'A pre-service welcome slide.', 960, 540)}
      <h2>A Sunday with LoopCast</h2>
      <ol>
        <li><strong>8:30</strong> The lobby TV starts by itself and loops the welcome playlist: coffee, kids’ check-in, this week’s events.</li>
        <li><strong>10:00</strong> On the sanctuary screen, a volunteer plays the Announcements playlist, with a giving QR code in the corner.</li>
        <li><strong>10:25</strong> T, then 10:30: a full-screen “Starting in” countdown on the projector and the livestream.</li>
        <li><strong>10:30</strong> H for the church logo as worship begins, or hand over to your worship software.</li>
        <li><strong>11:45</strong> The goodbye loop with next week’s events while people leave.</li>
      </ol>
      <h2>Built-in tools for Sunday</h2>
      <ul>
        <li><strong>QR code for giving or sign-ups:</strong> Q puts a code in a corner over every slide. <a href="/guides/qr-code-on-projector-screen/">How it works</a>.</li>
        <li><strong>Message bar:</strong> M shows a line of text along the bottom for a nursery call or a parking note.</li>
        <li><strong>Clock:</strong> C puts the time in a corner for the band and speakers.</li>
        <li><strong>Phone remote:</strong> run the screens from your phone while you’re down front. <a href="/guides/phone-remote-for-slideshow/">Set it up</a>.</li>
        <li><strong>Livestream:</strong> the streaming window sends the loop and countdown into OBS, vMix or Ecamm. <a href="/guides/obs-streaming-window/">How to add it</a>.</li>
        <li><strong>Picture in picture:</strong> the pastor or worship leader in a corner of the lobby and overflow screens. <a href="/guides/picture-in-picture-slides-camera/">How it works</a>.</li>
      </ul>
      <p>The phone remote, streaming window and picture in picture are Pro features in the desktop app, free for everyone during our launch.</p>
      <h2>Update it in seconds</h2>
      <p>Replace last week’s files with this week’s and LoopCast picks them up the next time the loop comes around. Want a version for the second service without one announcement? Duplicate the playlist and hide that slide. The original stays as it was. If the person making the slides works from home, a shared cloud folder lets them drop the file straight in.</p>
      <h2>Works alongside your worship software</h2>
      <p>LoopCast doesn’t replace lyric and sermon software. It’s for the loops around the service, on the same projector before worship starts or on a different screen entirely. If you use ProPresenter, FreeShow or OpenLP for worship, LoopCast can run the lobby and kids’ screens on other computers so your main operator can focus on the service. <a href="/propresenter-alternative/">LoopCast vs ProPresenter</a> · <a href="/guides/free-propresenter-alternatives/">free ProPresenter alternatives</a>.</p>
      <h2>Lobby and kids’ screens that run themselves</h2>
      <p>In the desktop app, turn on <strong>Start the show automatically</strong> and <strong>Open LoopCast when this computer starts</strong>. Turn the computer on Sunday morning and the screen comes up with your welcome loop. Use <strong>Settings › Schedule</strong> to switch to the after-service loop at noon.</p>
      <p>Step-by-step: <a href="/guides/church-announcement-loop/">set up a church announcement loop</a>.</p>
{fq}''',
         extra_ld=[ld], rel=['/guides/church-announcement-loop/', '/guides/free-countdown-timer-event-screen/', '/guides/free-propresenter-alternatives/'])
