# Fahrplan: Jedes Kryptogramm einzeln entschluesselt

Fuer jede Nachricht: (1) der Geheimtext, (2) der Schluessel, (3) die Permutation, (4) das Quadrat, (5) der Entschluesselungsweg Schritt fuer Schritt, (6) der Klartext.

**Verfahren (ADFGVX, 1918):** Zuerst wird der Klartext ueber ein 6×6-Quadrat in ADFGVX-Bigramme substituiert, dann werden die Bigramm-Zeichen per Spaltentransposition umsortiert. Entschluesselt wird in umgekehrter Reihenfolge: erst Transposition rueckgaengig, dann Substitution.

# A. Geloeste Korpus-Seiten

## Korpus Seite 100

**Status:** geloest, **bewiesen** — Geheimtext aus unabhaengiger Transkription, Roundtrip exakt

### 1. Die verschluesselte Nachricht

124 Zeichen = 62 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
VDDAD AADFG VVVAV GDAFV AAFGV DDVXF DFGGA AGXAA GGVAD XGAXV XAXGA XAGAX DDGDG VFFAX GDFGF DVGFA ADVVG VXGDV GGDDA DAVAG FXDFV ADVDG DGFGD DFGDA VGAA
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

Der Geheimtext hat 124 Zeichen. Bei n = 19 Spalten ergibt das 6 volle Zeilen; die Spaltenlaengen sind `7`×10 und `6`×9.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 14, 0, 2, 18, 7, 4, 9, 17, 13, 16, 5, 12, 15, 3, 1, 8, 6, 10
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
VVVGADGGVGDVFXAGVGDAAAGGFFGAAADADDVFAVVGADGGGADXVDADFXFXXGFF
DVFDAVVGADGGGAAFDXGAADDGDXADVDVDXGDADVDDVFXGAAAVGVVGAFFFDAXG
GADX
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRA
DX
```

### 6. Die entschluesselte Nachricht

**Klartext** (62 Zeichen, `X` = Worttrenner):

```
KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRA
DX
```

*Quelle des Klartexts: Armin #13 / Norbert #40.*

## Korpus Seite 105

**Status:** geloest, **bewiesen** — Geheimtext aus unabhaengiger Transkription, Roundtrip exakt

### 1. Die verschluesselte Nachricht

287 Zeichen = 143 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
GAGVA AXADF XVAXV XGVDA XDGAF ADFFG FXXXV DAGDX DXDXX VVGGA VDAGG GFDGG AFXDX AGAAF FDGDX GDVDV GGAFX DXAFA VDXFV VXDDF FXDAD DGVGD GDXVX XGDGD DGFFF GVADV XDVXF XDGXA ADDVX XGVDA XXVAX DXGFD DVVFV DAVXA DDGFA FDGAV XAGVD GAFFD DDGAG AGDGF DFXFD XGGFD DGVGA FAXFG AVDGG VFXGD GDFDX VXXAX GDXGG GVGDX GXXGV DFVXA AVGDX DXDGA DXGVA ADFXG GVDGG AX
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

Der Geheimtext hat 287 Zeichen. Bei n = 19 Spalten ergibt das 15 volle Zeilen; die Spaltenlaengen sind `16`×2 und `15`×17.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 14, 0, 2, 18, 7, 4, 9, 17, 13, 16, 5, 12, 15, 3, 1, 8, 6, 10
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
FFVGDAVDXGGGADXGXGFXXGVXVXVGVVAGGGDVFXXGGGFXADGGAGVXVGAFDXDA
AVAAVGDAVDADFXFXVGVFVDVGVGDAGAADDGADDDAXDGGGDFAADXFXVGAFAXDG
DADXXXFDDXGAAGDGFDFXFXVGAFVGFFDADXGGFADXGXGDDXADDVFXVGAFFXDX
XVFDXFXDXFDXFVXDDXXGDXDGAGVDDXXDDDGGAGDGVGVDGVVGDAGGAAAFVGGA
ADFFFXDXXGGDVDADDAXGAFDVFXXGAVDXXVFDXVAXGDDXGVD
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
GERMANIAATAPPEKONSTANTINOPELXRFUERMITTEHMEERDIVIC9VNZUXTEL9V
RX62XDOV2TTELEGRXN0X58XISTELTX32141XQ4XAXVOMX4CNOVEMBERNULED
IGTXA8MIRALSTAFX32398XB
```

### 6. Die entschluesselte Nachricht

**Klartext** (143 Zeichen, `X` = Worttrenner):

