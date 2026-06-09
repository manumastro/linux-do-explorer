# VPS — Stack AI, relay e configurazioni

**Host:** `vmi2825141` (Ubuntu, user `manu`)  
**Data documento:** 2026-06-08  
**Ambito:** tutto ciò che gira su **questo VPS** (Pi, Claude Code, Codex, chiavi in `~/.pi/agent`, `~/.claude`, `~/.codex`).

> 🔐 **Sicurezza:** questo file contiene **password e chiavi API crittografate**. Per decrittografare: `python3 encrypt_vps_v2.py decrypt VPS-STACK-RELAY-ENCRYPTED.md`

---

## 1. Strumenti installati sul VPS

| Strumento | Path / versione | Ruolo |
|-----------|-------------------|--------|
| **Pi** (`pi`) | `~/.nvm/.../pi-coding-agent` | Agente coding principale, multi-relay |
| **Claude Code** (`claude`) | `~/.claude/` | CLI Anthropic-style via relay |
| **Codex** (`codex`) | `~/.codex/` | CLI OpenAI-style (Codex / GPT) |
| **linux-do-explorer** | `/home/manu/linux-do-explorer` | Ricerca relay (guide AGENTS.md, HelpAIO, RouterPark) |
| **grok2api** (locale) | `/home/manu/grok2api` | Gateway Grok self-hosted, 150 SSO, WARP anti-403 |

---

## 2. Default attuali (cosa usiamo ogni giorno)

| App | File config | Provider / endpoint | Modello default |
|-----|-------------|---------------------|-----------------|
| **Pi** | `~/.pi/agent/settings.json` | `minimax-cn` → `api.minimaxi.com/anthropic` | `MiniMax-M3` |
| **Claude Code** | `~/.claude/settings.json` | **RouterPark BBS** → `https://routerpark.com` | `claude-sonnet-4-6` |
| **Codex** | `~/.codex/config.toml` | **Anbalu** → `https://api.anbalu.top/v1` | `gpt-5.5` |
| **Pi (Grok)** | `~/.pi/agent/models.json` | **grok2api-local** → `http://127.0.0.1:8000/v1` | `grok-4.3-console` (on demand) |

**Nota:** Pi e Claude Code **non** condividono lo stesso relay Claude. Codex usa Anbalu, non i relay del post RouterPark (`v2api.top` / whitedream). Grok via **grok2api** è self-hosted (non relay a pagamento).

---

## 3. Account relay (lista fornita) — stato sul VPS

Legenda: ✅ configurato e testato · 🟡 account / chiave nota, **non** in config VPS · ❌ non usato · 🔑 solo login console (API key da generare)

