# RICHI-264

*D. Nachrichten aus dem Childs-Buch — Kryptogramm 24 von 28*

[← vorherige](seite-217---richi-170.md) | [Index](README.md) | [naechste →](richi-222.md)

---

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


---

[← vorherige](seite-217---richi-170.md) | [Index](README.md) | [naechste →](richi-222.md)
