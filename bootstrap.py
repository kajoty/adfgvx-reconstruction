"""Zentraler Bootstrap fuer das ADFGVX-Projekt.

Setzt das Projektverzeichnis auf `sys.path`, damit die Skripte in den
Unterordnern (`solvers/`, `analysis/`, `tests/`) die Pakete `core`, `data`
usw. importieren koennen.

Verwendung in einem Skript:

    from bootstrap import setup
    setup()

    from core.adfgvx import decrypt
    from data.corpus import CORPUS
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def setup() -> str:
    """Fuegt das Projektverzeichnis zum Importpfad hinzu (idempotent)."""
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    return ROOT


# Beim Import selbst schon aktiv werden, damit `from bootstrap import setup`
# auch dann funktioniert, wenn das aufrufende Skript in einem Unterordner liegt
# und das Projektverzeichnis noch nicht im Suchpfad steht.
setup()
