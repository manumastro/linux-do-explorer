# 📚 AGENTS.md — Come Esplorare il Mercato Grigio API AI

**Data:** 2026-06-13

---

## ⚠️ REGOLA FONDAMENTALE

> **PRIMA di tutto, consulta sempre le guide in locale nella cartella `/home/manu/linux-do-explorer/`**
>
> 1. Leggi **`VPS-STACK-RELAY.md`** — **sorgente di verità** per stack VPS (Pi, Claude Code, Codex, provider attivi)
> 2. Leggi `MEGA-SUNTO.md` per un riepilogo rapido del mercato relay
> 3. Leggi `relay-services-guide.md` per dettagli completi
> 4. Leggi `recommended-relays.md` per i top pick commerciali
> 5. Leggi `linux-do-navigation-guide.md` per navigare il forum
> 6. Poi, solo se necessario, fai ricerche web aggiuntive

---

## 🔄 Workflow — Aggiornare stack VPS e documentazione

**`VPS-STACK-RELAY.md` comanda.** Ogni modifica a Pi, Claude Code, Codex o relay va propagata in ordine:

### 1. Test e config runtime

```bash
# Verifica endpoint (sostituisci URL, key, modello)
curl -s https://ESEMPIO.xyz/v1/models -H "Authorization: Bearer sk-..."

# Integra in Pi (~/.pi/agent/)
#   models.json   → nuovo provider (baseUrl, api, modelli, key)
#   settings.json → enabledModels
#   auth.json     → solo se usi placeholder $VAR (es. openai-777358)

# Test Pi
pi --provider NOME --model MODELLO --print "ok"
```

### 2. Aggiorna sorgente di verità (locale, gitignored)

Modifica **`VPS-STACK-RELAY.md`**:

- §2 Default attuali
- §3–§4 Provider Pi (`models.json`)
- §5 Claude Code / §6 Codex se cambiano
- §9 Cosa usiamo vs no
- §10 Cronologia (nuova riga)
- §13 Chiavi (se applicabile)

> ⚠️ `VPS-STACK-RELAY.md` **non va in git** (chiavi in chiaro). Resta solo sul VPS.

### 3. Rigenera versione crittografata (committabile)

```bash
cd /home/manu/linux-do-explorer
python3 encrypt_vps_v2.py
# → aggiorna VPS-STACK-RELAY-ENCRYPTED.md
```

### 4. Allinea le guide (stesso commit)

| File | Cosa aggiornare |
|------|-----------------|
| `AGENTS.md` | Stack VPS sintesi + questo workflow |
| `MEGA-SUNTO.md` | § Stack VPS + servizi verificati |
| `recommended-relays.md` | Sezione VPS configurato |
| `relay-services-guide.md` | Tabella provider Pi |
| `linux-do-navigation-guide.md` | Giveaway integrati + flusso |
| `GROK2API-DEPLOY.md` | Se tocca Grok |
| `minimax-setup-instructions.md` | Se tocca MiniMax |
| `relay-monitor-agent-design.md` | Se cambia il processo agente |
| `~/.pi/agent/SPEC.md` | Default provider/model |

### 5. Commit e push

```bash
git add AGENTS.md MEGA-SUNTO.md VPS-STACK-RELAY-ENCRYPTED.md \
  recommended-relays.md relay-services-guide.md linux-do-navigation-guide.md \
  GROK2API-DEPLOY.md minimax-setup-instructions.md relay-monitor-agent-design.md \
  grok-video-relay-guide.md
git commit -m "docs: allinea guide a VPS-STACK-RELAY (provider X)"
git push
```

**Checklist rapida**

- [ ] Relay testato con curl + `pi --print`
- [ ] `VPS-STACK-RELAY.md` aggiornato (locale)
- [ ] `python3 encrypt_vps_v2.py` eseguito
- [ ] Guide allineate (tabella §4)
- [ ] Data `2026-06-09` o corrente nei file toccati
- [ ] Nessun `VPS-STACK-RELAY.md` in `git add`

---

## 📖 Indice

