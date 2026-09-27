# Korpus Seite 146

*A. Geloeste Korpus-Seiten — Kryptogramm 5 von 28*

[← vorherige](korpus-132.md) | [Index](README.md) | [naechste →](korpus-153a.md)

---

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


---

[← vorherige](korpus-132.md) | [Index](README.md) | [naechste →](korpus-153a.md)
