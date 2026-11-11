# Contexto para cualquier IA (Gemini, Claude, ChatGPT…) que trabaje en este repositorio

Lee este archivo completo antes de cambiar algo. Aquí está todo lo necesario; no hace falta historial de chats.

## Qué es

**Rebajón MX** es una página de ofertas verificadas de Mercado Libre para México (programa de afiliados:
cada oferta usa un link de afiliado `meli.la/...`). Página: https://rebajonmx.netlify.app.
Gana dinero por comisiones de afiliado. **Presupuesto: $0** — todo debe seguir siendo gratis.
Dueño: opera desde el navegador y quiere intervención humana e IA **mínimas**: el sistema debe correr solo.

## Arquitectura (todo gratis)

```
data/links.txt  (lo único que edita una persona: links de afiliado)
      │
GitHub Actions  (.github/workflows/rebajon.yml, 7:00 y 19:00 CDMX = 13:00 y 01:00 UTC)
  1 actualizar_ofertas.py  links.txt → data/ofertas.json (API oficial de Mercado Libre si hay secretos; si no, precios manuales)
  2 construir_sitio.py     plantilla/sitio.html + ofertas → public/index.html y public/whatsapp.txt
  3 generar_video.py       contenido.py elige concepto+color → plantilla/motor.js dibuja en Chromium (Playwright)
                           cuadro por cuadro → ffmpeg → public/media/video-AAAAMMDD-HHMM.mp4 + turno.json
  4 Netlify CLI            publica public/ (página + video) en rebajonmx.netlify.app
  5 publicar_buffer.py     API de Buffer (GraphQL, api.buffer.com) → Reel en Instagram, Reel en Facebook, video en TikTok
  6 publicar_telegram.py   canal de Telegram (opcional)
  7 auditar.py             revisa todo → ESTADO.md (falla si hay problema grave → GitHub manda correo)
  8 commit                 guarda ofertas.json, historial.json, pendientes.json, ESTADO.md
.github/workflows/ideas.yml: al guardar contenido/pedido.txt, ideas_gemini.py convierte ideas en conceptos (Gemini gratis).
```

## Mapa de archivos

| Archivo | Qué hace / reglas |
|---|---|
| `config/marca.json` | **Única** configuración por marca/cliente: nombre, logo, web, WhatsApp, Telegram, hashtags, descuento mínimo, vigencia de precios, campaña (fechas), redes, colores de temas, modelo de IA. |
| `data/links.txt` | Entrada humana. `link | categoría | precio antes | precio ahora | nombre`. Lo manual manda sobre la API salvo precios cuando hay API. |
| `data/ofertas.json` | Generado. Campos: url, cat, name, now, was, off, img, active, revisado, firma, product, ml_id, ml_tipo, e. No editar a mano. |
| `data/historial.json` | Generado. Cada publicación: fecha, concepto, tema (color), categoria, archivo, ids de Buffer, errores. Base para métricas. |
| `data/pendientes.json` | Generado. Links sin datos completos. |
| `contenido/conceptos/*.json` | Ideas de video (formato en `docs/CONCEPTOS.md`). Crear videos nuevos = crear archivos aquí. |
| `contenido/pedido.txt` | Ideas en una frase para Gemini. |
| `plantilla/motor.js` | Motor de video (canvas 1080x1920, 30 fps, música generada sin derechos). Tipos de escena: gancho, texto, numero, lista, comparacion, producto, cierre. Para un tipo nuevo: agrégalo en `ESC` y `DUR`, documéntalo en CONCEPTOS.md y en `TIPOS` de ideas_gemini.py. |
| `plantilla/sitio.html` | Página (HTML+CSS+JS en un archivo). Marcadores `__DEALS__`, `__FAV__`, `__FECHA__`. |
| `scripts/comun.py` | Utilidades: config, fechas CDMX, carga de ofertas, vigencia, campaña, pie de publicación. |
| `scripts/contenido.py` | Elige concepto+color sin IA (temporada, requisitos, no repetir, reparte colores) y resuelve variables y productos. |
| `scripts/mercadolibre.py` | API oficial de ML (client_credentials). **No** leer páginas de ML desde servidores: ML las bloquea y no se debe intentar rodear el bloqueo. |
| `scripts/auditar.py` | Auditoría sin IA → `ESTADO.md`. |
| `docs/MANUAL.md` | Manual para personas. `docs/CONCEPTOS.md` formato de videos (también se le pasa a Gemini). |
| `docs/PLAN.md` | Plan de continuidad (qué IA gratuita hace qué), rutina semanal, calendario de campañas, ideas de crecimiento y riesgos. |
| `docs/PROMPTS.md` | Instrucciones listas para Jules/Gemini (arreglar errores, campañas, escenas nuevas, YouTube, SEO, métricas, clientes). |

