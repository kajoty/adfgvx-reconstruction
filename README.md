# ADFGVX — 22 Kryptogramme aus dem Ersten Weltkrieg, 11 davon ungelöst

Werkzeuge und Befunde zur Kryptanalyse der ADFGVX-Funksprüche, die Klaus Schmeh
2017 in seiner Cipherbrain-Kolumne veröffentlicht hat.

---

# 1. WHY — Warum dieses Projekt?

## Die Ausgangslage

Im Frühjahr 1918 führte die deutsche Armee ADFGVX ein: ein
Fractionating-Cipher-Verfahren, das Substitution und Transposition kombiniert.
Die Franzosen unter Georges Painvin brachen es im Juni 1918 — unter enormem
Zeitdruck und mit Papier und Bleistift.

Hundert Jahre später liegen 22 abgefangene Sprüche vor, für die **alle
verwendeten Schlüssel bekannt sind** — und trotzdem sind 11 davon bis heute
nicht lesbar.

## Die eigentliche Frage

Wenn die Schlüssel bekannt sind, warum sind die Nachrichten dann nicht lesbar?

Die Antwort ist unbequem: **Das Problem ist nicht die Kryptographie, sondern die
Datenqualität.** Die Sprüche wurden 1918 unter Funkbedingungen empfangen —
Störungen, Aussetzer, Übertragungsfehler. Was heute als „Geheimtext" vorliegt,
ist an vielen Stellen beschädigt.

> **Kernaussage:** Der Engpass ist die Quelle, nicht der Algorithmus.

Diese Erkenntnis bestimmt den ganzen Aufbau des Projekts. Es ist kein
Solver-Wettbewerb, sondern eine Beweissammlung: *Was wissen wir wirklich, und
wie sicher wissen wir es?*

## Was dieses Projekt beiträgt

1. **Eine ehrliche Evidenzlage.** Für jede der 11 gelösten Korpus-Seiten steht
   explizit dabei, ob sie unabhängig belegt oder nur rekonstruiert ist.
2. **Werkzeuge, die terminieren.** Alle Solver laufen mit Zeitbudget und
   Konvergenzabbruch durch — keine Endlosschleifen.
3. **Externe Validierung.** Die Lösung für `Nov1-3` wurde an einer Nachricht
   außerhalb des Korpus bewiesen (RICHI-264 aus dem Childs-Buch).
4. **Widerlegte Sackgassen.** Neun blinde Suchkriterien wurden getestet und
   verworfen — dokumentiert, damit sie niemand erneut versucht.

---

# 2. WHAT — Was ist das Problem?

## Das Verfahren

ADFGVX arbeitet in zwei Schritten.

**Schritt 1 — Substitution.** Ein 6×6-Quadrat wird mit den 26 Buchstaben und
10 Ziffern gefüllt. Jedes Klartextzeichen wird durch das Buchstabenpaar
(Row, Column) ersetzt, wobei die Reihen und Spalten mit `A D F G V X`
beschriftet sind — daher der Name.

```
      A  D  F  G  V  X
  A   U  I  L  O  F  9
  D   R  C  Z  V  S  X
  F   0  2  G  7  Q  T
  G   D  8  W  N  B  5
  V   J  M  H  E  K  P
  X   Y  4  1  A  3  6
```

`E` liegt in Zeile `V`, Spalte `G` → Bigramm `VG`.

**Schritt 2 — Transposition.** Die Bigramme werden zeilenweise in ein Raster
geschrieben und spaltenweise in einer durch ein Kennwort bestimmten Reihenfolge
ausgelesen.

## Die kritische Konvention

Die Permutation ist eine **Rangordnung**, keine Lesereihenfolge:

```python
perm[c]  # alphabetischer Rang der Spalte c
order = sorted(range(n), key=lambda c: perm[c])   # Auslesereihenfolge
```

Die naive Deutung als direkte Lesereihenfolge liefert ausschließlich
Kauderwelsch. Das war der erste Knackpunkt des Projekts.

## Der Datenbestand

| | Anzahl | Beschreibung |
|---|---|---|
| Korpus-Seiten | 22 | `data/corpus.py`, transkribiert aus dem Cipherbrain-Artikel |
| Gelöste Korpus-Seiten | 11 | Klartext bekannt, Quelle dokumentiert |
| Ungelöste Korpus-Seiten | 11 | Schlüssel bekannt, Text nicht lesbar |
| Lösungen gesamt | 12 | `data/solutions.py` — 11 Korpus-Seiten + 1 spruchfremde Seite (`??`) |
| Schlüssel | 14 | `core/adfgvx.py`, Zeiträume Sep 1918 – Dez 1918 |

Die 14 Schlüssel decken den Zeitraum 19.09.1918 bis 01.12.1918 ab. Jeder
Schlüssel besteht aus einer Permutation (Länge 16–23) und einem
Substitutionsquadrat (36 Zeichen, teils mit Lücken).

## Die Schwierigkeit

**Warum scheitert die blinde Suche?**

Die Fitness-Landschaft ist ein Nadel-im-Heuhaufen-Problem. Permutation und
Quadrat müssen *gleichzeitig* nahezu perfekt sein, sonst gibt es kein
Gradientensignal:

| Konfiguration | Ergebnis |
|---|---|
| Echte Perm + Zufallsquadrat | Rauschen |
| Hill-Climbing Perm, Quadrat bekannt | scheitert |
| Hill-Climbing Quadrat, Perm bekannt | fast, aber nicht ganz |
| Echte Perm + echtes Quadrat | perfektes lokales Optimum |

Zusätzlich ist die Bigramm-Verteilung des Zwischentexts **invariant** unter
Spaltenpermutationen. Kein quadratunabhängiges Kriterium kann die Permutation
eindeutig bestimmen — es existiert eine Äquivalenzklasse von Permutationen mit
identischer Bigramm-Verteilung.

## Der Stand

| Kategorie | Anzahl | Beweiskraft |
|---|---|---|
| Unabhängig belegt | 3 | echte Transkription + Roundtrip (100, 105, 146) |
| Synthetisch rekonstruiert | 9 | Klartext aus Kommentar, Geheimtext synthetisch |
| Extern bewiesen (außerhalb des Korpus) | 1 | Seite 217 / RICHI-170, 0 Konflikte |

Die 3 unabhängig belegten und die 9 synthetisch rekonstruierten Seiten
ergeben zusammen die **12 Lösungen** aus `data/solutions.py` — davon 11
Korpus-Seiten und die spruchfremde `??`-Seite. Die extern bewiesene Seite 217
gehört nicht zum Korpus und ist hier separat aufgeführt.

**Wichtig:** Bei den 9 rekonstruierten Seiten ist der Roundtrip *per
Konstruktion* garantiert — er beweist nichts über Klartext oder Quadrat. Diese
Seiten sind als „rekonstruiert" gekennzeichnet, nicht als „bewiesen".

