"""Busca solo (con la API oficial de Mercado Libre) las mejores ofertas de los más vendidos por categoría
y escribe data/sugerencias.md: una lista lista para copiar y pegar en data/links.txt.

Lo único que hace una persona: sacar el link de afiliado (Central de afiliados → Compartir → Copiar link)
y pegarlo en lugar de PEGA_AQUI_TU_LINK. Así las comisiones siempre usan el link oficial de Mercado Libre.

Necesita los secretos ML_CLIENT_ID y ML_CLIENT_SECRET. Corre cada semana (.github/workflows/sugerencias.yml)
o a mano: Actions → "Sugerencias de ofertas" → Run workflow.
"""
import re, time
import mercadolibre as ml
from comun import RAIZ, DESCUENTO_MINIMO, CONFIG, fecha_texto

SALIDA = RAIZ / "data" / "sugerencias.md"
LINKS = RAIZ / "data" / "links.txt"
POR_CATEGORIA = 6          # sugerencias por categoría
MIN_DESCUENTO = max(25, DESCUENTO_MINIMO)

# Nombre en la página  ←  palabras del nombre de la categoría de Mercado Libre
CATEGORIAS = {
    "Tecnología": ["Celulares y Telefonía", "Computación", "Electrónica, Audio y Video", "Consolas y Videojuegos"],
    "Electrodomésticos": ["Electrodomésticos"],
    "Hogar": ["Hogar, Muebles y Jardín"],
    "Belleza": ["Belleza y Cuidado Personal"],
    "Juguetes": ["Juegos y Juguetes"],
    "Herramientas": ["Herramientas"],
    "Mascotas": ["Animales y Mascotas"],
    "Deportes": ["Deportes y Fitness"],
    "Moda": ["Ropa, Bolsas y Calzado"],
}


def ya_publicados():
    texto = LINKS.read_text(encoding="utf-8")
    return set(re.findall(r"MLMU?\d+", texto))


def categorias_ml():
    lista = ml._get("/sites/MLM/categories") or []
    por_nombre = {c["name"]: c["id"] for c in lista}
    out = {}
    for nuestra, nombres in CATEGORIAS.items():
        out[nuestra] = [por_nombre[n] for n in nombres if n in por_nombre]
    return out


def candidato(tipo, ident):
    if tipo == "PRODUCT":
        d = ml.datos("producto", ident)
        url = f"https://www.mercadolibre.com.mx/p/{ident}"
    else:
        d = ml.datos("item", ident)
        url = f"https://articulo.mercadolibre.com.mx/{ident[:3]}-{ident[3:]}"
    if not d or not d.get("now") or not d.get("was") or d["was"] <= d["now"]:
        return None
    off = round((d["was"] - d["now"]) / d["was"] * 100)
    if off < MIN_DESCUENTO:
        return None
    return {**d, "off": off, "url": url, "id": ident}


def main():
    if not ml.disponible():
        raise SystemExit("Faltan los secretos ML_CLIENT_ID y ML_CLIENT_SECRET.")
    vistos = ya_publicados()
    cats = categorias_ml()
    secciones = []
    total = 0
    for nuestra, ids in cats.items():
        encontrados = []
        for cid in ids:
            h = ml._get(f"/highlights/MLM/category/{cid}") or {}
            for e in h.get("content", [])[:25]:
                if len(encontrados) >= POR_CATEGORIA * 2 or e.get("id") in vistos:
                    continue
                try:
                    c = candidato(e.get("type", "PRODUCT"), e["id"])
                except Exception as ex:
                    print("  !", e.get("id"), str(ex)[:100])
                    c = None
                if c:
                    c["pos"] = e.get("position", 99)
                    encontrados.append(c)
                    vistos.add(e["id"])
                time.sleep(0.2)
        encontrados.sort(key=lambda c: (-c["off"], c["pos"]))
        encontrados = encontrados[:POR_CATEGORIA]
        print(f"{nuestra}: {len(encontrados)} sugerencias")
        if encontrados:
            total += len(encontrados)
            filas = []
            for c in encontrados:
                nombre = re.sub(r"\s+", " ", c["name"] or "").strip()[:70]
                filas.append(f"**{nombre}** · ${c['now']:,.0f} (antes ${c['was']:,.0f}, -{c['off']}%) · "
                             f"[ver en Mercado Libre]({c['url']})\n```\nPEGA_AQUI_TU_LINK | {nuestra} | {c['was']} | "
                             f"{c['now']} | {nombre} | {c.get('img') or ''} | | | {c['url']}\n```")
            secciones.append(f"## {nuestra}\n\n" + "\n\n".join(filas))
    encabezado = f"""# Sugerencias de ofertas · {fecha_texto()}

{total} productos de los **más vendidos** de Mercado Libre con **{MIN_DESCUENTO}% o más** de descuento hoy,
que todavía no están en la página. Las genera solo el sistema (API oficial de Mercado Libre).

## Cómo agregar una (1 minuto cada una)

1. Abre **Mercado Libre → Mi cuenta → Afiliados y creadores**.
2. En "Busca productos" escribe el nombre de la sugerencia → en el producto dale **Compartir → Copiar link**.
3. Copia el renglón gris de la sugerencia (botón de copiar a la derecha).
4. Abre **data/links.txt** → lápiz ✏️ → pega el renglón al final → cambia `PEGA_AQUI_TU_LINK` por el link que copiaste
   (empieza con `https://meli.la/`) → **Commit changes**.

Listo: en la siguiente publicación sale en la página y en los videos, y el precio se actualiza solo.
Revisa la foto y que el producto sea confiable (marca conocida, buena calificación) antes de agregarlo.
"""
    SALIDA.write_text(encabezado + "\n" + "\n\n".join(secciones) + "\n", encoding="utf-8")
    print(f"Listo: {total} sugerencias en data/sugerencias.md")


if __name__ == "__main__":
    main()
