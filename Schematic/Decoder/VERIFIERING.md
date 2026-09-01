# Verifiering: decoder + loop amplifier

Använd detta vid bänken. Referensscheman i samma mapp:

- [LoopAmplifierRevB6.jpg](LoopAmplifierRevB6.jpg) — Cano loop amp Rev B
- [RCHourglass decoder schematic.png](RCHourglass%20decoder%20schematic.png) — Cano PDIA + PSoC (wiki-bygget)
- [Decoder Schematic.pdf](Decoder%20Schematic.pdf) — KiCad Rev 2 med testpunkter (LED/piezo/PIC valfritt)

PSoC-dotterkortet ska vara **urtaget** tills avsnitt 1–3 är klara.

---

## 1. Foton att ta (för visuell jämförelse)

Ta skarpa bilder, rakt ovanifrån, med komponentmärkningar läsbara.

Loop amplifier:

- [ ] Ovansida hela kortet
- [ ] Lödsida hela kortet
- [ ] Närbild Q1–Q6 (platt sida synlig)
- [ ] Närbild J1 (loop) och J2 (F-kontakt)
- [ ] Närbild jumpers J3/J4/J5 och ev. VR1

Decoder:

- [ ] Ovansida hela kortet
- [ ] Lödsida hela kortet
- [ ] Närbild F-kontakt + 75 Ω phantom
- [ ] Närbild analogsteget (Q1–Q5)
- [ ] Närbild 5 MHz-kristall + lastkondensatorer
- [ ] Närbild PSoC-stiftlistan (räkna stift från plasten, inte silkscreen)

Inkoppling:

- [ ] Coax mellan korten, skärm mot F-chassi

---

## 2. Visuell checklista — kända fel

### Loop amplifier (Cano Rev B)

| Kontroll | Rätt | Vanligt fel |
|---|---|---|
| Q1, Q2, Q5, Q6 | 2N3904 NPN | PNP i NPN-plats |
| Q3, Q4 | 2N3906 PNP | NPN i PNP-plats |
| TO-92 2Nxxxx | Platt sida mot dig: **E B C** | Spegelvänd |
| BC547 / BC307 | Fotavtryck är **spegelvänt** mot 2N-serien | Wiki-foton visar BC-par; 2N ska inte kopieras rakt av |
| R4 och R5 | 2k00 i återkopplingen till Q1/Q2-bas | R5 lätt att jorda fel (röd rättning i wikin) |
| C5-nätet | C5 hänger ihop med jumper J3 och övriga trimkondingar | Öppen förbindelse C5→övriga |
| J4, C6, R12 | Får saknas | Wiki: “have not been used” |
| J2 F-kontakt | Centerpin = signal + phantom. Skärm = GND | Rev B rättade pinout. Fel ger 0 V eller kort |
| Jord | Stjärnjord till en punkt | Lång jordslinga runt kortet |
| VR1 (valfri) | Sätter 2,15–2,25 V på Q6-bas | Inte obligatorisk |

Jumpers efter loopstorlek (Cano):

| Loop | Jumper |
|---|---|
| ca 9×1 till 12×1 fot | ingen |
| ca 6×1 till 8×1 fot | **J3** (C5 22 pF) |
| mellanstorlek | **J4** (C6 + R12 4k87) |
| ca 3×1 till 4×1 fot | **J5** (C7 82 pF + R13 2k) |

Cykelmållinje är oftast större än RC-bana: börja **utan jumper** eller med **J3**, inte J5.

### Decoder (PDIA + PSoC)

| Kontroll | Rätt | Vanligt fel |
|---|---|---|
| Q1, Q2, Q5 | 2N3906 PNP | NPN här |
| Q3, Q4 | 2N3904 NPN | PNP här |
| F-chassi | Jordad till kretsjord (wiki: vit tråd till R8) | Flytande skärm |
| Phantom 5 V | **75 Ω från +5 V till F-centerpin** | 75 Ω till jord kortar matningen till loop amp |
| Analogutgång | Till **P12_2** | En pinne fel p.g.a. offset silkscreen |
| Hysteres | **P12_3 → R11 4k87 → P12_2** | R11 till fel pinne |
| Kristall | **5 MHz** på **P15_0 / P15_1**, 22 pF till jord | 8 MHz, eller fel PSoC-hörn |
| PSoC-matning | +5 V till **VDDIO**, GND till nedre PSoC-GND | Bara USB, analogdelen strömlös |
| PSoC-list | Räkna stift på kortet | Silkscreen är förskjuten |
| Listavstånd | Matchar CY8CKIT-059 | En rad fel, kort när kortet trycks i |

---

## 3. Mätningar utan spänning

Multimeter i resistansläge. PSoC **urkopplad**.

