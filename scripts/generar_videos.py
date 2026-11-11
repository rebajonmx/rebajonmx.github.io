"""Crea los 3 videos animados (1080x1920, con música generada) con las ofertas del día.

Uso: python generar_videos.py [1 2 3]
Salida: public/media/video-<n>.mp4 y public/media/portada-<n>.jpg
"""
import base64, subprocess, sys
from playwright.sync_api import sync_playwright
from comun import PUBLICO, js_videos

def foto_embebida(url):
    """Descarga la foto del producto y la incrusta (evita bloqueos CORS en el lienzo)."""
    try:
        import requests
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if r.ok:
            tipo = r.headers.get("content-type", "image/webp").split(";")[0]
            return f"data:{tipo};base64," + base64.b64encode(r.content).decode()
    except Exception as e:
        print("  foto no disponible:", str(e)[:60])
    return url


def main(ids):
    media = PUBLICO / "media"
    media.mkdir(parents=True, exist_ok=True)
    js = js_videos(foto_embebida)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page()
        pag.set_content("<html><body></body></html>")
        pag.add_script_tag(content=js)
        for n in ids:
            info = pag.evaluate("id => RVinfo(id)", n)
            wav = media / f"audio-{n}.wav"
            wav.write_bytes(base64.b64decode(pag.evaluate("id => RVwav(id)", n)))
            final = media / f"video-{n}.mp4"
            # Cada cuadro se dibuja y se entrega uno por uno: el video sale fluido sin importar la velocidad del servidor.
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(info["fps"]),
                                   "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                                   "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
                                   "-movflags", "+faststart", str(final)], stdin=subprocess.PIPE)
            for i in range(info["frames"]):
                ff.stdin.write(base64.b64decode(pag.evaluate("([id, i]) => RVframe(id, i)", [n, i])))
            ff.stdin.close()
            if ff.wait() != 0:
                raise RuntimeError(f"ffmpeg falló en el video {n}")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.8", "-i", str(final),
                            "-frames:v", "1", "-q:v", "3", str(media / f"portada-{n}.jpg")], check=True)
            wav.unlink()
            print(f"Video {n} listo: {final.stat().st_size / 1e6:.1f} MB, {info['frames']} cuadros")
        nav.close()


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [1, 2, 3])