---

# 3. HOW — Wie funktioniert es?

## Projektstruktur

```
bootstrap.py            Projektwurzel auf sys.path (selbst-lokalisierend)
core/
  adfgvx.py             Kernbibliothek: encrypt, decrypt, KEYS
  langmodel.py          Deutsches Sprachmodell (Trigramme + Wortliste)
  fitness.py            Gewichtete Fitness (Score + Worttreffer)
  fastfitness.py        Inkrementelle Bewertung (delta_swap)
data/
  corpus.py             CORPUS — 22 Seiten, unreine Transkription
  corpus_corrected.py   CORRECTED / RECONSTRUCTED / UNVERIFIED
  solutions.py          SOLVED — 12 Klartexte mit Quelle
  childs_additional.py  Nachrichten aus dem Childs-Buch
  de_50k.txt            Worthäufigkeitsliste
  texte.txt             Cipherbrain-Kommentarthread (56 Kommentare)
solvers/
  base.py               Budget, SolverResult, build_parser, run_cli
  blind_solver.py       Simulated Annealing über Perm + Quadrat
  analytic_solver.py    Innerer Quadrat-Solver + äußerer Perm-Loop
  guided_solver.py      Coverage-geführte Quadrat-Suche
  conflict_solver.py    Fehlerrekonstruktion bei bekanntem Schlüssel
  friedman_solver.py    Friedman-Ansatz (IoC, MI)
  sub_solver.py         Reine Substitutionslösung
  alternating_solver.py Abwechselnd Perm und Quadrat optimieren
  reverse_square.py     Quadrat aus Klartext rekonstruieren
analysis/               48 Diagnose- und Verifikationsskripte
tests/                  5 Testdateien
docs/                   HANDBUCH.md, Quellen-PDFs, Transkriptionen
  FAHRPLAN_ENTSCHLUESSELUNG.md   alle 28 Kryptogramme in einer Datei
  fahrplan/                      dieselben 28 als Einzelseiten (MD + HTML) + Index
```

## Import-Konvention

Skripte in Unterordnern beginnen mit:

```python
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()
```

Danach `from core.adfgvx import ...`, `from data.corpus import ...` usw.

## Loslegen

```bash
cd /home/user/Projekte/adfgvx

# Testfälle prüfen (12/12 Roundtrip)
PYTHONPATH=. python3 tests/testcases.py

# Provenienz der Korpus-Daten prüfen
PYTHONPATH=. python3 tests/test_provenance.py

# Konfliktzahl aller gelösten Seiten validieren
PYTHONPATH=. python3 analysis/rank_conflicts.py --validate

# Ungelöste Seiten nach Reparierbarkeit ordnen
PYTHONPATH=. python3 analysis/rank_conflicts.py --unsolved
```

## Die Solver

Alle Solver außer `conflict_solver` nutzen die gemeinsame CLI:

```bash
PYTHONPATH=. python3 solvers/blind_solver.py --page 171 --seconds 60
PYTHONPATH=. python3 solvers/analytic_solver.py --page 171 --quick
```

| Option | Bedeutung |
|---|---|
| `--page` | Korpus-Seite (z. B. `105`, `171`) |
| `--n` | Spaltenzahl (0 = aus dem Schlüssel ableiten) |
| `--seconds` | Zeitbudget (Standard 60) |
| `--restarts` | Anzahl Neustarts |
| `--seed` | Zufallsseed |
| `--quick` | Kurzer Lauf (10 s) |
| `--verbose` | Zwischenstände ausgeben |

`conflict_solver.py` hat eine eigene CLI:

```bash
PYTHONPATH=. python3 solvers/conflict_solver.py --test
PYTHONPATH=. python3 solvers/conflict_solver.py --page 152 --key Nov4-6
```

## Die Methode

Der Fahrplan folgt der Logik der Fehlerrekonstruktion, nicht der blinden Suche.

**Stufe 0 — Problemklassifikation.** Ist der Schlüssel bekannt? Wenn ja, ist es
kein Kryptanalyse-Problem, sondern ein Datenproblem.

**Stufe 1 — Konfliktzahl.** Bei bekanntem Schlüssel: Wie viele Bigramme bilden
auf mehrere Klartextzeichen ab? **0 Konflikte = fertig.** Das ist das exakte
Kriterium — validiert an 11/11 gelösten Seiten (34–107 Konflikte vor der
Korrektur, 0 danach).

**Stufe 2 — Fehlerlokalisierung.** Edit-Distance-Alignment zwischen
Soll-Geheimtext und Ist-Geheimtext. Achtung: Greedy-Alignment ist defekt
(erkennt nur Einfügungen, keine Löschungen) — immer Levenshtein mit
Backtracking verwenden.

**Stufe 3 — Lückensuche.** Fehlende Zeichen per Sprachmuster-Scoring
ergänzen — immer gegen eine Zufalls-Baseline derselben Länge.

**Stufe 4 — Externe Verifikation.** Lücken mit historischem Wissen schließen
(z. B. Ziffern aus einem französischen Telegramm).

**Stufe 5 — Roundtrip-Beweis.** `decrypt(ct, perm, square) == klartext` und
Re-Encryption ergibt exakt den Originalgeheimtext.

## Die Fitness

```python
fitness(text, lam=1.0) = (score(text) - REF_SCORE) + lam * word_hits(text)
```

`REF_SCORE = -17.0` ist der empirisch gemessene Score eines echten deutschen
Militärtextes. Die Normierung verschiebt beide Terme in dieselbe
Größenordnung.

Die Fitness wächst mit der Textlänge, weil `word_hits` mitzählt. Gemessene
Werte (echte Klartexte aus `data/solutions.py`, Zufallstext über je 200 Läufe):

| Text | Länge | Fitness |
|---|---|---|
| Seite 100 | 62 Zeichen | 35 |
| Seite 105 | 143 Zeichen | 37 |
| Seite 146 | 122 Zeichen | 84 |
| Seite 171 | 157 Zeichen | 123 |
| Zufallstext | 62 Zeichen | −7 |
| Zufallstext | 122 Zeichen | −3 |
| Zufallstext | 314 Zeichen | +11 |

Die absoluten Zahlen sind also nur bei gleicher Länge vergleichbar. Bei
kurzen Texten trennt die Fitness echten Text (≈35) klar von Rauschen (≈−7);
bei langen Texten verschiebt sich beides nach oben (Seite 171: 123 gegen
Zufall 314 Zeichen: 11).

**Warum beide Terme?** Nur `score` führt zu Overfitting — der Solver verbiegt
Permutation und Quadrat so, dass sie das Sprachmodell täuschen. Nur
`word_hits` führt zu Plateaus — viele verschiedene Texte haben dieselbe
Trefferzahl. Die Kombination liefert den glatten Gradienten *und* den ehrlichen
Beleg.

## Nachrichtenverzeichnis erzeugen

