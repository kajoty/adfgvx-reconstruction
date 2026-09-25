# ADFGVX — 22 ungelöste Kryptogramme aus dem Ersten Weltkrieg

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
verwendeten Schlüssel bekannt sind** — und trotzdem sind 10 davon bis heute
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

1. **Eine ehrliche Evidenzlage.** Für jede der 12 „gelösten" Seiten steht
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
| Gelöste Seiten | 12 | Klartext bekannt, Quelle dokumentiert |
| Ungelöste Seiten | 10 | Schlüssel bekannt, Text nicht lesbar |
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
| Extern bewiesen | 1 | Seite 217 / RICHI-170, 0 Konflikte |
| Rekonstruiert | 9 | Klartext aus Kommentar, Geheimtext synthetisch |
| Ungelöst | 10 | Schlüssel bekannt, Text nicht lesbar |

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
analysis/               41 Diagnose- und Verifikationsskripte
tests/                  5 Testdateien
docs/                   HANDBUCH.md, Quellen-PDFs, Transkriptionen
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
Militärtextes. Die Normierung macht die Gewichte längenunabhängig.

| Text | Fitness |
|---|---|
| Echter deutscher Text | 35–40 |
| Overfit (Seite 152) | 30 |
| Rauschen | −2 |

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
`<!-- GENERATED: dump_messages.py -->` und `<!-- /GENERATED -->`. Der Aufruf ist
idempotent — mehrfaches Ausführen ändert nichts.

---

# 4. WHAT IF — Was wäre wenn?

## Wenn die Daten sauber wären

Dann wären die 10 ungelösten Seiten in Minuten gelöst. Die Schlüssel liegen
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

Vier genutzte Schlüssel haben Lücken im Substitutionsquadrat:

| Schlüssel | Lücken | Betroffene Seiten |
|---|---|---|
| Nov13-15a | 12 | 153a |
| Nov13-15b | 7 | 187 |
| Nov10-12 | 5 | 176a |
| Nov7-9 | 2 | 171, 164a, 164b |

`make_square()` füllt diese Lücken mit dem Restalphabet — eine willkürliche
Annahme. Bei Nov13-15a werden 8 der 12 gefüllten Zellen vom Klartext benutzt.
Solange die Lücken nicht aufgelöst sind, bleiben diese Quadrate Annahmen.

## Wenn es eine fundamentale Symmetrie gibt

Die Bigramm-Verteilung des Zwischentexts ist unter Spaltenpermutationen
invariant. Das ist kein Implementierungsdetail, sondern eine Eigenschaft des
Verfahrens:

- Die echte Permutation hat die **stärkste** Bigramm-Konzentration von 2000
  getesteten Permutationen (Rang 2000/2000).
- Aber: Simulated Annealing auf diesem Signal findet einen Zustand mit
  *exakt identischer* Bigramm-Verteilung — und trotzdem nur 2/20 korrekte
  Positionen.
- Grund: Verschiedene Auslesereihenfolgen erzeugen dieselbe
  Segment-Sequenz, ordnen sie aber anderen logischen Spalten zu.

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

**Wichtig:** `word_hits` auf Zufallstext ist genauso hoch wie auf echten
kurzen Seiten (24 vs. 29 Treffer bei Länge 104). Die Trefferzahl ist **kein**
Erfolgsindikator, solange keine Zufalls-Baseline gemessen wurde.

## Was wirklich hart bewiesen ist

| Befund | Beweis |
|---|---|
| Seite 217 / RICHI-170 | TRUPPENVERSCHIEBUNG, 0 Konflikte, Roundtrip gegen echtes CT |
| RICHI-264 | 2 Reparaturen, Re-Encryption == OCR-CT |
| RICHI-274 / RICHI-338 | Oct28-31 erstmals an echtem Klartext validiert |
| Seiten 100, 105, 146 | echte Transkription + vollständiger Roundtrip |
| Transposition | 100 % Zeichentreffer auf 10/10 Seiten (mit korrigiertem CT) |

## Der Ausblick

Die Kryptanalyse ist erschöpft. Die nächsten Schritte sind Datenarbeit:

1. **Unabhängige Transkriptionen** für die 10 rekonstruierten Seiten
   beschaffen — der eigentliche Engpass.
2. **Quadrat-Lücken** in Nov13-15a/b, Nov10-12, Nov7-9 auflösen.
3. **Erst dann** die Seiten mit 0 Lücken (152, 170, 176b, 187b, 198) mit dem
   `conflict_solver` angreifen.

## Wenn man es trotzdem blind versuchen will

Der `blind_solver` ist der ehrliche Test: Er bekommt nur den Geheimtext und die
Spaltenzahl. Er scheitert — auch auf einem *perfekten* synthetischen Testfall
mit bekanntem Klartext. Das ist kein Implementierungsfehler, sondern die
Aussage des Projekts: **Die Landschaft erlaubt keine blinde Suche.**

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
