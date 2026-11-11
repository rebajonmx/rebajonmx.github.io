"""Datos y utilidades compartidas de Rebajón MX."""
import json, datetime, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OFERTAS = RAIZ / "data" / "ofertas.json"
PUBLICO = RAIZ / "public"

WEB = "rebajonmx.netlify.app"
WHATSAPP = "https://whatsapp.com/channel/0029VbDg01SAYlUKlEiiDX1O"
DESCUENTO_MINIMO = 15          # % mínimo para publicar una oferta
BUEN_FIN = (datetime.date(2026, 11, 13), datetime.date(2026, 11, 17))
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()


def hoy():
    # Hora de Ciudad de México (UTC-6, sin horario de verano)
    return (datetime.datetime.utcnow() - datetime.timedelta(hours=6)).date()


def fecha_texto(d=None):
    d = d or hoy()
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def cargar():
    return json.loads(OFERTAS.read_text(encoding="utf-8"))


def guardar(ofertas):
    OFERTAS.write_text(json.dumps(ofertas, ensure_ascii=False, indent=1), encoding="utf-8")


def activas(ofertas=None):
    ofertas = ofertas if ofertas is not None else cargar()
    return sorted([o for o in ofertas if o.get("active")], key=lambda o: -o["off"])


def campana(d=None):
    """Textos del video 1 según la fecha (antes, durante y después del Buen Fin)."""
    d = d or hoy()
    ini, fin = BUEN_FIN
    if d < ini:
        n = (ini - d).days
        return {"eb": "EL BUEN FIN 2026", "l1": "13 al 17", "l2": "de noviembre",
                "badge": "⏰ ¡MAÑANA EMPIEZA!" if n == 1 else f"⏰ FALTAN {n} DÍAS"}
    if d <= fin:
        n = (fin - d).days
        return {"eb": "EL BUEN FIN 2026", "l1": "YA EMPEZÓ", "l2": "hasta el 17 nov",
                "badge": "🔥 ¡ÚLTIMO DÍA!" if n == 0 else f"🔥 QUEDAN {n + 1} DÍAS"}
    return {"eb": "OFERTAS DE HOY", "l1": "Rebajas", "l2": "reales", "badge": "✅ PRECIOS REVISADOS"}


def precio(n):
    return f"${n:,.2f}".replace(".00", "")


def texto_whatsapp(top):
    lineas = ["🔥 *Top ofertas de hoy* 🔥", ""]
    for o in top:
        lineas += [o["name"], f"~{precio(o['was'])}~ → *{precio(o['now'])}* (-{o['off']}%)", f"👉 {o['url']}", ""]
    lineas += [f"Más ofertas: {WEB}", f"_Precios revisados el {fecha_texto()}; pueden cambiar._"]
    return "\n".join(lineas)


def caption(tipo, top):
    base = {
        1: "{eb}: te avisamos solo de las rebajas REALES, con precio de antes vs. ahora y link directo.",
        2: "Top 5 rebajas de hoy en Mercado Libre: " + "; ".join(f"{o['name']} a {precio(o['now'])} (-{o['off']}%)" for o in top[:5]) + ".",
        3: "¿Ese -50% es real? Muchas tiendas suben el precio antes y luego lo rebajan. Nosotros comparamos el precio de antes vs. ahora.",
    }[tipo].format(**campana())
    return (f"{base} Ofertas en {WEB} y alertas gratis en nuestro canal de WhatsApp: {WHATSAPP} "
            "#buenfin #buenfin2026 #ofertas #descuentos #mexico #mercadolibre")


EMOJI = [("bocina|barra|audífono|sonido", "🔊"), ("power bank|batería", "🔋"), ("tv|pantalla", "📺"),
         ("colchón|almohada", "🛏️"), ("freidora", "🍟"), ("licuadora", "🥤"), ("báscula", "⚖️"),
         ("celular|samsung|iphone|xiaomi", "📱"), ("echo|alexa", "🔵"), ("recipiente|vidrio", "🥡")]


def emoji(nombre):
    return next((e for k, e in EMOJI if re.search(k, nombre, re.I)), "🛒")


def corto(nombre):
    n = re.split(r",\s|·|\(| con | para ", nombre)[0].strip()
    while len(n) > 30 and " " in n:     # recorta por palabras completas
        n = n.rsplit(" ", 1)[0]
    return n


def js_videos(foto=lambda u: u):
    """Código del generador de videos con las ofertas y la campaña del día."""
    datos = [{"n": o.get("short") or corto(o["name"]), "e": emoji(o["name"]),
              "now": o["now"], "was": o["was"], "off": o["off"], "img": foto(o["img"])} for o in activas()[:6]]
    return ((RAIZ / "plantilla" / "videos.js").read_text(encoding="utf-8")
            .replace("__D__", json.dumps(datos, ensure_ascii=False))
            .replace("__K__", json.dumps(campana(), ensure_ascii=False))
            .replace("__SEED__", str(hoy().toordinal())))
