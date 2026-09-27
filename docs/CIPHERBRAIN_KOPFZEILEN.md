# Die Kopfzeilen der Cipherbrain-Bilder

**Stand: 2026-09-27**

## Befund

Die 19 PNG-Bilder in `docs/cipherbrain_pages/` sind **nicht zweispaltig**.
Es handelt sich um ein **Funkspruch-Formular**:

| Bereich | y-Bereich | Inhalt |
|---|---|---|
| Oben | ca. 2–47 | der **Funkmeldungs-Kopf** (Datum, Rufzeichen, Adressat, Nummer) |
| Unten | ca. 50–155 | das **ADFGVX-Kryptogramm** in 5er-Gruppen |

Eine frühere Annahme („links Kryptogramm, rechts Kopf“) war **falsch**: Die
Zeilen sind lediglich unterschiedlich eingerückt (Kopfzeilen kurz, Krypto-Zeilen
breit). Die Krypto-Zeilen bestehen aus Wörtern mit **gleichmäßiger Breite**
(ca. 37 px pro 5er-Gruppe), die Kopfzeilen aus Fließtext mit unregelmäßigen
Wortbreiten. Das ist das sichere Unterscheidungsmerkmal.

## Struktur (Beispiel Seite 73, `cryptogram-01.png`, 614×180 px)

| Zeile | y-Bereich | Inhalt |
|---|---|---|
| 1 | 15–27 | `26th OCTOBER, 1918` (Datum, fett) |
| 2 | 52–64 | `PQT v NKJ (2.33 a.am. , November 8th)` (Rufzeichen + Uhrzeit) |
| 3 | 66–75 | `FÜR COS GENERAL VON KRESS 0911 (26)` (Adressat + Nummer) |
| 4 | 92–102 | Krypto Z1: `D--FX GDVDX DGGAA AGFFD DVDXF XFGGD DAVGD DDADG` |
| 5 | 105–115 | Krypto Z2 |
| 6 | 119–128 | Krypto Z3 |
| 7 | 132–141 | Krypto Z4 |
| 8 | 144–154 | Krypto Z5 (letzte, kurz) |

Die Meldungsnummer `RICHI-178` steht rechts in der Kopfzeile (nicht als eigene
Textzeile).

## Validierung: Seite 100 (`cryptogram-02.png`, 614×170 px)

Seite 100 ist **gelöst** (Key `Nov1-3`). Die Kopfzeile muss also ein Datum
zwischen dem 1. und 3. November 1918 zeigen — und tut es:

| Band | y-Bereich | Inhalt |
|---|---|---|
| 1 | 2–20 | `UKS v ZÖN (1.44 a.m., November 2nd)` |
| 2 | 35–47 | `2016 (1) 2 TLE` |
| 3 | 60–73 | Krypto Z1: `VDDDAD AADFG VVVAV GDAFV VAFGV DDVXF DFGGA AGXAA` |
| 4 | 87–99 | Krypto Z2 |
| 5 | 114–126 | Krypto Z3 |
| 6 | 145–153 | Krypto Z4 (letzte, kurz) |

**Datum 2. November 1918 → Key `Nov1-3` (1.–3. November). Passt.**
Damit ist die Methode „Kopfzeilen-Datum bestimmt den Schlüssel-Zeitraum“
validiert.

Die Segmentierung von Band 3 ergibt 9 Wortgruppen (erste verschmolzen:
`VDDDAD AADFG`), danach 8 × 5er-Gruppen — exakt die Transkriptionszeile 1.

## Format-Vergleich mit dem Childs-Buch

Das Format ist **identisch** mit den im Childs-Buch abgedruckten
Meldungsköpfen, z. B. (Childs, um Zeile 5262):

```
NKJ v LP
FUER COS

ALACHI-266
```

Die Cipherbrain-Kopfzeile folgt demselben Schema:

```
PQT v NKJ
FÜR COS GENERAL VON KRESS
0911 (26)
RICHI-178
```

## Bedeutung der Kürzel

| Kürzel | Bedeutung | Quelle |
|---|---|---|
| `RICHI` | Präfix der **östlichen** ADFGVX-Meldungen (Berlin ↔ Tiflis) | Childs S. 7580 ff. |
| `COS` | Kaukasus-Delegation (Tiflis) | Childs S. 10488, 17704 |
| `NKJ` | Nicolaiev (Relaisstation) | Childs S. 5262 |
| `LP` | Berlin | Childs S. 5262 |
| `OSM` | Constantinople | Childs S. 5262 |
| `PQT` | Rufzeichen (Sender) — im Childs-Buch nicht belegt | — |

## Konsequenz für die Kryptanalyse

1. **Die Bilder liefern keinen Klartext.** Der Kopf ist Metadaten.
2. **Aber sie liefern die Meldungsidentität**: Datum, Rufzeichen, RICHI-Nummer.
3. **Damit ist eine Schlüsselzuordnung möglich** — sofern der Key für das
   jeweilige Datum in der Lasry-Liste vorhanden ist.
4. **Für ungelöste Seiten ist das Datum der entscheidende neue Fakt**: Es sagt,
   welcher Key überhaupt in Frage kommt — und ob er in der Liste fehlt.

### Seite 73 = RICHI-178

