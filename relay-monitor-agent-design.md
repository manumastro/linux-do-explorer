# 🤖 Design Agente: Linux.do Relay Monitor

## Obiettivo
Creare un agente che monitora linux.do e altre fonti per trovare e valutare relay services (中转站) per API AI a prezzi economici.

---

## 🏗️ Architettura

```
┌─────────────────────────────────────────────────┐
│              Relay Monitor Agent                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Crawler  │───▶│ Analyzer │───▶│ Reporter │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │          │
│       ▼               ▼               ▼          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Forum   │    │  Price   │    │ Dashboard│  │
│  │  Parser  │    │  Tracker │    │ / Alerts │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 📦 Componenti

### 1. **Relay Tracker** (`tracker.py`)

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Relay:
    name: str
    url: str
    score: float  # Da HelpAIO
    availability: float  # Uptime %
    models: List[str]  # Claude, GPT, Gemini
    pricing: dict  # {model: price_per_dollar}
    payment_methods: List[str]
    refund_policy: Optional[str]
    invoice_support: bool
    last_updated: datetime
    notes: str

class RelayTracker:
    def __init__(self):
        self.relays: List[Relay] = []
        self.load_known_relays()
    
    def load_known_relays(self):
        """Carica relay noti da HelpAIO e altre fonti"""
        # Top relay da HelpAIO
        known_relays = [
            Relay(
                name="Micu",
                url="https://www.micuapi.ai",
                score=87.03,
                availability=98.47,
                models=["Claude", "GPT"],
                pricing={"Claude": 1.2, "GPT": 1.0},
                payment_methods=["Alipay", "WeChat"],
                refund_policy="Sì, no commissione",
                invoice_support=True,
                last_updated=datetime.now(),
                notes="#1 su HelpAIO, supporto rapido"
            ),
            Relay(
                name="Packy Code",
                url="https://www.packyapi.com",
                score=82.71,
                availability=99.02,
                models=["Claude", "GPT", "Gemini"],
                pricing={"Claude": 1.0, "GPT": 0.8},
                payment_methods=["Alipay", "WeChat", "Card"],
                refund_policy="Sì, 5% commissione",
                invoice_support=True,
                last_updated=datetime.now(),
                notes="Cache 88-93%, lunga history"
            ),
            # ... altri relay
        ]
        self.relays = known_relays
    
    def check_new_relays(self, forum_posts: List[dict]):
        """Cerca nuovi relay nei post del forum"""
        new_relays = []
        for post in forum_posts:
            relay = self._extract_relay_info(post)
            if relay and not self._relay_exists(relay.name):
                new_relays.append(relay)
        return new_relays
    
    def update_prices(self, relay_name: str, new_prices: dict):
        """Aggiorna prezzi di un relay"""
        for relay in self.relays:
            if relay.name == relay_name:
                relay.pricing.update(new_prices)
                relay.last_updated = datetime.now()
                break
    
    def get_best_relay(self, model: str, max_price: float = None) -> Optional[Relay]:
        """Trova il relay migliore per un modello"""
        candidates = [r for r in self.relays if model in r.models]
        
        if max_price:
            candidates = [r for r in candidates if r.pricing.get(model, float('inf')) <= max_price]
        
        if not candidates:
            return None
        
        # Ordina per score * availability
        candidates.sort(key=lambda r: r.score * r.availability, reverse=True)
        return candidates[0]
```

### 2. **Forum Crawler** (`crawler.py`)