```bash
PYTHONPATH=. python3 analysis/dump_messages.py --insert
```

Schreibt einen Block mit allen 28 Nachrichten (Geheimtext, Klartext, Schlüssel,
Permutation, Quadrat, 6×6-Raster) zwischen die Marker
``, direkt vor
den Abschnitt `## Quellen`. Der Aufruf ist idempotent — mehrfaches Ausführen
ändert nichts.

## Fahrplan erzeugen

```bash
python3 analysis/dump_fahrplan.py --write   # docs/FAHRPLAN_ENTSCHLUESSELUNG.md
python3 analysis/dump_fahrplan.py --pages   # docs/fahrplan/*.md + Index
python3 analysis/dump_fahrplan.py --html    # docs/fahrplan/*.html + index.html
python3 analysis/verify_fahrplan.py         # prüft alle Roundtrips
```

Der Fahrplan stellt **jedes** der 28 Kryptogramme einzeln dar, mit sechs
Abschnitten: (1) verschlüsselte Nachricht, (2) Schlüssel, (3) Permutation
(Rangfolge + Leseordnung), (4) Quadrat als 6×6-Raster, (5) Entschlüsselungsweg
Schritt für Schritt mit echten Zwischenwerten, (6) entschlüsselte Nachricht.

`--write` erzeugt die Sammeldatei, `--pages` eine eigene Markdown-Seite pro
Kryptogramm unter `docs/fahrplan/` samt Index (`docs/fahrplan/README.md`) und
Navigation vor/zurück. `--html` erzeugt dieselben 28 Seiten als eigenständige
HTML-Dateien mit dunklem Theme, Status-Badges, farbigem 6×6-Raster,
Permutations-Kacheln und Index (`docs/fahrplan/index.html`) — einfach im
Browser öffnen, keine Abhängigkeiten.

`verify_fahrplan.py` bestätigt `decrypt(ct, perm, square) == pt` für 13
Kryptogramme; 3 Abweichungen (RICHI-264, RICHI-222, RICHI-338) sind
dokumentiert, RICHI-240 hat keinen Geheimtext im Repo.

---

# 4. WHAT IF — Was wäre wenn?

## Wenn die Daten sauber wären

Dann wären die 11 ungelösten Seiten in Minuten gelöst. Die Schlüssel liegen
vollständig vor. Der `conflict_solver` braucht nur einen fehlerfreien
Geheimtext — dann liefert er 0 Konflikte und den Klartext.

**Der Engpass ist die Transkription.** Die Korpus-Daten stammen aus einer
Nutzer-Transkription des Cipherbrain-Artikels, mit dokumentierten
Leseunsicherheiten (`-` = unleserlich, `v` = unsicher). Es gibt keine
maschinenlesbare Quelle im Repo, gegen die man sie prüfen könnte.

**Konsequenz:** OCR-Reparatur ist der falsche Ansatz. Wer die Originalbilder
lesen kann, tippt die Daten direkt korrekt ein — das ist schneller und
zuverlässiger als jede algorithmische Rekonstruktion.

## Wenn die Quadrate vollständig wären

Fünf genutzte Schlüssel haben Lücken im Substitutionsquadrat:

| Schlüssel | Lücken | Betroffene Seiten |
|---|---|---|
| Nov13-15a | 12 | 153a |
| Nov16-18 | 8 | 176b (ungelöst) |
| Nov13-15b | 7 | 187 |
| Nov10-12 | 5 | 176a |
| Nov7-9 | 2 | 171, 164a, 164b |

`make_square()` füllt diese Lücken mit dem Restalphabet — eine willkürliche
Annahme. Bei Nov13-15a werden 2 der 12 gefüllten Zellen vom Klartext benutzt
(`0`, `1`), bei Nov13-15b 2 von 8 (`4`, `9`). Solange die Lücken nicht
aufgelöst sind, bleiben diese Quadrate Annahmen.

## Wenn es eine fundamentale Symmetrie gibt

Die Bigramm-Verteilung des Zwischentexts ist unter Spaltenpermutationen
invariant. Das ist kein Implementierungsdetail, sondern eine Eigenschaft des
Verfahrens:

- Die echte Permutation hat eine **erhöhte** Bigramm-Konzentration, aber
  keinen Spitzenplatz: gemessen über 20 000 Zufallspermutationen je Seite
  liegt sie zwischen Rang 917 (Seite 171) und Rang 17 702 (Seite 146) von
  20 001. Das Signal ist also real, aber schwach und längst nicht eindeutig.
- Aber: Die Verteilung ist **kein** eindeutiges Kriterium. Von 200 000
  getesteten Zufallspermutationen (Seite 171) erzeugte keine einzige exakt
  dieselbe Bigramm-Verteilung wie die echte — und auch kein einziger der
  190 Nachbar-Swaps der echten Permutation liefert dieselbe
  Segment-Sequenz. Das Signal ist also scharf, aber die Suche darüber
  konvergiert nicht auf die Lösung.
- Grund: Verschiedene Auslesereihenfolgen können dieselbe
  Segment-Sequenz erzeugen, ordnen sie aber anderen logischen Spalten zu.

**Konsequenz:** Kein quadratunabhängiges Kriterium kann die Permutation
eindeutig bestimmen. Die Suche muss Permutation und Quadrat gemeinsam
bewerten.

## Was widerlegt wurde

Neun blinde Suchkriterien wurden getestet und verworfen:

| Kriterium | Befund |
|---|---|
| Zell-Reinheit | korreliert **negativ** mit der Lösung |
| Zellenzahl | richtig nur in 5/10 Fällen |
| Adjazenz | kein Signal |
| Bigramm-Chi² | kein Signal |
| Known-Bigramm | kein Signal |
| Referenz-CT-Vergleich | kein Signal |
| Bigramm-Strom | kein Signal |
| Konsens-Test | funktioniert nur bei sauberem CT |
| Hill-Climbing auf Spaltenreihenfolge | Artefakt — findet nur, was schon da ist |

**Wichtig:** `word_hits` allein ist kein Erfolgsindikator. Auf Zufallstext
derselben Länge (104 Zeichen) schwankt die Trefferzahl zwischen 1 und 17
(Mittel 7,5 über 200 Läufe) — echte kurze Seiten liegen mit 39 Treffern
(Seite 100) zwar deutlich darüber, aber ohne gemessene Zufalls-Baseline sagt
eine einzelne Trefferzahl nichts.

## Was wirklich hart bewiesen ist

| Befund | Beweis |
|---|---|
| Seite 217 / RICHI-170 | TRUPPENVERSCHIEBUNG, 0 Konflikte, Roundtrip gegen echtes CT |
| RICHI-264 | 2 Reparaturen, Re-Encryption == OCR-CT |
| RICHI-274 | Oct28-31 an echtem Klartext validiert, Roundtrip OK |
| RICHI-338 | Oct28-31 an Klartext validiert, aber **nicht** roundtrip-verifiziert (22 CT-Fehler) |
| Seiten 100, 105, 146 | echte Transkription + vollständiger Roundtrip |
| Transposition | 100 % Zeichentreffer auf 12/12 Seiten (mit korrigiertem CT) |