```
GERMANIAATAPPEKONSTANTINOPELXRFUERMITTEHMEERDIVIC9VNZUXTEL9V
RX62XDOV2TTELEGRXN0X58XISTELTX32141XQ4XAXVOMX4CNOVEMBERNULED
IGTXA8MIRALSTAFX32398XB
```

*Quelle des Klartexts: Norbert #15 / Max Baertl #39.*

## Korpus Seite 109

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

## Korpus Seite 132

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

## Korpus Seite 146

**Status:** geloest, **bewiesen** — Geheimtext aus unabhaengiger Transkription, Roundtrip exakt

### 1. Die verschluesselte Nachricht

244 Zeichen = 122 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
FVFAF DXAXX GXDXA GVVXX FFFAX DXDXF AGVFV AXAXV VAFXA FVXAA XFGVD XGAXA VAVVX XVDVA AXAFA FFFXV DVXAV AXFGA DFFGA XAADG DAVAX GVGVA VXVGX AXXFX XVFAX XXAVV FAAVA FXAVX VGAGX FGFFV AFAVD FXADA DVAVX XXVGA FXDGX AAAFD AVAAF GVVFA DXVFX AFFVA FVFGX DVFDA XGXXF VFAVD XAAAV XAAXV XAAXX AXDGF GXXV
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

Der Geheimtext hat 244 Zeichen. Bei n = 17 Spalten ergibt das 14 volle Zeilen; die Spaltenlaengen sind `15`×6 und `14`×11.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 7, 16, 4, 10, 13, 8, 0, 2, 11, 1, 5, 14, 9, 3, 12, 6, 15
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
AVDVXXFFXGXAFAAXAXFAFFFAVAXAXGXDAGFAVAAGVFFAFXXAVAVGAADGFDAA
AVFDVAXVAVXXVFXFFAXXVAVXXDAGVFVADFFAXFVXAXFFVFVAAXFDAVDVXXFF
XGXAFAAXAXFAXXDFGAVAXAVXVVFAXXVGFAVAFAVXXDAGXGVGFAXXVFXDAGVA
VXXDAGXAVXVVFAXXFDXXVFXDAGVAVXXDAGXAFAXXXDAGFAAVXVVGVVADVDGG
XVFD
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
FUNKSTELLEKERTSCHERHAE9TRB12X1FXR4FNAMENRICHARDEMILKARLXFUNK
STELLENDORTIGENBEREICHSBENACHRICHTIGENXNACHRICHTENCHEF4BG783
4X
```

### 6. Die entschluesselte Nachricht

**Klartext** (122 Zeichen, `X` = Worttrenner):

```
FUNKSTELLEKERTSCHERHAE9TRB12X1FXR4FNAMENRICHARDEMILKARLXFUNK
STELLENDORTIGENBEREICHSBENACHRICHTIGENXNACHRICHTENCHEF4BG783
4X
```

*Quelle des Klartexts: Norbert #19 / Max Baertl #39.*

## Korpus Seite 153a

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

## Korpus Seite 164a

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

## Korpus Seite 164b

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

180 Zeichen = 90 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
XVDFF XVDGD GVAGD DDDDX XADDG ADAFG XDXXD GGXGD VXDAV VVXGX ADDDG AGGVX DDAGD AVAAD FDAAX GDXXD GXVFD VDDGV DGXXD FGVXG XDADV VVVFD FGXFF GVVVV GXVVX XGDGA XDGGD VGVXV DDGDV GGDVV VVFVG DFVVG FVGXG FXAAX VDDXF DXADG
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

Der Geheimtext hat 180 Zeichen. Bei n = 20 Spalten ergibt das 9 volle Zeilen; die Spaltenlaengen sind `9`×20.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 4, 14, 10, 19, 7, 0, 2, 8, 12, 17, 5, 1, 13, 9, 3, 6, 15, 11, 18, 16
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
VGGGXDVGGVDVAFDVDXGAVXADVGGXDVXGADGGDVXFXDGGDXVGAVXDXFVGXFGG
GAGAFXXDVGAFGGADFDFXXDVXFDVVAXDVDXGVDVXDAVXDXFDXAVDVXFDVXDAX
DVDGVGDDDVGGXFDVADAXDVDGDVGAFXAFDGDVDGXDDVADGXDVDXDVGVDFGVVG
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
XINXTEMESVARXBEFRIEDNISXUNDXDIVVONXMIRCONACHWESTENUNDSUEDENW
EGXLEIDERWEGEVOMGEGNERBESETZTX
```

### 6. Die entschluesselte Nachricht

**Klartext** (90 Zeichen, `X` = Worttrenner):

