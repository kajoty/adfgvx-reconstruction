# Handbuch zum ADFGVX-Projekt

Ein Leitfaden für Außenstehende.
Geschrieben nach den Regeln von Wolf Schneider: kurze Sätze, aktive Verben, klare Wörter.

---

## 1. Worum geht es hier?

Im Ersten Weltkrieg verschlüsselte das deutsche Heer seine Funksprüche mit einer Chiffre namens **ADFGVX**.
Der Name besteht aus sechs Buchstaben: A, D, F, G, V, X.
Diese sechs Buchstaben sind die einzigen Zeichen, die im Geheimtext vorkommen.

Viele dieser Funksprüche sind erhalten.
Einige davon hat bis heute niemand entziffert.
Dieses Projekt versucht, sie zu entziffern.

Das klingt nach Kryptanalyse. Ist es aber nur zum Teil.
Die eigentliche Arbeit ist **Datenrekonstruktion**.
Dazu später mehr — das ist die wichtigste Erkenntnis des ganzen Projekts.

---

## 2. Was ist ADFGVX? Eine Chiffre in zwei Stufen

ADFGVX arbeitet in zwei Schritten.
Man muss beide verstehen, sonst versteht man nichts.

### Stufe 1: Das Polybius-Quadrat

Man schreibt ein 6×6-Quadrat.
Darin stehen 26 Buchstaben und 10 Ziffern — also 36 Zeichen.

```
     A  D  F  G  V  X
A    B  C  E  F  G  H
D    I  J  K  L  M  N
F    O  P  Q  R  S  T
G    U  V  W  X  Y  Z
V    0  1  2  3  4  5
X    6  7  8  9  .  /
```

Jedes Klartextzeichen bekommt nun **zwei** Zeilen-/Spaltenbuchstaben.
Aus `B` wird `AA`. Aus `R` wird `FG`. Aus `7` wird `XD`.

So wird der Text doppelt so lang.
Und er besteht nur noch aus sechs Buchstaben.

**Wie entsteht das Quadrat?**
Auf zwei Wegen.

**Weg 1 — aus einem Schlüsselwort bauen.** Doppelte Buchstaben streichen, mit dem Restalphabet auffüllen.
Diese Regel steht in `core/adfgvx.py` als `make_square()`.
Aus `KOMMANDO` wird erst `KOMAND` — das zweite `M` und das zweite `O` fallen weg.
Dann kommt das Restalphabet:

```
K O M A N D B C E F G H I J L P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9
```

Das Alphabet läuft von `B` bis `9`, aber ohne `K`, `O`, `M`, `A`, `N`, `D`.
Die stehen schon vorn.

Friedman beschreibt genau das.
Das Quadrat sei „in mixed order, often according to some key word" gemischt.
Und er zeigt Beispiele: Ein Quadrat beruht auf `GERMAN MILITARY CIPHERS`, ein anderes auf `XYLOPHONIC BEDLAM`.

**Weg 2 — frei mischen.** Die 36 Zeichen ohne Regel verteilen.
Auch das kam vor.
Friedman schreibt „often" — nicht „immer".

**Was im Projekt steht.** Alle 14 Quadrate in `core/adfgvx.py` sind frei gemischt.
Die Ziffern stehen dort wild verstreut, nicht am Ende.
Beispiel `Nov1-3`:

```
UILOF9RCZVSX02G7QTD8WNB5JMHEKPY41A36
```

Die Ziffern sitzen an den Positionen 5, 12, 13, 15, 19, 23, 31, 32, 34, 35.
Ihre Reihenfolge lautet `9027854136` — kein Muster.

**Warum das Quadrat ein eigenes Geheimnis war.**
Friedman schreibt: „both the checkerboard and the transposition key were changed daily".
Childs bestätigt das für die RICHI-Chiffre: Der Schlüssel hatte eine Lebensdauer von drei Tagen.
Beide Teile wurden also **regelmäßig gewechselt** — Quadrat und Transpositionswort getrennt voneinander.
Wer das Quadrat kennt, hat noch nicht den Spruch.

**Und noch eins:** Diese Regel gilt nur für das Quadrat.
Das Transpositionswort in Stufe 2 wird *nicht* aufgefüllt.
Es bleibt, wie es ist — siehe Abschnitt 7.

### Stufe 2: Die Spaltentransposition

Jetzt kommt ein zweites Schlüsselwort ins Spiel.
Man schreibt die Bigramme zeilenweise unter dieses Wort.
Dann liest man sie spaltenweise wieder heraus — aber in der Reihenfolge des Alphabets der Schlüsselbuchstaben.

