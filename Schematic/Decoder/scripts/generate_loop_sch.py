#!/usr/bin/env python3
"""KiCad schematic for Cano Loop Amplifier Rev B."""

from pathlib import Path

from kicadlib import C_5V, C_BIAS, C_GND, C_RF, C_TRIM, Sch

OUT = Path(__file__).resolve().parents[1]
s = Sch(
    "LoopAmp",
    OUT,
    "LoopAmplifier",
    "Cano Loop Amplifier Rev B",
    [
        "Phantom 5 V via R11 75 Ω. J2 center = signal + DC, shield = GND.",
        "[n] = ledningsnummer i schema_oversikt_loop.png",
        "J4 / C6 / R12 används inte (wiki). VR1 valfri, 2,15–2,25 V på Q6-bas.",
    ],
)
tip, W, T, num, gnd, flag = s.tip, s.W, s.T, s.num, s.gnd, s.flag
add = s.add

Y418, Y37 = 30.48, 38.10
XL, XR = 88.90, 139.70

j2 = add("F", "J2", "75 Ω F", 22.86, 38.10)
r11 = add("R", "R11", "75", 48.26, 34.29)
W(tip(j2, 1), (tip(j2, 1)[0], Y418), (r11["x"], Y418), tip(r11, 1), c=C_RF)
num(1, (tip(j2, 1)[0], Y418), (r11["x"], Y418))
W(tip(j2, 2), (12.70, tip(j2, 2)[1]))
gnd((12.70, tip(j2, 2)[1]))
T("[2]", (16.51, tip(j2, 2)[1] + 2.0), 1.0)
T("4,18 V", (27.94, Y418 - 1.5), 1.0)

W((38.10, Y37), (r11["x"], Y37), tip(r11, 2), (177.80, Y37), c=C_5V)
num(3, tip(r11, 2), (r11["x"], Y37))
T("3,70 V", (71.12, Y37 - 1.5), 1.27)
flag((58.42, Y37))
flag((12.70, tip(j2, 2)[1]))

c4 = add("CP", "C4", "10uF", 66.04, 41.91)
c3 = add("C", "C3", "100n", 78.74, 41.91)
W((c4["x"], Y37), tip(c4, 1), c=C_5V)
W((c3["x"], Y37), tip(c3, 1), c=C_5V)
gnd(tip(c4, 2))
gnd(tip(c3, 2))
T("[4]", (c4["x"] + 2.0, 43.0), 1.0)

r2 = add("R", "R2", "200", 101.60, 41.91)
r3 = add("R", "R3", "200", 127.00, 41.91)
r8 = add("R", "R8", "4k87", 157.48, 41.91)
q3 = add("Q_PNP", "Q3", "2N3906", 101.60, 58.42)
q4 = add("Q_PNP", "Q4", "2N3906", 127.00, 58.42)
q6 = add("Q_NPN", "Q6", "2N3904", 177.80, 58.42)

W((r2["x"], Y37), tip(r2, 1), c=C_5V)
W((r3["x"], Y37), tip(r3, 1), c=C_5V)
W((r8["x"], Y37), tip(r8, 1), c=C_5V)
W(tip(r2, 2), tip(q3, 1), c=C_BIAS)
W(tip(r3, 2), tip(q4, 1), c=C_BIAS)
num(5, tip(r2, 2), tip(q3, 1))
T("3,20 V", (106.68, 48.26), 1.0)

# Q3/Q4 collectors to Q6 base (2,2 V)
W(tip(q3, 3), (q3["x"], 68.58), (q6["x"] - 5.08, 68.58), (q6["x"] - 5.08, q6["y"]), tip(q6, 2), c=C_RF)
W(tip(q4, 3), (q4["x"], 68.58), c=C_RF)
W(tip(r8, 2), (r8["x"], 68.58), c=C_RF)
num(6, (q3["x"], 68.58), (140.0, 68.58))
T("2,2 V", (165.10, 66.04), 1.0)

r9 = add("R", "R9", "4k53", 165.10, 81.28)
r10 = add("R", "R10", "301", 177.80, 73.66)
W((165.10, 68.58), tip(r9, 1), c=C_RF)
gnd(tip(r9, 2))
W(tip(q6, 3), tip(r10, 1), c=C_GND)
gnd(tip(r10, 2))
W(tip(q6, 1), (q6["x"], Y37), c=C_5V)
T("[7]", (180.34, 48.26), 1.0)