1. [Obiettivo](#obiettivo)
2. [Workflow aggiornamento stack](#-workflow--aggiornare-stack-vps-e-documentazione)
3. [Integrazione Pi (riproduzione ambiente)](#integrazione-pi-riproduzione-ambiente)
4. [Stack VPS attuale](#stack-vps-attuale-sintesi-da-vps-stack-relaymd)
5. [Strumenti Pi da Utilizzare](#strumenti-pi-da-utilizzare)
6. [Come Cercare su Linux.do](#come-cercare-su-linuxdo)
7. [Come Verificare un Relay](#come-verificare-un-relay)
8. [Come Comprare su Taobao](#come-comprare-su-taobao)
9. [Strategia Consigliata](#strategia-consigliata)
10. [Risorse da Monitorare](#risorse-da-monitorare)

---

## Obiettivo

Trovare **relay services (中转站)** affidabili che diano accesso a modelli AI (Claude, GPT, Gemini, Codex) a prezzi economici.

---

## Integrazione Pi — repo unico my-pi

> **Sorgente di verità:** `~/.pi/agent` → [github.com/manumastro/my-pi](https://github.com/manumastro/my-pi)  
> Le guide di questo repo sono copiate in **`my-pi/explorer/`**. Vedi `README-MY-PI.md`.

### Sync reciproco tra ambienti

```bash
bash ~/.pi/agent/scripts/stack-sync.sh push   # condividi modifiche da questo VPS
bash ~/.pi/agent/scripts/stack-sync.sh pull   # allineati agli altri VPS
```

In Pi: `/stack-sync push` · `/stack-sync pull`

### Nuovo VPS

```bash
git clone https://github.com/manumastro/my-pi.git ~/.pi/agent
cd ~/.pi/agent && npm install && bash scripts/stack-sync.sh pull
```

---

## Stack VPS attuale (sintesi da VPS-STACK-RELAY.md)

| App | Default | Endpoint |
|-----|---------|----------|
| **Pi** | `claude-anyrouter` / `claude-haiku-4-5-20251001` | `https://anyrouter.top` |
| **Claude Code** | `claude-haiku-4-5-20251001` | AnyRouter → `https://anyrouter.top` |
| **Codex** | `gpt-5.5` | Anbalu → `https://api.anbalu.top/v1` |
| **Pi (Grok)** | `grok-4.3-console` on demand | `grok2api-local` → `http://127.0.0.1:8000/v1` |

**Giveaway attivi in Pi:** `mimo-cn` (MiMo RouterPark BBS 2026-06-13), `bugteam-linuxdo`, `openai-777358`. **DeepSeek ufficiale:** endpoint pronto, manca key.

**Rimosso da Pi:** `lyclaude` (hotaruapi.com — disattivato 2026-06-09).

Per provider, chiavi, comandi e cronologia: vedi **`VPS-STACK-RELAY.md`** (versione crittografata: `VPS-STACK-RELAY-ENCRYPTED.md`).

---

## Strumenti Pi da Utilizzare

### 🔍 web_search
Ricerca web in tempo reale.

**Query consigliate:**
```
# Su Linux.do
site:linux.do 中转站 推荐
site:linux.do 淘宝 中转 充值
site:linux.do claude codex 中转

# Su GitHub
github relay API 中转 推荐
github CLIProxyAPI OR Sub2API

# Generali
AI relay services taobao 闲鱼
Claude API 中转 便宜 稳定
HelpAIO 中转站 评测
```

**Limiti:**
- A volte errore 429 (troppe richieste) → aspetta e riprova
- I risultati vengono salvati in file sandbox → leggili con `ctx_read_sandbox`

---

### 🌐 browser
Apre e interagisce con pagine web reali.

**Flusso base:**
```
1. open <url>           → Apre la pagina
2. snapshot -i          → Mostra tutti gli elementi con @ref
3. scroll down 5000     → Scorre per vedere altro
4. click @e131          → Clicca su un link/bottone
5. wait 3000            → Aspetta 3 secondi
6. screenshot --full    → Cattura schermata completa
```

**Per navigare Linux.do:**
```
open https://linux.do/c/welfare/36
snapshot -i             # Vedi i topic della categoria
click @e42              # Apri un topic
```

**Per navigare RouterPark:**
```
open https://routerpark.com
snapshot -i             # Vedi la directory
scroll down 5000        # Scendi per vedere i proxy
```

**Problema Cloudflare:**
Linux.do ha un protection Cloudflare che può bloccare l'accesso. Se vedi "Verify you are human":
```
click @e5               # Clicca il checkbox
wait 3000               # Aspetta
snapshot -i             # Controlla se è passato
```
Se non funziona, usa `web_search` con `site:linux.do` invece.

---

### 📄 web_fetch
Scarica il contenuto testuale di una pagina.

```
web_fetch(url="https://www.helpaio.com/transit")
```

**Utile per:** Siti che non richiedono JavaScript né login.

---

### 📁 read / write / edit
Gestione file locali.

```
read(path="/home/manu/linux-do-explorer/MEGA-SUNTO.md")
write(path="/home/manu/output.md", content="...")
edit(path="/home/manu/file.md", edits=[{"oldText": "...", "newText": "..."}])
```

---

## Come Cercare su Linux.do

### Categorie Principali
| Categoria | URL | Cosa trovi |
|-----------|-----|------------|
| **福利羊毛** | `linux.do/c/welfare/36` | Offerte, giveaway, codici sconto |
| **搞七捻三** | `linux.do/c/off-topic/3` | Recensioni, confronti, consigli |
| **开发调优** | `linux.do/c/develop/4` | Configurazione, troubleshooting |
| **文档共建** | `linux.do/c/doc/12` | Guide, "省钱系列" |

### Ricerche nella Barra
```
中转站 推荐           — Recensioni
中转站 评测           — Confronti
淘宝 中转             — Acquisti
Claude 中转           — Relay specifici
倍率 / 缓存率         — Metriche tecniche
```

### Topic Fondamentali
| Topic | ID | Contenuto |
|-------|-----|-----------|
| 省钱系列8 | 1740014 | Guida completa Claude Code Max |
| 包月中转站 | 1427797 | Relay con abbonamento mensile |
| 中转站能有claude，codex用 | 1968935 | Relay per Claude e Codex |

---

## Come Verificare un Relay

### Fonti di Verifica
| Fonte | URL | Cosa verifica |
|-------|-----|---------------|
| **HelpAIO** | helpaio.com/transit | Classifiche, uptime 24h, recensioni |
| **RouterPark** | routerpark.com | 679+ proxy monitorati, status reale |
| **GitHub relayAPI** | github.com/zzsting88/relayAPI | Lista completa con prezzi e recensioni |
| **禾维AI** | hvoy.ai | Dashboard ranking tempo reale |

### Checklist di Verifica
- [ ] Uptime >95% (controlla su HelpAIO o RouterPark)
- [ ] Cache rate >85% (importante per Claude)
- [ ] Politica rimborso presente
- [ ] Supporto fatture (se necessario)
- [ ] Gruppo QQ attivo (>1.000 membri)
- [ ] Prezzo in linea con la media (non troppo basso)

### Red Flags
- ❌ Prezzo troppo basso (modelli scambiati)
- ❌ Nessun gruppo QQ/post-vendita
- ❌ Account nuovo senza storico
- ❌ Nessuna politica rimborso
- ❌ Uptime <90%
- ❌ Problemi passati non risolti

---

## Come Comprare su Taobao

### Ricerche
```
"Claude API 中转"      — Relay per Claude
"GPT API 代理"         — Proxy per GPT
"Codex API 中转"       — Relay per Codex
"Gemini API 代理"      — Proxy per Gemini
"Claude Code API"      — Specifica per Claude Code
"API 充值卡"           — Card di credito
"API 兖值 套餐"        — Pacchetti prepagati
```

### Processo d'Acquisto
1. **Cerca** il relay su Taobao con le query sopra
2. **Verifica** il venditore (valutazioni >4.8, storico)
3. **Compra** un piccolo pacchetto di prova ($5-10)
4. **Ricevi** il codice/chiave via chat in-app
5. **Testa** su helpaio.com/transit o con un benchmark
6. **Poi** ricarica se è stabile

### Cosa Verificare nel Venditore
- ✅ Gruppo QQ con 1.000+ membri
- ✅ Valutazioni >4.8 stelle
- ✅ Storico vendite consistente
- ✅ Garanzia o rimborso entro X giorni
- ✅ Supporto clienti attivo

---

## 📚 Fonti con Liste di Relay

| Fonte | URL | # Relay | Descrizione |
|-------|-----|---------|-------------|
| **RouterPark** | [routerpark.com](https://routerpark.com) | 679+ | Directory completa, marketplace, forum |
| **HelpAIO** | [helpaio.com/transit](https://www.helpaio.com/transit) | ~40 | Classifiche indipendenti, uptime 24h |
| **GitHub relayAPI** | [github.com/zzsting88/relayAPI](https://github.com/zzsting88/relayAPI) | 40+ | Lista dettagliata con prezzi |
| **禾维AI** | [hvoy.ai](https://hvoy.ai) | Variabile | Ranking tempo reale |
| **Linux.do** | [linux.do](https://linux.do) | Discussioni | Forum tech cinese |

---

## Risorse da Monitorare

### Siti (aggiornamento continuo)
| Sito | Frequenza | Cosa guarda |
|------|-----------|-------------|
| [routerpark.com](https://routerpark.com) | Giornaliero | Nuovi proxy, status |
| [helpaio.com/transit](https://www.helpaio.com/transit) | Settimanale | Classifiche, uptime |
| [github.com/zzsting88/relayAPI](https://github.com/zzsting88/relayAPI) | Mensile | Nuove recensioni |
| [hvoy.ai](https://hvoy.ai) | Occasionale | Ranking tempo reale |

### Linux.do (aggiornamento continuo)
| Categoria | Frequenza | Cerca |
|-----------|-----------|-------|
| 福利羊毛 | Giornaliero | "中转", "免费", "福利" |
| 搞七捻三 | Settimanale | "中转站", "推荐", "评测" |
| 开发调优 | Occasionale | "中转 配置", "中转 问题" |

---

*Guida aggiornata il 2026-06-13 — stack VPS allineato a `VPS-STACK-RELAY.md`*
