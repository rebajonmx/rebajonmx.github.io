# Plan de continuidad y crecimiento (sin Claude, 100% gratis)

Escrito el 11 nov 2026. A partir del 17 nov 2026 el proyecto sigue sin Claude: el sistema corre solo en GitHub
y cualquier IA gratuita (o tú) puede mantenerlo con este repositorio. **Nada depende de una IA para funcionar a diario.**

## 1. Quién hace qué (reparto de trabajo)

| Trabajo | Quién / herramienta (gratis) | Frecuencia |
|---|---|---|
| Revisar ofertas, armar página, crear y publicar videos | **GitHub Actions** (automático, sin IA) | 2 veces al día |
| Auditoría | **GitHub Actions** → `ESTADO.md` + correo si falla | 2 veces al día |
| Agregar/actualizar ofertas | **Tú**: pegar links en `data/links.txt` (5 min) | 2-3 veces por semana |
| Ideas de videos nuevos | **Tú** (una frase en `contenido/pedido.txt`) + **Gemini API** (lo convierte solo) | Cuando quieras |
| Cambios al código, arreglos, funciones nuevas | **Jules** (agente de Google, plan gratis, trabaja directo en GitHub) | Cuando haga falta |
| Textos, estrategia, preguntas, imágenes | **App de Gemini** (gemini.google.com, gratis) | Cuando haga falta |
| Imágenes sueltas (portadas, historias) | **Gemini (imágenes)** o **Canva gratis** | Opcional |
| Videos | **El motor propio** (`plantilla/motor.js`): no necesita IA de video | Automático |

### ¿Cuál es la mejor IA gratuita para continuar?
1. **Jules (jules.google.com) — la principal para el código.** Es un agente gratuito de Google que se conecta a tu
   GitHub, lee el repositorio (incluido `AGENTS.md`), hace los cambios y te propone un "pull request" para aprobar.
   Plan gratis: unas 15 tareas al día (verifica límites actuales en su página). Inicia sesión con mxrebajon@gmail.com
   y conecta el repositorio `rebajonmx/rebajonmx-auto`.
2. **Gemini (gemini.google.com) — para ideas, textos, imágenes y dudas.** Pégale `AGENTS.md` y lo que necesites.
3. **Gemini API (aistudio.google.com/apikey) — dentro del sistema.** Llave gratis para modelos Flash; la usa
   `ideas_gemini.py`. Google ha ido cambiando sus llaves y límites en 2026: si deja de funcionar, crea una llave
   nueva en AI Studio (con restricción a "Generative Language API") y reemplaza el secreto `GEMINI_API_KEY`.
4. **GitHub Copilot Free** (dentro de github.com) — alternativa para preguntas sobre el código.

Por qué no hace falta una IA de video: los videos se generan con código propio (gratis, sin límites, mismo estilo
siempre). Una IA de video gratuita da pocos segundos al día y estilo inconsistente. Úsala solo para experimentos.

## 2. Antes del 17 de noviembre (con Claude)

- [x] Sistema automático: ofertas → página → video → Instagram/Facebook/TikTok → auditoría.
- [x] Motor de videos con conceptos y 3 colores; 10 conceptos nuevos.
- [x] Documentación: `README.md`, `AGENTS.md`, `docs/MANUAL.md`, `docs/CONCEPTOS.md`, `docs/PROMPTS.md`, este plan.
- [ ] Más ofertas para el Buen Fin (meta 30-40) con links de afiliado.
- [ ] Llave de Gemini (`GEMINI_API_KEY`) y prueba de `pedido.txt`.
- [ ] Canal de Telegram + secretos.
- [ ] App de Mercado Libre (`ML_CLIENT_ID/SECRET`) y prueba de "solo pegar links".
- [ ] Cambiar la llave de Buffer (quedó visible en una captura) y borrar las llaves viejas.
- [ ] Conectar Jules al repositorio y hacer una tarea de prueba pequeña.

## 3. Rutina semanal (15 minutos, sin IA)

