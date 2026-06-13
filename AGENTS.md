# linux-do-explorer → migrato in ~/.pi/agent

**Da ora lavora in `~/.pi/agent`** (repo [my-pi](https://github.com/manumastro/my-pi)).

Apri quella cartella in Cursor. Tutte le guide (`AGENTS.md`, `MEGA-SUNTO.md`, `VPS-STACK-RELAY.md`, …) sono lì.

```bash
# Sync
bash ~/.pi/agent/scripts/stack-sync.sh push   # dopo modifiche
bash ~/.pi/agent/scripts/stack-sync.sh pull   # allinearsi
```

Leggi `~/.pi/agent/AGENTS.md` per il workflow completo.

**Pi da questa cartella:** usa solo `~/.pi/agent` (nessun package in `.pi/settings.json`).
Meglio: `cd ~/.pi/agent && pi` oppure apri `~/.pi/agent` in Cursor.