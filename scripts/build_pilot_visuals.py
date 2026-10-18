#!/usr/bin/env python3
"""Build original, deterministic, text-based SVG teaching assets for P-01.

These are actual illustrations, not image specifications. No network, fonts,
AI service, or binary assets are required. Do not hand-edit generated SVGs.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content/A0/assets/p01"
INK = "#203846"
TEAL = "#0f766e"
BLUE = "#3565a0"
ORANGE = "#cf7027"
SKIN = "#e9b58c"
RED = "#b74444"
CREAM = "#fffdf7"


def text(x, y, value, size=34, color=INK, anchor="middle", weight="normal", opacity=1):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" '
            f'font-family="DejaVu Sans, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" opacity="{opacity}">{escape(value)}</text>')


def line(x1, y1, x2, y2, color=INK, width=5, arrow=False, dash=False):
    extra = ' marker-end="url(#arrow)"' if arrow else ""
    extra += ' stroke-dasharray="9 8"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{extra}/>')


def rect(x, y, w, h, fill="white", stroke="#ccd9d9", radius=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'


def circle(x, y, r, fill, stroke="none", width=3):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def bubble(x, y, w, h, value="", tail_x=None, tail_y=None, size=34):
    result = rect(x, y, w, h, "white", TEAL)
    if tail_x is not None:
        mid = min(max(tail_x, x + 30), x + w - 30)
        result += (f'<path d="M {mid-15} {y+h-2} L {tail_x} {tail_y} L {mid+15} {y+h-2}" '
                   f'fill="white" stroke="{TEAL}" stroke-width="3"/>')
    if value:
        result += text(x + w / 2, y + h / 2 + size / 3, value, size)
    return result


def person(x, y, who="Anna", pose="wave", scale=1, name=True, talking=False):
    """A body-based distinction; Anna and Tom are not colour-only cues."""
    c = ORANGE if who == "Anna" else BLUE if who == "Tom" else "#697b82"
    p = '<g>'
    # Feet, torso, head, hair, eyes and expression.
    p += line(-22, 118, -34, 191, INK, 13) + line(22, 118, 43, 191, INK, 13)
    p += rect(-49, 7, 98, 120, c, c, 22)
    if who == "Anna":
        p += '<path d="M 28 -81 Q 106 -108 86 -18 Q 48 -31 28 -81" fill="#583d32"/>'
    p += circle(0, -47, 48, SKIN, INK)
    p += '<path d="M -45 -61 Q -31 -113 18 -91 Q 45 -88 47 -56 Q 6 -66 -14 -80 Q -24 -58 -45 -61" fill="#583d32"/>'
    p += circle(-16, -48, 4, INK) + circle(16, -48, 4, INK)
    if talking:
        p += '<ellipse cx="0" cy="-23" rx="12" ry="8" fill="#8c3c35"/>'
    else:
        p += '<path d="M -13 -25 Q 0 -12 13 -25" fill="none" stroke="#8c3c35" stroke-width="4"/>'
    p += line(-46, 29, -69, 102, c, 17)
    if pose == "wave":
        p += line(46, 29, 81, -18, c, 17) + line(81, -18, 83, -75, SKIN, 13)
        for d in [-9, -3, 3, 9]:
            p += line(83 + d, -74, 82 + d, -96 - (3 - abs(d)) / 2, SKIN, 4)
        p += '<path d="M 104 -84 Q 124 -67 107 -48 M 117 -96 Q 145 -69 123 -41" fill="none" stroke="#8da6ab" stroke-width="4"/>'
    elif pose in ("self", "badge"):
        p += line(46, 29, 74, 65, c, 17) + line(74, 65, 17, 59, SKIN, 13)
        p += line(17, 59, 1, 57, SKIN, 6, True)
    elif pose == "other":
        p += line(46, 29, 88, 52, c, 17) + line(88, 52, 165, 48, SKIN, 13)
        p += line(158, 48, 183, 46, SKIN, 6, True)
    else:
        p += line(46, 29, 67, 102, c, 17)
    if name:
        p += rect(-53, 77, 106, 43, "white", c, 7)
        p += text(0, 106, who, 27)
    p += '</g>'
    return f'<g transform="translate({x} {y}) scale({scale})">{p}</g>'


def eye(x=0, y=0, scale=1):
    p = '<path d="M -39 0 Q 0 -38 39 0 Q 0 38 -39 0" fill="white" stroke="#203846" stroke-width="5"/>'
    p += circle(0, 0, 13, TEAL) + circle(0, 0, 6, INK)
    return f'<g transform="translate({x} {y}) scale({scale})">{p}</g>'


def mouth(x, y, shape="open", scale=1):
    p = ''
    if shape == "closed":
        p += '<path d="M -38 0 Q 0 7 38 0" fill="none" stroke="#a95857" stroke-width="8"/>'
    elif shape == "round":
        p += '<ellipse cx="0" cy="0" rx="17" ry="25" fill="#6d3434" stroke="#c77672" stroke-width="8"/>'
    elif shape == "smile":
        p += '<ellipse cx="0" cy="0" rx="37" ry="11" fill="#6d3434" stroke="#c77672" stroke-width="8"/>'
    elif shape == "tongue":
        p += '<ellipse cx="0" cy="0" rx="30" ry="23" fill="#6d3434" stroke="#c77672" stroke-width="6"/>'
        p += rect(-24, -19, 48, 8, "white", "white", 1)
        p += '<path d="M -10 16 Q -8 -21 9 -10 L 13 16" fill="#ed9a97"/>'
    else:
        p += '<ellipse cx="0" cy="0" rx="30" ry="26" fill="#6d3434" stroke="#c77672" stroke-width="7"/>'
        p += '<path d="M -17 14 Q 0 3 17 14" fill="none" stroke="#ed9a97" stroke-width="7"/>'
    return f'<g transform="translate({x} {y}) scale({scale})">{p}</g>'


def pencil(x, y, scale=1):
    return (f'<g transform="translate({x} {y}) rotate(-35) scale({scale})">'
            '<path d="M -7 -36 L 7 -36 L 7 24 L 0 38 L -7 24 Z" fill="#efb540" stroke="#203846" stroke-width="3"/>'
            '<path d="M -4 30 L 0 38 L 4 30" fill="#203846"/></g>')


def sun(x, y, r=15):
    result = circle(x, y, r, "#f2c15d", "#bd8123", 2)
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        result += line(x + dx * (r+6), y + dy * (r+6), x + dx * (r+12), y + dy * (r+12), "#bd8123", 2)
    return result


def svg(name, title, desc, body, w=1000, h=500, display_width=580):
    OUT.mkdir(parents=True, exist_ok=True)
    value = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{display_width}" height="{round(display_width*h/w)}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/></marker></defs>
<rect width="{w}" height="{h}" rx="20" fill="{CREAM}"/>
{body}
</svg>
'''
    # context-stroke is not supported by some print engines: use the ink colour.
    value = value.replace('fill="context-stroke"', f'fill="{INK}"')
    (OUT / name).write_text(value, encoding="utf-8")


def build_icons():
    svg("see.svg", "See and point", "An eye and a fingertip directed at a visible card.",
        eye(50, 36, .85) + line(50, 63, 50, 86, TEAL, 5, True), 100, 100, 52)
    svg("say.svg", "Speak aloud", "An open mouth with outward sound lines.",
        mouth(39, 50, "open", .7) + line(72, 40, 93, 31, TEAL, 4) + line(74, 50, 96, 50, TEAL, 4) + line(72, 60, 93, 70, TEAL, 4), 100, 100, 52)
    svg("write.svg", "Write or copy", "A pencil makes a line on paper.",
        rect(8, 12, 67, 76) + line(20, 66, 58, 66, INK, 3) + pencil(63, 46, .85), 100, 100, 52)
    svg("select.svg", "Select one answer", "Two circles; only the matching circle is marked.",
        circle(29, 50, 16, "white", INK) + circle(72, 50, 16, TEAL, TEAL) + '<path d="M 60 48 L 69 58 L 85 38" fill="none" stroke="white" stroke-width="5"/>', 100, 100, 52)
    svg("recall.svg", "Cover, recall, then check", "A flap hides a card; a mouth produces the answer before the flap opens.",
        rect(7, 14, 53, 67, "#d9e8e3", TEAL) + '<path d="M 7 14 L 60 14 L 72 4 L 19 4 Z" fill="#b4d1c6" stroke="#0f766e" stroke-width="2"/>' + mouth(77, 65, "open", .4), 100, 100, 52)
    svg("ear.svg", "Hear a helper", "An ear receives sound waves from another speaker.",
        '<path d="M 62 70 Q 38 94 39 62 Q 17 51 27 28 Q 39 4 67 21 Q 88 40 62 70 M 44 39 Q 59 21 66 43 Q 69 57 53 57" fill="none" stroke="#203846" stroke-width="6"/>' + line(3, 25, 14, 32, TEAL, 4) + line(1, 49, 13, 49, TEAL, 4), 100, 100, 52)


def build_actions():
    b = ''
    # The sequence uses shapes, not English instruction words.
    rows = [95, 245, 395, 545, 725]
    for i, y in enumerate(rows, 1):
        b += circle(43, y, 24, TEAL) + text(43, y+10, str(i), 27, "white")
        b += line(95, y, 155, y, TEAL, 5, True)
    b += eye(114, 95, .6) + rect(190, 48, 145, 95) + '<path d="M 240 119 L 263 67 L 286 119 Z" fill="#cf7027"/>'
    b += line(360, 95, 444, 95, TEAL, 5, True) + eye(485, 75, .65) + line(485, 106, 485, 128, TEAL, 4, True) + '<path d="M 533 120 L 557 69 L 581 120 Z" fill="#cf7027"/>'
    # An English-speaking helper supplies the sound; no text pretends to be audio.
    b += mouth(112, 245, "open", .55) + person(238, 248, "Tom", "neutral", .48, False, True)
    b += '<path d="M 278 202 Q 309 221 279 239 M 292 191 Q 337 221 294 250" fill="none" stroke="#0f766e" stroke-width="4"/>'
    b += line(352, 245, 417, 245, TEAL, 5, True) + person(497, 248, "Anna", "neutral", .48, False, True)
    b += '<path d="M 535 203 Q 568 222 536 241" fill="none" stroke="#0f766e" stroke-width="4"/>'
    b += rect(190, 350, 135, 88) + circle(255, 393, 23, "white", INK)
    b += line(352, 395, 417, 395, TEAL, 5, True) + rect(452, 350, 135, 88) + circle(518, 393, 23, "white", INK) + pencil(566, 388, .7)
    b += circle(113, 545, 19, "white", INK) + line(153, 545, 187, 545, TEAL, 4, True)
    b += rect(208, 505, 169, 82) + circle(247, 546, 20, "white", INK) + '<path d="M 302 568 L 322 525 L 343 568 Z" fill="#cf7027"/>'
    b += line(400, 545, 450, 545, TEAL, 4, True) + rect(470, 505, 165, 82) + circle(511, 546, 20, "#c9e2d8", TEAL)
    b += '<path d="M 496 546 L 507 557 L 530 532" fill="none" stroke="#0f766e" stroke-width="5"/><path d="M 562 568 L 582 525 L 603 568 Z" fill="#cf7027"/>'
    b += rect(185, 671, 91, 98) + circle(230, 717, 22, ORANGE)
    b += line(292, 720, 334, 720, TEAL, 4, True) + rect(346, 670, 91, 98, "#d7e4e4", TEAL)
    b += line(450, 720, 486, 720, TEAL, 4, True) + person(532, 721, "Anna", "neutral", .36, False, True)
    b += bubble(570, 652, 75, 58, "", 553, 686) + circle(607, 681, 15, ORANGE)
    b += line(658, 720, 701, 720, TEAL, 4, True) + rect(716, 670, 91, 98) + circle(760, 717, 22, ORANGE)
    b += '<path d="M 832 722 L 849 739 L 881 696" fill="none" stroke="#0f766e" stroke-width="7"/>'
    svg("actions.svg", "Five demonstrated actions", "From top to bottom: see and point at a shape; imitate a helper's spoken sound; copy a shape with a pencil; select the identical shape; hide a card, recall it, then uncover and check. No English instruction word is required.", b, 940, 820, 660)


def build_scenes():
    b = person(210, 230, "Anna", "wave", .85) + person(760, 230, "Tom", "wave", .85)
    b += line(100, 425, 365, 425, TEAL, 7, True) + line(895, 425, 630, 425, TEAL, 7, True)
    b += line(95, 460, 900, 460, "#d5dfdc", 3)
    b += bubble(355, 100, 260, 100, "...", 313, 195, 48)
    svg("meet.svg", "Meeting", "Anna and Tom approach each other with open hands, smiling and waving. Inward motion arrows show the start of a meeting, not departure. Their name badges remain visible.", b)
    b = person(220, 230, "Anna", "wave", .85) + person(680, 230, "Tom", "wave", .85)
    b += rect(849, 100, 112, 300, "#e3edf0", INK, 3) + circle(944, 260, 6, INK)
    b += line(487, 433, 870, 433, TEAL, 8, True) + line(93, 460, 965, 460, "#d5dfdc", 3)
    b += bubble(370, 85, 210, 100, "...", 640, 195, 48)
    svg("leave.svg", "Taking leave", "Tom moves away from Anna towards an exit, waving back. Anna stays and waves. An outward motion arrow and increasing separation distinguish this from the meeting picture.", b)
    for who in ["Anna", "Tom"]:
        b = person(470, 245, who, "self", 1, True, True)
        b += bubble(140, 30, 650, 105, "...", 458, 159, 50)
        svg(f"self-{who.lower()}.svg", f"{who} refers to the speaker", f"Only {who} speaks. The speech bubble points to {who}, and the fingertip points back to the speaker's own chest. The badge identifies the role without testing the name's meaning.", b)
    for speaker, other in [("Anna", "Tom"), ("Tom", "Anna")]:
        b = person(275, 245, speaker, "other", .95, True, True) + person(755, 245, other, "neutral", .95)
        b += bubble(86, 25, 570, 108, "...", 262, 156, 50)
        b += line(474, 271, 638, 271, TEAL, 5, True)
        svg(f"you-{other.lower()}.svg", f"{speaker} addresses {other}", f"The speech bubble belongs to {speaker}. An extended arm points to the listener, {other}. This is the opposite of pointing back to the speaker's own chest.", b)
    b = person(455, 245, "learner", "self", 1, False, True) + rect(404, 322, 103, 43)
    b += line(422, 350, 489, 350, INK, 3) + bubble(130, 25, 650, 108, "...", 449, 158, 50)
    svg("self-learner.svg", "Your own identity", "A neutral learner points to their own chest, with a blank name badge and a speech bubble. Substitute your actual name; a supplied English name can also be used for role-play.", b)
    b = ''
    for y, speaker, other in [(270, "Anna", "Tom"), (730, "Tom", "Anna")]:
        b += person(210, y, speaker, "self", .66, True, True) + person(765, y, other, "neutral", .66)
        b += bubble(350, y-237, 530, 73, f"I am {speaker}.", 240, y-65, 35)
        b += bubble(350, y-147, 530, 73, f"You are {other}.", 251, y-41, 35)
        b += line(295, y+39, 685, y+39, TEAL, 5, True)
    b += line(45, 455, 950, 455, "#d5dfdc", 3)
    svg("roles.svg", "The speaker changes", "Top: Anna speaks and points to herself for I, then towards Tom for you. Bottom: Tom speaks; now I identifies Tom and you identifies Anna. Pronouns follow the speaker, not a permanently assigned person.", b, 1000, 930, 640)


def build_names():
    b = person(220, 236, "Anna", "neutral", .9) + person(750, 236, "Tom", "neutral", .9)
    b += rect(350, 65, 282, 92, "#e3f1eb", TEAL) + text(491, 126, "name", 48)
    b += line(434, 173, 265, 306, TEAL, 5, True) + line(553, 173, 719, 306, TEAL, 5, True)
    svg("name-labels.svg", "A name is the identifying label", "The word name points to the written labels Anna and Tom on badges, not to the whole person or to an object such as a book.", b)
    b = ''
    for y, speaker, other in [(270, "Anna", "Tom"), (730, "Tom", "Anna")]:
        b += person(210, y, speaker, "badge", .67, True, True) + person(775, y, other, "neutral", .67)
        b += bubble(349, y-237, 580, 75, f"My name is {speaker}.", 241, y-64, 36)
        b += bubble(349, y-147, 580, 75, f"Your name is {other}.", 251, y-40, 36)
        b += line(303, y+56, 696, y+56, TEAL, 5, True)
    b += line(45, 455, 950, 455, "#d5dfdc", 3)
    svg("ownership.svg", "My name and your name change with the speaker", "Anna indicates her own name badge for my name and Tom's name badge for your name. When Tom speaks, the arrows reverse. My and your are taught only with name in this lesson.", b, 1000, 930, 650)
    for filename, speaker, target in [("my-anna.svg", "Anna", "Anna"), ("your-tom.svg", "Anna", "Tom")]:
        b = person(255, 240, speaker, "badge" if target == speaker else "other", .94, True, True)
        b += person(770, 240, "Tom", "neutral", .94)
        badge_x = 255 if target == speaker else 770
        b += f'<ellipse cx="{badge_x}" cy="332" rx="61" ry="29" fill="none" stroke="{TEAL}" stroke-width="6"/>'
        b += bubble(74, 25, 600, 105, "...", 240, 155, 50)
        if target != speaker:
            b += line(475, 287, 696, 328, TEAL, 5, True)
        svg(filename, f"{speaker} refers to {target}'s name label", f"{speaker} is the speaker. A ring and the pointing gesture pick out the name badge belonging to {target}. No possessive word is printed in this retrieval prompt.", b)
    b = ''
    for i, (old, new) in enumerate([("I am Anna.", "My name is Anna."), ("You are Tom.", "Your name is Tom.")]):
        y = 105 + i*210
        b += rect(25, y-53, 380, 112) + text(215, y+17, old, 36)
        b += line(430, y, 536, y, TEAL, 5, True)
        b += rect(563, y-53, 410, 112, "#e3f1eb", TEAL) + text(770, y+17, new, 36)
    svg("name-frames.svg", "Two ways to identify the same person", "I am Anna and My name is Anna refer to the same speaker. You are Tom and Your name is Tom refer to the same listener. The frame uses is after name, not am or are.", b, 1000, 460, 650)
    b = person(190, 230, "Anna", "other", .72, True, True) + person(795, 230, "Tom", "neutral", .72, False)
    b += rect(758, 285, 76, 40, "#d9e4e7", INK, 5) + text(796, 316, "?", 28)
    b += bubble(315, 28, 650, 90, "What is your name?", 221, 161, 43)
    b += line(240, 438, 744, 438, TEAL, 7, True)
    b += person(190, 665, "Anna", "neutral", .72, True) + person(795, 665, "Tom", "badge", .72, True, True)
    b += bubble(315, 469, 650, 90, "My name is Tom.", 781, 598, 43)
    b += '<path d="M 855 785 L 931 785 L 955 764 L 880 764 Z" fill="#c4d9dc" stroke="#203846" stroke-width="2"/>'
    svg("question.svg", "Ask for a hidden name; receive the name", "The listener's name label is covered. Anna asks What is your name? In the second scene Tom gives My name is Tom and reveals the badge. The information gap supplies the meaning of the fixed question.", b, 1000, 885, 650)
    b = person(250, 240, "Anna", "other", .94, True, True) + person(770, 240, "learner", "neutral", .94, False)
    b += rect(719, 314, 104, 43, "#d9e4e7", INK, 6) + text(770, 347, "?", 32)
    b += bubble(70, 25, 610, 108, "?", 235, 155, 50)
    svg("question-prompt.svg", "Ask for the hidden name", "The speaker faces a person whose name badge is covered by a question mark. The speech bubble contains no model English sentence, so the learner retrieves the name question rather than reading it.", b)


def build_sounds():
    # The IPA is an optional reference, not a prerequisite or a tested skill.
    sets = {
        "l01": [
            ("hello", "/həˈləʊ/", ["open", "tongue", "round"], 2),
            ("hi", "/haɪ/", ["open", "smile"], 1),
            ("goodbye", "/ˌɡʊdˈbaɪ/", ["closed", "open", "smile"], 2),
            ("bye", "/baɪ/", ["closed", "open", "smile"], 1),
            ("I", "/aɪ/", ["open", "smile"], 1),
            ("you", "/juː/", ["smile", "round"], 1),
            ("am", "/æm/", ["open", "closed"], 1),
            ("are", "/ɑː/", ["open"], 1),
        ],
        "l02": [
            ("name", "/neɪm/", ["tongue", "smile", "closed"], 1),
            ("my", "/maɪ/", ["closed", "open", "smile"], 1),
            ("your", "/jɔː/", ["smile", "round"], 1),
            ("is", "/ɪz/", ["smile", "smile"], 1),
            ("what", "/wɒt/", ["round", "open", "tongue"], 1),
        ],
    }
    for name, items in sets.items():
        b = ''
        for i, (word, ipa, shapes, beats) in enumerate(items):
            y = i*135 + 75
            b += text(145, y-6, word, 40, anchor="middle", weight="bold")
            b += text(145, y+34, ipa, 27, anchor="middle")
            if beats == 2:
                b += circle(300, y, 7, TEAL) + circle(333, y, 15, TEAL)
            else:
                b += circle(319, y, 14, TEAL)
            for j, shape in enumerate(shapes):
                x = 435 + j*180
                b += mouth(x, y, shape, 1)
                if j+1 < len(shapes):
                    b += line(x+60, y, x+115, y, TEAL, 4, True)
            if word == "goodbye":
                b += text(407, y-43, "/ɡʊd/ → /b/", 22)
            if word in ["you", "your", "are"]:
                b += line(841, y, 946, y, TEAL, 4, True)
            if word == "is":
                # A hand at the throat and vibration marks model voiced final /z/.
                b += circle(883, y-20, 19, SKIN, INK, 2) + line(883, y+1, 883, y+33, INK, 6)
                b += line(910, y+24, 885, y+17, SKIN, 10)
                b += '<path d="M 842 '+str(y+3)+' l -9 8 l 9 8 l -9 8" fill="none" stroke="#0f766e" stroke-width="3"/>'
            if i+1 < len(items):
                b += line(25, y+65, 975, y+65, "#dde5e0", 2)
        svg(f"sounds-{name}.svg", "Visual mouth and rhythm guidance", "Each row links a taught word to mouth positions in time order. Closed lips contrast with an open mouth; the raised tongue touches behind the upper teeth for the relevant consonant; rounded lips show the rounding movement. Small then large dots indicate a weak then strong beat in hello and goodbye. A long arrow extends the vowel. For is, a hand and vibration marks show final voiced z. IPA is optional helper reference; the diagrams do not replace hearing a competent model. This file contains no recording.", b, 1000, len(items)*135+20, 660)


def build_practice():
    for name, sentence in [("l01", "I am Anna."), ("l02", "My name is Anna.")]:
        b = text(495, 90, sentence, 62)
        b += line(490, 125, 490, 165, TEAL, 5, True)
        b += text(495, 245, sentence, 62, opacity=.25) + pencil(850, 219, 1)
        b += line(490, 284, 490, 329, TEAL, 5, True)
        b += line(140, 426, 850, 426, INK, 3) + pencil(850, 390, 1)
        svg(f"writing-{name}.svg", "Model, trace, copy", "A clear model appears first; the same line is pale for tracing; then a blank line and a pencil invite copying. Letter names are not required for tracing the shown shapes.", b, 1000, 470, 650)
    b = person(145, 240, "Tom", "neutral", .7, True, True)
    b += rect(217, 240, 74, 70, "white", INK, 4) + line(228, 258, 277, 258, INK, 2) + line(228, 274, 277, 274, INK, 2)
    b += '<path d="M 224 157 Q 263 179 224 198 M 239 145 Q 288 178 241 210" fill="none" stroke="#0f766e" stroke-width="5"/>'
    b += line(323, 195, 401, 195, TEAL, 6, True) + person(520, 240, "Anna", "neutral", .7, True)
    b += '<path d="M 453 180 Q 432 160 442 137 Q 453 119 471 132 Q 488 145 473 164 L 463 182" fill="none" stroke="#203846" stroke-width="5"/>'
    b += line(650, 195, 735, 195, TEAL, 6, True)
    b += rect(771, 126, 145, 139) + circle(807, 163, 11, "white", INK) + circle(807, 215, 11, TEAL, TEAL)
    b += '<path d="M 798 214 L 806 224 L 821 203" fill="none" stroke="white" stroke-width="4"/>'
    svg("helper-listening.svg", "A helper reads; the learner hears then responds", "An English-speaking helper reads the script without showing the text, the learner receives the sound, then selects a response. With no helper and no recording this activity cannot supply listening evidence; its text can only be read as rehearsal.", b, 1000, 430, 640)
    b = sun(90, 110, 30) + '<path d="M 149 130 Q 190 64 230 130" fill="none" stroke="#0f766e" stroke-width="5" marker-end="url(#arrow)"/>'
    b += circle(287, 109, 30, "#dae2f2", BLUE) + circle(300, 98, 28, CREAM)
    b += '<path d="M 345 130 Q 385 64 428 130" fill="none" stroke="#0f766e" stroke-width="5" marker-end="url(#arrow)"/>' + sun(484, 110, 30)
    b += text(705, 126, "+1", 57) + line(553, 110, 620, 110, TEAL, 5, True)
    b += text(80, 260, "✓", 55, TEAL)
    positions = [(190, "+1"), (345, "+3"), (500, "+7"), (655, "+21"), (830, "+60")]
    for i, (x, value) in enumerate(positions):
        b += rect(x-52, 211, 110, 72, "#e3f1eb", TEAL) + text(x+3, 258, value, 36)
        if i < len(positions)-1:
            b += line(x+68, 246, positions[i+1][0]-63, 246, TEAL, 4, True)
    b += text(150, 373, "✗", 54, RED) + line(196, 357, 411, 357, RED, 5, True) + text(490, 375, "+1", 54, RED)
    svg("review-cycle.svg", "Adaptive day intervals", "Sun, moon, sun show one day without requiring the English word day. After each successful retrieval the next interval is one, three, seven, twenty-one, then sixty days from that success. Any unsuccessful retrieval returns to a one-day interval. These are scheduling symbols, not vocabulary targets.", b, 1000, 430, 650)


def main():
    build_icons()
    build_actions()
    build_scenes()
    build_names()
    build_sounds()
    build_practice()
    files = sorted(OUT.glob("*.svg"))
    print(f"Built {len(files)} original SVG teaching assets in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
