# Korpus Seite 176a

*A. Geloeste Korpus-Seiten — Kryptogramm 10 von 28*

[← vorherige](korpus-171.md) | [Index](README.md) | [naechste →](korpus-187.md)

---

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


---

[← vorherige](korpus-171.md) | [Index](README.md) | [naechste →](korpus-187.md)
