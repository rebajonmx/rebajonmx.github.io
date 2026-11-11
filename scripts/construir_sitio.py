"""Genera la página (public/index.html) con las ofertas vigentes, más el texto de alertas del día."""
import base64, json
from comun import RAIZ, PUBLICO, activas, fecha_texto, texto_alerta


def main():
    PUBLICO.mkdir(exist_ok=True)
    top = activas()
    campos = ("cat", "name", "now", "was", "off", "rating", "sold", "img", "url")
    datos = [{k: o.get(k, "") for k in campos} for o in top]
    html = (RAIZ / "plantilla" / "sitio.html").read_text(encoding="utf-8")
    fav = (RAIZ / "plantilla" / "favicon.b64").read_text().strip()
    html = (html.replace("__DEALS__", json.dumps(datos, ensure_ascii=False))
                .replace("__FAV__", fav).replace("__FECHA__", fecha_texto()))
    (PUBLICO / "index.html").write_text(html, encoding="utf-8")
    (PUBLICO / "whatsapp.txt").write_text(texto_alerta(top[:5]), encoding="utf-8")
    (PUBLICO / "favicon.png").write_bytes(base64.b64decode(fav))
    print(f"Sitio listo con {len(datos)} ofertas ({fecha_texto()}).")


if __name__ == "__main__":
    main()