Ein Beispiel mit dem Wort `BART`:

```
B  A  R  T     <- Schlüsselwort
1  2  3  4     <- Rang der Buchstaben im Alphabet
```

`A` ist der kleinste Buchstabe, also Rang 1.
`B` ist Rang 2. `R` ist Rang 3. `T` ist Rang 4.

Gelesen wird also Spalte 2, dann Spalte 1, dann Spalte 3, dann Spalte 4.

**Wichtig — und hier stolpern fast alle:**
Die Permutation ist eine **Rangfolge**, keine Lesereihenfolge.
Im Code steht deshalb:

```python
order = sorted(range(n), key=lambda c: perm[c])
```

Wer das verwechselt, bekommt Unsinn. Das Projekt hat genau diesen Fehler dokumentiert.

### Der ganze Weg in einem Bild

```mermaid
flowchart LR
    A["Klartext<br/>ANGRIFF"] --> B["Polybius-Quadrat<br/>Stufe 1"]
    B --> C["Bigramme<br/>AD FG GV ..."]
    C --> D["Spaltentransposition<br/>Stufe 2 + Schlüsselwort"]
    D --> E["Geheimtext<br/>nur A D F G V X"]
```

Zum Entschlüsseln läuft alles rückwärts.
Man braucht dazu **zwei** Dinge: das Quadrat und das Schlüsselwort.

---

## 3. Was macht dieses Projekt konkret?

Das Projekt sammelt historische ADFGVX-Funksprüche.
Es prüft sie, korrigiert Lesefehler und versucht, sie zu entschlüsseln.

Die Arbeit läuft in vier Schritten:

1. **Sammeln.** Die Geheimtexte stammen aus Büchern und Scans. Sie liegen in `data/corpus.py`.
2. **Prüfen.** Stimmt der Text? Gibt es Lesefehler? Dafür gibt es die Skripte in `analysis/`.
3. **Entschlüsseln.** Verschiedene Löser in `solvers/` suchen Quadrat und Schlüsselwort.
4. **Beweisen.** Ein Ergebnis gilt erst, wenn es sich exakt nachrechnen lässt.

Der Kern des Ganzen liegt in `core/`.
Dort stehen die Chiffre (`adfgvx.py`) und das Sprachmodell (`langmodel.py`).

---

## 4. Die wichtigste Erkenntnis: Das Problem ist die Datenqualität

Das ist der Kernsatz des Projekts:

> **Nicht die Kryptanalyse ist das Problem. Die Daten sind das Problem.**

Die alten Funksprüche wurden von Hand abgeschrieben.
Dann wurden sie gescannt.
Dann hat eine OCR-Software sie gelesen.
Dann hat ein Mensch sie noch einmal abgetippt.

Auf jedem dieser Wege gehen Zeichen verloren oder werden falsch.
Ein `V` wird zu einem `X`. Ein `G` zu einem `F`.
Und schon ist der ganze Spruch unlesbar.

Das Projekt hat das gemessen.
Auf Seite 171 zum Beispiel:

- Der rohe Text hat 314 Zeichen.
- Nur 205 davon — also 65,3 Prozent — passen zum entschlüsselten Klartext.
- Die Editierdistanz beträgt 70: 8 Einfügungen, 4 Löschungen, 58 Ersetzungen.
- Das ist eine Fehlerquote von 22,3 Prozent.

Wer bei so einer Fehlerquote blind nach dem Schlüssel sucht, sucht ewig.
Deshalb dreht das Projekt die Reihenfolge um: **erst die Daten reparieren, dann entschlüsseln.**

---

## 5. Das schärfste Werkzeug: die Konfliktzahl

Das Projekt hat ein Kriterium gefunden, das exakt ist.
Es heißt **Konfliktzahl**.

Die Idee ist einfach.
Wenn Quadrat und Permutation stimmen, dann bildet jedes Bigramm auf **genau ein** Klartextzeichen ab.
Kommt ein Bigramm zweimal vor und liefert zwei verschiedene Zeichen, dann stimmt etwas nicht.

Die Konfliktzahl zählt genau diese Widersprüche.

```python
mapping = defaultdict(Counter)
for bg, ch in zip(bigrams, pt):
    mapping[bg][ch] += 1
conflicts = sum(len(v) - 1 for v in mapping.values())
```

Es gilt:

- `conflicts == 0` bedeutet: Quadrat, Permutation und Geheimtext passen exakt zusammen.
- `conflicts > 0` bedeutet: Mindestens ein Zeichen ist falsch.

