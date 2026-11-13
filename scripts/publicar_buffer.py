"""Publica el video del turno en Instagram (Reel), Facebook (Reel) y TikTok a la vez, vía Buffer (plan gratis).
Con --carrusel publica el carrusel de imágenes del día (public/media/carrusel.json), una vez al día.

Necesita el secreto BUFFER_API_KEY (Buffer → Settings → API). El video ya debe estar en la página
(Buffer lo descarga de https://<web>/media/<archivo>.mp4). Lee el texto y el archivo de public/media/turno.json
y deja registro en data/historial.json (sirve para comparar qué conceptos y colores funcionan mejor).
"""
import os, sys, requests
from comun import CONFIG, HISTORIAL, MEDIA, WEB, ahora, escribir_json, leer_json

API = "https://api.buffer.com"
META = {"instagram": {"instagram": {"type": "reel", "shouldShareToFeed": True}},
        "facebook": {"facebook": {"type": "reel"}},
        "tiktok": {"tiktok": {"isAiGenerated": False}}}
META_FOTOS = {"instagram": {"instagram": {"type": "post", "shouldShareToFeed": True}},
              "facebook": {"facebook": {"type": "post"}},
              "tiktok": {"tiktok": {"title": "Top ofertas de hoy"}}}
CREAR = """mutation($input: CreatePostInput!) {
  createPost(input: $input) { ... on PostActionSuccess { post { id } } ... on MutationError { message } } }"""


def gql(query, variables=None):
    r = requests.post(API, json={"query": query, "variables": variables or {}}, timeout=60,
                      headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY'].strip()}"})
    if r.status_code >= 400 and not r.text.startswith("{"):
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]


def canales():
    orgs = gql("query { account { organizations { id } } }")["account"]["organizations"]
    res = []
    for o in orgs:
        res += gql("query($o: OrganizationId!) { channels(input: {organizationId: $o}) { id service name } }",
                   {"o": o["id"]})["channels"]
    return res


def main():
    carrusel = "--carrusel" in sys.argv
    if carrusel:
        from generar_carrusel import toca_carrusel
        turno = leer_json(MEDIA / "carrusel.json", {})
        if not turno.get("archivos"):
            print("No hay carrusel listo: se omite.")
            return
        if not toca_carrusel() and "--forzar" not in sys.argv:
            print("Hoy ya se publicó el carrusel (o aún no son las 11:00): se omite.")
            return
        turno = {**turno, "concepto": "carrusel", "archivo": turno["archivos"][0]}
    else:
        turno = leer_json(MEDIA / "turno.json", None)
    if not turno:
        sys.exit("No hay public/media/turno.json: primero corre generar_video.py")
    if not os.environ.get("BUFFER_API_KEY"):
        print("Sin BUFFER_API_KEY: se omite la publicación.")
        return
    url = f"https://{WEB}/media/{turno['archivo']}"
    redes = CONFIG.get("redes", list(META))
    ids, fallas = {}, []
    for c in canales():
        if c["service"] not in redes:
            continue
        if carrusel:
            activos = [{"image": {"url": f"https://{WEB}/media/{a}"}} for a in turno["archivos"]]
            meta = META_FOTOS[c["service"]]
        else:
            activos = [{"video": {"url": url, "metadata": {"thumbnailOffset": 1500}}}]
            meta = META[c["service"]]
        entrada = {"text": turno["publicacion"], "channelId": c["id"], "schedulingType": "automatic", "mode": "shareNow",
                   "metadata": meta, "assets": activos}
        try:
            r = gql(CREAR, {"input": entrada})["createPost"]
            if "post" in r:
                ids[c["service"]] = r["post"]["id"]
                print(f"  ✓ {c['service']} ({c['name']}): {r['post']['id']}")
            else:
                fallas.append(f"{c['service']}: {r.get('message')}")
        except Exception as e:
            fallas.append(f"{c['service']}: {str(e)[:200]}")
    hist = leer_json(HISTORIAL, [])
    hist.append({"fecha": ahora().strftime("%Y-%m-%d %H:%M"), "concepto": turno["concepto"], "tema": turno["tema"],
                 "categoria": turno.get("categoria", ""), "archivo": turno["archivo"], "rebi": turno.get("rebi", ""), "buffer": ids, "errores": fallas})
    escribir_json(HISTORIAL, hist)
    for f in fallas:
        print("  ✗", f)
    if fallas and not ids and not carrusel:
        sys.exit(1)


if __name__ == "__main__":
    main()
