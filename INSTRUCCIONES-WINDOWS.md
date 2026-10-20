# Generador de Lecciones Moodle — versión 2: preguntas desde video

## 1. Descargar y abrir el editor manual

1. Descarga `Generador-Lecciones-Moodle-v2.zip` desde GitHub. Si ves la página del archivo, pulsa **Download raw file** (icono de descarga).
2. Haz clic derecho en el ZIP → **Extraer todo**. No trabajes dentro del ZIP.
3. Abre la carpeta extraída y haz doble clic en **index.html**; selecciona **Microsoft Edge** o **Google Chrome** actualizado.
4. Puedes crear, ordenar, editar, previsualizar y exportar sin instalar herramientas. Conserva juntos index.html, styles.css, core.js y app.js.

Este modo manual no conecta la IA. Para generar preguntas o transcribir usa el modo local siguiente. Los JSON de la primera versión siguen siendo editables; la nueva vista previa aplica un solo intento a todas las preguntas.

## 2. Activar la IA en Windows (solo la primera vez)

### Servicio y costo, antes de configurarlo

La aplicación usa **OpenAI API**, no tu sesión de ChatGPT. La API se paga por uso y su facturación es independiente de ChatGPT Plus u otros planes. Necesitas tu propia cuenta API con saldo o facturación habilitada y acceso a los modelos configurados.

- Generación: `gpt-4.1-mini` por defecto; el costo depende de los tokens del texto y de la respuesta.
- Transcripción: `gpt-transcribe` por defecto. La tarifa publicada consultada el 20 de octubre de 2026 es aproximadamente **USD 0,0045 por minuto**: 10 minutos serían unos USD 0,045 solo de transcripción, más la generación y posibles impuestos. Las tarifas y disponibilidad pueden cambiar.
- Pegar una transcripción evita transcribir audio; generar las preguntas sigue teniendo costo.
- No hay reintentos automáticos de llamadas de IA. Volver a pulsar Generar hace otra solicitud de pago. Una solicitud que falla o se interrumpe puede haber sido procesada y facturada por el proveedor.
- Consulta tarifas y uso en tu cuenta antes de trabajar con videos largos. Configura las alertas y controles de gasto que ofrezca tu cuenta; una alerta no garantiza un límite de gasto estricto.

