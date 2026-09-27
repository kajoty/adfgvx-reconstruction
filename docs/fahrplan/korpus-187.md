# Korpus Seite 187

*A. Geloeste Korpus-Seiten — Kryptogramm 11 von 28*

[← vorherige](korpus-176a.md) | [Index](README.md) | [naechste →](korpus-73.md)

---

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

214 Zeichen = 107 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AXFFD FADFG DAXDF FAVDD XGAAG DVXVG GDVVD FAGFF GGFVF FGDDG GVVVD DGVGG GADVV AFDDF AVGGF XFGVV ADDGV AXDAD VGFFV DFVDV VGDVG GAFGG AGGFA GDAVD VFFDD DAGAF DFADF AGAAD DXVGX GGDFA ADVVF GDGFF DFXDX AVFDG FGADD FFGDX AAGFD DADVF DFFDA DFGAF VFFDD VVVVV GVAF
```

### 2. Der Schluessel

**`Nov13-15b`** — n = 16 Spalten, laut Lasry-Liste 52× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
4-11-5-14-9-7-16-1-12-15-6-10-3-13-8-2
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
7, 15, 12, 0, 2, 10, 5, 14, 4, 11, 1, 8, 13, 3, 9, 6
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
H--BMUF15PX0DJLR---S6VONKZ-AWITEGC-
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
H . . B M U
F 1 5 P X 0
D J L R . .
. S 6 V O N
K Z . A W I
T E G C . .
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 214 Zeichen. Bei n = 16 Spalten ergibt das 13 volle Zeilen; die Spaltenlaengen sind `14`×6 und `13`×10.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 7, 15, 12, 0, 2, 10, 5, 14, 4, 11, 1, 8, 13, 3, 9, 6
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
FFVDFAFAFVDFVFVDGADFGDFXAFDFXXDFGGDFGDDFADFDVDFFFAGGAGDFDFAD
GXVAVAVDGVVDVFVDGADVFDGXGAVFVDGADVVDFDGAFXVAFAGGVFVDGXGAADVD
GDFAVDGXDVAGGAVFDFXFDGDGDGDFDDGGGGFDFFVAGXVDAVVDFAGFAGGAGGVD
VGAAFFVAGAGGVGAADFFXDVVDFDADVDFDVF
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
SELLVXGENXKOMX9XAXKXBRESLAUXXBITTEWEGENDRINGENDERNOTLAGEINBE
KLEIDUNGX4000XPAARSTIEFELZUNAECHSTNACHXODERBERG
```

### 6. Die entschluesselte Nachricht

**Klartext** (107 Zeichen, `X` = Worttrenner):

```
SELLVXGENXKOMX9XAXKXBRESLAUXXBITTEWEGENDRINGENDERNOTLAGEINBE
KLEIDUNGX4000XPAARSTIEFELZUNAECHSTNACHXODERBERG
```

*Quelle des Klartexts: Norbert #24 / Max Baertl #39.*


---

[← vorherige](korpus-176a.md) | [Index](README.md) | [naechste →](korpus-73.md)
