# Procesamiento de datos LEGENDplex™

Este documento describe el procedimiento utilizado para cargar, revisar y procesar archivos de citometría de flujo (`.fcs`) en **LEGENDplex™ Data Analysis Software**, disponible en [https://legendplex.qognit.com/](https://legendplex.qognit.com/).

El flujo de análisis del software se divide en cinco secciones: **Beads**, **Standards**, **Samples**, **Review Gating** y **Results**.

## 1. Paneles utilizados

Los datos se procesaron con los siguientes kits:

### LEGENDplex™ Human Inflammation Panel 1 (13-plex)

Cuantifica los siguientes analitos:

- IL-1β
- IFN-α2
- IFN-γ
- TNF-α
- MCP-1
- IL-6
- IL-8
- IL-10
- IL-12p70
- IL-17A
- IL-18
- IL-23
- IL-33

### LEGENDplex™ Human Immune Checkpoint Panel 1 (12-plex)

Cuantifica los siguientes analitos:

- sCD25 (IL-2Rα)
- 4-1BB (CD137)
- sCD27
- B7.2 (CD86)
- Free Active TGF-β1
- CTLA-4
- PD-L1
- PD-L2
- PD-1
- TIM-3
- LAG-3
- Galectin-9

## 2. Archivos requeridos

Antes de iniciar el análisis, se organizaron los archivos `.fcs` en tres grupos:

```text
legendplex_analysis/
├── beads/
│   ├── PE_beads.fcs
│   └── Raw_beads.fcs
├── standards/
│   ├── C0_rep1.fcs
│   ├── C0_rep2.fcs
│   ├── C1_rep1.fcs
│   └── ...
├── samples/
│   ├── sample_01_rep1.fcs
│   ├── sample_01_rep2.fcs
│   └── ...
└── results/
```

- **PE beads:** control empleado para verificar la señal del canal reportero PE.
- **Raw beads:** control de perlas sin señal específica, empleado para reconocer las poblaciones de perlas y establecer el gating inicial.
- **Standards:** archivos correspondientes al blanco y a los puntos de la curva estándar.
- **Samples:** archivos de las muestras experimentales y sus réplicas.

Se recomienda conservar nombres simples, únicos y consistentes. Los nombres deben permitir identificar la muestra, el grupo experimental, el tiempo y la réplica.

Ejemplo:

```text
GC_I_R1_6h.fcs
GC_I_R2_6h.fcs
GC_IV_R1_36h.fcs
```

## 3. Acceso al software

1. Ingresar a [https://legendplex.qognit.com/](https://legendplex.qognit.com/).
2. Iniciar sesión con la cuenta registrada.
3. Crear un nuevo experimento o espacio de trabajo.
4. Avanzar por las pestañas en el siguiente orden:

```text
Beads → Standards → Samples → Review Gating → Results
```

## 4. Configuración de las beads

En la pestaña **Beads** se seleccionó el panel correspondiente al kit utilizado.

El panel puede cargarse mediante:

- **Lot Number**, si se dispone del número de lote.
- **Name**, seleccionando el panel de BioLegend.
- **Custom**, cuando se requiere ingresar manualmente los analitos, los identificadores de las beads, las concentraciones máximas y las unidades.

Para este análisis, las concentraciones se expresaron en `pg/mL`.

Se verificó que cada analito estuviera asociado con su identificador de bead correspondiente, tanto para las poblaciones **A beads** como para las **B beads**. Esta asociación debe coincidir con la configuración del kit y no debe modificarse arbitrariamente.

## 5. Carga de los estándares

En la pestaña **Standards** se configuró la curva estándar:

- **Number of Curve Points:** 8.
- **Dilution factor:** 4.
- **Blank included:** activado.
- **Replicates:**
  - 2 réplicas para el Human Inflammation Panel 1.
  - 3 réplicas para el Human Immune Checkpoint Panel 1.

Luego se realizó el siguiente procedimiento:

1. Seleccionar **Select Standards FCS file(s)**.
2. Cargar los archivos del blanco y de cada estándar.
3. Asignar correctamente los archivos a `C0`, `C1`, `C2`, `C3`, `C4`, `C5`, `C6` y `C7`.
4. Confirmar que las réplicas de una misma concentración tengan el mismo nombre de estándar.
5. Verificar que todos los archivos aparezcan con estado correcto antes de continuar.

### Canales de adquisición

Se utilizaron los siguientes canales:

- **PE Reporter Channel:** `B4-A`.
- **APC Bead Channel:** `R1-A`.

El canal **PE** representa la intensidad asociada con la cantidad de analito unido a cada población de beads. El canal **APC** permite distinguir las diferentes poblaciones de beads y asociarlas con cada analito.

Los nombres de los canales pueden variar entre citómetros. Por ello, antes de ejecutar el análisis se debe confirmar que `B4-A` corresponde al detector PE y que `R1-A` corresponde al detector APC en la configuración del equipo utilizado.

## 6. Carga de las muestras

En la pestaña **Samples** se cargaron los archivos `.fcs` de las muestras experimentales:

1. Seleccionar **Select Samples FCS file(s)**.
2. Cargar todos los archivos correspondientes a las muestras.
3. Revisar la tabla **FCS File List**.
4. Editar el campo **Sample Name** para asignar el mismo nombre a las réplicas de una muestra.
5. Indicar el factor de dilución aplicado a cada muestra en la columna **Dilution**.
6. Seleccionar **Set Replicates** para agrupar correctamente las réplicas técnicas.
7. Presionar **Upload**.
8. Confirmar que los estándares y las muestras aparezcan con estado válido.
9. Seleccionar **Run Gating**.

Las réplicas no deben agruparse únicamente por similitud del nombre del archivo. Se debe verificar que correspondan realmente a la misma muestra, condición y tiempo experimental.

## 7. Revisión del gating

La revisión se realizó en la pestaña **Review Gating** mediante la opción **Review**.

El gating se comprobó archivo por archivo, incluyendo:

- Estándares.
- PE beads.
- Raw beads.
- Muestras experimentales.

### 7.1. Separación inicial de las beads

En el gráfico `FSC-A` frente a `SSC-A` se verificaron las regiones correspondientes a:

- **A beads**, de menor tamaño.
- **B beads**, de mayor tamaño.

Las regiones se ajustaron para incluir las poblaciones principales y excluir residuos, ruido electrónico, agregados y eventos localizados fuera de las nubes de beads.

El control **Raw beads** se utilizó como referencia para reconocer la distribución basal de las poblaciones A y B. El control **PE beads** se utilizó para comprobar la detección del canal reportero y la ubicación esperada de las beads con señal PE.

### 7.2. Identificación de las poblaciones por APC

Después de separar las A beads y B beads, se revisaron los histogramas del canal APC (`R1-A`).

Cada pico debe:

- Estar contenido dentro de su gate correspondiente.
- Alinearse con el identificador de bead asignado al analito.
- Mantener el orden esperado del panel.
- Mostrar una separación suficiente respecto de los picos adyacentes.

Los gates se ajustaron cuando un pico quedaba parcialmente excluido, cuando dos poblaciones se superponían de forma incorrecta o cuando la selección automática no coincidía con la distribución observada.

No se debe cambiar la identidad de una población solo para mejorar el resultado. La posición y el orden de los picos deben ser coherentes con las **PE beads**, las **Raw beads**, los estándares y la configuración específica del kit.

### 7.3. Aplicación del gating

Una vez verificada la posición de las poblaciones:

1. Seleccionar **Apply Gating**.
2. Revisar que el gating se haya aplicado correctamente.
3. Marcar el archivo como revisado.
4. Continuar con el siguiente archivo.

Cuando los patrones eran equivalentes entre archivos, se utilizó **Convert Gates** o la función de transferencia de gates como punto de partida. Sin embargo, cada archivo se inspeccionó individualmente antes de aprobarlo.

Las muestras con un número muy bajo de eventos por población, separación insuficiente de los picos o distribución anómala se identificaron para revisión adicional y posible exclusión técnica.

## 8. Generación y optimización de las curvas estándar

En la pestaña **Results** se inspeccionaron las curvas estándar de cada analito. El software permite ajustar curvas logísticas de cuatro o cinco parámetros, según la configuración y el comportamiento de los datos.

Para cada analito se evaluaron:

- La distribución de los puntos estándar.
- La concordancia entre réplicas.
- La forma sigmoidal de la curva.
- El coeficiente de determinación (`R²`).
- El límite de detección (`LOD`).
- El rango útil de cuantificación.
- El número de muestras cuya concentración podía calcularse dentro del rango de la curva.

Se seleccionaron los puntos técnicamente más adecuados para obtener curvas con un `R²` alto y calcular la mayor cantidad posible de concentraciones experimentales.

La exclusión de puntos se limitó a estándares con evidencia de falla técnica, como:

- Réplicas claramente discordantes.
- Número insuficiente de eventos.
- Señal incompatible con el orden de concentración esperado.
- Saturación extrema.
- Error de adquisición o gating.

No se eliminaron puntos únicamente para aumentar artificialmente el `R²`. Cada modificación de la curva debe conservarse en un registro de control de calidad, indicando el analito, el punto excluido y la razón técnica.

Cuando fue posible, se priorizó el ajuste que combinara:

1. `R²` alto.
2. Comportamiento sigmoidal coherente.
3. Réplicas consistentes.
4. Residuos bajos.
5. Mayor cobertura del rango de concentraciones de las muestras.
6. Menor cantidad de resultados fuera de rango.

Las muestras por debajo del rango de cuantificación deben reportarse como menores que el límite correspondiente, y las muestras por encima del estándar superior deben repetirse con una dilución adicional cuando exista volumen disponible.

## 9. Exportación de resultados

Una vez aprobadas las curvas:

1. Seleccionar **Report**.
2. Exportar el informe completo.
3. Descargar la tabla de concentraciones en formato Excel o CSV.
4. Conservar los valores de MFI, concentraciones calculadas, indicadores de calidad y resultados fuera de rango.
5. Guardar una copia del informe sin modificaciones junto con la tabla utilizada para el análisis estadístico.

Estructura recomendada:

```text
results/
├── raw_export/
│   ├── LEGENDplex_report_original.xlsx
│   └── LEGENDplex_report_original.pdf
├── processed/
│   └── concentrations_cleaned.csv
└── quality_control/
    ├── excluded_standard_points.csv
    └── gating_notes.md
```

## 10. Control de calidad y trazabilidad

Para garantizar la reproducibilidad se registraron:

- Nombre y versión del software.
- Fecha del análisis.
- Nombre y lote del kit.
- Panel seleccionado.
- Canales PE y APC utilizados.
- Número de puntos y réplicas de la curva.
- Factor de dilución de estándares y muestras.
- Archivos incluidos o excluidos.
- Cambios manuales realizados durante el gating.
- Puntos retirados de las curvas estándar.
- Justificación técnica de cada exclusión.
- Modelo de curva utilizado.
- `R²`, `LOD` y rango de cuantificación por analito.

## 11. Registro sugerido de exclusiones

```csv
panel,analyte,standard_point,replicate,action,reason,date,analyst
Inflammation Panel 1,IL-17A,C6,2,Excluded,Low bead count,YYYY-MM-DD,Initials
Immune Checkpoint Panel 1,PD-L1,C7,1,Excluded,Signal saturation,YYYY-MM-DD,Initials
```

## 12. Referencias

- BioLegend. *LEGENDplex™ Data Analysis Software User Guide*.
- BioLegend. *LEGENDplex™ Human Inflammation Panel 1 (13-plex)*.
- BioLegend. *LEGENDplex™ Human Immune Checkpoint Panel 1 (12-plex)*.
- Plataforma de análisis: [https://legendplex.qognit.com/](https://legendplex.qognit.com/).

---

**Nota:** este procedimiento documenta la configuración aplicada en este proyecto. Los nombres de canales, las diluciones, el número de réplicas y la disposición de las beads deben verificarse con el manual del lote, la configuración del citómetro y el diseño experimental correspondiente.
