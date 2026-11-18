# Registro de decisiones de diseño

Decisiones tomadas durante el desarrollo que no venían fijadas de antemano en el
planteamiento del TFM, con el motivo de cada una. Las decisiones sobre los datos
se detallan con su evidencia en `docs/datos.md`; aquí se resumen.

Para añadir una decisión: fecha, qué se decide y por qué, en dos o tres líneas.
Si una decisión cambia, no se borra: se marca como sustituida y se añade la nueva.

## Entorno y reproducibilidad

**2026-10-13 · Python 3.12 en local.** Es la versión de Kaggle, donde se ejecutan
las redes con GPU. Así el mismo `requirements.txt` sirve en los dos sitios y no
se usa en local ninguna función que falle en Kaggle.

**2026-10-13 · Dependencias fijadas a mano con `==`, sin `pip freeze`.** `freeze`
incluye dependencias indirectas, algunas exclusivas de Windows (p. ej. `pywin32`),
que fallarían al instalarse en el Linux de Kaggle. Las de desarrollo local
(`ipykernel`) van aparte, en `requirements-dev.txt`.

**2026-10-13 · Configuración en YAML, un archivo por entorno.** `configs/local.yaml`
y `configs/kaggle.yaml`, elegidos al ejecutar con `--config`. El código no cambia
entre entornos; solo las rutas.

**2026-10-13 · Rutas relativas a la raíz del repositorio.** `resolve_path` las
calcula desde la ubicación de `src/config.py`, no desde la carpeta en la que se
ejecuta el comando. Así funcionan igual desde la terminal, desde `notebooks/` y
desde Kaggle.

**2026-10-16 · Proyecto instalado en modo editable (`pip install -e .`).** Permite
importar `src` desde cualquier carpeta, incluidos los notebooks, sin manipular
`sys.path`. El lanzador de Kaggle deberá hacer lo mismo después de clonar.

## Datos

**2026-10-14 · Atributo protegido: `customer_age >= 50`.** El texto del paper dice
"> 50", pero el código oficial de los autores usa `>= 50`, y es el que produjo los
resultados publicados. Como `customer_age` va por décadas, `>= 50` es "50 años o
más". Se usa el del código, para que el cociente de FPR sea comparable.

**2026-11-03 · Ausentes a NaN, en un paso común a todos los modelos.** El -1 en
cinco columnas y los negativos de `intended_balcon_amount`, según el datasheet. NaN
dice lo que significa; un -1 es una convención oculta que una red interpretaría
como un número. Después, cada familia trata el NaN a su manera. Ver
`missing_to_nan` en `src/data.py`.

**2026-11-03 · `intended_balcon_amount`: negativos como ausentes.** La señal
principal (tener o no un negativo, ratio de fraude 2,46 en train) se conserva con
el indicador de ausencia. Se pierde el gradiente dentro de los negativos, que es
débil (ratio 1,31 entre quintiles extremos) y no tiene interpretación si esos
valores significan "sin dato".

**2026-10-14 · Negativos de `credit_risk_score` y `velocity_6h`: se dejan tal
cual.** El datasheet los incluye en el rango de valores válidos. Eliminar las 44
filas de `velocity_6h` distorsionaría la evaluación en test.

**2026-10-14 · Se descarta `device_fraud_count`.** Es constante (siempre 0) en
Base, así que no aporta información.

**2026-10-19 · `month` no es variable de entrada.** Es la variable que define la
partición; usarla permitiría al modelo saber de qué partición viene cada fila.

**2026-11-18 · Meses de cada partición como constantes** (`TRAIN_MONTHS`,
`VAL_MONTHS`, `TEST_MONTHS` en `src/data.py`). Se ven nada más abrir el archivo y,
si cambiaran, se cambian en un solo sitio. La partición se hace por el valor de
`month`, nunca por la posición de las filas.

## Preprocesamiento

**2026-11-18 · Random Forest: categóricas codificadas como enteros y NaN nativo.**
A un árbol le basta un código entero por categoría, y es más ligero que el one-hot.
scikit-learn admite NaN en Random Forest desde la versión 1.4.

**2026-11-18 · Redes: numéricas con transformación por cuantiles a una normal**
(`QuantileTransformer`). Es la que usan los autores de FT-Transformer y TabM en sus
benchmarks. Además acota los valores extremos, lo que ayuda con la deriva de las
variables `velocity_*` observada en el EDA.

**2026-11-18 · Categorías no vistas en train: índice reservado de "desconocido".**
En Base no ocurre, pero así el código no falla con las variantes del BAF ni si
alguna categoría rara no aparece en train.

## Análisis exploratorio

**2026-10-19 · PSI programado a mano**, sin librería externa. Variables con 20
valores distintos o menos: un tramo por valor; continuas: deciles de train. La
versión inicial, con deciles para todo, daba PSI = 0 en todas las binarias.

**2026-11-02 · Las decisiones de preprocesado se apoyan en train y val, no en
test.** El test se reserva para la evaluación final.

## Pendiente de decidir

- **Cálculo del umbral al 5 % de FPR.** El código oficial toma el FPR más alto
  estrictamente por debajo del 5 % (ver `docs/datos.md`). Decidir si se replica
  igual.
