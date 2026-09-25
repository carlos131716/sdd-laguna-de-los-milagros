# SDD-000 — Estándar de especificaciones

## Propósito

Todos los cambios relevantes deben tener una especificación que permita entender qué problema resuelve, qué contrato expone, cómo se prueba y qué deuda deja.

## Secciones obligatorias

1. Metadata: versión, estado, prioridad, responsables y dependencias.
2. Contexto y objetivo.
3. Alcance y fuera de alcance.
4. Actores y permisos.
5. Requisitos funcionales numerados.
6. Requisitos no funcionales medibles.
7. Flujos principales y alternos.
8. Modelo de datos y contratos.
9. Errores y observabilidad.
10. Criterios de aceptación en lenguaje verificable.
11. Implementación y pruebas.
12. Riesgos, pendientes y definición de terminado.

## Estados

- `Borrador`: en diseño.
- `Aprobado`: listo para implementación.
- `Implementado`: código y pruebas disponibles.
- `Endurecimiento pendiente`: funciona en MVP, faltan controles de producción.
- `Obsoleto`: reemplazado por una versión posterior.

## Convenciones

- Usar identificadores estables: `RF`, `RNF`, `SEC`, `QA`, `TUR`, `PRED`.
- No prometer datos que el sistema no observa.
- Separar hechos oficiales, promedios derivados y predicciones.
- Toda ruta protegida debe indicar actor y permiso.
- Toda fuente externa debe guardar URL, fecha y responsable.

## Definición de terminado

Un SDD está terminado cuando el requisito se puede implementar sin preguntas básicas, tiene casos positivos y negativos, el código está trazado y las pruebas pasan.
