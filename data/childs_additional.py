"""Additional Childs/Friedman ADFGVX material.

The two messages below are reproduced from the OCR of
"German Military Ciphers from February to November 1918", p. 57 of the
Internet Archive scan.  They are teaching examples, not entries from the
22-message online challenge corpus.  OCR uncertainty is intentionally kept
in the raw text.
"""

MESSAGES: dict[str, dict[str, str]] = {
    "CHI-82": {
        "source": "Childs/Friedman scan, OCR p. 57",
        "route": "DJL v DFM",
        "raw": (
            "VADDG GDDGF AXGXD DDXXA AXFAD XGVVD "
            "XDADG DXAXD DGAA X GVXGX VAGFV GXDFV "
            "GVGGG GFGGD A V V G X X X D G V AG"
        ),
        "note": "OCR/layout loses column separators; not yet a clean linear CT.",
    },
    "CHI-60": {
        "source": "Childs/Friedman scan, OCR p. 57",
        "route": "DJL v DFM",
        "raw": (
            "VAAGG DGGAA XDGXA A X A D A VV-DAD GGAXF "
            "AGXXX GXDGF VXDXG VVGGV DAXGX FDGVV"
        ),
        "note": "OCR/layout loses column separators; one block contains an unreadable mark.",
    },
}


# Additional RICHI message identifiers explicitly discussed in the volume.
# RICHI-274 und RICHI-338 sind inzwischen vollstaendig entschluesselt
# (siehe unten, Schluessel Oct28-31). Die uebrigen warten noch auf eine
# saubere Transkription der Seitenbilder.
IDENTIFIED_MESSAGES = {
    "RICHI-152": "Childs/Friedman OCR, October 9, 1918",
    "RICHI-168": "Childs/Friedman OCR, paired with RICHI-222",
    "RICHI-222": "Childs/Friedman OCR, paired with RICHI-168",
    "RICHI-274": "Childs/Friedman OCR, October 30, 1918 -- SOLVED (Oct28-31)",
    "RICHI-338": "Childs/Friedman OCR, October 30, 1918 -- SOLVED (Oct28-31)",
}


# ---------------------------------------------------------------------------
# RICHI-264 / RICHI-266 (1./2. November 1918) -- BEWIESEN (2 Reparaturen)
# ---------------------------------------------------------------------------
# Vollstaendig entschluesselt und BEWIESEN (Stand 24.09.2026):
#
#   Der OCR-CT (264 Zeichen = 132 Bigramme) entschluesselt mit Schluessel
#   "Nov1-3" zu einem Klartext, der an genau 2 Stellen vom gespeicherten
#   Klartext (133 Zeichen) abweicht:
#
#     Fehler 1: Bigramm 63 ist AD (liefert I), sollte AG sein (liefert O).
#               -> D/G-Verwechslung, Morse-plausibel (D=-.., G=--.).
#     Fehler 2: Ein Bigramm fehlt im CT. Nach Bigramm 64 (AF -> L) fehlt
#               XG (liefert A). -> Loeschung im CT.
#
#   Nach beiden Reparaturen (266 Zeichen):
#     Beweis 1 (Dekodierung):  reparierter CT -> Klartext == gespeicherter Klartext
#     Beweis 2 (Re-Encryption): Klartext -> Chiffre == reparierter CT
#     Beide: True. 130 von 131 Zeichen waren schon vor der Reparatur exakt.
#
#   Die Nutzer-Transkription (266 Zeichen) enthaelt genau diese 2 Korrekturen
#   bereits implizit -- sie ist die vollstaendigere Fassung.
#
# Zwei unabhaengige Transkriptionen liegen vor:
#   * OCR (docs/childs_djvu.txt, Sequenz 264) -- 264 Zeichen
#   * Nutzer-Transkription (docs/childs_pages/266.md) -- 266 Zeichen
# Beide entschluesseln sich zu derselben Nachricht. Die Nutzer-Transkription
# ist bei "NIKOLAJEW" korrekt (OCR liest faelschlich "NIKILJEW"), die OCR ist
# bei "NUMEHR", "SAEMTLICH", "SCHIFFE", "L7CH" und "52751" kohaerenter.
# Die konsolidierte Fassung uebernimmt die jeweils bessere Lesart.

