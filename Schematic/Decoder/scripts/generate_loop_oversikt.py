#!/usr/bin/env python3
"""Kopplingsöversikt för Cano Loop Amplifier Rev B."""

from pathlib import Path

from svglib import (
    BG,
    C_5V,
    C_GND,
    C_TRIM,
    C_TX,
    C_VIN,
    INK,
    MUTED,
    Box,
    Svg,
    badge,
    capacitor,
    gnd,
    header,
    resistor_h,
    svg_to_png,
    table,
    wire,
)

OUT = Path(__file__).resolve().parents[1]
W, H = 1600, 1240


def draw() -> str:
    s = Svg(W, H)
    header(
        s,
        "Cano Loop Amplifier Rev B — kopplingsöversikt",
        "Varje färgad linje = en ledning  ·  [n] = nummer, samma som i KiCad  ·  "
        "Phantom 5 V via 75 Ω  ·  J4 oanvänd",
        [
            (C_VIN, "J2 phantom 4,18 V"),
            (C_5V, "3,70 V-skena"),
            (C_GND, "GND"),
            (C_TX, "Loop / RF"),
            (C_TRIM, "Jumper / trim"),
        ],
    )

    j2 = Box(s, 48, 150, 160, 96, "J2  75 Ω F", C_VIN, "center = signal + DC")
    sig = j2.right("center", 188)
    sh = j2.bottom("skärm", 128)
    wire(s, C_VIN, sig, (260, 188), width=4)
    badge(s, 1, 230, 176, C_VIN)
    gnd(s, *sh, n=2)

    r11a, r11b = resistor_h(s, 260, 188, "R11", "75 Ω", C_VIN)
    wire(s, C_VIN, (316, 188), (316, 236), (1540, 236), width=4)
    badge(s, 3, 360, 188, C_VIN)
    s.dot(316, 236, C_5V)
    s.text(480, 222, "3,70 V-skena", 13, C_5V, "700")

    c4t, c4b = capacitor(s, 400, 250, "C4", "10 µF", C_5V)
    c3t, c3b = capacitor(s, 470, 250, "C3", "100 nF", C_5V)
    wire(s, C_5V, (400, 236), c4t)
    wire(s, C_5V, (470, 236), c3t)
    s.dot(400, 236, C_5V)
    s.dot(470, 236, C_5V)
    gnd(s, *c4b)
    gnd(s, *c3b)
    badge(s, 4, 430, 248, C_5V)

    pnp = Box(s, 560, 250, 220, 120, "Q3 / Q4  2N3906", C_5V, "PNP  ·  emitter 3,20 V")
    q3e = pnp.top("E R2 200", 620)
    q4e = pnp.top("E R3 200", 720)
    q3b = pnp.left("B", 320)
    q4b = pnp.right("B", 320)
    qc = pnp.bottom("C  2,2 V", 670)
    wire(s, C_5V, (620, 236), q3e)
    wire(s, C_5V, (720, 236), q4e)
    s.dot(620, 236, C_5V)
    s.dot(720, 236, C_5V)
    badge(s, 5, 620, 248, C_5V)

    q6 = Box(s, 920, 250, 180, 130, "Q6  2N3904", C_TX, "bas 2,2 V  ·  R8 4k87")
    q6b = q6.left("B", 400)
    q6c = q6.top("C", 1000)
    q6e = q6.bottom("E R10 301", 1000)
    wire(s, C_TX, qc, (670, 400), q6b)
    badge(s, 6, 800, 400, C_TX)
    wire(s, C_5V, (1000, 236), q6c)
    s.dot(1000, 236, C_5V)
    badge(s, 7, 1000, 248, C_5V)
    gnd(s, *q6e)
    r9a, r9b = resistor_h(s, 1120, 400, "R9", "4k53", C_TX)
    wire(s, C_TX, q6b, r9a)
    gnd(s, *r9b)

    npn = Box(s, 560, 430, 220, 120, "Q1 / Q2  2N3904", C_TX, "NPN  ·  bas 1,20 V")
    q1c = npn.top("C", 620)
    q2c = npn.top("C", 720)
    q1b = npn.left("B loop L", 490)
    q2b = npn.right("B loop R", 490)
    qe = npn.bottom("E R1 100", 670)
    wire(s, C_5V, q3b, (540, 320), (540, 370), (620, 370), q1c)
    wire(s, C_5V, q4b, (800, 320), (800, 370), (720, 370), q2c)
    badge(s, 8, 670, 548, C_GND)
    gnd(s, *qe, n=8)

    q5 = Box(s, 48, 300, 170, 110, "Q5  2N3904", C_VIN, "bias 1,25 V")
    q5c = q5.right("C R6 4k87", 340)
    q5e = q5.bottom("E", 130)
    gnd(s, *q5e)
    wire(s, C_5V, (130, 236), (130, 300))
    s.dot(130, 236, C_5V)
    s.text(140, 340, "R7 1k21  C2 100 nF", 12, C_VIN, "400")
    wire(s, C_VIN, q5c, (560, 340), (560, 490), q1b)
    badge(s, 9, 280, 328, C_VIN)
    badge(s, 12, 360, 340, C_VIN)
    wire(s, C_VIN, (400, 340), (400, 490), (780, 490), q2b)

    loop = Box(s, 920, 430, 220, 140, "J1  timing loop", C_TX, "banan / två ledare")
    l1 = loop.left("1", 490)
    l2 = loop.left("2", 530)
    wire(s, C_TX, q1b, (560, 490), l1)
    wire(s, C_TX, q2b, l2)
    badge(s, 10, 850, 478, C_TX)
    badge(s, 11, 850, 530, C_TX)
    badge(s, 17, 1040, 418, C_TX)
    s.dot(850, 490, C_TX)
    cap = capacitor(s, 850, 500, "C1", "39 pF", C_TX)
    wire(s, C_TX, (850, 490), cap[0])
    wire(s, C_TX, cap[1], (850, 530))
    badge(s, 13, 890, 518, C_TX)

    jmp = Box(s, 920, 600, 280, 130, "J3 / J4 / J5  avstämning", C_TRIM, "över loopen")
    j3 = jmp.left("J3 C5 22 pF", 640)
    j4 = jmp.left("J4 C6 R12 oanvänd", 680)
    j5 = jmp.left("J5 C7 82 p C8 R13", 720)
    wire(s, C_TRIM, (850, 530), (850, 640), j3)
    badge(s, 16, 880, 640, C_TRIM)
    badge(s, 15, 880, 680, C_TRIM)
    badge(s, 14, 880, 720, C_TRIM)

    vr = Box(s, 48, 500, 220, 100, "VR1  500 k  valfri", C_TRIM, "R14 / R15 200 k")
    v1 = vr.right("till loop", 540)
    vw = vr.bottom("wiper", 158)
    wire(s, C_TRIM, v1, (850, 540), (850, 530))
    badge(s, 18, 300, 540, C_TRIM)
    gnd(s, *vw)

    s.text(48, 640, "Alla GND-symboler = samma stjärnjord.", 13, C_GND, "700")
    s.text(48, 662, "Plus via decoder-phantom eller 5 V + 75 Ω in i J2.", 13, C_GND, "400")
    s.text(48, 690, "Q1 Q2 Q5 Q6 = 2N3904. Q3 Q4 = 2N3906.", 13, INK, "700")
    s.text(48, 712, "Platt sida mot dig: E B C. Inte BC-fotavtryck.", 13, INK, "400")
    s.text(48, 740, "Cykelmållinje: ingen jumper eller J3. Inte J5.", 13, INK, "400")
    s.text(48, 762, "J4 / C6 / R12 sitter inte i wiki-bygget.", 13, MUTED, "400")

    rows = [
        ("1", C_VIN, "J2", "J2 center → R11 75 Ω", "4,18 V med 5 V phantom"),
        ("2", C_GND, "GND", "J2 skärm → jord", "Rev B rättade pinout"),
        ("3", C_5V, "3V7", "R11 → 3,70 V-skena", "intern matning efter 75 Ω"),
        ("4", C_5V, "3V7", "C4 10 µF, C3 100 nF", "C4 plus mot skenan"),
        ("5", C_5V, "3V7", "R2/R3 200 Ω → Q3/Q4 E", "emitter 3,20 V"),
        ("6", C_TX, "RF", "Q3/Q4 C → Q6 bas", "2,2 V, R8 4k87 från 3,70 V"),
        ("7", C_5V, "3V7", "Q6 C → 3,70 V", "R9 4k53 och R10 301 till jord"),
        ("8", C_GND, "GND", "Q1/Q2 E → R1 100 → jord", "0,50 V"),
        ("9", C_VIN, "BIAS", "Q5 C = 1,25 V", "R6 4k87, R7 1k21, C2 100 nF"),
        ("10", C_TX, "LOOP", "Q1 bas → loop 1", "1,20 V, R4 2k00"),
        ("11", C_TX, "LOOP", "Q2 bas → loop 2", "1,20 V, R5 2k00"),
        ("12", C_VIN, "BIAS", "1,25 V → R4 / R5", "återkoppling, jorda inte R5"),
        ("13", C_TX, "LOOP", "C1 39 pF över loopen", "fast avstämning"),
        ("14", C_TRIM, "J5", "J5 + C7 82 p + R13 2k", "liten loop 3–4 fot"),
        ("15", C_TRIM, "J4", "J4 + C6 + R12 4k87", "oanvänd i wikin"),
        ("16", C_TRIM, "J3", "J3 + C5 22 pF", "mellanstor loop 6–8 fot"),
        ("17", C_TX, "LOOP", "J1 mellan loop 1 och 2", "banan / skruvplint OK"),
        ("18", C_TRIM, "VR1", "R14–VR1–R15 över loopen", "2,15–2,25 V på Q6-bas"),
    ]
    table(s, rows, 800, "Ledningslista — Loop Amplifier Rev B")
    s.text(
        40,
        H - 24,
        "CyclingHourglass  ·  KiCad: Schematic/Decoder/LoopAmplifier.kicad_pro  ·  "
        "scripts/generate_loop_oversikt.py",
        12,
        "#6b7280",
    )
    return s.build()


def main() -> None:
    svg = OUT / "schema_oversikt_loop.svg"
    png = OUT / "schema_oversikt_loop.png"
    svg.write_text(draw(), encoding="utf-8")
    print(f"Wrote {svg}")
    svg_to_png(svg, png, W, H)
    print(f"Wrote {png}")


if __name__ == "__main__":
    main()
