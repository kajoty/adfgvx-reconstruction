# Korpus Seite 100

*A. Geloeste Korpus-Seiten — Kryptogramm 1 von 28*

[Index](README.md) | [naechste →](korpus-105.md)

---

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


---

[Index](README.md) | [naechste →](korpus-105.md)
