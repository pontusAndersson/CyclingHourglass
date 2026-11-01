"""SVG overview helpers (ShockRemote / Transponder style)."""

from __future__ import annotations

import subprocess
from pathlib import Path

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
C_TRIM = "#a21caf"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class Svg:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts: list[str] = []

    def add(self, s: str) -> None:
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, stroke=INK, sw=2.0, rx=8):
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, s, size=13, fill=INK, weight="400", anchor="start", mono=False):
        ff = MONO if mono else FONT
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-family="{ff}" '
            f'font-size="{size}" font-weight="{weight}">{esc(s)}</text>'
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
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">\n'
            + "\n".join(self.parts)
            + "\n</svg>\n"
        )


def header(s: Svg, title: str, sub: str, legend: list[tuple[str, str]]):
    s.add(f'<rect width="{s.w}" height="{s.h}" fill="{BG}"/>')
    s.rect(0, 0, s.w, 78, INK, INK, 0, 0)
    s.text(40, 34, title, 26, "#f9fafb", "700")
    s.text(40, 58, sub, 14, "#d1d5db")
    for i, (col, name) in enumerate(legend):
        lx = 40 + i * 210
        s.path(f"M{lx},102 H{lx + 26}", col, 4)
        s.text(lx + 33, 106, name, 11, "#374151", "600", mono=True)


def wire(s: Svg, color, *pts, width=3.0):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    s.path(d, color, width)


def badge(s: Svg, n, x, y, color):
    label = str(n)
    w = 10 + 8 * len(label)
    s.rect(x - w / 2, y - 9, w, 18, PAPER, color, 1.8, 9)
    s.text(x, y + 4, label, 11, color, "700", "middle", mono=True)


def gnd(s: Svg, x, y, n=None):
    s.path(f"M{x},{y} V{y + 14}", C_GND, 2.4)
    for i, half in enumerate((11, 7, 3)):
        yy = y + 14 + i * 4
        s.path(f"M{x - half},{yy} H{x + half}", C_GND, 2.2)
    if n is not None:
        badge(s, n, x + 26, y + 18, C_GND)


class Box:
    def __init__(self, s: Svg, x, y, w, h, title, color, sub=""):
        self.s, self.x, self.y, self.w, self.h, self.color = s, x, y, w, h, color
        s.rect(x, y, w, h, PAPER, INK, 2.0, 10)
        s.rect(x, y, w, 26, color, color, 0, 10)
        s.rect(x, y + 14, w, 12, color, color, 0, 0)
        s.text(x + w / 2, y + 18, title, 13, PAPER, "700", "middle")
        if sub:
            s.text(x + w / 2, y + h - 9, sub, 11, MUTED, "400", "middle")

    def left(self, name, y):
        self.s.dot(self.x, y, self.color)
        self.s.text(self.x + 10, y + 4, name, 12, INK, "600", mono=True)
        return (self.x, y)

    def right(self, name, y):
        self.s.dot(self.x + self.w, y, self.color)
        self.s.text(self.x + self.w - 10, y + 4, name, 12, INK, "600", "end", mono=True)
        return (self.x + self.w, y)

    def top(self, name, x):
        self.s.dot(x, self.y, self.color)
        self.s.text(x, self.y + 42, name, 12, INK, "600", "middle", mono=True)
        return (x, self.y)

    def bottom(self, name, x):
        self.s.dot(x, self.y + self.h, self.color)
        self.s.text(x, self.y + self.h - 10, name, 12, INK, "600", "middle", mono=True)
        return (x, self.y + self.h)


def resistor_h(s: Svg, x_left, y, ref, value, color):
    s.path(f"M{x_left},{y} H{x_left + 8} M{x_left + 48},{y} H{x_left + 56}", color, 2.4)
    s.rect(x_left + 8, y - 8, 40, 16, PAPER, color, 2.2, 3)
    s.text(x_left + 28, y - 16, f"{ref}  {value}", 12, INK, "700", "middle")
    return (x_left, y), (x_left + 56, y)


def capacitor(s: Svg, x, y_top, ref, value, color):
    s.path(f"M{x},{y_top} V{y_top + 16} M{x},{y_top + 24} V{y_top + 40}", color, 2.4)
    s.path(f"M{x - 12},{y_top + 16} H{x + 12}", color, 3.2)
    s.path(f"M{x - 12},{y_top + 24} H{x + 12}", color, 3.2)
    s.text(x + 18, y_top + 17, ref, 12, INK, "700")
    s.text(x + 18, y_top + 32, value, 12, MUTED, "400")
    return (x, y_top), (x, y_top + 40)


def table(s: Svg, rows, ty, title):
    half = (len(rows) + 1) // 2
    h = 86 + half * 26 + 24
    s.rect(40, ty, s.w - 80, h, PAPER, INK, 2, 12)
    s.rect(40, ty, s.w - 80, 36, INK, INK, 0, 12)
    s.rect(40, ty + 18, s.w - 80, 18, INK, INK, 0, 0)
    s.text(s.w / 2, ty + 24, title, 16, "#f9fafb", "700", "middle")
    for col, ox in enumerate((60, 40 + (s.w - 80) / 2 + 20)):
        s.text(ox, ty + 60, "#", 12, MUTED, "700", mono=True)
        s.text(ox + 44, ty + 60, "Net", 12, MUTED, "700", mono=True)
        s.text(ox + 140, ty + 60, "Från → Till", 12, MUTED, "700")
        s.text(ox + 400, ty + 60, "Tips", 12, MUTED, "700")
        for i, (n, colr, net, route, tip) in enumerate(rows[col * half : (col + 1) * half]):
            y = ty + 86 + i * 26
            s.rect(ox - 4, y - 12, 34, 17, colr, colr, 0, 4)
            s.text(ox + 13, y + 1, n, 11, PAPER, "700", "middle", mono=True)
            s.text(ox + 44, y + 1, net, 11, colr, "700", mono=True)
            s.text(ox + 140, y + 1, route, 12, INK, "400")
            s.text(ox + 400, y + 1, tip, 11, MUTED, "400")


def svg_to_png(svg_path: Path, png_path: Path, w: int, h: int) -> None:
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
                f"--window-size={w},{h}",
                "--default-background-color=00000000",
                f"file://{html}",
            ],
            check=True,
            capture_output=True,
        )
        html.unlink(missing_ok=True)
        return
    subprocess.run(
        ["qlmanage", "-t", "-s", str(max(w, h)), "-o", str(png_path.parent), str(svg_path)],
        check=True,
        capture_output=True,
    )
    produced = png_path.parent / (svg_path.name + ".png")
    if produced.exists() and produced != png_path:
        produced.rename(png_path)
