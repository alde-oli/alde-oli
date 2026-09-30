#!/usr/bin/env python3
"""NieR:Automata weapon-illustration style emblems (original drawings traced from real references).

Composition studied from the in-game weapon illustrations: dark disc, concentric rings
lightening toward the centre, rotated light square, cardinal diamonds, light dots,
the subject as a dark flat silhouette laid diagonally with thin light detail lines.
Subjects drawn from reference photos/illustrations (helmet sketch, NOAA sperm whale,
field-guide raven) — outlines are my own paths, no image is embedded.
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emblems")
os.makedirs(OUT, exist_ok=True)
S = 460; C = S / 2

RIM, R1, R2, R3, CORE = "#57534a", "#78725f", "#918b77", "#aaa48e", "#c6c0a9"
SQ, DOT, INK, LINE, ACC = "#d3cdb6", "#d8d2bb", "#3f3b33", "#bdb7a0", "#cd664d"


def backdrop():
    out = f'<circle cx="{C}" cy="{C}" r="{C}" fill="{RIM}"/>'
    out += f'<circle cx="{C}" cy="{C}" r="{C - 10}" fill="none" stroke="{LINE}" stroke-width="1.5" opacity=".55"/>'
    for r, col in [(196, R1), (160, R2), (124, R3), (86, CORE)]:
        out += f'<circle cx="{C}" cy="{C}" r="{r}" fill="{col}"/>'
    # rotated light square frame
    out += (f'<rect x="{C - 108}" y="{C - 108}" width="216" height="216" fill="none" stroke="{SQ}" '
            f'stroke-width="7" transform="rotate(45 {C} {C})" opacity=".85"/>')
    # cardinal diamonds on the outer ring
    for a in range(0, 360, 90):
        x = C + 178 * math.cos(math.radians(a)); y = C + 178 * math.sin(math.radians(a))
        out += f'<rect x="{x - 11}" y="{y - 11}" width="22" height="22" fill="{INK}" transform="rotate(45 {x:.1f} {y:.1f})"/>'
    # light dots on the square
    for a in range(45, 360, 90):
        x = C + 104 * math.cos(math.radians(a)); y = C + 104 * math.sin(math.radians(a))
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{DOT}"/>'
    return out


def wrap(inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">'
            f'{backdrop()}{inner}</svg>')


def place(paths, cx, cy, scale, rot, dx=0, dy=0):
    return (f'<g transform="translate({C + dx},{C + dy}) rotate({rot}) scale({scale}) translate({-cx},{-cy})" '
            f'stroke-linejoin="round" stroke-linecap="round">{paths}</g>')


def helmet():
    shell = ("M85 205 L150 172 C165 150 190 130 230 115 C290 92 360 84 420 95 C480 108 525 145 550 190 "
             "C565 215 578 240 584 266 L590 420 C592 445 596 465 594 474 C585 492 566 505 548 512 "
             "C540 540 528 568 510 586 C470 570 420 548 370 520 C310 486 240 448 200 424 "
             "C170 410 150 398 145 388 C138 350 134 300 132 250 C120 232 102 218 85 205 Z")
    visor = "M428 282 C470 268 540 262 582 262 L588 412 C560 406 518 394 474 360 C446 338 430 314 428 282 Z"
    return place(
        f'<path d="{shell}" fill="{INK}"/>'
        f'<path d="{visor}" fill="{RIM}" stroke="{LINE}" stroke-width="5"/>'
        f'<path d="M440 292 C490 280 540 276 572 276" stroke="{LINE}" stroke-width="4" fill="none" opacity=".8"/>'
        f'<circle cx="452" cy="326" r="11" fill="none" stroke="{LINE}" stroke-width="5"/>'
        f'<path d="M150 178 L300 380 L330 372" stroke="{LINE}" stroke-width="4" fill="none"/>'
        f'<path d="M160 164 L250 128 M455 150 L510 180" stroke="{LINE}" stroke-width="5" fill="none"/>'
        f'<path d="M358 232 L392 226 L400 268 L368 276 Z" fill="none" stroke="{LINE}" stroke-width="4"/>'
        f'<path d="M150 392 C230 440 320 492 410 540" stroke="{LINE}" stroke-width="4" fill="none" opacity=".7"/>'
        f'<path d="M552 408 L590 474 M520 520 L540 560" stroke="{LINE}" stroke-width="4" fill="none"/>'
        f'<path d="M232 120 C300 96 380 90 430 100" stroke="{ACC}" stroke-width="7" fill="none"/>',
        340, 340, 0.5, 0, -4, 4)


def whale():
    body = ("M8 212 C40 196 90 188 150 186 C230 184 320 190 400 200 C430 196 445 198 462 206 "
            "L490 212 L505 208 L520 218 L540 214 L555 225 L575 222 L590 234 C615 245 640 252 660 256 "
            "L700 250 C715 246 730 250 736 262 C715 275 698 285 688 300 C702 318 720 332 732 348 "
            "C712 352 688 344 670 330 C650 312 630 305 600 302 C520 312 420 322 330 322 "
            "C290 322 262 318 240 312 C200 312 150 312 110 308 C70 304 30 298 14 286 C4 270 2 236 8 212 Z")
    wrinkles = "".join(f'<path d="M{x} {y} l{l} {d}" stroke="{LINE}" stroke-width="3" fill="none" opacity=".7"/>'
                       for x, y, l, d in [(250, 214, 60, 2), (300, 228, 70, 3), (360, 240, 60, 4), (420, 222, 50, 4),
                                          (440, 262, 60, 6), (330, 272, 50, 2), (500, 250, 50, 6), (540, 272, 40, 6)])
    return place(
        f'<path d="{body}" fill="{INK}"/>'
        f'<path d="M58 302 C110 309 170 309 222 303" stroke="{LINE}" stroke-width="6" fill="none"/>'
        + "".join(f'<path d="M{x} 303 l2 -8" stroke="{LINE}" stroke-width="3"/>' for x in range(70, 200, 16))
        + f'<circle cx="200" cy="262" r="7" fill="{LINE}"/>'
        f'<path d="M262 300 C282 320 302 332 316 328 C304 312 288 300 270 294 Z" fill="{RIM}" stroke="{LINE}" stroke-width="3"/>'
        f'<path d="M10 218 C60 204 120 196 160 196" stroke="{LINE}" stroke-width="4" fill="none" opacity=".8"/>'
        + wrinkles +
        f'<path d="M690 262 L712 272 M694 306 L716 330" stroke="{LINE}" stroke-width="3" fill="none"/>',
        370, 268, 0.54, -30, 4, 4)


def raven():
    body = ("M686 180 C664 164 632 152 600 150 C590 148 568 144 546 146 C520 150 500 162 488 180 "
            "C478 205 470 235 450 262 C400 300 330 330 250 380 C180 425 110 480 40 545 L70 598 "
            "C150 570 220 548 290 530 C330 525 360 530 385 532 L420 540 "
            "C470 520 530 470 565 400 C585 355 590 310 588 270 L600 252 L590 243 L603 231 L594 221 "
            "L606 208 C606 202 608 199 612 198 C644 194 668 188 686 180 Z")
    wing = ("M478 250 C420 282 330 332 250 392 C190 440 130 490 64 548 C150 522 250 484 330 444 "
            "C410 404 468 354 500 302 Z")
    feathers = "".join(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{LINE}" stroke-width="3" fill="none" opacity=".75"/>'
                       for x1, y1, x2, y2 in [(470, 300, 300, 420), (440, 330, 240, 470), (400, 370, 170, 510),
                                              (360, 400, 120, 530), (450, 270, 360, 330)])
    legs = (f'<path d="M398 534 L410 620 M410 620 L382 646 M410 620 L462 648 M410 620 L420 646" '
            f'stroke="{INK}" stroke-width="12" fill="none"/>')
    return place(
        f'<path d="{body}" fill="{INK}"/>{legs}'
        f'<path d="{wing}" fill="{RIM}" stroke="{LINE}" stroke-width="3"/>' + feathers +
        f'<path d="M606 176 L676 178" stroke="{LINE}" stroke-width="4" fill="none"/>'
        f'<path d="M604 156 C598 168 598 182 606 192" stroke="{LINE}" stroke-width="3" fill="none" opacity=".8"/>'
        f'<circle cx="572" cy="170" r="7" fill="{LINE}"/>'
        f'<path d="M548 150 C530 154 514 164 504 178" stroke="{LINE}" stroke-width="3" fill="none" opacity=".7"/>'
        f'<path d="M300 648 L500 648" stroke="{INK}" stroke-width="8" opacity=".6"/>',
        380, 400, 0.52, 0, -12, 8)


if __name__ == "__main__":
    for name, fn in [("helmet", helmet), ("whale", whale), ("raven", raven)]:
        open(os.path.join(OUT, f"{name}.svg"), "w").write(wrap(fn()))
    print("ok")
