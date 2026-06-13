---
name: vps-stack-relay
description: Sorgente di verità per stack VPS (Pi, Claude Code, Codex, relay). Usa prima di aggiungere provider, cambiare default o aggiornare chiavi.
---

# VPS Stack Relay

## Quando usare

- Aggiungere o testare un relay
- Cambiare default Pi / Claude Code / Codex
- Aggiornare documentazione dopo un test riuscito
- Riprodurre lo stack su un nuovo VPS

## Percorsi (repo linux-do-explorer)

| File | Uso |
|------|-----|
| `VPS-STACK-RELAY.md` | Sorgente in chiaro (locale, gitignored) |
| `VPS-STACK-RELAY-ENCRYPTED.md` | Versione committabile |
| `pi/manifest.json` | Manifest machine-readable per bootstrap |
| `scripts/bootstrap-pi.sh` | Script riproduzione ambiente |

## Workflow obbligatorio

1. Test: `curl` + `pi --provider X --model Y --print "ok"`
2. Aggiorna `VPS-STACK-RELAY.md` (§2 default, §4 Pi, §10 cronologia, §13 chiavi)
3. `python3 encrypt_vps_v2.py`
4. Allinea `AGENTS.md`, `MEGA-SUNTO.md`, `relay-services-guide.md`, `recommended-relays.md`, `linux-do-navigation-guide.md`
5. Commit solo file senza segreti in chiaro

## Runtime (fuori repo)

- `~/.pi/agent/settings.json` — default + packages
- `~/.pi/agent/models.json` — provider (gitignored in my-pi)
- `~/.pi/agent/auth.json` — chiavi (gitignored)
- `~/.claude/settings.json` — Claude Code attivo
- `~/.codex/config.toml` — Codex

## Comandi Pi

```text
/explorer-guide          # elenco guide
/stack-bootstrap         # checklist riproduzione
/relay-test [provider] [model]   # smoke test
```

Leggi `AGENTS.md` per il workflow completo agenti.