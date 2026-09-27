# Korpus Seite 109

*A. Geloeste Korpus-Seiten — Kryptogramm 3 von 28*

[← vorherige](korpus-105.md) | [Index](README.md) | [naechste →](korpus-132.md)

---

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

250 Zeichen = 125 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
XAAVF XAXGD VGGGG GXGFD AFGAD VAGDA VGFDV GDGVF DAXFD GVGXA AGDFG XDXVD ADXXV VXXAD FGFGV VVVAG VDDGF AGXAG GADDG XADDV VVXXA VGDAF GAGDA DGDXG GDFGG ADFDG AXVFV FVGGV DDGVG VVGGX VAAAD GVXXA VGVFA GAGVG DVFVD VVXDF FDDVX VDXGA GGDVG GXGGV FGDXD FGVVG XVFDF AXADG VFDDD GXDDG VDAAD DXDAA FAXGD VGVFA
```

### 2. Der Schluessel

**`Nov1-3`** — n = 19 Spalten, laut Lasry-Liste 100× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
3-16-4-15-7-12-18-6-17-8-19-1-13-10-2-14-11-9-5
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
11, 14, 0, 2, 18, 7, 4, 9, 17, 13, 16, 5, 12, 15, 3, 1, 8, 6, 10
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
UILOF9RCZVSX02G7QTD8WNB5JMHEKPY41A36
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
U I L O F 9
R C Z V S X
0 2 G 7 Q T
D 8 W N B 5
J M H E K P
Y 4 1 A 3 6
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 250 Zeichen. Bei n = 19 Spalten ergibt das 13 volle Zeilen; die Spaltenlaengen sind `14`×3 und `13`×16.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 14, 0, 2, 18, 7, 4, 9, 17, 13, 16, 5, 12, 15, 3, 1, 8, 6, 10
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
AGDXVVDXVDDXXGGVVGGGGAVDVGAFGAAAGGFFDXDVXDDGXDDXAAVDGVVADAFF
XGGDFFAFVGFXDFFXVGDGFXDGADAFVGGVVGVGDGAAVGFXDXXFGFVGADFXVGGA
VGAVGAAADXGGADDGGXADVDVDXGDADVDDVFXDAAAVGVVGAFFFDAXGGAVGDAVV
XGDGDGFDDXDVAGGGDVFXVVVGADGGVGVGGAVDADAFGGADDVDVVGDXDXXGDVAG
DXVVGXXFXF
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
OXKXMXABENDMELDUNGXS4V4XUMBJRGA8GLETZTEVTVILEBEEVUETX1WEITED
EFDUXNIV5IMMARSCH4UFBELGRADERKAVV2XSONSTKEINEEDMILNISSEXXASO
XK511
```

### 6. Die entschluesselte Nachricht

**Klartext** (125 Zeichen, `X` = Worttrenner):

```
OXKXMXABENDMELDUNGXS4V4XUMBJRGA8GLETZTEVTVILEBEEVUETX1WEITED
EFDUXNIV5IMMARSCH4UFBELGRADERKAVV2XSONSTKEINEEDMILNISSEXXASO
XK511
```

*Quelle des Klartexts: Norbert #18 / Max Baertl #39.*


---

[← vorherige](korpus-105.md) | [Index](README.md) | [naechste →](korpus-132.md)
