#!/usr/bin/env python3
"""Generate the KiCad schematic for AndreasM TransponderV3.

Same circuit as the OSH Park board: MCP1702 5 V, PIC16F18313, 5 MHz crystal,
LED, PCB loop. Wire numbers [n] match generate_schema_oversikt.py.
Symbols are embedded so the schematic opens without extra libraries.
"""

from __future__ import annotations

import json
import uuid
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def uid() -> str:
    return str(uuid.uuid4())


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def pin(name, num, x, y, length, orient, etype="passive"):
    return (
        f"(pin {etype} line\n"
        f"\t\t(at {x} {y} {orient})\n"
        f"\t\t(length {length})\n"
        f'\t\t(name "{esc(name)}" (effects (font (size 1.27 1.27))))\n'
        f'\t\t(number "{num}" (effects (font (size 1.27 1.27))))\n'
        f"\t)"
    )


def box(x0, y0, x1, y1):
    return (
        f"(rectangle (start {x0} {y0}) (end {x1} {y1})\n"
        f"\t\t(stroke (width 0.254) (type default)) (fill (type background)))"
    )


def poly(*pts, width=0.254, fill="none"):
    xy = " ".join(f"(xy {round(x, 3)} {round(y, 3)})" for x, y in pts)
    return f"(polyline (pts {xy}) (stroke (width {width}) (type default)) (fill (type {fill})))"


SYMBOL_TIPS: dict[str, dict[str, tuple[float, float]]] = {}


