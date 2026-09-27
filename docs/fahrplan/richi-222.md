# RICHI-222

*D. Nachrichten aus dem Childs-Buch — Kryptogramm 25 von 28*

[← vorherige](richi-264.md) | [Index](README.md) | [naechste →](richi-274.md)

---

**Status:** Struktur **bewiesen**, Lueckenfuellung Kandidat

### 1. Die verschluesselte Nachricht

144 Zeichen = 72 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
FVDFG GGAVG DADXF DXDVD VGVGG AVGVD GAVDD VFGAA AADVA GFFXG DAGGX AAVGV GDADD DVFFG DAVGX GGDFA FAGXG GGDVG ADGVD DFXGG GGGGD VVGDA GVGFX GDDXV VXVDD VDXFX XGXXF FFADD AVDX
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

Der Geheimtext hat 144 Zeichen. Bei n = 19 Spalten ergibt das 7 volle Zeilen; die Spaltenlaengen sind `8`×11 und `7`×8.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 14, 0, 2, 18, 7, 4, 9, 17, 13, 16, 5, 12, 15, 3, 1, 8, 6, 10
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
FGVDGGFGVGFFAFAXGDGDFGVFXXAXXAVDGVGGAAXXGVFGXAVADDGDGGDDVDGA
GXGGADADFVADGFDDVDVDGGXADVAGDVAGADDDDGADDXDVGVGDGDGFVVVXVGAV
FVDVDGFXXGAFFGVDVGGFAXGX
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
7MN7EGL9887H69YMBNU6B7YJC8NCMD5NIIQIWCMMNYSOSOICVIXSB88WKPEF
QSVTAL7MEW95
```

### 6. Die entschluesselte Nachricht

**Klartext** (114 Zeichen, `X` = Worttrenner):

```
TECHENDERXGESARMEEDENMERSCHDURMEINGARNAUFESERSCHLESIENANZITU
NTENSEINDERSTENNDWISSERDETERESEXKTERRMTLTAA1GRISISCASS
```

Von 114 Bigrammen sind nur 37 vollstaendig; 70 haben genau eine Luecke, 7 fehlen ganz. Der gezeigte Klartext ist der beste Beam-Search-Kandidat, **nicht** bewiesen.


---

[← vorherige](richi-264.md) | [Index](README.md) | [naechste →](richi-274.md)
