# Korpus Seite 132

*A. Geloeste Korpus-Seiten — Kryptogramm 4 von 28*

[← vorherige](korpus-109.md) | [Index](README.md) | [naechste →](korpus-146.md)

---

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

154 Zeichen = 77 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AAXFA FAXXF AAGVV FAFFA GVVAA AXVXX GVXVA FXDAX XADDG FFFDF AFGXA AVXVA FAVGD GAAFX XGDXF AGAXA VDVXA FXVAV AAFAV ADVXF FFFXF VVFFA VAFAV AGXVF GVAGX FDAAX ADXFA FVDAA XFXAV GFAFA DVFG
```

### 2. Der Schluessel

**`Nov4-6`** — n = 17 Spalten, laut Lasry-Liste 106× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
7-10-8-14-3-11-16-1-6-13-4-9-15-5-12-17-2
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
7, 16, 4, 10, 13, 8, 0, 2, 11, 1, 5, 14, 9, 3, 12, 6, 15
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
17WHFLJ5D2UPEXKVZ9O0Q3Y6R8ABGITCMS4N
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
1 7 W H F L
J 5 D 2 U P
E X K V Z 9
O 0 Q 3 Y 6
R 8 A B G I
T C M S 4 N
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 154 Zeichen. Bei n = 17 Spalten ergibt das 9 volle Zeilen; die Spaltenlaengen sind `10`×1 und `9`×16.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 7, 16, 4, 10, 13, 8, 0, 2, 11, 1, 5, 14, 9, 3, 12, 6, 15
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
AVDVFAVAFAVXAXFGFAXGFAFDAFVXFADFFAVAAGGAAXFAXAXAFAAXFAVVVAFD
FGGAXXFGVXFAVAXAFAVADXFAVAVXGADFFAVXXXAVDVFAXXAVXAFAVAFDVVFA
VGFAXAXGGAVADFFAVADDXFVXXXFDFGFGFG
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
FUEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUENFTERXGE
BETSORDER5MINXVVV
```

### 6. Die entschluesselte Nachricht

**Klartext** (77 Zeichen, `X` = Worttrenner):

```
FUEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUENFTERXGE
BETSORDER5MINXVVV
```

*Quelle des Klartexts: Norbert #37 / Max Baertl #39.*


---

[← vorherige](korpus-109.md) | [Index](README.md) | [naechste →](korpus-146.md)
