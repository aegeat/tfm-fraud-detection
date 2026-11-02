# Datos: Bank Account Fraud (BAF), versión Base

Fuente: Kaggle, `sgpjesus/bank-account-fraud-dataset-neurips-2022` (archivo
`Base.csv`). Paper: Jesus et al., *Turning the Tables: Biased, Imbalanced,
Dynamic Tabular Datasets for ML Evaluation*, NeurIPS 2022. Datasheet:
`documents/datasheet.pdf` en el repositorio `feedzai/bank-account-fraud`.

1.000.000 de filas, 32 columnas, sin NaN. Prevalencia de fraude: 1,10 %.

## Diccionario de variables

"Documentado" es lo que dice la descripción de Kaggle, salvo donde se indica
"datasheet". "Observado" es lo que hay en `Base.csv` (mínimo y máximo sobre todas
las filas). Si Kaggle y el datasheet no coinciden, manda el datasheet.

### Objetivo y tiempo

| Variable | Descripción | Documentado | Observado |
|---|---|---|---|
| `fraud_bool` | Etiqueta: 1 = fraude, 0 = legítima. | {0, 1} | {0, 1} |
| `month` | Mes de la solicitud. | [0, 7] | [0, 7] |

### Numéricas

| Variable | Descripción | Documentado | Observado |
|---|---|---|---|
| `income` | Ingresos anuales del solicitante, en cuantiles. | [0, 1] | [0,1; 0,9]: 9 valores (deciles) |
| `name_email_similarity` | Similitud entre el email y el nombre; más alto = más parecido. | [0, 1] | [0, 1] |
| `prev_address_months_count` | Meses en la dirección anterior, si la hay. | [-1, 380]; -1 = ausente | [-1, 383] |
| `current_address_months_count` | Meses en la dirección actual. | [-1, 406]; -1 = ausente | [-1, 428] |
| `customer_age` | Edad en tramos de una década (20-29 se codifica como 20). | — | {10, 20, …, 90} |
| `days_since_request` | Días desde que se hizo la solicitud. | [0, 78] | [0; 78,5] |
| `intended_balcon_amount` | Importe transferido inicialmente. | Kaggle: [-1, 108]. Datasheet: [-16, 114]; negativos = ausentes | [-15,5; 113,0] |
| `zip_count_4w` | Solicitudes con el mismo código postal en las últimas 4 semanas. | [1, 5767] | [1, 6700] |
| `velocity_6h` | Media de solicitudes por hora en las últimas 6 h. | [-211, 24763] | [-170,6; 16715,6] |
| `velocity_24h` | Media de solicitudes por hora en las últimas 24 h. | [1329, 9527] | [1300,3; 9506,9] |
| `velocity_4w` | Media de solicitudes por hora en las últimas 4 semanas. | [2779, 7043] | [2825,7; 6994,8] |
| `bank_branch_count_8w` | Solicitudes en la sucursal elegida en las últimas 8 semanas. | [0, 2521] | [0, 2385] |
| `date_of_birth_distinct_emails_4w` | Emails de solicitantes con la misma fecha de nacimiento en las últimas 4 semanas. | [0, 42] | [0, 39] |
| `credit_risk_score` | Puntuación interna de riesgo de la solicitud. | [-176, 387] | [-170, 389] |
| `bank_months_count` | Antigüedad de la cuenta anterior, si la hay, en meses. | [-1, 31]; -1 = ausente | [-1, 32] |
| `proposed_credit_limit` | Límite de crédito propuesto. | [200, 2000] | [190, 2100]: 12 valores |
| `session_length_in_minutes` | Duración de la sesión en la web del banco, en minutos. | [-1, 107]; -1 = ausente (datasheet) | [-1; 85,9] |
| `device_distinct_emails_8w` | Emails distintos desde el mismo dispositivo en las últimas 8 semanas. | Kaggle: [0, 3]. Datasheet: [-1, 2]; -1 = ausente | [-1, 2] |
| `device_fraud_count` | Solicitudes fraudulentas con el mismo dispositivo. | [0, 1] | **Siempre 0** |

### Binarias (0/1)

| Variable | Descripción |
|---|---|
| `email_is_free` | Dominio del email gratuito (1) o de pago (0). |
| `phone_home_valid` | El teléfono fijo es válido. |
| `phone_mobile_valid` | El teléfono móvil es válido. |
| `has_other_cards` | Tiene otras tarjetas del mismo banco. |
| `foreign_request` | La solicitud llega de un país distinto al del banco. |
| `keep_alive_session` | Opción del usuario al cerrar sesión. |

### Categóricas