## Der Ausblick

Die Kryptanalyse ist erschöpft. Die nächsten Schritte sind Datenarbeit:

1. **Unabhängige Transkriptionen** für die 9 rekonstruierten Seiten
   beschaffen — der eigentliche Engpass.
2. **Quadrat-Lücken** in Nov13-15a/b, Nov16-18, Nov10-12, Nov7-9 auflösen.
3. **Erst dann** die Seiten mit 0 Lücken (152, 170, 176b, 187b, 198) mit dem
   `conflict_solver` angreifen.

## Wenn man es trotzdem blind versuchen will

Der `blind_solver` ist der ehrliche Test: Er bekommt nur den Geheimtext und die
Spaltenzahl. Er scheitert — auch auf einem *perfekten* synthetischen Testfall
mit bekanntem Klartext. Das ist kein Implementierungsfehler, sondern die
Aussage des Projekts: **Die Landschaft erlaubt keine blinde Suche.**

---

<!-- GENERATED: dump_messages.py -->
# Nachrichtenverzeichnis

Jede Nachricht einzeln: Geheimtext, Klartext, Schlüssel, Quadrat und
Permutation. Generiert aus dem Code (`analysis/dump_messages.py`).

## Gelöste Korpus-Seiten

Für jede Seite: der Geheimtext, mit dem sie tatsächlich entschlüsselt wurde (korrigiert bzw. rekonstruiert), der Klartext, und der vollständige Schlüssel.

### Korpus Seite 100

**Status:** gelöst, **bewiesen** — Geheimtext aus unabhängiger Transkription, Roundtrip exakt, 0 Konflikte

**Schlüssel:** `Nov1-3`

**Geheimtext** (124 Zeichen, 62 Bigramme):

```
VDDADAADFGVVVAVGDAFVAAFGVDDVXFDFGGAAGXAAGGVADXGAXVXAXGAXAGAX
DDGDGVFFAXGDFGFDVGFAADVVGVXGDVGGDDADAVAGFXDFVADVDGDGFGDDFGDA
VGAA
```

**Klartext** (62 Zeichen):

```
KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRA
DX
```

*Quelle des Klartexts: Armin #13 / Norbert #40.*

**Schlüssel `Nov1-3`** — n = 19, Quadrat-Lücken: 0, laut Lasry-Liste 100× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
3-16-4-15-7-12-18-6-17-8-19-1-13-10-2-14-11-9-5
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 105

**Status:** gelöst, **bewiesen** — Geheimtext aus unabhängiger Transkription, Roundtrip exakt, 0 Konflikte

**Schlüssel:** `Nov1-3`

**Geheimtext** (287 Zeichen, 143 Bigramme):

```
GAGVAAXADFXVAXVXGVDAXDGAFADFFGFXXXVDAGDXDXDXXVVGGAVDAGGGFDGG
AFXDXAGAAFFDGDXGDVDVGGAFXDXAFAVDXFVVXDDFFXDADDGVGDGDXVXXGDGD
DGFFFGVADVXDVXFXDGXAADDVXXGVDAXXVAXDXGFDDVVFVDAVXADDGFAFDGAV
XAGVDGAFFDDDGAGAGDGFDFXFDXGGFDDGVGAFAXFGAVDGGVFXGDGDFDXVXXAX
GDXGGGVGDXGXXGVDFVXAAVGDXDXDGADXGVAADFXGGVDGGAX
```

**Klartext** (143 Zeichen):

```
GERMANIAATAPPEKONSTANTINOPELXRFUERMITTEHMEERDIVIC9VNZUXTEL9V
RX62XDOV2TTELEGRXN0X58XISTELTX32141XQ4XAXVOMX4CNOVEMBERNULED
IGTXA8MIRALSTAFX32398XB
```

*Quelle des Klartexts: Norbert #15 / Max Baertl #39.*

**Schlüssel `Nov1-3`** — n = 19, Quadrat-Lücken: 0, laut Lasry-Liste 100× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
3-16-4-15-7-12-18-6-17-8-19-1-13-10-2-14-11-9-5
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 109

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov1-3`

**Geheimtext** (250 Zeichen, 125 Bigramme):

```
XAAVFXAXGDVGGGGGXGFDAFGADVAGDAVGFDVGDGVFDAXFDGVGXAAGDFGXDXVD
ADXXVVXXADFGFGVVVVAGVDDGFAGXAGGADDGXADDVVVXXAVGDAFGAGDADGDXG
GDFGGADFDGAXVFVFVGGVDDGVGVVGGXVAAADGVXXAVGVFAGAGVGDVFVDVVXDF
FDDVXVDXGAGGDVGGXGGVFGDXDFGVVGXVFDFAXADGVFDDDGXDDGVDAADDXDAA
FAXGDVGVFA
```

**Klartext** (125 Zeichen):

```
OXKXMXABENDMELDUNGXS4V4XUMBJRGA8GLETZTEVTVILEBEEVUETX1WEITED
EFDUXNIV5IMMARSCH4UFBELGRADERKAVV2XSONSTKEINEEDMILNISSEXXASO
XK511
```

*Quelle des Klartexts: Norbert #18 / Max Baertl #39.*

**Schlüssel `Nov1-3`** — n = 19, Quadrat-Lücken: 0, laut Lasry-Liste 100× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
3-16-4-15-7-12-18-6-17-8-19-1-13-10-2-14-11-9-5
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 132

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov4-6`

**Geheimtext** (154 Zeichen, 77 Bigramme):

```
AAXFAFAXXFAAGVVFAFFAGVVAAAXVXXGVXVAFXDAXXADDGFFFDFAFGXAAVXVA
FAVGDGAAFXXGDXFAGAXAVDVXAFXVAVAAFAVADVXFFFFXFVVFFAVAFAVAGXVF
GVAGXFDAAXADXFAFVDAAXFXAVGFAFADVFG
```

**Klartext** (77 Zeichen):

```
FUEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUENFTERXGE
BETSORDER5MINXVVV
```

*Quelle des Klartexts: Norbert #37 / Max Baertl #39.*

**Schlüssel `Nov4-6`** — n = 17, Quadrat-Lücken: 0, laut Lasry-Liste 106× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
7-10-8-14-3-11-16-1-6-13-4-9-15-5-12-17-2
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 146

**Status:** gelöst, **bewiesen** — Geheimtext aus unabhängiger Transkription, Roundtrip exakt, 0 Konflikte

**Schlüssel:** `Nov4-6`

**Geheimtext** (244 Zeichen, 122 Bigramme):

