#!/usr/bin/env bash
# DEPRECATED — use my-pi single repo instead.
set -euo pipefail
echo "linux-do-explorer è migrato in my-pi (~/.pi/agent)."
echo ""
echo "  git clone https://github.com/manumastro/my-pi.git ~/.pi/agent"
echo "  cd ~/.pi/agent && npm install"
echo "  bash scripts/stack-sync.sh pull"
echo ""
echo "Sync reciproco: stack-sync.sh push | pull"
exit 0