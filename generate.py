#!/usr/bin/env python3
"""
Regenerate the animated GitHub profile files from config.json.

Usage:
    python3 generate.py

Edit config.json (name, role, skills, stats, languages, projects, etc.)
then rerun this script. It rewrites banner.svg, banner-light.svg,
lanyard.svg, stats.svg, langs.svg, trophies.svg and README.md in the
same folder. Upload those files to your username/username repo root.
"""
import json
import os
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "config.json"), encoding="utf-8") as f:
    C = json.load(f)

T = C["theme"]
NAME = C["name"]
ROLE = C["role_titles"][0]
USER = C["username"]
EMAIL = C["email"]
TAGLINE = C["tagline"]
QUOTE = C["quote"]
SKILLS = C["skills"]
STATS = C["stats"]
LANGS = C["languages"]
TROPHIES = C["trophies"]
PROJECTS = C["projects"]
SOCIALS = C["socials"]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------------------
# BANNER (dark)
# ---------------------------------------------------------------------------
def role_clip_defs(roles, cycle=16):
    """Build clipPaths that cycle through role titles like a typewriter."""
    n = len(roles)
    seg = 1.0 / n
    defs = []
    for i in range(n):
        start = i * seg
        show = start + seg * 0.28
        hide = start + seg * 0.86
        end = start + seg
        defs.append(
            f'<clipPath id="role{i}"><rect x="48" y="216" width="0" height="36">'
            f'<animate attributeName="width" values="0;0;340;340;0;0" '
            f'keyTimes="0;{start:.3f};{show:.3f};{hide:.3f};{end:.3f};1" '
            f'dur="{cycle}s" repeatCount="indefinite" begin="2.9s"/></rect></clipPath>'
        )
    return "\n".join(defs)


def role_text_nodes(roles):
    nodes = []
    for i, r in enumerate(roles):
        nodes.append(
            f'<g clip-path="url(#role{i})"><text x="48" y="244" font-size="26" '
            f'font-weight="700" fill="${{ACCENT1}}">{esc(r)}</text></g>'
        )
    return "\n".join(nodes)


def pill_nodes(skills):
    nodes = []
    x = 48
    y = 320
    for i, s in enumerate(skills):
        w = 46 + len(s) * 9
        delay = 3.6 + i * 0.15
        nodes.append(f'''<g class="pill" style="animation:popPill .45s cubic-bezier(.2,.8,.3,1.3) {delay:.2f}s backwards">
  <rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="#101a2e" stroke="${{ACCENT2}}" stroke-width="1.2"/>
  <text x="{x + w/2:.0f}" y="{y+22}" text-anchor="middle" font-size="13.5" fill="${{TEXTMAIN}}">{esc(s)}</text>
</g>''')
        x += w + 12
        if x > 900:
            x = 48
            y += 46
    return "\n".join(nodes)


