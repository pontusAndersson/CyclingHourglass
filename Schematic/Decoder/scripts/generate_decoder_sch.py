#!/usr/bin/env python3
"""KiCad schematic for RCHourglass decoder PDIA + CY8CKIT-059."""

from pathlib import Path

from kicadlib import C_5V, C_BIAS, C_GND, C_IO, C_OSC, C_RF, Sch, lib_symbol

OUT = Path(__file__).resolve().parents[1]
s = Sch(
    "Decoder",
    OUT,
    "Decoder",
    "RCHourglass Decoder PDIA",
    [
        "Cano phase detector + CY8CKIT-059. Wiki-bygget.",
        "[n] = ledningsnummer i schema_oversikt_decoder.png",
        "LED / piezo / PIC-prog är valfria extras, se original PDF Rev 2.",
    ],
)

s.extra_lib(
    "Decoder:PSOC",
    {
        "VDDIO": (-15.24, 10.16),
        "GND": (-15.24, -10.16),
        "P12_2": (15.24, 5.08),
        "P12_3": (15.24, 0),
        "P15_0": (15.24, -5.08),
        "P15_1": (15.24, -10.16),
    },
    lib_symbol(
        "Decoder:PSOC",
        [
            ("VDDIO", "VDDIO", -15.24, 10.16, 2.54, 0, "power_in"),
            ("GND", "GND", -15.24, -10.16, 2.54, 0, "power_in"),
            ("P12_2", "P12_2", 15.24, 5.08, 2.54, 180, "bidirectional"),
            ("P12_3", "P12_3", 15.24, 0, 2.54, 180, "bidirectional"),
            ("P15_0", "P15_0", 15.24, -5.08, 2.54, 180, "bidirectional"),
            ("P15_1", "P15_1", 15.24, -10.16, 2.54, 180, "bidirectional"),
        ],
        "\n\t\t".join(
            [
                "(rectangle (start -12.7 -12.7) (end 12.7 12.7)\n"
                "\t\t(stroke (width 0.254) (type default)) (fill (type background)))"
            ]
        ),
    ),
    ((0, 16.51), (0, -16.51), ""),
)

tip, W, T, num, gnd, flag, vcc, add = s.tip, s.W, s.T, s.num, s.gnd, s.flag, s.vcc, s.add

Y5 = 27.94

j1 = add("F", "J1", "75 Ω från loop amp", 22.86, 71.12)
r1 = add("R", "R1", "75", 38.10, 48.26)
W(tip(j1, 1), (tip(j1, 1)[0], tip(r1, 2)[1]), (r1["x"], tip(r1, 2)[1]), tip(r1, 2), c=C_RF)
num(1, (tip(j1, 1)[0], tip(r1, 2)[1]), (r1["x"], tip(r1, 2)[1]))
W(tip(j1, 2), (12.70, tip(j1, 2)[1]))
gnd((12.70, tip(j1, 2)[1]))
T("[2]", (16.51, tip(j1, 2)[1] + 2.0), 1.0)
T("phantom", (30.48, 41.91), 1.0)

W(tip(r1, 1), (r1["x"], Y5), (185.42, Y5), c=C_5V)
flag((48.26, Y5))
flag((12.70, tip(j1, 2)[1]))
T("+5 V", (71.12, Y5 - 1.5), 1.27)

c3 = add("C", "C3", "100n", 63.50, 34.29)
r7 = add("R", "R7", "1k21", 78.74, 34.29)
q5 = add("Q_PNP", "Q5", "2N3906", 78.74, 50.80)
r8 = add("R", "R8", "10k", 78.74, 66.04)
W((c3["x"], Y5), tip(c3, 1), c=C_5V)
W((r7["x"], Y5), tip(r7, 1), c=C_5V)
W(tip(r7, 2), tip(q5, 1), c=C_BIAS)
W(tip(c3, 2), (c3["x"], tip(q5, 3)[1]), (q5["x"], tip(q5, 3)[1]), tip(q5, 3), c=C_BIAS)
W(tip(q5, 3), tip(r8, 1), c=C_BIAS)
W(tip(q5, 2), (71.12, tip(q5, 2)[1]), (71.12, tip(q5, 3)[1]), c=C_BIAS)
gnd(tip(r8, 2))
num(3, tip(r7, 2), tip(q5, 1))
T("3,7 V  TP1/TP2", (86.36, 58.42), 1.0)

