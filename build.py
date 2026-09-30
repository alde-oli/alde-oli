#!/usr/bin/env python3
"""YoRHa-style SVG components for the GitHub profile of alde-oli.

Style reference (no game assets are used):
- palette from metakirby5/yorha (MIT) : #d1cdb7 #454138 #dcd8c0 #bab5a1 #ccc8b1
- UI principles from the PlatinumGames blog post "UI Design in NieR:Automata"
Font: Noto Sans (SIL Open Font License 1.1), subset and embedded as WOFF2.
"""
import base64, io, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
VF = "/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf"

BG, INK, PAPER, MUTED, GRID, ACCENT = "#d1cdb7", "#454138", "#dcd8c0", "#bab5a1", "#c6c1aa", "#cd664d"
CHARS = "".join(chr(c) for c in range(32, 127)) + "▸■□─·—…→éèàçÉ×©"


def font_b64(weight):
    f = instancer.instantiateVariableFont(TTFont(VF), {"wght": weight})
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
    s = subset.Subsetter(opts); s.populate(text=CHARS); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


FONTS = {}


def style(extra=""):
    if not FONTS:
        FONTS["l"], FONTS["m"] = font_b64(300), font_b64(500)
    return f"""<style>
@font-face{{font-family:Y;font-weight:300;src:url(data:font/woff2;base64,{FONTS['l']}) format('woff2')}}
@font-face{{font-family:Y;font-weight:500;src:url(data:font/woff2;base64,{FONTS['m']}) format('woff2')}}
text{{font-family:Y,'Noto Sans',Helvetica,sans-serif;fill:{INK}}}
.l{{font-weight:300}} .m{{font-weight:500}} .inv{{fill:{PAPER}}} .mut{{fill:#7d7766}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes scan{{0%{{transform:translateY(-40px)}}100%{{transform:translateY(var(--h))}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{.blink,.pulse,.scan{{animation:none}}}}
{extra}
</style>"""


def esc(s):
    return html.escape(s, quote=True)


