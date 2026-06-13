#!/usr/bin/env bash
# Bootstrap Pi stack from linux-do-explorer + my-pi on a fresh machine.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PI_AGENT="${PI_AGENT_DIR:-$HOME/.pi/agent}"
MANIFEST="$REPO_ROOT/pi/manifest.json"

echo "==> linux-do-explorer bootstrap"
echo "    repo: $REPO_ROOT"
echo "    pi agent dir: $PI_AGENT"

if ! command -v pi >/dev/null 2>&1; then
  echo "ERROR: pi CLI not found. Install Node 24+ and pi-coding-agent first." >&2
  exit 1
fi

echo "==> Decrypt VPS-STACK-RELAY.md if missing"
PLAIN_STACK="$REPO_ROOT/VPS-STACK-RELAY.md"
if [[ ! -f "$PLAIN_STACK" ]] && [[ -f "$REPO_ROOT/VPS-STACK-RELAY-ENCRYPTED.md" ]]; then
  python3 "$REPO_ROOT/encrypt_vps_v2.py" decrypt "$REPO_ROOT/VPS-STACK-RELAY-ENCRYPTED.md"
  chmod 600 "$PLAIN_STACK" 2>/dev/null || true
  echo "    decrypted → VPS-STACK-RELAY.md"
elif [[ -f "$PLAIN_STACK" ]]; then
  echo "    VPS-STACK-RELAY.md already present"
else
  echo "    WARN: no stack doc found; continue without decrypt"
fi

echo "==> Install my-pi (settings + extensions, no secrets)"
pi install git:github.com/manumastro/my-pi@master || {
  echo "WARN: my-pi install failed — clone manually into $PI_AGENT"
}

echo "==> Install linux-do-explorer pi package"
if [[ -f "$REPO_ROOT/package.json" ]]; then
  pi install "$REPO_ROOT" || pi install git:github.com/manumastro/linux-do-explorer@main
else
  pi install git:github.com/manumastro/linux-do-explorer@main
fi

echo "==> Import Pi secrets if backup present"
if [[ -x "$REPO_ROOT/scripts/sync-pi-secrets.sh" ]]; then
  "$REPO_ROOT/scripts/sync-pi-secrets.sh" import || true
fi

echo "==> Ensure agent directories"
mkdir -p "$PI_AGENT" "$HOME/.claude" "$HOME/.codex"

echo "==> Secrets (manual step)"
cat <<'EOF'

  models.json and auth.json are NOT in git.
  Copy from VPS-STACK-RELAY.md §13 or restore a backup:

    ~/.pi/agent/models.json
    ~/.pi/agent/auth.json

  Optional env vars (see pi/manifest.json):
    ROUTERPARK_API_KEY, ROUTERPARK_BBS_API_KEY, API_777358_KEY,
    MIMO_CN_API_KEY, DEEPSEEK_API_KEY, GROK2API_API_KEY

EOF

if [[ -f "$MANIFEST" ]] && command -v jq >/dev/null 2>&1; then
  echo "==> Smoke tests from manifest"
  while IFS= read -r cmd; do
    [[ -z "$cmd" ]] && continue
    echo "    $ $cmd"
    if $cmd >/dev/null 2>&1; then
      echo "      OK"
    else
      echo "      SKIP/FAIL (missing keys or provider)"
    fi
  done < <(jq -r '.smokeTests[].cmd' "$MANIFEST")
fi

echo "==> Done. In Pi run: /explorer-guide  /stack-bootstrap  /relay-test"
echo "    Skills: /skill:vps-stack-relay  /skill:relay-explorer"