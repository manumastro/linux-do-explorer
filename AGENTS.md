# 📚 AGENTS.md — Come Esplorare il Mercato Grigio API AI

**Data:** 2026-05-30

---

## ⚠️ REGOLA FONDAMENTALE

> **PRIMA di tutto, consulta sempre le guide in locale nella cartella `/home/manu/linux-do-explorer/`**
>
> 1. Leggi `MEGA-SUNTO.md` per un riepilogo rapido
> 2. Leggi `relay-services-guide.md` per dettagli completi
> 3. Leggi `recommended-relays.md` per i top pick
> 4. Leggi `linux-do-navigation-guide.md` per navigare il forum
> 5. Poi, solo se necessario, fai ricerche web aggiuntive

---

## 📖 Indice

1. [Obiettivo](#obiettivo)
2. [Strumenti Pi da Utilizzare](#strumenti-pi-da-utilizzare)
3. [Come Cercare su Linux.do](#come-cercare-su-linuxdo)
4. [Come Verificare un Relay](#come-verificare-un-relay)
5. [Come Comprare su Taobao](#come-comprare-su-taobao)
6. [Strategia Consigliata](#strategia-consigliata)
7. [Risorse da Monitorare](#risorse-da-monitorare)

---

## Obiettivo

Trovare **relay services (中转站)** affidabili che diano accesso a modelli AI (Claude, GPT, Gemini, Codex) a prezzi economici.

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

*Guida aggiornata il 2026-05-30*