def svg(w, h, body, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
{style(extra_css)}
<defs><pattern id="g" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M6 0H0V6" fill="none" stroke="{GRID}" stroke-width="0.6"/></pattern>
<radialGradient id="v" cx="50%" cy="50%" r="75%"><stop offset="70%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#3a372f" stop-opacity=".18"/></radialGradient></defs>
<rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#g)"/>
{arcs(w, h)}
{body}
<rect width="{w}" height="{h}" fill="url(#v)" pointer-events="none"/>
</svg>"""


def arcs(w, h):
    """Large faint arcs behind the menus, as in the in-game system screens."""
    out = ""
    for cx, cy, r in [(w * 0.82, h * 1.9, w * 0.62), (w * 0.82, h * 1.9, w * 0.66), (-w * 0.1, -h * 0.9, w * 0.45)]:
        out += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" stroke="{INK}" stroke-width="1" opacity=".08"/>'
    return out


def analog_border(w, y, flip=False):
    """Top/bottom border frieze: thin rule, end blocks, then a band of short dashes and dot triplets."""
    by = y + 5 if not flip else y - 7
    out = (f'<rect x="16" y="{y}" width="{w - 32}" height="1.2" fill="{INK}"/>'
           f'<rect x="16" y="{y - 3}" width="7" height="7" fill="{INK}"/><rect x="{w - 23}" y="{y - 3}" width="7" height="7" fill="{INK}"/>')
    x = 36
    while x < w - 60:
        out += f'<rect x="{x}" y="{by}" width="14" height="2" fill="{INK}" opacity=".6"/>'
        for k in range(3):
            out += f'<rect x="{x + 22 + k * 5}" y="{by}" width="2" height="2" fill="{INK}" opacity=".6"/>'
        x += 48
    return out


def title(x, y, txt, size=34, sub=None):
    t = f'<text x="{x}" y="{y}" class="l" font-size="{size}" letter-spacing="{size * 0.18:.1f}">{esc(txt)}</text>'
    t += f'<rect x="{x}" y="{y + 10}" width="{len(txt) * size * 0.78:.0f}" height="1" fill="{INK}"/>'
    t += f'<rect x="{x}" y="{y + 7}" width="6" height="6" fill="{INK}"/>'
    if sub:
        t += f'<text x="{x + 12}" y="{y + 30}" class="l mut" font-size="13" letter-spacing="2">{esc(sub)}</text>'
    return t


def cursor(x, y):
    """Menu cursor: flattened diamond with a tail and a ':' pair in front."""
    return (f'<g transform="translate({x},{y})"><path d="M-2 0 L5 -6 L12 0 L5 6 Z" fill="{INK}"/>'
            f'<rect x="-16" y="-0.6" width="13" height="1.2" fill="{INK}"/>'
            f'<rect x="-22" y="-4" width="2.4" height="2.4" fill="{INK}"/><rect x="-22" y="1.6" width="2.4" height="2.4" fill="{INK}"/></g>')


def glyph(i, x, y, col):
    """Small knocked-out glyph for tab badges (circle, square, triangle, cross, diamond)."""
    k = i % 5
    if k == 0:
        return f'<circle cx="{x}" cy="{y}" r="3.2" fill="none" stroke="{col}" stroke-width="1.4"/>'
    if k == 1:
        return f'<rect x="{x - 3}" y="{y - 3}" width="6" height="6" fill="{col}"/>'
    if k == 2:
        return f'<path d="M{x} {y - 3.6} L{x + 3.6} {y + 3} L{x - 3.6} {y + 3} Z" fill="{col}"/>'
    if k == 3:
        return f'<path d="M{x - 3} {y - 3} L{x + 3} {y + 3} M{x + 3} {y - 3} L{x - 3} {y + 3}" stroke="{col}" stroke-width="1.5"/>'
    return f'<path d="M{x} {y - 4} L{x + 4} {y} L{x} {y + 4} L{x - 4} {y} Z" fill="{col}"/>'



def menu_item(x, y, w, label, selected=False, right=""):
    h = 30
    if selected:
        out = (f'<rect x="{x - 6}" y="{y - 5}" width="{w + 12}" height="1" fill="{INK}"/>'
               f'<rect x="{x - 6}" y="{y + h + 4}" width="{w + 12}" height="1" fill="{INK}"/>'
               f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{INK}"/>'
               f'<rect x="{x + 10}" y="{y + 11}" width="8" height="8" fill="{PAPER}"/>'
               f'<text x="{x + 30}" y="{y + 20}" class="m inv" font-size="14" letter-spacing="1.6">{esc(label)}</text>'
               f'<text x="{x + w - 12}" y="{y + 20}" class="l inv" font-size="12" text-anchor="end" letter-spacing="1">{esc(right)}</text>'
               + cursor(x - 18, y + h / 2))
    else:
        out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" opacity=".55"/>'
               f'<rect x="{x + 10}" y="{y + 11}" width="8" height="8" fill="{INK}"/>'
               f'<text x="{x + 30}" y="{y + 20}" class="l" font-size="14" letter-spacing="1.6">{esc(label)}</text>'
               f'<text x="{x + w - 12}" y="{y + 20}" class="l mut" font-size="12" text-anchor="end" letter-spacing="1">{esc(right)}</text>')
    return out


def panel(x, y, w, h, head, lines, size=14, lh=22):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="30" fill="{INK}"/>'
           f'<text x="{x + 14}" y="{y + 20}" class="m inv" font-size="14" letter-spacing="2">{esc(head)}</text>'
           f'<rect x="{x}" y="{y + h - 1}" width="{w}" height="1" fill="{INK}"/>'
           f'<rect x="{x + w - 10}" y="{y + h - 10}" width="6" height="6" fill="{INK}"/>')
    for i, ln in enumerate(lines):
        cls = "m" if ln.startswith("!") else "l"
        ln = ln.lstrip("!")
        out += f'<text x="{x + 16}" y="{y + 56 + i * lh}" class="{cls}" font-size="{size}" letter-spacing=".4">{esc(ln)}</text>'
    return out


def tabs(w, y, labels, sel):
    out, x = "", 40
    for i, lab in enumerate(labels):
        tw = len(lab) * 9.6 + 48
        on = i == sel
        if on:
            out += f'<rect x="{x}" y="{y}" width="{tw}" height="28" fill="{INK}"/>'
        fg, bg = (INK, PAPER) if on else (PAPER, INK)
        out += f'<rect x="{x + 8}" y="{y + 7}" width="14" height="14" fill="{bg}"/>' + glyph(i, x + 15, y + 14, fg)
        cls = "m inv" if on else "l"
        out += f'<text x="{x + 30 + (tw - 30) / 2 - 4}" y="{y + 19}" class="{cls}" font-size="13" letter-spacing="2.4" text-anchor="middle">{esc(lab)}</text>'
        if not on:
            out += f'<rect x="{x}" y="{y + 27}" width="{tw}" height="1" fill="{INK}" opacity=".35"/>'
        x += tw + 8
    return out


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name}: {len(content) // 1024} KB")


# ─────────────────────────────── components ───────────────────────────────
W = 1000
TABS = ["UNIT", "MISSIONS", "EQUIPMENT", "ARCHIVE", "COMMS"]


def emblem(cx, cy, d):
    """Sperm-whale emblem from emblems.py, scaled to diameter d."""
    import emblems as E
    k = d / E.S
    return (f'<g transform="translate({cx - d / 2:.1f},{cy - d / 2:.1f}) scale({k:.4f})">'
            f'{E.backdrop()}{E.whale()}</g>')


def header():
    h = 250
    b = analog_border(W, 22)
    b += tabs(W, 40, TABS, 0)
    b += f'<text x="{W - 40}" y="60" class="l" font-size="12" letter-spacing="3" text-anchor="end">LAUSANNE · CH</text>'
    b += f'<text x="44" y="116" class="l" font-size="17" letter-spacing="7">YoRHa //</text>'
    b += f'<text x="40" y="168" class="l" font-size="46" letter-spacing="10">UNIT ALDE-OLI</text>'
    b += f'<rect x="512" y="132" width="18" height="36" fill="{INK}" class="blink"/>'
    b += f'<rect x="40" y="182" width="490" height="1.2" fill="{INK}"/><rect x="40" y="179" width="7" height="7" fill="{INK}"/>'
    b += f'<text x="44" y="208" class="m" font-size="14" letter-spacing="5">BACKEND &amp; PLATFORM DEVELOPER</text>'
    b += emblem(628, 150, 128)
    rows = [("STATUS", "OPERATIONAL"), ("STATION", "SYNCAI"), ("TRAINING", "42 LAUSANNE"), ("CORE", "PYTHON · DJANGO")]
    x0 = 722
    for i, (k, v) in enumerate(rows):
        yy = 112 + i * 26
        b += f'<rect x="{x0}" y="{yy - 9}" width="5" height="5" fill="{INK}"/>'
        b += f'<text x="{x0 + 13}" y="{yy}" class="l" font-size="12" letter-spacing="1.6">{k}</text>'
        b += f'<text x="{W - 40}" y="{yy}" class="m" font-size="12" letter-spacing="1.6" text-anchor="end">{esc(v)}</text>'
    b += f'<rect x="{x0 - 14}" y="98" width="1" height="96" fill="{INK}"/>'
    b += f'<rect x="{W - 46}" y="{h - 44}" width="6" height="6" fill="{ACCENT}" class="pulse"/>'
    b += analog_border(W, h - 22, flip=True)
    write("header.svg", svg(W, h, b))


def unit():
    h = 330
    b = title(40, 58, "UNIT DATA", 26, "PERSONNEL RECORD // SYNCAI")
    items = [("DESIGNATION", "A. DE OLIVEIRA MAIA"), ("CLASS", "BACKEND & PLATFORM"),
             ("STATION", "SYNCAI · LAUSANNE"), ("TRAINING", "42 LAUSANNE"), ("LANGUAGES", "FR · EN")]
    for i, (k, v) in enumerate(items):
        b += menu_item(56, 110 + i * 40, 360, k, selected=(i == 1), right=v if i != 1 else "")
    b += panel(460, 100, 500, 200, "CLASS // BACKEND & PLATFORM", [
        "I build Python/Django tools that automate business",
        "decisions: setting a price, proposing a supplier order,",
        "reading an order confirmation.",
        "!I take them to production, reliably:",
        "pipeline, monitoring, verified backups.",
        "Trained at 42 Lausanne. French native, fluent English."], size=14, lh=22)
    write("unit.svg", svg(W, h, b))


def missions():
    h = 400
    b = title(40, 58, "MISSIONS", 26, "ACTIVE ASSIGNMENTS // CODE CLASSIFIED")
    items = [("ATHENA", "2024 ─ NOW"), ("PLATFORM & RELIABILITY", "2026 ─ NOW"), ("PROCUREMENT AUTOMATION", "2026 ─ NOW")]
    for i, (k, v) in enumerate(items):
        b += menu_item(56, 110 + i * 40, 380, k, selected=(i == 0), right=v)
    b += (f'<text x="60" y="270" class="l mut" font-size="12" letter-spacing="1.5">CLIENT · SYNCAI SA</text>'
          f'<text x="60" y="292" class="l mut" font-size="12" letter-spacing="1.5">CLEARANCE · PRIVATE REPOSITORIES</text>'
          f'<rect x="60" y="306" width="376" height="1" fill="{INK}" opacity=".4"/>')
    b += panel(480, 100, 480, 272, "ATHENA // REPRICING PLATFORM", [
        "!Repricing & product integration for",
        "!Digitec Galaxus sellers.",
        "Python/Django backend: catalogue sync,",
        "competitor-offer tracking, automatic pricing",
        "(margin, fees, VAT, shipping), publication.",
        "Designed the move from Airflow to ~10 Python",
        "microservices driven by PostgreSQL queues.",
        "Migration to the official marketplace API.",
        "Near-real-time sales & pricing analytics.",
        "Also: CI/CD, servers and alerting since 2026."], size=13, lh=22)
    write("missions.svg", svg(W, h, b))


def missions_more():
    h = 210
    b = ""
    b += panel(40, 20, 450, 170, "PLATFORM & RELIABILITY", [
        "GitLab CI/CD, deploys gated by a health check.",
        "Linux staging & production servers, firewall,",
        "encryption-key rotation.",
        "Grafana alerting as code; PostgreSQL backups",
        "restored and verified before switchover."], size=13, lh=22)
    b += panel(510, 20, 450, 170, "PROCUREMENT AUTOMATION", [
        "Consulting for a Swiss technical-distribution SME.",
        "On-site audit, then improved the ERP's order-",
        "proposal engine (Access, SQL Server, VBA).",
        "Supplier confirmations read automatically",
        "(PDF, OCR, generative AI). Both in production."], size=13, lh=22)
    write("missions-2.svg", svg(W, h, b))


def equipment():
    groups = [("BACKEND", ["PYTHON", "DJANGO / DRF", "POSTGRESQL", "SQL SERVER"]),
              ("PLATFORM", ["DOCKER", "GITLAB CI/CD", "LINUX", "GRAFANA · PROMETHEUS · LOKI"]),
              ("FOUNDATIONS", ["C", "C++", "PYTEST", "GIT"])]
    h = 300
    b = title(40, 58, "EQUIPMENT", 26, "INSTALLED PLUG-IN CHIPS")
    y = 104
    for g, chips in groups:
        b += f'<text x="44" y="{y + 19}" class="m" font-size="12" letter-spacing="3">{g}</text>'
        x = 190
        for c in chips:
            cw = len(c) * 9.2 + 40
            b += (f'<rect x="{x}" y="{y}" width="{cw}" height="28" fill="{PAPER}"/>'
                  f'<rect x="{x}" y="{y}" width="4" height="28" fill="{INK}"/>'
                  f'<rect x="{x + cw - 9}" y="{y + 4}" width="5" height="5" fill="{INK}" opacity=".6"/>'
                  f'<text x="{x + 16}" y="{y + 19}" class="l" font-size="13" letter-spacing="1.4">{esc(c)}</text>')
            x += cw + 10
        y += 56
    write("equipment.svg", svg(W, h, b))


def section(name, label, sub):
    h = 80
    b = (f'<rect x="16" y="40" width="{W - 32}" height="1.2" fill="{INK}"/>'
         f'<rect x="16" y="37" width="7" height="7" fill="{INK}"/><rect x="{W - 23}" y="37" width="7" height="7" fill="{INK}"/>'
         f'<rect x="40" y="18" width="{len(label) * 13 + 40}" height="30" fill="{INK}"/>'
         f'<text x="60" y="39" class="m inv" font-size="15" letter-spacing="4">{esc(label)}</text>'
         f'<text x="{W - 40}" y="66" class="l mut" font-size="12" letter-spacing="2" text-anchor="end">{esc(sub)}</text>')
    write(name, svg(W, h, b))


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def card(repo, kind, pitch, stack, status="■ COMPLETE"):
    w, h = 480, 170
    b = (f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" fill="{PAPER}"/>'
         f'<rect x="10" y="10" width="{w - 20}" height="32" fill="{INK}"/>'
         f'<rect x="22" y="22" width="8" height="8" fill="{PAPER}"/>'
         f'<text x="40" y="31" class="m inv" font-size="14" letter-spacing="2.2">{esc(repo.upper())}</text>'
         f'<text x="{w - 22}" y="31" class="l inv" font-size="11" letter-spacing="1.5" text-anchor="end">{esc(kind)}</text>')
    for i, ln in enumerate(wrap(pitch, 58)[:3]):
        b += f'<text x="24" y="{66 + i * 20}" class="l" font-size="13" letter-spacing=".3">{esc(ln)}</text>'
    b += f'<rect x="24" y="{h - 42}" width="{w - 48}" height="1" fill="{INK}" opacity=".4"/>'
    b += f'<text x="24" y="{h - 22}" class="m" font-size="11" letter-spacing="1.6">{esc(stack.upper())}</text>'
    b += f'<text x="{w - 24}" y="{h - 22}" class="l" font-size="11" letter-spacing="1.6" text-anchor="end">{esc(status)}</text>'
    b += f'<rect x="{w - 16}" y="{h - 16}" width="6" height="6" fill="{INK}"/>'
    write(f"card-{repo}.svg", svg(w, h, b))


def comms():
    h = 130
    b = (f'<rect x="40" y="24" width="{W - 80}" height="82" fill="{PAPER}"/>'
         f'<rect x="40" y="24" width="4" height="82" fill="{INK}"/>'
         f'<text x="62" y="52" class="m" font-size="13" letter-spacing="3">POD 042 // COMMS</text>'
         f'<text x="62" y="80" class="l" font-size="14" letter-spacing=".5">Proposal: open a channel on LinkedIn — linkedin.com/in/alexandre-deoliveiramaia</text>'
         f'<rect x="{W - 58}" y="36" width="6" height="6" fill="{ACCENT}" class="pulse"/>'
         f'<text x="62" y="98" class="l mut" font-size="11" letter-spacing="1.5">FR · développeur backend &amp; plateforme chez SyncAI à Lausanne, formé à 42 Lausanne.</text>')
    write("comms.svg", svg(W, h, b))


if __name__ == "__main__":
    header(); unit(); missions(); missions_more(); equipment(); comms()
    section("sec-archive.svg", "ARCHIVE", "SELECTED PUBLIC RECORDS")
    CARDS = [
        ("ft_place_bot", "PERSONAL", "Keeps a pixel-art image intact on 42 Lausanne's FTPlace board, repainting wrong pixels by priority.", "Python · Poetry · CI", "□ ARCHIVED"),
        ("webserv", "42 · TEAM OF 2", "HTTP/1.1 server from scratch: non-blocking poll() loop, virtual hosts, uploads, directory listing, CGI.", "C++98"),
        ("ft_transcendance", "42 · TEAM OF 4", "Multiplayer Pong platform with accounts, live chat, tournaments and an AI opponent.", "Django · Channels · PostgreSQL · Docker"),
        ("SuperMiniRT", "42 · TEAM OF 2", "Multithreaded CPU ray tracer with reflections, textures, bump maps and a free-flying camera.", "C · MiniLibX · pthreads"),
        ("minishell", "42 · TEAM OF 2", "Bash-like shell: pipes, redirections, heredocs, && / || with parentheses, wildcards.", "C · readline"),
        ("Inception", "42 · SOLO", "WordPress stack in Docker Compose: NGINX (TLS only), PHP-FPM and MariaDB, each built from Debian.", "Docker · NGINX · MariaDB"),
        ("upsi-jam-5", "GAME JAM · TEAM OF 5", "Platformer: split into a chained clone to swing and climb. Web build auto-deployed to itch.io.", "Godot 4 · GitHub Actions"),
        ("dslr", "42 · TEAM OF 2", "One-vs-all logistic regression and data visualisation from scratch in Julia.", "Julia"),
    ]
    for c in CARDS:
        card(*c)
