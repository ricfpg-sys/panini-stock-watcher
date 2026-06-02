# 🟢 Panini Stock Watcher

Bot que monitoriza produtos em esgotado no site da Panini Portugal e envia uma notificação via **Telegram** assim que voltam a ter stock.

Corre automaticamente na cloud com **GitHub Actions** — gratuitamente, sem servidor.

---

## Como funciona

1. O GitHub Actions corre o script a cada 15 minutos (24h por dia)
2. O script acede à página de cada produto e deteta se está disponível
3. Se o estado mudou (sem stock → com stock), envia uma mensagem Telegram imediatamente
4. O estado anterior é guardado para evitar notificações repetidas

---

## Configuração

### 1. Telegram Bot

1. Abre o Telegram e fala com [@BotFather](https://t.me/BotFather)
2. Envia `/newbot` e segue as instruções
3. Guarda o **token** gerado
4. Envia uma mensagem ao teu bot e acede a:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
5. Copia o valor de `chat.id` no JSON

### 2. GitHub Secrets

No repositório: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|--------|-------|
| `TELEGRAM_TOKEN` | Token do bot Telegram |
| `CHAT_ID` | O teu chat ID numérico |

### 3. Ficheiros do projeto

```
panini-stock-watcher/
├── .github/
│   └── workflows/
│       └── check_stock.yml   ← agenda e corre na cloud
├── check_stock.py            ← script principal
├── requirements.txt          ← dependências Python
└── README.md
```

---

## Adicionar produtos a monitorizar

Edita a lista `PRODUTOS` em `check_stock.py`:

```python
PRODUTOS = [
    {
        "nome": "FIFA WC 2026 – Big Collector's Box",
        "url": "https://www.paniniportugal.com/shp_prt_pt/...",
        "preco": "215€",
    },
    {
        "nome": "Outro produto",
        "url": "https://www.paniniportugal.com/shp_prt_pt/...",
        "preco": "9,99€",
    },
]
```

---

## Testar manualmente

No repositório: **Actions → Panini Stock Watcher → Run workflow**

O output mostra o estado atual de cada produto em tempo real.

---

## Notificações Telegram

**Stock disponível:**
```
🟢 STOCK DISPONÍVEL!

📦 FIFA WC 2026 – Big Collector's Box
💶 215€

👉 [Comprar agora]
```

**Ficou sem stock:**
```
🔴 Sem stock

📦 FIFA WC 2026 – Big Collector's Box ficou indisponível novamente.
```

---

## Notas

- Repositório **público** = minutos GitHub Actions ilimitados e gratuitos
- O GitHub pode desativar workflows agendados após **60 dias sem commits** — faz um commit ocasional ou usa o botão "Run workflow" para manter ativo
- Os atrasos de execução podem chegar a 10–30 minutos em horas de pico, o que é aceitável para alertas de stock

<!-- last updated: 2026-06-02 09:59 UTC -->
