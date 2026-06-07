# 🎬 GROK VIDEO API — Guida Completa Relay

**Data:** 2026-05-31  
**Ultimo aggiornamento:** Ricerca relay per Grok Video (xAI) — image-to-video, text-to-video

---

## 📌 Riepilogo Rapido

Grok Video è il modello di generazione video di xAI (azienda di Elon Musk). Offre:
- **Text-to-Video:** genera video da descrizioni testuali
- **Image-to-Video:** anima immagini statiche con movimento naturale
- **Audio + Video:** generazione sincronizzata di audio e video
- **Durata:** 5-30 secondi
- **Qualità:** 480p, 720p, 1080p

**Prezzo ufficiale xAI:** ~$0.40-0.50/request  
**Prezzo migliore via relay:** **$0.04/video** (sconto ~90%)

---

## 🏆 Classifica Relay — I Più Economici

### 🥇 1. API Models (IL MIGLIORE)

| Dettaglio | Valore |
|-----------|--------|
| **Sito** | [apimodels.app](https://apimodels.app/zh/models?type=video) |
| **Documentazione** | [apimodels.app/zh/docs/video](https://apimodels.app/zh/docs/video) |
| **Prezzo** | **$0.04/video (10s)** oppure **$0.01/secondo** |
| **Free trial** | $1 gratis alla registrazione |
| **Pagamento** | Stripe, Alipay |
| **SLA** | 99.9% |

#### Modelli Disponibili

| Model ID | Prezzo | Durata | Note |
|----------|--------|--------|------|
| `grok-video-3-10s` | **$0.04** | 10s fisso | ⭐ Il più economico, audio incluso |
| `grok-video-3` | $0.01/secondo | 6-30s | Variabile per durata |
| `grok-video-3-official` | $0.06-0.30 | 6-30s | Versione ufficiale |

#### Funzionalità

- ✅ Text-to-Video
- ✅ Image-to-Video (fino a 3 immagini di riferimento)
- ✅ Audio + Video sincronizzato
- ✅ Aspect ratio: 16:9, 9:16, 1:1, 2:3, 3:2
- ✅ Qualità: 720P, 1080P
- ✅ Callback URL per notifiche
- ✅ Video salvati 7 giorni

#### Esempio Codice

**Text-to-Video:**
```bash
# Step 1: Crea task
curl -X POST https://apimodels.app/api/v1/video/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-video-3-10s",
    "prompt": "A cat playing piano in a jazz club, cinematic lighting",
    "aspect_ratio": "16:9"
  }'

# Step 2: Poll status
curl "https://apimodels.app/api/v1/video/generations?task_id=TASK_ID" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Image-to-Video:**
```bash
curl -X POST https://apimodels.app/api/v1/video/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-video-3",
    "prompt": "Animate this image with natural motion",
    "image_urls": ["https://example.com/image.png"],
    "aspect_ratio": "16:9"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "https://apimodels.app/api/v1/video/generations",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-video-3-10s",
        "prompt": "A majestic eagle soaring over mountains",
        "aspect_ratio": "16:9"
    }
)

print(response.json())
```

**Node.js:**
```javascript
const response = await fetch("https://apimodels.app/api/v1/video/generations", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "grok-video-3-10s",
    prompt: "A dog running on the beach at sunset",
    aspect_ratio: "16:9"
  })
});

const data = await response.json();
console.log(data);
```

---

### 🥈 2. APIMart (OTTIMO RAPPORTO QUALITÀ/PREZZO)

| Dettaglio | Valore |
|-----------|--------|
| **Sito** | [apimart.ai](https://apimart.ai/model/grok-video) |
| **Documentazione** | [docs.apimart.ai](https://docs.apimart.ai/cn/api-reference/videos/grok-imagine/generation) |
| **Prezzo** | ~$0.10-0.30/video (variabile per durata/qualità) |
| **Sconto** | 20% rispetto al prezzo ufficiale |
| **SLA** | 99.9% |

#### Modello

| Model ID | Prezzo | Durata | Note |
|----------|--------|--------|------|
| `grok-imagine-1.0-video-apimart` | Variabile | 6-30s | Supporta image-to-video |

#### Funzionalità

- ✅ Text-to-Video
- ✅ Image-to-Video (max 7 immagini di riferimento)
- ✅ Durata: 6-30 secondi
- ✅ Qualità: 480p, 720p
- ✅ Aspect ratio: 16:9, 9:16, 1:1, 3:2, 2:3

#### Esempio Codice

```bash
curl --request POST \
  --url https://api.apimart.ai/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "grok-imagine-1.0-video-apimart",
    "prompt": "A dog running on the beach, sunny weather, slow motion",
    "size": "16:9",
    "duration": 10,
    "quality": "720p",
    "image_urls": ["https://example.com/start.png"]
  }'
