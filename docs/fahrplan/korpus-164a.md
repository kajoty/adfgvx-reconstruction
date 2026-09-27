# Korpus Seite 164a

*A. Geloeste Korpus-Seiten — Kryptogramm 7 von 28*

[← vorherige](korpus-153a.md) | [Index](README.md) | [naechste →](korpus-164b.md)

---

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

126 Zeichen = 63 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
VFVDG GVFFF XDGDV ADGDV VXVAD FDFVG VDDDF AFDDV DXDXV GFGVX XVVVG DAVVG VVVGA GXGXG VVVXD XGVVG GXVGA GFDFD GDDVD GXGGG DDXXX DXVVG DVGVV VDDGX DDVDD A
```

### 2. Der Schluessel

**`Nov7-9`** — n = 20 Spalten, laut Lasry-Liste 93× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
6-12-7-15-1-11-16-5-8-14-3-18-9-13-2-17-20-10-19-4
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
4, 14, 10, 19, 7, 0, 2, 8, 12, 17, 5, 1, 13, 9, 3, 6, 15, 11, 18, 16
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
PRMYUW3LZGES8C71QOV29ITB40-KXH-AJNDF
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
P R M Y U W
3 L Z G E S
8 C 7 1 Q O
V 2 9 I T B
4 0 . K X H
. A J N D F
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 126 Zeichen. Bei n = 20 Spalten ergibt das 6 volle Zeilen; die Spaltenlaengen sind `7`×6 und `6`×14.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 4, 14, 10, 19, 7, 0, 2, 8, 12, 17, 5, 1, 13, 9, 3, 6, 15, 11, 18, 16
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
DVDDVGXFGGDVVVFXDVVVDVVGFAGDFAVGVVFXDVVVDVDDVGGFGGADVGFXVGDX
FXXDDXGVVFDVGGXDDVDVADDVGGDGXDGGDXDXDVGAFXXDGXDVXFDVAVGVAVXD
DGVGVG
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
ELXDIEHOEHEX828XHOEHELX9IRXOXSONSTKEINEEREIGNISSEVONBEDEUTUN
GXX
```

### 6. Die entschluesselte Nachricht

**Klartext** (63 Zeichen, `X` = Worttrenner):

```
ELXDIEHOEHEX828XHOEHELX9IRXOXSONSTKEINEEREIGNISSEVONBEDEUTUN
GXX
```

*Quelle des Klartexts: Norbert #41 / #44.*


---

[← vorherige](korpus-153a.md) | [Index](README.md) | [naechste →](korpus-164b.md)
