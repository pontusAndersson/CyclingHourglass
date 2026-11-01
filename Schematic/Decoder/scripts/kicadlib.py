"""Shared KiCad schematic emitter for Decoder and LoopAmplifier."""

from __future__ import annotations

import json
import uuid
from collections import Counter
from pathlib import Path


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


def lib_symbol(fullname, pins, body_extra="", hide_pin_names=False, hide_pin_numbers=False):
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


PASSIVE_2 = """
\t(pin_numbers (hide yes))
\t(pin_names (offset 0.254))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
"""


def common_symbols(pfx: str) -> tuple[list[str], dict[str, dict[str, tuple[float, float]]], dict]:
    libs = []
    tips: dict[str, dict[str, tuple[float, float]]] = {}

    def add_lib(name, pinmap, text):
        tips[name] = pinmap
        libs.append(text)

    add_lib(
        f"{pfx}:R",
        {"1": (0, 3.81), "2": (0, -3.81)},
        f'''(symbol "{pfx}:R"
{PASSIVE_2}\t(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
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
)''',
    )
    add_lib(
        f"{pfx}:C",
        {"1": (0, 3.81), "2": (0, -3.81)},
        f'''(symbol "{pfx}:C"
{PASSIVE_2}\t(property "Reference" "C" (at 1.778 0.508 0) (effects (font (size 1.27 1.27)) (justify left)))
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
)''',
    )
    add_lib(
        f"{pfx}:CP",
        {"1": (0, 3.81), "2": (0, -3.81)},
        f'''(symbol "{pfx}:CP"
{PASSIVE_2}\t(property "Reference" "C" (at 2.032 0.508 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Value" "CP" (at 2.032 -1.016 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "CP_0_1"
\t\t(polyline (pts (xy -1.524 0.508) (xy 1.524 0.508)) (stroke (width 0.508) (type default)) (fill (type none)))
\t\t(polyline (pts (xy -1.524 -0.508) (xy -0.3 -0.508) (xy 0 -1.016) (xy 0.3 -0.508) (xy 1.524 -0.508))
\t\t\t(stroke (width 0.371) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 2.54) (xy 0 0.508)) (stroke (width 0) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 -2.54) (xy 0 -0.508)) (stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "CP_1_1"
\t\t(pin passive line (at 0 3.81 270) (length 1.27) (name "+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at 0 -3.81 90) (length 1.27) (name "-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)''',
    )
    add_lib(
        f"{pfx}:Q_NPN",
        {"1": (0, 5.08), "2": (-5.08, 0), "3": (0, -5.08)},
        lib_symbol(
            f"{pfx}:Q_NPN",
            [
                ("C", "1", 0, 5.08, 2.54, 270),
                ("B", "2", -5.08, 0, 2.54, 0),
                ("E", "3", 0, -5.08, 2.54, 90),
            ],
            "\n\t\t".join(
                [
                    box(-2.54, -2.54, 2.54, 2.54),
                    poly((-1.27, -1.27), (-1.27, 1.27)),
                    poly((-1.27, 0.4), (1.2, 2.0)),
                    poly((-1.27, -0.4), (1.2, -2.0), (0.4, -1.2), (1.2, -2.0), (0.6, -1.0)),
                ]
            ),
        ),
    )
    add_lib(
        f"{pfx}:Q_PNP",
        {"1": (0, 5.08), "2": (-5.08, 0), "3": (0, -5.08)},
        lib_symbol(
            f"{pfx}:Q_PNP",
            [
                ("E", "1", 0, 5.08, 2.54, 270),
                ("B", "2", -5.08, 0, 2.54, 0),
                ("C", "3", 0, -5.08, 2.54, 90),
            ],
            "\n\t\t".join(
                [
                    box(-2.54, -2.54, 2.54, 2.54),
                    poly((-1.27, -1.27), (-1.27, 1.27)),
                    poly((-1.27, 0.4), (0.4, 1.2), (1.2, 2.0), (0.6, 1.0)),
                    poly((-1.27, -0.4), (1.2, -2.0)),
                ]
            ),
        ),
    )
    add_lib(
        f"{pfx}:POT",
        {"1": (-5.08, 2.54), "2": (0, -5.08), "3": (5.08, 2.54)},
        lib_symbol(
            f"{pfx}:POT",
            [
                ("1", "1", -5.08, 2.54, 2.54, 0),
                ("2", "2", 0, -5.08, 2.54, 90),
                ("3", "3", 5.08, 2.54, 2.54, 180),
            ],
            box(-2.54, -2.54, 2.54, 2.54) + "\n\t\t" + poly((0, -2.54), (0, 0), (1.0, -1.0)),
        ),
    )
    add_lib(
        f"{pfx}:F",
        {"1": (-5.08, 2.54), "2": (-5.08, 0)},
        f'''(symbol "{pfx}:F"
\t(pin_names (offset 1.016) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "J" (at 1.27 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Value" "F" (at 1.27 -3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "F_1_1"
\t\t(rectangle (start 0 -1.27) (end 2.54 3.81) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t(circle (center 1.27 2.54) (radius 0.6) (stroke (width 0.2) (type default)) (fill (type none)))
\t\t(pin passive line (at -5.08 2.54 0) (length 5.08) (name "SIG" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t(pin passive line (at -5.08 0 0) (length 5.08) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t)
)''',
    )
    add_lib(
        f"{pfx}:JUMP",
        {"1": (-3.81, 0), "2": (3.81, 0)},
        lib_symbol(
            f"{pfx}:JUMP",
            [("1", "1", -3.81, 0, 2.54, 0), ("2", "2", 3.81, 0, 2.54, 180)],
            box(-1.27, -1.27, 1.27, 1.27),
            hide_pin_names=True,
        ),
    )
    add_lib(
        f"{pfx}:LOOP",
        {"1": (-7.62, 0), "2": (7.62, 0)},
        lib_symbol(
            f"{pfx}:LOOP",
            [("1", "1", -7.62, 0, 2.54, 0), ("2", "2", 7.62, 0, 2.54, 180)],
            poly((-5.08, 0), (-3.81, 2.54), (-1.27, -2.54), (1.27, 2.54), (3.81, -2.54), (5.08, 0)),
            hide_pin_names=True,
        ),
    )
    add_lib(
        f"{pfx}:Crystal",
        {"1": (-3.81, 0), "2": (3.81, 0)},
        f'''(symbol "{pfx}:Crystal"
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
)''',
    )
    add_lib(
        f"{pfx}:+5V",
        {"1": (0, 0)},
        f'''(symbol "{pfx}:+5V"
\t(power)
\t(pin_numbers (hide yes))
\t(pin_names (offset 0) (hide yes))
\t(exclude_from_sim no)
\t(in_bom yes)
\t(on_board yes)
\t(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Value" "+5V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t(symbol "+5V_0_1"
\t\t(polyline (pts (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
\t\t(polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
\t)
\t(symbol "+5V_1_1"
\t\t(pin power_in line (at 0 0 90) (length 0) (name "+5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t)
)''',
    )
    add_lib(
        f"{pfx}:GND",
        {"1": (0, 0)},
        f'''(symbol "{pfx}:GND"
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
)''',
    )
    add_lib(
        f"{pfx}:PWR_FLAG",
        {"1": (0, 0)},
        f'''(symbol "{pfx}:PWR_FLAG"
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
)''',
    )

    side = ((3.81, -1.27), (3.81, 1.27), "left")
    text_pos = {
        f"{pfx}:R": side,
        f"{pfx}:C": side,
        f"{pfx}:CP": side,
        f"{pfx}:Q_NPN": ((4.0, 6.0), (4.0, -6.0), "left"),
        f"{pfx}:Q_PNP": ((4.0, 6.0), (4.0, -6.0), "left"),
        f"{pfx}:POT": ((0, 6.0), (0, -8.0), ""),
        f"{pfx}:F": ((3.81, -5.08), (3.81, 5.08), "left"),
        f"{pfx}:JUMP": ((0, 3.81), (0, -3.81), ""),
        f"{pfx}:LOOP": ((0, -5.08), (0, 5.08), ""),
        f"{pfx}:Crystal": ((0, 5.08), (0, -5.08), ""),
        f"{pfx}:+5V": ((0, 5.08), (0, 5.08), ""),
        f"{pfx}:GND": ((0, 5.08), (0, 5.08), ""),
        f"{pfx}:PWR_FLAG": ((0, -5.08), (0, -5.08), ""),
    }
    return libs, tips, text_pos