def lib_symbol(fullname, pins, body_extra="", hide_pin_names=False, hide_pin_numbers=False):
    SYMBOL_TIPS[fullname] = {p[1]: (p[2], p[3]) for p in pins}
    short = fullname.split(":")[-1]
    lines = [f'(symbol "{esc(fullname)}"']
    if hide_pin_numbers:
        lines.append("\t(pin_numbers (hide yes))")
    lines += [
        "\t(pin_names (offset 1.016)" + (" (hide yes))" if hide_pin_names else ")"),
        "\t(exclude_from_sim no)",
        "\t(in_bom yes)",
        "\t(on_board yes)",
        f'\t(property "Reference" "U" (at 0 {max(p[3] for p in pins)+3.81:.2f} 0) (effects (font (size 1.27 1.27))))',
        f'\t(property "Value" "{esc(short)}" (at 0 {min(p[3] for p in pins)-3.81:.2f} 0) (effects (font (size 1.27 1.27))))',
        '\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        f'\t(symbol "{esc(short)}_0_1"',
        f"\t\t{body_extra}",
        "\t)",
        f'\t(symbol "{esc(short)}_1_1"',
    ]
    for p in pins:
        lines.append("\t\t" + pin(*p))
    lines.append("\t)")
    lines.append(")")
    return "\n".join(lines)


LIBS = []

LIBS.append(
    lib_symbol(
        "TransponderV3:MCP1702",
        [
            ("VIN", "1", -12.70, 2.54, 2.54, 0, "power_in"),
            ("GND", "2", 0, -7.62, 2.54, 90, "power_in"),
            ("VOUT", "3", 12.70, 2.54, 2.54, 180, "power_out"),
        ],
        box(-10.16, -5.08, 10.16, 7.62),
    )
)

LIBS.append(
    lib_symbol(
        "TransponderV3:PIC16F18313",
        [
            ("VDD", "1", -17.78, 7.62, 2.54, 0, "power_in"),
            ("RA5", "2", -17.78, 2.54, 2.54, 0, "bidirectional"),
            ("RA4", "3", -17.78, -2.54, 2.54, 0, "bidirectional"),
            ("MCLR", "4", -17.78, -7.62, 2.54, 0, "input"),
            ("RA2", "5", 17.78, -7.62, 2.54, 180, "bidirectional"),
            ("RA1", "6", 17.78, -2.54, 2.54, 180, "bidirectional"),
            ("RA0", "7", 17.78, 2.54, 2.54, 180, "bidirectional"),
            ("VSS", "8", 17.78, 7.62, 2.54, 180, "power_in"),
        ],
        box(-15.24, -10.16, 15.24, 10.16),
    )
)

LIBS.append(
    lib_symbol(
        "TransponderV3:Antenna",
        [
            ("1", "1", -7.62, 0, 2.54, 0, "passive"),
            ("2", "2", 7.62, 0, 2.54, 180, "passive"),
        ],
        "\n\t\t".join(
            [
                poly((-5.08, 0), (-3.81, 2.54), (-1.27, -2.54), (1.27, 2.54), (3.81, -2.54), (5.08, 0)),
            ]
        ),
        hide_pin_names=True,
    )
)

LIBS.append(
    """(symbol "TransponderV3:R"
\t(pin_numbers (hide yes))
\t(pin_names (offset 0))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t(property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "R_0_1"
\t\t(polyline (pts (xy 0 2.54) (xy 0.762 1.905) (xy -0.762 0.635) (xy 0.762 -0.635) (xy -0.762 -1.905) (xy 0 -2.54))
\t\t\t(stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "R_1_1"
\t\t(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:C"
\t(pin_numbers (hide yes))
\t(pin_names (offset 0.254))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "C" (at 1.778 0.508 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Value" "C" (at 1.778 -1.016 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "C_0_1"
\t\t(polyline (pts (xy -1.524 0.508) (xy 1.524 0.508)) (stroke (width 0.371) (type default)) (fill (type none)))
\t\t(polyline (pts (xy -1.524 -0.508) (xy 1.524 -0.508)) (stroke (width 0.371) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 2.54) (xy 0 0.508)) (stroke (width 0) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 -2.54) (xy 0 -0.508)) (stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "C_1_1"
\t\t(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:LED"
\t(pin_numbers (hide yes))
\t(pin_names (offset 0) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "D" (at 2.54 1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Value" "LED" (at 2.54 -1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "LED_0_1"
\t\t(polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27) (xy 1.27 0) (xy -1.27 -1.27))
\t\t\t(stroke (width 0.254) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 -2.54) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 2.54) (xy 0 1.27)) (stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "LED_1_1"
\t\t(pin passive line (at 0 3.81 270) (length 1.27) (name "A" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 0 -3.81 90) (length 1.27) (name "K" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:Crystal"
\t(pin_numbers (hide yes))
\t(pin_names (offset 0) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "Y" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
\t(property "Value" "Crystal" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "Crystal_0_1"
\t\t(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t(polyline (pts (xy -2.032 -2.54) (xy -2.032 2.54)) (stroke (width 0.381) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 2.032 -2.54) (xy 2.032 2.54)) (stroke (width 0.381) (type default)) (fill (type none)))
\t)
\t(symbol "Crystal_1_1"
\t\t(pin passive line (at -3.81 0 0) (length 1.778) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 3.81 0 180) (length 1.778) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:Conn_01x02"
\t(pin_names (offset 1.016) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "J" (at 0.635 3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Value" "Conn_01x02" (at 0.635 -3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "Conn_01x02_1_1"
\t\t(rectangle (start 0 -1.27) (end 1.27 3.81) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t(pin passive line (at -5.08 2.54 0) (length 5.08) (name "+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at -5.08 0 0) (length 5.08) (name "-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:Conn_01x05"
\t(pin_names (offset 1.016) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "J" (at 0 6.35 0) (effects (font (size 1.27 1.27))))
\t(property "Value" "Prog" (at 0 -8.89 0) (effects (font (size 1.27 1.27))))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "Conn_01x05_1_1"
\t\t(rectangle (start -6.35 -2.54) (end 6.35 2.54) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t(pin passive line (at -5.08 5.08 270) (length 2.54) (name "VPP" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at -2.54 5.08 270) (length 2.54) (name "CLK" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 0 5.08 270) (length 2.54) (name "DAT" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 2.54 5.08 270) (length 2.54) (name "+V" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 5.08 5.08 270) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:GND"
\t(power)
\t(pin_numbers (hide yes))
\t(pin_names (offset 0) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "GND_0_1"
\t\t(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
\t\t\t(stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "GND_1_1"
\t\t(pin power_in line (at 0 0 270) (length 0) (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

LIBS.append(
    """(symbol "TransponderV3:PWR_FLAG"
\t(power)
\t(pin_numbers (hide yes))
\t(pin_names (offset 0) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "#FLG" (at 0 1.905 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Value" "PWR_FLAG" (at 0 2.54 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "PWR_FLAG_0_1"
\t\t(polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.016 1.27) (xy 0 2.54) (xy 1.016 1.27) (xy 0 1.27))
\t\t\t(stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "PWR_FLAG_1_1"
\t\t(pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t)
)"""
)

SYMBOL_TIPS.update(
    {
        "TransponderV3:R": {"1": (0, 3.81), "2": (0, -3.81)},
        "TransponderV3:C": {"1": (0, 3.81), "2": (0, -3.81)},
        "TransponderV3:LED": {"1": (0, 3.81), "2": (0, -3.81)},
        "TransponderV3:Crystal": {"1": (-3.81, 0), "2": (3.81, 0)},
        "TransponderV3:Conn_01x02": {"1": (-5.08, 2.54), "2": (-5.08, 0)},
        "TransponderV3:Conn_01x05": {
            "1": (-5.08, 5.08),
            "2": (-2.54, 5.08),
            "3": (0, 5.08),
            "4": (2.54, 5.08),
            "5": (5.08, 5.08),
        },
        "TransponderV3:GND": {"1": (0, 0)},
        "TransponderV3:PWR_FLAG": {"1": (0, 0)},
        "TransponderV3:Antenna": {"1": (-7.62, 0), "2": (7.62, 0)},
    }
)

SIDE = ((3.81, -1.27), (3.81, 1.27), "left")
TEXT_POS = {
    "TransponderV3:MCP1702": ((0, 10.16), (0, -8.89), ""),
    "TransponderV3:PIC16F18313": ((0, 13.97), (0, -13.97), ""),
    "TransponderV3:Antenna": ((0, -5.08), (0, 5.08), ""),
    "TransponderV3:Conn_01x02": ((3.81, -5.08), (3.81, 5.08), "left"),
    "TransponderV3:Conn_01x05": ((0, -11.43), (0, 8.89), ""),
    "TransponderV3:R": SIDE,
    "TransponderV3:C": SIDE,
    "TransponderV3:LED": SIDE,
    "TransponderV3:Crystal": ((0, 5.08), (0, -5.08), ""),
    "TransponderV3:GND": ((0, 5.08), (0, 5.08), ""),
    "TransponderV3:PWR_FLAG": ((0, -5.08), (0, -5.08), ""),
}

INST = []
WIRES = []
TEXTS = []
_pwr_n = 0
_flg_n = 0

C_VIN = (180, 83, 9, 0.3)
C_5V = (29, 78, 216, 0.3)
C_GND = (55, 65, 81, 0.15)
C_OSC = (14, 116, 144, 0.2)
C_LED = (162, 28, 175, 0.2)
C_TX = (21, 128, 61, 0.2)
C_ICSP = (67, 56, 202, 0.2)


def P(x, y):
    return (round(x, 2), round(y, 2))


def add(lib, ref, value, x, y):
    pins = {n: uid() for n in SYMBOL_TIPS[lib]}
    inst = {"lib": lib, "ref": ref, "value": value, "x": x, "y": y, "uuid": uid(), "pins": pins}
    INST.append(inst)
    return inst


def tip(inst, n):
    ox, oy = SYMBOL_TIPS[inst["lib"]][str(n)]
    return P(inst["x"] + ox, inst["y"] - oy)


def W(*pts, c=C_GND):
    pts = [P(*p) for p in pts]
    for a, b in zip(pts, pts[1:]):
        if a == b:
            continue
        if a[0] != b[0] and a[1] != b[1]:
            raise SystemExit(f"diagonal wire {a} -> {b}")
        WIRES.append((a, b, c))


def T(s, p, size=1.27, justify="left bottom"):
    TEXTS.append((s, P(*p), size, justify))


def num(n, a, b):
    a, b = P(*a), P(*b)
    if a[1] == b[1]:
        T(f"[{n}]", ((a[0] + b[0]) / 2, a[1] - 0.508), 1.0, "bottom")
    else:
        T(f"[{n}]", (a[0] + 0.762, (a[1] + b[1]) / 2), 1.0, "left")


def gnd(p, dy=2.54):
    global _pwr_n
    _pwr_n += 1
    end = P(p[0], p[1] + dy)
    W(p, end)
    add("TransponderV3:GND", f"#PWR{_pwr_n:02d}", "GND", end[0], end[1])


def flag(p):
    global _flg_n
    _flg_n += 1
    add("TransponderV3:PWR_FLAG", f"#FLG{_flg_n:02d}", "PWR_FLAG", p[0], p[1])


# ============================= Layout =======================================
Y_VIN = 38.10
Y_5V = 50.80

j1 = add("TransponderV3:Conn_01x02", "J1", "6,0–8,4 V", 30.48, 55.88)
u1 = add("TransponderV3:MCP1702", "U1", "MCP1702 5,0 V", 81.28, 55.88)
c1 = add("TransponderV3:C", "C1", "10uF", 63.50, 71.12)
c2 = add("TransponderV3:C", "C2", "10uF", 99.06, 71.12)

W(tip(j1, 1), (25.40, tip(j1, 1)[1]), (25.40, Y_VIN), (tip(u1, 1)[0], Y_VIN), tip(u1, 1), c=C_VIN)
num(1, (25.40, tip(j1, 1)[1]), (25.40, Y_VIN))
W(tip(j1, 2), (tip(j1, 2)[0] - 2.54, tip(j1, 2)[1]))
gnd((tip(j1, 2)[0] - 2.54, tip(j1, 2)[1]))
W((20.32, tip(j1, 2)[1]), (tip(j1, 2)[0] - 2.54, tip(j1, 2)[1]))
flag((20.32, tip(j1, 2)[1]))
T("[2]", (tip(j1, 2)[0] + 1.27, tip(j1, 2)[1] + 3.81), 1.0)
T("J1+ / GND", (33.02, 48.26), 1.0)

W((c1["x"], Y_VIN), tip(c1, 1), c=C_VIN)
gnd(tip(c1, 2))
num(3, (c1["x"], Y_VIN), tip(c1, 1))
flag((48.26, Y_VIN))

W(tip(u1, 3), (tip(u1, 3)[0], Y_5V), c=C_5V)
num(4, tip(u1, 3), (tip(u1, 3)[0], Y_5V))
W((c2["x"], Y_5V), tip(c2, 1), c=C_5V)
gnd(tip(c2, 2))
gnd(tip(u1, 2))
T("[5]", (tip(u1, 2)[0] + 0.762, tip(u1, 2)[1] + 1.27), 1.0)
T("+5 V", (139.70, Y_5V - 0.762), 1.27)

pic = add("TransponderV3:PIC16F18313", "U2", "PIC16F18313 SOIC-8", 152.40, 81.28)
W((tip(pic, 1)[0], Y_5V), tip(pic, 1), c=C_5V)
num(6, (tip(pic, 1)[0], 60.96), tip(pic, 1))
gnd((tip(pic, 8)[0] + 5.08, tip(pic, 8)[1]))
W(tip(pic, 8), (tip(pic, 8)[0] + 5.08, tip(pic, 8)[1]))
T("[7]", (tip(pic, 8)[0] + 2.54, tip(pic, 8)[1] - 1.27), 1.0)

y1 = add("TransponderV3:Crystal", "Y1", "5,000 MHz", 116.84, 106.68)
c3 = add("TransponderV3:C", "C3", "20pF", 101.60, 119.38)
c4 = add("TransponderV3:C", "C4", "20pF", 132.08, 119.38)
W(tip(pic, 2), (tip(y1, 1)[0], tip(pic, 2)[1]), tip(y1, 1), c=C_OSC)
num(8, tip(pic, 2), (tip(y1, 1)[0], tip(pic, 2)[1]))
W(tip(pic, 3), (tip(y1, 2)[0], tip(pic, 3)[1]), tip(y1, 2), c=C_OSC)
num(9, tip(pic, 3), (tip(y1, 2)[0], tip(pic, 3)[1]))
W(tip(y1, 1), (c3["x"], y1["y"]), tip(c3, 1), c=C_OSC)
W(tip(y1, 2), (c4["x"], y1["y"]), tip(c4, 1), c=C_OSC)
gnd(tip(c3, 2))
gnd(tip(c4, 2))

ra0, ra1, ra2 = tip(pic, 7), tip(pic, 6), tip(pic, 5)

d1 = add("TransponderV3:LED", "D1", "röd 1206", 190.50, ra2[1] + 3.81)
r1 = add("TransponderV3:R", "R1", "1k5", 190.50, d1["y"] + 15.24)
W(ra2, tip(d1, 1), c=C_LED)
num(10, ra2, tip(d1, 1))
W(tip(d1, 2), tip(r1, 1), c=C_LED)
gnd(tip(r1, 2))
T("[11]", (r1["x"] + 2.54, r1["y"]), 1.0)

# R2 hänger uppåt från RA0 så RA1 kan passera under. R3 till höger om LED.
r2 = add("TransponderV3:R", "R2", "100", 233.68, ra0[1] - 3.81)
r3 = add("TransponderV3:R", "R3", "100", 246.38, ra1[1] + 3.81)
W(ra0, tip(r2, 2), c=C_TX)
num(12, ra0, tip(r2, 2))
W(ra1, tip(r3, 1), c=C_TX)
num(13, ra1, tip(r3, 1))

c6 = add("TransponderV3:C", "C6", "47pF", 254.00, tip(r2, 1)[1] - 3.81)
ant = add("TransponderV3:Antenna", "AE1", "PCB-slinga", 276.86, tip(r3, 2)[1])
c5 = add("TransponderV3:C", "C5", "150pF", 254.00, ant["y"] + 12.70)

W(tip(r2, 1), (c6["x"], tip(r2, 1)[1]), tip(c6, 2), c=C_TX)
W(tip(c6, 1), (c6["x"], 27.94), (tip(ant, 1)[0], 27.94), tip(ant, 1), c=C_TX)
num(14, (c6["x"], 27.94), (tip(ant, 1)[0], 27.94))
W(tip(r3, 2), tip(ant, 2), c=C_TX)
num(15, tip(r3, 2), tip(ant, 2))
W((c5["x"], ant["y"]), tip(c5, 1), c=C_TX)
W(tip(c5, 2), (c5["x"], 114.30), (tip(ant, 2)[0], 114.30), tip(ant, 2), c=C_TX)

jp = add("TransponderV3:Conn_01x05", "J2", "ICSP undersida", 261.62, 134.62)
W(tip(jp, 1), (tip(jp, 1)[0], 124.46), (tip(pic, 4)[0], 124.46), tip(pic, 4), c=C_ICSP)
num(16, (tip(jp, 1)[0], 124.46), (180.00, 124.46))
W(tip(jp, 2), (tip(jp, 2)[0], tip(r3, 1)[1]), tip(r3, 1), c=C_ICSP)
num(17, tip(jp, 2), (tip(jp, 2)[0], tip(r3, 1)[1]))
W(tip(jp, 3), (tip(jp, 3)[0], tip(r2, 2)[1]), tip(r2, 2), c=C_ICSP)
num(18, tip(jp, 3), (tip(jp, 3)[0], tip(r2, 2)[1]))
W((tip(u1, 3)[0], Y_5V), (tip(jp, 4)[0], Y_5V), tip(jp, 4), c=C_5V)
num(19, tip(jp, 4), (tip(jp, 4)[0], 70.00))
gnd((tip(jp, 5)[0], tip(jp, 5)[1] + 7.62))
W(tip(jp, 5), (tip(jp, 5)[0], tip(jp, 5)[1] + 7.62))
T("[20]", (tip(jp, 5)[0] + 2.54, tip(jp, 5)[1] + 3.81), 1.0)

T("AndreasM TransponderV3 — CyclingHourglass", (25.40, 20.32), 2.0)
NOTES = [
    "[n] = ledningsnummer i kopplingsöversikten (schema_oversikt.png). Färgerna är desamma.",
    "Orange = VIN 6,0–8,4 V, blå = +5 V, grå = GND, cyan = kristall, lila = LED, grön = TX/antenn, indigo = ICSP.",
    "Ingen omvändpolaritetsskydd. Plus till J1 pin 1, minus till pin 2.",
    "C5 ~130 pF (150 pF i TME-ordern). Byt till 100 pF om räckvidden är dålig.",
    "Antennen är kopparslingan på undersidan. Linda inte extra varv.",
    "Programmera via J2: VPP CLK DAT +V GND. Detect = 3066.",
]
for i, line in enumerate(NOTES):
    T(line, (25.40, 160.02 + i * 4.445), 1.27)


def on_segment(p, a, b):
    if a[0] == b[0] == p[0]:
        return min(a[1], b[1]) < p[1] < max(a[1], b[1])
    if a[1] == b[1] == p[1]:
        return min(a[0], b[0]) < p[0] < max(a[0], b[0])
    return False


def overlaps(a, b, c, d):
    if a[1] == b[1] == c[1] == d[1]:
        lo, hi = max(min(a[0], b[0]), min(c[0], d[0])), min(max(a[0], b[0]), max(c[0], d[0]))
        return hi > lo
    if a[0] == b[0] == c[0] == d[0]:
        lo, hi = max(min(a[1], b[1]), min(c[1], d[1])), min(max(a[1], b[1]), max(c[1], d[1]))
        return hi > lo
    return False


def finalize():
    tips = [tip(i, n) for i in INST for n in SYMBOL_TIPS[i["lib"]]]
    poi = set(tips) | {p for a, b, _ in WIRES for p in (a, b)}
    out = []
    for a, b, col in WIRES:
        inner = sorted(
            (p for p in poi if on_segment(p, a, b)),
            key=lambda p: abs(p[0] - a[0]) + abs(p[1] - a[1]),
        )
        pts = [a, *inner, b]
        out += [(p, q, col) for p, q in zip(pts, pts[1:])]
    for i, (a, b, _) in enumerate(out):
        for c, d, _ in out[i + 1 :]:
            if overlaps(a, b, c, d):
                raise SystemExit(f"overlapping wires {a}-{b} and {c}-{d}")
    count = Counter(p for a, b, _ in out for p in (a, b))
    count.update(tips)
    return out, sorted(p for p, n in count.items() if n >= 3)


WIRES, JUNCTIONS = finalize()


def emit_inst(inst):
    lib = inst["lib"]
    is_pwr = lib.endswith(":GND") or lib.endswith(":PWR_FLAG")
    ref_hide = " (hide yes)" if is_pwr else ""
    val_hide = " (hide yes)" if lib.endswith(":PWR_FLAG") else ""
    (rdx, rdy), (vdx, vdy), just = TEXT_POS[lib]
    justify = f" (justify {just})" if just else ""
    ref_at = P(inst["x"] + rdx, inst["y"] + rdy)
    val_at = P(inst["x"] + vdx, inst["y"] + vdy)
    pins = "\n".join(f'\t\t(pin "{n}" (uuid "{u}"))' for n, u in inst["pins"].items())
    return f"""\t(symbol
\t\t(lib_id "{esc(lib)}")
\t\t(at {inst['x']} {inst['y']} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{inst['uuid']}")
\t\t(property "Reference" "{esc(inst['ref'])}"
\t\t\t(at {ref_at[0]} {ref_at[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)){justify}{ref_hide}))
\t\t(property "Value" "{esc(inst['value'])}"
\t\t\t(at {val_at[0]} {val_at[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)){justify}{val_hide}))
\t\t(property "Footprint" ""
\t\t\t(at {inst['x']} {inst['y']} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Datasheet" ""
\t\t\t(at {inst['x']} {inst['y']} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes)))
{pins}
\t)"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parts = [
        "(kicad_sch",
        "\t(version 20231120)",
        '\t(generator "eeschema")',
        '\t(generator_version "8.0")',
        f'\t(uuid "{uid()}")',
        '\t(paper "A3")',
        "\t(title_block",
        '\t\t(title "AndreasM TransponderV3")',
        '\t\t(date "2026-11-01")',
        '\t\t(rev "1")',
        '\t\t(company "CyclingHourglass")',
        '\t\t(comment 1 "RC Hourglass-krets, OSH Park-kort, 5 V")',
        '\t\t(comment 2 "MCP1702 + PIC16F18313 + 5 MHz + PCB-slinga")',
        "\t)",
        "\t(lib_symbols",
    ]
    for lib in LIBS:
        for line in lib.splitlines():
            parts.append("\t\t" + line)
    parts.append("\t)")

    for a, b, (r, g, bl, width) in WIRES:
        parts.append(
            f"\t(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))"
            f" (stroke (width {width}) (type default) (color {r} {g} {bl} 1))"
            f' (uuid "{uid()}"))'
        )
    for j in JUNCTIONS:
        parts.append(
            f'\t(junction (at {j[0]} {j[1]}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))'
        )
    for s, (x, y), size, justify in TEXTS:
        parts.append(
            f'\t(text "{esc(s)}" (exclude_from_sim no) (at {x} {y} 0)'
            f' (effects (font (size {size} {size})) (justify {justify})) (uuid "{uid()}"))'
        )
    for inst in INST:
        parts.append(emit_inst(inst))

    parts.append('\t(sheet_instances\n\t\t(path "/" (page "1"))\n\t)')
    parts.append(")")

    sch_path = OUT / "TransponderV3.kicad_sch"
    sch_path.write_text("\n".join(parts) + "\n", encoding="utf-8")

    pro = {
        "board": {"design_settings": {"defaults": {}, "rules": {}}, "layer_presets": [], "viewports": []},
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": "TransponderV3.kicad_pro", "version": 1},
        "net_settings": {
            "classes": [
                {
                    "bus_width": 12,
                    "clearance": 0.2,
                    "diff_pair_gap": 0.25,
                    "diff_pair_via_gap": 0.25,
                    "diff_pair_width": 0.2,
                    "line_style": 0,
                    "microvia_diameter": 0.3,
                    "microvia_drill": 0.1,
                    "name": "Default",
                    "pcb_color": "rgba(0, 0, 0, 0.000)",
                    "schematic_color": "rgba(0, 0, 0, 0.000)",
                    "track_width": 0.25,
                    "via_diameter": 0.8,
                    "via_drill": 0.4,
                    "wire_width": 6,
                }
            ],
            "meta": {"version": 3},
        },
        "pcbnew": {"last_paths": {}, "page_layout_descr_file": ""},
        "schematic": {
            "annotate_start_num": 0,
            "drawing": {
                "default_line_thickness": 6.0,
                "default_text_size": 50.0,
                "field_names": [],
                "intersheets_ref_show": False,
                "junction_size_choice": 3,
                "label_size_ratio": 0.375,
                "pin_symbol_size": 25.0,
                "text_offset_ratio": 0.15,
            },
            "legacy_lib_dir": "",
            "legacy_lib_list": [],
            "meta": {"version": 1},
            "plot_directory": "",
        },
        "sheets": [[uid(), "Root"]],
        "text_variables": {},
    }
    pro_path = OUT / "TransponderV3.kicad_pro"
    pro_path.write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")

    sym_lines = ["(kicad_symbol_lib", "\t(version 20231120)", '\t(generator "transponderv3")']
    for lib in LIBS:
        for line in lib.replace('(symbol "TransponderV3:', '(symbol "', 1).splitlines():
            sym_lines.append("\t" + line)
    sym_lines.append(")")
    (OUT / "TransponderV3.kicad_sym").write_text("\n".join(sym_lines) + "\n", encoding="utf-8")
    (OUT / "sym-lib-table").write_text(
        "(sym_lib_table\n\t(version 7)\n"
        '\t(lib (name "TransponderV3") (type "KiCad") '
        '(uri "${KIPRJMOD}/TransponderV3.kicad_sym") (options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    print(f"Wrote {sch_path}")
    print(f"Wrote {pro_path}")
    print(f"Instances={len(INST)} wires={len(WIRES)} junctions={len(JUNCTIONS)}")


if __name__ == "__main__":
    main()
