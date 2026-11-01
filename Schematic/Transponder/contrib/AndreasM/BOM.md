# TransponderV3 BOM

**Den här listan är bara för AndreasM TransponderV3** (OSH Park, 4 lager, 19,5 × 19,6 mm). Bygginstruktion: [wiki/TransponderBuild.md](../../../../wiki/TransponderBuild.md#andreasm-transponderv3-smd-kretskort).

Den är **inte** för:

| Variant | Varför inte |
| --- | --- |
| Officiellt perfboard | Annan kretsbyggnad: LP2950, Q1 VP2106, DIP-sockel, lindad antenn, polariserade C1/C2 |
| AndreasM **TransponderV2** | Samma krets, andra referenser. På V2 är avstämningen **C4**, inte C5 |
| WBorek EasyEDA | 3,3 V-regulator, C5 68 pF, R1 65 Ω, extra knapp |

Parts as ordered from [TME](https://www.tme.eu/se/) (order **35407144**). Enough for **4 boards**. Part references match the official GitHub schematic and the [OSH Park TransponderV3](https://oshpark.com/profiles/AndreasM) PCB.

Source CSV: [TME-order-35407144.csv](TME-order-35407144.csv).

| Per board | Ordered | Ref | TME / MPN | What it is | Package |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | U2 | [PIC16F18313-I/SN](https://www.tme.eu/se/details/pic16f18313-i_sn/8-bit-pic-family/microchip-technology/) | PIC, 3.5 kB Flash | SOIC-8 |
| 1 | 4 | U1 | [MCP1702T-5002E/CB](https://www.tme.eu/se/details/mcp1702t-5002e_cb/) | LDO **5.0 V**, 250 mA | SOT-23 |
| 1 | 4 | Y1 | [5.00M-SMDHC49R](https://www.tme.eu/se/details/5.00m-smdhc49r/) (IQD LFXTAL012312BULK) | 5.000 MHz, 30 pF, HC-49 SMD | Crystal_SMD |
| 1 | 10 | D1 | [LTST-C150KRKT](https://www.tme.eu/se/details/ltst-c150krkt/led-smd-dioder-fargare/liteon/) | Red LED | 1206 |
| 2 | 10 | R2, R3 | [WR08X1000FTL](https://www.tme.eu/se/details/wr08x1000ftl/) | 100 Ω 1 % | 0805 |
| 1 | 10 | R1 | [ERJP06F1501V](https://www.tme.eu/se/details/erjp06f1501v/) | 1.5 kΩ 1 % | 0805 |
| 2 | 10 | C1, C2 | [CL21A106MPFNNNE](https://www.tme.eu/se/details/cl21a106mpfnnne/) | 10 µF 10 V X5R | 0805 |
| 2 | 10 | C3, C4 | [C0805C200J5GACTU](https://www.tme.eu/se/details/c0805c200j5gactu/) | 20 pF 50 V C0G | 0805 |
| 1 | 10 | C6 | [VJ0805A470GXCAC](https://www.tme.eu/se/details/vj0805a470gxcac/) | 47 pF C0G | 0805 |
| 1 | 10 | C5 | [0805N151J500CT](https://www.tme.eu/se/details/0805n151j500ct/) | **150 pF** 50 V C0G (130 pF substitute) | 0805 |
| — | 10 | C5 alt. | [CL21C101JC61PNC](https://www.tme.eu/se/details/cl21c101jc61pnc/) | **100 pF** C0G, spare for TX tune | 0805 |
| 1 | — | PCB | TransponderV3, 4-layer, 19.5 × 19.6 mm | [OSH Park](https://oshpark.com/profiles/AndreasM) | |

### Notes

- **C5:** schematic says ~130 pF. This order uses **150 pF**; **100 pF** is extra if range is poor (swap and compare over the loop). Both C0G.
- **C1, C2:** 10 V rating. Fine on the 5 V rail. If VIN is 2S LiPo (8.4 V), that is close to the limit — keep the input cap on the 5 V side of the LDO if in doubt.
- **Y1:** 30 pF load crystal with 20 pF C3/C4. Close enough for this circuit; do not use a through-hole HC-49S.
- PIC must be **SOIC-8** (`…/SN`), not Electrokit DIP-8 (`…/P`).

**Not on this board:** buzzer, SMA, screw terminals, 4.87 kΩ / 1.21 kΩ, SS8050/SS8550, NE592, 1N4148.

Firmware: `Firmware/Transponder/`. Program via **VPP, CLK, DAT, +V, GND**.

Power: typically 6–8.4 V into the LDO (MCP1702 max Vin 13.2 V).
