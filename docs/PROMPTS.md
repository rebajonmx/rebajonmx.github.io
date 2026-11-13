# Instrucciones listas para copiar y pegar en una IA gratuita

Úsalas en **Jules** (jules.google.com, conectado al repositorio `rebajonmx/rebajonmx-auto`) para cambios de código,
o en **Gemini** (gemini.google.com) para ideas y textos. Copia el bloque completo y cambia lo que está entre [corchetes].

## Regla para cualquier IA (pégala siempre al inicio)

```
Antes de cambiar algo, lee AGENTS.md completo y respeta sus "Reglas que no se rompen".
Haz el cambio más pequeño posible, no agregues servicios de pago, no guardes llaves en archivos,
y al terminar actualiza la sección "Estado actual" de AGENTS.md con lo que cambiaste.
Prueba con: Actions → "Rebajón MX automático" → Run workflow sin publicar.
```

## 1. Arreglar un error (cuando ESTADO.md está 🔴)

```
El sistema falló. Esto dice ESTADO.md: [pega el contenido]
Y este es el registro del paso que falló en GitHub Actions: [pega el texto del paso en rojo]
Encuentra la causa y corrígela. Si la causa es una llave vencida o una cuenta desconectada,
no cambies código: dime exactamente qué debo hacer yo y dónde.
```

## 2. Crear un video nuevo a partir de una idea (Gemini)

```
Lee este formato y crea UN concepto de video en JSON para la idea: [tu idea, por ejemplo
"video en rosa: 3 errores que comete la gente en el Buen Fin"].
[pega aquí el contenido de docs/CONCEPTOS.md]
Responde solo con el JSON. Textos cortos, español de México, sin datos inventados.
```
Luego en GitHub: `contenido/conceptos` → Add file → Create new file → nombre `[id].json` → pega → Commit.

## 3. Campaña nueva (Navidad, Hot Sale, etc.)

```
Cambia la campaña a [nombre] del [fecha inicio AAAA-MM-DD] al [fecha fin] en config/marca.json,
actualiza los hashtags a [hashtags], y crea 4 conceptos nuevos en contenido/conceptos para esa campaña
(uno con temporada "antes", dos "durante", uno "siempre") siguiendo docs/CONCEPTOS.md.
Desactiva (activo: false) los conceptos que solo aplican al Buen Fin.
```

## 4. Nuevo tipo de escena para los videos

```
Agrega un tipo de escena llamado "[nombre]" que muestre [descripción]. Debe funcionar en los 3 temas
(azul, blanco, rosa), respetar la zona segura (y=440 a y=1480) y documentarse en docs/CONCEPTOS.md y en
TIPOS de scripts/ideas_gemini.py. Crea un concepto de ejemplo que lo use y pruébalo sin publicar.
```

## 5. Publicar también en YouTube Shorts (crecimiento)

```
Agrega publicación automática a YouTube Shorts usando la API oficial de YouTube (gratis) desde GitHub Actions:
script scripts/publicar_youtube.py que suba public/media/<archivo>.mp4 con el título y la descripción de
turno.json (agregando #Shorts). Usa secretos YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN; si no existen,
que no haga nada. Agrega el paso al flujo con continue-on-error y documenta en docs/MANUAL.md cómo obtener
esos secretos paso a paso para una persona sin conocimientos técnicos.
```

## 6. SEO: páginas por categoría

```
Haz que construir_sitio.py genere además una página por categoría (public/<categoria>/index.html) con las
mismas tarjetas y un sitemap.xml con todas las páginas. Mantén el diseño actual de plantilla/sitio.html.
Documenta en docs/MANUAL.md cómo dar de alta el sitemap en Google Search Console.
```

## 7. Métricas automáticas

```
Agrega un script que lea de la API de Buffer (https://developers.buffer.com) las estadísticas de las
publicaciones guardadas en data/historial.json (campo buffer con ids) y guarde las vistas en el historial.
Después, en contenido.py, da más probabilidad a los conceptos y colores con más vistas promedio
(sin dejar de probar los demás al menos 1 de cada 4 veces). Muestra un resumen en ESTADO.md.
```

## 8. Nuevo cliente

```
Quiero usar este sistema para otro cliente: [nombre, página, colores, redes, tienda].
Dime paso a paso qué cuentas crear (GitHub, Buffer) y prepara el contenido de config/marca.json
y un data/links.txt de ejemplo para ese cliente. No modifiques el repositorio de Rebajón MX.
```
