# Verificación — versión 2

Comprobaciones realizadas el 20 de octubre de 2026 en Linux con Node 24 y Chromium automatizado mediante Playwright.

## Comprobado

- Sintaxis de app.js, core.js, ai.js y server.js.
- Tres pruebas de núcleo: JSON editable e inválido; exportación GIFT con selección múltiple y verdadero/falso, respuesta correcta, feedback y caracteres especiales; guía HTML escapada y enlaces YouTube.
- Cinco pruebas nuevas de lógica e integración: validación de fuente, cantidad y dificultad; rechazo de citas inexistentes, preguntas inválidas y objetivos no evaluados; solicitudes Responses y transcripción con un proveedor simulado; bloqueo de exportación antes de revisar y guía de un intento; servidor HTTP con origen, host y token, y archivos privados inaccesibles.
- Recorrido manual automatizado en navegador: crear y ordenar los tres tipos, guardar y reabrir JSON, persistencia, descargas GIFT y HTML, error con bloqueo de alternativas y avance, respuesta correcta y final sin repetir; cerrar y reabrir la vista previa conserva su estado.
- Recorrido de IA con respuestas simuladas: enlace YouTube sin extracción, bloqueo sin transcripción, cantidad y dificultad enviadas, objetivos editables y preguntas incorporadas, revisión obligatoria, edición que invalida la revisión, evidencia y transcripción conservadas en JSON, exportación tras revisar, fallos de generación y transcripción con recuperación manual.
- Interfaz a 390 px sin desbordamiento horizontal en ambos recorridos y sin errores JavaScript.
- Archivo ZIP comprobado con testzip; incluye solo archivos enumerados, sin configuración privada, .git, claves, videos ni datos de trabajo.

## Límites de esta verificación

**No se realizaron llamadas reales de pago a OpenAI.** No hay credencial configurada en este entorno. Las pruebas verifican la lógica, el contrato de solicitudes/respuestas y la interfaz mediante respuestas simuladas; no demuestran calidad pedagógica real, reproducción de audio, extracción real de voz ni disponibilidad de modelos en una cuenta concreta. La prueba inicial real debe hacerse con un fragmento propio y revisar la transcripción y preguntas. El programa no presenta datos simulados como resultados reales ni tiene modo ficticio activado en producción.

No se ejecutó Windows. Se incluyen instrucciones y un lanzador CMD para Node.js 22 o superior sin dependencias npm. El modo de archivo HTML se conserva para edición manual; las pruebas de navegador se realizaron sobre HTTP local porque el Chromium del entorno restringe file://.

No se dispone de Moodle 5.0.4+ para restaurar/importar y ejecutar con estudiantes. Se revisaron los campos y saltos del código fuente de la versión v5.0.4. GIFT no conserva maxattempts, review, modattempts, retake ni saltos personalizados. La guía indica configurarlos y probarlos con una cuenta de estudiante, con puntuación personalizada 1/0 y avance tras cualquier respuesta. No se ofrece exportación MBZ en esta versión.

No se extraen subtítulos de YouTube. La URL se guarda como fuente y se solicita una transcripción manual. El archivo subido se envía al servicio de transcripción: se usa su audio, sin analizar imágenes del video.

Las citas se comprueban por coincidencia textual normalizando espacios. Esto evita referencias inexistentes, pero no demuestra que la pregunta, los distractores o la interpretación sean correctos. La revisión docente sigue siendo obligatoria.

## Corrección 2.0.1

Se añadió una prueba con archivos temporales sin claves reales: el mismo servidor detecta la clave añadida después del arranque, acepta BOM y espacios, identifica extensión .json.txt y JSON inválido sin revelar valores privados en sus respuestas. No se valida una clave real con OpenAI.
