"""Conexión con la API oficial (gratis) de Mercado Libre.

Mercado Libre bloquea la lectura de sus páginas desde servidores, así que los datos (nombre, foto,
precio, precio anterior) se piden a su API oficial con una "app de desarrollador" gratuita:
secretos ML_CLIENT_ID y ML_CLIENT_SECRET (cómo crearlos: docs/MANUAL.md, sección Mercado Libre).
Sin esos secretos todo sigue funcionando con los precios que pongas a mano en data/links.txt.
"""
import os, re, requests

API = "https://api.mercadolibre.com"
_token = None


def disponible():
    return bool(os.environ.get("ML_CLIENT_ID") and os.environ.get("ML_CLIENT_SECRET"))


def token():
    global _token
    if _token is None:
        r = requests.post(f"{API}/oauth/token", timeout=30, data={
            "grant_type": "client_credentials", "client_id": os.environ["ML_CLIENT_ID"].strip(),
            "client_secret": os.environ["ML_CLIENT_SECRET"].strip()})
        if not r.ok:
            raise RuntimeError(f"Mercado Libre no dio acceso ({r.status_code}): {r.text[:200]}")
        _token = r.json()["access_token"]
    return _token


def _get(ruta):
    r = requests.get(API + ruta, headers={"Authorization": f"Bearer {token()}"}, timeout=30)
    return r.json() if r.ok else None


def resolver(link):
    """Convierte un link corto de afiliado (meli.la/...) en la URL del producto y su identificador MLM."""
    url = link
    if "meli.la" in link:
        try:
            url = requests.get(link, timeout=20, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}).url
        except requests.RequestException:
            pass
    m = re.search(r"/p/(MLM\d+)", url) or re.search(r"(MLM)-?(\d+)", url)
    if not m:
        return url, None, None
    if m.re.pattern.startswith("/p/"):
        return url, "producto", m.group(1)
    return url, "item", m.group(1) + m.group(2)


def datos(tipo, ident):
    """Devuelve {name, now, was, img} o None."""
    if tipo == "item":
        it = _get(f"/items/{ident}")
        if not it:
            return None
        return {"name": it.get("title"), "now": it.get("price"), "was": it.get("original_price"),
                "img": (it.get("pictures") or [{}])[0].get("secure_url") or it.get("thumbnail")}
    pr = _get(f"/products/{ident}")
    if not pr:
        return None
    bb = pr.get("buy_box_winner") or {}
    if not bb.get("price"):
        items = _get(f"/products/{ident}/items") or {}
        bb = (items.get("results") or [{}])[0]
    return {"name": pr.get("name"), "now": bb.get("price"), "was": bb.get("original_price"),
            "img": (pr.get("pictures") or [{}])[0].get("url")}