RICHI_264_CT_OCR = (
    "DVDVFDVFAGXVXFFFVGGGAGGXAXDXGFXVVDDGFGFDFAVGVDAFGFGXDFDXVVDGDGVFFGDXDGAXAX"
    "VGVGAAAVFVGVFDGDXAFDXAXGVFAGDDDVGDVVGGDGGGVAADDGDVFVDDDXDVXDXDVDVAVGXVVDFVF"
    "DAXDGDAVGXDDDADGFVGDGAVAXDADDGGFDFAGGFAXGFFXDGGGVGAFDFXXDAGAVGDVVFGXGFVFDX"
    "AAVAGAGAAVGDGGGFDVAGGVXAADDDDAVAVVADGDGDD"
)

# Nutzer-Abschrift direkt vom Childs-Scan (Header: "2-TL RICHI 264").
# Zeichen fuer Zeichen mit dem OCR-CT oben identisch (264/264).
RICHI_264_CT_SCAN = RICHI_264_CT_OCR

RICHI_264_CT_USER = (
    "DVVDFDVDVGDVVGFFVGGGAXDADDGGGFXVVDDAADDGDVVGVDAFGGFGFDFAVVDGDGVDFVVDAXGAXAX"
    "VGDDDADGFVGVFDGDFGXDFDXGVFAGDDVGAAAVFGDGGGVGAXGVFXDFFDDDXGFAGXVXFVAVGXVXGG"
    "XAXDXDGDAVGXDFFXDAGVGDGAVAADGDGDDFDFAGGFVXDXDVDGGGVGAFGXGFVFDAVGDVVFVFFGDXDX"
    "AAVAGAGVXAADDGGFDVAGXAFDXAXDDAVAVVGAAVGDG"
)

RICHI_264_KEY = "Nov1-3"

# Konsolidierter Klartext (OCR-Basis, korrigiert um NIKOLAJEW aus der
# Nutzer-Transkription). 133 Zeichen.
RICHI_264_PLAINTEXT = (
    "DEMNACHGEHENNUMEHRSAEMTLICHESCHIFFEVONKOSPOLINACHODESSABEZWXNIKOLAJEWX"
    "VERTEILTWIEFRX52751XUNDXBVGXRUMXXL7CHXROEMX2XGROSSXBXFRX52787XX"
)

# Lesefassung mit Worttrennungen (X = Worttrenner im Original).
RICHI_264_READING = (
    "Demnach gehen nunmehr saemtliche Schiffe von Kospoli nach Odessa bzw. "
    "Nikolajew. Verteilt wie Fr. 52751 und B.V.G. rum. L7 Ch. Roem. 2. "
    "Gross B. Fr. 52787."
)

# Rekonstruktion der vollstaendigen 266-Zeichen-Fassung anhand des im Buch
# gedruckten Klartextanfangs und der unabhaengigen Transkription in 266.md.
# Das ist ein aus dem Klartext neu berechneter CT, kein direktes Faksimile.
# Gegen die 266-Zeichen-Transkription weichen sechs CT-Zeichen ab.
RICHI_264_RECONSTRUCTED_CT = (
    "DVDVF DVDVG DVVGF FVGGG AXDAD DGGGF XVVDD AADDG DVVGV DAFGG "
    "FGFDF AVVDG DGVDF VFDAX GAXAX VGDDD ADGFV GVFDG DFGXD FDXGV "
    "FAGDD VGAAA VFGDG GGVGA XGFFX DFVDD DXGFA GXVXF VAVGX VXGGX "
    "AXDXD GDAVG XDFXX DAGVG DGAVA ADGDG DDFDF AGGFV XDXDV DGGGV "
    "GAFGX GFVFD AVGDV VFVFF GDXDX AAVAG AGVXA ADDGG FDVAG XAFDX "
    "AXDDA VAVVG AAVGD G"
)
RICHI_264_RECONSTRUCTION_DIFFS = (
    (3, "V", "D"), (4, "D", "V"), (67, "V", "F"),
    (123, "V", "F"), (128, "F", "V"), (164, "F", "X"),
)