Fuentes oficiales: [tarifas](https://developers.openai.com/api/docs/pricing), [modelo de transcripción](https://developers.openai.com/api/docs/models/gpt-transcribe), [facturación separada](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform).

### Pasos

1. Instala **Node.js LTS, versión 22 o superior**, desde https://nodejs.org. Usa el instalador de Windows y las opciones predeterminadas. No necesitas ejecutar `npm install`.
2. Crea una clave en tu cuenta de https://platform.openai.com/api-keys. **No la compartas por chat ni la publiques en GitHub.**
3. En la carpeta extraída, copia `config.example.json` y cambia el nombre de la copia a **config.local.json**. En el Explorador, activa **Ver → Mostrar → Extensiones de nombre de archivo** para evitar llamarlo `config.local.json.txt`.
4. Abre **config.local.json** con Bloc de notas. Entre las comillas vacías de `OPENAI_API_KEY`, pega tu clave. Conserva las comillas, comas y llaves. Guarda el archivo. No edites el archivo de ejemplo.
5. Haz doble clic en **INICIAR-IA.cmd**. Mantén abierta la ventana que aparece.
6. Abre **http://127.0.0.1:8765** en Edge o Chrome. La página debe indicar «Servicio local conectado». Si dice que falta la clave, revisa el archivo y cierra/vuelve a abrir INICIAR-IA.cmd.
7. Para cerrar el servidor, vuelve a su ventana y pulsa **Ctrl+C**. No se instala ningún servicio permanente.

Los modelos se pueden cambiar en config.local.json si tu cuenta no tiene acceso a los predeterminados o si el proveedor los retira. El modelo de texto debe admitir Responses API y salidas estructuradas JSON Schema; el de audio debe admitir `/v1/audio/transcriptions` con respuesta JSON. Reinicia tras cambiar la configuración.

### Protección de credenciales y contenido

La clave se usa solo en el servidor local, que escucha en 127.0.0.1, y no se devuelve al navegador. La aplicación sirve únicamente los archivos públicos autorizados, no el archivo de configuración. También puede leer `OPENAI_API_KEY` desde una variable de entorno.

`config.local.json` y archivos .env están excluidos de Git mediante .gitignore. El ZIP de distribución tampoco los incluye. **El archivo local es texto plano**, así que guárdalo en tu perfil privado y no compartas tu carpeta configurada ni la subas manualmente a GitHub: .gitignore no protege las subidas hechas desde la web. Comparte el ZIP original sin clave. Si expones la clave, revócala y crea otra.

Al transcribir, se envía el archivo completo al servicio de OpenAI para obtener su audio transcrito; al generar, se envía el texto de la transcripción y las preferencias. Las imágenes del video no se analizan. No envíes información que no desees compartir con el proveedor. El servidor no guarda archivos de video ni registra claves o transcripciones; el proveedor aplica sus propias políticas. La generación solicita `store:false`, lo cual no equivale a prometer retención cero por parte del proveedor.

El navegador guarda los datos de la lección, incluidas las transcripciones, en su almacenamiento local cuando es posible. El JSON descargado también contiene esas fuentes: revísalo antes de compartirlo.

[Seguridad de claves de OpenAI](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).

## 3. Generar desde contenido real

### Enlace de YouTube

1. Pega el enlace y pulsa **Usar enlace como fuente**.
2. Esta versión **no descarga YouTube ni extrae subtítulos automáticamente**. Te informa de esta limitación; el enlace solo registra la procedencia.
3. Abre el video en YouTube y busca **Mostrar transcripción**, en la descripción o menú si está disponible. Copia su texto y pégalo en **Transcripción editable**.
4. Si no existe transcripción, usa un archivo con audio que ya tengas o transcribe manualmente. Sin contenido textual suficiente la aplicación no genera preguntas. No se usa el título del video para inventarlas.

### Archivo de video o audio

1. Selecciona un archivo **MP4, WebM, MP3, M4A o WAV con voz**, de hasta **24 MB**.
2. Marca que entiendes el envío a OpenAI y su costo.
3. Pulsa **Transcribir audio con IA (de pago)**.
4. Revisa y corrige el texto devuelto. Se transcribe lo que se dice, sin analizar esquemas, fórmulas, textos o acciones que solo se vean en pantalla. Añade manualmente una descripción fiel si es necesaria.
5. Si no hay audio utilizable o la transcripción falla, se muestra el error y puedes pegarla manualmente. Para archivos más grandes, utiliza un fragmento menor o pega la transcripción; no se recorta el video automáticamente.

### Preguntas y objetivos

1. Revisa la fuente: debe contener de **100 a 60000 caracteres**. El mínimo técnico no garantiza contenido suficiente para todas las preguntas.
2. Elige de **1 a 20 preguntas**, dificultad y tipos. «Ambos» requiere al menos dos preguntas para incluir los dos tipos.
3. Pulsa **Proponer preguntas y objetivos**. Con información insuficiente puede rechazarse la propuesta; no se completa con hechos externos.
4. Revisa los objetivos propuestos y edítalos. Se solicitan acciones observables y evaluables mediante las preguntas. La dificultad básica identifica datos; la intermedia relaciona ideas; la avanzada aplica o analiza relaciones sustentadas por la fuente.
5. La propuesta muestra alternativas, respuesta correcta, mensajes, objetivo asociado y una cita textual. El programa verifica que la cita aparezca en la transcripción, pero **no puede garantizar que la IA la interprete bien**: revisa la exactitud y ambigüedad de las preguntas y distractores.
6. Pulsa **Añadir borradores a la secuencia**. Se añaden sin reemplazar las páginas existentes; los objetivos se agregan a los existentes. También puedes descartar la propuesta.
7. Selecciona cada borrador en la secuencia. Edita enunciado, alternativas, respuesta correcta, ambos mensajes y objetivo evaluado.
8. Marca **He revisado esta pregunta…** en cada pregunta generada. Hasta hacerlo no se permite previsualizar ni exportar. Cambiar una pregunta quita su marca de revisión; cambiar los objetivos generales obliga a revisar de nuevo las preguntas de IA.
9. Guarda el JSON editable. Incluye fuentes, evidencia, objetivos, preguntas y su revisión; no incluye el video ni la clave.

## 4. Funciones manuales y guardado

- Completa título, descripción y objetivos de la lección.
- Añade páginas con textos, ejemplos y enlaces YouTube, o preguntas manuales de selección múltiple y verdadero/falso.
- Selección múltiple admite cuatro alternativas y una correcta. Personaliza siempre ambos mensajes; el incorrecto debe explicar el error y señalar la respuesta correcta, sin pedir que se reintente.
- Ordena con ↑ y ↓ y selecciona un elemento para editarlo. Eliminar pide confirmación.
- **Guardar archivo editable** descarga `leccion-editable.json`. **Abrir lección** lo recupera, incluidos los archivos de la versión 1.
- Se intenta guardar automáticamente en el navegador, pero esto no es una copia de seguridad. Descargar el JSON es imprescindible al terminar. El modo privado, cambiar de perfil o cambiar entre file:// y el servidor local cambia el almacenamiento disponible. Abre tu JSON para trasladarlo entre modos.
- No se envían datos de una lección a IA al abrirla o exportarla: solo al pulsar Transcribir o Generar.

## 5. Vista del estudiante: un solo intento

Cada pregunta admite una respuesta: tras acertar o fallar se bloquean todas las alternativas, se muestra la explicación y se habilita **Continuar**. El estudiante puede leer el mensaje a su ritmo antes de avanzar. No hay botón Reintentar, retroceso para volver a contestar ni botón para repetir toda la lección.

Cerrar y volver a abrir la vista previa mantiene el estado de esa prueba. Editar la lección inicia una nueva prueba docente. La simulación no almacena intentos reales de estudiantes ni controla identidades: las restricciones reales deben establecerse en Moodle. No es un sistema de evaluación para distribuir directamente al alumnado.

## 6. Exportar a Moodle 5.0.4+

### Qué hace GIFT

**Descargar preguntas GIFT** crea `preguntas.gift` UTF-8 con preguntas, alternativas, respuesta correcta y retroalimentación. **No es una configuración completa de Lección**: no incluye páginas de contenido, objetivos, videos, reglas de intentos ni saltos personalizados.

1. En un curso de prueba, crea una actividad **Lección**.
2. Usa **Importar preguntas** desde esa Lección, elige GIFT y sube el archivo. Importarlo en el banco de preguntas no lo añade a una Lección.
3. **Descargar guía de contenido** crea una guía HTML con contenidos, objetivos, orden, evidencia y saltos. Ábrela con Edge o Chrome; puedes imprimirla o guardarla como PDF.
4. Copia los contenidos a páginas de Lección y ordénalos según la guía.

### Ajustes obligatorios: dos restricciones distintas

En los ajustes de la Lección (los textos pueden variar con la traducción):

| Ajuste | Valor |
|---|---|
| Número máximo de intentos por pregunta (`maxattempts`) | **1** |
| Proporcionar opción para intentar de nuevo una pregunta (`review`, «displayreview» en la interfaz interna) | **No** |
| Permitir revisión del estudiante (`modattempts`) | **No** |
| Se permite volver a tomar la lección (`retake`) | **No** |
| Acción posterior a una respuesta correcta (`nextpagedefault`) | **Normal: seguir la secuencia** |
| Mostrar menú izquierdo | **No**, para no ofrecer accesos a preguntas anteriores |
| Puntuación personalizada | **Sí**: correcta 1, incorrectas 0 |

El máximo de intentos y la opción de reintentar se refieren a **una pregunta**. `retake` permite repetir **toda la Lección**: es independiente y también debe estar desactivado. Desactivar revisión evita una vía adicional para volver a recorrer respuestas.

### Saltos: hay que cambiarlos tras importar GIFT

El importador estándar puede asignar **Esta página** a respuestas incorrectas. Cámbialo, no basta con importar GIFT:

- Para **cada alternativa**, correcta o incorrecta, el salto será **Página siguiente** o el título exacto del siguiente elemento de la guía.
- En el último elemento, todas las alternativas deben ir a **Fin de la lección**.
- Pega la retroalimentación en el campo **Respuesta** correspondiente de cada alternativa, para verla antes de continuar.
- Las páginas de contenido tendrán su botón Continuar hacia el siguiente elemento.
- Mantén puntuación correcta 1 e incorrecta 0. No marques una incorrecta como correcta para forzar el avance; usa saltos y puntuación personalizada.

Prueba con una cuenta de estudiante: responde mal, lee el mensaje, continúa y comprueba que no se ofrece reintento. Haz lo mismo con una correcta. Termina y vuelve a abrir la actividad para confirmar que Moodle impide una nueva realización. La vista previa del profesor no demuestra que se apliquen las restricciones a estudiantes.

Se verificaron estos campos y el comportamiento del importador en el código de Moodle 5.0.4; **no se hizo una importación en un servidor Moodle real**. Debe comprobarse en tu instalación antes de usarlo con alumnos.

Fuentes: [ajustes de Lección 5.0.4](https://github.com/moodle/moodle/blob/v5.0.4/mod/lesson/mod_form.php), [importador y saltos predeterminados](https://github.com/moodle/moodle/blob/v5.0.4/mod/lesson/format.php).

## 7. Si algo falla

- **No funciona IA al abrir index.html:** abre INICIAR-IA.cmd y visita http://127.0.0.1:8765; el editor manual sigue disponible al abrir el HTML directamente.
- **Windows dice que falta Node:** instala Node.js LTS 22 o superior y vuelve a abrir INICIAR-IA.cmd.
- **Clave no válida / sin saldo / modelo no disponible:** revisa tu cuenta API, los modelos y config.local.json; reinicia. No compartas la clave para pedir ayuda.
- **Puerto ocupado:** cierra otra ventana de INICIAR-IA.cmd; no ejecutes dos copias a la vez.
- **Video grande, sin voz o formato incompatible:** usa un archivo menor compatible o pega la transcripción manualmente.
- **Fuente insuficiente, cita inexistente o propuesta inválida:** revisa el texto, reduce la cantidad o dificultad y vuelve a generar si lo deseas. Cada nueva solicitud puede tener costo. El sistema no agrega preguntas de relleno.
- **Exportación bloqueada:** completa los títulos y alternativas y marca la revisión de cada pregunta generada. No generes preguntas si solo tienes una URL o texto ajeno al video.
- **No encuentro la lección:** abre tu JSON. Las descargas suelen estar en la carpeta Descargas de Windows.

## Pruebas para personal técnico

Sin dependencias npm: `node tests/core.test.js` y `node tests/ai.test.js`. Las pruebas de servidor usan un proveedor simulado, sin credenciales reales ni cargos. Las pruebas de interfaz en Linux requieren Python, Playwright y Chromium: `python tests/browser_test.py` y `python tests/browser_ai_test.py`. No son necesarios para utilizar el programa.