```
XINXTEMESVARXBEFRIEDNISXUNDXDIVVONXMIRCONACHWESTENUNDSUEDENW
EGXLEIDERWEGEVOMGEGNERBESETZTX
```

*Quelle des Klartexts: Norbert #42 / #43.*

## Korpus Seite 171

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

314 Zeichen = 157 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AAVGF DDADX XDAAV GXAGX AFVAA ADDVD AVDDD DGDDD AAGDV XGVXD GDVXV GVVVF VFFXV VDFVD GVVDV DDVGX DVXVX XGAXA XDDDX XDDXD XXAXD VDXFX ADAGD AGXGA ADDFV XGXDD GDFFA VGDDX XDVVX FVVDA DVFDD VDVAF VXXVV VFFVD VVVGD VFDVD DVVDD DXXVG DVVXX DXDXG VDFFV DDDGG XVFGD DXXDX DDFDX GVFFD DGVGF DDVFA DDDAX DDDAA ADDDD VDDDV XVDVD XVVXV XGVGX XVXXV XVDVA GAGFD VDDAD AXGXD AVXAV DXXGX DXAX
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

Der Geheimtext hat 314 Zeichen. Bei n = 20 Spalten ergibt das 15 volle Zeilen; die Spaltenlaengen sind `16`×14 und `15`×6.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 4, 14, 10, 19, 7, 0, 2, 8, 12, 17, 5, 1, 13, 9, 3, 6, 15, 11, 18, 16
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
GGXDAVVFADVXGGXDDVAVXDXFAAFXDDDVXDADAVGXDVDDVFAVADDXDVGVVXAD
VFDXGVDVGGDGDVXDXFGGXDXGFXDDDGDVGXADAVFDVVDVDXDFAXGGDXFDVVDV
XDXFDVAVGVDXFDVVDDVXXDXFAVXDXFDXFXAXXADVGVADDVDGGGDVADAVXDDG
AVXDXFDVADAXVXADGVAVXDDGXFDVADAXGGDVXFDVADVVDVADDXGVDVDDDDAV
XDDGADAVDXDXDDVXXDXFDXXFAVADFDVVXFDVAVGVDXFDVVDDVXXDXFAVXDXF
DVXDGVDVXDGVDV
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHESZWISCHE
NDEUTSCHLANDUNDSOWJETREGIERUNGUNDERWARTUNGDERWIEDERHERSTELLU
NGRUSSLANDSDURCHDEUTSCHLANDUNDENTENTE
```

### 6. Die entschluesselte Nachricht

**Klartext** (157 Zeichen, `X` = Worttrenner):

```
INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHESZWISCHE
NDEUTSCHLANDUNDSOWJETREGIERUNGUNDERWARTUNGDERWIEDERHERSTELLU
NGRUSSLANDSDURCHDEUTSCHLANDUNDENTENTE
```

*Quelle des Klartexts: Norbert #20 / Max Baertl #39.*

## Korpus Seite 176a

**Status:** geloest — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulaer)

### 1. Die verschluesselte Nachricht

224 Zeichen = 112 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AAAVD ADDDD DFFGA FVFAA AGXGF VVAAF AVDAD GDAVD AVGFG AXFXX XXADX GAVGG ADAVV ADADD VAGDV VAAAA VDFFA VDGAD VAADG VVGFV VADDX AFFGX GGGGV ADVGD VGDGV AFFGA ADVAV DAVVV GADVF XGFFD DAGXA VGFGV AAGXX VGVFG AVGAF GGDXV DXVAA AVVGD FGFGA GDDGG VXGVV VVAGG GDVFG GDDDG ADAA
```

### 2. Der Schluessel

