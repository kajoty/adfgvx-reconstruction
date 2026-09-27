# RICHI-338

*D. Nachrichten aus dem Childs-Buch — Kryptogramm 27 von 28*

[← vorherige](richi-274.md) | [Index](README.md) | [naechste →](richi-240.md)

---

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


---

[← vorherige](richi-274.md) | [Index](README.md) | [naechste →](richi-240.md)