```
FVFAFDXAXXGXDXAGVVXXFFFAXDXDXFAGVFVAXAXVVAFXAFVXAAXFGVDXGAXA
VAVVXXVDVAAXAFAFFFXVDVXAVAXFGADFFGAXAADGDAVAXGVGVAVXVGXAXXFX
XVFAXXXAVVFAAVAFXAVXVGAGXFGFFVAFAVDFXADADVAVXXXVGAFXDGXAAAFD
AVAAFGVVFADXVFXAFFVAFVFGXDVFDAXGXXFVFAVDXAAAVXAAXVXAAXXAXDGF
GXXV
```

**Klartext** (122 Zeichen):

```
FUNKSTELLEKERTSCHERHAE9TRB12X1FXR4FNAMENRICHARDEMILKARLXFUNK
STELLENDORTIGENBEREICHSBENACHRICHTIGENXNACHRICHTENCHEF4BG783
4X
```

*Quelle des Klartexts: Norbert #19 / Max Baertl #39.*

**Schlüssel `Nov4-6`** — n = 17, Quadrat-Lücken: 0, laut Lasry-Liste 106× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
7-10-8-14-3-11-16-1-6-13-4-9-15-5-12-17-2
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 153a

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov13-15a`

**Geheimtext** (352 Zeichen, 176 Bigramme):

```
AFGGGAAAAADFFGGAGGGGXVAGFXAGFVAAVGGAGAAGGGFGGAAGFGDGDAFGGGGA
GDDAFFDGGGGAAGAFGFAFGAAAAADDAAGFFDAGDGGGGAAGAFFADGDGAAGDGGGG
GVVVXXVXXVXAGXVGXXGGGAAAGFFADGGGGGDAFVAGDFAGFDFFGAAAGGGVGXGX
DXVDDXXXXVXAGXVAXXXXVVAVGDDADXAGGFGAAAFFFGADGAGFXXXXDXXGXDFG
DDXGVFXVFGGVXXVGVVVGFDGGXGXFFDVFGXXDXADXGFGAGFDDAGDFGGFDAFAX
FAFVXXXFVVADVGGFFXXVXAVAXXVXGVVXFGDFVVGXFVADXXXGAVVF
```

**Klartext** (176 Zeichen):

```
RUSSISCHEUNDPOLNHEERESVERKEHRVOLLERFASSENXWICHTIGESBESONDERE
SAUSPOLNVERKEHRUEBEROHLSTATIONVERZIFFERTFUNKENXSOWEITFERNSCH
REIBERVERBDGNICHTARBEICETXRESTSSCHRIFTLICHXNACHCHEFX0X01
```

*Quelle des Klartexts: George Lasry #50 / Norbert #53.*

**Schlüssel `Nov13-15a`** — n = 20, Quadrat-Lücken: 12, laut Lasry-Liste 13× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
13-8-6-16-7-18-1-14-9-20-10-15-17-2-3-11-5-19-4-12
```

Quadrat (36 Zeichen, zeilenweise gelesen):

```
JZLH-R--S-T-MKDWU-V-B-P--FAO-GIX-CNE
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
J Z L H . R
. . S . T .
M K D W U .
V . B . P .
. F A O . G
I X . C N E
```

### Korpus Seite 164a

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov7-9`

**Geheimtext** (126 Zeichen, 63 Bigramme):

```
VFVDGGVFFFXDGDVADGDVVXVADFDFVGVDDDFAFDDVDXDXVGFGVXXVVVGDAVVG
VVVGAGXGXGVVVXDXGVVGGXVGAGFDFDGDDVDGXGGGDDXXXDXVVGDVGVVVDDGX
DDVDDA
```

**Klartext** (63 Zeichen):

```
ELXDIEHOEHEX828XHOEHELX9IRXOXSONSTKEINEEREIGNISSEVONBEDEUTUN
GXX
```

*Quelle des Klartexts: Norbert #41 / #44.*

**Schlüssel `Nov7-9`** — n = 20, Quadrat-Lücken: 2, laut Lasry-Liste 93× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
6-12-7-15-1-11-16-5-8-14-3-18-9-13-2-17-20-10-19-4
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 164b

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov7-9`

**Geheimtext** (180 Zeichen, 90 Bigramme):

```
XVDFFXVDGDGVAGDDDDDXXADDGADAFGXDXXDGGXGDVXDAVVVXGXADDDGAGGVX
DDAGDAVAADFDAAXGDXXDGXVFDVDDGVDGXXDFGVXGXDADVVVVFDFGXFFGVVVV
GXVVXXGDGAXDGGDVGVXVDDGDVGGDVVVVFVGDFVVGFVGXGFXAAXVDDXFDXADG
```

**Klartext** (90 Zeichen):

```
XINXTEMESVARXBEFRIEDNISXUNDXDIVVONXMIRCONACHWESTENUNDSUEDENW
EGXLEIDERWEGEVOMGEGNERBESETZTX
```

*Quelle des Klartexts: Norbert #42 / #43.*

**Schlüssel `Nov7-9`** — n = 20, Quadrat-Lücken: 2, laut Lasry-Liste 93× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
6-12-7-15-1-11-16-5-8-14-3-18-9-13-2-17-20-10-19-4
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 171

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov7-9`

**Geheimtext** (314 Zeichen, 157 Bigramme):

```
AAVGFDDADXXDAAVGXAGXAFVAAADDVDAVDDDDGDDDAAGDVXGVXDGDVXVGVVVF
VFFXVVDFVDGVVDVDDVGXDVXVXXGAXAXDDDXXDDXDXXAXDVDXFXADAGDAGXGA
ADDFVXGXDDGDFFAVGDDXXDVVXFVVDADVFDDVDVAFVXXVVVFFVDVVVGDVFDVD
DVVDDDXXVGDVVXXDXDXGVDFFVDDDGGXVFGDDXXDXDDFDXGVFFDDGVGFDDVFA
DDDAXDDDAAADDDDVDDDVXVDVDXVVXVXGVGXXVXXVXVDVAGAGFDVDDADAXGXD
AVXAVDXXGXDXAX
```

**Klartext** (157 Zeichen):

```
INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHESZWISCHE
NDEUTSCHLANDUNDSOWJETREGIERUNGUNDERWARTUNGDERWIEDERHERSTELLU
NGRUSSLANDSDURCHDEUTSCHLANDUNDENTENTE
```

*Quelle des Klartexts: Norbert #20 / Max Baertl #39.*

**Schlüssel `Nov7-9`** — n = 20, Quadrat-Lücken: 2, laut Lasry-Liste 93× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
6-12-7-15-1-11-16-5-8-14-3-18-9-13-2-17-20-10-19-4
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 176a

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov10-12`

**Geheimtext** (224 Zeichen, 112 Bigramme):

