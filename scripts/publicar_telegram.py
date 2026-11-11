"""Publica en un canal de Telegram (gratis y 100% automático, alternativa a WhatsApp).

Necesita dos secretos: TELEGRAM_BOT_TOKEN (de @BotFather) y TELEGRAM_CHAT_ID (por ejemplo @rebajonmx).
El bot debe ser administrador del canal. Si no existen los secretos, no hace nada.
Envía: 1) el video del turno con su texto y 2) un mensaje con el top de ofertas y sus links.
"""
import os, requests
from comun import MEDIA, WEB, activas, leer_json, texto_alerta


def main():
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(), os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        print("Sin TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID: se omite Telegram.")
        return
    api = f"https://api.telegram.org/bot{token}"
    turno = leer_json(MEDIA / "turno.json", None)
    if turno:
        r = requests.post(f"{api}/sendVideo", timeout=120, data={
            "chat_id": chat, "video": f"https://{WEB}/media/{turno['archivo']}", "caption": turno["publicacion"][:1024]})
        print("  video:", "✓" if r.ok else f"✗ {r.text[:200]}")
    top = activas()[:5]
    if top:
        r = requests.post(f"{api}/sendMessage", timeout=60, data={
            "chat_id": chat, "text": texto_alerta(top), "parse_mode": "Markdown", "disable_web_page_preview": "true"})
        print("  ofertas:", "✓" if r.ok else f"✗ {r.text[:200]}")


if __name__ == "__main__":
    main()
