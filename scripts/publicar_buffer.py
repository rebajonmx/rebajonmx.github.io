"""Publica el video del turno en Instagram (Reel), Facebook (Reel) y TikTok a la vez, vía Buffer (plan gratis).

Necesita el secreto de GitHub BUFFER_API_KEY (Buffer → Settings → API).
El video debe estar ya publicado en el sitio (Buffer lo descarga desde la URL pública).
Uso: python publicar_buffer.py <n_video> [instagram facebook tiktok]
"""
import os, sys, time, requests
from comun import WEB, activas, caption

API = "https://api.buffer.com"


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
        res += gql("query($o: OrganizationId!) { channels(input: {organizationId: $o}) { id service name isQueuePaused } }",
                   {"o": o["id"]})["channels"]
    return res


CREAR = """mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id } }
    ... on MutationError { message }
  }
}"""

META = {
    "instagram": {"instagram": {"type": "reel", "shouldShareToFeed": True}},
    "facebook": {"facebook": {"type": "reel"}},
    "tiktok": {"tiktok": {"isAiGenerated": False}},
}


def main(n, redes=("instagram", "facebook", "tiktok")):
    if not os.environ.get("BUFFER_API_KEY"):
        print("Sin BUFFER_API_KEY: se omite la publicación.")
        return 0
    url = f"https://{WEB}/media/video-{n}.mp4?v={int(time.time())}"
    texto = caption(n, activas())
    fallas = 0
    for c in canales():
        if c["service"] not in redes:
            continue
        entrada = {"text": texto, "channelId": c["id"], "schedulingType": "automatic", "mode": "shareNow",
                   "metadata": META[c["service"]],
                   "assets": [{"video": {"url": url, "metadata": {"thumbnailOffset": 1800}}}]}
        try:
            r = gql(CREAR, {"input": entrada})["createPost"]
            print(f"{c['service']} ({c['name']}):", r.get("post", {}).get("id") or r.get("message"))
            fallas += "post" not in r
        except Exception as e:
            print(f"{c['service']} ({c['name']}): ERROR", str(e)[:300])
            fallas += 1
    return fallas


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sys.exit(1 if main(n, tuple(sys.argv[2:]) or ("instagram", "facebook", "tiktok")) else 0)
"""Publica el video del turno en Instagram (Reel), Facebook (Reel) y TikTok a la vez, vía Buffer (plan gratis).

Necesita el secreto de GitHub BUFFER_API_KEY (Buffer → Settings → API).
El video debe estar ya publicado en el sitio (Buffer lo descarga desde la URL pública).
Uso: python publicar_buffer.py <n_video> [instagram facebook tiktok]
"""
import os, sys, time, requests
from comun import WEB, activas, caption

API = "https://api.buffer.com"


def gql(query, variables=None):
    r = requests.post(API, json={"query": query, "variables": variables or {}}, timeout=60,
                      headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}"})
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]


def canales():
    orgs = gql("query { account { organizations { id } } }")["account"]["organizations"]
    res = []
    for o in orgs:
        res += gql("query($o: OrganizationId!) { channels(input: {organizationId: $o}) { id service name isQueuePaused } }",
                   {"o": o["id"]})["channels"]
    return res


CREAR = """mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id } }
    ... on MutationError { message }
  }
}"""

META = {
    "instagram": {"instagram": {"type": "reel", "shouldShareToFeed": True}},
    "facebook": {"facebook": {"type": "reel"}},
    "tiktok": {"tiktok": {"isAiGenerated": False}},
}


def main(n, redes=("instagram", "facebook", "tiktok")):
    if not os.environ.get("BUFFER_API_KEY"):
        print("Sin BUFFER_API_KEY: se omite la publicación.")
        return 0
    url = f"https://{WEB}/media/video-{n}.mp4?v={int(time.time())}"
    texto = caption(n, activas())
    fallas = 0
    for c in canales():
        if c["service"] not in redes:
            continue
        entrada = {"text": texto, "channelId": c["id"], "schedulingType": "automatic", "mode": "shareNow",
                   "metadata": META[c["service"]],
                   "assets": [{"video": {"url": url, "metadata": {"thumbnailOffset": 1800}}}]}
        try:
            r = gql(CREAR, {"input": entrada})["createPost"]
            print(f"{c['service']} ({c['name']}):", r.get("post", {}).get("id") or r.get("message"))
            fallas += "post" not in r
        except Exception as e:
            print(f"{c['service']} ({c['name']}): ERROR", str(e)[:300])
            fallas += 1
    return fallas


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sys.exit(1 if main(n, tuple(sys.argv[2:]) or ("instagram", "facebook", "tiktok")) else 0)