```
AAAVDADDDDDFFGAFVFAAAGXGFVVAAFAVDADGDAVDAVGFGAXFXXXXADXGAVGG
ADAVVADADDVAGDVVAAAAVDFFAVDGADVAADGVVGFVVADDXAFFGXGGGGVADVGD
VGDGVAFFGAADVAVDAVVVGADVFXGFFDDAGXAVGFGVAAGXXVGVFGAVGAFGGDXV
DXVAAAVVGDFGFGAGDDGGVXGVVVVAGGGDVFGGDDDGADAA
```

**Klartext** (112 Zeichen):

```
DURCHBRUCHVORBEREITETXDURCHBRUCHSRICHTUNGNACHNORDENODERNORDO
STENERFOLGENWIRDXKANNJETZTNOCHNICHTBEEURTEILTWERDENX
```

*Quelle des Klartexts: Norbert #26 / Max Baertl #39.*

**Schlüssel `Nov10-12`** — n = 16, Quadrat-Lücken: 5, laut Lasry-Liste 46× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
9-12-7-11-3-8-16-6-14-2-10-15-5-13-1-4
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### Korpus Seite 187

**Status:** gelöst — Klartext aus dem Kommentarthread, Geheimtext synthetisch aus dem Klartext rekonstruiert (Roundtrip zirkulär)

**Schlüssel:** `Nov13-15b`

**Geheimtext** (214 Zeichen, 107 Bigramme):

```
AXFFDFADFGDAXDFFAVDDXGAAGDVXVGGDVVDFAGFFGGFVFFGDDGGVVVDDGVGG
GADVVAFDDFAVGGFXFGVVADDGVAXDADVGFFVDFVDVVGDVGGAFGGAGGFAGDAVD
VFFDDDAGAFDFADFAGAADDXVGXGGDFAADVVFGDGFFDFXDXAVFDGFGADDFFGDX
AAGFDDADVFDFFDADFGAFVFFDDVVVVVGVAF
```

**Klartext** (107 Zeichen):

```
SELLVXGENXKOMX9XAXKXBRESLAUXXBITTEWEGENDRINGENDERNOTLAGEINBE
KLEIDUNGX4000XPAARSTIEFELZUNAECHSTNACHXODERBERG
```

*Quelle des Klartexts: Norbert #24 / Max Baertl #39.*

