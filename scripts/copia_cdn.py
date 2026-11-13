"""Copia el video del turno a un CDN gratis (jsDelivr) para Facebook.

Facebook no logra bajar los videos desde rebajonmx.github.io (Buffer: "Facebook was unable to process the media",
12-nov-2026); Instagram y TikTok sí. Se sube el video a la rama `media` del repositorio (un solo commit que se
reemplaza cada vez, así no crece) y Facebook lo toma de https://cdn.jsdelivr.net/gh/<repo>@<commit>/<archivo>.
Deja VIDEO_URL_FACEBOOK en $GITHUB_ENV; si algo falla, Facebook usa la URL normal de la página.
"""
import os, shutil, subprocess, tempfile, time
import requests
from comun import MEDIA, leer_json


def main():
    turno = leer_json(MEDIA / "turno.json", None)
    if not turno or not (MEDIA / turno.get("archivo", "-")).exists():
        print("No hay video del turno: se omite.")
        return
    a, repo, token = turno["archivo"], os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_TOKEN"]
    d = tempfile.mkdtemp()
    shutil.copy(MEDIA / a, os.path.join(d, a))

    def git(*c):
        return subprocess.run(["git", "-C", d, *c], check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q")
    git("checkout", "-q", "-b", "media")
    git("add", a)
    git("-c", "user.name=rebajon-bot", "-c", "user.email=bot@users.noreply.github.com", "commit", "-q", "-m", "video " + a)
    sha = git("rev-parse", "HEAD")
    git("push", "-q", "-f", f"https://x-access-token:{token}@github.com/{repo}.git", "media")
    url = f"https://cdn.jsdelivr.net/gh/{repo}@{sha}/{a}"
    for _ in range(12):   # se "calienta" el CDN para que Facebook lo encuentre listo
        try:
            r = requests.get(url, timeout=90)
            if r.ok and r.headers.get("content-type", "").startswith("video") and len(r.content) > 10000:
                break
            print("  CDN aún no:", r.status_code, r.headers.get("content-type"))
        except Exception as e:
            print("  CDN aún no:", str(e)[:100])
        time.sleep(10)
    else:
        print("El CDN no respondió: Facebook usará la URL de la página.")
        return
    with open(os.environ["GITHUB_ENV"], "a") as f:
        f.write(f"VIDEO_URL_FACEBOOK={url}\n")
    print("Facebook usará", url)


if __name__ == "__main__":
    main()
