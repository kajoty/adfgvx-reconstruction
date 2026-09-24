#!/usr/bin/env bash
#
# run_detached.sh — startet ein Analyse-Skript in einer tmux-Session.
#
# Warum? Wenn der Arbeitsplatz-PC (Windows) in Standby geht, stirbt die
# SSH-Verbindung. Ein normal gestarteter Prozess bekommt dann SIGHUP und
# wird abgeschossen. In tmux laeuft er unabhaengig weiter.
#
# Benutzung:
#   ./run_detached.sh analysis/solve_152.py
#   ./run_detached.sh analysis/solve_152.py --name s152
#
# Danach:
#   ./run_detached.sh --attach s152     # ansehen (Strg+B, D zum Loesen)
#   ./run_detached.sh --log s152        # Logdatei anzeigen
#   ./run_detached.sh --list            # laufende Sessions
#   ./run_detached.sh --stop s152       # beenden
#
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

usage() {
    sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit "${1:-0}"
}

# --- Unterbefehle -----------------------------------------------------------
case "${1:-}" in
    --list|-l)
        tmux ls 2>/dev/null || echo "Keine tmux-Sessions."
        exit 0
        ;;
    --attach|-a)
        name="${2:?Session-Name fehlt}"
        exec tmux attach -t "$name"
        ;;
    --log)
        name="${2:?Session-Name fehlt}"
        exec tail -f "$LOG_DIR/$name.log"
        ;;
    --stop)
        name="${2:?Session-Name fehlt}"
        tmux kill-session -t "$name" 2>/dev/null \
            && echo "Session '$name' beendet." \
            || echo "Session '$name' laeuft nicht."
        exit 0
        ;;
    --help|-h|"")
        usage 0
        ;;
esac

# --- Solver starten ---------------------------------------------------------
SCRIPT="$1"; shift || true

# Optionaler Name: --name <name>
NAME=""
if [[ "${1:-}" == "--name" ]]; then
    NAME="${2:?Name fehlt}"
    shift 2
fi

if [[ ! -f "$PROJECT_DIR/$SCRIPT" ]]; then
    echo "Fehler: '$SCRIPT' nicht gefunden in $PROJECT_DIR" >&2
    exit 1
fi

# Session-Name aus Skriptnamen ableiten, falls nicht gesetzt.
if [[ -z "$NAME" ]]; then
    NAME="$(basename "$SCRIPT" .py)"
fi

if tmux has-session -t "$NAME" 2>/dev/null; then
    echo "Fehler: Session '$NAME' laeuft schon." >&2
    echo "  Ansehen:  $0 --attach $NAME" >&2
    echo "  Beenden:  $0 --stop $NAME" >&2
    exit 1
fi

LOG="$LOG_DIR/$NAME.log"
: > "$LOG"   # Log leeren

# Der eigentliche Start: neue, abgekoppelte tmux-Session.
# PYTHONPATH=. sorgt fuer die Projekt-Imports.
tmux new-session -d -s "$NAME" \
    "cd '$PROJECT_DIR' && \
     echo \"=== Start: \$(date '+%F %T') ===\" | tee -a '$LOG' && \
     PYTHONPATH=. python3 -u '$SCRIPT' $* 2>&1 | tee -a '$LOG'; \
     echo \"=== Ende: \$(date '+%F %T') (Exit \$?) ===\" | tee -a '$LOG'; \
     echo; echo 'Fertig. Fenster bleibt offen.'; exec bash"

echo "Gestartet in tmux-Session '$NAME'."
echo "  Log:      $LOG"
echo "  Ansehen:  $0 --attach $NAME"
echo "  Live-Log: $0 --log $NAME"
echo "  Beenden:  $0 --stop $NAME"
echo
echo "Der Prozess laeuft unabhaengig von SSH/VS Code weiter."
echo "Du kannst VS Code schliessen und den PC in Standby schicken."
