# Verificación de la versión 1

Comprobado el 19 de octubre de 2026 en Linux, Node 24 y Chromium automatizado con Playwright.

- Sintaxis de app.js y core.js: correcta.
- Tres pruebas unitarias aprobadas: JSON válido e inválido; GIFT con cuatro alternativas, verdadero/falso, retroalimentación y escape de caracteres reservados; guía HTML segura, orden y enlaces de video.
- Flujo de navegador aprobado: edición de datos generales y los tres tipos de elemento, cambio de orden, persistencia tras recargar, vista del estudiante, error con reintento, acierto con avance y finalización.
- Descargas comprobadas desde el navegador: JSON editable, GIFT UTF-8 y guía HTML; se verificó su contenido y se volvió a abrir el JSON para editarlo.
- Vista móvil de 390 px sin desbordamiento horizontal.
- Sin errores JavaScript durante el recorrido.

La automatización usó un servidor HTTP temporal local porque las políticas del Chromium de este entorno bloquean las URL file://. La aplicación utiliza scripts clásicos y rutas relativas, sin solicitudes fetch ni módulos, para permitir abrir index.html directamente en navegadores normales de Windows. No se ejecutó Windows ni se verificó allí el guardado local; se incluye la descarga JSON como respaldo independiente del almacenamiento del navegador.

No se dispuso de una instancia Moodle 5.0.4+ para verificar la importación. Se verificaron la estructura GIFT y los archivos generados, no la aceptación del importador de Moodle. Las páginas de contenido se configuran manualmente con la guía. El usuario debe comprobar en un curso de prueba la conversión de verdadero/falso, las puntuaciones, retroalimentaciones y saltos antes del uso real.

Los videos necesitan Internet; no se comprobó reproducción de videos externos.
