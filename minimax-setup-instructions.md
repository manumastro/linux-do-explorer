# 🛠️ Istruzioni: Configurare MiniMax M2.7 Gratis su Pi

**Data:** 2026-06-08  
**Fonte:** RouterPark (chiave gratuita)

---

## 📋 Riepilogo

MiniMax M2.7 è un modello AI gratuito disponibile via RouterPark. La chiave è stata testata e funziona.

---

## 🔑 Credenziali

| Campo | Valore |
|-------|--------|
| **Provider** | `minimax-cn` |
| **API Key** | `sk-cp-79eekiGFmHisGc2hp4Cb9wT_Sm0JC9ZEl_BvD-ze4PqH4cCsCpOkEFb7G9Yuftm68cIRKTRU00cCwI4QUMSpaQrMw4EMg1Rta0AHy3jmSRjHgtvEyPH_myQ` |
| **Base URL** | `https://api.minimaxi.com/anthropic` |
| **Model ID** | `MiniMax-M2.7` |
| **API Type** | `anthropic-messages` |

---

## 📁 File da Modificare

### 1. `~/.pi/agent/models.json`

Aggiungere/aggiornare il provider `minimax-cn`:

```json
"minimax-cn": {
  "baseUrl": "https://api.minimaxi.com/anthropic",
  "api": "anthropic-messages",
  "apiKey": "sk-cp-79eekiGFmHisGc2hp4Cb9wT_Sm0JC9ZEl_BvD-ze4PqH4cCsCpOkEFb7G9Yuftm68cIRKTRU00cCwI4QUMSpaQrMw4EMg1Rta0AHy3jmSRjHgtvEyPH_myQ",
  "models": [
    {
      "id": "MiniMax-M2.7",
      "name": "MiniMax M2.7 (RouterPark Free)",
      "reasoning": true,
      "input": ["text"],
      "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
      "contextWindow": 1000000,
      "maxTokens": 131072
    }
  ]
}
```

### 2. `~/.pi/agent/settings.json`

Nel array `enabledModels`, assicurarsi che sia presente:

```json
"minimax-cn/MiniMax-M2.7"
```

---

## ✅ Verifica

Testare la chiave con questo comando curl:

```bash
curl -s https://api.minimaxi.com/anthropic/v1/messages \
  -H "x-api-key: sk-cp-79eekiGFmHisGc2hp4Cb9wT_Sm0JC9ZEl_BvD-ze4PqH4cCsCpOkEFb7G9Yuftm68cIRKTRU00cCwI4QUMSpaQrMw4EMg1Rta0AHy3jmSRjHgtvEyPH_myQ" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "MiniMax-M2.7",
    "max_tokens": 50,
    "messages": [{"role": "user", "content": "Ciao!"}]
  }'
```

**Risposta attesa:** HTTP 200 con un messaggio JSON contenente la risposta del modello.

---

## ⚠️ Note Importanti

1. **Chiave gratuita** — Potrebbe avere rate limit o essere disattivata in futuro
2. **Modello reasoning** — MiniMax M2.7 supporta il thinking/reasoning
3. **Costo** — Gratuito (input: $0, output: $0)
4. **Context window** — 1M tokens (molto generoso)

---

## 🔄 Per Aggiornare la Chiave

Se la chiave scade, cercarne una nuova su:
- https://routerpark.com/zh/free-claude-code
- https://routerpark.com/zh/t/97efe9bd-386f-4d6a-bed4-d9fefe5fb229

Poi aggiornare il campo `apiKey` in `models.json`.
