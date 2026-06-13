# linux-do-explorer → migrato in my-pi

Le guide relay e lo stack VPS sono ora in **`~/.pi/agent/explorer/`** nel repo unico:

**https://github.com/manumastro/my-pi**

## Sync tra ambienti

```bash
# Clone (nuovo VPS)
git clone https://github.com/manumastro/my-pi.git ~/.pi/agent
cd ~/.pi/agent && npm install
bash scripts/stack-sync.sh pull

# Dopo modifiche (qualsiasi VPS)
bash scripts/stack-sync.sh push

# Altro VPS si allinea
bash scripts/stack-sync.sh pull
```

In Pi: `/stack-sync push` · `/stack-sync pull`

Questo repo (`linux-do-explorer`) resta come archivio/workspace locale; la sorgente di verità è **my-pi**.