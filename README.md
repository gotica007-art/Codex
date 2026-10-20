# Generador de Lecciones Interactivas Moodle

Versión 2 con interfaz en español: edición manual, preguntas y objetivos con IA a partir de transcripciones, vista previa, guardado JSON y exportación de preguntas GIFT con guía de configuración para Moodle 5.0.4+.

## Descargar y ejecutar en Windows

1. Abre [Generador-Lecciones-Moodle-v2.zip](output/Generador-Lecciones-Moodle-v2.zip) y pulsa **Download raw file** (icono de descarga).
2. Haz clic derecho en el ZIP descargado → **Extraer todo**.
3. Para edición manual, abre **index.html** con Edge o Chrome.
4. Para IA, instala **Node.js LTS 22 o superior**, copia `config.example.json` como `config.local.json`, configura tu clave OpenAI y abre **INICIAR-IA.cmd**. Visita **http://127.0.0.1:8765** y mantén abierta la ventana del lanzador. No necesitas npm install.

Lee [INSTRUCCIONES-WINDOWS.md](INSTRUCCIONES-WINDOWS.md) para la configuración paso a paso, costos, protección de claves, uso y pruebas en Moodle.

## Preguntas desde video: alcance real

- Pega una transcripción o sube MP4/WebM/MP3/M4A/WAV con audio, de hasta 24 MB, para transcribirlo mediante OpenAI API. No se analizan las imágenes.
- El enlace de YouTube registra la fuente; esta versión no extrae sus subtítulos. Si no hay acceso, permite pegar la transcripción. Nunca genera preguntas a partir de la URL o del título.
- Elige cantidad (1–20), dificultad y tipo de pregunta. La IA propone objetivos observables, respuesta correcta, retroalimentación y citas de evidencia; valida las citas contra el texto.
- Edita los objetivos, incorpora los borradores y revisa cada pregunta antes de exportarla. Una cita real no garantiza una interpretación correcta: la aprobación docente es obligatoria.
- OpenAI API es de pago y su facturación es independiente de ChatGPT. La clave se usa en el servidor local; `config.local.json` está excluido de Git y de la distribución. No lo compartas ni lo subas manualmente a GitHub. El modo manual sigue disponible sin clave.

## Un intento y exportación Moodle

Cada pregunta admite una sola respuesta; tanto un acierto como un error muestran retroalimentación y habilitan Continuar. No hay reintento, retroceso ni repetición de toda la lección en la simulación. Editar inicia una nueva prueba docente.

**GIFT contiene solo preguntas: no es una configuración completa de Lección.** Las páginas, objetivos, orden, intentos y saltos se configuran en Moodle siguiendo la guía HTML generada. Esta explica `maxattempts=1`, `review=0`, `modattempts=0`, `retake=0`, puntuación personalizada y saltos hacia la siguiente página tanto en correctas como incorrectas, con Fin de la lección al terminar.

Se conserva el **JSON editable**, compatible con los proyectos de la versión 1. Ahora puede incluir transcripciones, evidencia y revisión. No contiene credenciales ni el video.

## Verificación

Las pruebas de lógica, API local y recorridos en Chromium pasan usando un proveedor de IA simulado, sin cargos. **No se hicieron llamadas reales a OpenAI ni pruebas en Windows o en una instancia Moodle real.** Consulta [VERIFICACION.md](VERIFICACION.md) para el detalle y las limitaciones.

Pruebas sin dependencias npm: `node tests/core.test.js` y `node tests/ai.test.js`.

## Solicitud original

Quiero desarrollar una aplicación web sencilla llamada "Generador de Lecciones Interactivas Moodle", compatible con mi trabajo en Moodle 5.0.4+.
La aplicación debe permitir:
1. Ingresar el título, descripción y objetivos de una lección.
2. Crear páginas de contenido educativo con textos, ejemplos y videos de YouTube.
3. Crear preguntas de selección múltiple con cuatro alternativas y preguntas de verdadero o falso.
4. Incorporar retroalimentación personalizada para respuestas correctas e incorrectas.
5. Organizar las páginas y preguntas en una secuencia pedagógica.
6. Previsualizar la experiencia del estudiante.
7. Exportar las preguntas en formato GIFT compatible con la actividad Lección de Moodle.
8. Generar una guía con las páginas de contenido, sus textos y el orden recomendado para configurarlas en Moodle.
9. Permitir guardar y volver a editar una lección.

La interfaz debe estar completamente en español y tener un diseño profesional, limpio y educativo.
No tengo conocimientos previos de programación. Necesito que desarrolles una primera versión funcional, que pueda ejecutar en mi computadora Windows.
No supongas que GIFT permite importar páginas de contenido. Separa correctamente las funciones de exportación y verifica los archivos generados.
Explícame paso a paso cómo ejecutar, probar y utilizar la aplicación.
