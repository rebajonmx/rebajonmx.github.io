"""Convierte ideas cortas (contenido/pedido.txt) en conceptos de video listos, usando Gemini (gratis).

Escribe una idea por renglón en contenido/pedido.txt, por ejemplo:
    video en rosa con 3 errores que comete la gente en el Buen Fin
Este script (lo corre GitHub solo al guardar pedido.txt) pide a Gemini un concepto en el formato de
docs/CONCEPTOS.md, lo valida y lo guarda en contenido/conceptos/<id>.json. El renglón queda marcado como HECHO.
Necesita el secreto GEMINI_API_KEY (gratis en https://aistudio.google.com/apikey). Sin él no hace nada.
"""
import json, os, re, requests
from comun import RAIZ, CONFIG

PEDIDO = RAIZ / "contenido" / "pedido.txt"
CONCEPTOS = RAIZ / "contenido" / "conceptos"
TIPOS = {"gancho", "texto", "numero", "lista", "comparacion", "producto", "productos", "cierre"}


def validar(c):
    errores = [f"falta '{k}'" for k in ("id", "nombre", "publicacion", "escenas") if not c.get(k)]
    for i, e in enumerate(c.get("escenas", [])):
        if e.get("tipo") not in TIPOS:
            errores.append(f"escena {i + 1}: tipo '{e.get('tipo')}' no existe")
        if e.get("tipo") == "lista" and not e.get("items"):
            errores.append(f"escena {i + 1}: la lista no tiene items")
    if c.get("temas") and not set(c["temas"]) <= set(CONFIG["temas"]):
        errores.append("temas no válidos")
    return errores


def pedir(idea, key):
    guia = (RAIZ / "docs" / "CONCEPTOS.md").read_text(encoding="utf-8")
    ejemplos = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(CONCEPTOS.glob("*.json"))[:2]]
    prompt = (f"Eres el creador de contenido de {CONFIG['nombre']} ({CONFIG['web']}), una página de ofertas verificadas "
              f"de {CONFIG['tienda']} en México. Crea UN concepto de video corto vertical para esta idea:\n\n«{idea}»\n\n"
              f"Sigue EXACTAMENTE este formato (guía y reglas):\n{guia}\n\nEjemplos válidos:\n"
              f"{json.dumps(ejemplos, ensure_ascii=False)}\n\nResponde solo con el JSON del concepto, en español de México, "
              "con textos cortos y llamativos. No inventes datos falsos ni promesas. El id en minúsculas-con-guiones.")
    modelo = CONFIG.get("ia", {}).get("modelo", "gemini-flash-latest")
    r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                      params={"key": key}, timeout=120,
                      json={"contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.9}})
    r.raise_for_status()
    texto = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(texto)


def main():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print("Sin GEMINI_API_KEY: se omite. (También puedes crear conceptos a mano, ver docs/CONCEPTOS.md)")
        return
    lineas = PEDIDO.read_text(encoding="utf-8").splitlines()
    for i, l in enumerate(lineas):
        idea = l.strip()
        if not idea or idea.startswith("#"):
            continue
        try:
            c = pedir(idea, key)
            c["id"] = re.sub(r"[^a-z0-9-]", "", c.get("id", "").lower().replace(" ", "-"))[:50] or f"idea-{i}"
            errores = validar(c)
            if errores:
                lineas[i] = f"# ERROR ({'; '.join(errores)[:120]}): {idea}"
                continue
            c.setdefault("temporada", "siempre")
            c["origen"] = f"Gemini a partir de: {idea}"
            (CONCEPTOS / f"{c['id']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            lineas[i] = f"# HECHO → contenido/conceptos/{c['id']}.json: {idea}"
            print("  ✓", c["id"])
        except Exception as e:
            lineas[i] = f"# ERROR ({str(e)[:100]}): {idea}"
    PEDIDO.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
