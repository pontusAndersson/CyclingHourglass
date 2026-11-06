#!/usr/bin/env python3
"""Kopplingsöversikt för RCHourglass decoder PDIA + CY8CKIT-059."""

from pathlib import Path

from svglib import (
    C_5V,
    C_GND,
    C_ICSP,
    C_OSC,
    C_TX,
    C_VIN,
    INK,
    Box,
    Svg,
    badge,
    capacitor,
    gnd,
    header,
    resistor,
    resistor_h,
    svg_to_png,
    table,
    wire,
)

OUT = Path(__file__).resolve().parents[1]
W, H = 1600, 1180


def draw() -> str:
    s = Svg(W, H)
    header(
        s,
        "RCHourglass Decoder — kopplingsöversikt",
        "Varje färgad linje = en ledning  ·  [n] = nummer, samma som i KiCad  ·  "
        "Cano PDIA + CY8CKIT-059  ·  Wiki-bygget",
        [
            (C_VIN, "Phantom / bias"),
            (C_5V, "+5 V"),
            (C_GND, "GND"),
            (C_TX, "RF / analog ut"),
            (C_ICSP, "PSoC"),
            (C_OSC, "Kristall 5 MHz"),
        ],
    )

    j1 = Box(s, 48, 220, 170, 100, "J1  från loop amp", C_VIN, "75 Ω F  ·  phantom")
    sig = j1.right("center", 258)
    sh = j1.bottom("skärm", 130)
    r1a, r1b = resistor_h(s, 250, 188, "R1", "75 Ω", C_VIN)
    wire(s, C_VIN, sig, (250, 258), (250, 188), r1a)
    badge(s, 1, 230, 230, C_VIN)
    wire(s, C_5V, r1b, (320, 188), (320, 160), (1540, 160), width=4)
    s.dot(320, 160, C_5V)
    s.text(500, 146, "+5 V-skena  (USB / VDDIO)", 13, C_5V, "700")
    gnd(s, *sh, n=2)

    q5 = Box(s, 360, 200, 180, 110, "Q5  2N3906", C_VIN, "3,7 V  TP1/TP2")
    q5e = q5.top("E R7 1k21", 430)
    q5c = q5.bottom("C R8 10k", 450)
    wire(s, C_5V, (430, 160), q5e)
    s.dot(430, 160, C_5V)
    badge(s, 3, 430, 188, C_VIN)
    gnd(s, *q5c)
    s.text(560, 280, "C3 100 nF mot +5 V", 12, C_VIN, "400")

    pair = Box(s, 360, 360, 280, 160, "Q1 / Q2  2N3906", C_TX, "PNP-par  ·  R2 100 Ω till +5 V")
    q1b = pair.left("Q1 B  C1 47 pF", 420)
    q2b = pair.right("Q2 B  C2 470 pF", 420)
    q1c = pair.bottom("Q1 C", 430)
    q2c = pair.bottom("Q2 C = ut", 560)
    et = pair.top("E", 500)
    wire(s, C_5V, (500, 160), et)
    s.dot(500, 160, C_5V)
    badge(s, 5, 500, 188, C_5V)
    wire(s, C_TX, sig, (250, 258), (250, 420), q1b)
    badge(s, 4, 250, 360, C_TX)
    wire(s, C_VIN, (450, 310), (300, 310), (300, 420), q1b)
    badge(s, 6, 300, 390, C_VIN)
    s.text(300, 448, "R5 1k00", 12, C_VIN, "400")
    s.text(660, 408, "R6 1k00", 12, C_VIN, "400")

    bot = Box(s, 360, 580, 280, 110, "Q3 / Q4  2N3904", C_TX, "NPN  ·  R3/R4 200 Ω")
    q3c = bot.top("Q3 C", 430)
    q4c = bot.top("Q4 C", 560)
    qe = bot.bottom("E", 500)
    wire(s, C_TX, q1c, q3c)
    wire(s, C_TX, q2c, q4c)
    badge(s, 7, 430, 560, C_TX)
    gnd(s, *qe)
    s.text(560, 700, "TP10/11 ~0,39 V   TP9 ~1,05 V", 12, C_TX, "400")

    r9a, r9b = resistor_h(s, 680, 640, "R9", "2k00", C_TX)
    wire(s, C_5V, (736, 160), (736, 640), r9a)
    s.dot(736, 160, C_5V)
    wire(s, C_TX, q4c, (560, 640), r9a)
    badge(s, 8, 640, 628, C_TX)
    r10t, r10b = resistor(s, 800, 640, "R10", "2k00", C_GND)
    wire(s, C_TX, r9b, r10t)
    gnd(s, *r10b)
    s.text(820, 628, "TP8 ~1,87 V", 12, C_TX, "700")

    psoc = Box(s, 980, 300, 280, 260, "U1  CY8CKIT-059", C_ICSP, "PSoC 5LP  ·  räkna stift på listen")
    p12_2 = psoc.left("P12_2 analog in", 420)
    p12_3 = psoc.left("P12_3 hysteres", 480)
    vdd = psoc.top("VDDIO", 1080)
    gndp = psoc.bottom("GND", 1080)
    p150 = psoc.right("P15_0", 400)
    p151 = psoc.right("P15_1", 460)
    wire(s, C_ICSP, r9b, (920, 640), (920, 420), p12_2)
    badge(s, 9, 900, 420, C_ICSP)
    r11a, r11b = resistor_h(s, 820, 480, "R11", "4k87", C_ICSP)
    wire(s, C_ICSP, p12_3, r11b)
    wire(s, C_ICSP, r11a, (820, 420), (920, 420))
    badge(s, 10, 800, 468, C_ICSP)
    wire(s, C_5V, (1080, 160), vdd)
    s.dot(1080, 160, C_5V)
    badge(s, 11, 1080, 188, C_5V)
    gnd(s, *gndp, n=12)

    xtal = Box(s, 1320, 360, 160, 100, "Y1  5,000 MHz", C_OSC, "C4/C5 22 pF")
    y1 = xtal.left("1", 400)
    y2 = xtal.left("2", 460)
    wire(s, C_OSC, p150, y1)
    wire(s, C_OSC, p151, y2)
    badge(s, 13, 1290, 400, C_OSC)
    badge(s, 14, 1290, 460, C_OSC)

    s.text(48, 760, "F-chassi jordas till kretsjord (wiki: vit tråd till R8).", 13, C_GND, "700")
    s.text(48, 782, "Q1 Q2 Q5 = 2N3906 PNP. Q3 Q4 = 2N3904 NPN.", 13, INK, "400")
    s.text(48, 804, "Kristall på P15_0 / P15_1, inte kitets XTAL-silk.", 13, INK, "400")
    s.text(48, 826, "LED, piezo och PIC-prog är valfria. Se original PDF Rev 2.", 13, "#6b7280", "400")

    rows = [
        ("1", C_VIN, "PHAN", "J1 center → R1 75 Ω → +5 V", "phantom till loop amp"),
        ("2", C_GND, "GND", "J1 skärm → jord", "måste sitta i kretsjord"),
        ("3", C_VIN, "BIAS", "R7 → Q5 E, C3 100 n, R8 10k", "TP1/TP2 ~3,7 V"),
        ("4", C_TX, "RF", "J1 → C1 47 pF → Q1 bas", "TP7 ~3,96 V"),
        ("5", C_5V, "+5V", "R2 100 Ω → Q1/Q2 E", "PNP-svans mot +5 V"),
        ("6", C_VIN, "BIAS", "3,7 V → R5/R6 1k → baser", "TP6/TP5 ~3,7 V"),
        ("7", C_TX, "RF", "Q1 C → Q3, Q2 C → Q4", "strömsspegel, TP9 ~1,05 V"),
        ("8", C_TX, "UT", "Q4 C → R9 2k / R10 2k", "TP8 ~1,87 V utan PSoC"),
        ("9", C_ICSP, "P12", "analog ut → P12_2", "räkna stift, silk är förskjuten"),
        ("10", C_ICSP, "P12", "P12_3 → R11 4k87 → P12_2", "hysteres"),
        ("11", C_5V, "+5V", "+5 V → VDDIO", "inte bara USB till kitprog"),
        ("12", C_GND, "GND", "nedre PSoC-GND → jord", "4 kΩ Vcc–GND med PSoC ur"),
        ("13", C_OSC, "OSC", "P15_0 / P15_1 → Y1", "bästa 5 MHz-kristallen här"),
        ("14", C_OSC, "OSC", "C4 C5 22 pF till jord", "inte 8 MHz"),
    ]
    table(s, rows, 860, "Ledningslista — Decoder PDIA")
    s.text(
        40,
        H - 24,
        "CyclingHourglass  ·  KiCad: Schematic/Decoder/Decoder.kicad_pro  ·  "
        "scripts/generate_decoder_oversikt.py",
        12,
        "#6b7280",
    )
    return s.build()


def main() -> None:
    svg = OUT / "schema_oversikt_decoder.svg"
    png = OUT / "schema_oversikt_decoder.png"
    svg.write_text(draw(), encoding="utf-8")
    print(f"Wrote {svg}")
    svg_to_png(svg, png, W, H)
    print(f"Wrote {png}")


if __name__ == "__main__":
    main()
