---
name: relay-explorer
description: Esplorare e verificare relay API (linux.do, HelpAIO, RouterPark). Usa per cercare, confrontare e integrare nuovi 中转站.
---

# Relay Explorer

## Fonti di verifica

| Fonte | URL |
|-------|-----|
| RouterPark | https://routerpark.com |
| HelpAIO | https://www.helpaio.com/transit |
| GitHub relayAPI | https://github.com/zzsting88/relayAPI |
| linux.do 福利羊毛 | https://linux.do/c/welfare/36 |

## Checklist relay

- [ ] Uptime >95%
- [ ] Cache rate >85% (Claude)
- [ ] Politica rimborso
- [ ] Gruppo QQ attivo
- [ ] Prezzo in linea con la media

## Integrazione in Pi

Dopo test curl:

1. Aggiungi provider in `~/.pi/agent/models.json`
2. Key in `auth.json` o placeholder `$VAR` in `models.json`
3. Abilita in `settings.json` → `enabledModels`
4. Aggiorna `VPS-STACK-RELAY.md` + encrypt + guide

## Guide nel repo

- `MEGA-SUNTO.md` — panoramica mercato
- `relay-services-guide.md` — dettaglio provider
- `recommended-relays.md` — top pick
- `linux-do-navigation-guide.md` — forum + giveaway → Pi