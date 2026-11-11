"""Sincroniza data/links.txt (lo que escribe una persona) con data/ofertas.json (lo que usa el sistema).

- Agrega las ofertas nuevas de links.txt y completa sus datos.
- Con la API de Mercado Libre (ML_CLIENT_ID/ML_CLIENT_SECRET): nombre, foto y precios automáticos.
- Sin API: usa lo que venga en el renglón: link | categoría | precio antes | precio ahora | nombre [| foto | calificación | vendidos]
- Recalcula descuento; una oferta se publica solo con descuento >= descuento_minimo (config/marca.json).
- Los links que se borran de links.txt dejan de publicarse (no se borran del historial).
- Lo que no se pudo completar queda en data/pendientes.json (aparece en ESTADO.md).
"""
import time
import mercadolibre as ml
from comun import RAIZ, DESCUENTO_MINIMO, cargar, guardar, escribir_json, hoy, emoji

LINKS = RAIZ / "data" / "links.txt"


def num(s):
    try:
        return float(str(s).replace("$", "").replace(",", "").strip())
    except ValueError:
        return None


def leer_links():
    filas = []
    for linea in LINKS.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        p = [x.strip() for x in linea.split("|")]
        filas.append({"url": p[0], "cat": p[1] if len(p) > 1 and p[1] else "",
                      "was": num(p[2]) if len(p) > 2 else None, "now": num(p[3]) if len(p) > 3 else None,
                      "name": p[4] if len(p) > 4 else "",
                      # Opcionales: foto (link .webp/.jpg de mlstatic), calificación y ventas
                      "img": p[5] if len(p) > 5 else "", "rating": p[6] if len(p) > 6 else "",
                      "sold": p[7] if len(p) > 7 else ""})
    return filas


def calcular(o):
    if o.get("now") and o.get("was") and o["was"] > o["now"]:
        o["off"] = round((o["was"] - o["now"]) / o["was"] * 100)
    else:
        o["off"] = 0
    o["active"] = o["off"] >= DESCUENTO_MINIMO and bool(o.get("name"))


def main():
    ofertas = cargar()
    por_url = {o["url"]: o for o in ofertas}
    filas = leer_links()
    en_lista = {f["url"] for f in filas}
    api = ml.disponible()
    pendientes = []
    print(f"{len(filas)} links en links.txt · API de Mercado Libre: {'sí' if api else 'no (precios manuales)'}")
    for f in filas:
        o = por_url.get(f["url"])
        if o is None:
            o = {"url": f["url"], "cat": f["cat"] or "Otros", "name": f["name"], "now": f["now"], "was": f["was"],
                 "img": "", "rating": "", "sold": "", "active": False}
            ofertas.append(o)
            por_url[f["url"]] = o
        # Lo escrito a mano en links.txt manda (sirve para corregir)
        for k in ("cat", "name", "now", "was", "img", "rating", "sold"):
            if f.get(k):
                o[k] = f[k]
        # Si cambiaste los precios del renglón, cuenta como revisión de hoy (los precios vencen en N días)
        firma = f"{f['was']}|{f['now']}"
        if f["now"] and f["was"] and o.get("firma") != firma:
            o["firma"], o["revisado"] = firma, hoy().isoformat()
        if api:
            try:
                if not o.get("product") or not o.get("ml_id"):
                    o["product"], o["ml_tipo"], o["ml_id"] = ml.resolver(o["url"])
                d = ml.datos(o["ml_tipo"], o["ml_id"]) if o.get("ml_id") else None
                if d and d.get("now"):
                    o["now"] = d["now"]
                    o["was"] = d.get("was") or o["was"]
                    o["name"] = o["name"] or d["name"]
                    o["img"] = o["img"] or d.get("img") or ""
                    o["revisado"] = hoy().isoformat()
                time.sleep(0.5)
            except Exception as e:
                print("  ! API Mercado Libre:", str(e)[:150])
                api = False
        o["e"] = emoji(o.get("name", ""))
        calcular(o)
        if not (o.get("name") and o.get("now") and o.get("was")):
            pendientes.append({"url": o["url"], "falta": [k for k in ("name", "now", "was") if not o.get(k)]})
        print(f"  {'✓' if o['active'] else '·'} {o.get('name', '')[:40] or o['url']}: {o.get('now')} (antes {o.get('was')}) -{o['off']}%")
    for o in ofertas:
        if o["url"] not in en_lista:
            o["active"] = False
    guardar(ofertas)
    escribir_json(RAIZ / "data" / "pendientes.json", pendientes)
    print(f"Listo: {sum(o['active'] for o in ofertas)} ofertas publicables, {len(pendientes)} pendientes.")


if __name__ == "__main__":
    main()