q1 = add("Q_NPN", "Q1", "2N3904", 101.60, 86.36)
q2 = add("Q_NPN", "Q2", "2N3904", 127.00, 86.36)
r1 = add("R", "R1", "100", 114.30, 99.06)
W(tip(q3, 2), (83.82, tip(q3, 2)[1]), (83.82, tip(q1, 1)[1]), tip(q1, 1), c=C_BIAS)
W(tip(q4, 2), (134.62, tip(q4, 2)[1]), (134.62, tip(q2, 1)[1]), tip(q2, 1), c=C_BIAS)
W(tip(q1, 3), (q1["x"], tip(r1, 1)[1]), tip(r1, 1), c=C_GND)
W(tip(q2, 3), (q2["x"], tip(r1, 1)[1]), tip(r1, 1), c=C_GND)
gnd(tip(r1, 2))
num(8, tip(q1, 3), (q1["x"], tip(r1, 1)[1]))
T("0,50 V", (117.0, 93.98), 1.0)
T("1,20 V", (91.44, 83.82), 1.0)

# Q5 bias 1,25 V
q5 = add("Q_NPN", "Q5", "2N3904", 38.10, 86.36)
r6 = add("R", "R6", "4k87", 38.10, 41.91)
c2 = add("C", "C2", "100n", 50.80, 81.28)
r7 = add("R", "R7", "1k21", 27.94, 81.28)
W((r6["x"], Y37), tip(r6, 1), c=C_5V)
W(tip(r6, 2), tip(q5, 1), c=C_BIAS)
W(tip(q5, 1), (c2["x"], tip(q5, 1)[1]), tip(c2, 1), c=C_BIAS)
gnd(tip(c2, 2))
W(tip(q5, 1), (r7["x"], tip(q5, 1)[1]), (r7["x"], tip(r7, 1)[1]), tip(r7, 1), c=C_BIAS)
W(tip(r7, 2), (r7["x"], tip(q5, 2)[1]), tip(q5, 2), c=C_BIAS)
gnd(tip(q5, 3))
num(9, tip(r6, 2), tip(q5, 1))
T("1,25 V", (41.91, 72.39), 1.0)

# Loop rails from Q1/Q2 bases
W(tip(q1, 2), (XL, tip(q1, 2)[1]), (XL, 172.72), c=C_RF)
W(tip(q2, 2), (XR, tip(q2, 2)[1]), (XR, 172.72), c=C_RF)
num(10, (XL, 81.28), (XL, 99.06))
num(11, (XR, 81.28), (XR, 99.06))

r4 = add("R", "R4", "2k00", 63.50, 85.09)
r5 = add("R", "R5", "2k00", 190.50, 68.58)
W((c2["x"], tip(q5, 1)[1]), (r4["x"], tip(q5, 1)[1]), tip(r4, 1), c=C_BIAS)
W(tip(r4, 2), (r4["x"], tip(q1, 2)[1]), (XL, tip(q1, 2)[1]), c=C_RF)
W((r4["x"], tip(q5, 1)[1]), (r4["x"], tip(r5, 1)[1]), (r5["x"], tip(r5, 1)[1]), tip(r5, 1), c=C_BIAS)
W(tip(r5, 2), (r5["x"], tip(q2, 2)[1]), (XR, tip(q2, 2)[1]), c=C_RF)
T("[12]", (68.58, 83.82), 1.0)

c1 = add("C", "C1", "39pF", 114.30, 109.22)
W((XL, tip(c1, 1)[1]), (c1["x"], tip(c1, 1)[1]), tip(c1, 1), c=C_RF)
W(tip(c1, 2), (c1["x"], tip(c1, 2)[1]), (XR, tip(c1, 2)[1]), c=C_RF)
T("[13]", (116.84, 107.0), 1.0)