Das Projekt hat das geprüft.
Ergebnis: **Alle 11 geprüften Korpus-Seiten zeigen nach der Korrektur null Konflikte.**
Vorher lagen sie bei 34 bis 107 Konflikten.

Warum 11 und nicht 12? Das Projekt kennt 12 Lösungen.
Aber eine davon (Seite `??`, Schlüssel `Nov22-24`) hat keine Korpus-Seite in `data/corpus.py`.
Sie stammt aus einem Forum und ist nicht Teil der 22 Seiten.
Der Konflikt-Test läuft nur über Korpus-Seiten — deshalb 11.

> **Wichtig — was die Konfliktzahl beweist und was nicht.**
> Die Konfliktzahl ist nur dann ein *Beweis*, wenn sie gegen ein
> **unabhängig überliefertes** Chiffrat geprüft wird. Das trifft auf die
> Seiten **100**, **105** und **146** zu. Für die übrigen gelösten Seiten
> wurde der Geheimtext aus dem Klartext **rekonstruiert**
> (`transpose(bigrams(pt), perm)`) — dort ist der Roundtrip per Konstruktion
> garantiert und die Konfliktzahl 0 trivial. Siehe Abschnitt 7.

Die Konfliktzahl ist also ein Beweis, kein Gefühl.
Aber sie hat einen Haken: Man braucht den Klartext, um sie zu messen.
Für unbekannte Seiten hilft sie erst, wenn man einen Kandidaten hat.

---

## 6. Die Werkzeuge im Einzelnen

### Das Sprachmodell (`core/langmodel.py`)

Das Modell bewertet, wie „deutsch" ein Text aussieht.
Es zählt Einzelbuchstaben, Buchstabenpaare und Buchstabentripel.
Die Häufigkeiten stammen aus `data/de_50k.txt`.

Die Bewertungsskala:

| Textart | Score |
|---|---|
| Echter deutscher Text | −16 bis −21 |
| Zufallstext | −27 bis −32 |
| Lesbarkeitsschwelle | etwa −24 |

Dazu kommt `word_hits()`: Es zählt, wie viele echte Wörter im Text stecken.

**Warnung aus dem Projekt:** Das Trigramm-Modell schadet bei historischem Militärtext mehr, als es nützt.
Die Sprache ist zu eigen. Man sollte es abschalten oder niedrig gewichten.

### Die Löser (`solvers/`)

| Datei | Verfahren |
|---|---|
| `blind_solver.py` | Simulated Annealing über Quadrat und Permutation |
| `sub_solver.py` | Simulated Annealing über das Quadrat, Permutation bekannt |
| `analytic_solver.py` | Häufigkeitsanalyse als Start, dann Hill Climbing |
| `guided_solver.py` | Gezielte Suche mit Abdeckungskriterium |
| `friedman_solver.py` | Struktureller Ansatz nach Friedman |
| `conflict_solver.py` | Sucht Fehler über die Konfliktzahl |
| `reverse_square.py` | Rekonstruiert das Quadrat aus gelösten Texten |

### Die Analyse (`analysis/`)

Der Ordner enthält 36 Skripte. Hier ist die vollständige Liste.

**Verifikation und Beweise:**

| Datei | Aufgabe |
|---|---|
| `verify_article_claim.py` | Prüft die Behauptung zu Seite 217 |
| `verify_217.py` | Vollständige Prüfung aller Konventionen für Seite 217 |
| `verify_solutions.py` | Prüft alle gelösten Seiten gegen den Klartext |
| `verify_richi_264.py` | Beweis für RICHI-264 (2 Reparaturen, Roundtrip) |
| `richi_222.py` | RICHI-222: Prüfung der Struktur |
| `richi_222_reconstruct.py` | RICHI-222: Struktur-Beweis + Beam-Search-Kandidat |
| `verify_corpus_provenance.py` | Vergleicht den Korpus mit der Originalquelle |
| `parse_cipherbrain.py` | Extrahiert die Artikel-Transkription aus dem HTML |
| `dump_keys.py` | Erzeugt die Schlüssel- und Spruchtabellen für die README |
| `rank_conflicts.py` | Belegt die Konfliktzahl als exaktes Kriterium |

**Reparatur und Suche:**