**`Nov10-12`** — n = 16 Spalten, laut Lasry-Liste 46× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
9-12-7-11-3-8-16-6-14-2-10-15-5-13-1-4
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
14, 9, 4, 15, 12, 7, 2, 5, 0, 10, 3, 1, 13, 8, 11, 6
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
4ARUT1OIFSKN3-BZPVLD-JMXCWHQ2E-G0-Y-
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
4 A R U T 1
O I F S K N
3 . B Z P V
L D . J M X
C W H Q 2 E
. G 0 . Y .
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 224 Zeichen. Bei n = 16 Spalten ergibt das 14 volle Zeilen; die Spaltenlaengen sind `14`×16.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 14, 9, 4, 15, 12, 7, 2, 5, 0, 10, 3, 1, 13, 8, 11, 6
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
GAAGAFGVVAFDAFAGGVVAFVDAAFFDVGAFVGDDAVVGAVGGGAAGAFGVVAFDAFAG
GVVADGAFDDGVVAAVAGDXVVDXADGVVADXDAAFGAVGDXDAGAVGAFDXDAAFGADA
DGAVVGDXVGAFDFDAFXVVVGDXGXDDAFGAGGDVADDXDXGDVGAVFFAVDXDAGVVA
DXDDGVVAAVFDVGVGAGAFAVVGDDFXAVGXVGAFGAVGDXGG
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
DURCHBRUCHVORBEREITETXDURCHBRUCHSRICHTUNGNACHNORDENODERNORDO
STENERFOLGENWIRDXKANNJETZTNOCHNICHTBEEURTEILTWERDENX
```

### 6. Die entschluesselte Nachricht

**Klartext** (112 Zeichen, `X` = Worttrenner):

```
DURCHBRUCHVORBEREITETXDURCHBRUCHSRICHTUNGNACHNORDENODERNORDO
STENERFOLGENWIRDXKANNJETZTNOCHNICHTBEEURTEILTWERDENX
```

*Quelle des Klartexts: Norbert #26 / Max Baertl #39.*

## Korpus Seite 187

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

# B. Ungeloeste Korpus-Seiten

Der Geheimtext ist die Roh-Transkription aus `data/corpus.py` (`-` = unlesbares Zeichen). Kein Schluessel, kein Klartext — deshalb nur Schritt 1.

## Korpus Seite 73

**Status:** ungeloest — 1 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

176 Zeichen = 88 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
DFXGD VDXDG GAAAG FFDDV DXFXF GGDDA VGDDD ADGDG FGGDD VVDXD GDAFD DXGXX DGXAV DXXDD GADDF GFAGV DXVFD XFDDF DDDFX DFGXF XVFDD DXXDX GDAGX FDGDD VFXGA XDFVF DVDXV XDFXD DXFDF VDGFD GDADG DGXXF GXFAA AXXXD XAGVX D
```

## Korpus Seite 152

**Status:** ungeloest — 0 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

104 Zeichen = 52 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
FXVAD FDXAA XXFAG VFVDX AAGFD DFDVV VAAVA AXVGX GDAXA AGVAV ADAFD DGVDD FVAVX FVXXV FXXXG FGXGF AFXXG XGFAA AVFFX XFDFV VVAX
```

## Korpus Seite 153b

**Status:** ungeloest — 15 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

93 Zeichen = 46 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AXVAA DDAFF VAXAG GADAF DXAXX XVDGD XVXFF GXFAV VAADA GXXXA XDDGV AVAXV AXAAV VXVAV GXAXX FGXXF AAAFX VADFD XVF
```

## Korpus Seite 158

**Status:** ungeloest — 1 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

240 Zeichen = 120 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
GDDFV VXVDD VVVFG XXVDD XVADD VVFGV VDDVV DVAXV XVGVV GVXDD XVVVG XGVDD GDXVA VGGAA AXGAF FADVD ADDVA XVDVV DDDGA DAXFA XXFGF FXFXD VVDDX DGDDA XVAVX XVVVV FGDVV FGDVV FGVDD DAGGV XDGXD DVVXX VDGVV VXGDX XVXVA DDFGG GDXAX VFXVD GDDFV GVGVD GVGVV DADVV DADVV VGAVV XVDGG XFAXV XGVVD DDXXF
```

## Korpus Seite 170

**Status:** ungeloest — 0 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

106 Zeichen = 53 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AAGVG VVDAG GAGAV AGGAA VAXGV AAAXF AAXAF AGVGV VVVVG DADAF GDVGV GVGAD XAGAA GXGGA GVFVG XGXAG GGAFA XGFXX AGXVG VFDVX VDFGX V
```

## Korpus Seite 176b

**Status:** ungeloest — 0 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

220 Zeichen = 110 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
GGDAA FXAVD FFFDG XXAGV XXXDV XAAFV GAGAF VFAGA VDDDD AVXGF FAFXG XXXXX GAVAA AAGDV GGGVA AXDVX XXFAD FXXXX DGVDG FDVGD DAADV XXXFV XGXXD XGGGG AGVDG VAGGG DVVDF VAFAV VVXDF DFFFF XXXAX XGVDX XFXDF FXXDX XXXXV GGGDA FGGDX VVVAA FDVFX XVXXF VGGFG DAAFV GGGGX AVVVV
```

## Korpus Seite 187b

**Status:** ungeloest — 0 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

142 Zeichen = 71 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AFAFF AXDVA VVVVF ADVFA GXGVX AGVAX AXGGA AAAAA ADDVV XVGAG AGXVV FGAAF VVXGD GGAVG VFDVD VDDDV DXFAD DDDAX ADVVG AAFFG XGXAG GDADF VFXDA DGDDG GAAXD VDFAD FFDDX VADDV GD
```

