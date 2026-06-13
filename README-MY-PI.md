# Deprecato — usa ~/.pi/agent

Il progetto **linux-do-explorer** è stato unificato in **my-pi**:

```bash
# Workspace unico (Pi + relay explorer)
cd ~/.pi/agent    # git clone https://github.com/manumastro/my-pi.git ~/.pi/agent

# Sync tra VPS
bash scripts/stack-sync.sh pull
bash scripts/stack-sync.sh push
```

Apri **`~/.pi/agent`** in Cursor al posto di questa cartella.

`~/linux-do-explorer/` può restare solo per file legacy (es. `grok_register/`).