| Datei | Aufgabe |
|---|---|
| `repair_171.py` | Repariert Seite 171 per Editierdistanz |
| `reconstruct_171.py` | Rekonstruiert Seite 171 |
| `search_all.py` | Testet alle Seiten gegen alle 14 Schlüssel |
| `search_fix.py` | Sucht pro Seite und Schlüssel nach Korrekturen |
| `search_fix2.py` | Korrekturen mit 1–2 Einfügungen/Löschungen |
| `fix_search.py` | Sucht Einfüge-/Löschoperationen für lesbaren Text |
| `run_corpus.py` | Testet den ganzen Korpus gegen alle Schlüssel |
| `solve_152.py` | Gezielter Angriff auf Seite 152 (SA, langsam) |
| `solve_152_fast.py` | Seite 152 mit dem analytischen Solver (schnell) |
| `solve_73.py` | Lösungsversuch Seite 73: alle Schlüssel durchprobieren |

**Anomalien:**

| Datei | Aufgabe |
|---|---|
| `anomaly_scan.py` | Sucht fehlende Zeichen, testet Hypothesen |
| `analyze_170.py` | Tiefenanalyse der Seite 170 (RICHI-240) |

**Seite 217:**

| Datei | Aufgabe |
|---|---|
| `exhaustive_217.py` | Erschöpfende Suche nach der Transpositionskonvention |
| `new_approach_217.py` | Korrigierter Ansatz: `TRUPPENVERSCHIEBUNG` als Transpositionswort |
| `refine_217.py` | Verfeinert die Transpositionskonvention |

**Quellen-Arbeit (PDF und Scans):**

| Datei | Aufgabe |
|---|---|
| `extract_friedman.py` | Holt Text aus dem Friedman-PDF |
| `childs_scan.py` | Sucht ungelöste Seiten im Childs-Buch |
| `pdf_page_order.py` | Ordnet gedruckte Seitenzahlen den PDF-Seiten zu |
| `pdf_page_text.py` | Extrahiert Text einzelner PDF-Seiten |
| `pdf_tail.py` | Zeigt PDF-Text nach einem Suchbegriff |
| `find_page38.py` | Findet gedruckte Seite 38 in der OCR |
| `map_jpgs.py` | Ordnet die JPG-Dateien den PDF-Seiten zu |
| `crop_p51.py` | Schneidet die Scan-Seite 51 zu |
| `render_p50.py` | Rendert PDF-Seite 50 als Bild |
| `render_p51.py` | Rendert PDF-Seite 51 als Bild |
| `render_s214.py` | Rendert die Scan-Seite 214 als Bild |

---

## 7. Was das Projekt erreicht hat

### Der Bestand

- 22 Seiten im Korpus (`data/corpus.py`)
- 12 Lösungen (`data/solutions.py`) — 11 davon zu Korpus-Seiten, 1 extra (Seite `??`)
- 11 Korpus-Seiten noch offen (die README zählt 10, weil sie die `??`-Seite mitzählt)
- 14 bekannte Schlüsselwörter (`core/adfgvx.py`)
- 3 Seiten mit Anomalien
- Dazu aus dem Childs-Buch: RICHI-264 (bewiesen), RICHI-222 (Struktur bewiesen),
  RICHI-274 und RICHI-338 (verifiziert)

Eine vollständige Liste aller Sprüche mit Schlüsseln, Quadraten und
Permutationen steht in der README (`analysis/dump_keys.py` erzeugt sie).

> **Provenienz.** Der Korpus ist eine **treue Abschrift der Originalquelle**.
> 14 von 22 Seiten stimmen zeichengenau mit dem Cipherbrain-Artikel überein,
> die übrigen acht Abweichungen sind rein kosmetisch. Der Korpus ist also
> **nicht beschädigt** — er ist die (leicht bereinigte) Abschrift der Quelle.
> Details in Abschnitt 10.

> **Evidenzlage.** Von den 11 gelösten Korpus-Seiten sind nur **3** (100, 105,
> 146) gegen ein unabhängig überliefertes Chiffrat geprüft. Bei den übrigen 8
> wurde der Geheimtext aus dem Klartext rekonstruiert
> (`transpose(bigrams(pt), perm)`) — der Roundtrip ist dort per Konstruktion
> garantiert und beweist nichts. Verstärkt wird das durch unvollständige
> Quadrate (`Nov13-15a/b`, `Nov10-12`, `Nov7-9`), deren `-`-Lücken
> `make_square()` willkürlich füllt. Die externen Beweise (217,
> RICHI-264/274/338, RICHI-222) sind davon nicht betroffen.
> Details: README, Abschnitt „Evidenzlage der gelösten Seiten".

### Seite 217 (RICHI-170) — gelöst und bewiesen

Ein Artikel behauptete: „GPT-6 ASTRA SOLVES A WWI GERMAN RADIO".
Das Projekt hat die Behauptung geprüft — und bestätigt.

Das Schlüsselwort lautet `TRUPPENVERSCHIEBUNG`.
Der Klartext beginnt so:

```
EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENX
EINGESCHWADERDERXALLIIERTENFOLGT26STENX
```

**Achtung — das Schlüsselwort liefert beides.**
Der Artikel nutzt `TRUPPENVERSCHIEBUNG` für **beide Stufen**:

1. **Als Quadrat-Grundlage.** Der Artikel druckt ein 6×6-Quadrat mit
   ADFGVX-Achsen ab, das aus dem Schlüsselwort abgeleitet ist (Zeile 1:
   `T R U P E …` — die Keyword-Reihenfolge).
2. **Als Transpositionswort.** Alphabetisch sortiert ergeben die 19
   Buchstaben die Spaltenreihenfolge (das `T` hat Rang 16, das `R` Rang 13).

**Die Füllregel ist aber nicht die naive.** Füllt man nach der schematischen
Regel aus Abschnitt 2 (`make_square()`: Keyword ohne Doppel + Restalphabet),
bekommt man Unsinn — nur 29 von 85 Zeichen stimmen. Das historische Quadrat
mischt die Ziffern **einflechtend** zwischen die Keyword-Buchstaben
(Zeile 1: `T R U P E 4`, Zeile 2: `N V S C 2 H` — im Artikel-Bild sind alle
Ziffern handschriftlich nachgetragen). Die 23 aus dem Klartext belegten
Quadratzellen decken sich zu 82 von 85 Zeichen mit dieser Version. 0 Konflikte.

Genau diese feine Unterscheidung — *Keyword liefert das Quadrat, aber nicht
durch die schematische Füllregel* — war der Denkfehler des Projekts: erst
wurde die Konvention ignoriert, dann die Füllregel übertrieben.

Drei Tests laufen durch:

1. **Transposition:** Rang 16 (das `T`) beginnt beim 135. Zeichen. Dort steht ein `A`. Stimmt.
2. **Substitution:** Null Konflikte. Das Quadrat ist widerspruchsfrei.
3. **Roundtrip:** Verschlüsselt man den Klartext neu, kommt exakt der Geheimtext heraus.

**Wichtig:** Eine frühere „Widerlegung" im Projekt war ein Denkfehler.
Der Fehler lag in der Rangfolge der Permutation. Siehe Abschnitt 2.

**Zusatz 24.09.2026 — Quelle präzisiert.** Der Artikel nutzt
`TRUPPENVERSCHIEBUNG` für Quadrat **und** Transposition. Das Quadrat ist
kein schematisches `make_square()`-Produkt, sondern ein historisches
Keyword-Quadrat mit eingestreuten Ziffern (im Artikel-Bild handschriftlich
nachgetragen). Siehe oben.

### RICHI-274 und RICHI-338 — gelöst

Beide Seiten nutzen den Schlüssel `Oct28-31`.
Die Permutation ist `[6,15,12,16,5,7,14,4,13,8,11,1,17,2,10,3,18,9]`.
Die Tabellen stehen in `data/childs_additional.py`.

### RICHI-264 — aus dem Childs-Buch, gelöst und bewiesen

Der erste Funkspruch aus dem Childs-Buch, der nicht im 22-Seiten-Korpus steht.
Der Schlüssel `Nov1-3` war schon bewiesen. Der Geheimtext enthielt zwei Fehler:

1. Bigramm 63: `AD` statt `AG` — eine D/G-Verwechslung (Morse: `D = -..`, `G = --.`).
2. Nach Bigramm 64 fehlte das Bigramm `XG` — eine Löschung.

Nach beiden Reparaturen gilt der volle Beweis: Dekodierung und Re-Encryption
stimmen exakt. Der Klartext (133 Zeichen):

```
DEMNACHGEHENNUMEHRSAEMTLICHESCHIFFEVONKOSPOLINACHODESSABEZWX
NIKOLAJEWXVERTEILTWIEFRX52751XUNDXBVGXRUMXXL7CHXROEMX2XGROSSXBXFRX52787XX
```

Lesefassung: *Demnach gehen nunmehr sämtliche Schiffe von Kospoli nach Odessa
bzw. Nikolajew. Verteilt wie Fr. 52751 und B.V.G. rum. L7 Ch. Röm. 2. Groß B.
Fr. 52787.* — Ein Marine-Funkspruch vom 1. November 1918.

Reproduzierbar: `python3 analysis/verify_richi_264.py`

### RICHI-222 — Struktur bewiesen, Lücken offen

Der 13. Teil einer 13-teiligen Nachricht (Konstantinopel nach Berlin, 3.11.1918).
Der Schlüssel `Nov1-3` bestätigt sich zum dritten Mal — die Spaltenköpfe der
Tabelle sind exakt die bewiesene Permutation.

