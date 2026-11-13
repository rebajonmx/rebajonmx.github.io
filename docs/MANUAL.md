# Manual de operación (para personas)

Todo se hace desde el navegador en **github.com/rebajonmx/rebajonmx-auto**. No necesitas instalar nada.
Para editar un archivo: ábrelo → botón del lápiz ✏️ → cambia → **Commit changes**.

## 1. Lo diario (no hay que hacer nada)

GitHub corre el sistema solo a las **7:00 a. m. y 7:00 p. m.** (hora de CDMX). Durante una campaña (fechas en
`config/marca.json`) también a las **12:00 p. m. y 5:00 p. m.** (para apagarlo: `"publicaciones_extra_en_campana": false`):
ofertas → página → video nuevo → Instagram, Facebook y TikTok (vía Buffer) → Telegram (si está activo) → auditoría.

## 2. Auditar en 10 segundos

Abre **`ESTADO.md`** en el repositorio:
- 🟢 TODO BIEN · 🟡 BIEN, CON AVISOS (algo conviene atender) · 🔴 REVISAR (algo falló).
- Si algo falla, GitHub también manda un correo a mxrebajon@gmail.com ("Run failed").
- Para ver el detalle: pestaña **Actions** → la última ejecución → el paso en rojo.

## 3. Agregar, cambiar o quitar ofertas (copiar y pegar)

**Lo más fácil: usa las sugerencias.** Cada lunes y jueves el sistema busca solo (API de Mercado Libre) los productos
más vendidos con 25% o más de descuento y los deja en **`data/sugerencias.md`**, cada uno con su renglón listo.
Para agregar uno:

1. Mercado Libre → **Mi cuenta → Afiliados y creadores** → en "Busca productos" escribe el nombre →
   en el producto: **Compartir → Copiar link** (link de afiliado, empieza con `https://meli.la/`).
2. En `data/sugerencias.md` copia el renglón gris del producto (botón de copiar).
3. Abre **`data/links.txt`** → lápiz ✏️ → pega el renglón al final → cambia `PEGA_AQUI_TU_LINK` por tu link → **Commit changes**.

**Formato de cada renglón** (una oferta por renglón):
```
link de afiliado | categoría | precio antes | precio ahora | nombre corto | foto | calificación | vendidos | URL del producto
https://meli.la/abc123 | Hogar | 999 | 499 | Freidora de aire 5 L | https://http2.mlstatic.com/....webp | 4.8 | 10mil | https://www.mercadolibre.com.mx/p/MLM123
```
- **Siempre** usa el link de "Compartir → Copiar link" de la Central de afiliados: es el que te paga comisión.
  No armes links a mano.
- La **URL del producto** (columna 9) es la dirección normal del producto en Mercado Libre (la que tiene `/p/MLM…`).
  Con ella el sistema actualiza solo precio y foto 2 a 4 veces al día. El link corto `meli.la` no sirve para esto porque
  abre tu perfil de afiliado, no el producto.
- Sin URL del producto, el precio que escribas vale 10 días; después la oferta se oculta hasta que lo actualices.
- Una oferta se publica solo si tiene **15% o más** de descuento. Si el precio sube y deja de ser oferta, se oculta sola.
- Quitar: borra el renglón o ponle `#` al inicio. Un renglón que no empieza con `http` se ignora.
- Los cambios salen en la siguiente ejecución. Para verlos ya: Actions → "Rebajón MX automático" → **Run workflow**
  (desmarca "¿Publicar en redes?" si solo quieres actualizar la página).

## 4. Videos: ideas nuevas

- **Opción fácil (con Gemini gratis):** escribe la idea en `contenido/pedido.txt`, un renglón, por ejemplo
  `video en rosa con 3 errores que comete la gente en el Buen Fin`. Al guardar, GitHub crea el concepto solo.
- **A mano:** copia un archivo de `contenido/conceptos/`, cámbiale el `id` y los textos. Guía: `docs/CONCEPTOS.md`.
- **Pausar un video:** en su archivo pon `"activo": false`.
- **Forzar un video y color hoy:** Actions → Run workflow → escribe el concepto (ej. `oferta-del-dia`) y el color.
- El sistema reparte solo los colores (azul, blanco, rosa) y nunca repite el concepto anterior.

## 5. Métricas: qué funciona mejor

`ESTADO.md` y `data/historial.json` guardan qué concepto y color salió en cada fecha.
Una vez por semana: abre Buffer → **Analytics** (o las estadísticas de cada red), mira las visualizaciones de cada video
y cruza con el historial. Lo que funcione mejor: haz más conceptos parecidos o limita colores con `"temas"`.

