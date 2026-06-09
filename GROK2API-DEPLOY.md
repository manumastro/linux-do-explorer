# grok2api — Deploy locale + integrazione Pi

**Data:** 2026-06-09
**Host:** VPS `vmi2825141` (Ubuntu, user `manu`)  
**Fork:** [jiujiu532/grok2api](https://github.com/jiujiu532/grok2api) (anti-403 / WARP)  
**Account SSO:** `grok_register/sso.txt` (150 token, gitignored)

> Questo documento descrive il deploy fatto sul VPS e come ripeterlo. Contiene riferimenti a path locali; le credenziali API sono in `~/.pi/agent/auth.json` e `~/grok2api/data/config.toml` (non committare).

---

## Cosa ottieni

| Componente | Ruolo |
|------------|-------|
| **grok2api** | Gateway OpenAI-compatible su `http://127.0.0.1:8000/v1` |
| **warp-proxy** | Uscita IP via Cloudflare WARP |
| **privoxy** | HTTP proxy → WARP SOCKS5 |
| **flaresolverr** | Refresh automatico `cf_clearance` |
| **Pi `grok2api-local`** | Provider custom in `~/.pi/agent/models.json` |

Modelli disponibili (esempi):

- `grok-4.3-console` — console gratuito, veloce
- `grok-4.20-multi-agent-xhigh` — 16 agenti paralleli
- `grok-4.20-0309-console`, `grok-4.3-fast`, ecc.

---

## 1. Prerequisiti

```bash
# Docker + docker-compose (v1)
docker --version
docker-compose --version   # /usr/bin/docker-compose su questo VPS

# Account SSO Grok (una riga JWT per account)
ls linux-do-explorer/grok_register/sso.txt
```

Ogni riga di `sso.txt` è un JWT SSO (`eyJ0eXAiOiJKV1Qi...`). Sono i cookie di sessione Grok, non API key xAI ufficiali.

---

## 2. Deploy stack anti-403 (WARP)

```bash
cd ~
git clone https://github.com/jiujiu532/grok2api.git
cd grok2api

# Avvia stack completo (init-config + WARP + privoxy + flaresolverr + grok2api)
docker-compose -f docker-compose.warp.yml up -d

# Verifica
docker-compose -f docker-compose.warp.yml ps
```

Stato atteso:

| Container | Stato |
|-----------|-------|
| `grok2api` | Up (healthy), porta `8000` |
| `warp-proxy` | Up (healthy) |
| `privoxy` | Up, `127.0.0.1:40080→8118` |
| `flaresolverr` | Up |
| `init-config` | Exit 0 (scrive proxy in `data/config.toml`) |

### File generati

```
~/grok2api/
├── data/
│   ├── config.toml      # proxy + api_key
│   └── accounts.db      # pool account SSO
├── logs/
└── docker-compose.warp.yml
```

`data/config.toml` (proxy, scritto da init-config):

```toml
[proxy.egress]
mode = "single_proxy"
proxy_url = "http://privoxy:8118"

[proxy.clearance]
mode = "flaresolverr"
flaresolverr_url = "http://flaresolverr:8191"
```

---

## 3. Configurare API key

L'API key è in `data/config.toml` sotto `[app]`:

```bash
sudo cat ~/grok2api/data/config.toml | grep api_key
```

Se manca, generane una e aggiungila:

```bash
API_KEY="grok-local-$(openssl rand -hex 16)"
sudo python3 - <<EOF
import pathlib, re
p = pathlib.Path("/home/manu/grok2api/data/config.toml")
text = p.read_text()
if "[app]" not in text:
    text += f"\n[app]\napi_key = \"{API_KEY}\"\n"
else:
    text = re.sub(r'api_key\s*=\s*".*"', f'api_key = "{API_KEY}"', text)
p.write_text(text)
print(API_KEY)
EOF
```

Poi riavvia:

```bash
cd ~/grok2api && docker-compose -f docker-compose.warp.yml restart grok2api
```

**Admin UI:** http://127.0.0.1:8000/admin/login — password default `app_key`: `grok2api`

---

## 4. Importare token SSO

### Opzione A — script incluso

```bash
cd ~/linux-do-explorer
./scripts/import-grok2api-tokens.sh
```

### Opzione B — manuale (batch da 50)

```bash
APP_KEY="grok2api"   # o la tua app_key admin
API="http://127.0.0.1:8000/admin/api"

# Login admin → cookie session (opzionale; Bearer app_key funziona anche)
curl -s -X POST "$API/tokens/add" \
  -H "Authorization: Bearer $APP_KEY" \
  -H "Content-Type: application/json" \
  -d "$(python3 - <<'PY'
import json
lines = open("/home/manu/linux-do-explorer/grok_register/sso.txt").read().splitlines()
batch = [l.strip() for l in lines[:50] if l.strip()]
print(json.dumps({"pool": "auto", "tokens": batch}))
PY
)"
```

Ripeti per le righe 51–100 e 101–150. Con `pool: "auto"` grok2api rileva automaticamente il pool (`basic` per account console gratuiti).

### Verifica account

```bash
docker exec grok2api python3 -c "
import sqlite3
c = sqlite3.connect('/app/data/accounts.db')
print('accounts:', c.execute('SELECT COUNT(*) FROM accounts').fetchone()[0])
print('active:', c.execute(\"SELECT COUNT(*) FROM accounts WHERE status='active'\").fetchone()[0])
"
```

Risultato atteso: **150/150 active**, pool `basic`, quota console ~30/30 per account.

---

## 5. Test API

```bash
export GROK2API_API_KEY="$(sudo grep api_key ~/grok2api/data/config.toml | cut -d'"' -f2)"

# Lista modelli
curl -s http://127.0.0.1:8000/v1/models \
  -H "Authorization: Bearer $GROK2API_API_KEY" | python3 -m json.tool | head -30

# Chat semplice
curl -s -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer $GROK2API_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-4.3-console","messages":[{"role":"user","content":"Say hi in 3 words"}]}'

# Multi-agent (più lento, più token)
curl -s -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer $GROK2API_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-4.20-multi-agent-xhigh","messages":[{"role":"user","content":"ok"}]}'
```

> Il primo request dopo l'avvio può dare **502** (`CONNECT tunnel failed 503`) mentre WARP/privoxy si stabilizzano. Attendi 30–60s e riprova.

---

## 6. Integrazione Pi

### File modificati

| File | Modifica |
|------|----------|
| `~/.pi/agent/models.json` | Provider `grok2api-local` → `http://127.0.0.1:8000/v1` |
| `~/.pi/agent/auth.json` | API key grok2api |
| `~/.pi/agent/settings.json` | Modelli in `enabledModels` |
| `~/.bashrc` | `export GROK2API_API_KEY=...` |

### Provider aggiunto

```json
"grok2api-local": {
  "baseUrl": "http://127.0.0.1:8000/v1",
  "apiKey": "$GROK2API_API_KEY",
  "api": "openai-completions",
  "models": [ "grok-4.3-console", "grok-4.20-multi-agent-xhigh", ... ]
}
```

Usa `openai-completions` (non `openai-responses`) — grok2api espone `/v1/chat/completions`.

### Comandi Pi

```bash
# Lista modelli
pi --list-models grok2api-local

# Chat rapida
pi --provider grok2api-local --model grok-4.3-console --print "ok"

# Multi-agent (16 agenti)
pi --provider grok2api-local --model grok-4.20-multi-agent-xhigh

# Default Pi attuale (VPS-STACK-RELAY.md): openai-anbalu / gpt-5.4-mini
# Grok resta on demand. Per default Grok (opzionale):
# "defaultProvider": "grok2api-local",
# "defaultModel": "grok-4.3-console"
```

### Altri client OpenAI-compatible

| Client | Base URL | API Key |
|--------|----------|---------|
| Cursor / Continue | `http://127.0.0.1:8000/v1` | `GROK2API_API_KEY` |
| Codex CLI | `base_url` in `config.toml` | stessa key |
| curl / script | `http://127.0.0.1:8000/v1/chat/completions` | Bearer |

---

## 7. Operazioni quotidiane

```bash
# Avvio / stop
cd ~/grok2api
docker-compose -f docker-compose.warp.yml up -d
docker-compose -f docker-compose.warp.yml down

# Log
docker logs grok2api --tail 50 -f
docker logs warp-proxy --tail 20
docker logs flaresolverr --tail 20

# Health
curl -s http://127.0.0.1:8000/health

# Aggiornare immagine
docker-compose -f docker-compose.warp.yml pull
docker-compose -f docker-compose.warp.yml up -d
```

### Riavvio dopo reboot VPS

I container hanno `restart: unless-stopped` — ripartono da soli. Verifica con `docker ps | grep grok`.

---

## 8. Troubleshooting

| Sintomo | Causa probabile | Fix |
|---------|-----------------|-----|
| **502** `CONNECT tunnel failed 503` | WARP/privoxy non pronti | Attendi 1 min, `docker-compose restart` |
| **403** su grok.com | IP in blacklist CF | Stack WARP già mitiga; controlla log flaresolverr |
| **401** API | API key sbagliata | Allinea `config.toml`, `auth.json`, `GROK2API_API_KEY` |
| Quota sync failed all'import | Token SSO scaduti/invalidi | Normale per batch bulk; i validi restano `active` |
| Pi risposta vuota | Provider sbagliato | Usa `openai-completions`, non `anthropic-messages` |
| `grok2api` unhealthy | DB/config corrotti | `docker logs grok2api`; verifica `data/accounts.db` |

### Test proxy WARP

```bash
curl -s --proxy http://127.0.0.1:40080 https://ifconfig.me
# Deve mostrare IP Cloudflare WARP (es. 161.x.x.x), non IP VPS diretto
```

### Log utili

```bash
docker logs grok2api 2>&1 | grep -E "chat request|console|error|502"
docker logs flaresolverr 2>&1 | grep -E "Challenge|Response"
```

---

## 9. Sicurezza

- **Non esporre** porta 8000 su Internet senza reverse proxy + auth
- `grok_register/` e `sso.txt` sono in `.gitignore` — non committare
- Ruota `api_key` in `config.toml` se esposta
- Gli SSO JWT sono credenziali di sessione — trattali come password

---

## 10. Riferimenti

| Risorsa | URL |
|---------|-----|
| Fork deployato | https://github.com/jiujiu532/grok2api |
| Thread linux.do | https://linux.do/t/topic/2193859 |
| Stack Pi completo (sorgente di verità) | `VPS-STACK-RELAY.md` |
| Stack crittografato | `VPS-STACK-RELAY-ENCRYPTED.md` |
| Account bulk | `grok_register/sso.txt` |
| Admin | http://127.0.0.1:8000/admin/login |

---

*Aggiornare la data in testa quando si aggiungono account, si cambia API key o si modifica lo stack Docker.*