**Schlüssel `Nov13-15b`** — n = 16, Quadrat-Lücken: 7, laut Lasry-Liste 52× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
4-11-5-14-9-7-16-1-12-15-6-10-3-13-8-2
```

Quadrat (36 Zeichen, zeilenweise gelesen):

```
H--BMUF15PX0DJLR---S6VONKZ-AWITEGC-
```

Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):

```
H . . B M U
F 1 5 P X 0
D J L R . .
. S 6 V O N
K Z . A W I
T E G C . .
```

## Ungelöste Korpus-Seiten

Der Geheimtext ist die Roh-Transkription aus `data/corpus.py` (`-` = unlesbares Zeichen). Kein Klartext, kein Schlüssel.

### Korpus Seite 73

**Status:** ungelöst — 1 unlesbare Zeichen in der Transkription

**Geheimtext** (176 Zeichen, 88 Bigramme):

```
DFXGDVDXDGGAAAGFFDDVDXFXFGGDDAVGDDDADGDGFGGDDVVDXDGDAFDDXGXX
DGXAVDXXDDGADDFGFAGVDXVFDXFDDFDDDFXDFGXFXVFDDDXXDXGDAGXFDGDD
VFXGAXDFVFDVDXVXDFXDDXFDFVDGFDGDADGDGXXFGXFAAAXXXDXAGVXD
```

### Korpus Seite 152

**Status:** ungelöst — 0 unlesbare Zeichen in der Transkription

**Geheimtext** (104 Zeichen, 52 Bigramme):

```
FXVADFDXAAXXFAGVFVDXAAGFDDFDVVVAAVAAXVGXGDAXAAGVAVADAFDDGVDD
FVAVXFVXXVFXXXGFGXGFAFXXGXGFAAAVFFXXFDFVVVAX
```

### Korpus Seite 153b

**Status:** ungelöst — 15 unlesbare Zeichen in der Transkription

**Geheimtext** (93 Zeichen, 46 Bigramme):

```
AXVAADDAFFVAXAGGADAFDXAXXXVDGDXVXFFGXFAVVAADAGXXXAXDDGVAVAXV
AXAAVVXVAVGXAXXFGXXFAAAFXVADFDXVF
```

### Korpus Seite 158

**Status:** ungelöst — 1 unlesbare Zeichen in der Transkription

**Geheimtext** (240 Zeichen, 120 Bigramme):

```
GDDFVVXVDDVVVFGXXVDDXVADDVVFGVVDDVVDVAXVXVGVVGVXDDXVVVGXGVDD
GDXVAVGGAAAXGAFFADVDADDVAXVDVVDDDGADAXFAXXFGFFXFXDVVDDXDGDDA
XVAVXXVVVVFGDVVFGDVVFGVDDDAGGVXDGXDDVVXXVDGVVVXGDXXVXVADDFGG
GDXAXVFXVDGDDFVGVGVDGVGVVDADVVDADVVVGAVVXVDGGXFAXVXGVVDDDXXF
```

### Korpus Seite 170

**Status:** ungelöst — 0 unlesbare Zeichen in der Transkription

**Geheimtext** (106 Zeichen, 53 Bigramme):

```
AAGVGVVDAGGAGAVAGGAAVAXGVAAAXFAAXAFAGVGVVVVVGDADAFGDVGVGVGAD
XAGAAGXGGAGVFVGXGXAGGGAFAXGFXXAGXVGVFDVXVDFGXV
```

### Korpus Seite 176b

**Status:** ungelöst — 0 unlesbare Zeichen in der Transkription

**Geheimtext** (220 Zeichen, 110 Bigramme):

```
GGDAAFXAVDFFFDGXXAGVXXXDVXAAFVGAGAFVFAGAVDDDDAVXGFFAFXGXXXXX
GAVAAAAGDVGGGVAAXDVXXXFADFXXXXDGVDGFDVGDDAADVXXXFVXGXXDXGGGG
AGVDGVAGGGDVVDFVAFAVVVXDFDFFFFXXXAXXGVDXXFXDFFXXDXXXXXVGGGDA
FGGDXVVVAAFDVFXXVXXFVGGFGDAAFVGGGGXAVVVV
```

### Korpus Seite 187b

**Status:** ungelöst — 0 unlesbare Zeichen in der Transkription

**Geheimtext** (142 Zeichen, 71 Bigramme):

```
AFAFFAXDVAVVVVFADVFAGXGVXAGVAXAXGGAAAAAAADDVVXVGAGAGXVVFGAAF
VVXGDGGAVGVFDVDVDDDVDXFADDDDAXADVVGAAFFGXGXAGGDADFVFXDADGDDG
GAAXDVDFADFFDDXVADDVGD
```

### Korpus Seite 189

**Status:** ungelöst — 5 unlesbare Zeichen in der Transkription

**Geheimtext** (84 Zeichen, 42 Bigramme):

```
DVGAGGAAVVAXFVXXVADAXXAGAVDVGXAXVVXVVVAVDXVXXXVGVXAAVAGAXXGA
XXFXVXXFXXGVVVDFFXDXAXDV
```

### Korpus Seite 198

**Status:** ungelöst — 0 unlesbare Zeichen in der Transkription

**Geheimtext** (165 Zeichen, 82 Bigramme):

```
DFVXVXGAXDGXVXDVGVGDVADXFFADVXXXVFVAAXGFDGFFAVXAVVVXVFVGFVFG
DGVFGFFFGVVVGGGXVFXFXXFVDVDFDDFXAAXVVXAAFXXXVGXFVDVVXXFFGXGV
FGXFGGFAAAFGXVVFXXXFFADXDAFXFVVDGVXFGAGFADDFX
```

### Korpus Seite 215

**Status:** ungelöst — 9 unlesbare Zeichen in der Transkription

**Geheimtext** (237 Zeichen, 118 Bigramme):

```
VGADAFAXADXFAXFFVXDDXXXDXDFDDAVFVGXDFFXDGFVVVFAGXXXAFAGDDFAV
DGVAVXFAFDXAFDGADVAFFVVFFAAXDGVVAVXXVGDFDFVVGDFAAFAVFVXGGVFA
AAXXDAVAVFFADAFAAXAGGADADVDFVVDFGAAVAAXADVDAXVFDFGDFGVFAGDDA
FGGDVFFDXVDFAAAXXADGFFDFFXVAAAAXXVXFXDFXGFDAVAADFDDVVXXXF
```

### Korpus Seite 217

**Status:** ungelöst — 0 unlesbare Zeichen in der Transkription

**Geheimtext** (170 Zeichen, 85 Bigramme):

```
DXXXGGVXAXADXVDGDAAADGXAGAVDGVFAFAADFFFGXFVXDDVDVFGFVVVAADXG
AAVAVAAXDGVADDDDVADGFAGVVGVVGDAVXFFDAADVFFAXGVDVDDAGDVFXAAVA
ADDAFFDFAAGXVAAGAFXDADFFXAVDAADADXXAADVAXVVADFDVAA
```

## Seite 217 (RICHI-170) — extern bewiesen

Nicht über die Lasry-Schlüsselliste gelöst, sondern über ein **Schlüsselwort**, das beide Stufen liefert: die Permutation (alphabetische Rangfolge) und ein Keyword-Quadrat mit eingestreuten Ziffern. Verifikation: `analysis/verify_article_claim.py`.

### Seite 217 / RICHI-170

**Status:** gelöst, **bewiesen** — Roundtrip exakt, 0 Konflikte

**Geheimtext** (170 Zeichen, 85 Bigramme):

```
DXXXGGVXAXADXVDGDAAADGXAGAVDGVFAFAADFFFGXFVXDDVDVFGFVVVAADXG
AAVAVAAXDGVADDDDVADGFAGVVGVVGDAVXFFDAADVFFAXGVDVDDAGDVFXAAVA
ADDAFFDFAAGXVAAGAFXDADFFXAVDAADADXXAADVAXVVADFDVAA
```

**Klartext** (85 Zeichen):

```
EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENXEINGESCHWADERD
ERXALLIIERTENFOLGT26STENX
```

**Lesefassung:** Ein englischer Kreuzer liegt in Sewastopol. (am) 24. Ein Geschwader der Alliierten folgt (am) 26.

**Schlüsselwort:** `TRUPPENVERSCHIEBUNG` — daraus die Permutation (Rangfolge der 19 Buchstaben) und das Quadrat `TRUPE4 / NVSC2H / 1I6B?G / 6AQD8F / 5?JKLM / 0?WXYZ` (`?` = handschriftlich nachgetragene Ziffer).

## Nachrichten aus dem Childs-Buch (außerhalb des Korpus)

### RICHI-264

**Status:** gelöst, **bewiesen** — 2 Reparaturen, exakter Roundtrip

**Schlüssel:** `Nov1-3`

**Geheimtext** (264 Zeichen, 132 Bigramme):

```
DVDVFDVFAGXVXFFFVGGGAGGXAXDXGFXVVDDGFGFDFAVGVDAFGFGXDFDXVVDG
DGVFFGDXDGAXAXVGVGAAAVFVGVFDGDXAFDXAXGVFAGDDDVGDVVGGDGGGVAAD
DGDVFVDDDXDVXDXDVDVAVGXVVDFVFDAXDGDAVGXDDDADGFVGDGAVAXDADDGG
FDFAGGFAXGFFXDGGGVGAFDFXXDAGAVGDVVFGXGFVFDXAAVAGAGAAVGDGGGFD
VAGGVXAADDDDAVAVVADGDGDD
```

**Klartext** (133 Zeichen):

```
DEMNACHGEHENNUMEHRSAEMTLICHESCHIFFEVONKOSPOLINACHODESSABEZWX
NIKOLAJEWXVERTEILTWIEFRX52751XUNDXBVGXRUMXXL7CHXROEMX2XGROSS
XBXFRX52787XX
```

**Lesefassung:** Demnach gehen nunmehr saemtliche Schiffe von Kospoli nach Odessa bzw. Nikolajew. Verteilt wie Fr. 52751 und B.V.G. rum. L7 Ch. Roem. 2. Gross B. Fr. 52787.

**Die zwei Reparaturen:** Bigramm 63 `AD` → `AG` (D/G-Verwechslung, Morse-plausibel), und `XG` fehlt nach Bigramm 64. Vor der Reparatur stimmten bereits 130 von 131 Zeichen. Verifikation: `analysis/verify_richi_264.py`.

**Schlüssel `Nov1-3`** — n = 19, Quadrat-Lücken: 0, laut Lasry-Liste 100× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
3-16-4-15-7-12-18-6-17-8-19-1-13-10-2-14-11-9-5
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### RICHI-222

**Status:** Struktur **bewiesen**, Lückenfüllung Kandidat

**Schlüssel:** `Nov1-3`

**Geheimtext** (144 Zeichen, 72 Bigramme):

```
FVDFGGGAVGDADXFDXDVDVGVGGAVGVDGAVDDVFGAAAADVAGFFXGDAGGXAAVGV
GDADDDVFFGDAVGXGGDFAFAGXGGGDVGADGVDDFXGGGGGGDVVGDAGVGFXGDDXV
VXVDDVDXFXXGXXFFFADDAVDX
```

**Klartext** (114 Zeichen):

```
TECHENDERXGESARMEEDENMERSCHDURMEINGARNAUFESERSCHLESIENANZITU
NTENSEINDERSTENNDWISSERDETERESEXKTERRMTLTAA1GRISISCASS
```

Von 114 Bigrammen sind nur 37 vollständig; 70 haben genau eine Lücke, 7 fehlen ganz. 144 CT-Zeichen sind überliefert und werden von der Re-Encryption exakt reproduziert (0 Mismatches). Der gezeigte Klartext ist der beste Beam-Search-Kandidat (64 Worttreffer), **nicht** bewiesen. Verifikation: `analysis/richi_222_reconstruct.py`.

**Schlüssel `Nov1-3`** — n = 19, Quadrat-Lücken: 0, laut Lasry-Liste 100× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
3-16-4-15-7-12-18-6-17-8-19-1-13-10-2-14-11-9-5
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### RICHI-274

**Status:** gelöst, verifiziert

**Schlüssel:** `Oct28-31`

**Geheimtext** (270 Zeichen, 135 Bigramme):

```
AAXFAVDXFDDAGAAAAFAADAVDAXAADXGXAAAXFFAXVAAVDAAGVGDXXVGAAVDA
GXDXGXFXXVVDXGVVXGFXVFDAFFADFAVXDAXFAXXGVFXVVADAVAAADGFXDXAD
FDAVAVFGAFFADAAFXFDFXXDAXVDXAAFDXGXADXXXDXFXXDFFAAFXGADDFGVA
XDFGDXXDFXXAGADAFVAFXXXAFFFAGFVVVAXGAFAAADAAXAGADVGVVDAAAVVX
XFGXFAFVGFXFDAVGFDGDVXFFDDXXXX
```

**Klartext** (135 Zeichen):

```
DRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTU
ELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDA
CHTISTXXDEUTZIT
```

**Lesefassung:** Drahtet ob von euren Kaeufen bereits Abtransporte erfolgt sind. Eventuell wann und wohin solche erfolgen werden und wie weiter Transport gedacht ist. Deutz it...

Erste Prüfung des Schlüssels `Oct28-31` an echtem Klartext. Die Tabelle im Buch ist 15 Zeilen × 18 Zeichen und wird spaltenweise gelesen; der Roundtrip ergibt 135/135 Zeichentreffer.

**Schlüssel `Oct28-31`** — n = 18, Quadrat-Lücken: 0, laut Lasry-Liste 33× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
6-15-12-16-5-7-14-4-13-8-11-1-17-2-10-3-18-9
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### RICHI-338

**Status:** gelöst, aber **nicht** roundtrip-verifiziert (22 CT-Fehler)

**Schlüssel:** `Oct28-31`

**Geheimtext** (306 Zeichen, 153 Bigramme):

```
VAXVVVAVGVFVGFXFDVAAAGADXFAXDFXAAGDDFVXDAAAXAVDAXAAADGAGXAXF
AFGAFFADFFVFXFFGDXXVGAAVDVAADXDFAFVXXVVDXGAAVDAAAVAFDAFFADFX
XXXFDVGDFDXXXDXFFDXAAGXGXAXFFDDXXDAXGXDFXVVXDAXVDXADGVXGXGXX
ADGFXDXDDAXFDDGDADXFDDAGAXGAGFFDFXGADDFGVDAFXFXAVAXXAFFFAGGX
ADADXFAFAAADAAXDFXXAAAAFVDAAAVVXGFFDFFAFXXXGVFXVVXGGAFVXGAFF
AXVAAV
```

**Klartext** (162 Zeichen):

```
FUERXSAULXWEINREICHXDOPPELPUNKTXDRAHTETOBVONEURENKAEUF1REH6T
IENABTRANSPORT7ERFOLGNNSN24VHLTUELLWANNUNDWOHINSOLCHEERFOLGE
NWERDEXUNDWIEWEITERTRANSPORTGEDACHTISTXXDE
```

**Lesefassung:** Fuer Saul Weinreich Doppelpunkt: Drahtet ob von euren Kaeufen Abtransporte erfolgt sind. Eventuell wann und wohin solche erfolgen werden und wie weiter Transport gedacht ist. De...

Beginnt mit den drei zusätzlichen Einleitungszeilen `FUER SAUL WEINREICH DOPPELPUNKT`; danach weicht der Text von RICHI-274 ab (nur der Kern stimmt überein). Die Tabelle ist 18 Zeilen × 18 Zeichen (324 Zeichen, davon 4 Nicht-ADFGVX-Artefakte → 320 bereinigt). Nach dem spaltenweisen Lesen bleiben 306 Zeichen (17 volle Zeilen); die letzten 14 Zeichen passen in keine volle Zeile mehr und entfallen. Re-Encryption des gespeicherten Klartexts ergibt 22 Abweichungen — der Klartext ist daher nicht als bewiesen einzustufen.

**Schlüssel `Oct28-31`** — n = 18, Quadrat-Lücken: 0, laut Lasry-Liste 33× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
6-15-12-16-5-7-14-4-13-8-11-1-17-2-10-3-18-9
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

### RICHI-240

**Status:** verifiziert, **nicht von diesem Projekt gelöst**

**Schlüssel:** `Nov10-12`

**Klartext** (156 Zeichen):

```
ANOBERSTEHEERESLEITUNGX11XARMEEXALPENKORPSIMRAUMPETERREVEVER
BASZX217X219XDIVISIONENUND6XRESERVEDIVISIONANDERLINIENAGYBEC
SKEREKVERSECXVERSECVONSERBENBESETZTX
```

**Lesefassung:** An Oberste Heeresleitung. 11. Armee: Alpenkorps im Raum Peterreve-Verbasz. 217.-219. Divisionen und 6. Reserve-Division an der Linie Nagybecskerek-Versec. Versec von Serben besetzt.

Der Geheimtext ist **nicht im Repo abgebildet** — von 220 der 240 Zeichen überliefert. Die 20 fehlenden Zeichen wurden extern ergänzt (`VFFXX DXXVV XDXDX GXXAF`), drei Ziffern über ein französisches Aufklärungstelegramm bestimmt (7, 9, 6). Quelle: prinzai.com, 19.09.2026.

**Schlüssel `Nov10-12`** — n = 16, Quadrat-Lücken: 5, laut Lasry-Liste 46× verwendet.

Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):

```
9-12-7-11-3-8-16-6-14-2-10-15-5-13-1-4
```

Quadrat (36 Zeichen, zeilenweise gelesen):

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

<!-- /GENERATED -->

---

## Quellen

- Klaus Schmeh, *The Top 50 unsolved encrypted messages: 46 — Unsolved ADFGVX
  cryptograms from World War 1*, Cipherbrain, 23.02.2017
- George Lasry, Norbert Biermann, *Schlüsselliste* (Cryptologia 2017)
- J. Rives Childs, *German Military Ciphers From February To November 1918*
  (Hrsg. William F. Friedman), archive.org 41784789082381
- William F. Friedman, *Military Cryptanalysis Part IV — Transposition and
  Fractionating Systems*, Section IX (NSA A59439)

## Lizenz

Keine. Privates Forschungsprojekt.
