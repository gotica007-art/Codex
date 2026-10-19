# Generador de Lecciones Interactivas Moodle — versión 1

## Ejecutar en Windows

1. Descarga el ZIP y haz clic derecho → **Extraer todo**. No abras la aplicación dentro del ZIP.
2. Abre la carpeta extraída y haz doble clic en **index.html**. Si Windows pregunta con qué abrirlo, elige **Microsoft Edge** o **Google Chrome** actualizado.
3. Ya puedes trabajar. No necesitas instalar Python, Node, un servidor ni crear una cuenta. La interfaz está en español.
4. Conserva juntos index.html, styles.css, core.js y app.js. Puedes copiar la carpeta a otro equipo.

La aplicación funciona sin Internet salvo los videos de YouTube. Los videos pueden bloquearse por políticas del navegador, restricciones del video o de la red. No se necesita conectarse a Moodle para preparar la lección.

## Crear y utilizar una lección

1. Completa título, descripción y objetivos.
2. Pulsa **Página de contenido**. Escribe título, texto y ejemplo; opcionalmente pega una URL de YouTube (watch, youtu.be o shorts). Los textos son texto plano, no código HTML.
3. Pulsa **Selección múltiple**, completa las cuatro alternativas y elige la respuesta correcta. Solo se admite una respuesta correcta.
4. Añade una pregunta **Verdadero o falso** y selecciona la respuesta correcta.
5. Personaliza los mensajes para aciertos y errores en cada pregunta.
6. Usa las flechas ↑ y ↓ para cambiar el orden. Pulsa un elemento para editarlo. Eliminar pide confirmación.
7. Pulsa **Vista del estudiante** → **Comenzar lección**. Una respuesta incorrecta muestra retroalimentación y permite reintentar; la correcta habilita continuar. Esta es una simulación lineal, sin calificaciones almacenadas.
8. Pulsa **Guardar archivo editable** para descargar `leccion-editable.json`. Para continuar otro día, usa **Abrir lección** y elige ese archivo.

Los cambios se guardan automáticamente en el navegador cuando este lo permite. Este guardado depende del navegador, el perfil y la ubicación de la carpeta; no es una copia de seguridad. El modo privado o borrar datos puede perderlo. Descarga siempre el JSON al terminar. **Nueva lección** y **Abrir lección** reemplazan la lección actual tras confirmar.

## Exportar y configurar en Moodle 5.0.4+

### Preguntas

1. Pulsa **Descargar preguntas GIFT**. Obtendrás `preguntas.gift` en UTF-8 con selección múltiple y verdadero/falso; incluye los mensajes personalizados.
2. En un curso de prueba de Moodle, añade una actividad **Lección**.
3. En la edición de la Lección, busca **Importar preguntas** y selecciona **GIFT**. Los nombres y la ubicación exacta pueden variar según el tema, permisos y complementos. No confundas esta opción con la importación del banco de preguntas.
4. Sube `preguntas.gift` y revisa el resultado. GIFT es un formato de preguntas; no es una copia de seguridad de una actividad Lección.
5. Comprueba especialmente verdadero/falso: el importador de Lección instalado puede convertirlo en selección múltiple o no admitirlo. Si lo rechaza, créalo manualmente con las dos alternativas de la guía.
6. Revisa las respuestas, puntuaciones, retroalimentación y saltos de cada pregunta antes de usarla con estudiantes.

### Contenido y orden

1. Pulsa **Descargar guía de contenido** y abre `guia-de-contenido.html` con Edge o Chrome. Puedes imprimirla o guardarla como PDF desde el navegador.
2. Copia la descripción y objetivos a la introducción de la actividad.
3. Crea manualmente las páginas de contenido en la Lección: copia sus títulos, textos y ejemplos. Inserta los enlaces de YouTube con el editor de Moodle.
4. Intercala páginas y preguntas siguiendo la numeración de la guía. La importación GIFT no reconstruye esta secuencia.
5. Configura los saltos: avanzar tras acertar y reintentar tras fallar si deseas reproducir la simulación. Revisa la configuración de reintentos y puntuación de la actividad.
6. Usa la vista previa de Moodle para recorrer toda la lección antes de publicarla.

**No se ha probado la importación en una instancia real de Moodle 5.0.4+.** Se ha comprobado la generación local de GIFT; la aceptación final depende del importador instalado. La guía conserva todos los elementos para configurarlos manualmente si es necesario.

## Prueba rápida (cinco minutos)

1. Crea una página llamada «Evaporación» y escribe «El agua pasa a vapor».
2. Añade una pregunta con alternativas «Vapor», «Hielo», «Piedra», «Metal» y marca «Vapor» como correcta.
3. Añade una pregunta verdadera/falsa y personaliza ambos mensajes.
4. Cambia el orden con las flechas, abre la vista del estudiante y prueba una respuesta incorrecta y una correcta.
5. Descarga JSON, GIFT y guía. Comprueba que GIFT contiene solo preguntas y que la guía incluye la página y el orden.
6. Abre el JSON: el contenido debe recuperarse y seguir siendo editable.

## Solución de problemas

- **La página no tiene estilo o no funcionan los botones:** extrae todo el ZIP y conserva los cuatro archivos principales juntos; abre index.html con Edge o Chrome.
- **No encuentro las descargas:** revisa la carpeta Descargas de Windows y los avisos de descarga del navegador.
- **No aparece mi lección al volver:** usa Abrir lección con el JSON que guardaste. El guardado del navegador no se comparte entre perfiles ni equipos.
- **No puedo exportar:** completa los campos indicados en el aviso; las preguntas de selección múltiple requieren cuatro alternativas y todos los elementos un título.
- **No funciona el video:** comprueba conexión, enlace y permisos de reproducción del video.
- **Moodle rechaza GIFT:** confirma formato GIFT y UTF-8, prueba en una Lección vacía y revisa el mensaje de importación. Utiliza la guía para crear manualmente las preguntas que tu importador no acepte.

## Verificación para personal técnico

La aplicación no tiene dependencias de ejecución ni envía las lecciones a un servidor. No incluye cuentas, sincronización ni archivos .mbz. JSON usa un esquema versionado y validado al abrir.

- `node --check app.js` y `node --check core.js`: sintaxis.
- `node tests/core.test.js`: validación de JSON, GIFT, caracteres reservados, HTML seguro y URL de video.
- `python tests/browser_test.py`: prueba de navegador con Playwright y Chromium en Linux; estas herramientas solo son necesarias para repetir la prueba automatizada, no para usar la aplicación. La prueba escribe descargas temporales en work/.

Consulta VERIFICACION.md para el alcance de las comprobaciones realizadas.
