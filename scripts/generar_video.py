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


# ---------- Voz de Rebi (mascota) ----------
# Piper (voz neuronal libre, gratis, corre en el servidor). El flujo la instala en PIPER_BIN / PIPER_MODEL.
# Si no está disponible, el video sale igual con subtítulos y Rebi animado (sin voz).
import os, re, wave, array, math
DUR = {"gancho": 2.6, "texto": 3.2, "numero": 2.8, "lista": 3.8, "comparacion": 3.8, "producto": 2.4, "cierre": 3.4,
       "rebi": 3.2, "adivina": 4.2, "califica": 3.6}
SR = 22050


def en_palabras(texto):
    try:
        from num2words import num2words
    except ImportError:
        return texto
    texto = texto.replace("$", "").replace('"', " pulgadas").replace("%", " por ciento")
    return re.sub(r"\d[\d,]*(?:\.\d+)?", lambda m: num2words(int(round(float(m.group(0).replace(",", "")))), lang="es"), texto)


def guion(e):
    """Lo que dice Rebi en cada escena (se puede escribir en el concepto con "dice"; si no, se arma solo)."""
    d = e.get("producto")
    if e.get("dice"):
        return e["dice"], e.get("dice2", "")
    if e["tipo"] == "producto" and d:
        return f"{d['n']}. Antes {round(d['was'])} pesos, hoy {round(d['now'])}. ¡{d['off']} por ciento menos!", ""
    if e["tipo"] == "califica" and d:
        return f"{d['n']}, a {round(d['now'])} pesos. Le doy {str(d.get('calif', 8)).replace('.', ' punto ')} de diez.", ""
    if e["tipo"] == "adivina" and d:
        return f"¿Cuánto crees que cuesta? Tres, dos, uno...", f"¡Solo {round(d['now'])} pesos!"
    if e["tipo"] == "cierre":
        return "Todas las ofertas con link directo están en nuestra página. El link está en el perfil. ¡Nos vemos!", ""
    return "", ""


def trozos(texto, a, b):
    """Parte el subtítulo en frases cortas repartidas en el tiempo que dura la voz."""
    partes, cur = [], ""
    for w in texto.split():
        cur = (cur + " " + w).strip()
        if len(cur) > 48 or w[-1] in ".!?…,":
            partes.append(cur); cur = ""
    if cur:
        partes.append(cur)
    total, t, out = sum(len(p) for p in partes) or 1, a, []
    for p in partes:
        d = (b - a) * len(p) / total
        out.append({"a": round(t, 2), "b": round(t + d, 2), "t": p}); t += d
    return out


def sintetizar(texto, ruta):
    bin_, modelo = os.environ.get("PIPER_BIN"), os.environ.get("PIPER_MODEL")
    if not texto or not bin_ or not modelo or not os.path.exists(bin_) or not os.path.exists(modelo):
        return 0
    try:
        # Rebi: mismo ritmo y pausas del original (0.92 / 0.12) con voz real de hombre (es_MX-ald-medium), sin efectos.
        subprocess.run([bin_, "--model", modelo, "--output_file", str(ruta), "--length_scale", "0.92",
                        "--sentence_silence", "0.12"], input=en_palabras(texto).encode(), check=True,
                       capture_output=True, timeout=120)
        with wave.open(str(ruta)) as w:
            return w.getnframes() / w.getframerate()
    except Exception as ex:
        print("  voz no disponible:", str(ex)[:120])
        return 0


def preparar_voz(video, carpeta):
    """Genera la voz, ajusta la duración de cada escena a lo que dice Rebi y calcula boca (por cuadro) y subtítulos."""
    clips, subs, t = [], [], 0.0
    hay_voz = False
    for i, e in enumerate(video["escenas"]):
        base = e.get("seg") or DUR.get(e["tipo"], 3)
        d1, d2 = guion(e)
        r1, r2 = carpeta / f"voz{i}a.wav", carpeta / f"voz{i}b.wav"
        s1 = sintetizar(d1, r1) if d1 else 0
        s2 = sintetizar(d2, r2) if d2 else 0
        hay_voz |= bool(s1 or s2)
        est1 = s1 or len(d1) / 14
        est2 = s2 or len(d2) / 14
        dur = max(base, est1 + 0.7) if not d2 else max(base, est1 + 1.6 + est2)
        e["seg"] = round(dur, 2)
        if d1:
            clips.append((t + 0.25, r1 if s1 else None)); subs += trozos(d1, t + 0.2, t + 0.25 + est1)
        if d2:
            inicio = t + dur - est2 - 0.4
            clips.append((inicio, r2 if s2 else None)); subs += trozos(d2, inicio, t + dur - 0.05)
        t += dur
    video["subs"] = subs
    if not hay_voz:
        return None
    pista = array.array("h", bytes(2 * int(SR * (t + 1))))
    for inicio, ruta in clips:
        if not ruta:
            continue
        with wave.open(str(ruta)) as w:
            datos = array.array("h", w.readframes(w.getnframes()))
        k = int(inicio * SR)
        for j, v in enumerate(datos):
            if k + j < len(pista):
                pista[k + j] = v
    # Apertura de boca por cuadro (30 fps) según el volumen de la voz
    paso, boca = SR // 30, []
    for f in range(int(t * 30) + 1):
        seg = pista[f * paso:(f + 1) * paso]
        rms = math.sqrt(sum(v * v for v in seg) / len(seg)) if seg else 0
        boca.append(rms)
    mx = max(boca) or 1
    video["voz"] = [round(min(1, (b / mx) * 1.6), 2) if b / mx > .08 else 0 for b in boca]
    salida = carpeta / "voz.wav"
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pista.tobytes())
    return salida


def renderizar(turno, salida):
    video = turno["video"]
    voz = preparar_voz(video, salida.parent) if video.get("mascota") else None
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
        if voz:   # música más baja + voz de Rebi encima
            mezcla = salida.with_name("mezcla.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-i", str(voz), "-filter_complex",
                            "[0]volume=0.28[m];[1]aresample=48000,volume=1.9,pan=stereo|c0=c0|c1=c0[v];[m][v]amix=inputs=2:duration=first:normalize=0",
                            str(mezcla)], check=True)
            mezcla.replace(wav)
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
    for f in salida.parent.glob("voz*.wav"):
        f.unlink()
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