c1 = add("C", "C1", "47pF", 38.10, 81.28)
W(tip(j1, 1), (tip(j1, 1)[0], 77.47), (c1["x"], 77.47), tip(c1, 1), c=C_RF)
num(4, (c1["x"], 77.47), tip(c1, 1))
T("TP7 ~3,96 V", (43.18, 76.20), 1.0)

q1 = add("Q_PNP", "Q1", "2N3906", 71.12, 91.44)
q2 = add("Q_PNP", "Q2", "2N3906", 101.60, 91.44)
r2 = add("R", "R2", "100", 86.36, 71.12)
r5 = add("R", "R5", "1k00", 58.42, 81.28)
r6 = add("R", "R6", "1k00", 119.38, 81.28)
c2 = add("C", "C2", "470pF", 109.22, 63.50)

W((r2["x"], Y5), tip(r2, 1), c=C_5V)
W(tip(r2, 2), (q1["x"], tip(r2, 2)[1]), tip(q1, 1), c=C_5V)
W(tip(r2, 2), (q2["x"], tip(r2, 2)[1]), tip(q2, 1), c=C_5V)
num(5, tip(r2, 2), (q1["x"], tip(r2, 2)[1]))

W(tip(c1, 2), (c1["x"], tip(q1, 2)[1]), tip(q1, 2), c=C_RF)
W(tip(q5, 3), (83.82, tip(q5, 3)[1]), (83.82, 77.47), c=C_BIAS)
W((83.82, 77.47), (r5["x"], 77.47), tip(r5, 1), c=C_BIAS)
W(tip(r5, 2), (r5["x"], tip(q1, 2)[1]), c=C_BIAS)
T("[6]", (62.0, 80.0), 1.0)
T("TP6 ~3,71 V", (50.80, 91.44), 1.0)

W((83.82, 77.47), (r6["x"], 77.47), tip(r6, 1), c=C_BIAS)
W(tip(r6, 2), (r6["x"], tip(q2, 2)[1]), (c2["x"], tip(q2, 2)[1]), c=C_BIAS)
W((c2["x"], Y5), tip(c2, 1), c=C_5V)
W(tip(c2, 2), (c2["x"], tip(q2, 2)[1]), tip(q2, 2), c=C_RF)
T("TP5 ~3,73 V", (119.38, 91.44), 1.0)

q3 = add("Q_NPN", "Q3", "2N3904", 71.12, 116.84)
q4 = add("Q_NPN", "Q4", "2N3904", 101.60, 116.84)
r3 = add("R", "R3", "200", 71.12, 132.08)
r4 = add("R", "R4", "200", 101.60, 132.08)
W(tip(q1, 3), tip(q3, 1), c=C_BIAS)
W(tip(q2, 3), tip(q4, 1), c=C_RF)
W(tip(q3, 3), tip(r3, 1), c=C_GND)
W(tip(q4, 3), tip(r4, 1), c=C_GND)
gnd(tip(r3, 2))
gnd(tip(r4, 2))
W(tip(q3, 2), (86.36, tip(q3, 2)[1]), tip(q4, 2), c=C_BIAS)
W(tip(q3, 1), (63.50, tip(q3, 1)[1]), (63.50, tip(q3, 2)[1]), (tip(q3, 2)[0], tip(q3, 2)[1]), c=C_BIAS)
num(7, tip(q1, 3), tip(q3, 1))
T("TP10/11 ~0,39 V", (109.22, 132.08), 1.0)
T("TP9 ~1,05 V", (88.90, 114.30), 1.0)