| Mätning | Förväntat | Ditt värde | OK? |
|---|---|---|---|
| Decoder: blivande PSoC Vcc ↔ GND | ca **4 kΩ** | | |
| Decoder: F-center ↔ skärm | **inte kort** (∞ eller hög) | | |
| Decoder: F-center ↔ +5 V-buss | ca **75 Ω** (phantom-R) | | |
| Loop amp: J2-center ↔ skärm | **inte kort** | | |
| Loop amp: J2-center → intern 3,7 V-nod | ca **75 Ω** (R11) | | |

Stoppa om Vcc–GND är nära 0 Ω (kort) eller om F-center sitter i jord.

---

## 4. DC-test — loop amplifier

Mata **5 V via 75 Ω** in i J2 (samma som decodern gör). Mät mot GND. Loop **ifrån**.

| Punkt | Schema | Ditt värde | OK? (±0,3 V) |
|---|---|---|---|
| J2 centerpin | **4,18 V** | | |
| Intern matning efter R11 | **3,70 V** | | |
| Q3/Q4-emitter (R2/R3) | **3,20 V** | | |
| Q1/Q2-bas | **1,20 V** | | |
| Q1/Q2-emitter (R1-svans) | **0,50 V** | | |
| Q5-biasnod | **1,25 V** | | |
| Q6-bas | **2,2 V** (trim 2,15–2,25 om VR1 sitter) | | |
| DC mellan loop-ingångarna | **≈ 0 V** (trimma VR1) | | |

Flera punkter fel samtidigt: kolla NPN/PNP och R5 först.

När decodern matar via coax ska **samma** tal synas — då är phantom-matningen rätt.

---

## 5. DC-test — decoder (KiCad-testpunkter, PSoC ur)

Mata +5 V på analogkortets +5 V/GND. Loop amp kan sitta på coaxen.

| Punkt (KiCad Rev 2) | Schema | Ditt värde | OK? |
|---|---|---|---|
| TP1 / TP2 (Q5) | ~3,7 V | | |
| TP6 Q1-bas | ~3,71 V | | |
| TP5 Q2-bas | ~3,73 V | | |
| TP7 efter C1 | ~3,96 V | | |
| TP9 | ~1,05 V | | |
| TP10 / TP11 | ~0,39 V | | |
| TP8 analogutgång (utan PSoC-hysteres) | ~1,87 V | | |
| TP3 nära matning | ~4,76 V | | |

TP8 ändras när PSoC sitter i och R11 får hysteres från P12_3.

---

## 6. Funktionstest (först när DC stämmer)

1. Programmera PSoC från KitProg-USB (den stora USB-A-fliken, ingen kabel behövs) med PSoC Programmer.
2. Hex: [Firmware/Decoder/Version010_beta.hex](../../Firmware/Decoder/Version010_beta.hex)
3. Sätt i PSoC på analogkortet. Mini-USB till PC. Installera Cypress USB-UART-drivrutin.
4. Terminal mot COM-porten: **115200 8N1**.
5. Kommandon (ingen echo): `VERSION` och `LICENSE` ska ge svar.
6. Oscilloskop (valfritt): transponder över loopen → signal på noden mot **P12_2**.
7. Stäng inte loop amp-lådan förrän passager syns i timingprogrammet.

---

## Fotojämförelse 2026-08-29 (`images/build imgs`)

### Loop amplifier (`amplifier front/rear`)

- Två 5×7 cm-hålkort hopsatta. 500 kΩ-trimmer **67W P500K** = VR1, rätt.
- Skruvplintar istället för F/banan — OK om loop och utgång sitter rätt.
- Matning via jack (röd/grå) — avvikelse från Cano phantom via coax. Använd **antingen** jack **eller** decoder-5 V, inte båda.
- Cirka **5** TO-92 synliga. Schemat kräver **6** (Q1–Q6). Räkna fysiskt.
- Ingen tydlig **10 µF ellyt (C4)**. Film-rutor (troligen 100 nF) syns.
- Inga synliga jumperstift J3/J4/J5 — kan vara hårdlödda.
- Undersida: avsiktliga lödbryggor i skarven + risk för lödviskar. PSoC-4 kΩ-testet gäller inte här.

### Decoder (`Decoder front/rear`)

- CY8CKIT-059 rätt typ. KitProg sitter kvar (bra för flash).
- Analogdel ovanför PSoC: **5** TO-92 = rätt antal för PDIA (Q1–Q5).
- RF-kontakt finns. Piezo + LED under PSoC är valfria extras, OK.
- PSoC redan ilödd — wiki-testet “4 kΩ Vcc–GND med PSoC ur” går **inte** att använda.
- **5 MHz-kristall** inte identifierad på bilderna. Måste sitta på **P15.0 och P15.1** (nedre listen), inte P15.2/P15.3 (kitets XTAL-silk).
- Stor grön resistor märkt **R2**: avläs värde. PDIA-R2 = 100 Ω; phantom-R1 = 75 Ω. Inte 22 Ω.
- Analogutgång ska till **P12.2**, hysteres **P12.3** via 4k87. F-chassi ska vara jordat.

### Inte gjort än

- DC-mätning (väntar på stegvis kontroll)
- Flash / VERSION / LICENSE