## 6. WhatsApp y Telegram

- **WhatsApp:** los canales de WhatsApp **no permiten** publicar en automático de forma oficial (las herramientas no oficiales
  pueden hacer que bloqueen el número). El texto listo del día queda en la página: `rebajonmx.github.io/whatsapp.txt`.
  Recomendación: fija en el canal un mensaje invitando al canal de Telegram y a la página.
- **Telegram (100% automático y gratis):**
  1. En Telegram crea un canal público (ej. `@rebajonmx`).
  2. Abre **@BotFather** → `/newbot` → copia el token.
  3. Agrega el bot a tu canal como **administrador**.
  4. En GitHub: Settings → Secrets and variables → Actions → New repository secret:
     `TELEGRAM_BOT_TOKEN` = el token, `TELEGRAM_CHAT_ID` = `@rebajonmx`.
  5. En `config/marca.json` pon el link del canal en `"telegram"` (así sale en videos y textos).

## 7. API de Mercado Libre (ya está activa)

App de desarrollador **"Rebajon MX Ofertas"** (Client ID 7642238823271133) en developers.mercadolibre.com.mx con la
cuenta de Samuel. Secretos `ML_CLIENT_ID` y `ML_CLIENT_SECRET` ya guardados en GitHub.
- Actualiza precio, foto y nombre de cada oferta con URL del producto, y genera `data/sugerencias.md`.
- Si algún día falla (el paso "1. Ofertas" dice "Mercado Libre no dio acceso"): developers.mercadolibre.com.mx →
  Mis aplicaciones → la app → copiar de nuevo el **Client Secret** → GitHub → Settings → Secrets → `ML_CLIENT_SECRET` → Update.
- Sugerencias a mano: Actions → "Sugerencias de ofertas" → Run workflow.

## 8. Llaves y secretos (GitHub → Settings → Secrets and variables → Actions)

| Secreto | Para qué | Obligatorio |
|---|---|---|
| (ninguno) | La página se publica con GitHub Pages: el repositorio debe ser público y Settings → Pages → Source = "GitHub Actions". Netlify se dejó el 12-nov-2026 (plan gratis sin créditos) | — |
| `BUFFER_API_KEY` | Publicar en Instagram, Facebook y TikTok | Sí |
| `ML_CLIENT_ID`, `ML_CLIENT_SECRET` | Precios automáticos y sugerencias de Mercado Libre | Sí (ya están) |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Canal de Telegram | No |
| `GEMINI_API_KEY` | Convertir ideas en videos (gratis en aistudio.google.com/apikey) | No |

Al copiar llaves usa el botón de copiar de cada página y revisa que se peguen letras y números (no puntitos ••••).
La llave de Buffer vence en noviembre de 2027: crea otra en Buffer → Settings → API y reemplázala igual.

## 9. Cambiar colores, textos de marca o campaña

Todo está en **`config/marca.json`**: nombre, logo, página, WhatsApp, Telegram, hashtags, descuento mínimo,
fechas de la campaña (ej. Buen Fin, Hot Sale, Navidad) y los colores de cada tema. Para una campaña nueva cambia
`campana` (nombre, inicio, fin) y los hashtags.

## 10. Otro cliente o marca (escalar)

1. En GitHub: **Use this template** / o "Fork" del repositorio con otro nombre.
2. Cambia `config/marca.json` y `data/links.txt` del nuevo cliente.
3. Copia el repositorio con el nombre `<usuario>.github.io`, activa Pages (GitHub Actions) y crea una cuenta de Buffer para el cliente; agrega sus secretos (sección 8).
Cada cliente queda separado y gratis (GitHub Actions gratis en repos privados: 2,000 minutos/mes; cada ejecución usa ~5).

## 11. Problemas comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| ESTADO 🔴 "Falló la publicación (Buffer)" | Llave de Buffer vencida o mal pegada | Crea otra llave y reemplaza `BUFFER_API_KEY` |
| "Solo hay N ofertas vigentes" | Precios vencidos o pocas ofertas | Actualiza precios o agrega links en `links.txt` |
| Video con emojis en lugar de fotos | No se pudo descargar la foto | Normal si pasa a veces; con la API de ML mejora |
| No corrió a la hora | GitHub a veces se retrasa unos minutos; tras 60 días sin cambios en el repo pausa los horarios | Actions → habilitar de nuevo |