r9 = add("R", "R9", "2k00", 127.00, 71.12)
r10 = add("R", "R10", "2k00", 127.00, 116.84)
W((r9["x"], Y5), tip(r9, 1), c=C_5V)
W(tip(r9, 2), (r9["x"], tip(q4, 1)[1]), tip(q4, 1), c=C_RF)
W((r9["x"], tip(q4, 1)[1]), tip(r10, 1), c=C_RF)
gnd(tip(r10, 2))
num(8, tip(r9, 2), (r9["x"], tip(q4, 1)[1]))
T("TP8 ~1,87 V ut", (132.08, 99.06), 1.0)

psoc = add("PSOC", "U1", "CY8CKIT-059", 200.66, 91.44)
W((r9["x"], tip(q4, 1)[1]), (tip(psoc, "P12_2")[0], tip(q4, 1)[1]), tip(psoc, "P12_2"), c=C_IO)
num(9, (140.0, tip(q4, 1)[1]), (180.0, tip(q4, 1)[1]))

r11 = add("R", "R11", "4k87", 165.10, 91.44)
W(tip(psoc, "P12_3"), (tip(r11, 1)[0], tip(psoc, "P12_3")[1]), tip(r11, 1), c=C_IO)
W(tip(r11, 2), (r11["x"], tip(q4, 1)[1]), c=C_IO)
num(10, tip(psoc, "P12_3"), (r11["x"], tip(psoc, "P12_3")[1]))

W((tip(psoc, "VDDIO")[0], Y5), tip(psoc, "VDDIO"), c=C_5V)
num(11, (tip(psoc, "VDDIO")[0], 35.56), tip(psoc, "VDDIO"))
gnd(tip(psoc, "GND"), dy=5.08)
T("[12]", (tip(psoc, "GND")[0] + 2.0, tip(psoc, "GND")[1] + 3.0), 1.0)

y1 = add("Crystal", "Y1", "5,000 MHz", 238.76, 109.22)
c4 = add("C", "C4", "22pF", 228.60, 121.92)
c5 = add("C", "C5", "22pF", 248.92, 121.92)
W(tip(psoc, "P15_0"), (tip(y1, 1)[0], tip(psoc, "P15_0")[1]), tip(y1, 1), c=C_OSC)
W(tip(psoc, "P15_1"), (tip(y1, 2)[0], tip(psoc, "P15_1")[1]), tip(y1, 2), c=C_OSC)
num(13, tip(psoc, "P15_0"), (tip(y1, 1)[0], tip(psoc, "P15_0")[1]))
W(tip(y1, 1), (c4["x"], y1["y"]), tip(c4, 1), c=C_OSC)
W(tip(y1, 2), (c5["x"], y1["y"]), tip(c5, 1), c=C_OSC)
gnd(tip(c4, 2))
gnd(tip(c5, 2))
T("[14]", (231.14, 121.92), 1.0)

T("RCHourglass Decoder — CyclingHourglass", (20.32, 15.24), 2.0)
for i, line in enumerate(
    [
        "[n] = ledningsnummer i kopplingsöversikten. Blå = +5 V, orange = phantom/bias, grön = RF, indigo = PSoC, cyan = kristall.",
        "Q1 Q2 Q5 = 2N3906 PNP. Q3 Q4 = 2N3904 NPN. Inte BC547/BC307-fotavtryck.",
        "+5 V till VDDIO, jord till nedre PSoC-GND. Analogutgång till P12_2, hysteres P12_3 via R11.",
        "Kristall 5 MHz på P15_0 / P15_1 (nedre listen), inte kitets XTAL-silk P15.2/P15.3.",
        "F-chassi ska jordas (vit tråd till R8). LED/piezo/PIC-prog valfritt: original PDF Rev 2.",
    ]
):
    T(line, (20.32, 160.02 + i * 4.445), 1.27)

if __name__ == "__main__":
    s.write()