## Reglas que no se rompen

1. **Cada publicación lleva SIEMPRE la página y el WhatsApp** (lo hace `pie_publicacion()` en comun.py). No quitarlo.
2. Solo ofertas reales: descuento ≥ `descuento_minimo` y precio revisado dentro de `dias_vigencia_precio`.
3. Videos: contenido importante entre y=440 y y=1480 (zona visible en el feed de Instagram y libre de botones de TikTok).
   Logo arriba (y≈370). Fluidez: se dibuja cuadro por cuadro (nunca grabar en tiempo real).
4. No reciclar videos: variedad de conceptos y colores (azul, blanco, rosa) para medir qué funciona.
5. Nada de datos inventados, marcas/personajes ajenos ni promesas falsas en los textos.
6. Todo gratis. No agregar servicios de pago. No guardar llaves en archivos: solo en Secrets de GitHub.
7. No automatizar WhatsApp con herramientas no oficiales (riesgo de bloqueo del número) salvo que el dueño lo pida
   expresamente sabiendo el riesgo.
8. La persona dueña no borra/edita a mano `data/*.json` generados; si hay que corregir, se corrige `links.txt` o el script.

## Cómo probar cambios

- Rápido, sin publicar: Actions → "Rebajón MX automático" → Run workflow → desmarcar "¿Publicar en redes?".
- Local (si alguien tiene Python): `pip install requests playwright && playwright install chromium`, tener ffmpeg,
  luego `cd scripts && python actualizar_ofertas.py && python construir_sitio.py && python generar_video.py --concepto oferta-del-dia --tema rosa`.

## Herramientas de IA gratuitas recomendadas (desde el 17 nov 2026 ya no hay Claude)

- **Jules** (jules.google.com): cambios de código directo en este repositorio (lee este archivo).
- **Gemini** (gemini.google.com): ideas, textos, imágenes. **Gemini API** gratis (Flash) dentro de `ideas_gemini.py`.
- Detalle y reparto de trabajo: `docs/PLAN.md`.

## Estado actual (actualízalo al terminar cada cambio importante)

- 2026-11-11: sistema en producción. Buffer conectado a Instagram @rebajonmx, Facebook página Rebajón MX y TikTok @rebajonmx.
  Secretos configurados: NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID, BUFFER_API_KEY.
- Motor v2 con 10 conceptos y 3 colores. Campaña activa: Buen Fin 2026 (13–17 nov).
- 10 ofertas activas con precios manuales en links.txt (sin API de ML todavía).
- Pendiente del dueño (opcional): app de Mercado Libre (ML_CLIENT_ID/SECRET), canal de Telegram, GEMINI_API_KEY,
  más ofertas (meta 30–40 para el Buen Fin), cambiar la llave de Buffer (quedó visible en una captura).
- Por verificar cuando exista la app de ML: que `client_credentials` dé acceso a /items y /products (si no, cambiar
  a flujo authorization_code con refresh token guardado como secreto).

## Ideas siguientes (por prioridad)

1. Leer métricas de cada publicación desde la API de Buffer y agregarlas a `historial.json` para elegir conceptos/colores
   automáticamente según visualizaciones (hoy se reparten parejo).
2. Más tipos de escena (encuesta, antes/después con imagen, cuenta regresiva animada).
3. Carrusel de imágenes además de video.
4. Plantilla de repositorio para clientes nuevos.