```

**Image-to-Video:**
```json
{
  "model": "grok-imagine-1.0-video-apimart",
  "prompt": "Bring the scene to life with natural dynamic effects",
  "image_urls": ["https://example.com/start.png"],
  "size": "16:9",
  "duration": 10,
  "quality": "720p"
}
```

---

### 🥉 3. Hypereal (PER PROFESSIONISTI)

| Dettaglio | Valore |
|-----------|--------|
| **Sito** | [hypereal.cloud](https://hypereal.cloud/zh/models/grok-video) |
| **Documentazione** | [hypereal.cloud/zh/docs](https://hypereal.cloud/zh/docs) |
| **Prezzo** | **$0.322/request** (fisso) |
| **SLA** | 99.9% |
| **Latenza media** | <2s |

#### Modelli Disponibili

| Model ID | Prezzo | Tipo | Note |
|----------|--------|------|------|
| `grok-imagine-video-t2v` | $0.322 | Text-to-Video | Generazione creativa |
| `grok-imagine-video-reference` | $0.322 | Reference-to-Video | Style transfer da immagine |
| `grok-imagine-video-edit` | $0.322 | Video Editing | Modifica video esistenti |

#### Funzionalità

- ✅ Text-to-Video
- ✅ Reference-to-Video (style transfer)
- ✅ Video Editing
- ✅ 50+ altri modelli sulla stessa API key
- ✅ API OpenAI-compatible

#### Esempio Codice

```python
import requests

response = requests.post(
    "https://api.hypereal.cloud/v1/videos/generate",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-imagine-video-t2v",
        "prompt": "A majestic eagle soaring over snow-capped mountains"
    }
)

print(response.json()["output_url"])
```

---

### 4. Atlas Cloud

| Dettaglio | Valore |
|-----------|--------|
| **Sito** | [atlascloud.ai](https://www.atlascloud.ai/it/models/xai/grok-imagine-video/text-to-video) |
| **Prezzo** | $0.06/secondo |
| **Modelli** | Text-to-Video, Image-to-Video, Reference-to-Video, Extend, Edit |

#### Funzionalità

- ✅ Text-to-Video (1-15s, 480p/720p)
- ✅ Image-to-Video (animazione da frame iniziale)
- ✅ Reference-to-Video (1-7 immagini di riferimento)
- ✅ Extend (estensione video esistente)
- ✅ Edit (modifica video con prompt testuali)

---

### 5. UnoRouter (SCONSIGLIATO)

| Dettaglio | Valore |
|-----------|--------|
| **Sito** | [unorouter.ai](https://unorouter.ai/en/models/grok-video-3) |
| **Prezzo** | **$0.40/request** (fisso) |
| **Note** | Più caro degli altri, non supporta image-to-video |

---

## 📊 Tabella Confronto Finale

| Cosa | API Models | APIMart | Hypereal | Atlas Cloud |
|------|------------|---------|----------|-------------|
| **Video 10s** | **$0.04** | ~$0.15 | $0.32 | $0.60 |
| **Video 30s** | **$0.30** | ~$0.45 | $0.32 | $1.80 |
| **Image-to-Video** | ✅ | ✅ | ✅ | ✅ |
| **Audio incluso** | ✅ | ❌ | ❌ | ❌ |
| **Free trial** | **$1** | ❌ | ❌ | ❌ |
| **Alipay** | ✅ | ✅ | ✅ | ❌ |
| **API OpenAI-compat.** | ✅ | ✅ | ✅ | ✅ |

---

## 🛒 Come Iniziare (Passo per Passo)

### Opzione 1: API Models (Consigliata)

1. Vai su [apimodels.app](https://apimodels.app/zh)
2. Clicca "获取 API 密钥" (Ottieni API Key)
3. Registrati (ricevi $1 gratis)
4. Vai su Console → API Keys → Crea nuova chiave
5. Scegli il modello `grok-video-3-10s`
6. Fai la prima chiamata API!

### Opzione 2: APIMart

1. Vai su [apimart.ai](https://apimart.ai)
2. Registrati e accedi
3. Vai su API Key Management
4. Crea una nuova API key
5. Usa il modello `grok-imagine-1.0-video-apimart`

### Opzione 3: Hypereal

1. Vai su [hypereal.cloud](https://hypereal.cloud/auth/register)
2. Registrati per un account gratuito
3. Vai su Dashboard → API Keys
4. Crea una nuova chiave API
5. Usa uno dei modelli video disponibili

---

## ⚠️ Limiti e Note

- **Durata massima:** 30 secondi (API Models, APIMart)
- **Qualità massima:** 1080p (dipende dal modello)
- **Video salvati:** 7 giorni (API Models), 24 ore (APIMart)
- **Contenuti vietati:** NSFW, volti reali di persone famose, contenuti protetti da copyright
- **Tempo di generazione:** ~30s per 5s di video, ~60s per 10s di video

---

## 🔗 Link Utili

| Risorsa | URL |
|---------|-----|
| API Models | [apimodels.app](https://apimodels.app/zh/models?type=video) |
| API Models Docs | [apimodels.app/zh/docs/video](https://apimodels.app/zh/docs/video) |
| APIMart | [apimart.ai](https://apimart.ai/model/grok-video) |
| APIMart Docs | [docs.apimart.ai](https://docs.apimart.ai/cn/api-reference/videos/grok-imagine/generation) |
| Hypereal | [hypereal.cloud](https://hypereal.cloud/zh/models/grok-video) |
| Hypereal Docs | [hypereal.cloud/zh/docs](https://hypereal.cloud/zh/docs) |
| Atlas Cloud | [atlascloud.ai](https://www.atlascloud.ai/it/models/xai/grok-imagine-video/text-to-video) |

---

## 💡 Consiglio Finale

**Per il massimo risparmio:** usa **API Models** con `grok-video-3-10s` a **$0.04/video** — è il prezzo più basso che ho trovato per Grok Video con audio incluso.

**Per qualità professionale:** usa **Hypereal** se hai bisogno di reference-to-video o video editing.

**Per bilanciamento qualità/prezzo:** usa **APIMart** con il suo sconto del 20% e supporto per fino a 7 immagini di riferimento.

---

*Guida aggiornata il 2026-05-31*
