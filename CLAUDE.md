# TFM: GBDT vs deep learning tabular en detección de fraude (BAF)

## Objetivo del proyecto
Comparar, en condiciones controladas, gradient boosting y deep learning tabular
en la detección de fraude en apertura de cuentas (dataset BAF, NeurIPS 2022).
Hipótesis: con igual presupuesto de optimización, el mejor modelo de DL tabular
(FT-Transformer o TabM) supera al mejor GBDT (XGBoost o LightGBM) en recall al
5 % de FPR en test. Se confirma si el IC 95 % por bootstrap pareado de la
diferencia tiene límite inferior > 0.

## Modo de trabajo (importante)
El autor quiere APRENDER a programar este tipo de proyectos. Trabaja en pasos
pequeños, explica cada decisión de código y su porqué, y no generes módulos
completos sin explicarlos. Pregunta antes de tomar decisiones de diseño que no
estén en este archivo.

### Modo educativo: el autor escribe el código
El autor lleva tiempo sin programar en Python y quiere recordarlo y aprender
cosas nuevas. Claude NO entrega código terminado: hace de profesor.
- En cada paso pequeño, Claude elige la modalidad que mejor encaja:
  - enunciado en texto ("construye una función que haga X"),
  - código parcial con huecos para completar,
  - preguntas socráticas que guían hacia la solución.
- Dificultad adaptativa: empezar con tareas relativamente fáciles y ajustar
  según cómo las resuelva. Al principio el autor indica la dificultad que ha
  percibido en cada tarea; usarla para calibrar.
- Si se atasca: pistas graduales, de menos a más. La solución completa solo
  si la pide.
- Sin excepciones: también los archivos auxiliares (requisitos, `.gitignore`,
  configuración, lanzador de Kaggle) se hacen juntos.
- Tras cada entrega del autor, Claude revisa el código y da feedback.
- Ritmo: no preguntar por detalles de librerías que el autor no conoce
  (p. ej. yaml, Optuna, CodeCarbon). Ese código lo da Claude, explicado en
  pocas líneas. Los ejercicios se reservan para lo que merece la pena
  aprender: Python, numpy/pandas/sklearn, PyTorch y la lógica del TFM.
  Como mucho, una o dos preguntas por paso.
- Nivel de partida: ha usado bastante numpy, pandas y scikit-learn, pero hace
  tiempo que no los usa, así que necesita calentamiento. Git: desde cero.
- Estilo: nombres de variables, funciones y módulos en inglés; comentarios y
  docstrings en español.

## Datos
- BAF Base (Kaggle: sgpjesus/bank-account-fraud-dataset-neurips-2022). El
  dataset NO se sube al repositorio (licencia): solo el código que lo procesa.
- Objetivo: `fraud_bool`. Temporal: `month` (0–7).
- Atributo protegido: `customer_age`, en dos grupos: `customer_age >= 50`
  (50 años o más) y `< 50`. Es el corte del código oficial de los autores; el
  texto del paper dice ">50", pero los tramos van por décadas (50 = 50-59).
  Ver `docs/datos.md`.
- Varias variables codifican los ausentes con valores negativos: verificarlo
  con la documentación del dataset antes de tratarlos.

## Partición (fija, no modificar)
- Entrenamiento: meses 0–4 · Validación: mes 5 · Test: meses 6–7.
- El test se evalúa UNA sola vez, al final. Todas las transformaciones se
  ajustan solo con los datos de entrenamiento.

## Modelos
- Contendientes: XGBoost, LightGBM, FT-Transformer, TabM.
- Referencia: regresión logística, Random Forest, MLP. El MLP usa el mismo
  tratamiento de variables que TabM y NO entra en el contraste de la hipótesis.
- FT-Transformer y TabM: usar las implementaciones oficiales de sus autores
  (verificar los paquetes disponibles).

## Preprocesamiento por familia
- GBDT: categóricas nativas, sin escalado.
- Regresión logística: one-hot y estandarización.
- Redes: embeddings para categóricas, transformación de numéricas, indicadores
  explícitos de ausencia.

## Desbalance
Solo ponderación de la clase positiva, como hiperparámetro dentro de la
búsqueda. NUNCA remuestreo (ni SMOTE ni undersampling).

## Optimización de hiperparámetros
- Optuna con TPE. El MISMO número de intentos N para los 7 modelos; N se fija
  tras una prueba piloto que mide el coste por intento.
- Criterio: recall al 5 % de FPR en validación.
- Registrar el tiempo por intento. Guardar los estudios en SQLite.
- En Base, repetir la búsqueda con 3 semillas para las curvas de "mejor
  resultado frente a número de intentos".

## Umbral y evaluación
- Umbral: el que da un 5 % de FPR sobre los legítimos de validación; se aplica
  tal cual al test.
- Reportar también el recall con el umbral fijado sobre el propio test
  (referencia para comparar con el paper de BAF).
- Configuración final de cada modelo: 5 semillas.
- Métricas: recall al 5 % de FPR, AUC-PR, Brier, FPR real en test, cociente de
  FPR entre grupos de edad, tiempo de cómputo y energía (CodeCarbon).
- Contraste: bootstrap pareado sobre el test. El mejor modelo de cada familia
  se elige por validación, nunca por test.

## Reproducibilidad
Versiones de librerías fijadas, semillas fijadas, configuraciones en archivos
y resultados guardados (CSV/JSON). Desarrollo y pruebas en local con
submuestras; ejecuciones pesadas en GPU (Kaggle o AWS).

## Fase actual
T3: estructura del repositorio, entorno, descarga y verificación de los datos.
T4: análisis exploratorio (esquema, ausentes, prevalencia por mes y partición,
deriva entre meses, atributo protegido).

## Entorno y estructura del código
- Desarrollo en Windows, solo CPU. Las ejecuciones con GPU (FT-Transformer,
  TabM) se lanzan en Kaggle clonando este repositorio desde un notebook que
  solo hace de lanzador. Ningún código del proyecto debe depender de Kaggle.
- Python con entorno virtual y dependencias fijadas en un archivo de requisitos.
- Todo el código en módulos de Python dentro de `src/`, ejecutable desde línea
  de comandos. Notebooks solo para el análisis exploratorio y las figuras.
- Windows: todo script que use multiproceso (Optuna, DataLoader de PyTorch,
  joblib) debe tener el punto de entrada protegido con
  `if __name__ == "__main__":`.
- Las rutas a los datos y a los resultados se leen de un archivo de
  configuración, no se escriben en el código, para que el mismo código
  funcione en local y en Kaggle.
- Redes neuronales en PyTorch. El autor conoce TensorFlow pero tiene poca
  experiencia con PyTorch: explicar el bucle de entrenamiento, los DataLoader
  y la gestión de dispositivos (CPU/GPU) con detalle la primera vez.