## Korpus Seite 189

**Status:** ungeloest — 5 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

84 Zeichen = 42 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
DVGAG GAAVV AXFVX XVADA XXAGA VDVGX AXVVX VVVAV DXVXX XVGVX AAVAG AXXGA XXFXV XXFXX GVVVD FFXDX AXDV
```

## Korpus Seite 198

**Status:** ungeloest — 0 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

165 Zeichen = 82 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
DFVXV XGAXD GXVXD VGVGD VADXF FADVX XXVFV AAXGF DGFFA VXAVV VXVFV GFVFG DGVFG FFFGV VVGGG XVFXF XXFVD VDFDD FXAAX VVXAA FXXXV GXFVD VVXXF FGXGV FGXFG GFAAA FGXVV FXXXF FADXD AFXFV VDGVX FGAGF ADDFX
```

## Korpus Seite 215

**Status:** ungeloest — 9 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

237 Zeichen = 118 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
VGADA FAXAD XFAXF FVXDD XXXDX DFDDA VFVGX DFFXD GFVVV FAGXX XAFAG DDFAV DGVAV XFAFD XAFDG ADVAF FVVFF AAXDG VVAVX XVGDF DFVVG DFAAF AVFVX GGVFA AAXXD AVAVF FADAF AAXAG GADAD VDFVV DFGAA VAAXA DVDAX VFDFG DFGVF AGDDA FGGDV FFDXV DFAAA XXADG FFDFF XVAAA AXXVX FXDFX GFDAV AADFD DVVXX XF
```

## Korpus Seite 217

**Status:** ungeloest — 0 unlesbare Zeichen in der Transkription

### 1. Die verschluesselte Nachricht

170 Zeichen = 85 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
DXXXG GVXAX ADXVD GDAAA DGXAG AVDGV FAFAA DFFFG XFVXD DVDVF GFVVV AADXG AAVAV AAXDG VADDD DVADG FAGVV GVVGD AVXFF DAADV FFAXG VDVDD AGDVF XAAVA ADDAF FDFAA GXVAA GAFXD ADFFX AVDAA DADXX AADVA XVVAD FDVAA
```

# C. Seite 217 (RICHI-170) — extern bewiesen

Nicht ueber die Lasry-Liste geloest, sondern ueber das **Schluesselwort** `TRUPPENVERSCHIEBUNG`: es liefert die Permutation, das Quadrat wird aus dem Paar (Geheimtext, Klartext) rekonstruiert.

## Seite 217 / RICHI-170

**Status:** geloest, **bewiesen** — Roundtrip exakt, 0 Konflikte

### 1. Die verschluesselte Nachricht