C_5V = (29, 78, 216, 0.3)
C_GND = (55, 65, 81, 0.15)
C_RF = (21, 128, 61, 0.25)
C_BIAS = (180, 83, 9, 0.25)
C_OSC = (14, 116, 144, 0.2)
C_IO = (67, 56, 202, 0.2)
C_TRIM = (162, 28, 175, 0.2)


class Sch:
    def __init__(self, pfx: str, out: Path, name: str, title: str, comments: list[str]):
        self.pfx = pfx
        self.out = out
        self.name = name
        self.title = title
        self.comments = comments
        self.libs, self.tips, self.text_pos = common_symbols(pfx)
        self.inst: list[dict] = []
        self.wires: list[tuple] = []
        self.texts: list[tuple] = []
        self._pwr = 0
        self._flg = 0
        self._vcc = 0

    def P(self, x, y):
        return (round(x, 2), round(y, 2))

    def add(self, lib, ref, value, x, y):
        if ":" not in lib:
            lib = f"{self.pfx}:{lib}"
        pins = {n: uid() for n in self.tips[lib]}
        inst = {"lib": lib, "ref": ref, "value": value, "x": x, "y": y, "uuid": uid(), "pins": pins}
        self.inst.append(inst)
        return inst

    def extra_lib(self, fullname, pinmap, text, text_pos):
        self.tips[fullname] = pinmap
        self.libs.append(text)
        self.text_pos[fullname] = text_pos

    def tip(self, inst, n):
        ox, oy = self.tips[inst["lib"]][str(n)]
        return self.P(inst["x"] + ox, inst["y"] - oy)

    def W(self, *pts, c=C_GND):
        pts = [self.P(*p) for p in pts]
        for a, b in zip(pts, pts[1:]):
            if a == b:
                continue
            if a[0] != b[0] and a[1] != b[1]:
                raise SystemExit(f"diagonal wire {a} -> {b}")
            self.wires.append((a, b, c))

    def T(self, s, p, size=1.27, justify="left bottom"):
        self.texts.append((s, self.P(*p), size, justify))

    def num(self, n, a, b):
        a, b = self.P(*a), self.P(*b)
        if a[1] == b[1]:
            self.T(f"[{n}]", ((a[0] + b[0]) / 2, a[1] - 0.508), 1.0, "bottom")
        else:
            self.T(f"[{n}]", (a[0] + 0.762, (a[1] + b[1]) / 2), 1.0, "left")

    def gnd(self, p, dy=2.54):
        self._pwr += 1
        end = self.P(p[0], p[1] + dy)
        self.W(p, end)
        self.add("GND", f"#PWR{self._pwr:02d}", "GND", end[0], end[1])

    def vcc(self, p, dy=-2.54):
        self._vcc += 1
        end = self.P(p[0], p[1] + dy)
        self.W(p, end, c=C_5V)
        self.add("+5V", f"#PWRV{self._vcc:02d}", "+5V", end[0], end[1])

    def flag(self, p):
        self._flg += 1
        self.add("PWR_FLAG", f"#FLG{self._flg:02d}", "PWR_FLAG", p[0], p[1])

    def finalize(self):
        tips = [self.tip(i, n) for i in self.inst for n in self.tips[i["lib"]]]
        poi = set(tips) | {p for a, b, _ in self.wires for p in (a, b)}
        out = []
        for a, b, col in self.wires:
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

    def write(self):
        wires, junctions = self.finalize()
        parts = [
            "(kicad_sch",
            "\t(version 20231120)",
            '\t(generator "eeschema")',
            '\t(generator_version "8.0")',
            f'\t(uuid "{uid()}")',
            '\t(paper "A3")',
            "\t(title_block",
            f'\t\t(title "{esc(self.title)}")',
            '\t\t(date "2026-11-01")',
            '\t\t(rev "1")',
            '\t\t(company "CyclingHourglass")',
        ]
        for i, c in enumerate(self.comments, 1):
            parts.append(f'\t\t(comment {i} "{esc(c)}")')
        parts += ["\t)", "\t(lib_symbols"]
        for lib in self.libs:
            for line in lib.splitlines():
                parts.append("\t\t" + line)
        parts.append("\t)")
        for a, b, (r, g, bl, width) in wires:
            parts.append(
                f"\t(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))"
                f" (stroke (width {width}) (type default) (color {r} {g} {bl} 1))"
                f' (uuid "{uid()}"))'
            )
        for j in junctions:
            parts.append(
                f'\t(junction (at {j[0]} {j[1]}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))'
            )
        for s, (x, y), size, justify in self.texts:
            parts.append(
                f'\t(text "{esc(s)}" (exclude_from_sim no) (at {x} {y} 0)'
                f' (effects (font (size {size} {size})) (justify {justify})) (uuid "{uid()}"))'
            )
        for inst in self.inst:
            parts.append(self._emit_inst(inst))
        parts.append('\t(sheet_instances\n\t\t(path "/" (page "1"))\n\t)')
        parts.append(")")
        self.out.mkdir(parents=True, exist_ok=True)
        sch = self.out / f"{self.name}.kicad_sch"
        sch.write_text("\n".join(parts) + "\n", encoding="utf-8")
        pro = {
            "board": {"design_settings": {"defaults": {}, "rules": {}}, "layer_presets": [], "viewports": []},
            "boards": [],
            "cvpcb": {"equivalence_files": []},
            "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
            "meta": {"filename": f"{self.name}.kicad_pro", "version": 1},
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
        (self.out / f"{self.name}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n")
        sym = ["(kicad_symbol_lib", "\t(version 20231120)", '\t(generator "cyclinghourglass")']
        for lib in self.libs:
            for line in lib.replace(f'(symbol "{self.pfx}:', '(symbol "', 1).splitlines():
                sym.append("\t" + line)
        sym.append(")")
        (self.out / f"{self.name}.kicad_sym").write_text("\n".join(sym) + "\n")
        self._write_lib_table()
        print(f"Wrote {sch} inst={len(self.inst)} wires={len(wires)} junc={len(junctions)}")

    def _write_lib_table(self) -> None:
        table = self.out / "sym-lib-table"
        libs = {
            "LoopAmp": "LoopAmplifier.kicad_sym",
            "Decoder": "Decoder.kicad_sym",
        }
        if table.exists():
            text = table.read_text()
            for name, fn in libs.items():
                if f'(name "{name}")' in text and "(type \"KiCad\")" in text:
                    continue
            # rewrite cleanly each time
        lines = ["(sym_lib_table", "\t(version 7)"]
        for name, fn in libs.items():
            if (self.out / fn).exists() or name == self.pfx:
                lines.append(
                    f'\t(lib (name "{name}") (type "KiCad") '
                    f'(uri "${{KIPRJMOD}}/{fn}") (options "") (descr ""))'
                )
        lines.append(")")
        table.write_text("\n".join(lines) + "\n")

    def _emit_inst(self, inst):
        lib = inst["lib"]
        is_pwr = lib.endswith(":GND") or lib.endswith(":PWR_FLAG") or lib.endswith(":+5V")
        ref_hide = " (hide yes)" if is_pwr else ""
        val_hide = " (hide yes)" if lib.endswith(":PWR_FLAG") else ""
        (rdx, rdy), (vdx, vdy), just = self.text_pos[lib]
        justify = f" (justify {just})" if just else ""
        ref_at = self.P(inst["x"] + rdx, inst["y"] + rdy)
        val_at = self.P(inst["x"] + vdx, inst["y"] + vdy)
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
