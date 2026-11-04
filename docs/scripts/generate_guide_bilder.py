#!/usr/bin/env python3
"""Generate the diagrams used by the walkthroughs in docs/."""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Schematic" / "Decoder" / "scripts"))

from svglib import (  # noqa: E402
    BG,
    C_5V,
    C_GND,
    C_ICSP,
    C_LED,
    C_OSC,
    C_TX,
    C_VIN,
    INK,
    MUTED,
    PAPER,
    Svg,
    svg_to_png,
    wire,
)

OUT = ROOT / "docs" / "bilder"
C_USB = "#0f766e"
C_WARN = "#b91c1c"


def title_bar(s: Svg, title: str, sub: str) -> None:
    s.add(f'<rect width="{s.w}" height="{s.h}" fill="{BG}"/>')
    s.rect(0, 0, s.w, 78, INK, INK, 0, 0)
    s.text(40, 34, title, 26, "#f9fafb", "700")
    s.text(40, 58, sub, 14, "#d1d5db")


def card(s: Svg, x, y, w, h, title, color, lines=(), size=13):
    s.rect(x, y, w, h, PAPER, INK, 2.0, 10)
    s.rect(x, y, w, 30, color, color, 0, 10)
    s.rect(x, y + 16, w, 14, color, color, 0, 0)
    s.text(x + w / 2, y + 21, title, 14, PAPER, "700", "middle")
    for i, line in enumerate(lines):
        s.text(x + 14, y + 54 + i * 20, line, size, INK)


def arrow(s: Svg, x1, y1, x2, y2, color, label="", dashed=False, width=3.0):
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    s.add(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round"{dash}/>'
    )
    a = math.atan2(y2 - y1, x2 - x1)
    for side in (-1, 1):
        ax = x2 - 12 * math.cos(a + side * 0.45)
        ay = y2 - 12 * math.sin(a + side * 0.45)
        s.path(f"M{x2},{y2} L{ax:.1f},{ay:.1f}", color, width)
    if label:
        s.text((x1 + x2) / 2, (y1 + y2) / 2 - 10, label, 12, color, "700", "middle")


CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def render_png(svg: Path, png: Path, w: int, h: int) -> None:
    if not CHROME.exists():
        svg_to_png(svg, png, w, h)
        return
    html = svg.with_suffix(".html")
    html.write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>html,body{{margin:0;overflow:hidden;background:{BG}}}</style></head><body>"
        + svg.read_text(encoding="utf-8")
        + "</body></html>",
        encoding="utf-8",
    )
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--screenshot={png}",
            f"--window-size={w},{h}",
            f"file://{html}",
        ],
        check=True,
        capture_output=True,
    )
    html.unlink(missing_ok=True)