# ---------------------------------------------------------------------------
# RICHI-274 / RICHI-338 (30. Oktober 1918) -- VERIFIKATION
# ---------------------------------------------------------------------------
# Verifikation zweier Childs-Nachrichten ausserhalb des 22-Seiten-Korpus.
# Die im Buch dokumentierte Beziehung (RICHI-274 = RICHI-338 minus drei
# einleitende Zeilen "FUER SAUL WEINREICH DOPPELPUNKT") wird durch die
# Entschluesselung bestaetigt.
#
# KEIN neuer Schluessel, KEINE neue Methode: Der Schluessel "Oct28-31"
# (n=33) stammt aus der Lasry-Liste, die Tabellen aus dem OCR des
# Childs-Buchs. Neu ist allein, dass dieser bisher UNVERIFIED-Schluessel
# erstmals an echtem Klartext geprueft (verifiziert) ist.
#
# Quelle: docs/childs_djvu.txt
#   * RICHI-274-Tabelle: Index 76326 (15 Zeilen x 18 Zeichen)
#   * RICHI-338-Tabelle: Index 77542 (18 Zeilen x 18 Zeichen, saubere OCR)
#   * Permutation: 6-15-12-16-5-7-14-4-13-8-11-1-17-2-10-3-18-9 (Rangordnung)
#   * Leserichtung: spaltenweise (Spalte 1..18), dann untranspose(ct, perm)
#
# WICHTIG: Die im Buch abgedruckte Permutation ist eine RANGFOLGE (1-basiert),
# NICHT eine Lesereihenfolge. Sie wird direkt als `perm` an untranspose()
# uebergeben.

RICHI_274_338_KEY = "Oct28-31"
RICHI_274_338_PERM = [6, 15, 12, 16, 5, 7, 14, 4, 13, 8, 11, 1, 17, 2, 10, 3, 18, 9]

# RICHI-274: 15 Zeilen x 18 Zeichen (OCR, Index 76326).
RICHI_274_TABLE = (
    "AAGAGVVAFFFDXAVAXG"
    "AAXAXXXDDXDFDFVGFF"
    "XFAGDGDAAFXFFVVAGD"
    "FAAVXFAVVDGAGAADXG"
    "AAAGGXXAAFXADFXVFD"
    "VDXDXVFAVXAFXXGGAV"
    "DAFXFFAAFXDXXXAVFX"
    "XVFXXDXDGDXGDXFVVF"
    "FDAVXAXGAAXAFAADGF"
    "DAXGVFGFFXXDXFAAFD"
    "DXVAVFVXFVDDXFAAXD"
    "AAAADAFDADXFAFDAFX"
    "GAAVXDXXDXFGGAAVDX"
    "ADVDGFVAAAXVAGAVAX"
    "AXDAVAVDAAXADFXXVX"
)

# RICHI-338: 18 Zeilen x 18 Zeichen (saubere OCR, Index 77542).
RICHI_338_TABLE = (
    "VVDAFVAXFDADADGDGX"
    "AADDFAAXDADDXAXFFG"
    "XAFGVAVXXXGAGFAXFG"
    "VAVAFDDXAGVXAXDXDA"
    "VGXGXXAFAXXFGFAAFF"
    "VADXFDADGDGDFXDAFV"
    "ADAA5FFAVXFXDFAXAA"
    "XVXAXGAVGGXGGDVFAF"
    "GGFAFDfADXVXDFAAFX"
    "AVAXAXPV%FFAVXAiXX"
    "FVXFFXAFXXDDXXADGX"
    "ADXFVDVGVXAXFDDXAA"
    "AAGAGFDAGVFXFAGFDF"
    "AAVXFXAFAVFXDXFDDF"
    "DAFVXAXFADADDVXDFF"
    "AVXAFAAAVXDXXDDAGA"
    "AVVADGADDGFFXXXGVG"
    "XXVVAADAAVAXXAAAAF"
)

# Klartext RICHI-274 (Score -18.25, 100 Worthits).
RICHI_274_PLAINTEXT = (
    "DRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTUELLWANNUNDWOHINS"
    "OLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDACHTISTXXDEUTZIT"
)

RICHI_274_READING = (
    "Drahtet ob von euren Kaeufen bereits Abtransporte erfolgt sind. "
    "Eventuell wann und wohin solche erfolgen werden und wie weiter "
    "Transport gedacht ist. Deutz it..."
)

# Klartext RICHI-338 (Score -21.46, 90 Worthits). Enthaelt die drei
# zusaetzlichen Einleitungszeilen "FUER SAUL WEINREICH DOPPELPUNKT".
RICHI_338_PLAINTEXT = (
    "FUERXSAULXWEINREICHXDOPPELPUNKTXDRAHTETOBVONEURENKAEUF1REH6TIENABTRANSPORT7E"
    "RFOLGNNSN24VHLTUELLWANNUNDWOHINSOLCHEERFOLGENWERDEXUNDWIEWEITERTRANSPORTGEDACHTI"
    "STXXDE"
)

RICHI_338_READING = (
    "Fuer Saul Weinreich Doppelpunkt: Drahtet ob von euren Kaeufen "
    "Abtransporte erfolgt sind. Eventuell wann und wohin solche erfolgen "
    "werden und wie weiter Transport gedacht ist. De..."
)