170 Zeichen = 85 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
DXXXG GVXAX ADXVD GDAAA DGXAG AVDGV FAFAA DFFFG XFVXD DVDVF GFVVV AADXG AAVAV AAXDG VADDD DVADG FAGVV GVVGD AVXFF DAADV FFAXG VDVDD AGDVF XAAVA ADDAF FDFAA GXVAA GAFXD ADFFX AVDAA DADXX AADVA XVVAD FDVAA
```

### 2. Der Schluessel

**Schluesselwort `TRUPPENVERSCHIEBUNG`** — liefert die Permutation. Das Quadrat wird aus dem Paar (Geheimtext, Klartext) rekonstruiert (26 von 36 Zellen direkt belegt, Rest aufgefuellt).

### 3. Die Permutation

Rangfolge der 19 Buchstaben des Schluesselworts:

```
16-13-17-11-12-3-9-19-4-14-15-2-7-8-5-1-18-10-6
```

### 4. Das Quadrat

```
TRUPE4NBSC2HJIMQVG6AYD0F135KL7O8WX9Z
```

```
T R U P E 4
N B S C 2 H
J I M Q V G
6 A Y D 0 F
1 3 5 K L 7
O 8 W X 9 Z
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 170 Zeichen. Bei n = 19 Spalten ergibt das 8 volle Zeilen; die Spaltenlaengen sind `9`×18 und `8`×1.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 15, 11, 5, 8, 14, 18, 12, 13, 6, 17, 3, 4, 1, 9, 10, 0, 2, 16, 7
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
AVFDDAAVDAFXVVFDDFDGDXAVADVGADAVAFXXAVADAVFDDAVVFDAVFXXGDFAV
XFGDDFAAXAAGXAVVXGDFAXDFAAAVDAXGAVFDDAFXAVDFDGDXXFGDGGAVADGG
AVADXGGDVVVVFDFDAVADAAAVDAGXXAVVFXAADVGADFAAAVDAXG
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENXEINGESCHWADERD
ERXALLIIERTENFOLGT26STENX
```

### 6. Die entschluesselte Nachricht

**Klartext** (85 Zeichen, `X` = Worttrenner):

```
EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENXEINGESCHWADERD
ERXALLIIERTENFOLGT26STENX
```

**Lesefassung:** Ein englischer Kreuzer liegt in Sewastopol. (am) 24. Ein Geschwader der Alliierten folgt (am) 26.

# D. Nachrichten aus dem Childs-Buch (ausserhalb des Korpus)

## RICHI-264

**Status:** geloest, **bewiesen** — 2 Reparaturen, exakter Roundtrip

### 1. Die verschluesselte Nachricht

264 Zeichen = 132 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
DVDVF DVFAG XVXFF FVGGG AGGXA XDXGF XVVDD GFGFD FAVGV DAFGF GXDFD XVVDG DGVFF GDXDG AXAXV GVGAA AVFVG VFDGD XAFDX AXGVF AGDDD VGDVV GGDGG GVAAD DGDVF VDDDX DVXDX DVDVA VGXVV DFVFD AXDGD AVGXD DDADG FVGDG AVAXD ADDGG FDFAG GFAXG FFXDG GGVGA FDFXX DAGAV GDVVF GXGFV FDXAA VAGAG AAVGD GGGFD VAGGV XAADD DDAVA VVADG DGDD
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

Der Geheimtext hat 264 Zeichen. Bei n = 19 Spalten ergibt das 13 volle Zeilen; die Spaltenlaengen sind `14`×17 und `13`×2.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 14, 0, 2, 18, 7, 4, 9, 17, 13, 16, 5, 12, 15, 3, 1, 8, 6, 10
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
GAVGVDGGXGDDVFFFVGVFVGGGGGAAVDVGVFDADVXGVGVDFXAFADDDVFVGDVDD
VFADAVAVVGDGAGGGVVAGDVVXAGAFADGGXGDDVFAGGAVGDVDVXGGVVGDFGFDX
GGADVVADAFVAVGGFDXDGVGDAFXVGADAFFXGFADVGAVDADXGXFDFGGXXFDXAA
GGGADXGVDGFFDXDAAAVDDXDXAFFGDDVFDXDAAGVGVDDXFDDXFFDAAGDVDVDX
GVDXAVDADXGXFDFGGDFGDXDX
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
DEMNACHGEHENNUMEHRSAEMTLICHESCHIFFEVONKOSPOLINACHODESSABEZWX
NIKILJEWXVERTEILTWIEFRX52751XUNDXBVGXRUMXXL7CHXROEMX2XGROSSX
BXFRX52787XX
```

### 6. Die entschluesselte Nachricht

**Klartext** (133 Zeichen, `X` = Worttrenner):

```
DEMNACHGEHENNUMEHRSAEMTLICHESCHIFFEVONKOSPOLINACHODESSABEZWX
NIKOLAJEWXVERTEILTWIEFRX52751XUNDXBVGXRUMXXL7CHXROEMX2XGROSS
XBXFRX52787XX
```

**Lesefassung:** Demnach gehen nunmehr saemtliche Schiffe von Kospoli nach Odessa bzw. Nikolajew. Verteilt wie Fr. 52751 und B.V.G. rum. L7 Ch. Roem. 2. Gross B. Fr. 52787.

**Die zwei Reparaturen:** Bigramm 63 `AD` → `AG` (D/G-Verwechslung, Morse-plausibel), und `XG` fehlt nach Bigramm 64.

## RICHI-222

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

## RICHI-274

**Status:** geloest, verifiziert (Roundtrip)

### 1. Die verschluesselte Nachricht