def save(s: Svg, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    svg = OUT / f"{name}.svg"
    svg.write_text(s.build(), encoding="utf-8")
    render_png(svg, OUT / f"{name}.png", s.w, s.h)
    print(f"Wrote {OUT / name}.png")


def systemkedja() -> None:
    s = Svg(1200, 560)
    title_bar(s, "CyclingHourglass — hela kedjan", "Datorn pratar bara med dekodern. Transpondern har ingen kabel till datorn.")

    card(s, 40, 120, 210, 150, "Transponder", C_LED, ["AndreasM V3 på cykeln", "Batteri 6–8,4 V på J1", "Sänder sitt nummer"])
    card(s, 300, 120, 170, 150, "Slinga", C_TX, ["En tråd över", "mållinjen", "flytande, ej jordad"])
    card(s, 520, 120, 190, 150, "Loop amplifier", C_VIN, ["Cano Rev B", "J1 = slingan", "J2 = koax ut"])
    card(s, 760, 120, 190, 150, "Dekoder", C_ICSP, ["PDIA + CY8CKIT-059", "Firmware v0.10", "COM-port via USB"])
    card(s, 1000, 120, 160, 150, "Dator", C_5V, ["Manager", "ZRound / LAPS", "eller PuTTY"])

    s.text(275, 190, "≈ ≈", 22, C_TX, "700", "middle")
    s.text(275, 215, "magnetiskt", 11, C_TX, "600", "middle")
    arrow(s, 470, 195, 518, 195, C_TX)
    arrow(s, 710, 195, 758, 195, C_VIN, "koax")
    s.text(734, 232, "5 V phantom", 11, C_VIN, "600", "middle")
    s.text(734, 248, "tillbaka", 11, C_VIN, "600", "middle")
    arrow(s, 950, 195, 998, 195, C_USB, "USB")
    s.text(974, 232, "micro-USB", 11, C_USB, "600", "middle")
    s.text(974, 248, "PSoC-sidan", 11, C_USB, "600", "middle")

    s.rect(40, 310, 1120, 220, PAPER, MUTED, 1.5, 12)
    s.text(60, 340, "Bara när du programmerar", 16, INK, "700")

    card(s, 60, 360, 250, 140, "PICkit / MPLAB Snap", C_ICSP, ["USB till datorn", "5 trådar till transpondern"])
    arrow(s, 310, 430, 420, 430, C_ICSP, "ICSP")
    card(s, 420, 360, 220, 140, "Transponder", C_LED, ["Undersidans dynor", "VPP CLK DAT +V GND"])
    s.text(80, 476, "Guide 1", 12, MUTED, "700")

    card(s, 700, 360, 220, 140, "KitProg (USB-A)", C_USB, ["Vänstra delen av", "CY8CKIT-059"])
    arrow(s, 920, 430, 1000, 430, C_USB, "flash")
    card(s, 1000, 360, 140, 140, "PSoC 5LP", C_ICSP, ["Dekoderns", "hjärna"])
    s.text(720, 476, "Guide 2", 12, MUTED, "700")

    save(s, "systemkedja")


def transponder_icsp() -> None:
    s = Svg(1200, 640)
    title_bar(s, "Guide 1 — koppla PICkit / Snap till transpondern", "5 dupont-trådar. Stift 1 på programmeraren har en pil ▲ på höljet.")

    hx, hy, hw = 70, 130, 300
    s.rect(hx, hy, hw, 400, PAPER, INK, 2, 12)
    s.rect(hx, hy, hw, 32, C_ICSP, C_ICSP, 0, 12)
    s.rect(hx, hy + 16, hw, 16, C_ICSP, C_ICSP, 0, 0)
    s.text(hx + hw / 2, hy + 22, "PICkit 4/5 · MPLAB Snap", 15, PAPER, "700", "middle")
    s.text(hx + 20, hy + 58, "8-stifts kontakt (ICSP)", 12, MUTED, "600")

    pins = [
        ("1", "▲ MCLR / VPP", C_ICSP, "VPP"),
        ("2", "VDD (target)", C_5V, "+V"),
        ("3", "GND", C_GND, "GND"),
        ("4", "PGD  = data", C_TX, "DAT"),
        ("5", "PGC  = klocka", C_OSC, "CLK"),
        ("6", "—", MUTED, ""),
        ("7", "—", MUTED, ""),
        ("8", "—", MUTED, ""),
    ]
    for i, (n, name, col, pad) in enumerate(pins):
        y = hy + 90 + i * 38
        s.rect(hx + hw - 34, y - 12, 24, 24, "#d4d4d8" if pad else "#f4f4f5", INK, 1.5, 3)
        s.text(hx + hw - 22, y + 5, n, 12, INK, "700", "middle", mono=True)
        s.text(hx + 20, y + 5, name, 13, col if pad else MUTED, "700" if pad else "400", mono=True)
        if pad:
            wire(s, col, (hx + hw - 10, y), (hx + hw + 60, y), width=3.4)
            s.rect(hx + hw + 60, y - 13, 120, 26, col, col, 0, 13)
            s.text(hx + hw + 120, y + 5, f"→ {pad}-dynan", 12, PAPER, "700", "middle")
    s.text(hx + 20, hy + 392, "Stift 6–8 kopplas inte in.", 12, MUTED)

    bx, by, bw, bh = 640, 130, 480, 400
    s.rect(bx, by, bw, bh, "#3b1d5e", INK, 2, 14)
    for k in range(5):
        inset = 10 + k * 9
        s.rect(bx + inset, by + inset, bw - 2 * inset, bh - 2 * inset, "none", "#b08a3e", 2, 10)
    s.text(bx + bw / 2, by + 90, "TransponderV3 — UNDERSIDAN", 15, "#f3e8ff", "700", "middle")
    s.text(bx + bw / 2, by + 112, "(sidan med kopparslingan)", 12, "#e9d5ff", "400", "middle")
    s.text(bx + bw / 2, by + 134, "dynorna i den här ordningen, vänster → höger", 12, "#e9d5ff", "400", "middle")

    pads = [("VPP", "1", C_ICSP), ("CLK", "5", C_OSC), ("DAT", "4", C_TX), ("+V", "2", C_5V), ("GND", "3", C_GND)]
    pad_y = by + 160
    for i, (name, pin, col) in enumerate(pads):
        x = bx + 90 + i * 75
        s.rect(x - 18, pad_y, 36, 76, "#c08457", "#7c4a1e", 1.5, 3)
        s.add(
            f'<text x="{x + 5}" y="{pad_y + 38}" fill="#1c1917" font-family="Menlo, monospace" font-size="13" '
            f'font-weight="700" text-anchor="middle" transform="rotate(90 {x + 5} {pad_y + 38})">{name}</text>'
        )
        wire(s, col, (x, pad_y + 76), (x, pad_y + 120), width=3.4)
        s.rect(x - 32, pad_y + 120, 64, 44, col, col, 0, 10)
        s.text(x, pad_y + 138, "stift", 11, PAPER, "600", "middle")
        s.text(x, pad_y + 156, pin, 15, PAPER, "700", "middle", mono=True)

    s.rect(70, 556, 520, 66, PAPER, C_5V, 2, 10)
    s.text(86, 580, "PICkit 4/5: får mata kortet (Power target 5,0 V).", 13, INK, "700")
    s.text(86, 602, "Inget batteri på J1 samtidigt.", 13, C_WARN, "700")
    s.rect(620, 556, 540, 66, PAPER, C_VIN, 2, 10)
    s.text(636, 580, "MPLAB Snap: kan inte mata kortet.", 13, INK, "700")
    s.text(636, 602, "Sätt batteri 6–8,4 V på J1 (ovansidan) under programmeringen.", 13, C_VIN, "700")

    save(s, "transponder_icsp")


def cy8ckit() -> None:
    s = Svg(1200, 600)
    title_bar(s, "Guide 2 — CY8CKIT-059 har två halvor", "Vänster halva programmerar. Höger halva är själva dekodern.")

    y0, h = 170, 170
    s.rect(70, y0 + 45, 60, 80, "#d1d5db", INK, 2, 4)
    for k in range(4):
        s.rect(78, y0 + 55 + k * 17, 44, 9, "#f59e0b", "#92400e", 1, 2)
    s.text(100, y0 + 150, "USB-A", 12, INK, "700", "middle")

    s.rect(130, y0, 330, h, "#1f2937", INK, 2, 8)
    s.text(295, y0 + 40, "KitProg", 22, "#f9fafb", "700", "middle")
    s.text(295, y0 + 66, "(inbyggd programmerare)", 13, "#d1d5db", "400", "middle")
    s.rect(240, y0 + 85, 110, 55, "#111827", "#6b7280", 1.5, 4)
    s.text(295, y0 + 118, "PSoC 5LP", 11, "#9ca3af", "400", "middle")

    s.path(f"M470,{y0 - 10} V{y0 + h + 10}", C_WARN, 2.5)
    s.add(
        f'<line x1="470" y1="{y0 - 10}" x2="470" y2="{y0 + h + 10}" stroke="{BG}" stroke-width="2.5" stroke-dasharray="4 8"/>'
    )
    s.text(470, y0 - 20, "perforering", 12, C_WARN, "700", "middle")

    swd = ["SWDIO", "SWDCLK", "RST/XRES", "GND", "VTARG"]
    for i, name in enumerate(swd):
        y = y0 + 22 + i * 27
        s.rect(446, y - 7, 14, 14, "#fbbf24", INK, 1, 2)
        s.rect(480, y - 7, 14, 14, "#fbbf24", INK, 1, 2)
        s.text(504, y + 5, name, 11, "#f9fafb", "600", mono=True)

    s.rect(470, y0, 600, h, "#1f2937", INK, 2, 8)
    for i, name in enumerate(swd):
        y = y0 + 22 + i * 27
        s.rect(480, y - 7, 14, 14, "#fbbf24", INK, 1, 2)
        s.text(504, y + 5, name, 11, "#f9fafb", "600", mono=True)
    s.text(800, y0 + 40, "PSoC 5LP (target)", 22, "#f9fafb", "700", "middle")
    s.text(800, y0 + 66, "kör RC Hourglass-firmware", 13, "#d1d5db", "400", "middle")
    s.rect(740, y0 + 85, 120, 60, "#111827", "#6b7280", 1.5, 4)
    s.text(800, y0 + 120, "CY8C5888", 11, "#9ca3af", "400", "middle")
    for x in range(600, 1050, 18):
        s.dot(x, y0 + 8, "#fbbf24", 3.2)
        s.dot(x, y0 + h - 8, "#fbbf24", 3.2)
    s.text(985, y0 + 120, "P12_2 / P12_3", 11, "#a5b4fc", "600", "middle", mono=True)
    s.text(985, y0 + 138, "P15_0 / P15_1", 11, "#67e8f9", "600", "middle", mono=True)

    s.rect(1070, y0 + 60, 50, 50, "#9ca3af", INK, 2, 6)
    s.rect(1080, y0 + 76, 30, 18, "#374151", INK, 1, 3)
    s.text(1095, y0 + h + 24, "micro-USB", 12, INK, "700", "middle")

    card(s, 70, 390, 470, 180, "Vänster: KitProg + USB-A", C_USB, [
        "Används för att FLASHA firmware.",
        "Stick USB-A direkt i datorn (ingen kabel).",
        "PSoC Programmer hittar ”KitProg”.",
        "Matar inte analogkortet i drift.",
    ])
    card(s, 600, 390, 520, 180, "Höger: PSoC 5LP + micro-USB", C_ICSP, [
        "Används i DRIFT: ström + COM-port till datorn.",
        "Sitter i analogkortet (PDIA).",
        "Flashar inte firmware.",
        "Brutna isär? Koppla 5 SWD-stift 1:1 (gula).",
    ])
    save(s, "cy8ckit059")


def programvara() -> None:
    s = Svg(1200, 520)
    title_bar(s, "Guide 3 — ett program i taget på COM-porten", "Stäng det ena innan du öppnar det andra. Annars: ”port busy” eller inga svar.")

    card(s, 40, 170, 220, 160, "Dekoder", C_ICSP, ["micro-USB (PSoC-sidan)", "Windows: COMx", "Mac: /dev/cu.usbmodem…"])
    arrow(s, 260, 250, 340, 250, C_USB, "USB")
    s.rect(340, 200, 120, 100, PAPER, C_USB, 2.5, 50)
    s.text(400, 246, "COM-", 15, C_USB, "700", "middle")
    s.text(400, 266, "port", 15, C_USB, "700", "middle")

    rows = [
        ("PuTTY / terminal", C_GND, "Test: VERSION, LICENSE, se passager", "115200 8N1"),
        ("RCHourglass Manager", C_ICSP, "Ställ in läge (CANO / AMBRC), ID, LED/summer", "Windows"),
        ("Varvprogram", C_TX, "ZRound / FlipSide = CANO · Everlaps, Alycat m.fl. = AMBRC", "under lopp"),
    ]
    for i, (name, col, desc, tag) in enumerate(rows):
        y = 120 + i * 130
        arrow(s, 460, 250, 560, y + 50, col, dashed=i != 0)
        s.rect(560, y, 600, 100, PAPER, col, 2.2, 10)
        s.rect(560, y, 12, 100, col, col, 0, 6)
        s.text(590, y + 36, name, 17, INK, "700")
        s.text(590, y + 64, desc, 13, INK)
        s.text(1140, y + 36, tag, 12, MUTED, "700", "end", mono=True)
    s.text(40, 380, "Bara EN av de tre", 16, C_WARN, "700")
    s.text(40, 404, "får ha porten öppen.", 16, C_WARN, "700")
    save(s, "programvara")


if __name__ == "__main__":
    systemkedja()
    transponder_icsp()
    cy8ckit()
    programvara()
