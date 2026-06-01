import requests
from bs4 import BeautifulSoup
import os
import json

# ── Produtos a monitorizar ──────────────────────────────────────────────────
PRODUTOS = [
    {
        "nome": "FIFA WC 2026 – Big Collector's Box",
        "url": "https://www.paniniportugal.com/shp_prt_pt/fifa-world-cup-2026-big-collector-s-box-cole-o-oficial-de-cromos-005460box144oe-es01.html",
        "preco": "215€",
    },
]

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID        = os.environ["CHAT_ID"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

STATE_FILE = "stock_state.json"


def carregar_estado():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def guardar_estado(estado):
    with open(STATE_FILE, "w") as f:
        json.dump(estado, f, indent=2)


def verificar_stock(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Sinal 1: botão "Adicionar ao carrinho" presente?
        add_btn = soup.find("button", {"id": "product-addtocart-button"})

        # Sinal 2: texto "Indisponível" presente?
        indisponivel = any(
            "Indispon" in tag.get_text()
            for tag in soup.find_all(["span", "p", "div", "button"])
            if tag.get_text(strip=True)
        )

        return add_btn is not None and not indisponivel

    except Exception as e:
        print(f"  ⚠ Erro ao verificar {url}: {e}")
        return None  # None = inconclusivo, não alterar estado


def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()


def main():
    estado = carregar_estado()

    for produto in PRODUTOS:
        nome = produto["nome"]
        url  = produto["url"]
        key  = url  # URL como chave única de estado

        print(f"\n🔍 A verificar: {nome}")
        em_stock = verificar_stock(url)

        if em_stock is None:
            print("  → Resultado inconclusivo, a saltar.")
            continue

        estava_em_stock = estado.get(key, False)

        print(f"  → Agora: {'✅ Em stock' if em_stock else '❌ Sem stock'}")
        print(f"  → Antes: {'✅ Em stock' if estava_em_stock else '❌ Sem stock'}")

        if em_stock and not estava_em_stock:
            msg = (
                f"🟢 <b>STOCK DISPONÍVEL!</b>\n\n"
                f"📦 <b>{nome}</b>\n"
                f"💶 {produto['preco']}\n\n"
                f"👉 <a href=\"{url}\">Comprar agora</a>"
            )
            enviar_telegram(msg)
            print("  → 📨 Notificação enviada!")

        elif not em_stock and estava_em_stock:
            msg = (
                f"🔴 <b>Sem stock</b>\n\n"
                f"📦 <b>{nome}</b> ficou indisponível novamente."
            )
            enviar_telegram(msg)
            print("  → 📨 Notificação de saída de stock enviada.")

        estado[key] = em_stock

    guardar_estado(estado)
    print(f"\n💾 Estado guardado.")


if __name__ == "__main__":
    main()