```python
import requests
import time
from bs4 import BeautifulSoup

class LinuxDoCrawler:
    BASE_URL = "https://linux.do"
    
    def __init__(self, rate_limit=2.0):
        self.rate_limit = rate_limit
        self.session = requests.Session()
    
    def search_relay_topics(self, query: str):
        """Cerca topic su relay/中转站"""
        url = f"{self.BASE_URL}/search.json?q={query}"
        response = self.session.get(url)
        time.sleep(self.rate_limit)
        return response.json()
    
    def get_category_topics(self, category_slug: str, page: int = 1):
        """Ottieni topic da una categoria"""
        url = f"{self.BASE_URL}/c/{category_slug}.json?page={page}"
        response = self.session.get(url)
        time.sleep(self.rate_limit)
        return response.json()
    
    def crawl_welfare_category(self):
        """Crawla la categoria 福利羊毛 per offerte relay"""
        topics = self.get_category_topics("welfare")
        return self._filter_relay_topics(topics)
    
    def crawl_offtopic_category(self):
        """Crawla la categoria 搞七捻三 per discussioni relay"""
        topics = self.get_category_topics("off-topic")
        return self._filter_relay_topics(topics)
    
    def _filter_relay_topics(self, topics: dict):
        """Filtra topic relativi a relay"""
        relay_keywords = [
            "中转", "中转站", "relay", "api 代理", "api 中转",
            "claude 中转", "codex 中转", "gemini 中转",
            "micu", "packy", "timicc", "sssaicode", "right code"
        ]
        
        filtered = []
        for topic in topics.get('topic_list', {}).get('topics', []):
            title = topic.get('title', '').lower()
            if any(kw in title for kw in relay_keywords):
                filtered.append(topic)
        
        return filtered
```

### 3. **Price Monitor** (`prices.py`)

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class PriceMonitor:
    def __init__(self):
        self.price_history = []
    
    def fetch_helpaio_prices(self):
        """Recupera prezzi da HelpAIO"""
        url = "https://www.helpaio.com/transit"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parsing della tabella prezzi
        prices = self._parse_helpaio_table(soup)
        return prices
    
    def fetch_relay_prices(self, relay_url: str):
        """Recupera prezzi dal sito del relay"""
        # Ogni relay ha un formato diverso
        # Questa è una struttura generica
        try:
            response = requests.get(f"{relay_url}/api/models")
            return response.json()
        except:
            return None
    
    def compare_prices(self, model: str):
        """Confronta prezzi di un modello su tutti i relay"""
        from .tracker import RelayTracker
        tracker = RelayTracker()
        
        comparisons = []
        for relay in tracker.relays:
            if model in relay.models:
                comparisons.append({
                    'name': relay.name,
                    'price': relay.pricing.get(model),
                    'availability': relay.availability,
                    'score': relay.score
                })
        
        comparisons.sort(key=lambda x: x['price'])
        return comparisons
    
    def detect_price_drops(self, model: str, threshold: float = 0.1):
        """Rileva cali significativi di prezzo"""
        if len(self.price_history) < 2:
            return []
        
        drops = []
        current = self.price_history[-1]
        previous = self.price_history[-2]
        
        for relay_name in current:
            if relay_name in previous:
                current_price = current[relay_name].get(model, 0)
                previous_price = previous[relay_name].get(model, 0)
                
                if previous_price > 0:
                    change = (current_price - previous_price) / previous_price
                    if change < -threshold:
                        drops.append({
                            'relay': relay_name,
                            'model': model,
                            'old_price': previous_price,
                            'new_price': current_price,
                            'change': change
                        })
        
        return drops
```

### 4. **Alert System** (`alerts.py`)

```python
from enum import Enum
import requests

class AlertType(Enum):
    NEW_RELAY = "new_relay"
    PRICE_DROP = "price_drop"
    OUTAGE = "outage"
    HIGH_VALUE_DEAL = "high_value_deal"

class AlertSystem:
    def __init__(self, config: dict):
        self.config = config
        self.telegram_bot_token = config.get('telegram_bot_token')
        self.telegram_chat_id = config.get('telegram_chat_id')
    
    def send_alert(self, alert_type: AlertType, message: str, data: dict = None):
        """Invia alert via Telegram"""
        if not self.telegram_bot_token:
            print(f"[ALERT] {alert_type.value}: {message}")
            return
        
        formatted = self._format_message(alert_type, message, data)
        
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': formatted,
            'parse_mode': 'HTML'
        }
        
        requests.post(url, json=payload)
    
    def _format_message(self, alert_type: AlertType, message: str, data: dict) -> str:
        """Formatta il messaggio per Telegram"""
        icons = {
            AlertType.NEW_RELAY: "🆕",
            AlertType.PRICE_DROP: "📉",
            AlertType.OUTAGE: "⚠️",
            AlertType.HIGH_VALUE_DEAL: "🔥"
        }
        
        icon = icons.get(alert_type, "📢")
        return f"{icon} <b>{alert_type.value.upper()}</b>\n\n{message}"
    
    def check_new_deals(self, forum_posts: list):
        """Controlla nuovi post per offerte"""
        for post in posts:
            if self._is_good_deal(post):
                self.send_alert(
                    AlertType.HIGH_VALUE_DEAL,
                    f"Nuova offerta: {post['title']}",
                    {'url': post['url']}
                )