270 Zeichen = 135 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
AAXFA VDXFD DAGAA AAFAA DAVDA XAADX GXAAA XFFAX VAAVD AAGVG DXXVG AAVDA GXDXG XFXXV VDXGV VXGFX VFDAF FADFA VXDAX FAXXG VFXVV ADAVA AADGF XDXAD FDAVA VFGAF FADAA FXFDF XXDAX VDXAA FDXGX ADXXX DXFXX DFFAA FXGAD DFGVA XDFGD XXDFX XAGAD AFVAF XXXAF FFAGF VVVAX GAFAA ADAAX AGADV GVVDA AAVVX XFGXF AFVGF XFDAV GFDGD VXFFD DXXXX
```

### 2. Der Schluessel

**`Oct28-31`** — n = 18 Spalten, laut Lasry-Liste 33× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
6-15-12-16-5-7-14-4-13-8-11-1-17-2-10-3-18-9
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
11, 13, 15, 7, 4, 0, 5, 9, 17, 14, 10, 2, 8, 6, 1, 3, 12, 16
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
HI20SXRUWQY8EK7O619CBJAP453FDZTGLMVN
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
H I 2 0 S X
R U W Q Y 8
E K 7 O 6 1
9 C B J A P
4 5 3 F D Z
T G L M V N
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 270 Zeichen. Bei n = 18 Spalten ergibt das 15 volle Zeilen; die Spaltenlaengen sind `15`×18.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 13, 15, 7, 4, 0, 5, 9, 17, 14, 10, 2, 8, 6, 1, 3, 12, 16
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
VVDAGVAAXAFAXAFGGFXVFGXXFADDDAFAXXFDGVFADDVGFAXXGFFADAFAADXA
AVGVGFXADAGVXXAVGXFGDAXAFAFADAVGFGXFXDXAAVADXXVVFAXVFAXXXADD
FAXFXFDFGVXXXXDDXXVVDFFGAAADXXAVFGXFGDAAFAFADAVGFGXFXDFAXXDF
FADAVVFAXXDDXXVVDFADFADFFAADXAFADAXADAGVXXAVGXFGDAXAXDFAVVGV
GDAAXAADAVXAAXAXVVFADDXAVXADXA
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
DRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTU
ELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDA
CHTISTXXDEUTZIT
```

### 6. Die entschluesselte Nachricht

**Klartext** (135 Zeichen, `X` = Worttrenner):

```
DRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTU
ELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDA
CHTISTXXDEUTZIT
```

**Lesefassung:** Drahtet ob von euren Kaeufen bereits Abtransporte erfolgt sind. Eventuell wann und wohin solche erfolgen werden und wie weiter Transport gedacht ist. Deutz it...

Die Tabelle im Buch ist 15 Zeilen × 18 Zeichen und **zeilenweise** notiert; fuer die Entschluesselung wird sie **spaltenweise** gelesen (der oben gezeigte Geheimtext ist bereits die spaltenweise Lesung). Schluessel `Oct28-31` erstmals an echtem Klartext geprueft.

## RICHI-338

**Status:** geloest, **NICHT** roundtrip-verifiziert (22 CT-Fehler in der Tabelle)

### 1. Die verschluesselte Nachricht

306 Zeichen = 153 Bigramme. Gruppiert in Fuenfergruppen (Transkriptions-Konvention):

```
VAXVV VAVGV FVGFX FDVAA AGADX FAXDF XAAGD DFVXD AAAXA VDAXA AADGA GXAXF AFGAF FADFF VFXFF GDXXV GAAVD VAADX DFAFV XXVVD XGAAV DAAAV AFDAF FADFX XXXFD VGDFD XXXDX FFDXA AGXGX AXFFD DXXDA XGXDF XVVXD AXVDX ADGVX GXGXX ADGFX DXDDA XFDDG DADXF DDAGA XGAGF FDFXG ADDFG VDAFX FXAVA XXAFF FAGGX ADADX FAFAA ADAAX DFXXA AAAFV DAAAV VXGFF DFFAF XXXGV FXVVX GGAFV XGAFF AXVAA V
```

### 2. Der Schluessel

