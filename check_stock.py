name: Panini Stock Watcher

on:
  schedule:
    - cron: "*/15 7-23 * * *"  # cada 15 min, das 8h às 00h (Lisboa = UTC+1)
  workflow_dispatch:             # permite correr manualmente a qualquer momento

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependências
        run: pip install -r requirements.txt

      - name: Verificar stock
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python check_stock.py
