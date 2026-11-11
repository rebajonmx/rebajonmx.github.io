"""Elige el video del turno (concepto + color) y lo deja listo para el motor de videos.

Reglas de elección (sin IA):
- Solo conceptos de la temporada actual ('siempre' o la etapa de la campaña: antes/durante/despues).
- Se descartan los que no tienen suficientes productos (campo "requiere").
- Nunca repite el concepto del turno anterior; prefiere el concepto y el color menos usados.
  Así los 3 colores se reparten parejo y luego se pueden comparar visualizaciones (data/historial.json).
"""
import json, random, re
from comun import (RAIZ, CONFIG, HISTORIAL, activas, campana, corto, emoji, hoy, leer_json, precio,
                   pie_publicacion, DESCUENTO_MINIMO)

CONCEPTOS = RAIZ / "contenido" / "conceptos"


def conceptos():
    out = []
    for f in sorted(CONCEPTOS.glob("*.json")):
        try:
            c = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ! Concepto con error de formato, se ignora: {f.name} ({e})")
            continue
        if c.get("activo", True):
            out.append(c)
    return out


def producto_video(o):
    return {"n": o.get("short") or corto(o["name"]), "e": emoji(o["name"]), "now": o["now"], "was": o["was"],
            "off": o["off"], "img": o["img"], "cat": o.get("cat", "")}


def filtrar(ofertas, esc):
    lista = [o for o in ofertas if (not esc.get("categoria") or o.get("cat") == esc["categoria"])
             and (not esc.get("categorias") or o.get("cat") in esc["categorias"])
             and (not esc.get("max_precio") or o["now"] <= esc["max_precio"])]
    if esc.get("elegir") == "barato":
        lista.sort(key=lambda o: o["now"])
    elif esc.get("elegir") == "aleatorio":
        random.Random(hoy().toordinal()).shuffle(lista)
    elif esc.get("elegir") == "vendidos":
        def n(v):
            m = re.match(r"(\d+(?:\.\d+)?)\s*(mil|M)?", str(v or ""))
            return float(m.group(1)) * {"mil": 1e3, "M": 1e6}.get(m.group(2), 1) if m else 0
        lista.sort(key=lambda o: -n(o.get("sold")))
    elif esc.get("elegir") == "variado" and lista:
        # Rota por número de publicaciones: cada video muestra productos distintos (sigue ordenado por descuento)
        k = len(leer_json(HISTORIAL, [])) * esc.get("cuantos", 1) % len(lista)
        lista = lista[k:] + lista[:k]
    return lista


def categoria_del_dia(ofertas):
    """Categoría del turno: cambia en cada publicación (no solo cada día)."""
    cats = {}
    for o in ofertas:
        cats.setdefault(o.get("cat", ""), []).append(o)
    validas = sorted([c for c, v in cats.items() if c and len(v) >= 2])
    n = hoy().toordinal() + len(leer_json(HISTORIAL, []))
    return validas[n % len(validas)] if validas else ""


def variables(ofertas, cat):
    camp = campana()
    top = ofertas[0] if ofertas else None
    top3 = ofertas[:3]
    v = {"marca": CONFIG["nombre"], "web": CONFIG["web"], "tienda": CONFIG["tienda"], "campana": camp["nombre"],
         "dias": camp["dias"], "dias_restantes": camp["dias_restantes"], "descuento_minimo": DESCUENTO_MINIMO,
         "n_ofertas": len(ofertas), "categoria": cat, "categoria_mayus": cat.upper(),
         "ahorro_top3": precio(sum(o["was"] - o["now"] for o in top3))}
    if top:
        v.update(top_nombre=corto(top["name"]), top_precio=precio(top["now"]), top_antes=precio(top["was"]),
                 top_off=top["off"], top_ahorro=precio(top["was"] - top["now"]))
    return v


def rellenar(obj, v):
    """Reemplaza {variables} en todos los textos del concepto."""
    if isinstance(obj, str):
        return re.sub(r"\{(\w+)\}", lambda m: str(v.get(m.group(1), m.group(0))), obj)
    if isinstance(obj, list):
        return [rellenar(x, v) for x in obj]
    if isinstance(obj, dict):
        return {k: rellenar(x, v) for k, x in obj.items()}
    return obj


def cumple(c, ofertas, cat):
    req = c.get("requiere", {})
    lista = [o for o in ofertas if not req.get("max_precio") or o["now"] <= req["max_precio"]]
    if req.get("por_categoria"):
        lista = [o for o in lista if o.get("cat") == cat]
        if not cat:
            return False
    usa_productos = any(e["tipo"] in ("producto", "productos") for e in c["escenas"])
    return len(lista) >= req.get("minimo", 1 if usa_productos else 0)


def elegir(forzar_concepto=None, forzar_tema=None):
    ofertas = activas()
    cat = categoria_del_dia(ofertas)
    etapa = campana()["etapa"]
    hist = leer_json(HISTORIAL, [])
    candidatos = [c for c in conceptos() if c.get("temporada", "siempre") in ("siempre", etapa) and cumple(c, ofertas, cat)]
    if forzar_concepto:
        candidatos = [c for c in conceptos() if c["id"] == forzar_concepto] or candidatos
    if not candidatos:
        raise SystemExit("No hay conceptos disponibles para hoy (revisa contenido/conceptos y las ofertas).")
    ultimo = hist[-1]["concepto"] if hist else None
    usos = lambda clave, val: sum(1 for h in hist if h.get(clave) == val)
    pool = [c for c in candidatos if c["id"] != ultimo] or candidatos
    concepto = min(pool, key=lambda c: (usos("concepto", c["id"]), c["id"]))
    temas = concepto.get("temas") or list(CONFIG["temas"])
    tema = forzar_tema or min(temas, key=lambda t: (usos("tema", t), hist[-1]["tema"] == t if hist else False, t))
    return armar(concepto, tema, ofertas, cat)


def armar(concepto, tema, ofertas, cat):
    v = variables(ofertas, cat)
    c = rellenar(concepto, v)
    escenas, usados = [], set()
    for e in c["escenas"]:
        if e["tipo"] == "producto":
            lista = [o for o in filtrar(ofertas, e) if o["url"] not in usados] or filtrar(ofertas, e)
            if lista:
                o = lista[min(e.get("indice", 0), len(lista) - 1)]
                usados.add(o["url"])
                escenas.append({**e, "producto": producto_video(o)})
        elif e["tipo"] == "productos":
            lista = [o for o in filtrar(ofertas, e) if o["url"] not in usados][:e.get("cuantos", 3)]
            for k, o in enumerate(lista):
                usados.add(o["url"])
                escenas.append({"tipo": "producto", "etiqueta": f"#{k + 1}", "producto": producto_video(o),
                                "seg": e.get("seg_cada", 2.4)})
        else:
            escenas.append(e)
    if not escenas or escenas[-1]["tipo"] != "cierre":
        escenas.append({"tipo": "cierre"})
    return {"concepto": c["id"], "nombre": c["nombre"], "tema": tema, "categoria": cat,
            "publicacion": c["publicacion"].strip() + pie_publicacion(),
            "video": {"tema": CONFIG["temas"][tema], "logo": CONFIG["logo"], "web": CONFIG["web"],
                      "tienda": CONFIG["tienda"], "telegram": bool(CONFIG.get("telegram")),
                      "seed": hoy().toordinal() * 7 + len(leer_json(HISTORIAL, [])), "escenas": escenas}}


if __name__ == "__main__":
    t = elegir()
    print(json.dumps({k: t[k] for k in ("concepto", "tema", "categoria", "publicacion")}, ensure_ascii=False, indent=1))
