#!/usr/bin/env python3
"""Kopplingsöversikt för AndreasM TransponderV3.

Samma färger och ledningsnummer [n] som KiCad-schemat.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[1]
SVG_PATH = OUT_DIR / "schema_oversikt.svg"
PNG_PATH = OUT_DIR / "schema_oversikt.png"

W, H = 1600, 1180
FONT = "IBM Plex Sans, Helvetica Neue, Arial, sans-serif"
MONO = "IBM Plex Mono, Menlo, Consolas, monospace"
INK = "#1f2937"
PAPER = "#fffef9"
BG = "#ece7dc"
MUTED = "#6b7280"

C_VIN = "#b45309"
C_5V = "#1d4ed8"
C_GND = "#374151"
C_OSC = "#0e7490"
C_LED = "#a21caf"
C_TX = "#15803d"
C_ICSP = "#4338ca"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class Svg:
    def __init__(self):
        self.parts: list[str] = []

    def add(self, s: str) -> None:
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, stroke=INK, sw=2.0, rx=8):
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, s, size=13, fill=INK, weight="400", anchor="start", mono=False, rotate=0):
        ff = MONO if mono else FONT
        tf = f' transform="rotate({rotate} {x} {y})"' if rotate else ""
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-family="{ff}" '
            f'font-size="{size}" font-weight="{weight}"{tf}>{esc(s)}</text>'
        )

    def path(self, d, color, width=3.0):
        self.add(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def dot(self, x, y, color=INK, r=4.5):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')

    def build(self) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            + "\n".join(self.parts)
            + "\n</svg>\n"
        )


s = Svg()


def wire(color, *pts, width=3.0):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    s.path(d, color, width)


def badge(n, x, y, color):
    label = str(n)
    w = 10 + 8 * len(label)
    s.rect(x - w / 2, y - 9, w, 18, PAPER, color, 1.8, 9)
    s.text(x, y + 4, label, 11, color, "700", "middle", mono=True)


def gnd(x, y, n=None):
    s.path(f"M{x},{y} V{y + 14}", C_GND, 2.4)
    for i, half in enumerate((11, 7, 3)):
        yy = y + 14 + i * 4
        s.path(f"M{x - half},{yy} H{x + half}", C_GND, 2.2)
    if n is not None:
        badge(n, x + 26, y + 18, C_GND)


class Box:
    def __init__(self, x, y, w, h, title, color, sub=""):
        self.x, self.y, self.w, self.h, self.color = x, y, w, h, color
        s.rect(x, y, w, h, PAPER, INK, 2.0, 10)
        s.rect(x, y, w, 26, color, color, 0, 10)
        s.rect(x, y + 14, w, 12, color, color, 0, 0)
        s.text(x + w / 2, y + 18, title, 13, PAPER, "700", "middle")
        if sub:
            s.text(x + w / 2, y + h - 9, sub, 11, MUTED, "400", "middle")

    def left(self, name, y):
        s.dot(self.x, y, self.color)
        s.text(self.x + 10, y + 4, name, 12, INK, "600", mono=True)
        return (self.x, y)

    def right(self, name, y):
        s.dot(self.x + self.w, y, self.color)
        s.text(self.x + self.w - 10, y + 4, name, 12, INK, "600", "end", mono=True)
        return (self.x + self.w, y)

    def top(self, name, x):
        s.dot(x, self.y, self.color)
        s.text(x, self.y + 42, name, 12, INK, "600", "middle", mono=True)
        return (x, self.y)

    def bottom(self, name, x):
        s.dot(x, self.y + self.h, self.color)
        s.text(x, self.y + self.h - 10, name, 12, INK, "600", "middle", mono=True)
        return (x, self.y + self.h)


def resistor(x, y_top, ref, value, color):
    s.rect(x - 8, y_top + 8, 16, 34, PAPER, color, 2.2, 3)
    s.path(f"M{x},{y_top} V{y_top + 8} M{x},{y_top + 42} V{y_top + 50}", color, 2.4)
    s.text(x + 16, y_top + 22, ref, 12, INK, "700")
    s.text(x + 16, y_top + 37, value, 12, MUTED, "400")
    return (x, y_top), (x, y_top + 50)


def capacitor(x, y_top, ref, value, color):
    s.path(f"M{x},{y_top} V{y_top + 16} M{x},{y_top + 24} V{y_top + 40}", color, 2.4)
    s.path(f"M{x - 12},{y_top + 16} H{x + 12}", color, 3.2)
    s.path(f"M{x - 12},{y_top + 24} H{x + 12}", color, 3.2)
    s.text(x + 18, y_top + 17, ref, 12, INK, "700")
    s.text(x + 18, y_top + 32, value, 12, MUTED, "400")
    return (x, y_top), (x, y_top + 40)


def resistor_h(x_left, y, ref, value, color):
    s.path(f"M{x_left},{y} H{x_left + 8} M{x_left + 48},{y} H{x_left + 56}", color, 2.4)
    s.rect(x_left + 8, y - 8, 40, 16, PAPER, color, 2.2, 3)
    s.text(x_left + 28, y - 16, f"{ref}  {value}", 12, INK, "700", "middle")
    return (x_left, y), (x_left + 56, y)


def capacitor_h(x_left, y, ref, value, color):
    s.path(f"M{x_left},{y} H{x_left + 14}", color, 2.4)
    s.path(f"M{x_left + 14},{y - 12} V{y + 12}", color, 3.2)
    s.path(f"M{x_left + 22},{y - 12} V{y + 12}", color, 3.2)
    s.path(f"M{x_left + 22},{y} H{x_left + 36}", color, 2.4)
    s.text(x_left + 18, y - 18, f"{ref}  {value}", 12, INK, "700", "middle")
    return (x_left, y), (x_left + 36, y)


def draw() -> str:
    s.add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.rect(0, 0, W, 78, INK, INK, 0, 0)
    s.text(40, 34, "AndreasM TransponderV3 — kopplingsöversikt", 26, "#f9fafb", "700")
    s.text(
        40,
        58,
        "Varje färgad linje = en ledning  ·  [n] = nummer, samma som i KiCad-schemat  ·  "
        "OSH Park 4-lager, 5 V  ·  Ingen backspänningsskydd",
        14,
        "#d1d5db",
    )
    legend = [
        (C_VIN, "VIN 6,0–8,4 V"),
        (C_5V, "+5 V"),
        (C_GND, "GND"),
        (C_OSC, "Kristall"),
        (C_LED, "LED"),
        (C_TX, "TX / antenn"),
        (C_ICSP, "ICSP"),
    ]
    for i, (col, name) in enumerate(legend):
        lx = 40 + i * 220
        s.path(f"M{lx},102 H{lx + 26}", col, 4)
        s.text(lx + 33, 106, name, 11, "#374151", "600", mono=True)

    Y_VIN, Y_5V = 178, 236

    bat = Box(48, 268, 150, 96, "Batteri J1", C_VIN, "2S LiPo / 4× AAA")
    bp = bat.top("+", 123)
    bm = bat.bottom("−", 123)

    ldo = Box(370, 148, 200, 112, "U1 MCP1702", C_5V, "LDO 5,0 V  ·  SOT-23")
    vin = ldo.left("VIN 1", 204)
    vout = ldo.right("VOUT 3", 204)
    lgnd = ldo.bottom("GND 2", 470)

    wire(C_VIN, bp, (123, Y_VIN), (370, Y_VIN), (370, 204), vin, width=4.0)
    badge(1, 250, Y_VIN, C_VIN)
    gnd(*bm, n=2)
    c1t, c1b = capacitor(270, 200, "C1", "10 µF", C_VIN)
    wire(C_VIN, (270, Y_VIN), c1t)
    s.dot(270, Y_VIN, C_VIN)
    gnd(*c1b)
    badge(3, 270, 190, C_VIN)
    gnd(*lgnd, n=5)

    wire(C_5V, vout, (570, 204), (570, Y_5V), (1540, Y_5V), width=4.0)
    badge(4, 600, 204, C_5V)
    s.text(820, Y_5V - 14, "+5 V-skena", 13, C_5V, "700")
    c2t, c2b = capacitor(610, 250, "C2", "10 µF", C_5V)
    wire(C_5V, (610, Y_5V), c2t)
    s.dot(610, Y_5V, C_5V)
    gnd(*c2b)

    pic = Box(640, 292, 250, 268, "U2 PIC16F18313", C_5V, "SOIC-8")
    p_vdd = pic.top("VDD 1", 765)
    ra5 = pic.left("RA5 2", 360)
    ra4 = pic.left("RA4 3", 414)
    mclr = pic.left("MCLR 4", 500)
    ra0 = pic.right("RA0 7", 360)
    ra1 = pic.right("RA1 6", 414)
    ra2 = pic.right("RA2 5", 478)
    p_vss = pic.bottom("VSS 8", 830)

    wire(C_5V, (765, Y_5V), p_vdd)
    s.dot(765, Y_5V, C_5V)
    badge(6, 765, 258, C_5V)
    gnd(*p_vss, n=7)

    s.rect(458, 336, 118, 50, PAPER, C_OSC, 2.0, 8)
    s.text(517, 356, "Y1", 13, INK, "700", "middle")
    s.text(517, 374, "5,000 MHz", 11, MUTED, "400", "middle")
    y1l, y1r = (458, 361), (576, 361)
    s.dot(*y1l, C_OSC)
    s.dot(*y1r, C_OSC)
    c3t, c3b = capacitor(458, 410, "C3", "20 pF", C_OSC)
    c4t, c4b = capacitor(576, 410, "C4", "20 pF", C_OSC)
    wire(C_OSC, ra5, (458, 360), y1l)
    wire(C_OSC, ra4, (576, 414), y1r)
    badge(8, 458, 338, C_OSC)
    badge(9, 598, 400, C_OSC)
    wire(C_OSC, y1l, c3t)
    wire(C_OSC, y1r, c4t)
    s.dot(*y1l, C_OSC)
    s.dot(*y1r, C_OSC)
    gnd(*c3b)
    gnd(*c4b)

    s.rect(980, 456, 52, 38, PAPER, C_LED, 2.0, 6)
    s.text(1006, 479, "D1", 13, INK, "700", "middle")
    d1t, d1b = (1006, 456), (1006, 494)
    s.dot(*d1t, C_LED)
    s.dot(*d1b, C_LED)
    r1t, r1b = resistor(1006, 494, "R1", "1k5", C_LED)
    wire(C_LED, ra2, (1006, 478), d1t)
    badge(10, 940, 478, C_LED)
    gnd(*r1b, n=11)

    r2t, r2b = resistor_h(930, 360, "R2", "100 Ω", C_TX)
    r3t, r3b = resistor_h(930, 414, "R3", "100 Ω", C_TX)
    wire(C_TX, ra0, r2t)
    wire(C_TX, ra1, r3t)
    badge(12, 910, 348, C_TX)
    badge(13, 910, 432, C_TX)

    c6t, c6b = capacitor_h(1006, 360, "C6", "47 pF", C_TX)
    wire(C_TX, r2b, c6t)
    ant = Box(1220, 308, 170, 130, "AE1 PCB-slinga", C_TX, "undersidan")
    a1 = ant.left("1", 360)
    a2 = ant.left("2", 414)
    wire(C_TX, c6b, a1)
    badge(14, 1140, 348, C_TX)
    wire(C_TX, r3b, a2)
    badge(15, 1140, 432, C_TX)
    s.dot(1100, 360, C_TX)
    c5t, c5b = capacitor(1100, 370, "C5", "150 pF", C_TX)
    wire(C_TX, (1100, 360), c5t)
    wire(C_TX, c5b, (1100, 414), a2)
    s.dot(1100, 414, C_TX)

    prog = Box(640, 680, 380, 78, "J2 ICSP  ·  VPP CLK DAT +V GND", C_ICSP)
    vpp = prog.top("VPP", 680)
    pv = prog.top("+V", 735)
    clk = prog.top("CLK", 800)
    dat = prog.top("DAT", 870)
    pg = prog.right("GND", 718)

    wire(C_ICSP, vpp, (680, 640), (580, 640), (580, 500), mclr)
    badge(16, 580, 560, C_ICSP)
    wire(C_5V, pv, (735, 620), (610, 620), (610, Y_5V))
    s.dot(610, Y_5V, C_5V)
    badge(19, 670, 620, C_5V)
    wire(C_ICSP, clk, (800, 650), (910, 650), (910, 414), ra1)
    badge(17, 850, 650, C_ICSP)
    s.dot(910, 414, C_ICSP)
    wire(C_ICSP, dat, (870, 662), (900, 662), (900, 360), ra0)
    badge(18, 885, 662, C_ICSP)
    s.dot(900, 360, C_ICSP)
    gnd(*pg, n=20)

    s.text(48, 430, "Alla GND-symboler = samma jordskena.", 13, C_GND, "700")
    s.text(48, 450, "Plus till J1+, minus till GND.", 13, C_GND, "400")
    s.text(48, 478, "Ingen MOSFET. Fel polaritet tar LDO och PIC.", 13, "#991b1b", "700")
    s.text(48, 506, "C5: 150 pF i ordern (~130 pF i schemat).", 13, INK, "400")
    s.text(48, 524, "100 pF i reserv om räckvidden är dålig.", 13, INK, "400")
    s.text(48, 552, "Täck inte slingan med metall eller batteri.", 13, MUTED, "400")

    rows = [
        ("1", C_VIN, "VIN", "J1+ → U1 VIN", "6,0–8,4 V. Inte 1S / USB 5 V"),
        ("2", C_GND, "GND", "J1− → jordskena", "stjärnpunkt"),
        ("3", C_VIN, "VIN", "VIN → C1 10 µF", "keramisk, ingen polaritet"),
        ("4", C_5V, "+5V", "U1 VOUT → +5 V-skena", "C2 10 µF, PIC VDD, J2 +V"),
        ("5", C_GND, "GND", "U1 GND → jord", "SOT-23 ben 2"),
        ("6", C_5V, "+5V", "+5 V → PIC VDD", "ben 1"),
        ("7", C_GND, "GND", "PIC VSS → jord", "ben 8"),
        ("8", C_OSC, "OSC", "RA5 → Y1 / C3", "5 MHz, C3 20 pF till jord"),
        ("9", C_OSC, "OSC", "RA4 → Y1 / C4", "C4 20 pF till jord"),
        ("10", C_LED, "LED", "RA2 → D1 anod", "katodstreck mot R1"),
        ("11", C_LED, "LED", "D1 → R1 1k5 → jord", "1206 röd"),
        ("12", C_TX, "TX", "RA0 → R2 100 Ω", "också ICSP DAT"),
        ("13", C_TX, "TX", "RA1 → R3 100 Ω", "också ICSP CLK"),
        ("14", C_TX, "ANT", "R2 → C6 47 pF → slinga", "serie mot antennen"),
        ("15", C_TX, "ANT", "R3 → slinga, C5 150 pF", "avstämning, prova 100 pF"),
        ("16", C_ICSP, "VPP", "J2 VPP → MCLR/RA3", "programmering"),
        ("17", C_ICSP, "CLK", "J2 CLK → RA1", "ICSPCLK"),
        ("18", C_ICSP, "DAT", "J2 DAT → RA0", "ICSPDAT"),
        ("19", C_5V, "+5V", "J2 +V → +5 V", "mata PIC vid programmering"),
        ("20", C_GND, "GND", "J2 GND → jord", "Detect = 3066"),
    ]
    TY = 800
    s.rect(40, TY, 1520, 340, PAPER, INK, 2, 12)
    s.rect(40, TY, 1520, 36, INK, INK, 0, 12)
    s.rect(40, TY + 18, 1520, 18, INK, INK, 0, 0)
    s.text(800, TY + 24, "Ledningslista — TransponderV3", 16, "#f9fafb", "700", "middle")
    half = (len(rows) + 1) // 2
    for col, ox in enumerate((60, 820)):
        s.text(ox, TY + 60, "#", 12, MUTED, "700", mono=True)
        s.text(ox + 44, TY + 60, "Net", 12, MUTED, "700", mono=True)
        s.text(ox + 140, TY + 60, "Från → Till", 12, MUTED, "700")
        s.text(ox + 400, TY + 60, "Tips", 12, MUTED, "700")
        for i, (n, colr, net, route, tip) in enumerate(rows[col * half : (col + 1) * half]):
            y = TY + 86 + i * 26
            s.rect(ox - 4, y - 12, 34, 17, colr, colr, 0, 4)
            s.text(ox + 13, y + 1, n, 11, PAPER, "700", "middle", mono=True)
            s.text(ox + 44, y + 1, net, 11, colr, "700", mono=True)
            s.text(ox + 140, y + 1, route, 12, INK, "400")
            s.text(ox + 400, y + 1, tip, 11, MUTED, "400")

    s.text(
        40,
        H - 24,
        "CyclingHourglass  ·  KiCad: Schematic/Transponder/TransponderV3.kicad_pro  ·  "
        "Genereras av scripts/generate_schema_oversikt.py",
        12,
        MUTED,
    )
    return s.build()


def svg_to_png(svg_path: Path, png_path: Path) -> None:
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if chrome.exists():
        html = svg_path.with_suffix(".html")
        html.write_text(
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<style>html,body{{margin:0;background:{BG}}}</style></head><body>"
            + svg_path.read_text(encoding="utf-8")
            + "</body></html>",
            encoding="utf-8",
        )
        subprocess.run(
            [
                str(chrome),
                "--headless=new",
                "--disable-gpu",
                f"--screenshot={png_path}",
                f"--window-size={W},{H}",
                "--default-background-color=00000000",
                f"file://{html}",
            ],
            check=True,
            capture_output=True,
        )
        html.unlink(missing_ok=True)
        return
    subprocess.run(
        ["qlmanage", "-t", "-s", str(max(W, H)), "-o", str(png_path.parent), str(svg_path)],
        check=True,
        capture_output=True,
    )
    produced = png_path.parent / (svg_path.name + ".png")
    if produced.exists() and produced != png_path:
        produced.rename(png_path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(draw(), encoding="utf-8")
    print(f"Wrote {SVG_PATH}")
    svg_to_png(SVG_PATH, PNG_PATH)
    print(f"Wrote {PNG_PATH}")


if __name__ == "__main__":
    main()
