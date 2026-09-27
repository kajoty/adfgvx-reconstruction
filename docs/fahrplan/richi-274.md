# RICHI-274

*D. Nachrichten aus dem Childs-Buch — Kryptogramm 26 von 28*

[← vorherige](richi-222.md) | [Index](README.md) | [naechste →](richi-338.md)

---

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


---

[← vorherige](richi-222.md) | [Index](README.md) | [naechste →](richi-338.md)