- Datum: **26. Oktober 1918** (Kopfzeile) bzw. **8. November 1918** (Uhrzeit-Zeile)
- Rufzeichen: `PQT` → `NKJ`
- Adressat: `COS General von Kress`
- Meldungsnummer: `RICHI-178`

**RICHI-178 ist im Childs-Buch nicht dokumentiert.** Die dort behandelten
RICHI-Nummern sind: 152, 168, 222, 264, 266, 274, 338.

**Kein Key der Liste entschlüsselt Seite 73** — auch nicht mit doppelter
Transposition. Die Key-Liste hat eine Lücke zwischen `Oct4-6` und `Oct28-31`;
für den 26. Oktober fehlt der Schlüssel.

### Seite 152 = `cryptogram-07.png` (ungelöst)

Kopfzeile (manuell gelesen):

```
E) NKJ v LP (9.10 p.m., November 7th)
```

| Band | y-Bereich | Inhalt |
|---|---|---|
| 1 | 11–24 | `E) NKJ v LP (9.10 p.m., November 7th)` |
| 2 | 39–49 | Krypto Z1 |
| 3 | 52–62 | Krypto Z2 |
| 4 | 66–74 | Krypto Z3 (letzte, kurz) |

**Datum 7. November 1918 → Key `Nov7-9` (7.–9. November, 20 Spalten, n=93).**

Die Segmentierung der Kopfzeile ergibt 8 Wörter mit 2/3/1/2/5/5/9/4 Zeichen —
exakt `E)` `NKJ` `v` `LP` `(9.10` `p.m.,` `November` `7th)`. Die Glyphen wurden
zusätzlich einzeln als Pixelmatrix verifiziert (`E`, `)`, `N`, `K`, `J`, `v`,
`L`, `P`).

**Bedeutung**: `NKJ` = Nicolaiev (Relaisstation), `LP` = Berlin. Der Kopf
entspricht dem Childs-Schema `NKJ v LP` (Childs, um Zeile 5262).

**Krypto-Struktur** (Pixelprofil, y-Bereiche wie oben):

| Zeile | Wortgruppen (Zeichen) |
|---|---|
| Z1 | 1, 2, 5, 4, 5, 5, 5, 5, 4, 6 |
| Z2 | 12, 5, 5, 5, 5, 4, 5, 5, 4 |
| Z3 | 4, 4, 5, 5, 4 |

Die Transkription in `article_body.txt` lautet:

```
FXVAD FDXAA XXFAG VFVDX AAGFD DFDVv VAAVA AXVGX
GDAXA AGVAV ADAFD DGVDD FVAVX FVXXv FXXXG FGXGF
AFXXG XGFAA AVFFX XFDFV VVAX
```

**Befund**: Die Transkription enthält **OCR-Fehler in Kleinbuchstaben** —
`DFDVv` und `FVXXv` (Zeile 1 bzw. 2). Das `v` ist jeweils das letzte Zeichen
einer 5er-Gruppe und muss `V` sein. Die Pixelbreiten bestätigen das: die
betreffenden Gruppen sind 4–6 px breiter als eine reine 5er-Gruppe, weil das
`v`-Glyph schmaler ist als `V` und die Segmentierung dadurch verschoben wird.
Damit ist die Transkription von Seite 152 **nicht zeichengenau** — ein
zusätzlicher Beleg für den Datenengpass.

**Entschlüsselungsversuch**: Die bereinigte CT-Länge ist **104 Zeichen**.
104 ist **nicht durch 20 teilbar** (Rest 4) — die Transposition geht also
nicht sauber auf. Kein Key der Liste liefert Klartext; die Fitness-Werte
liegen alle zwischen −14,9 und −19,9 (Rauschen). Der scheinbar beste Wert
(`Nov4-6`, −14,90) ist nur minimal besser als Zufall und gehört zu einem
Datumsbereich, der nicht zum Kopf passt.

**Konsequenz**: Selbst mit dem durch das Datum belegten Key `Nov7-9` ist
Seite 152 nicht entschlüsselbar. Der Grund ist die **fehlerhafte
Transkription**, nicht der Algorithmus. Seite 152 ist damit ein weiteres
Beispiel für den Datenengpass — und **kein** geeigneter Kandidat für den
`conflict_solver`, solange die Transkription nicht unabhängig verifiziert ist.

## Methodik

- Zeilen-/Spaltentrennung: Pixelprofil (dunkle Pixel < Schwellwert 150).
- **Automatisches OCR ist gescheitert**: Template-Matching (Liberation Serif
  Italic, 6×9/12×16 normalisiert, Hamming-Distanz) liefert Unsinn
  (Distanzen 40–80 von 192 Pixeln). Die Bildglyphen sind nur ~6×10 px groß.
- **Die Kopfzeilen wurden manuell gelesen** (mit Unterstützung durch den Nutzer).

## Skripte

- `/tmp/scan_headers.py` — listet die Zeilenstruktur der rechten Spalte für
  alle 19 Bilder.
- `/tmp/ocr_match.py` — Template-Matching-OCR (gescheitert, nur als
  Negativbeleg aufbewahrt).
- `/tmp/glyph152.py`, `/tmp/chars152.py` — isolieren Wörter bzw. Einzelzeichen
  der Kopfzeile von Seite 152 als Pixelmatrix (ASCII-Art in Datei schreiben,
  dann mit dem Editor lesen — **nicht** mit `cat`, das Terminal bricht breite
  Zeilen um und verstümmelt die Ausgabe).
