"""Crea el video del turno (1080x1920, 30 fps, música propia) a partir de un concepto.

Uso:
  python generar_video.py                         -> elige solo concepto y color
  python generar_video.py --concepto oferta-del-dia --tema rosa
Salida: public/media/<archivo>.mp4, public/media/portada.jpg y public/media/turno.json
(turno.json lleva el texto de la publicación; lo usan publicar_buffer.py y publicar_telegram.py).
"""
import argparse, base64, json, subprocess
from playwright.sync_api import sync_playwright
from comun import RAIZ, MEDIA, ahora, escribir_json
from contenido import elegir


def foto_embebida(url, cache={}):
    """Descarga la foto y la incrusta en el video (si falla, el motor usa un servicio de imágenes o un emoji)."""
    if not url or url.startswith("data:"):
        return url
    if url not in cache:
        try:
            import requests
            r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            ok = r.ok and r.headers.get("content-type", "").startswith("image")
            cache[url] = f"data:{r.headers['content-type'].split(';')[0]};base64," + base64.b64encode(r.content).decode() if ok else url
        except Exception as e:
            print("  foto no disponible:", str(e)[:60])
            cache[url] = url
    return cache[url]


def renderizar(turno, salida):
    video = turno["video"]
    for e in video["escenas"]:
        if "producto" in e:
            e["producto"]["img"] = foto_embebida(e["producto"]["img"])
    js = (RAIZ / "plantilla" / "motor.js").read_text(encoding="utf-8").replace("__VIDEO__", json.dumps(video, ensure_ascii=False))
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page()
        pag.set_content("<html><body></body></html>")
        pag.add_script_tag(content=js)
        fotos = pag.evaluate("RVfotos()")
        info = pag.evaluate("RVinfo()")
        wav = salida.with_suffix(".wav")
        wav.write_bytes(base64.b64decode(pag.evaluate("RVwav()")))
        # Cada cuadro se dibuja y se entrega uno por uno: el video sale fluido sin importar la velocidad del servidor.
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(info["fps"]),
                               "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
                               "-movflags", "+faststart", str(salida)], stdin=subprocess.PIPE)
        for i in range(info["frames"]):
            ff.stdin.write(base64.b64decode(pag.evaluate("i => RVframe(i)", i)))
        ff.stdin.close()
        if ff.wait() != 0:
            raise RuntimeError("ffmpeg falló")
        wav.unlink()
        nav.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5", "-i", str(salida), "-frames:v", "1", "-q:v", "3",
                    str(salida.parent / "portada.jpg")], check=True)
    return info, fotos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--concepto")
    ap.add_argument("--tema")
    a = ap.parse_args()
    MEDIA.mkdir(parents=True, exist_ok=True)
    turno = elegir(a.concepto or None, a.tema or None)
    archivo = f"video-{ahora():%Y%m%d-%H%M}.mp4"   # nombre nuevo cada vez: evita que redes usen una copia vieja
    info, fotos = renderizar(turno, MEDIA / archivo)
    escribir_json(MEDIA / "turno.json", {"archivo": archivo, "concepto": turno["concepto"], "nombre": turno["nombre"],
                                         "tema": turno["tema"], "categoria": turno["categoria"], "publicacion": turno["publicacion"],
                                         "duracion": round(info["dur"], 1), "fotos": fotos})
    print(f"Video listo: {archivo} · concepto={turno['concepto']} · color={turno['tema']} · "
          f"{info['dur']:.1f}s · fotos {fotos['cargadas']}/{fotos['total']}")


if __name__ == "__main__":
    main()
