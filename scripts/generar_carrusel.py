"""Crea el carrusel de imágenes del día: "Top 5 ofertas de hoy" (7 imágenes 1080x1350 para Instagram, Facebook y TikTok).

Uso:  python generar_carrusel.py            (elige solo productos y color)
      python generar_carrusel.py --tema rosa
Salida: public/media/carrusel-AAAAMMDD-HHMM-N.jpg y public/media/carrusel.json (texto + archivos).
Lo publica publicar_buffer.py --carrusel (una vez al día, ver toca_carrusel()).
"""
import argparse, base64, html, random, requests
from playwright.sync_api import sync_playwright
from comun import (CONFIG, HISTORIAL, MEDIA, WEB, activas, ahora, campana, escribir_json, fecha_texto, leer_json,
                   pie_publicacion, precio)

CUANTOS = 5


def foto(url):
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if r.ok and r.headers.get("content-type", "").startswith("image"):
            return f"data:{r.headers['content-type'].split(';')[0]};base64," + base64.b64encode(r.content).decode()
    except Exception as e:
        print("  foto no disponible:", str(e)[:60])
    return ""


def toca_carrusel():
    """Un carrusel al día, en la primera publicación desde las 11:00 (hora CDMX)."""
    hoy = ahora().strftime("%Y-%m-%d")
    ya = any(h.get("concepto") == "carrusel" and h.get("fecha", "").startswith(hoy) and h.get("buffer")
             for h in leer_json(HISTORIAL, []))
    return not ya and ahora().hour >= 11


def elegir_productos():
    """Los de más descuento, de categorías distintas, rotando día a día para no repetir siempre los mismos."""
    lista = sorted([o for o in activas() if o.get("img")], key=lambda o: -o["off"])
    n_carr = sum(1 for h in leer_json(HISTORIAL, []) if h.get("concepto") == "carrusel")
    if lista:
        k = (n_carr * CUANTOS) % len(lista)
        lista = lista[k:] + lista[:k]
    elegidos, cats = [], set()
    for o in lista:                      # primero uno por categoría
        if o.get("cat") not in cats:
            elegidos.append(o); cats.add(o.get("cat"))
        if len(elegidos) == CUANTOS:
            break
    for o in lista:                      # si faltan, completa con los siguientes
        if len(elegidos) == CUANTOS:
            break
        if o not in elegidos:
            elegidos.append(o)
    return sorted(elegidos, key=lambda o: -o["off"])


CSS = """
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1350px;background:var(--fondo);color:var(--texto);font-family:Figtree,Arial,sans-serif;
 position:relative;overflow:hidden}
.deco{position:absolute;border-radius:50%;background:var(--deco);opacity:.55}
.logo{position:absolute;top:56px;left:0;right:0;text-align:center;font-family:'Bowlby One',Impact,sans-serif;font-size:46px}
.logo span{background:var(--acento2);color:#141a33;padding:6px 26px;border-radius:18px;display:inline-block;transform:rotate(-3deg)}
.logo b{background:var(--acento);color:var(--sobre);font-size:26px;padding:4px 12px;border-radius:10px;margin-left:8px;vertical-align:middle}
.centro{position:absolute;left:70px;right:70px;top:190px;bottom:150px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.titulo{font-family:'Bowlby One',Impact,sans-serif;font-size:118px;line-height:1.02;text-transform:uppercase}
.sub{font-size:44px;font-weight:700;margin-top:28px;color:var(--suave)}
.pill{display:inline-block;background:var(--acento);color:var(--sobre);font-weight:800;font-size:38px;padding:14px 34px;border-radius:999px;margin-top:40px}
.foto{width:660px;height:600px;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center;
 box-shadow:0 18px 50px rgba(0,0,0,.18);position:relative}
.foto img{max-width:560px;max-height:520px;object-fit:contain}
.foto .e{font-size:260px}
.num{position:absolute;top:-26px;left:-26px;width:110px;height:110px;border-radius:50%;background:var(--acento2);color:#141a33;
 font-family:'Bowlby One',Impact,sans-serif;font-size:56px;display:flex;align-items:center;justify-content:center}
.off{position:absolute;top:-26px;right:-30px;background:var(--acento);color:var(--sobre);font-family:'Bowlby One',Impact,sans-serif;
 font-size:58px;padding:10px 26px;border-radius:24px;transform:rotate(4deg)}
.nombre{font-size:46px;font-weight:800;margin-top:44px;line-height:1.15;max-width:900px}
.precios{margin-top:22px;display:flex;align-items:baseline;gap:28px;justify-content:center}
.antes{font-size:42px;color:var(--suave);text-decoration:line-through}
.ahora{font-family:'Bowlby One',Impact,sans-serif;font-size:96px;color:var(--acento)}
.ahorro{font-size:36px;font-weight:700;margin-top:6px}
.pie{position:absolute;bottom:56px;left:0;right:0;text-align:center;font-size:34px;font-weight:700;color:var(--suave)}
.lista{font-size:44px;font-weight:700;line-height:1.45;margin-top:30px}
"""


