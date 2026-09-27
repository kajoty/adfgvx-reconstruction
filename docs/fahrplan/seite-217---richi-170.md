# Seite 217 / RICHI-170

*C. Seite 217 (RICHI-170) — Kryptogramm 23 von 28*

[← vorherige](korpus-217.md) | [Index](README.md) | [naechste →](richi-264.md)

---

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


---

[← vorherige](korpus-217.md) | [Index](README.md) | [naechste →](richi-264.md)
