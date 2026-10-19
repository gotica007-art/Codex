# Generador de Lecciones Interactivas Moodle

Primera versión funcional con interfaz en español. Permite crear páginas de contenido, preguntas de selección múltiple y verdadero/falso, organizar su orden, previsualizar, guardar y volver a editar.

## Descargar y ejecutar en Windows

1. En GitHub, abre `output/Generador-Lecciones-Moodle-v1.zip` y pulsa **Download raw file** (icono de descarga).
2. Haz clic derecho sobre el ZIP descargado → **Extraer todo**.
3. Abre la carpeta extraída y haz doble clic en **index.html**; elige Edge o Chrome.
4. Lee [INSTRUCCIONES-WINDOWS.md](INSTRUCCIONES-WINDOWS.md) para crear, guardar y exportar tu lección.

También puedes pulsar el botón verde **Code** → **Download ZIP** en el repositorio y extraerlo; los cuatro archivos de la aplicación están en la raíz.

No requiere instalar programas de desarrollo ni usar una terminal. Los videos necesitan conexión a Internet. Guarda una copia JSON al terminar.

## Exportación y verificación

GIFT exporta **solo preguntas**. La guía HTML contiene las páginas de contenido y la secuencia que debes configurar manualmente en Moodle. La importación no se ha probado en una instancia real de Moodle 5.0.4+; revisa especialmente verdadero/falso, puntuaciones y saltos en un curso de prueba.

Se verificaron la lógica, las descargas, la edición y la vista del estudiante con Chromium en Linux. Consulta [VERIFICACION.md](VERIFICACION.md) para el alcance y las limitaciones.

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