def pagina(tema, cuerpo):
    t = CONFIG["temas"][tema]
    var = (f"--fondo:{t['fondo']};--texto:{t['texto']};--suave:{t['suave']};--acento:{t['acento']};"
           f"--acento2:{t['acento2']};--sobre:{t['sobre_acento']};--deco:{t['decoracion']}")
    logo = CONFIG.get("logo", ["REBAJÓN", "MX"])
    return f"""<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bowlby+One&family=Figtree:wght@400;700;800&display=swap" rel="stylesheet">
<style>:root{{{var}}}{CSS}</style></head><body>
<div class="deco" style="width:520px;height:520px;left:-200px;top:-160px"></div>
<div class="deco" style="width:420px;height:420px;right:-160px;bottom:-140px"></div>
<div class="logo"><span>{html.escape(logo[0])}</span><b>{html.escape(logo[1])}</b></div>
{cuerpo}</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tema", default="")
    a = ap.parse_args()
    temas = list(CONFIG["temas"])
    tema = a.tema if a.tema in temas else temas[ahora().timetuple().tm_yday % len(temas)]
    prods = elegir_productos()
    if len(prods) < 3:
        print("Pocas ofertas con foto: no se crea carrusel.")
        escribir_json(MEDIA / "carrusel.json", {})
        return
    c = campana()
    etiqueta = c["nombre"] if c["etapa"] == "durante" else fecha_texto()
    slides = [f"""<div class="centro"><div class="titulo">Top {len(prods)}<br>ofertas<br>de hoy</div>
<div class="sub">{html.escape(etiqueta)} · precios revisados</div><div class="pill">Desliza →</div></div>
<div class="pie">{html.escape(WEB)}</div>"""]
    for i, o in enumerate(prods, 1):
        img = foto(o["img"])
        dentro = f'<img src="{img}">' if img else f'<span class="e">{o.get("e", "🛒")}</span>'
        slides.append(f"""<div class="centro"><div class="foto"><div class="num">{i}</div><div class="off">-{o['off']}%</div>{dentro}</div>
<div class="nombre">{html.escape(o['name'][:60])}</div>
<div class="precios"><span class="antes">{precio(o['was'])}</span><span class="ahora">{precio(o['now'])}</span></div>
<div class="ahorro">Ahorras {precio(o['was'] - o['now'])}</div></div>
<div class="pie">Link directo en {html.escape(WEB)}</div>""")
    slides.append(f"""<div class="centro"><div class="titulo" style="font-size:96px">¿Cuál te<br>llevas?</div>
<div class="lista">💬 Coméntalo abajo<br>💾 Guarda este post<br>📲 Compártelo con quien lo necesita</div>
<div class="pill">{html.escape(WEB)}</div><div class="sub">Alertas gratis en nuestro canal de WhatsApp</div></div>""")
    sello = ahora().strftime("%Y%m%d-%H%M")
    for viejo in MEDIA.glob("carrusel-*.jpg"):
        viejo.unlink()
    archivos = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": 1080, "height": 1350})
        for n, cuerpo in enumerate(slides, 1):
            pag.set_content(pagina(tema, cuerpo), wait_until="networkidle")
            pag.wait_for_timeout(300)
            nombre = f"carrusel-{sello}-{n}.jpg"
            pag.screenshot(path=str(MEDIA / nombre), type="jpeg", quality=90)
            archivos.append(nombre)
        nav.close()
    lineas = [f"{i}. {o['name'][:55]}: {precio(o['now'])} (antes {precio(o['was'])}, -{o['off']}%)" for i, o in enumerate(prods, 1)]
    texto = (f"🔥 Top {len(prods)} ofertas de hoy · {etiqueta}\n\n" + "\n".join(lineas) +
             "\n\n¿Cuál te llevas? Coméntalo 👇 y guarda este post.\n\n" + pie_publicacion())
    escribir_json(MEDIA / "carrusel.json", {"archivos": archivos, "publicacion": texto, "tema": tema,
                                           "productos": [o["url"] for o in prods]})
    print(f"Carrusel {tema}: {len(archivos)} imágenes · " + " | ".join(o["name"][:25] for o in prods))


if __name__ == "__main__":
    main()