Der Geheimtext ist schwer beschädigt: 79 Empfangslücken, dazu fehlt das Ende.
Von 114 Bigrammen sind nur 37 vollständig. Der Beweis gilt für die Struktur:
Re-Encryption deckt alle 144 überlieferten CT-Zeichen exakt.

Der Klartext selbst ist an den Lücken **nicht eindeutig bestimmt**. Der beste
Kandidat (Beam-Search mit dem Sprachmodell, 64 Worttreffer):

```
TECHENDERXGESARMEEDENMERSCHDURMEINGARNAUFESERSCHLESIENANZIT
UNTENSEINDERSTENNDWISSERDETERESEXKTERRMTLTAA1GRISISCASS
```

Childs hat die Lücken per Elimination gefüllt (Buch S. 43). Das Handbuch
trennt beides: Struktur = bewiesen. Füllung = Kandidat.

Reproduzierbar: `python3 analysis/richi_222_reconstruct.py`

### RICHI-240 — verifiziert, nicht selbst gelöst

Von 240 Zeichen fehlen 20.
Die Ziffern 7, 9 und 6 stammen aus einem französischen Telegramm.

**Wichtig:** RICHI-240 wurde **nicht von diesem Projekt** gelöst.
Der Artikel von Astra (prinzai.com) hat es getan.
Dieses Projekt hat die Behauptung **geprüft** — und bestätigt.
Das ist ein Unterschied. Gelöst heißt: selbst gerechnet. Verifiziert heißt: nachgerechnet.

---

## 8. Die Sackgassen — und was sie gelehrt haben

Ein ehrliches Handbuch verschweigt die Irrwege nicht.
Dieses Projekt hat viele davon dokumentiert.

| Sackgasse | Lehre |
|---|---|
| Trigramm-Modell als Hauptkriterium | Schadet bei historischem Militärtext |
| Nur `word_hits` als Fitness | Erzeugt Plateaus, die Suche bleibt stehen |
| Greedy-Alignment | Fehlerhaft. Editierdistanz benutzen |
| Blinde Suche nach Quadrat und Permutation | Löst das falsche Problem — die Schlüssel sind meist bekannt |
| Anomalie-Reparatur | War ein Artefakt. Gelöste Seiten zeigen größere Abweichungen |
| Seite 170 als „einziger Astra-Kandidat" | Falsch. Nur 106 statt 240 Zeichen |
| „Der Korpus ist beschädigt" | Falsch. Er ist eine treue Abschrift der Quelle (14/22 zeichengenau) |
| „Eine neue Quelle würde die offenen Seiten lösen" | Falsch. Die Originalquelle liefert dieselbe Transkription |

Die wichtigste Lehre steht schon in Abschnitt 4:
**Erst die Daten, dann die Krypto.**

---

## 9. Wie man den Code benutzt

Alle Skripte sind Python 3.
Man startet sie aus dem Projektverzeichnis.

```bash
cd adfgvx

# Chiffre testen
python3 -c "import bootstrap; from core.adfgvx import *; print(KEYS.keys())"

# Seite 217 verifizieren
python3 analysis/verify_article_claim.py

# Alle gelösten Seiten prüfen
python3 analysis/verify_solutions.py

# Konfliktzahl als Kriterium belegen
python3 analysis/rank_conflicts.py

# Tests laufen lassen
python3 tests/testcases.py
python3 tests/test_171.py
python3 tests/test_fitness.py
python3 tests/test_provenance.py
```

`bootstrap.py` setzt den Projektpfad auf `sys.path`.
Man muss es nur einmal importieren.

Es gibt keine externen Abhängigkeiten. Nur die Standardbibliothek.

### Lange Läufe im Hintergrund

Manche Löser rechnen Stunden.
Wenn man sie in einem normalen Terminal startet, sterben sie, sobald die
SSH-Verbindung abbricht — etwa wenn der Arbeitsplatz-PC in Standby geht.
Der Prozess bekommt dann ein `SIGHUP` und wird beendet.

Dafür gibt es `run_detached.sh`.
Es startet ein Skript in einer **tmux**-Session.
Die läuft unabhängig von SSH und VS Code weiter.

```bash
# Solver im Hintergrund starten
./run_detached.sh analysis/solve_152_fast.py --name s152

# Live mitlesen
./run_detached.sh --log s152

# In die Session springen (Strg+B, dann D zum Lösen)
./run_detached.sh --attach s152

# Laufende Sessions anzeigen
./run_detached.sh --list

# Beenden
./run_detached.sh --stop s152
```