| Variable | Descripción | Valores observados (filas) |
|---|---|---|
| `payment_type` | Tipo de plan de pago (anonimizado). | AB 370.554 · AA 258.249 · AC 252.071 · AD 118.837 · **AE 289** |
| `employment_status` | Situación laboral (anonimizada). | CA 730.252 · CB 138.288 · CF 44.034 · CC 37.758 · CD 26.522 · CE 22.693 · **CG 453** |
| `housing_status` | Situación de vivienda (anonimizada). | BC 372.143 · BB 260.965 · BA 169.675 · BE 169.135 · BD 26.161 · BF 1.669 · **BG 252** |
| `source` | Canal de la solicitud: navegador (INTERNET) o app (TELEAPP). | INTERNET 992.952 · TELEAPP 7.048 |
| `device_os` | Sistema operativo del dispositivo. | other 342.728 · linux 332.712 · windows 263.506 · macintosh 53.826 · x11 7.228 |

Las categorías en negrita tienen menos de 500 filas. Hay que tenerlas en
cuenta al codificar las categóricas, por ejemplo con los embeddings de las
redes.

## Observaciones

- **Los rangos de Kaggle no coinciden exactamente con los observados**, en
  ninguna dirección fija: unas veces el documentado es más amplio y otras
  más estrecho. El datasheet tampoco coincide en todas las variables. No afecta
  al tratamiento.
- **`device_fraud_count` es constante (siempre 0) en Base.** No aporta
  información y se descarta como variable de entrada. Pendiente: comprobar si
  también es constante en las variantes.

## Valores ausentes codificados como negativos

Las variables marcadas con (*) tienen como único valor negativo el -1.

| Variable | Filas con negativo | ¿Es ausente? |
|---|---|---|
| `prev_address_months_count` (*) | 712.920 (71,3 %) | **Sí** (documentado) |
| `current_address_months_count` (*) | 4.254 (0,4 %) | **Sí** (documentado) |
| `bank_months_count` (*) | 253.635 (25,4 %) | **Sí** (documentado) |
| `session_length_in_minutes` (*) | 2.015 (0,2 %) | **Sí** (datasheet) |
| `device_distinct_emails_8w` (*) | 359 (0,04 %) | **Sí** (datasheet) |
| `intended_balcon_amount` | 742.523 (74,3 %) | **Sí** (datasheet), ver abajo |

### `intended_balcon_amount`

- El datasheet dice: *"Ranges between [−16, 114] (negatives are missing
  values)"*. La descripción de Kaggle da [-1, 108] y no lo menciona.
- En los datos, los negativos no son un valor fijo: son continuos y casi
  todos distintos. Se concentran alrededor de -1 (en train: mediana -1,00,
  percentiles 1 y 99 de -1,86 y -0,17), con un mínimo de -15,5.
- Tener un negativo se relaciona con el fraude: 1,19 % frente a 0,48 % en train
  (ratio 2,46) y 1,41 % frente a 0,42 % en val (ratio 3,35).
- La magnitud aporta mucho menos: entre el primer y el último quintil de los
  negativos, la tasa pasa del 1,02 % al 1,33 % en train (ratio 1,31) y del 1,18 %
  al 1,75 % en val (ratio 1,47). En los meses 1 y 2 de train es casi plana.
- **Recomendación, pendiente de aprobar:** convertir los negativos a NaN, como
  el resto de ausentes, y conservar la señal principal con el indicador de
  ausencia.

### Negativos legítimos (se dejan tal cual)

- `credit_risk_score`: la documentación incluye negativos en el rango
  ([-176, 387]). Es una puntuación, no un ausente.
- `velocity_6h`: la documentación incluye negativos en el rango
  ([-211, 24763]). Son 44 filas (0,004 %). Se dejan tal cual: forman parte de
  la distribución, y eliminarlas del test distorsionaría la evaluación. Pueden
  deberse al ruido añadido a los datos que describe el datasheet, aunque este no
  lo afirma.

## Atributo protegido: `customer_age`

Los tramos son {10, 20, …, 90}, y el valor 50 representa a los de 50-59 años.

- **El paper** dice: *"separating applicants with age >50 in one group and
  ≤50 in the other group"*.
- **El código oficial de los autores**
  (`feedzai/bank-account-fraud`, `notebooks/empirical_results.ipynb`) usa
  `X_test["customer_age"] >= 50`: el grupo "mayor" es el de 50 o más años.

Paper y código no coinciden. **Decisión: `customer_age >= 50`**, como en el
código oficial, para que los resultados de equidad sean comparables con los
publicados.

## Referencia: umbral al 5 % de FPR en el código oficial

```python
threshold = np.min(thresholds[fprs == max(fprs[fprs < 0.05])])
```

Se toma el umbral cuyo FPR es el mayor **estrictamente por debajo** del 5 %.
El cociente de FPR entre grupos se calcula como el FPR menor dividido entre el
mayor (1 = paridad).
