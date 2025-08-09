# 🧪 Plan de Pruebas – MotoFit

**Versión:** v1.0  
**Fecha:** (yyyy-mm-dd)  
**Entorno:**  
- Local: `data/motofit_demo.csv`  
- Producción: `st.secrets["DATA_URL"]` (CSV remoto)

---

## 0) Preparación

- [ ] `streamlit run app.py` arranca sin errores.
- [ ] KPIs iniciales muestran valores válidos (> 0 cuando corresponda).
- [ ] El botón **🔍 Buscar motos** responde y no deja el estado inconsistente.

---

## 1) Pruebas del Recomendador

| ID  | Caso | Pasos | Esperado | Resultado | OK |
|-----|------|------|----------|-----------|----|
| R1  | Presupuesto básico | Min=2.000, Max=8.000; buscar | Todas las motos en [2000, 8000] |  | ☐ |
| R2  | Validación min/max | Min=9000, Max=3000 | Mensaje de error “El mínimo no puede ser ≥ al máximo.” y no ejecuta búsqueda |  | ☐ |
| R3  | Carnet A2 | Carnet=A2; buscar | No aparecen motos que exijan A |  | ☐ |
| R4  | Estatura extrema | Altura=150 cm y luego 195 cm; buscar | Cambia la priorización/orden (cuando orden = Altura/Peso) |  | ☐ |
| R5  | Filtro por marca | Marca=Yamaha; buscar | Solo Yamaha |  | ☐ |
| R6  | Filtro por tipo múltiple | Tipo = Naked + Scooter; buscar | Solo Naked/Scooter |  | ☐ |
| R7  | Orden asc/desc | Ordenar por Precio ascendente y luego descendente | El primer/último elemento cambia acorde |  | ☐ |
| R8  | Paginación | Ir a última página | Sin tarjetas en blanco; contador “Mostrando X–Y de Z” correcto |  | ☐ |
| R9  | Favoritos (agregar) | Marcar “Guardar ❤️” en 2–3 modelos | Aparecen en “Tus favoritas” inmediatamente |  | ☐ |
| R10 | Favoritos (quitar) | Quitar “Guardar ❤️” desde la grilla y desde “Tus favoritas” | Se eliminan al instante de la sección |  | ☐ |
| R11 | Estado tras rerun | Cambiar un favorito y luego mover la página | La selección de favoritos persiste |  | ☐ |

---

## 2) Pruebas del Dashboard

**Filtros aplican a todos los gráficos:**
- [ ] Tipo = Naked
- [ ] Marca = Honda
- [ ] Combinación Tipo + Marca

### 2.1 KPIs
| ID  | Caso | Pasos | Esperado | Resultado | OK |
|-----|------|------|----------|-----------|----|
| D1  | KPIs con datos | Sin filtros | `Modelos > 0`, `Precio mediano` con €, `Altura mediana` en mm |  | ☐ |
| D2  | KPIs con filtros | Tipo=Adventure, Marca=KTM | Cambian acorde al subconjunto |  | ☐ |

### 2.2 Gráficos
| ID  | Caso | Pasos | Esperado | Resultado | OK |
|-----|------|------|----------|-----------|----|
| D3  | Altura por tipo | Sin filtros | Boxplot + puntos; eje Y ~650–950 mm (auto‑ajuste) |  | ☐ |
| D4  | Precio vs Potencia | Sin filtros | Puntos con hover (Marca/Modelo); eje Y con prefijo € |  | ☐ |
| D5  | Precio por tipo | Sin filtros | Cajas por tipo; sin NaN visibles |  | ☐ |
| D6  | Licencias por tipo | Sin filtros | Barras apiladas normalizadas; leyenda AM/B/A1/A2/A |  | ☐ |
| D7  | Filtros sincronizados | Tipo=Naked y Marca=Yamaha | Todos los gráficos y KPIs reflejan la selección |  | ☐ |

---

## 3) Calidad de Datos

| ID  | Caso | Pasos | Esperado | Resultado | OK |
|-----|------|------|----------|-----------|----|
| DA1 | Limpieza numérica | Revisar muestra en CSV con formatos “€7.499,00”, “7499” | Se cargan como números (sin NaN inesperados) |  | ☐ |
| DA2 | Rango altura | Revisar outliers <500 o >1100 mm | Se filtran/limpian; no rompen gráficos |  | ☐ |
| DA3 | Texto normalizado | MARCA/Tipo/Carnet | Sin espacios extra; mezcla de mayúsculas controlada |  | ☐ |
| DA4 | Columnas mínimas | PRECIO, ALTURA_ASIENTO, CARNET_MINIMO, MARCA, TIPO_SIMPLIFICADO | No faltan; sin KeyError |  | ☐ |

---

## 4) UX / Visual

| ID  | Caso | Pasos | Esperado | Resultado | OK |
|-----|------|------|----------|-----------|----|
| UX1 | Responsive | Cambiar ancho de ventana | Tarjetas alineadas; dashboard no se descuadra |  | ☐ |
| UX2 | Modo oscuro/claro | Cambiar preferencia del sistema | Colores de texto/gráficos legibles |  | ☐ |
| UX3 | Logos de marcas | Ver tarjetas con logos disponibles | Se muestran; si faltan, cae a texto **MARCA** |  | ☐ |
| UX4 | Tooltips | Pasar el mouse por puntos/barras | Información clara (Marca, Modelo, etc.) |  | ☐ |

---

## 5) Regresión (antes de release)

| ID  | Cambio reciente | Qué verificar | OK |
|-----|-----------------|---------------|----|
| RG1 | Favoritos con callback | Agregar/quitar en grilla y en “favoritas” actualiza al instante | ☐ |
| RG2 | Rerun streamlit | Tras quitar favorito no desaparecen resultados buscados | ☐ |
| RG3 | Rango de altura | El eje Y no corta bigotes; no hay overflow hacia arriba | ☐ |
| RG4 | Precio por tipo (Plotly) | No sale vacío; y‑axis con € | ☐ |
| RG5 | Orden por potencia | Cambia correctamente al alternar asc/desc | ☐ |

---

## 6) Producción (Streamlit Cloud)

| ID  | Caso | Pasos | Esperado | Resultado | OK |
|-----|------|------|----------|-----------|----|
| P1  | Secrets | Definir `DATA_URL` en Cloud | La app carga el dataset remoto |  | ☐ |
| P2  | Sin datos locales | No subir CSV privados al repo | La app sigue funcionando con `DATA_URL` |  | ☐ |
| P3  | Latencia razonable | Primer render | < 3–5 s con cache |  | ☐ |

---

## 7) Observaciones

- [ ] Notas, errores, decisiones y pendientes.
- [ ] Capturas de pantalla si algo falla (adjuntar en `/assets/test/` si quieres).

---

## 8) Aprobación

- **Probado por:** __________________  
- **Fecha:** __________________  
- **Resultado global:** ✅ Aprobado / ⛔ Requiere ajustes