Die Ausgabe landet zusätzlich in `logs/<name>.log`.
Man kann VS Code schließen und den PC in Standby schicken — der Lauf geht weiter.

**Warum das funktioniert.** Der Prozess hängt dann nicht mehr am
SSH-Terminal, sondern am tmux-Server. Dessen Elternprozess ist `init` (PID 1).
Ein Verbindungsabbruch erreicht ihn nicht mehr.

**Wichtig:** Das schützt nur gegen den Abbruch der *Verbindung*.
Wenn der **Analyse-Rechner selbst** in Standby geht, schläft die CPU — dann
rechnet nichts mehr. Für einen headless Server schaltet man den Standby ab
(`sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`).

### Das Projekt auf GitHub

Das Projekt liegt als Open Source bereit:

**https://github.com/kajoty/adfgvx-reconstruction**

- **README.md** — der kompakte Einstieg. Oben: Worum geht es, Stand, Loslegen. Unten: das Arbeitsprotokoll mit allen Befunden.
- **LICENSE** — MIT. Der Code darf frei genutzt werden.
- Die historischen Quellen in `docs/` unterliegen eigenen Rechten. Sie werden zu Forschungszwecken zitiert.

Wer einen Fehler findet oder eine Seite löst: Ein Issue auf GitHub genügt.

---

## 10. Die Quellen

Das Projekt stützt sich auf historisches Material.
Die Dateien liegen in `docs/`.

### Friedmans Lehrbuch

William F. Friedman: *Military Cryptanalysis, Part IV*.
Das PDF liegt als `docs/41761079080022.pdf`.
Der relevante Abschnitt ist als Text in `docs/friedman_section_IX.txt` gespeichert.

### Die Schlüsselliste

Die bekannten ADFGVX-Schlüssel stammen aus einer Liste von Lasry.
Sie liegt als `docs/adfgvx_keys.pdf`.

### Die Quadrate

Die Quadrate stehen als Tabelle in den Quellen — nicht als Schlüsselwort.
Ein Beispiel: das Quadrat für den 1.–3. November.
Es steht in `docs/childs_book.pdf` auf der gedruckten Seite 44 (PDF-Seite 52).
Dort heißt es schlicht „ADFGVX KEY FOR NOVEMBER 1, 2, AND 3".

```
     A  D  F  G  V  X
A    U  I  L  O  F  9
D    R  C  Z  V  S  X
F    0  2  G  7  Q  T
G    D  8  W  N  B  5
V    J  M  H  E  K  P
X    Y  4  1  A  3  6
```

Kein Schlüsselwort, keine Auffüllregel.
Die 36 Zeichen sind frei gemischt.
Genau so steht es auch in `core/adfgvx.py` unter `Nov1-3`.

Das ist ein Einzelfall, kein Beweis.
Friedman zeigt an anderen Stellen Quadrate, die sehr wohl aus einem Schlüsselwort stammen.
Wer wissen will, wie das geht, liest Abschnitt 2.

**Ein Hinweis zur Quelle.** Der Scan ist alt und die automatische Texterkennung
verwechselt `O` und `0` leicht. Im Quadrat für den 1.–3. November steht in der
ersten Zeile ein `O` (Buchstabe), in der dritten Zeile eine `0` (Ziffer).
Wer die Tabelle aus dem PDF ausliest, muss das prüfen — sonst wird aus
`STOERUNG` schnell `ST0ERUNG`.

### Das Childs-Buch

Ein Buch mit abgedruckten Funksprüchen.
Es liegt als PDF (`docs/childs_book.pdf`) und als OCR-Text (`docs/childs_djvu.txt`) vor.

Die einzelnen Seiten sind als Bilder gescannt.
Sie liegen in `docs/childs_pages/` — 63 JPG-Dateien von `page_00.jpg` bis `page_62.jpg`.

**Achtung, zwei verschiedene Zählungen.**
Die JPG-Dateien sind nach PDF-Seiten nummeriert, nicht nach gedruckten Seitenzahlen.
Es gilt: `page_NN.jpg` = PDF-Seite `NN + 1`.
Die gedruckte Seitenzahl im Buch liegt um 8 niedriger als die PDF-Seite.
Der Grund ist das Vorwort: acht Seiten vornweg.

| Nachricht | gedruckte Seite | PDF-Seite | Bilddatei |
|---|---|---|---|
| RICHI 266 | 36 | 44 | `page_43.jpg` |
| RICHI 338 | 32 | 40 | `page_39.jpg` |

**RICHI 266** (gedruckte Seite 36, PDF-Seite 44):