# J5 + C7 82p + C8 100n + R13 2k  (serie XL → jumper → cap → XR)
j5 = add("JUMP", "J5", "jumper", 99.06, 116.84)
c7 = add("C", "C7", "82pF", 111.76, 120.65)
c8 = add("C", "C8", "100n", 124.46, 125.73)
r13 = add("R", "R13", "2k00", 119.38, 134.62)
W((XL, 116.84), tip(j5, 1), c=C_TRIM)
W(tip(j5, 2), (c7["x"], 116.84), tip(c7, 1), c=C_TRIM)
W(tip(c7, 2), (c8["x"], tip(c7, 2)[1]), tip(c8, 1), c=C_TRIM)
W(tip(c8, 2), (c8["x"], tip(c8, 2)[1]), (XR, tip(c8, 2)[1]), c=C_TRIM)
W((r13["x"], tip(c7, 2)[1]), tip(r13, 1), c=C_TRIM)
W(tip(r13, 2), (XR, tip(r13, 2)[1]), c=C_TRIM)
T("[14]", (96.52, 115.0), 1.0)

# J4 + C6 + R12 (unused)
j4 = add("JUMP", "J4", "oanvänd", 99.06, 147.32)
c6 = add("C", "C6", "oanvänd", 111.76, 151.13)
r12 = add("R", "R12", "4k87", 124.46, 151.13)
W((XL, 147.32), tip(j4, 1), c=C_TRIM)
W(tip(j4, 2), (c6["x"], 147.32), tip(c6, 1), c=C_TRIM)
W(tip(c6, 2), (r12["x"], tip(c6, 2)[1]), tip(r12, 1), c=C_TRIM)
W(tip(r12, 2), (r12["x"], tip(r12, 2)[1]), (XR, tip(r12, 2)[1]), c=C_TRIM)
T("[15]", (96.52, 145.5), 1.0)

# J3 + C5 22p
j3 = add("JUMP", "J3", "jumper", 99.06, 162.56)
c5 = add("C", "C5", "22pF", 111.76, 166.37)
W((XL, 162.56), tip(j3, 1), c=C_TRIM)
W(tip(j3, 2), (c5["x"], 162.56), tip(c5, 1), c=C_TRIM)
W(tip(c5, 2), (c5["x"], tip(c5, 2)[1]), (XR, tip(c5, 2)[1]), c=C_TRIM)
T("[16]", (96.52, 161.0), 1.0)

j1 = add("LOOP", "J1", "timing loop", 114.30, 172.72)
W((XL, 172.72), tip(j1, 1), c=C_RF)
W((XR, 172.72), tip(j1, 2), c=C_RF)
num(17, (XL, 165.10), (XL, 172.72))

r14 = add("R", "R14", "200k", 88.90, 185.42)
vr1 = add("POT", "VR1", "500k", 114.30, 190.50)
r15 = add("R", "R15", "200k", 139.70, 185.42)
W((XL, 172.72), (XL, 181.61), tip(r14, 1), c=C_TRIM)
W(tip(r14, 2), (r14["x"], 187.96), tip(vr1, 1), c=C_TRIM)
W((XR, 172.72), (XR, 181.61), tip(r15, 1), c=C_TRIM)
W(tip(r15, 2), (r15["x"], 187.96), tip(vr1, 3), c=C_TRIM)
gnd(tip(vr1, 2))
T("[18]", (114.30, 183.0), 1.0)
T("Valfri offset. Sätt 2,15–2,25 V på Q6-bas.", (165.10, 190.50), 1.27)

T("Cano Loop Amplifier Rev B — CyclingHourglass", (20.32, 17.78), 2.0)
for i, line in enumerate(
    [
        "[n] = ledningsnummer i kopplingsöversikten. Orange = phantom/J2, blå = 3,70 V, grön = loop/RF, lila = jumper/trim.",
        "J2 centerpin = signal + phantom. Skärm = jord. Rev B rättade pinout.",
        "Q1 Q2 Q5 Q6 = 2N3904 NPN. Q3 Q4 = 2N3906 PNP. Platt sida: E B C.",
        "J4, C6, R12 har inte använts i wiki-bygget. Cykelmållinje: börja utan jumper eller med J3.",
        "Testa med 5 V via 75 Ω in i J2, loop ifrån. Spänningar är DC mot jord.",
    ]
):
    T(line, (20.32, 210.82 + i * 4.445), 1.27)

if __name__ == "__main__":
    s.write()
