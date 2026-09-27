# Korpus Seite 105

*A. Geloeste Korpus-Seiten — Kryptogramm 2 von 28*

[← vorherige](korpus-100.md) | [Index](README.md) | [naechste →](korpus-109.md)

---

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


---

[← vorherige](korpus-100.md) | [Index](README.md) | [naechste →](korpus-109.md)
