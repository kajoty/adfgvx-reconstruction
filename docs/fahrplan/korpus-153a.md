# Korpus Seite 153a

*A. Geloeste Korpus-Seiten — Kryptogramm 6 von 28*

[← vorherige](korpus-146.md) | [Index](README.md) | [naechste →](korpus-164a.md)

---

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

352 Zeichen = 176 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AFGGG AAAAA DFFGG AGGGG XVAGF XAGFV AAVGG AGAAG GGFGG AAGFG DGDAF GGGGA GDDAF FDGGG GAAGA FGFAF GAAAA ADDAA GFFDA GDGGG GAAGA FFADG DGAAG DGGGG GVVVX XVXXV XAGXV GXXGG GAAAG FFADG GGGGD AFVAG DFAGF DFFGA AAGGG VGXGX DXVDD XXXXV XAGXV AXXXX VVAVG DDADX AGGFG AAAFF FGADG AGFXX XXDXX GXDFG DDXGV FXVFG GVXXV GVVVG FDGGX GXFFD VFGXX DXADX GFGAG FDDAG DFGGF DAFAX FAFVX XXFVV ADVGG FFXXV XAVAX XVXGV VXFGD FVVGX FVADX XXGAV VF
```

### 2. Der Schluessel

**`Nov13-15a`** — n = 20 Spalten, laut Lasry-Liste 13× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
13-8-6-16-7-18-1-14-9-20-10-15-17-2-3-11-5-19-4-12
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
6, 13, 14, 18, 16, 2, 4, 1, 8, 10, 15, 19, 0, 7, 11, 3, 12, 5, 17, 9
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
JZLH-R--S-T-MKDWU-V-B-P--FAO-GIX-CNE
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
J Z L H . R
. . S . T .
M K D W U .
V . B . P .
. F A O . G
I X . C N E
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 352 Zeichen. Bei n = 20 Spalten ergibt das 17 volle Zeilen; die Spaltenlaengen sind `18`×12 und `17`×8.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 6, 13, 14, 18, 16, 2, 4, 1, 8, 10, 15, 19, 0, 7, 11, 3, 12, 5, 17, 9
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
AVDXAXAXGDAXGGAGGXDXGVDGFFFXAFGVAGGXGXAVGXAXFAGXAVDFGXAGAVFA
FXAFAFGXAVFGFVAXAXGXGVGFDVGDGGAGDAGDGAGXAXFDGXAXFXGVDGGXAVGX
AXFVDXAXFFFXAFGVFAGXAVDFGXAGAVDXGXFDGXAVFXAGAFAXDAFVDAGDFXGV
FAGXAVADGDFGFGGXAVDAFGDXGVDFGXGVGFAXFXDVGXGDDAFGGXAVGVAXGGAG
AVGXGDFDGXAVFAGXAVFDDGGAGVGDGGAGDAFVAVFDGXGDGGGXDAGFAVGXAXDA
AXAXGGAGAVGDFGDAAFGDGGAGGFGVFVGGAGGGAGGXFGGFVFGFVFVG
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
RUSSISCHEUNDPOLNHEERESVERKEHRVOLLERFASSENXWICHTIGESBESONDERE
SAUSPOLNVERKEHRUEBEROHLSTATIONVERZIFFERTFUNKENXSOWEITFERNSCH
REIBERVERBDGNICHTARBEICETXRESTSSCHRIFTLICHXNACHCHEFX0X01
```

### 6. Die entschluesselte Nachricht

**Klartext** (176 Zeichen, `X` = Worttrenner):

```
RUSSISCHEUNDPOLNHEERESVERKEHRVOLLERFASSENXWICHTIGESBESONDERE
SAUSPOLNVERKEHRUEBEROHLSTATIONVERZIFFERTFUNKENXSOWEITFERNSCH
REIBERVERBDGNICHTARBEICETXRESTSSCHRIFTLICHXNACHCHEFX0X01
```

*Quelle des Klartexts: George Lasry #50 / Norbert #53.*


---

[← vorherige](korpus-146.md) | [Index](README.md) | [naechste →](korpus-164a.md)
