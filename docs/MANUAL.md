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

## 3. Agregar, cambiar o quitar ofertas

Edita **`data/links.txt`**. Una oferta por renglón:

```
link | categoría | precio antes | precio ahora | nombre corto | foto | calificación | vendidos
https://meli.la/abc123 | Hogar | 999 | 499 | Freidora de aire 5 L | https://http2.mlstatic.com/....webp | 4.8 | 10mil
```
- Las 3 últimas son opcionales pero recomendadas: sin foto el video usa un emoji.
- **Cómo sacar los datos rápido:** Mercado Libre → Afiliados y creadores → buscar el producto → **Compartir → Copiar link**
  (ese es el link de afiliado). Para la foto: abre el producto, clic derecho en la foto → *Copiar dirección de imagen*.
- Con la API de Mercado Libre activada (sección 7) basta con pegar el link.
- Sin la API, escribe los 5 datos. Cuando cambien los precios, actualízalos (cuentan como revisados ese día).
- Una oferta se publica solo si tiene **15% o más** de descuento y precio revisado en los últimos **10 días**.
- Quitar: borra el renglón o ponle `#` al inicio.
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
  pueden hacer que bloqueen el número). El texto listo del día queda en la página: `rebajonmx.netlify.app/whatsapp.txt`.
  Recomendación: fija en el canal un mensaje invitando al canal de Telegram y a la página.
- **Telegram (100% automático y gratis):**
  1. En Telegram crea un canal público (ej. `@rebajonmx`).
  2. Abre **@BotFather** → `/newbot` → copia el token.
  3. Agrega el bot a tu canal como **administrador**.
  4. En GitHub: Settings → Secrets and variables → Actions → New repository secret:
     `TELEGRAM_BOT_TOKEN` = el token, `TELEGRAM_CHAT_ID` = `@rebajonmx`.
  5. En `config/marca.json` pon el link del canal en `"telegram"` (así sale en videos y textos).

## 7. API de Mercado Libre (para pegar solo links)

Mercado Libre bloquea la lectura de sus páginas desde servidores; con su API oficial gratuita no.
1. Entra a **developers.mercadolibre.com.mx** con tu cuenta de Mercado Libre → "Crear aplicación".
2. Nombre: Rebajón MX · URL de redirección: `https://rebajonmx.netlify.app` · Permisos: solo lectura.
3. Copia el **Client ID** y el **Client Secret**.
4. En GitHub agrega los secretos `ML_CLIENT_ID` y `ML_CLIENT_SECRET`.
5. Corre el flujo a mano y revisa el paso "1. Ofertas": debe decir "API de Mercado Libre: sí".

## 8. Llaves y secretos (GitHub → Settings → Secrets and variables → Actions)

| Secreto | Para qué | Obligatorio |
|---|---|---|
| `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID` | Publicar la página | Sí |
| `BUFFER_API_KEY` | Publicar en Instagram, Facebook y TikTok | Sí |
| `ML_CLIENT_ID`, `ML_CLIENT_SECRET` | Datos automáticos de Mercado Libre | No |
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
3. Crea un sitio en Netlify y una cuenta de Buffer para el cliente; agrega sus secretos (sección 8).
Cada cliente queda separado y gratis (GitHub Actions gratis en repos privados: 2,000 minutos/mes; cada ejecución usa ~5).

## 11. Problemas comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| ESTADO 🔴 "Falló la publicación (Buffer)" | Llave de Buffer vencida o mal pegada | Crea otra llave y reemplaza `BUFFER_API_KEY` |
| "Solo hay N ofertas vigentes" | Precios vencidos o pocas ofertas | Actualiza precios o agrega links en `links.txt` |
| Video con emojis en lugar de fotos | No se pudo descargar la foto | Normal si pasa a veces; con la API de ML mejora |
| No corrió a la hora | GitHub a veces se retrasa unos minutos; tras 60 días sin cambios en el repo pausa los horarios | Actions → habilitar de nuevo |