| Sito | Login console | API / endpoint atteso | Stato VPS | Provider Pi (se esiste) |
|------|---------------|------------------------|-----------|---------------------------|
| [micuapi.ai](https://www.micuapi.ai/) | GitHub **manumastro** | `https://www.micuapi.ai` (tipico `/v1`) | 🟡 Account only | — (non in `models.json`) |
| [zjapi.com](https://zjapi.com/) | **manustrong1212** / ENC:aPbNZjS9pzZSZw== | `https://zjapi.com/v1` | ✅ In Pi | `openai-zjapi` |
| [app.anbalu.top](https://app.anbalu.top/) | **emanuele.mastronardi.2002.12@gmail.com** / ENC:aPbNZjS9pzZSZw== | `https://api.anbalu.top/v1` | ✅ Pi + **Codex default** | `openai-anbalu` |
| [rkapi.com](https://rkapi.com/console/personal) | **manustrong** / ENC:aPbNZjS9pzZSZw== | (console RK API) | 🟡 Account only | — |
| [freemodel.dev](https://freemodel.dev/dashboard) | **emanuele.mastronardi.2002.12@gmail.com** | `https://api.freemodel.dev` · Claude: `https://cc.freemodel.dev` | ✅ Pi + **Claude Code** | `openai-freemodel`, `claude-freemodel` |
| [api.bluesminds.com](https://api.bluesminds.com/) | GitHub | `https://api.bluesminds.com/v1` | ✅ In Pi (non default) | `bluesminds` |
| [52mx.net](https://52mx.net/console) | **manumastro** / ENC:aPbNZjS9pzZSZw== | `https://52mx.net/v1` | ✅ In Pi | `52model` |
| [api520.pro](https://api520.pro/) | **trapbeats1212@gmail.com** / ENC:aPbNZjS9pzZSZw== | (prob. OpenAI-compatible) | 🟡 Account only | — |
| [api.iamhc.cn](https://api.iamhc.cn/console) | **trapbeats1212@gmail.com** / ENC:aPbNZjS9pzZSZw== | `https://api.iamhc.cn` | ✅ In Pi (MiniMax M3) | `minimax-iamhc` |

### Altri relay attivi su VPS (non nella lista sopra)

| Servizio | Uso | Note |
|----------|-----|------|
| **grok2api-local** `http://127.0.0.1:8000/v1` | Pi Grok console + multi-agent | 150 SSO da `grok_register/`; stack Docker WARP; guida `GROK2API-DEPLOY.md` |
| **RouterPark** `https://routerpark.com/v1` | Pi Claude (2 provider) + **Claude CLI** | Account `sk-HhQF…` + BBS `sk-P42A…` (attivo); API Pi = **openai-completions** |
| **MiniMax ufficiale CN** `https://api.minimaxi.com/anthropic` | Pi `minimax-cn` | Key Token Plan `sk-cp-...` (anche key pubblica forum) |
| **OpenAI Codex OAuth** | Pi `openai-codex`, `openai-codex-2` | Account ChatGPT Plus collegati in `auth.json` |
| **OpenCode / OpenCode-Go** | Pi `opencode`, `opencode-go` | Key in `auth.json` (non è uno dei siti nella tabella) |
| **OAuth gratuiti** | Pi | GitHub Copilot, Google Gemini/Antigravity, Qwen portal, Cline, Kilo (extension `custom-free-models`) |

---

## 4. Pi — configurazione completa

**Directory:** `~/.pi/agent/`

| File | Contenuto |
|------|-----------|
| `settings.json` | Default provider/model, `enabledModels`, extension `packages` |
| `models.json` | Provider custom (URL, modelli, `authHeader`, headers) |
| `auth.json` | API key e OAuth per provider |

### 4.1 Default Pi (2026-06-09)

```json
"defaultProvider": "xiaomi-cn-scadenza-10giugno",
"defaultModel": "mimo-v2.5"
```

Comando rapido:

```bash
pi                                    # MiMo V2.5 (default)
pi --provider xiaomi-sgp-scadenza-10giugno --model mimo-v2.5    # MiMo via SGP
pi --provider claude-routerpark --model claude-sonnet-4-6    # tuo account RouterPark
pi --provider claude-routerpark-bbs --model claude-sonnet-4-6   # key giveaway BBS
pi --model claude-routerpark/claude-opus-4-8
```

### 4.2 Provider in `models.json` (relay a pagamento / custom)

| Provider ID | Base URL | API | Modelli principali | In `auth.json` |
|-------------|----------|-----|-------------------|----------------|
| `openai-anbalu` | `https://api.anbalu.top/v1` | openai-responses | gpt-5.5, gpt-5.4, gpt-5.3-codex, … | Key in `models.json` |
| `openai-zjapi` | `https://zjapi.com/v1` | openai-responses | gpt-5.4-mini, gpt-5.3-codex | Key in `models.json` |
| `openai-freemodel` | `https://api.freemodel.dev` | openai-responses | gpt-5.5, gpt-5.4, gpt-5.3-codex, … | Key in `models.json` |
| `bluesminds` | `https://api.bluesminds.com/v1` | openai-completions | qwen3.6-plus, qwen3.6-max-preview, glm-5.1 | Key in `models.json` |
| `52model` | `https://52mx.net/v1` | openai-responses | gpt-5.3-codex | Key in `models.json` |
| `xiaomi-sgp-scadenza-10giugno` | `https://token-plan-sgp.xiaomimimo.com/v1` | openai-completions | MiMo V2.5, V2.5 Pro, V2 Pro, V2 Omni | ✅ `tp-s94z…` (scadenza 10/06) |
| `xiaomi-cn-scadenza-10giugno` | `https://token-plan-cn.xiaomimimo.com/v1` | openai-completions | MiMo V2.5, V2.5 Pro, V2 Pro, V2 Omni | ✅ key CN (scadenza 10/06) |
| `claude-routerpark` | `https://routerpark.com/v1` | **openai-completions** | claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5-… | ✅ account `sk-HhQF…` |
| `claude-routerpark-bbs` | `https://routerpark.com/v1` | **openai-completions** | stessi modelli (label · BBS) | ✅ giveaway `sk-P42A…` (attivo CLI) |
| `minimax-iamhc` | `https://api.iamhc.cn` | anthropic-messages | **MiniMax-M3** | ✅ `sk-41Ek…` |
| `minimax-cn` | `https://api.minimaxi.com/anthropic` | anthropic-messages | MiniMax-M3 | ✅ `sk-cp-…` |
| `grok2api-local` | `http://127.0.0.1:8000/v1` | openai-completions | grok-4.3-console, grok-4.20-multi-agent-xhigh, … | ✅ `grok-local-…` |

**Comandi Grok (Pi):**

```bash
pi --provider grok2api-local --model grok-4.3-console --print "ok"
pi --provider grok2api-local --model grok-4.20-multi-agent-xhigh
```

Deploy e import SSO: vedi `linux-do-explorer/GROK2API-DEPLOY.md`.

### 4.3 Provider via extension (non in `models.json`)

| Provider | Extension | Endpoint |
|----------|-----------|----------|
| `claude-freemodel` | `claude-code-multi-account` | `https://cc.freemodel.dev` |
| `minimax` (international) | `custom-free-models` *(disattivato)* | `api.minimax.io` |
| ~~`kilo-free`, `nvidia-free`, `ollama-free`~~ | ~~`custom-free-models`~~ | **rimossi da Pi** (2026-06-03) |
| `cline-free` | `custom-free-models` *(disattivato)* | opzionale se riattivi extension |

**Comandi extension Claude:**

```text
/claude-list
/claude-use claude-freemodel
/claude-use claude-routerpark        # account (Anthropic URL per Claude Code)
/claude-use claude-routerpark-bbs    # key BBS giveaway
```

**Nota Pi vs Claude Code:** in Pi i provider RouterPark usano `openai-completions` su `/v1/chat/completions` (streaming stabile). L’extension `/claude-use` scrive ancora `ANTHROPIC_BASE_URL=https://routerpark.com` per il CLI `claude` esterno.

### 4.4 OAuth in Pi (`auth.json`)

| Slot | Tipo | Uso |
|------|------|-----|
| `openai-codex` | OAuth ChatGPT | Codex ufficiale slot 1 |
| `openai-codex-2` | OAuth ChatGPT | Secondo account; sync da `~/.codex/auth.json` |
| `github-copilot` | OAuth | Copilot |
| `google-gemini-cli` / `google-antigravity` | OAuth | Gemini |
| `qwen-oauth` / `qwen-oauth-2` | OAuth | Qwen portal |
| `cline-free` | OAuth | Solo se `custom-free-models` è riattivato in Pi |

### 4.5 Extension caricate (`settings.json` → `packages`)

- `pi-qwen-oauth`, `pi-context-saver`, `context-guard-wrapper`
- `pi-dcp`, `codex-multi-account` *(no `custom-free-models` — free tier disattivato)*
- `claude-code-multi-account`, `@ramarivera/pi-grok-build`

---

## 5. Claude Code — profili multi-relay

### 5.1 File di configurazione

| File | Ruolo |
|------|--------|
| `~/.claude/settings.json` | **Config attiva** usata da `claude` CLI |
| `~/.claude/profiles.json` | **Catalogo** di tutti i profili disponibili (sorgente di verità) |
| `~/.pi/agent/extensions/claude-code-multi-account/index.ts` | Definizione profili + comandi `/claude-*` in Pi |

### 5.2 Profilo attivo (2026-06-06)

**`claude-routerpark-bbs`** — key cpass giveaway del post RouterPark.

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme",
    "ANTHROPIC_BASE_URL": "https://routerpark.com",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  },
  "model": "claude-sonnet-4-6"
}
```

| Aspetto | Valore |
|---------|--------|
| Relay attivo | **RouterPark BBS** (cpass whitedream, 0.2x, quota condivisa) |
| Saldo stimato | ~18.5M token (da risposta API) |
| Modelli validi | `claude-sonnet-4-6`, `claude-opus-4-8`, `claude-haiku-4-5-20251001` |
| ❌ Non usare | `sonnet`, `haiku`, `opus` (alias corti → 503 su RouterPark) |

### 5.3 Tutti i profili disponibili

| Profilo | Relay | Key | Modello default | Switch |
|---------|-------|-----|-----------------|--------|
| `claude-routerpark-bbs` | RouterPark BBS | `sk-P42A...` | `claude-sonnet-4-6` | **ATTIVO** |
| `claude-routerpark` | RouterPark account | `sk-HhQF...` | `claude-sonnet-4-6` | `/claude-external claude-routerpark` |
| `claude-freemodel` | FreeModel | `fe_oa_...` | `sonnet` | `/claude-external claude-freemodel` |

Ogni profilo ha la config completa in `~/.claude/profiles.json` → `profiles.<nome>.settings`.

### 5.4 Comandi switch (da Pi)

```text
/claude-list                              # elenca profili + segna quello attivo
/claude-external claude-routerpark-bbs    # attiva BBS (default)
/claude-external claude-routerpark        # passa all'account personale
/claude-external claude-freemodel         # torna a FreeModel
/claude claude-routerpark-bbs             # switch + avvia claude CLI
```

Dopo `/claude-external <nome>`, lancia `claude` in un altro terminale.

### 5.5 Note tecniche

- RouterPark in **Pi** usa `openai-completions` su `/v1/chat/completions` (più stabile in TUI).
- RouterPark in **Claude Code CLI** usa endpoint Anthropic su `https://routerpark.com` + `ANTHROPIC_AUTH_TOKEN`.
- FreeModel usa `apiKeyHelper` + alias corti (`sonnet`, `opus`) — funzionano solo su `cc.freemodel.dev`.

---

## 6. Codex — `~/.codex/config.toml`

```toml
model_provider = "OpenAI"
model = "gpt-5.5"
base_url = "https://api.anbalu.top/v1"
```

| Aspetto | Valore |
|---------|--------|
| Relay attivo | **Anbalu** |
| Key | `~/.codex/auth.json` → `OPENAI_API_KEY` (Anbalu) |
| Backup precedente | `config.toml.bk` usava **ZjAPI** `https://zjapi.com/v1` |

**Non configurato su VPS:** relay Codex del post RouterPark (`https://v2api.top/`, whitedream, `sub.ranai.chat`).

Script sync Codex OAuth → Pi: `~/.pi/agent/bin/sync-codex-to-pi-slot.sh`

---

## 7. MiniMax — tre canali

| Canale | Endpoint | Modello | Stato |
|--------|----------|---------|--------|
| **Ufficiale CN Token Plan** | `https://api.minimaxi.com/anthropic` | `MiniMax-M3` (non `MiniMax-M3.0`) | ✅ Pi `minimax-cn` |
| **iamhc relay** | `https://api.iamhc.cn` | `MiniMax-M3` | ✅ Pi `minimax-iamhc` (~$5/M) |
| **Forum RouterPark** | stessa key `sk-cp-...` | M2.7 nel post, M3 in test | Key pubblica; quota condivisa |

Quota Token Plan (endpoint ufficiale):

```bash
curl -s https://api.minimaxi.com/v1/token_plan/remains \
  -H "Authorization: Bearer <sk-cp-...>"
```

**iamhc** (stessa account console): supporta anche `qwen3.6-plus`, altri modelli via `/v1/chat/completions` e `/v1/messages`.

---

## 8. RouterPark — account, BBS e fix Pi (2026-06-02)

### 8.1 Due provider Pi

| Provider | Key | Origine | `auth.json` |
|----------|-----|---------|-------------|
| `claude-routerpark` | `ENC:VvyOW27c0XEbMKHtbLqkIUw1nZQpJNqf+lWJwmyGFE9z4eFqa+DVUyQApvo2pIZBVx+O` | Console RouterPark (account **Emanuele Mastronardi**, check-in ~$40) | ✅ |
| `claude-routerpark-bbs` | `ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme` | Post BBS giveaway cpass (2026-06-05) — **attivo anche in Claude CLI** | ✅ |

Env: `ROUTERPARK_API_KEY` + `ROUTERPARK_BBS_API_KEY` in `~/.bashrc`.

### 8.2 Fix TUI Pi (risposta vuota)

RouterPark con `anthropic-messages` + `stream:true` a volte risponde in **JSON** invece che **SSE** → Pi mostrava `content: []` senza errore.

**Soluzione:** entrambi i provider in `models.json` usano `api: openai-completions` e `baseUrl: https://routerpark.com/v1`.

### 8.3 Post BBS originali (2026-06-02)

| Offerta post | Key / URL | Test | Config VPS |
|--------------|-----------|------|------------|
| MiniMax | `sk-cp-...` + `api.minimaxi.com/anthropic` | ✅ API + Pi | `minimax-cn` |
| Claude cpass (2026-06-05) | `sk-P42A...` + `routerpark.com` | ✅ Pi + Claude CLI; alias `haiku` → 503 | `claude-routerpark-bbs` |
| Codex v2api | `sk-Clt5...` + `v2api.top` | Non testato | ❌ |

### 8.4 Post BBS 六一福利 — aicodelink (2026-06-02, sera)

Sponsor **aicodelink** ([aicodelink.top](https://aicodelink.top)) + commento OP **ranai Codex**:

| Relay | URL | Key nel post | Test 2026-06-02 |
|-------|-----|--------------|-----------------|
| aicodelink | `https://aicodelink.top/v1` | `ENC:VvyOW3T+2FBQMZ/RMZGgLlE3vfRabPbYx1rU1WOxXEUX3dVhSMmgMwQRrpkRm4kBRSeV` | ❌ `Invalid token` |
| ranai | `https://sub.ranai.chat/v1` | `ENC:VvyOdjO18jZQYNiYb5KPGDFCoqMNPrOZ3B/alQuQXCRH8ZYrY+v2N1Q0iJ1mxdpNYBfy91w54JraGN/FWsVbIhD0kQ==` | ❌ `INVALID_API_KEY` |

Non configurati su VPS. Per provare: registrazione su aicodelink ($1 test citato nel post) e key personale dalla console.

### 8.5 Modelli e alias

- ✅ Usare ID completi: `claude-sonnet-4-6`, `claude-opus-4-8`, `claude-haiku-4-5-20251001`
- ❌ `haiku` / `sonnet` corti → spesso 503 su endpoint Anthropic
- Header consigliato: `User-Agent: claude-cli/2.1.159`

---

## 9. Cosa usiamo vs cosa no (riepilogo)

### ✅ Usiamo (configurato + usato)

- **Pi:** minimax-cn (default), RouterPark account + BBS, iamhc MiniMax-M3, Anbalu, ZjAPI, FreeModel, 52mx, Bluesminds, **grok2api-local**, OAuth Codex/Qwen/Copilot/Gemini
- **Claude Code:** FreeModel
- **Codex:** Anbalu

### 🟡 Abbiamo account / chiavi ma non integrati (o solo parziale)

- **MicuAPI** — login GitHub; nessun provider Pi
- **RKAPI** — login console; nessun provider Pi
- **api520.pro** — login; nessun provider Pi

### ❌ Non usiamo sul VPS (anche se nel post o in guide)

- RouterPark **Codex** (`v2api.top`, whitedream keys)
- **aicodelink** / **sub.ranai.chat** — key post 六一福利 scadute/invalid
- Relay Claude **whitedream** / **bytecatcode** del post
- **Micu** come endpoint (solo citato in `MEGA-SUNTO.md` / HelpAIO)

---

## 10. Lavoro svolto (cronologia)

1. Mappatura stack vs post RouterPark BBS (Claude/Codex/MiniMax).
2. Account RouterPark personale + API key dashboard (`sk-HhQF…`).
3. Due provider Pi: **`claude-routerpark`** (account) e **`claude-routerpark-bbs`** (giveaway).
4. Fix Pi TUI: `anthropic-messages` → **`openai-completions`** su `routerpark.com/v1`.
5. Test post **aicodelink** / **ranai** — key pubbliche non funzionanti.
6. Config **`minimax-iamhc`**, **`minimax-cn`**, test `token_plan/remains`.
7. Deploy **grok2api** (fork jiujiu532, stack WARP), import 150 SSO, provider Pi **`grok2api-local`**.

---

## 11. Comandi utili

```bash
# Pi — lista modelli per provider
pi --list-models claude-routerpark
pi --list-models claude-routerpark-bbs
pi --list-models minimax-iamhc

# Test rapido RouterPark (openai-completions)
pi --provider claude-routerpark --model claude-sonnet-4-6 --print "ok"
pi --provider claude-routerpark-bbs --model claude-sonnet-4-6 --print "ok"
pi --provider minimax-iamhc --model MiniMax-M3 --print "ok"

# Claude Code (config attuale FreeModel)
claude -p "ok"

# Codex (config attuale Anbalu)
codex -p "ok"

# Grok locale (grok2api)
pi --provider grok2api-local --model grok-4.3-console --print "ok"
docker-compose -f ~/grok2api/docker-compose.warp.yml ps
```

---

## 12. File da toccare per cambiare relay

| Obiettivo | File |
|-----------|------|
| Default Pi | `~/.pi/agent/settings.json` |
| Nuovo provider Pi | `~/.pi/agent/models.json` + `auth.json` |
| Claude Code | `~/.claude/settings.json` |
| Codex | `~/.codex/config.toml` + `~/.codex/auth.json` |
| Profili Claude in Pi | `~/.pi/agent/extensions/claude-code-multi-account/index.ts` |
| Grok self-hosted | `~/grok2api/data/config.toml` + `linux-do-explorer/GROK2API-DEPLOY.md` |

---

## 13. Credenziali e chiavi API (completo)

Tutto ciò che è salvato su questo VPS al 2026-06-02. Per siti 🟡 senza riga API: generare la key dalla console con i login sotto.

### 13.1 Login console (account web)

| Sito | URL | Utente / metodo | Password |
|------|-----|-----------------|----------|
| MicuAPI | https://www.micuapi.ai/ | GitHub **manumastro** | (OAuth GitHub) |
| ZjAPI | https://zjapi.com/ | **manustrong1212** | `ENC:aPbNZjS9pzZSZw==` |
| Anbalu | https://app.anbalu.top/ | **emanuele.mastronardi.2002.12@gmail.com** | `ENC:aPbNZjS9pzZSZw==` |
| RKAPI | https://rkapi.com/console/personal | **manustrong** | `ENC:aPbNZjS9pzZSZw==` |
| FreeModel | https://freemodel.dev/dashboard | **emanuele.mastronardi.2002.12@gmail.com** | (login email; API key sotto) |
| Bluesminds | https://api.bluesminds.com/ | GitHub | (OAuth GitHub) |
| 52mx | https://52mx.net/console | **manumastro** | `ENC:aPbNZjS9pzZSZw==` |
| api520 | https://api520.pro/ | **trapbeats1212@gmail.com** | `ENC:aPbNZjS9pzZSZw==` |
| iamhc | https://api.iamhc.cn/console | **trapbeats1212@gmail.com** | `ENC:aPbNZjS9pzZSZw==` |

### 13.2 API key relay — Pi `~/.pi/agent/models.json`

| Provider | Base URL | API Key |
|----------|----------|---------|
| `openai-anbalu` | `https://api.anbalu.top/v1` | `ENC:VvyOdmDoomFXbdqRPcPcTDUVoaVXareciRzfwgrKXSNBpZZ3M7nxM1pkip86xdxKNhOh9V4+4J+MT9mRAcMKckD0wg==` |
| `openai-zjapi` | `https://zjapi.com/v1` | `ENC:VvyOcX/B020SYJH/BpbYMFYl/P8lKueSiErNkw6zWGRo3M0kM8/uV1ob3cRpu91KSwiV` |
| `openai-freemodel` | `https://api.freemodel.dev` | `ENC:Q/L8fGfSpTxVbd+aa8zZTTVH/PVZP7WS2UiOlF3LXCBGrsAmPu7zPVM0i547kdpKNhKg8F8+` |
| `bluesminds` | `https://api.bluesminds.com/v1` | `ENC:VvyOa0L82047FNDYLb2NFEVElK4EBLXry0mIz16fGi5J/MxZPsncaRoviPwVhJgKUwKv` |
| `52model` | `https://52mx.net/v1` | `ENC:VvyOcla/+0YVJtnNOY6sEjIooKoNM+HA0UTj0A2dFFJg0/pSP++jSjkS2tEbuZIKchq3` |

In `models.json` i provider sotto usano placeholder; la key reale è in `auth.json`:

| Provider | Placeholder in models.json | Key in `auth.json` |
|----------|---------------------------|-------------------|
| `claude-routerpark` | `$ROUTERPARK_API_KEY` | `ENC:VvyOW27c0XEbMKHtbLqkIUw1nZQpJNqf+lWJwmyGFE9z4eFqa+DVUyQApvo2pIZBVx+O` |
| `claude-routerpark-bbs` | `$ROUTERPARK_BBS_API_KEY` | `ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme` |
| `minimax-iamhc` | `$MINIMAX_IAMHC_API_KEY` | `ENC:VvyOJzfI/FFVEKznNJ+pCVgQlp8dZbbC1nvf5GqHWVBf8dZYfP/ibzAe3fs0pIE/UQOD` |
| `minimax-cn` | `$MINIMAX_CN_API_KEY` | `ENC:VvyOcHago1YVbJPwL62kGmweiYQ9Zfbmimv4xFqIV0EQ5dAgZ9jAZhkXpv0InLUtcCeUnQk0xe6LbuTlWqZXURzPjn1V5dpzVBiAwBWMq0t0FKLwGjzl5JJj3eV/hhlmQsD1Y3bHwzUqI7bbKMSyPnsutZQDb+aY8XTUkVY=` |
| `grok2api-local` | `$GROK2API_API_KEY` | `ENC:QuXMeCvh+GcCOcTNb5bZHzMTpfJWa7TOiRWKx1yXCCQc9JZ3P+jxMFBh3w==` |

### 13.3 API key — Pi `~/.pi/agent/auth.json` (altri provider)

| Provider | Key |
|----------|-----|
| `opencode` | `ENC:VvyOXXD73D0iN4TIKbytHzI7jbAtDLbjyUnD+067HWMS2OJXR8PZdCQdg+4Rpb8YNT+D8Qg/x+zqQP6UcbojdmCnzQ==` |
| `opencode-go` | `ENC:VvyOXXD73D0iN4TIKbytHzI7jbAtDLbjyUnD+067HWMS2OJXR8PZdCQdg+4Rpb8YNT+D8Qg/x+zqQP6UcbojdmCnzQ==` |

### 13.4 Claude Code — profili (`~/.claude/`)

**Attivo:** `claude-routerpark-bbs` in `settings.json`

| Campo | Valore |
|-------|--------|
| `ANTHROPIC_BASE_URL` | `https://routerpark.com` |
| `ANTHROPIC_AUTH_TOKEN` | `ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme` |
| Modello | `claude-sonnet-4-6` |

**Catalogo completo:** `~/.claude/profiles.json` (contiene anche FreeModel e RouterPark account).

Env manuale equivalente (profilo attivo):

```bash
export ANTHROPIC_BASE_URL="https://routerpark.com"
export ANTHROPIC_AUTH_TOKEN="ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme"
# Non impostare ANTHROPIC_API_KEY insieme al token — Claude CLI segnala conflitto auth
```

Profilo FreeModel (in catalogo, non attivo):

```bash
export ANTHROPIC_BASE_URL="https://cc.freemodel.dev"
export ANTHROPIC_API_KEY="ENC:Q/L8fGfSpTxVbd+aa8zZTTVH/PVZP7WS2UiOlF3LXCBGrsAmPu7zPVM0i547kdpKNhKg8F8+"
```

### 13.5 Codex — `~/.codex/`

| File | Campo | Valore |
|------|-------|--------|
| `config.toml` | `base_url` | `https://api.anbalu.top/v1` |
| `config.toml` | `model` | `gpt-5.5` |
| `auth.json` | `OPENAI_API_KEY` | `ENC:VvyOK2W5rmVRYNibbsePGjBC9fFZO7Sehh2IwF+RCiYdp8FxNrqkYVY22Z8+x4hIYxSl9Ag455qNS4/FCZAKIxanwA==` |

**Nota:** la key Codex Anbalu (`sk-8c49…`) è **diversa** dalla key Pi Anbalu (`sk-efe5…`) — due token sullo stesso relay.

Backup `config.toml.bk`: relay **ZjAPI** `https://zjapi.com/v1`, modello `gpt-5.4-mini` (senza key nel file bk).

### 13.6 Extension Claude — `~/.pi/agent/extensions/claude-code-multi-account/index.ts`

| Profilo | Base URL | API Key | Header auth |
|---------|----------|---------|-------------|
| `claude-freemodel` | `https://cc.freemodel.dev` | `ENC:Q/L8fGfSpTxVbd+aa8zZTTVH/PVZP7WS2UiOlF3LXCBGrsAmPu7zPVM0i547kdpKNhKg8F8+` | `ANTHROPIC_API_KEY` |
| `claude-routerpark` | `https://routerpark.com` | `ENC:VvyOW27c0XEbMKHtbLqkIUw1nZQpJNqf+lWJwmyGFE9z4eFqa+DVUyQApvo2pIZBVx+O` | `ANTHROPIC_AUTH_TOKEN` |
| `claude-routerpark-bbs` | `https://routerpark.com` | `ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme` | `ANTHROPIC_AUTH_TOKEN` |

RouterPark in Pi (`models.json`) usa **openai-completions**; l’extension Claude Code usa Anthropic URL + header:

```
User-Agent: claude-cli/2.1.159
```

### 13.7 Variabili ambiente — `~/.bashrc`

| Variabile | Valore | Uso |
|-----------|--------|-----|
| `OPENCODE_API_KEY` | `ENC:VvyOeWTc21RUI7HwZ7qpIEYypqECaPDJ/V3UyV64CG93wtRyMcPRQwcgnJ1szYIxbCSJlSs06MOGRu/NboIrdnPH1g==` | OpenCode CLI (≠ key in `auth.json` opencode) |
| `OPENROUTER_API_KEY` | `ENC:VvyOfHSg4TVON96Qb5bbGGVF/PNfaLqf3EnZkAGUWHJBoZomY72mN1Q0i5hqx90bMxPx9ghuss+KFN+WAJcKJhSukSMwuKM1Vw==` | OpenRouter |
| `ROUTERPARK_API_KEY` | `ENC:VvyOW27c0XEbMKHtbLqkIUw1nZQpJNqf+lWJwmyGFE9z4eFqa+DVUyQApvo2pIZBVx+O` | Pi `claude-routerpark` |
| `ROUTERPARK_BBS_API_KEY` | `ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme` | Pi `claude-routerpark-bbs` + **Claude CLI attivo** |
| `GROK2API_API_KEY` | `ENC:QuXMeCvh+GcCOcTNb5bZHzMTpfJWa7TOiRWKx1yXCCQc9JZ3P+jxMFBh3w==` | Pi `grok2api-local` + curl verso `127.0.0.1:8000` |
| `MINIMAX_API_KEY` | JWT `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.ENC:QO7pW2XgrjUAENzBPaO/EE4YjoEMCsTf23rt0mOhLFl8z+0jZeCucToNo8I+p6MKSB2SvTQFyOXmeorNcJgBfnfAkntk48FoARK8zgujrANlOY6xDDDE0+Vq0Mh1sSRVfKXtZWLaojQqP4bAFp2dEFRCkq4PMNTA22jX5HCYAX5ow8hpSNn0NC0/oNMSjrtLTyWJvyMJ15nwbvLScJ4seEelln9P5/htKjyewA3HoA9lKYaNPB7LnPZH/pR0iDska9P6akv32jQtAbCcEp6jTE8Lha4iHsj75nrfzW2fKGN/xOolT+Tedyo+2ME+o50QThiOqwwKxN/beu3SY6FbY3zP7SNl4K5xOg2jwj6n3gBMNYW+IjfH0+5q39VgpQJkafrtZWTe3ncqPqfQBaOsSVsnlrcMCtfD8ETy2HS2JyZpw+ZrStnSfSoRrJsQnqtNThuF9Sc09cPpaoLTY6VbQkDP4X9P5/g0Lxaj2TzHpxBOGI6zDwq32t16/ZVwnF4=.uQNurkOsZCFUv97ufB3m_DNFMfs7xlBefTrElQ_fQKmvM5cHm0-nCPTaQ0NgFzC7i4A-kXZ0x3VHyIjn6hv3fpWclyx85JWlhNM9H5Mn8NAkQA-vdswAcrG-NmODroIpWLnuVF3pSB_XeqWOsCmKkQNWlU_jVVzYNl7DSxP-Vv1MeroLcY6jmGs3tPMpXXGtNigiHVbp51JAx_L-qgDzulkvUs3bnXKiMDMZfmWvsZ94EsKyxQStmsrxb1ewUSXKUi7jtB03RK6fgE8R4x23sc0Q6_s_i2Nr142VRasNfgDFzKf3cx4Uo8-vb5bU0B5sL0H4erAJinI2cf_rEJzs0Q` | MiniMax internazionale (`api.minimax.io`, extension) |
| `NVIDIA_API_KEY` | `ENC:S+HCY2+g3XEEOoORZryZAzEYifJfKO/46GeMlWuXN19T5+94YtLGcCoWm58s2aMWbkb08whwxM+NeInIQIErWWfx81lSwg==` | NVIDIA free tier Pi |
| `MODAL_API_KEY` | `ENC:SPjHcmr/8ncGNJvKN6vZHGQiqqI7DM7i73vL+Wi5Olhnz+ZxNL7WMDYx2P0Gm64rSAKGpCtq0+eL` | Modal |
| `OLLAMA_API_KEY` | `ENC:QfWXImK09jwAZtyea8KOTThJ9PZXbbLJjRWCw1+UDHIL381SdP72aS0fmPltjNsQez+woTllzdOG` | Ollama cloud |

`GOOGLE_API_KEY`: commentato in `.bashrc` (“moved to bashrc_env”) — **non presente** in `~/.bashrc_env` al momento.

### 13.8 OAuth Pi — `~/.pi/agent/auth.json` (token completi)

Account collegati via OAuth (refresh + access). Scadenze in millisecondi nel JSON.

<details>
<summary><strong>github-copilot</strong></summary>

- **refresh:** `ENC:Qv/WTD+902JXML/GOqbfSFMDqv8dOLbG2GX392vHXFl/4pJ0aMv0Uw==`
- **access:** (cookie Copilot lungo — vedi file `auth.json` riga `github-copilot.access`)
- **expires:** `1778917131000`

</details>

<details>
<summary><strong>google-antigravity</strong></summary>

- **refresh:** `ENC:FLiMIzXewGMaCrHjJp6wSkIWnY4vD8Pr+Gz28neFKDppruphQuTRMRMmn54YxJoQajKwki0et9DYQ/rPaZkELhLZwWBJz+5pM2yi+hy+iU1CSLOuGh+z+/VH/s5mqyMuUdv7V2fF+A==`
- **access:** `ENC:XPaRKijsp0UCYqTwNoSPA0wpp5EHLu7z3EP1mWyANHVOwNZ0SsnkNTNh3NoWhNw6MkHwiCFsyf7LT9iXfLYZfGDc5Vtq/qBcNiyu3CjEizBoOb6tFhrt2cZL8ekLkT51EODhJFP32TNXL6ibDp6PNkU1tJIPCLri0Rr5/gmTDVFS+u1BPuH+QlYQpOUpjaUMWQGX9SY4+OjYXozIcsAnZhPC2kdCzqVqAASt7zaAhjczSbSOHGTWxepF6IxQpC90ZOPNQUTp4jUuOabbbrmdN0gjvbYJPMHN5mb68g2hL0VoxOVCTsrPNi48s/MHx90NczOcpgonxJ7PHNflXbQ6RhWlkiA=`
- **projectId:** `snappy-oasis-2jgzv`

</details>

<details>
<summary><strong>google-gemini-cli</strong></summary>

- **refresh:** `ENC:FLiMIzX6wEohIZ/MZ6yoVEIWnY4vD8Pr+Gz28neFKDppruphQLzxfFs4oftps9k2Tjuvnyxq+tjbX/2Wbb8YVmre1ndU+PpxAmKx/i2e3TFpPYKsOTaxxvl+4stSiwFHY8KWX0fJow==`
- **access:** `ENC:XPaRKijsp0UCYqTwNpvZTDlIso0lGbSf6hz2zUuWHVBwuvdHbuP1ZRZghPEzh440RB6znVcn4P70eMPvFKIAbV+hxEB0ueBbJBe46yrGqE5NLqmQO2ndxe1Y9/FjqAx7btLoJXX6+mYpEr7ocsOnOHYjhrNeHtvY7GjBz1ujAlQX4fpHaO+mZiIRod0Qq6APUFyViSsZ0vzRSe/2a4ZeQWzP92RkxPlSJyGx3yWsmihXFZKgGRvJ+PdG4ZRxnyxlQePzdzPC3lM7ZN7dMI2wKnMhg4YZPMHN5mb69mihL0VoxOVCTsrPNi483PM9od0qMxOv6iI125r9as7EQYEhRhWlkiA=`
- **projectId:** `snappy-oasis-2jgzv`

</details>

<details>
<summary><strong>qwen-oauth</strong></summary>

- **refresh:** `ENC:V670aSvV53IPOa7LCKOyKUQShqUPFMXB8mqO7UHENnhw3I57dbnzfDEhpcI7taINZjaurzkfuv/Pe5aTXr42Il2n00s+6aZiLw+oyzGlqAxMRIP3IQw=`
- **access:** `VUmaxJ-Tr6_Jbw-4MOLuMdZaRav9iOOQF3sCfljC-rCsD2i3k78bnqMtmJ5AcKqnVUm1QqWKiPlRhKW0b_iRmQ`
- **enterpriseUrl:** `portal.qwen.ai`

</details>

<details>
<summary><strong>qwen-oauth-2</strong></summary>

- **refresh:** `ENC:Fd7ZUnC9rkUABaTsPI2oMmgCt/ADF/XbjBTu41O7P0VL+fZ0SePva1YssJAOuqQmQDzymAMwxtPsesnxbMRdVlW693w39eZdUAexzCawg0osKbHyVgw=`
- **access:** `BlzIWGyNeWkPda24t93TIb-ARFdHBCgccOrsuNvlioOSMsUr_QjM5j-OB-FfIOkL2Hwo4PFRlIWeg1fSO4_4EQ`

</details>

<details>
<summary><strong>kilo-free</strong> (non usato in Pi dal 2026-06-03)</summary>

- Extension `custom-free-models` disattivata; token eventualmente ancora in `auth.json` ma provider non caricato.
- **refresh / access** (JWT Kilo, stesso token):  
  `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ENC:QO7pf2Tjzm0sPKPePJnTEmUmivcPCrvf9kTMyFjAAmRHpvVpXNXdTjkWoJ8WnqNMWxuGqiAa09Lzev6VdMAjY2vQ8iBIzqZtLT+8mxOgvw5YC6ewNDDExuV57pN2oSdkbPrlZGfbxXICZ7/cCrO8DmI2kr4nN/Lf23rD0nWxJCV/z+lpZ9qucSo/htMTt6ASWymetzdv1OjbdenObJ84b0HA9WliyNlyORK8wBCdoC9UNPGMIgvA4+to/sh1sSRnfM/yeknn0jctL7DeEKCvSk81p7QnMNSe3G7yl3SmBW1o7cAgS9n0NC1m2Q==.mjVDCe6YujtVFgvhrCSvfc-H4mNrxpLl3t7poaSKC3A`

</details>

<details>
<summary><strong>cline-free</strong></summary>

- **refresh:** `ENC:fcXrXkjB/XELMrzDDJ+eITUA86scOtXk9A==`
- **access** (JWT WorkOS/Cline): vedi `auth.json` → `cline-free.access` (email `emanuele.mastronardi.2002.12@gmail.com`)

</details>

<details>
<summary><strong>openai-codex</strong> (ChatGPT Plus #1)</summary>

- **email:** `trapbeats1212@gmail.com`
- **accountId:** `ENC:EaSWd2Tu8WBOZNzLZ9neHDgU6f5XbrKHjEjZkAHLDSMT8ccj`
- **refresh:** `ENC:V+P8TFDB0jESHLDPENm7AFgwqok8Gsry+WfUkWukV2diz5U+d+ngMw8bmOIbvcQTSxaLoAtu+NjvWfXLWJEpQEvw1X1B66FgNxai0xClrR1sF7y3WhHs/tlK`
- **access** (JWT): vedi `auth.json` → `openai-codex.access` (lungo)

</details>

<details>
<summary><strong>openai-codex-2</strong> (ChatGPT Plus #2)</summary>

- **email:** `oefombph108@hotmail.com`
- **accountId:** `ENC:FvaUdTC682FOYtzMatneSGBF6aZfaOeHhh6OlF/KCycSopEq`
- **refresh:** `rt_zQzWCeUSizyjQlsP8YecJxbrprhaT8aROJgJJ7UNEzc.HAwXxyZD8cGqzVw8XMjupHQYRmJ1WA-OD1qBKy8doxs`
- **access** (JWT): vedi `auth.json` → `openai-codex-2.access`

</details>

Per i JWT OAuth molto lunghi (Copilot, Codex, Cline), il file sorgente canonico è sempre:

```text
/home/manu/.pi/agent/auth.json
```

### 13.9 Chiavi RouterPark e post BBS

| Offerta | Endpoint | Key | Provider Pi |
|---------|----------|-----|-------------|
| **Account RouterPark** | `routerpark.com/v1` | `ENC:VvyOW27c0XEbMKHtbLqkIUw1nZQpJNqf+lWJwmyGFE9z4eFqa+DVUyQApvo2pIZBVx+O` | ✅ `claude-routerpark` |
| Claude cpass (giveaway 2026-06-05) | `routerpark.com/v1` | `ENC:VvyOQzK/1mYPG4jYOISsHVc7kJAEOe+e8UvJwnS4I3ZQ8ft0Td6uRShnsJotjoI6czme` | ✅ `claude-routerpark-bbs` + Claude CLI |
| MiniMax (post) | `api.minimaxi.com/anthropic` | `ENC:VvyOcHago1YVbJPwL62kGmweiYQ9Zfbmimv4xFqIV0EQ5dAgZ9jAZhkXpv0InLUtcCeUnQk0xe6LbuTlWqZXURzPjn1V5dpzVBiAwBWMq0t0FKLwGjzl5JJj3eV/hhlmQsD1Y3bHwzUqI7bbKMSyPnsutZQDb+aY8XTUkVY=` | ✅ `minimax-cn` |
| Codex v2api (post) | `https://v2api.top/` | `sk-Clt5…` (nel thread) | ❌ |
| aicodelink (post 六一) | `https://aicodelink.top/v1` | `ENC:VvyOW3T+2FBQMZ/RMZGgLlE3vfRabPbYx1rU1WOxXEUX3dVhSMmgMwQRrpkRm4kBRSeV` | ❌ invalid |
| ranai Codex (commento OP) | `https://sub.ranai.chat/v1` | `ENC:VvyOdjO18jZQYNiYb5KPGDFCoqMNPrOZ3B/alQuQXCRH8ZYrY+v2N1Q0iJ1mxdpNYBfy91w54JraGN/FWsVbIhD0kQ==` | ❌ invalid |

### 13.10 Siti senza API key sul VPS

| Sito | Stato |
|------|--------|
| **micuapi.ai** | Solo login GitHub — generare key in dashboard |
| **rkapi.com** | Solo login **manustrong** — generare key in console |
| **api520.pro** | Solo login **trapbeats1212@gmail.com** — generare key in console |

### 13.11 Test curl rapidi (con le key sopra)

```bash
# Anbalu (Pi key)
curl -s https://api.anbalu.top/v1/models -H "Authorization: Bearer ENC:VvyOdmDoomFXbdqRPcPcTDUVoaVXareciRzfwgrKXSNBpZZ3M7nxM1pkip86xdxKNhOh9V4+4J+MT9mRAcMKckD0wg=="

# RouterPark (come Pi — openai-completions)
curl -s https://routerpark.com/v1/chat/completions \
  -H "Authorization: Bearer ENC:VvyOW27c0XEbMKHtbLqkIUw1nZQpJNqf+lWJwmyGFE9z4eFqa+DVUyQApvo2pIZBVx+O" \
  -H "User-Agent: claude-cli/2.1.159" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-sonnet-4-6","max_tokens":16,"messages":[{"role":"user","content":"ok"}]}'

# MiniMax CN quota
curl -s https://api.minimaxi.com/v1/token_plan/remains \
  -H "Authorization: Bearer ENC:VvyOcHago1YVbJPwL62kGmweiYQ9Zfbmimv4xFqIV0EQ5dAgZ9jAZhkXpv0InLUtcCeUnQk0xe6LbuTlWqZXURzPjn1V5dpzVBiAwBWMq0t0FKLwGjzl5JJj3eV/hhlmQsD1Y3bHwzUqI7bbKMSyPnsutZQDb+aY8XTUkVY="

# iamhc MiniMax-M3
curl -s https://api.iamhc.cn/v1/messages \
  -H "Authorization: Bearer ENC:VvyOJzfI/FFVEKznNJ+pCVgQlp8dZbbC1nvf5GqHWVBf8dZYfP/ibzAe3fs0pIE/UQOD" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","max_tokens":16,"messages":[{"role":"user","content":"ok"}]}'
```

---

## 14. Prossimi passi suggeriti (opzionali)

1. **MicuAPI** — generare API key in console e aggiungere `openai-micu` in `models.json` (top HelpAIO).
2. **RKAPI / api520** — stesso flusso se i prezzi conviene.
3. Allineare **Claude Code** a RouterPark o Micu se FreeModel dà limiti (con modello ID completo, non `haiku`).
4. Ruotare key **pubbliche** se esposte in chat (account RouterPark `sk-HhQF…`); BBS `sk-P42A…` è giveaway condivisa — usare con moderazione.
5. **aicodelink** — solo con key personale da registrazione, non quella del post.
6. Aggiungere **iamhc** provider OpenAI per `qwen3.6-plus` se vuoi un solo billing su quel conto.

---

*Documento generato per il VPS `vmi2825141`. Sezione 13 = inventario credenziali. Aggiornare la data in testa quando si aggiungono provider o si ruotano key.*