![Childs, RICHI 266, PDF-Seite 44](childs_pages/page_43.jpg)

**RICHI 338** (gedruckte Seite 32, PDF-Seite 40):

![Childs, RICHI 338, PDF-Seite 40](childs_pages/page_39.jpg)

Die zugehörigen Transkriptionen stehen in `docs/childs_pages/266.md` und `docs/childs_pages/338.md`.

Ein Prüfbericht über die Scans liegt in `docs/childs_scan_report.txt`.

### Der Kommentar-Entwurf

Ein Entwurf für einen Kommentar auf Cipherbrain liegt in `docs/cipherbrain_kommentar_entwurf.md`.

### Der Cipherbrain-Artikel (Originalquelle)

Der Artikel, aus dem die 22 Funksprüche stammen, ist selbst eine Quelle —
und zwar eine bessere, als lange angenommen.

Klaus Schmeh: *Unsolved ADFXVX messages from World War I*, Cipherbrain,
23.02.2017 (Sammlung von George Lasry):
`scienceblogs.de/klausis-krypto-kolumne/unsolved-adfxvx-messages-from-world-war-i/`

Der Artikel enthält die Geheimtexte **nicht nur als Bild**, sondern als
**Klartext-Transkription im HTML**. Das Rohmaterial liegt unter
`docs/cipherbrain_pages/`:

| Datei | Inhalt |
|---|---|
| `article.html` | Original-HTML der Seite |
| `article_body.txt` | extrahierter Artikeltext mit Bildmarkern |
| `cryptogram-01..19.png` | die 19 Original-Geheimtext-Bilder |

Die Transkription ist als `data/article_transcription.py` (`ARTICLE_CT`)
verfügbar. `analysis/parse_cipherbrain.py` extrahiert sie aus dem HTML,
`analysis/verify_corpus_provenance.py` vergleicht sie mit dem Korpus.

**Befund: `corpus.py` ist eine treue Abschrift der Originalquelle.**
14 von 22 Seiten stimmen zeichengenau (100,0 %) überein. Die übrigen acht
Abweichungen sind rein kosmetisch — zusätzliche `-` (unleserliche Zeichen)
oder bereits angewandte Kommentar-Korrekturen (Seite 100: die `DG`-Einfügung
aus Armin #13). Der Korpus ist also **keine beschädigte Transkription**,
sondern die (leicht bereinigte) Abschrift der Quelle. Der Test
`tests/test_provenance.py` prüft das.

**Was das nicht löst.** Die Originalquelle liefert nur *dieselbe*
Transkription, die der Korpus bereits enthält. Für die 9 synthetischen
Seiten fehlt weiterhin ein *unabhängiger* Beleg. Der Engpass verschiebt sich
damit von „Quelle unbekannt" zu „Quelle bekannt, aber nur einfach belegt".

---

## 11. Die Regeln dieses Handbuchs

Dieses Handbuch folgt Wolf Schneider.
Was heißt das konkret?

- **Kurze Sätze.** Ein Gedanke pro Satz.
- **Aktiv statt Passiv.** „Das Projekt prüft" statt „Es wird geprüft".
- **Konkrete Verben.** „messen", „zählen", „reparieren" — nicht „vornehmen", „durchführen".
- **Kein Nominalstil.** „Wir prüfen" statt „Die Durchführung der Prüfung".
- **Keine Füllwörter.** Kein „eigentlich", „gewissermaßen", „sozusagen".
- **Klare Wörter.** Kein Fachjargon ohne Erklärung.
- **Ein Bild pro Abschnitt.** Wo es hilft, nicht wo es schmückt.

Wer das befolgt, schreibt verständlich.
Und darum geht es hier: Ein Außenstehender soll verstehen, was passiert.

---

## 12. Kurzfassung

1. ADFGVX ist eine Chiffre in zwei Stufen: Quadrat, dann Transposition.
2. Das Projekt entziffert alte deutsche Funksprüche.
3. Das größte Problem sind Lesefehler, nicht die Krypto.
4. Die Konfliktzahl ist ein exakter Beweis — aber nur gegen ein unabhängig überliefertes Chiffrat.
5. 11 von 22 Korpus-Seiten sind gelöst, dazu 4 aus dem Childs-Buch. Nur 3 der 11 sind unabhängig belegt.
6. Seite 217 ist mit `TRUPPENVERSCHIEBUNG` bewiesen.
7. Der Korpus ist eine treue Abschrift der Originalquelle (14 von 22 Seiten zeichengenau).
8. Erst die Daten reparieren, dann entschlüsseln.