1. Abrir `ESTADO.md`. Si está 🔴 o 🟡, seguir lo que dice (o pedirle a Jules: ver `docs/PROMPTS.md`).
2. Actualizar precios y agregar 5-10 ofertas nuevas en `data/links.txt`.
3. Revisar en Buffer → Analytics qué videos tuvieron más vistas; anotar el concepto y color ganador.
4. Escribir 2-3 ideas nuevas en `contenido/pedido.txt` parecidas a lo que funcionó.

## 4. Calendario de campañas (cambia `campana` en `config/marca.json`)

| Fecha | Campaña | Hashtags sugeridos |
|---|---|---|
| 13-17 nov | Buen Fin | #buenfin |
| 1-24 dic | Regalos de Navidad | #navidad #regalos |
| 26 dic-6 ene | Reyes Magos | #reyesmagos #juguetes |
| enero | Cuesta de enero / regreso a clases | #cuestadeenero #ahorro |
| febrero | San Valentín | #sanvalentin |
| mayo/junio | Hot Sale (verificar fechas oficiales) | #hotsale |
| julio | Ofertas de verano / Prime Day (verificar) | #ofertas |
| agosto | Regreso a clases | #regresoaclases |
| fuera de campaña | Ofertas de la semana | #ofertas #descuentos |

## 5. Ideas de crecimiento (todas gratis), por prioridad

1. **Más canales automáticos:** Telegram (ya programado). YouTube Shorts se puede automatizar con la API gratuita de
   YouTube desde GitHub Actions (tarea para Jules: `docs/PROMPTS.md`). Buffer gratis solo permite 3 redes.
2. **Tráfico de Google (SEO):** generar una página por categoría y por oferta (`/tecnologia/`, `/hogar/`…) con
   `sitemap.xml` y darlas de alta en Google Search Console. Trae visitas sin pagar anuncios.
3. **Medir clics:** agregar Cloudflare Web Analytics o GoatCounter (gratis) a la página para saber qué ofertas
   generan más clics y priorizarlas en videos.
4. **Métricas automáticas de videos:** leer de la API de Buffer las vistas de cada publicación y guardarlas en
   `data/historial.json`; luego `contenido.py` puede elegir más seguido los conceptos/colores ganadores.
5. **Más tiendas:** Amazon Afiliados y otras tiendas mexicanas con programa de afiliados. Solo cambia el link y
   la etiqueta de tienda (agregar campo `tienda` a `links.txt`).
6. **Más tipos de video:** encuesta, "antes vs. después", cuenta regresiva animada, carrusel de imágenes.
7. **Clientes:** cada cliente = copia del repositorio + su `config/marca.json` + su Netlify y Buffer (ver MANUAL §10).
   Ofrecer el servicio a tiendas o creadores que quieran su propia página de ofertas automatizada.
8. **Correo/boletín:** cuando haya audiencia, un boletín semanal gratis (por ejemplo, plan gratis de un servicio
   de boletines) con las mejores ofertas.

## 6. Riesgos y qué hacer

| Riesgo | Señal | Acción |
|---|---|---|
| Vence o se revoca la llave de Buffer | ESTADO 🔴 "Falló la publicación" | Nueva llave en Buffer → reemplazar `BUFFER_API_KEY` |
| Una red desconecta su cuenta en Buffer | Error en el paso 5 con el nombre de la red | Buffer → Channels → reconectar |
| Pocas ofertas vigentes | ESTADO 🟡/🔴 | Agregar links / actualizar precios |
| Cambian límites gratuitos (Gemini, GitHub, Buffer, Netlify) | Errores de cuota | Revisar páginas oficiales; el sistema funciona sin Gemini |
| GitHub pausa horarios tras 60 días sin cambios | No corre a la hora | Actions → habilitar flujo (los commits automáticos lo evitan) |
| Mercado Libre cambia su API | Paso 1 con error de API | Seguir con precios manuales; pedir a Jules que ajuste `mercadolibre.py` |