**`Oct28-31`** — n = 18 Spalten, laut Lasry-Liste 33× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
6-15-12-16-5-7-14-4-13-8-11-1-17-2-10-3-18-9
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
11, 13, 15, 7, 4, 0, 5, 9, 17, 14, 10, 2, 8, 6, 1, 3, 12, 16
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
HI20SXRUWQY8EK7O619CBJAP453FDZTGLMVN
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
H I 2 0 S X
R U W Q Y 8
E K 7 O 6 1
9 C B J A P
4 5 3 F D Z
T G L M V N
```

### 5. Wie man entschluesselt

**Schritt 1 — Spaltentransposition rueckgaengig machen**

Der Geheimtext hat 306 Zeichen. Bei n = 18 Spalten ergibt das 17 volle Zeilen; die Spaltenlaengen sind `17`×18.

Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer **Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau dieser Reihenfolge wieder ein:

```
Leseordnung (Spaltenindex, 0-basiert): 11, 13, 15, 7, 4, 0, 5, 9, 17, 14, 10, 2, 8, 6, 1, 3, 12, 16
```

Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):

```
VGDDFADAAXAVGVDDXFAXDFFAADXXDAFAADGDAAAXVVFGGXGXFAXFGXDDXXFD
XAAXVVDAGVAAXAFAXAFGGFXVFGXXFADDDAFAXXFDGVFADDVGFXDAFAAAFVXA
ADFAXXAFGAGVVXDGGVFXXAGGFADFDAAFFDXGXFVAAXVFAVXFXAXFXVXAVXFA
XADDXDXFGDAFXXXAFXXAXAVAAGAXDVGDDVAFVAFAGFFADXGGVFADXFVDDAAF
FFDXFFFXXAVDDADVAAFFFDXXXAVXADXAAVVDAAGXDFVADAAXGXGXDFGDVFXD
VGXAVX
```

**Schritt 2 — Substitution rueckgaengig machen**

Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle ist der Klartextbuchstabe.

```
FUERXSAULXWEINREICHXDOPPELPUNKTXDRAHTETOBVONEURENKAEUF1REH6T
IEN29AZQA1TJEWR2KML4X3SLTLVTZETUGLC2NT1TT40XYCY24EBE8J3IL5R2
7871T5RYH7KNTZITS5HPW4RXPPWC3GFTZ
```

### 6. Die entschluesselte Nachricht

**Klartext** (162 Zeichen, `X` = Worttrenner):

```
FUERXSAULXWEINREICHXDOPPELPUNKTXDRAHTETOBVONEURENKAEUF1REH6T
IENABTRANSPORT7ERFOLGNNSN24VHLTUELLWANNUNDWOHINSOLCHEERFOLGE
NWERDEXUNDWIEWEITERTRANSPORTGEDACHTISTXXDE
```

**Lesefassung:** Fuer Saul Weinreich Doppelpunkt: Drahtet ob von euren Kaeufen Abtransporte erfolgt sind. Eventuell wann und wohin solche erfolgen werden und wie weiter Transport gedacht ist. De...

Beginnt mit den drei Einleitungszeilen `FUER SAUL WEINREICH DOPPELPUNKT`. Die Tabelle ist 18 Zeilen × 18 Zeichen und enthaelt OCR-Artefakte (`5`, `f`, `P`, `%`, `i`). Re-Encryption des Klartexts ergibt 22 Abweichungen — der Klartext ist sprachlich plausibel, aber nicht hart belegt.

## RICHI-240

**Status:** verifiziert, **nicht von diesem Projekt geloest**

### 1. Die verschluesselte Nachricht

*Kein Geheimtext im Repo abgebildet.*

### 2. Der Schluessel

**`Nov10-12`** — n = 16 Spalten, laut Lasry-Liste 46× verwendet.

### 3. Die Permutation

Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` (1 = kleinster Rang, wird zuerst ausgelesen).

```
9-12-7-11-3-8-16-6-14-2-10-15-5-13-1-4
```

Leseordnung (Spalten in aufsteigender Rangfolge):

```
14, 9, 4, 15, 12, 7, 2, 5, 0, 10, 3, 1, 13, 8, 11, 6
```

### 4. Das Quadrat

36 Zeichen, zeilenweise gelesen:

```
4ARUT1OIFSKN3-BZPVLD-JMXCWHQ2E-G0-Y-
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
4 A R U T 1
O I F S K N
3 . B Z P V
L D . J M X
C W H Q 2 E
. G 0 . Y .
```

### 5. Wie man entschluesselt

*Nicht moeglich — der Geheimtext ist nicht im Repo abgebildet. Der Klartext stammt aus einer externen Quelle.*

### 6. Die entschluesselte Nachricht

**Klartext** (156 Zeichen, `X` = Worttrenner):

```
ANOBERSTEHEERESLEITUNGX11XARMEEXALPENKORPSIMRAUMPETERREVEVER
BASZX217X219XDIVISIONENUND6XRESERVEDIVISIONANDERLINIENAGYBEC
SKEREKVERSECXVERSECVONSERBENBESETZTX
```

**Lesefassung:** An Oberste Heeresleitung. 11. Armee: Alpenkorps im Raum Peterreve-Verbasz. 217.-219. Divisionen und 6. Reserve-Division an der Linie Nagybecskerek-Versec. Versec von Serben besetzt.

Der Geheimtext ist **nicht im Repo abgebildet** — von 240 Zeichen sind 220 ueberliefert. Die 20 fehlenden Zeichen wurden extern ergaenzt (`VFFXX DXXVV XDXDX GXXAF`), drei Ziffern ueber ein franzoesisches Aufklaerungstelegramm bestimmt (7, 9, 6). Quelle: prinzai.com, 19.09.2026.