BANNER_TMPL = Template(r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 740" width="1280" height="740" role="img" aria-label="$NAME - $ROLE">
<title>$NAME — $ROLE</title>
<defs>
<style type="text/css"><![CDATA[
text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes popPill{0%{opacity:0;transform:translateY(10px) scale(.75)}70%{opacity:1;transform:translateY(-2px) scale(1.05)}100%{opacity:1;transform:translateY(0) scale(1)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
@keyframes neonFlicker{0%{opacity:0}5%{opacity:.7}7%{opacity:.1}10%{opacity:.9}12%{opacity:.3}16%,100%{opacity:1}}
@keyframes neonPulse{0%,100%{opacity:.55}50%{opacity:1}}
@keyframes twinkle{0%,100%{opacity:0;transform:scale(.4)}50%{opacity:1;transform:scale(1)}}
.ltr{opacity:0;animation:popPill .5s cubic-bezier(.2,.8,.3,1.3) forwards;transform-box:fill-box;transform-origin:center bottom}
.pill{opacity:0;transform-box:fill-box;transform-origin:center;transition:transform .2s ease,filter .2s ease;cursor:pointer}
.pill:hover{transform:scale(1.08);filter:brightness(1.3)}
.cur{animation:blink 1s step-end infinite}
.tw{transform-box:fill-box;transform-origin:center;animation:twinkle 2.6s ease-in-out infinite}
.fl{animation:floaty 5s ease-in-out infinite}
.neon-on{animation:neonFlicker 2.4s ease 3.2s backwards}
.np{animation:neonPulse 2.6s ease-in-out infinite}
.sep{stroke:#22314a;stroke-width:1;opacity:.7}
]]></style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="$BG1"/><stop offset="55%" stop-color="$BG2"/><stop offset="100%" stop-color="$BG3"/>
</linearGradient>
<linearGradient id="nameg" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%"><animate attributeName="stop-color" values="$ACCENT1;$ACCENT2;$ACCENT3;$ACCENT1" dur="7s" repeatCount="indefinite"/></stop>
  <stop offset="55%"><animate attributeName="stop-color" values="$ACCENT3;$ACCENT1;$ACCENT2;$ACCENT3" dur="7s" repeatCount="indefinite"/></stop>
  <stop offset="100%"><animate attributeName="stop-color" values="$ACCENT2;$ACCENT3;$ACCENT1;$ACCENT2" dur="7s" repeatCount="indefinite"/></stop>
</linearGradient>
<linearGradient id="borderg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="$ACCENT1" stop-opacity=".35"/>
  <stop offset="50%" stop-color="$ACCENT2" stop-opacity=".3"/>
  <stop offset="100%" stop-color="$ACCENT3" stop-opacity=".35"/>
</linearGradient>
<linearGradient id="scanEdge" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="$ACCENT1" stop-opacity="0"/><stop offset="18%" stop-color="$ACCENT1"/>
  <stop offset="50%" stop-color="$ACCENT3"/><stop offset="82%" stop-color="$ACCENT2"/>
  <stop offset="100%" stop-color="$ACCENT2" stop-opacity="0"/>
</linearGradient>
<linearGradient id="scanTrail" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="$ACCENT1" stop-opacity="0"/><stop offset="100%" stop-color="$ACCENT1" stop-opacity=".18"/>
</linearGradient>
<filter id="glow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glowBig"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="15" cy="15" r=".6" fill="rgba(56,189,248,.10)"/></pattern>
<clipPath id="cPrompt"><rect x="48" y="48" width="0" height="32"><animate attributeName="width" from="0" to="560" dur="1s" begin=".3s" fill="freeze"/></rect></clipPath>
<clipPath id="cHi"><rect x="48" y="86" width="0" height="42"><animate attributeName="width" from="0" to="260" dur=".5s" begin="1.2s" fill="freeze"/></rect></clipPath>
$ROLE_DEFS
<clipPath id="q1"><rect x="76" y="258" width="0" height="46"><animate attributeName="width" from="0" to="420" dur=".8s" begin="3.4s" fill="freeze"/></rect></clipPath>
<clipPath id="bannerBox"><rect x="0" y="0" width="1280" height="740" rx="22"/></clipPath>
<radialGradient id="charGlow"><stop offset="0%" stop-color="$ACCENT2" stop-opacity=".16"/><stop offset="100%" stop-color="$ACCENT2" stop-opacity="0"/></radialGradient>
<clipPath id="charReveal"><rect x="760" y="170" width="480" height="0">
  <animate attributeName="height" from="0" to="500" dur="1.6s" begin=".5s" fill="freeze"/>
</rect></clipPath>
<clipPath id="charBox"><rect x="760" y="170" width="480" height="500" rx="16"/></clipPath>
</defs>

<rect width="1280" height="740" rx="22" fill="url(#bg)"/>
<rect width="1280" height="740" rx="22" fill="url(#dots)"/>
<rect x="1" y="1" width="1278" height="738" rx="21" fill="none" stroke="url(#borderg)" stroke-width="2"/>

<!-- terminal prompt line -->
<g clip-path="url(#cPrompt)">
  <text x="48" y="72" font-size="18" fill="$ACCENT1">user@dev:~$ <tspan fill="$TEXTDIM">cat README.md</tspan></text>
</g>
<rect x="454" y="56" width="9" height="20" fill="$ACCENT1" class="cur">
  <animate attributeName="x" from="454" to="454" dur="1s" begin="1.3s" fill="freeze"/>
</rect>

<!-- name -->
<g clip-path="url(#cHi)">
  <text x="48" y="122" font-size="52" font-weight="800" fill="url(#nameg)">$NAME</text>
</g>

<!-- cycling role titles -->
$ROLE_TEXTS

<!-- tagline / quote -->
<g clip-path="url(#q1)">
  <rect x="48" y="256" width="440" height="48" rx="10" fill="#0d1626" stroke="$ACCENT2" stroke-width="1"/>
  <text x="66" y="286" font-size="15" fill="$TEXTMAIN">&quot;$TAGLINE&quot;</text>
</g>

<!-- tech pills -->
$PILLS

<!-- code card -->
<g style="animation:fadeIn .5s ease 3.2s forwards" opacity="0">
  <rect x="552" y="40" width="286" height="212" rx="12" fill="#0d1626" fill-opacity=".95" stroke="#22314a" stroke-width="1.2"/>
  <rect x="552" y="40" width="286" height="28" rx="12" fill="#101d33"/>
  <circle cx="572" cy="54" r="4.5" fill="#ff5f57"/><circle cx="588" cy="54" r="4.5" fill="#febc2e"/><circle cx="604" cy="54" r="4.5" fill="#28c840"/>
  <text x="695" y="58" text-anchor="middle" font-size="11" fill="$TEXTDIM">build.jsx</text>
  <text x="568" y="90" font-size="12.5"><tspan fill="$ACCENT2">function</tspan><tspan fill="$ACCENT3"> build</tspan><tspan fill="$TEXTMAIN">() {</tspan></text>
  <text x="582" y="110" font-size="12.5"><tspan fill="$ACCENT2">return</tspan><tspan fill="$TEXTMAIN"> (</tspan></text>
  <text x="596" y="130" font-size="12.5"><tspan fill="$TEXTDIM">&lt;</tspan><tspan fill="#4ade80">div</tspan><tspan fill="$ACCENT2"> className</tspan><tspan fill="$TEXTMAIN">=</tspan><tspan fill="#fde047">"dreams"</tspan><tspan fill="$TEXTDIM">&gt;</tspan></text>
  <text x="610" y="150" font-size="12.5"><tspan fill="$TEXTDIM">&lt;</tspan><tspan fill="$ACCENT1">Code</tspan><tspan fill="$TEXTDIM"> /&gt;</tspan></text>
  <text x="610" y="168" font-size="12.5"><tspan fill="$TEXTDIM">&lt;</tspan><tspan fill="#fde047">Learn</tspan><tspan fill="$TEXTDIM"> /&gt;</tspan></text>
  <text x="610" y="186" font-size="12.5"><tspan fill="$TEXTDIM">&lt;</tspan><tspan fill="$ACCENT3">Ship</tspan><tspan fill="$TEXTDIM"> /&gt;</tspan></text>
  <text x="596" y="204" font-size="12.5"><tspan fill="$TEXTDIM">&lt;/</tspan><tspan fill="#4ade80">div</tspan><tspan fill="$TEXTDIM">&gt;</tspan><tspan fill="$TEXTMAIN">);</tspan></text>
  <text x="568" y="222" font-size="12.5"><tspan fill="$TEXTMAIN">}</tspan><tspan fill="$TEXTDIM"> // export default</tspan></text>
</g>

<!-- neon sign -->
<g class="neon-on">
  <rect x="1012" y="42" width="238" height="128" rx="14" fill="none" stroke="$ACCENT3" stroke-width="1.5" opacity=".5" filter="url(#glow)"/>
  <text class="np" x="1131" y="86" text-anchor="middle" font-size="30" font-weight="bold" fill="$ACCENT1" filter="url(#glowBig)">&lt;/&gt;</text>
  <text class="np" x="1131" y="118" text-anchor="middle" font-size="19" font-weight="bold" fill="$ACCENT3" filter="url(#glow)" letter-spacing="2">KEEP CODING</text>
  <text class="np" x="1131" y="146" text-anchor="middle" font-size="19" font-weight="bold" fill="$ACCENT2" filter="url(#glow)" letter-spacing="1.5">KEEP GROWING</text>
</g>

<!-- character panel -->
<ellipse cx="1000" cy="430" rx="280" ry="260" fill="url(#charGlow)"/>
<g clip-path="url(#charBox)">
$CHARACTER
  <!-- top-down hologram formation edge -->
  <rect x="760" y="168" width="480" height="4" fill="url(#scanEdge)" filter="url(#glow)" opacity="0">
    <animate attributeName="opacity" values="0;.95;.95;0" keyTimes="0;.04;.9;1" dur="1.8s" begin=".5s" fill="freeze"/>
    <animate attributeName="y" from="170" to="666" dur="1.6s" begin=".5s" fill="freeze"/>
  </rect>
</g>

<!-- footer -->
<line x1="48" y1="676" x2="1232" y2="676" class="sep" stroke-dasharray="1184" stroke-dashoffset="1184">
  <animate attributeName="stroke-dashoffset" from="1184" to="0" dur=".7s" begin="4.2s" fill="freeze"/>
</line>
<g style="animation:fadeIn .5s ease 4.4s forwards" opacity="0">
  <text x="48" y="707" font-size="12.5" fill="$TEXTMAIN">$USER</text>
  <text x="240" y="707" font-size="12.5" fill="$TEXTMAIN">$EMAIL</text>
</g>
<text x="1232" y="707" text-anchor="end" font-size="13" style="animation:fadeIn .5s ease 4.5s forwards" opacity="0">
  <tspan fill="$TEXTDIM">“</tspan><tspan fill="$ACCENT3">$QUOTE</tspan><tspan fill="$TEXTDIM">” </tspan><tspan fill="$ACCENT1">❤</tspan>
</text>
<text x="700" y="707" font-size="11.5" style="animation:fadeIn .5s ease 4.4s forwards" opacity="0">
  <tspan fill="#28c840">●</tspan><tspan fill="$TEXTDIM"> open to collaborate</tspan>
</text>

<!-- full-banner scanner sweep -->
<g clip-path="url(#bannerBox)" opacity="0">
  <animate attributeName="opacity" from="0" to="1" dur=".6s" begin="3s" fill="freeze"/>
  <g>
    <animateTransform attributeName="transform" type="translate" values="0,-40;0,780" dur="3.5s" begin="3s" repeatCount="indefinite"/>
    <rect x="0" y="-34" width="1280" height="34" fill="url(#scanTrail)"/>
    <rect x="0" y="0" width="1280" height="2.6" fill="url(#scanEdge)" opacity=".6" filter="url(#glow)"/>
  </g>
</g>
</svg>
''')


def build_character_placeholder():
    """A simple original vector illustration used until a real character
    image is supplied via config['character_image']."""
    a1, a2, a3 = T["accent1"], T["accent2"], T["accent3"]
    return f'''<rect x="760" y="170" width="480" height="500" fill="#0d1626"/>
  <!-- floor -->
  <rect x="760" y="560" width="480" height="110" fill="#0a101f"/>
  <!-- desk -->
  <rect x="880" y="470" width="280" height="14" rx="4" fill="#182036" stroke="{a2}" stroke-opacity=".5"/>
  <line x1="900" y1="484" x2="900" y2="560" stroke="#182036" stroke-width="10"/>
  <line x1="1120" y1="484" x2="1120" y2="560" stroke="#182036" stroke-width="10"/>
  <!-- chair -->
  <rect x="930" y="330" width="120" height="150" rx="30" fill="#141f38" stroke="{a2}" stroke-opacity=".4"/>
  <!-- person: simple stylized silhouette -->
  <g fill="{a1}" fill-opacity=".9">
    <circle cx="990" cy="300" r="42"/>
    <path d="M930 470 q0-90 60-95 q60 5 60 95 z"/>
  </g>
  <g fill="#0d1626">
    <path d="M955 285 q35-30 70 0 q0 40-35 45 q-35-5-35-45z" fill="{a2}" fill-opacity=".85"/>
  </g>
  <!-- laptop -->
  <g>
    <rect x="945" y="452" width="90" height="8" rx="2" fill="{a3}"/>
    <rect x="955" y="415" width="70" height="40" rx="3" fill="#0a101f" stroke="{a3}" stroke-width="2"/>
    <rect x="960" y="420" width="60" height="30" fill="{a3}" fill-opacity=".18"/>
  </g>
  <!-- speech / status bubble -->
  <g class="fl">
    <rect x="1020" y="230" width="150" height="46" rx="12" fill="#101d33" stroke="{a3}" stroke-width="1.2"/>
    <text x="1095" y="259" text-anchor="middle" font-size="13" fill="{a3}">&lt;coding/&gt;</text>
  </g>
  <text x="1000" y="600" text-anchor="middle" font-size="12.5" fill="#5b6b85">add your character art — see config.json</text>'''


def build_character_real(path):
    import base64
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = "image/png" if ext == "png" else ("image/jpeg" if ext in ("jpg", "jpeg") else "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (f'<image x="760" y="170" width="480" height="500" '
            f'preserveAspectRatio="xMidYMax slice" '
            f'href="data:{mime};base64,{b64}"/>')


def build_banner(light=False):
    if not light:
        bg1, bg2, bg3 = T["bg1"], T["bg2"], T["bg3"]
        textmain, textdim = T["textMain"], T["textDim"]
    else:
        bg1, bg2, bg3 = "#f8fafc", "#eef2f9", "#ffffff"
        textmain, textdim = "#1e293b", "#64748b"

    role_defs = role_clip_defs(C["role_titles"])
    role_texts = role_text_nodes(C["role_titles"])
    pills = pill_nodes(SKILLS)

    char_path = C.get("character_image", "")
    if char_path and os.path.exists(os.path.join(HERE, char_path)):
        character = build_character_real(os.path.join(HERE, char_path))
    else:
        character = build_character_placeholder()

    svg = BANNER_TMPL.safe_substitute(
        NAME=esc(NAME), ROLE=esc(ROLE), USER=esc(USER), EMAIL=esc(EMAIL),
        TAGLINE=esc(TAGLINE), QUOTE=esc(QUOTE),
        BG1=bg1, BG2=bg2, BG3=bg3,
        ACCENT1=T["accent1"], ACCENT2=T["accent2"], ACCENT3=T["accent3"],
        TEXTMAIN=textmain, TEXTDIM=textdim,
        ROLE_DEFS=role_defs, ROLE_TEXTS=role_texts, PILLS=pills,
        CHARACTER=character,
    )
    # fill in the $ACCENT1/$TEXTMAIN etc left inside role_texts/pills (built before substitution)
    svg = Template(svg).safe_substitute(
        ACCENT1=T["accent1"], ACCENT2=T["accent2"], ACCENT3=T["accent3"],
        TEXTMAIN=textmain, TEXTDIM=textdim,
    )
    return svg


# ---------------------------------------------------------------------------
# LANYARD (swinging ID badge, initials avatar)
# ---------------------------------------------------------------------------
def build_lanyard():
    initials = "".join([w[0] for w in NAME.split()][:2]).upper()
    return Template(r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 460" width="330" height="460" role="img" aria-label="$NAME ID badge">
<defs>
<style><![CDATA[
@keyframes swing{0%{transform:rotate(0deg)}25%{transform:rotate(4.5deg)}50%{transform:rotate(0deg)}75%{transform:rotate(-4.5deg)}100%{transform:rotate(0deg)}}
@keyframes dropIn{0%{transform:translateY(-160px);opacity:0}60%{transform:translateY(8px);opacity:1}80%{transform:translateY(-4px)}100%{transform:translateY(0)}}
@keyframes shine{0%{transform:translateX(-140px) rotate(20deg)}100%{transform:translateX(240px) rotate(20deg)}}
.rig{transform-box:fill-box;transform-origin:top center;animation:dropIn 1.1s cubic-bezier(.3,.6,.3,1) forwards, swing 4.5s ease-in-out 1.1s infinite}
.shine{animation:shine 3.5s ease-in-out 1.6s infinite}
text{font-family:'SFMono-Regular',Consolas,monospace}
]]></style>
<linearGradient id="strap" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="$ACCENT1"/><stop offset="100%" stop-color="$ACCENT2"/>
</linearGradient>
<linearGradient id="cardg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="#101a2e"/><stop offset="100%" stop-color="#0a1120"/>
</linearGradient>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="$ACCENT1"/><stop offset="50%" stop-color="$ACCENT3"/><stop offset="100%" stop-color="$ACCENT2"/>
</linearGradient>
<clipPath id="cardClip"><rect x="55" y="150" width="220" height="280" rx="18"/></clipPath>
</defs>

<g class="rig">
  <!-- strap -->
  <path d="M150 0 L150 165 M180 0 L180 165" stroke="url(#strap)" stroke-width="26" stroke-linecap="round"/>
  <text x="165" y="40" text-anchor="middle" font-size="10" fill="#0a1120" transform="rotate(90,165,40)">$USER</text>
  <text x="165" y="100" text-anchor="middle" font-size="10" fill="#0a1120" transform="rotate(90,165,100)">$USER</text>

  <!-- clasp -->
  <circle cx="165" cy="150" r="12" fill="#c8d0dc" stroke="#8a94a3" stroke-width="2"/>
  <circle cx="165" cy="150" r="5" fill="#0a1120"/>

  <!-- card -->
  <rect x="55" y="150" width="220" height="280" rx="18" fill="url(#cardg)" stroke="$ACCENT2" stroke-width="1.5"/>
  <g clip-path="url(#cardClip)">
    <rect x="55" y="150" width="220" height="46" fill="#141f38"/>
    <text x="165" y="180" text-anchor="middle" font-size="13" fill="$ACCENT3" letter-spacing="2">DEVELOPER</text>

    <!-- avatar ring + initials -->
    <circle cx="165" cy="260" r="46" fill="none" stroke="url(#ring)" stroke-width="3"/>
    <circle cx="165" cy="260" r="40" fill="#0d1626"/>
    <text x="165" y="272" text-anchor="middle" font-size="30" font-weight="800" fill="url(#ring)">$INITIALS</text>

    <text x="165" y="336" text-anchor="middle" font-size="19" font-weight="700" fill="#f1f5f9">$NAME</text>
    <text x="165" y="358" text-anchor="middle" font-size="12.5" fill="$ACCENT1">$ROLE</text>
    <text x="165" y="380" text-anchor="middle" font-size="11" fill="#8b949e">@$USER</text>

    <!-- barcode -->
    <g transform="translate(85,398)" fill="#c9d1d9">
      <rect x="0" y="0" width="2" height="18"/><rect x="4" y="0" width="1" height="18"/><rect x="7" y="0" width="3" height="18"/>
      <rect x="12" y="0" width="1" height="18"/><rect x="15" y="0" width="2" height="18"/><rect x="19" y="0" width="1" height="18"/>
      <rect x="22" y="0" width="3" height="18"/><rect x="27" y="0" width="1" height="18"/><rect x="30" y="0" width="2" height="18"/>
      <rect x="34" y="0" width="1" height="18"/><rect x="37" y="0" width="3" height="18"/><rect x="42" y="0" width="1" height="18"/>
      <rect x="45" y="0" width="2" height="18"/><rect x="49" y="0" width="1" height="18"/><rect x="52" y="0" width="3" height="18"/>
      <rect x="57" y="0" width="1" height="18"/><rect x="60" y="0" width="2" height="18"/><rect x="64" y="0" width="1" height="18"/>
      <rect x="67" y="0" width="3" height="18"/><rect x="72" y="0" width="1" height="18"/><rect x="75" y="0" width="2" height="18"/>
      <rect x="79" y="0" width="1" height="18"/><rect x="82" y="0" width="3" height="18"/><rect x="87" y="0" width="1" height="18"/>
      <rect x="90" y="0" width="2" height="18"/><rect x="94" y="0" width="1" height="18"/><rect x="97" y="0" width="3" height="18"/>
      <rect x="102" y="0" width="1" height="18"/><rect x="105" y="0" width="2" height="18"/><rect x="109" y="0" width="1" height="18"/>
      <rect x="112" y="0" width="3" height="18"/><rect x="117" y="0" width="1" height="18"/><rect x="120" y="0" width="2" height="18"/>
      <rect x="124" y="0" width="1" height="18"/><rect x="127" y="0" width="3" height="18"/><rect x="132" y="0" width="1" height="18"/>
      <rect x="135" y="0" width="2" height="18"/><rect x="139" y="0" width="1" height="18"/><rect x="142" y="0" width="3" height="18"/>
      <rect x="147" y="0" width="1" height="18"/><rect x="150" y="0" width="2" height="18"/>
    </g>

    <!-- holo shine sweep -->
    <rect class="shine" x="0" y="150" width="60" height="290" fill="#ffffff" opacity=".08" transform="skewX(-20)"/>
  </g>
</g>
</svg>
''').safe_substitute(
        NAME=esc(NAME), ROLE=esc(ROLE), USER=esc(USER), INITIALS=esc(initials),
        ACCENT1=T["accent1"], ACCENT2=T["accent2"], ACCENT3=T["accent3"],
    )


# ---------------------------------------------------------------------------
# STATS
# ---------------------------------------------------------------------------
def build_stats():
    rows = [
        ("Total Stars", STATS["total_stars"]),
        ("Total Commits", STATS["total_commits"]),
        ("Total PRs", STATS["total_prs"]),
        ("Total Issues", STATS["total_issues"]),
        ("Contributed To", STATS["contributed_to"]),
    ]
    row_nodes = []
    y = 76
    for i, (label, val) in enumerate(rows):
        delay = 0.3 + i * 0.15
        row_nodes.append(f'''<g opacity="0" style="animation:slideIn .5s ease {delay:.2f}s forwards">
  <text x="24" y="{y}" font-size="13.5" fill="$TEXTDIM">{esc(label)}</text>
  <text x="330" y="{y}" text-anchor="end" font-size="13.5" font-weight="700" fill="$TEXTMAIN">{val}</text>
</g>''')
        y += 30
    rows_svg = "\n".join(row_nodes)

    pct = max(0, min(100, STATS.get("rank_percent", 50)))
    circumference = 2 * 3.14159265 * 40
    dash = circumference * (pct / 100)

    return Template(r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 230" width="420" height="230" role="img" aria-label="$NAME GitHub stats">
<defs>
<style><![CDATA[
@keyframes slideIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}
@keyframes ringFill{from{stroke-dashoffset:$CIRC}to{stroke-dashoffset:$OFFSET}}
text{font-family:'SFMono-Regular',Consolas,monospace}
]]></style>
<linearGradient id="ringg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="$ACCENT1"/><stop offset="100%" stop-color="$ACCENT2"/>
</linearGradient>
</defs>
<rect width="420" height="230" rx="14" fill="$BG2" stroke="$ACCENT2" stroke-opacity=".4" stroke-width="1"/>
<text x="24" y="36" font-size="16" font-weight="700" fill="$TEXTMAIN">$NAME&#8217;s GitHub Stats</text>

$ROWS

<g transform="translate(370,100)">
  <circle r="40" fill="none" stroke="#1c2942" stroke-width="8"/>
  <circle r="40" fill="none" stroke="url(#ringg)" stroke-width="8" stroke-linecap="round"
    transform="rotate(-90)" stroke-dasharray="$CIRC" stroke-dashoffset="$CIRC">
    <animate attributeName="stroke-dashoffset" from="$CIRC" to="$OFFSET" dur="1.4s" begin=".4s" fill="freeze"/>
  </circle>
  <text text-anchor="middle" y="7" font-size="20" font-weight="800" fill="$TEXTMAIN">$RANK</text>
</g>
</svg>
''').safe_substitute(
        NAME=esc(NAME), ROWS=rows_svg, RANK=esc(STATS["rank"]),
        CIRC=f"{circumference:.2f}", OFFSET=f"{circumference - dash:.2f}",
        BG2=T["bg2"], ACCENT1=T["accent1"], ACCENT2=T["accent2"],
        TEXTMAIN=T["textMain"], TEXTDIM=T["textDim"],
    )


# ---------------------------------------------------------------------------
# LANGUAGES
# ---------------------------------------------------------------------------
def build_langs():
    rows = []
    y = 60
    for i, lang in enumerate(LANGS):
        w = max(2, lang["percent"] * 2.4)
        delay = 0.3 + i * 0.15
        rows.append(f'''<g opacity="0" style="animation:fadeIn .4s ease {delay:.2f}s forwards">
  <text x="24" y="{y-6}" font-size="12.5" fill="$TEXTMAIN">{esc(lang['name'])}</text>
  <text x="396" y="{y-6}" text-anchor="end" font-size="12.5" fill="$TEXTDIM">{lang['percent']}%</text>
  <rect x="24" y="{y}" width="372" height="8" rx="4" fill="#1c2942"/>
  <rect x="24" y="{y}" width="0" height="8" rx="4" fill="{lang['color']}">
    <animate attributeName="width" from="0" to="{w:.1f}" dur="1s" begin="{delay+0.1:.2f}s" fill="freeze"/>
  </rect>
</g>''')
        y += 38
    rows_svg = "\n".join(rows)
    height = y + 16
    return Template(r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 $H" width="420" height="$H" role="img" aria-label="$NAME top languages">
<defs><style><![CDATA[
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
text{font-family:'SFMono-Regular',Consolas,monospace}
]]></style></defs>
<rect width="420" height="$H" rx="14" fill="$BG2" stroke="$ACCENT2" stroke-opacity=".4" stroke-width="1"/>
<text x="24" y="30" font-size="16" font-weight="700" fill="$TEXTMAIN">Most Used Languages</text>
$ROWS
</svg>
''').safe_substitute(
        NAME=esc(NAME), ROWS=rows_svg, H=height,
        BG2=T["bg2"], ACCENT2=T["accent2"],
        TEXTMAIN=T["textMain"], TEXTDIM=T["textDim"],
    )


# ---------------------------------------------------------------------------
# TROPHIES
# ---------------------------------------------------------------------------
def build_trophies():
    cells = []
    cw = 150
    for i, tr in enumerate(TROPHIES):
        x = 16 + i * (cw + 12)
        delay = 0.2 + i * 0.15
        cells.append(f'''<g opacity="0" style="animation:popIn .5s cubic-bezier(.2,.8,.3,1.3) {delay:.2f}s forwards" transform-box="fill-box" transform-origin="center">
  <rect x="{x}" y="10" width="{cw}" height="150" rx="12" fill="$BG2" stroke="$ACCENT2" stroke-opacity=".5" stroke-width="1.2"/>
  <text x="{x+cw/2:.0f}" y="60" text-anchor="middle" font-size="34">🏆</text>
  <text x="{x+cw/2:.0f}" y="100" text-anchor="middle" font-size="12.5" fill="$TEXTDIM">{esc(tr['label'])}</text>
  <text x="{x+cw/2:.0f}" y="132" text-anchor="middle" font-size="22" font-weight="800" fill="$ACCENT1">{esc(tr['rank'])}</text>
</g>''')
    cells_svg = "\n".join(cells)
    width = 16 + len(TROPHIES) * (cw + 12)
    return Template(r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 $W 175" width="$W" height="175" role="img" aria-label="$NAME trophies">
<defs><style><![CDATA[
@keyframes popIn{0%{opacity:0;transform:translateY(12px) scale(.75)}70%{opacity:1;transform:translateY(-3px) scale(1.05)}100%{opacity:1;transform:translateY(0) scale(1)}}
text{font-family:'SFMono-Regular',Consolas,monospace}
]]></style></defs>
$CELLS
</svg>
''').safe_substitute(
        NAME=esc(NAME), CELLS=cells_svg, W=width,
        BG2=T["bg2"], ACCENT1=T["accent1"], ACCENT2=T["accent2"], TEXTDIM=T["textDim"],
    )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------
def build_readme():
    proj_rows = "\n".join(
        f"| [{esc(p['name'])}]({p['url']}) | `{esc(p['tech'])}` | {p['stars']} |"
        for p in PROJECTS
    )
    social_links = []
    if SOCIALS.get("email"):
        social_links.append(f'<a href="mailto:{SOCIALS["email"]}"><img src="https://img.shields.io/badge/Email-{T["accent1"].lstrip("#")}?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>')
    if SOCIALS.get("github"):
        social_links.append(f'<a href="https://github.com/{SOCIALS["github"]}"><img src="https://img.shields.io/badge/GitHub-{T["accent2"].lstrip("#")}?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>')
    if SOCIALS.get("linkedin"):
        social_links.append(f'<a href="https://linkedin.com/in/{SOCIALS["linkedin"]}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>')
    if SOCIALS.get("instagram"):
        social_links.append(f'<a href="https://instagram.com/{SOCIALS["instagram"]}"><img src="https://img.shields.io/badge/Instagram-{T["accent3"].lstrip("#")}?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"/></a>')
    if SOCIALS.get("youtube"):
        social_links.append(f'<a href="https://youtube.com/@{SOCIALS["youtube"]}"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"/></a>')
    socials_html = "\n".join(social_links)

    return f'''<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./banner.svg?v=1">
  <source media="(prefers-color-scheme: light)" srcset="./banner-light.svg?v=1">
  <img src="./banner.svg?v=1" alt="{esc(NAME)} — {esc(ROLE)}" width="100%"/>
</picture>

</div>

<br/>

<table align="center" border="0">
<tr>
<td width="35%" align="center" valign="middle">

<img src="./lanyard.svg?v=1" alt="{esc(NAME)} ID badge" width="300"/>

</td>
<td width="65%" valign="middle">

### 🚀 About Me

Hi, I'm **{esc(NAME)}** — a **{esc(ROLE)}**.

- 🔭 Currently building projects with {", ".join(SKILLS)}
- 🌱 Always learning something new
- 📫 Reach me at **{esc(EMAIL)}**

### 📌 Projects

| Project | Tech | ⭐ |
|:---|:---:|:---:|
{proj_rows}

<br/>

> 💬 *"{esc(TAGLINE)}"*

</td>
</tr>
</table>

<br/>

<div align="center">

### 📊 GitHub Stats & Graphs

<img src="./stats.svg?v=1" alt="GitHub Stats" height="200"/>
<img src="./langs.svg?v=1" alt="Top Languages" height="200"/>

<br/><br/>

<img src="https://streak-stats.demolab.com?user={SOCIALS.get('github','')}&theme=dark&hide_border=true&background=0f172a&ring={T['accent1'].lstrip('#')}&fire={T['accent2'].lstrip('#')}&currStreakLabel={T['accent3'].lstrip('#')}" alt="GitHub Streak"/>

<br/><br/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username={SOCIALS.get('github','')}&bg_color=0f172a&color={T['accent1'].lstrip('#')}&line={T['accent2'].lstrip('#')}&point={T['accent3'].lstrip('#')}&area=true&area_color={T['accent2'].lstrip('#')}&hide_border=true&custom_title=Contribution%20Graph" alt="Contribution graph" width="95%"/>

<br/><br/>

<img src="./trophies.svg?v=1" alt="Trophies" width="95%"/>

<br/><br/>

### 🐍 Contribution Snake

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{SOCIALS.get('github','')}/{SOCIALS.get('github','')}/output/github-snake.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{SOCIALS.get('github','')}/{SOCIALS.get('github','')}/output/github-snake-light.svg">
  <img src="https://raw.githubusercontent.com/{SOCIALS.get('github','')}/{SOCIALS.get('github','')}/output/github-snake.svg" alt="Contribution snake"/>
</picture>

<br/><br/>

### 📫 Let's Connect

{socials_html}

<br/><br/>

<img src="https://komarev.com/ghpvc/?username={SOCIALS.get('github','')}&color={T['accent1'].lstrip('#')}&style=for-the-badge&label=PROFILE+VIEWS" alt="Profile views"/>

<br/><br/>

*⭐️ Always learning, always building.*

</div>
'''


# ---------------------------------------------------------------------------
# WRITE FILES
# ---------------------------------------------------------------------------
def write(path, content):
    with open(os.path.join(HERE, path), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


if __name__ == "__main__":
    write("banner.svg", build_banner(light=False))
    write("banner-light.svg", build_banner(light=True))
    write("lanyard.svg", build_lanyard())
    write("stats.svg", build_stats())
    write("langs.svg", build_langs())
    write("trophies.svg", build_trophies())
    write("README.md", build_readme())
    print("Done. Edit config.json and rerun `python3 generate.py` anytime.")
