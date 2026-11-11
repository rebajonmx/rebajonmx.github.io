"""Datos y utilidades compartidas. Todo lo que cambia por marca/cliente está en config/marca.json."""
import json, datetime, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OFERTAS = RAIZ / "data" / "ofertas.json"
HISTORIAL = RAIZ / "data" / "historial.json"
PUBLICO = RAIZ / "public"
MEDIA = PUBLICO / "media"
CONFIG = json.loads((RAIZ / "config" / "marca.json").read_text(encoding="utf-8"))

WEB = CONFIG["web"]
WHATSAPP = CONFIG["whatsapp"]
TELEGRAM = CONFIG.get("telegram", "")
DESCUENTO_MINIMO = CONFIG["descuento_minimo"]
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()


def hoy():
    """Fecha de Ciudad de México (UTC-6, sin horario de verano)."""
    return ahora().date()


def ahora():
    return datetime.datetime.utcnow() - datetime.timedelta(hours=6)


def fecha_texto(d=None):
    d = d or hoy()
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def leer_json(ruta, defecto):
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return defecto


def escribir_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def cargar():
    return leer_json(OFERTAS, [])


def guardar(ofertas):
    escribir_json(OFERTAS, ofertas)


def vigente(o):
    """Una oferta se publica si está activa y su precio se revisó hace pocos días."""
    if not o.get("active"):
        return False
    rev = o.get("revisado")
    if not rev:
        return True
    dias = (hoy() - datetime.date.fromisoformat(rev)).days
    return dias <= CONFIG.get("dias_vigencia_precio", 10)


def activas(ofertas=None):
    ofertas = ofertas if ofertas is not None else cargar()
    return sorted([o for o in ofertas if vigente(o)], key=lambda o: -o["off"])


def campana(d=None):
    """Etapa de la campaña: 'antes', 'durante' o 'despues', con los días que faltan/quedan."""
    d = d or hoy()
    c = CONFIG["campana"]
    ini, fin = datetime.date.fromisoformat(c["inicio"]), datetime.date.fromisoformat(c["fin"])
    if d < ini:
        return {"etapa": "antes", "nombre": c["nombre"], "dias": (ini - d).days, "dias_restantes": (fin - ini).days + 1}
    if d <= fin:
        return {"etapa": "durante", "nombre": c["nombre"], "dias": 0, "dias_restantes": (fin - d).days + 1}
    return {"etapa": "despues", "nombre": c["nombre"], "dias": 0, "dias_restantes": 0}


def precio(n):
    return f"${n:,.2f}".replace(".00", "")


def pie_publicacion():
    """Texto que va SIEMPRE al final de cada publicación: página, WhatsApp (y Telegram si existe) y hashtags."""
    canales = f"alertas gratis en WhatsApp: {WHATSAPP}"
    if TELEGRAM:
        canales += f" y Telegram: {TELEGRAM}"
    return f"\n\n🌐 Ofertas con link directo: {WEB}\n🔔 {canales}\n\n" + " ".join(CONFIG["hashtags"])


def texto_alerta(top):
    """Mensaje de texto con las mejores ofertas (para Telegram o para pegar en WhatsApp)."""
    lineas = ["🔥 *Top ofertas de hoy* 🔥", ""]
    for o in top:
        lineas += [o["name"], f"~{precio(o['was'])}~ → *{precio(o['now'])}* (-{o['off']}%)", f"👉 {o['url']}", ""]
    lineas += [f"Más ofertas: {WEB}", f"_Precios revisados; pueden cambiar. {fecha_texto()}_"]
    return "\n".join(lineas)


EMOJI = [("bocina|barra|audífono|sonido", "🔊"), ("power bank|batería", "🔋"), ("tv|pantalla", "📺"),
         ("colchón|almohada", "🛏️"), ("freidora", "🍟"), ("licuadora", "🥤"), ("báscula", "⚖️"),
         ("celular|samsung|iphone|xiaomi", "📱"), ("echo|alexa", "🔵"), ("recipiente|vidrio", "🥡")]


def emoji(nombre):
    return next((e for k, e in EMOJI if re.search(k, nombre, re.I)), "🛒")


def corto(nombre):
    n = re.split(r",\s|·|\(| con | para ", nombre)[0].strip()
    while len(n) > 30 and " " in n:
        n = n.rsplit(" ", 1)[0]
    return n
