"""Auditoría automática: revisa que todo esté bien y escribe ESTADO.md (se ve en GitHub en 10 segundos).

Revisa: página en línea y con fecha de hoy, video del turno publicado en la página, publicación en redes,
número de ofertas vigentes, precios por vencer y links pendientes. Si hay un problema GRAVE termina con error,
y GitHub manda un correo automático a la cuenta. No usa IA.
Uso: python auditar.py [resultado_buffer]   (el flujo le pasa success/failure del paso de publicación)
"""
import datetime, sys, requests
from comun import RAIZ, CONFIG, HISTORIAL, MEDIA, WEB, activas, cargar, fecha_texto, hoy, ahora, leer_json


def revisar_url(url):
    try:
        r = requests.get(url, timeout=30)
        return r.status_code, r.text if "html" in r.headers.get("content-type", "") else ""
    except requests.RequestException as e:
        return 0, str(e)


def revisar_links(ofertas):
    """Cada link de afiliado debe redirigir a Mercado Libre con el código de afiliado (matt_word)."""
    import re
    malos, codigos = [], set()
    for o in ofertas:
        try:
            r = requests.get(o["url"], allow_redirects=False, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            destino = r.headers.get("location", "")
            m = re.search(r"matt_word=([\w-]+)", destino)
            if r.status_code in (301, 302, 303, 307, 308) and "mercadolibre" in destino and m:
                codigos.add(m.group(1))
            else:
                malos.append(f"{o['name'][:40]} ({o['url']} → HTTP {r.status_code})")
        except requests.RequestException as e:
            malos.append(f"{o['name'][:40]} ({o['url']} → {str(e)[:40]})")
    return malos, codigos


def main():
    graves, avisos, ok = [], [], []
    buffer = sys.argv[1] if len(sys.argv) > 1 else "desconocido"
    st, html = revisar_url(f"https://{WEB}/")
    if st != 200:
        graves.append(f"La página no responde (HTTP {st}).")
    elif fecha_texto() not in html:
        avisos.append("La página está en línea pero no muestra la fecha de hoy.")
    else:
        ok.append("Página en línea con la fecha de hoy.")
    turno = leer_json(MEDIA / "turno.json", None)
    if turno:
        st, _ = revisar_url(f"https://{WEB}/media/{turno['archivo']}")
        (ok if st == 200 else graves).append(f"Video del turno en la página: {turno['archivo']} (HTTP {st}).")
        if turno.get("fotos", {}).get("cargadas", 1) < turno.get("fotos", {}).get("total", 0):
            avisos.append(f"Fotos en el video: {turno['fotos']['cargadas']}/{turno['fotos']['total']} (las demás salieron como emoji).")
    if buffer == "success":
        ok.append("Publicado en redes vía Buffer.")
    elif buffer in ("failure", "cancelled"):
        graves.append("Falló la publicación en redes (Buffer). Revisa el registro del paso 'Publicar'.")
    vig = activas()
    if len(vig) < 3:
        graves.append(f"Solo hay {len(vig)} ofertas vigentes: agrega links en data/links.txt.")
    elif len(vig) < 8:
        avisos.append(f"Hay {len(vig)} ofertas vigentes; conviene tener al menos 8.")
    else:
        ok.append(f"{len(vig)} ofertas vigentes.")
    malos, codigos = revisar_links(vig)
    if malos:
        (graves if len(malos) > len(vig) / 3 else avisos).append(f"{len(malos)} links de afiliado no abren bien: " + "; ".join(malos[:5]))
    else:
        ok.append(f"{len(vig)}/{len(vig)} links de afiliado abren Mercado Libre con tu código de afiliado ({', '.join(sorted(codigos))}).")
    if len(codigos) > 1:
        avisos.append(f"Hay links con distintos códigos de afiliado: {', '.join(sorted(codigos))}. Revisa que todos sean tuyos.")
    dias = CONFIG.get("dias_vigencia_precio", 10)
    por_vencer = [o["name"] for o in cargar() if o.get("active") and o.get("revisado")
                  and (hoy() - datetime.date.fromisoformat(o["revisado"])).days >= dias - 2]
    if por_vencer:
        avisos.append(f"{len(por_vencer)} ofertas con precio por vencer (actualiza sus precios en links.txt): " + ", ".join(por_vencer[:5]))
    pend = leer_json(RAIZ / "data" / "pendientes.json", [])
    if pend:
        avisos.append(f"{len(pend)} links sin datos completos (ver data/pendientes.json).")
    hist = leer_json(HISTORIAL, [])
    resumen = {}
    for h in hist:
        resumen.setdefault(h["tema"], 0)
        resumen[h["tema"]] += 1
    estado = "🔴 REVISAR" if graves else ("🟡 BIEN, CON AVISOS" if avisos else "🟢 TODO BIEN")
    md = [f"# Estado de {CONFIG['nombre']}: {estado}", "", f"Última revisión automática: {ahora():%Y-%m-%d %H:%M} (hora CDMX)", ""]
    for titulo, lista, icono in (("Problemas", graves, "🔴"), ("Avisos", avisos, "🟡"), ("Correcto", ok, "🟢")):
        if lista:
            md += [f"## {titulo}"] + [f"- {icono} {x}" for x in lista] + [""]
    md += ["## Últimas publicaciones", "", "| Fecha | Concepto | Color | Redes | Errores |", "|---|---|---|---|---|"]
    for h in hist[-10:][::-1]:
        md.append(f"| {h['fecha']} | {h['concepto']}{' (Rebi ' + h['rebi'] + ')' if h.get('rebi') else ''} | {h['tema']} | {', '.join(h.get('buffer', {})) or '-'} | {len(h.get('errores', []))} |")
    rebis = {}
    for h in hist:
        if h.get("rebi"):
            rebis[h["rebi"]] = rebis.get(h["rebi"], 0) + 1
    md += ["", "Rebi (voz que se alterna para comparar): " + (", ".join(f"{k}: {v}" for k, v in sorted(rebis.items())) or "aún no hay")]
    md += ["", f"Publicaciones por color: " + (", ".join(f"{k}: {v}" for k, v in sorted(resumen.items())) or "aún no hay"), "",
           "Para comparar resultados, mira las visualizaciones de cada video en Buffer (Analytics) o en cada red,",
           "y cruza con esta tabla (concepto y color). Guía: docs/MANUAL.md → Métricas."]
    (RAIZ / "ESTADO.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    if graves:
        sys.exit(1)


if __name__ == "__main__":
    main()
