# Transponder build instructions

This instruction will guide you through building a transponder to use in the car.

The PIC chip used in the transponder can be programmed with the decoder optional programmer hardware or Microchip tools.

# Vilken variant?

Det finns mer än ett transponderbygge i det här repot. Använd rätt kapitel och rätt komponentlista.

| Variant | Kapitel | Komponentlista |
| --- | --- | --- |
| **AndreasM TransponderV3** (OSH Park, SMD, 4 lager) | [AndreasM TransponderV3](#andreasm-transponderv3-smd-kretskort) | [contrib/AndreasM/BOM.md](../Schematic/Transponder/contrib/AndreasM/BOM.md) |
| Officiellt perfboard (hålmonterat) | [Perfboard](#perfboard-officiellt-genom-hålsbygge) | Ingen separat BOM. Följ fotona och [GitHub-schemat](../Schematic/Transponder/RCHourglassTransponder.sch.svg) |
| AndreasM Transponder**V2** | — | **Använd inte** V3-BOM:en. Samma krets, andra referenser (antennkondingen heter **C4** på V2) |
| WBorek EasyEDA | — | **Inte** V3-BOM:en. Annan matning (3,3 V) och andra värden |

[BOM.md](../Schematic/Transponder/contrib/AndreasM/BOM.md) (TME-order **35407144**) är **bara** för AndreasM **TransponderV3**.

# Perfboard (officiellt genom-hålsbygge)

# General building tips

The project can be built on perfboard. The critical part for manual assembly is winding the spiral antenna. The circuit itself is very simple.

## Step 1.

This is the schematic for the transponder:

[[https://github.com/mv4wd/RCHourglass/blob/master/Schematic/Transponder/RCHourglassTransponder.sch.svg|alt=RCHourglass transponder schematic]]

Cut a small piece of perfboard 7 holes *  11 holes (standard 0.1 inch). Notice in the image the two larger holes drilled for the servo wire.

![Transponder build step 1](./images/TransponderBuild/Transponder_1.jpg)

Install the chip socket and solder the **5MHz** crystal and the two capacitors **C3** and **C4**. The chip is held in place by the solder on pins 2 and 3. Leave the other pin of C3 and C4 unsoldered.


![Transponder build step 2](./images/TransponderBuild/Transponder_2.jpg)

Mount all the power supply components:

* the P Mosfet **Q1** VP2106N3-G
* the low drop regulator **U1** LP2950
* the two filter capacitors **C1** and **C2** - **CHECK THE POLARITY**

Leave the ground pins unconnected, and solder all the others. Pin 1 of the chip socket will be soldered as well. Leave unconnected the two input pins of **Q1** as in the image:

![Transponder build step 3](./images/TransponderBuild/Transponder_3.jpg)

Mount the LED and the limiting resistor **R1**. Use a piece of shinrk tube around R1 and led pins to avoid rubbing against the antenna wire. Align one terminal of the LED to the teriminals of capacitors *C3* and *C4*. When bent, it will connect most of the ground points.

![Transponder build step 4](./images/TransponderBuild/Transponder_4.jpg)

Mount the output resistors **R2** and **R3** and the two capacitors **C5** and **C6**.
Leave unsoldered the pins that go to the antenna, solder and cut all the other.

![Transponder build step 5](./images/TransponderBuild/Transponder_5.jpg)

Connect the servo wire. Use a piece of shrink tube as an extra strain relief across the two enlarged holes. Bend and solder the wire, and connect all the ground points.

![Transponder build step 6](./images/TransponderBuild/Transponder_6.jpg)

Solder 4 small pieces of wire in the four corners. Wrap **19 turns of 0.125 mm diameter** enamel-insulated wire around the board. Clear the ends and solder to the output terminals of *C5* and *C6*. Bend the corners on the outside. Program the PIC with the firmware and push it into the socket

![Transponder build step 7](./images/TransponderBuild/Transponder_7.jpg)

You can wrap the transponder in rigid shrink plastic or in a small box. This is how it looks:

![Transponder build step 8](./images/TransponderBuild/Transponder_8.jpg)

# AndreasM TransponderV3 (SMD-kretskort)

Det här kapitlet är för det delade 4-lagerskortet **TransponderV3** på [OSH Park (AndreasM)](https://oshpark.com/profiles/AndreasM) och komponenterna i [BOM.md](../Schematic/Transponder/contrib/AndreasM/BOM.md).

Kretsen följer det officiella GitHub-schemat (samma referenser: **U1** = 5 V-LDO, **U2** = PIC, **C5** = antennavstämning). Det är **inte** perfboard-bygget ovan: inget MOSFET, ingen hålmonterad kristall, ingen lindad antenn. Slingan är koppar på undersidan.

![TransponderV3 ovansida och undersida](../Schematic/Transponder/contrib/AndreasM/TransponderV3.png)

## BOM: vilken variant den är för

[Schematic/Transponder/contrib/AndreasM/BOM.md](../Schematic/Transponder/contrib/AndreasM/BOM.md) är inköpslistan från TME (order **35407144**, tillräckligt för **4 kort**). Den gäller **endast AndreasM TransponderV3**.

| Kort / schema | Använd V3-BOM:en? |
| --- | --- |
| AndreasM **TransponderV3** (OSH Park) | **Ja.** Referenserna stämmer med silkscreen och GitHub-schemat. |
| AndreasM **TransponderV2** | **Nej.** Samma krets, men C1/C2/C4/C5/C6 byter namn. På V2 är avstämningen **C4**. |
| Officiellt perfboard (kapitlet ovan) | **Nej.** Där sitter LP2950, Q1 VP2106, DIP-sockel och lindad trådantenn. C1/C2 är polariserade. |
| WBorek (EasyEDA, contrib/WBorek) | **Nej.** 3,3 V-regulator, C5 **68 pF**, R1 **65 Ω**, extra knapp. |

OSH Park-texten på V3 säger fortfarande “play around with **C4**” — det är kvar från V2. På V3 stämmer du **C5** (schemat ~130 pF). TME-ordern har **150 pF** på C5 och **100 pF** som reserv.

## Vad du behöver

- PCB TransponderV3, 19,5 × 19,6 mm, 4 lager
- Komponenter enligt BOM: PIC **SOIC-8** (`PIC16F18313-I/SN`), inte DIP (`…/P`)
- SMD-lödning: 0805, 1206 LED, SOT-23, SOIC-8. Fluss och pincett
- Programmerare: decoderns PIC-prog (RCHourglass Manager) eller PICkit/ICSP på dynorna **VPP, CLK, DAT, +V, GND**
- Hex-fil i `Firmware/Transponder/bin/` — varje `RCHourglassT.X.<nummer>.hex` är ett unikt transpondernummer. Ett nummer per bil

## Orientering

**Ovansida:** **J1+** (matningsplus), **R1** **D1** **C5** längs kanten, **U1** (LDO), avkoppling **C1/C2**, kristalllast **C3/C4**, sänd **R2/R3 C6**, kristall **Y1**. PIC **U2** (SOIC-8) i mitten; **J2** är tvådynan intill.

**Undersida:** antennslinga i koppar plus programmeringsdynor **VPP CLK DAT +V GND**. Linda inte extra varv.

## Steg 1. Kontrollera kortet

Lägg ut alla delar på BOM:en och kryssa av referenserna mot silkscreen. Kontrollera särskilt:

- **U1** är MCP1702 **5,0 V** (`…-5002E/CB`), inte 3,3 V
- **Y1** är HC-49 **SMD**, inte hålmonterad HC-49S
- **C5** är 150 pF (eller 130 pF). Lägg 100 pF-reserven åt sidan
- Inget Q1, ingen sockel, ingen 68 pF som primär C5

Titta igenom slingan på undersidan: inga kopparrester mellan varven.

## Steg 2. 0805-passiva

Löd motstånd och små kondingar först, medan kortet är lätt att vända.

| Ref | Värde | Anmärkning |
| --- | --- | --- |
| R1 | 1,5 kΩ | LED-seriemotstånd |
| R2, R3 | 100 Ω | Push-pull till antennen |
| C3, C4 | 20 pF C0G | Kristallast |
| C5 | 150 pF C0G | Avstämning. Byt till 100 pF om räckvidden är dålig |
| C6 | 47 pF C0G | Serie mot slingan |
| C1, C2 | 10 µF X5R | Keramiska. **Ingen polaritet** (till skillnad från perfboard-elcyterna) |

## Steg 3. LED D1

1206 röd LED. Schemat: PIC **RA2** → D1-anod → katod → **R1** → jord. Katodstrecket på dioden mot **R1**.

## Steg 4. U1, 5 V-LDO

MCP1702 i SOT-23. Pin 1 VIN, pin 2 GND, pin 3 VOUT — matcha silkscreen. Det här kortet har ingen VP2106 före regulatorn.

## Steg 5. U2, PIC

`PIC16F18313-I/SN`, SOIC-8. Pin 1 (prick / fasning) är **VDD**. Felvänd PIC går sönder vid matning.

## Steg 6. Y1, 5,000 MHz

SMD HC-49, ingen polaritet. C3 och C4 ska redan sitta. Använd inte hålmonterad kristall i det här fotavtrycket.

## Steg 7. Matning

Löd plus till **J1+**. Jord till **GND** (undersidans programmeringsdyna duger). Typiskt 6–8,4 V från ESC/BEC eller 2S. MCP1702 tål max 13,2 V in. PIC:en ska se **5 V** på VDD, inte 3,3 V.

## Steg 8. Programmera

Dynor på undersidan, i ordning: **VPP, CLK, DAT, +V, GND**.

Med decoderns programmerare och RCHourglass Manager: **Detect** ska svara modell **3066** (PIC16F18313). **Program Pic**, välj hex, behåll originalnummer eller byt i tweak-dialogen.

En hex-fil per transponder. Samma nummer i två bilar ger krockar i tidtagningen.

## Steg 9. Test och C5

- Efter LDO: ca **5,0 V** mot jord
- Firmware togglar LED på RA2 — den ska blinka när kortet sänder
- Antennen är slingan. Tejpa inte metall över den
- Börja med **150 pF** på C5. Om dekodern tar svagt över loopen: byt till **100 pF** och jämför. OSH Park-blurbens “C4 ≈ 130 pF” avser V2-namnet; här är det **C5**

Kapsla in i krympslang eller liten ask. Donera €5 per byggd transponder till barnverksamhet (projektets licens).
