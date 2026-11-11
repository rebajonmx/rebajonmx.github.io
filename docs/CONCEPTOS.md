# Cómo crear un video nuevo (concepto)

Un **concepto** es un archivo `.json` en `contenido/conceptos/`. Describe las escenas del video con textos.
El sistema lo convierte solo en un video vertical de 1080x1920 con música, en el color que toque
(azul, blanco o rosa), y siempre le agrega al final la escena de cierre con la página y WhatsApp.

No hay que programar. Para crear uno: copia un concepto que se parezca, cámbiale el `id` (y el nombre del archivo)
y los textos. O escribe la idea en `contenido/pedido.txt` y deja que Gemini lo arme (ver MANUAL.md).

## Estructura

```json
{
 "id": "errores-buen-fin",
 "nombre": "3 errores del Buen Fin",
 "objetivo": "Para qué sirve este video (solo informativo)",
 "temporada": "siempre",
 "temas": ["rosa"],
 "requiere": {"minimo": 2},
 "publicacion": "Texto de la publicación en redes (1-2 frases). La página, WhatsApp y hashtags se agregan solos.",
 "escenas": [
  {"tipo": "gancho", "emoji": "😱", "titulo": "3 ERRORES", "texto": "que casi todos cometen en el Buen Fin"},
  {"tipo": "numero", "numero": "1", "titulo": "Comprar sin comparar", "texto": "el precio de antes"},
  {"tipo": "producto", "elegir": "top"}
 ]
}
```

| Campo | Obligatorio | Qué es |
|---|---|---|
| `id` | sí | Nombre único en minúsculas-con-guiones. Igual al nombre del archivo. |
| `nombre` | sí | Título corto para identificarlo. |
| `publicacion` | sí | Texto que acompaña al video en Instagram/Facebook/TikTok. |
| `escenas` | sí | Lista de escenas (abajo). Entre 3 y 7 escenas = 10 a 20 segundos. |
| `temporada` | no | `siempre` (por defecto), `antes`, `durante` o `despues` de la campaña de `config/marca.json`. |
| `temas` | no | Colores permitidos: `azul`, `blanco`, `rosa`. Si no se pone, se reparten todos. |
| `requiere` | no | `minimo`: cuántas ofertas necesita; `max_precio`; `por_categoria: true`. Si no se cumple, no se usa ese día. |
| `activo` | no | `false` para pausarlo sin borrarlo. |

## Tipos de escena

| `tipo` | Campos | Se ve así |
|---|---|---|
| `gancho` | `titulo`, `texto`, `emoji`, `etiqueta` | Título gigante que "tiembla" para atrapar en el primer segundo. |
| `texto` | `titulo`, `texto`, `etiqueta` | Título de color + párrafo corto. |
| `numero` | `numero`, `titulo`, `texto` | Un número o dato enorme (ej. "1", "5 días", "$2,000"). |
| `lista` | `titulo`, `items` (3 a 5), `marca` | Lista con palomitas que aparecen una por una. |
| `comparacion` | `titulo`, `izq` y `der` (cada uno con `titulo`, `valor`, `texto`), `texto` | Dos tarjetas lado a lado (antes/después, sin/con). |
| `producto` | `elegir`, `indice`, `categoria` (o `categorias`: lista), `max_precio`, `etiqueta` | Foto del producto, % de descuento y precio animado. |
| `productos` | igual que `producto` + `cuantos` (1 a 5) | Varias escenas de producto seguidas con #1, #2, #3. |
| `cierre` | `titulo`, `titulo2` | Se agrega solo al final. Solo ponlo si quieres cambiar sus títulos. |

Todas aceptan `seg` (duración en segundos) si quieres cambiar la duración normal.
`elegir`: `top` (más descuento), `barato` (precio más bajo), `aleatorio`, `vendidos` (más ventas) o `variado` (rota: cada publicación muestra productos distintos; recomendado para listas).

## Variables que se rellenan solas

Escríbelas entre llaves dentro de cualquier texto: `{campana}` (nombre de la campaña), `{dias}` (días que faltan),
`{dias_restantes}`, `{marca}`, `{web}`, `{tienda}`, `{descuento_minimo}`, `{n_ofertas}`, `{categoria}`,
`{categoria_mayus}`, `{ahorro_top3}`, `{top_nombre}`, `{top_precio}`, `{top_antes}`, `{top_off}`, `{top_ahorro}`.

## Reglas de estilo (para personas y para IA)

- Textos **cortos**: título máximo ~22 caracteres, texto máximo ~70. Se lee en el celular en 2 segundos.
- La primera escena debe ser un `gancho` (detiene el scroll).
- Nada de datos inventados, promesas falsas ni "garantizado". Si das un dato, que sea verificable.
- No nombres marcas ni personajes ajenos en los textos. Las fotos de productos salen solas de las ofertas.
- Siempre aporta valor: ahorrar dinero, evitar trucos o ahorrar tiempo. Tono cercano, español de México.
