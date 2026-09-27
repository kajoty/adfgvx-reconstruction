# Korpus Seite 171

*A. Geloeste Korpus-Seiten — Kryptogramm 9 von 28*

[← vorherige](korpus-164b.md) | [Index](README.md) | [naechste →](korpus-176a.md)

---

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


---

[← vorherige](korpus-164b.md) | [Index](README.md) | [naechste →](korpus-176a.md)