```

### 5. **Dashboard** (`dashboard.py`)

```python
from flask import Flask, render_template, jsonify
from .tracker import RelayTracker
from .prices import PriceMonitor

app = Flask(__name__)
tracker = RelayTracker()
price_monitor = PriceMonitor()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/relays')
def get_relays():
    return jsonify([r.__dict__ for r in tracker.relays])

@app.route('/api/relays/best/<model>')
def get_best_relay(model):
    relay = tracker.get_best_relay(model)
    if relay:
        return jsonify(relay.__dict__)
    return jsonify({'error': 'No relay found'}), 404

@app.route('/api/prices/compare/<model>')
def compare_prices(model):
    comparisons = price_monitor.compare_prices(model)
    return jsonify(comparisons)

@app.route('/api/prices/drops')
def price_drops():
    drops = price_monitor.detect_price_drops('Claude')
    return jsonify(drops)
```

---

## 🔄 Pipeline Operativa

```
1. CRAWL (ogni ora)
   │
   ├── Linux.do: 福利羊毛, 搞七捻三
   ├── Cerca: "中转", "relay", nomi relay noti
   └── Salva nuovi post
   │
   ▼
2. ANALYZE (ogni crawl)
   │
   ├── Estrai info relay (nome, URL, prezzi)
   ├── Confronta con HelpAIO
   ├── Aggiorna database
   └── Rileva cambiamenti
   │
   ▼
3. ALERT (on-demand)
   │
   ├── Nuovo relay scoperto
   ├── Calo prezzo significativo
   ├── Problema disponibilità
   └── Offerta speciale
   │
   ▼
4. REPORT (giornaliero)
   │
   ├── Top relay per modello
   ├── Trend prezzi
   ├── Nuove offerte
   └── Raccomandazioni
```

---

## 🛠️ Stack Tecnologico

```
Core:
├── Python 3.11+
├── SQLite (storage)
├── Requests (HTTP)
└── BeautifulSoup (parsing)

Monitoring:
├── APScheduler (cron)
├── Telegram Bot API (notifiche)
└── Webhook support

Dashboard:
├── Flask (backend)
├── Chart.js (grafici)
└── TailwindCSS (UI)
```

---

## 📊 Metriche da Monitorare

| Metrica | Frequenza | Fonte |
|---------|-----------|-------|
| **Prezzo per modello** | Oraria | Sito relay + HelpAIO |
| **Disponibilità** | 5 min | Health check endpoint |
| **Nuovi relay** | Ora | Linux.do crawl |
| **Cambiamenti prezzo** | Ora | Confronto storico |
| **Offerte speciali** | Continua | Linux.do + Telegram |

---

## 🚀 Implementazione Fase 1 (MVP)

### Settimana 1: Tracker Base
- [ ] Database SQLite con relay noti
- [ ] Fetch da HelpAIO (scraping/API)
- [ ] Store prezzi storici

### Settimana 2: Crawler
- [ ] Linux.do crawl categorie base
- [ ] Filtro topic relay
- [ ] Estrazione info da post

### Settimana 3: Alert
- [ ] Telegram bot setup
- [ ] Alert per nuovi relay
- [ ] Alert per cali prezzo

### Settimana 4: Dashboard
- [ ] Dashboard web base
- [ ] Confronto prezzi
- [ ] Grafici trend

---

*Design v1.0 — 2026-05-30*
