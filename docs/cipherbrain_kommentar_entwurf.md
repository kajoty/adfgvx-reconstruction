# Kommentar-Entwurf für den Cipherbrain-Thread

**Ziel-Thread:** Klaus Schmeh, „Unsolved ADFGVX messages from World War I"
(scienceblogs.de/klausis-krypto-kolumne/unsolved-adfxvx-messages-from-world-war-i/)

**Framing:** Bestätigung / Verifikation — **keine** Entdeckung, **kein**
Durchbruch. Der Schlüssel ist bekannt (Lasry-Liste), die Tabellen stehen im
Childs-Buch. Neu ist nur die erstmalige Prüfung an echtem Klartext.

---

## Entwurf (deutsch)

Hallo zusammen,

als kleine Ergänzung zur Schlüsselliste von George Lasry: Ich habe zwei
Nachrichten aus dem Childs-Buch („German Military Ciphers From February To
November 1918", 30.10.1918) mit dem dort gelisteten Schlüssel **Oct 28–31**
entschlüsselt. Es handelt sich um **RICHI-274** und **RICHI-338**.

Das Buch beschreibt die beiden als Duplikat: RICHI-274 sei RICHI-338 ohne
drei einleitende Zeilen. Die Entschlüsselung bestätigt das im Kern —
RICHI-338 beginnt mit „FUER SAUL WEINREICH DOPPELPUNKT", danach folgt
derselbe Text wie in RICHI-274. Allerdings weichen die beiden Klartexte
danach an mehreren Stellen voneinander ab (Ähnlichkeit ~0.77), was auf
OCR-Fehler in der RICHI-338-Tabelle hindeutet.

Klartext (RICHI-274, 15×18-Tabelle, spaltenweise gelesen, Permutation
6-15-12-16-5-7-14-4-13-8-11-1-17-2-10-3-18-9):

`DRAHTET OB VON EUREN KAEUFEN BEREITS ABTRANSPORTE ERFOLGT SIND.
EVENTUELL WANN UND WOHIN SOLCHE ERFOLGEN WERDEN UND WIE WEITER TRANSPORT
GEDACHT IST. DEUTZ IT …`

Der Sprachmodell-Score liegt bei −18.25 (RICHI-274) bzw. −21.46 (RICHI-338),
also klar im Bereich echten deutschen Textes.

**Was daran neu ist:** nicht der Schlüssel und nicht die Methode — beides
war bekannt. Neu ist, dass der Schlüssel Oct 28–31 damit erstmals an
tatsächlichem Klartext geprüft ist. Falls das für die Liste nützlich ist,
stelle ich die Tabellen und den Code gern bereit.

Viele Grüße

---

## Hinweise zur Verwendung

- **Nicht** als „gelöst" oder „geknackt" formulieren — der Schlüssel war
  bekannt.
- Die 11 ungelösten Korpus-Seiten sind davon **unberührt**; das klarstellen,
  falls jemand danach fragt.
- Die Tabellen stammen aus dem OCR (`childs_djvu.txt`, Index 76326 und 77542);
  OCR-Fehler sind möglich, der Klartext ist aber kohärent.
- **Wichtig:** Die Duplikat-Beziehung (274 = 338 ohne Präfix) gilt nur im Kern.
  Die Klartexte weichen danach ab (Ähnlichkeit ~0.77) — vermutlich OCR-Fehler
  in der 338-Tabelle. Nicht als „identisch" formulieren.
- Bei Rückfragen auf `data/childs_additional.py` verweisen (enthält Tabellen,
  Permutation, Klartexte, Lesefassungen).
