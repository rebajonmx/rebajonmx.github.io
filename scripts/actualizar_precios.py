"""Revisa el precio actual de cada oferta en su página de Mercado Libre.

- Usa la página del producto (la API pública de ML ya pide autenticación).
- Si ML bloquea la petición, conserva el precio anterior y lo reporta; no rompe nada.
- Una oferta se publica solo si tiene precio "antes" y descuento >= DESCUENTO_MINIMO.
"""
import re, sys, time, requests
from comun import cargar, guardar, DESCUENTO_MINIMO

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
      "Accept-Language": "es-MX,es;q=0.9"}
R_PRECIO = re.compile(r'"price":(\d+(?:\.\d+)?)')
R_ANTES = re.compile(r'"original_price":(\d+(?:\.\d+)?)')


def leer(url):
    r = requests.get(url, headers=UA, timeout=25)
    if r.status_code != 200:
        return None, None, f"HTTP {r.status_code}"
    p, a = R_PRECIO.search(r.text), R_ANTES.search(r.text)
    if not p:
        return None, None, "sin precio (posible bloqueo)"
    return float(p.group(1)), (float(a.group(1)) if a else None), "ok"


def main():
    ofertas, fallos = cargar(), 0
    for o in ofertas:
        if not o.get("product"):
            continue
        try:
            ahora, antes, estado = leer(o["product"])
        except requests.RequestException as e:
            ahora, antes, estado = None, None, str(e)[:60]
        if ahora is None:
            fallos += 1
            print(f"  ! {o['name'][:40]}: {estado} (se conserva el precio anterior)")
            continue
        o["now"] = ahora
        if antes:
            o["was"] = antes
        o["off"] = round((o["was"] - ahora) / o["was"] * 100) if antes else 0
        o["active"] = bool(antes) and o["off"] >= DESCUENTO_MINIMO
        print(f"  {'✓' if o['active'] else '·'} {o['name'][:40]}: ${ahora} (antes {antes}) -{o['off']}%")
        time.sleep(1.5)
    guardar(ofertas)
    print(f"Listo. {len(ofertas) - fallos} revisadas, {fallos} sin respuesta.")
    if fallos == len(ofertas):
        print("ML bloqueó todas las peticiones: usa navegador/actualizar_en_navegador.js")
        sys.exit(2)


if __name__ == "__main__":
    main()
