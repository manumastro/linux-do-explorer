#!/usr/bin/env bash
# Import SSO tokens from grok_register/sso.txt into local grok2api admin API.
set -euo pipefail

SSO_FILE="${SSO_FILE:-/home/manu/linux-do-explorer/grok_register/sso.txt}"
API_BASE="${API_BASE:-http://127.0.0.1:8000/admin/api}"
APP_KEY="${APP_KEY:-grok2api}"
BATCH_SIZE="${BATCH_SIZE:-50}"

if [[ ! -f "$SSO_FILE" ]]; then
  echo "ERROR: SSO file not found: $SSO_FILE" >&2
  exit 1
fi

mapfile -t TOKENS < <(grep -v '^[[:space:]]*$' "$SSO_FILE")
TOTAL="${#TOKENS[@]}"

if [[ "$TOTAL" -eq 0 ]]; then
  echo "ERROR: No tokens in $SSO_FILE" >&2
  exit 1
fi

echo "Importing $TOTAL tokens from $SSO_FILE (batch=$BATCH_SIZE, pool=auto)..."

added=0
skipped=0
batch_num=0

for ((i = 0; i < TOTAL; i += BATCH_SIZE)); do
  batch_num=$((batch_num + 1))
  slice=("${TOKENS[@]:i:BATCH_SIZE}")
  payload=$(python3 -c "
import json, sys
tokens = sys.stdin.read().splitlines()
print(json.dumps({'pool': 'auto', 'tokens': tokens}))
" <<< "$(printf '%s\n' "${slice[@]}")")

  resp=$(curl -s -X POST "$API_BASE/tokens/add" \
    -H "Authorization: Bearer $APP_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")

  count=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('count',0))" 2>/dev/null || echo "?")
  skip=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('skipped',0))" 2>/dev/null || echo "?")
  added=$((added + count))
  skipped=$((skipped + skip))
  echo "  batch $batch_num: added=$count skipped=$skip"
done

echo "Done. reported added=$added skipped=$skipped (total lines=$TOTAL)"

docker exec grok2api python3 -c "
import sqlite3
c = sqlite3.connect('/app/data/accounts.db')
n = c.execute('SELECT COUNT(*) FROM accounts').fetchone()[0]
a = c.execute(\"SELECT COUNT(*) FROM accounts WHERE status='active'\").fetchone()[0]
print(f'DB: {n} accounts, {a} active')
" 2>/dev/null || echo "(skip DB check — grok2api container not running)"