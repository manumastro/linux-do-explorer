#!/usr/bin/env bash
# Export/import Pi secrets (models.json, auth.json) for stack reproduction.
# Backup dir is gitignored — copy to new VPS via scp/rsync.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${STACK_BACKUP_DIR:-$REPO_ROOT/stack-backup/pi-agent}"
PI_AGENT="${PI_AGENT_DIR:-$HOME/.pi/agent}"

usage() {
  cat <<EOF
Usage: $(basename "$0") export|import|status

  export  Copy ~/.pi/agent/{models,auth}.json → stack-backup/pi-agent/
  import  Restore backup → ~/.pi/agent/ (chmod 600)
  status  Show which files exist in backup vs runtime

Env: PI_AGENT_DIR, STACK_BACKUP_DIR
EOF
}

mkdir -p "$BACKUP_DIR"

export_secrets() {
  local copied=0
  for f in models.json auth.json; do
    if [[ -f "$PI_AGENT/$f" ]]; then
      cp "$PI_AGENT/$f" "$BACKUP_DIR/$f"
      chmod 600 "$BACKUP_DIR/$f"
      echo "  exported $f"
      copied=$((copied + 1))
    else
      echo "  skip $f (not in $PI_AGENT)" >&2
    fi
  done
  if [[ $copied -eq 0 ]]; then
    echo "ERROR: nothing to export" >&2
    exit 1
  fi
  echo "Backup: $BACKUP_DIR"
}

import_secrets() {
  local imported=0
  mkdir -p "$PI_AGENT"
  for f in models.json auth.json; do
    if [[ -f "$BACKUP_DIR/$f" ]]; then
      cp "$BACKUP_DIR/$f" "$PI_AGENT/$f"
      chmod 600 "$PI_AGENT/$f"
      echo "  imported $f → $PI_AGENT/$f"
      imported=$((imported + 1))
    fi
  done
  if [[ $imported -eq 0 ]]; then
    echo "WARN: no backup in $BACKUP_DIR — copy from VPS-STACK-RELAY.md §13 or scp from source machine"
    exit 0
  fi
}

show_status() {
  echo "Runtime: $PI_AGENT"
  echo "Backup:  $BACKUP_DIR"
  for f in models.json auth.json; do
    local r b
    r=$([[ -f "$PI_AGENT/$f" ]] && echo yes || echo no)
    b=$([[ -f "$BACKUP_DIR/$f" ]] && echo yes || echo no)
    printf "  %-12s runtime=%s  backup=%s\n" "$f" "$r" "$b"
  done
}

cmd="${1:-}"
case "$cmd" in
  export) export_secrets ;;
  import) import_secrets ;;
  status) show_status ;;
  -h|--help|help|"") usage ;;
  *) echo "Unknown command: $cmd" >&2; usage; exit 1 ;;
esac