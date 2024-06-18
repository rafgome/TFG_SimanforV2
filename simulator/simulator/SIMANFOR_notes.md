# SIMANFOR notas


Aitor Vázquez Veloso, Julio 2023

---

### 4 de julio de 2023

Los modelos mixtos que existen en SIMANFOR son los recogidos en la tesis de Diego Rodríguez de Prado. Se han programado varios modelos que están funcionando, pero en lugar de tener una mezcla de especies por archivo vamos a diseñar una estructura que permita tener un modelo (estructura) única y que acceda a un recopilatorio de ecuaciones alojado en otro archivo, de manera que permita automatizar mucho más cada cambio que hagamos.

Para ello creo 3 documentos:

- mixed_models_Spain: es el "modelo maestro" al que ha de llamar desde el escenario, y que contiene las llamadas a los distintos cálculos programados en otros archivos
- equations_mixed_models: archivo con funciones para el cálculo de variables relacionadas con los modelos mixtos
- equations_tree_models: archivo con funciones para el cálculo de variables relacionadas con los modelos de árbol individual que no diferencian entre especies

---

Hago el siguiente cambio para evitar tener logs muy pesados en el archivo congif_files/logging.conf:

```
	[logger_root]
	level: DEBUG -> CRITICAL
```

Incluyo *TODO* en las partes del código nuevo que dejo sin terminar


---


### julio y agosto de 2023

Irene Arroyo está trabajando en la creación de informes con la librería *shiny* de **R**


---


### 7 de julio de 2023

Incluyo un escenario más para las simulaciones del Life Rebollo.

Voy a incluir índices de diversidad en SIMANFOR como variables nuevas

:bulb: Usando pycharm creo que el trabajo irá mejor

---

### 5 de julio de 2023

Continuo creando funciones para mejorar los modelos mixtos. Hay que crear las siguientes variables:

- DOMINANT_SECTION_SP3, DOMINANT_DBH_SP3, DOMINANT_H_SP3
- MEAN_H_SP3, MEAN_DBH_SP3, MEAN_BA_SP3, H_MIN_SP3, DBH_MIN_SP3, BA_MIN_SP3, H_MAX_SP3, DBH_MAX_SP3, BA_MAX_SP3
- DENSITY_SP3, QM_DBH_SP3, BASAL_AREA_SP3
- SP3_N_PROPORTION and 1/2

Tengo ya el esqueleto principal para las funciones initialize, survival, growth y update_model, aunque todavía hay mucho trabajo por delante.

:pushpin: Falta hacer lo mismo con el ingrowth y con el resto de funciones (crown, biomass...); para estas últimas puedo usar el modelo de existencias.

---

### 6 de julio de 2023

Actualizo requirements (numpy 1.22.0) y la creación de un *virtual environment* en Windows en el README principal. Incluyo la explicación de cómo cambiar el lenguaje del output.

Termino de montar la estructura para introducir la parametrización de todas las especies y mezclas de modelos mixtos.

Tareas:

- Aitor: resolver todos los TODO, revisar que todas las combinaciones funcionen correctamente, crear un inventario de
ejemplo para cada mezcla de especie y un escenario y dejarlo en carpeta test; subir modelos a la web

- Irene: resolver todos los # TODO: *irene* (hasta donde pueda). Dependiendo del tiempo que tengas, si no tienes tareas 
de mayor prioridad, puedes coger el excel de test de modelos mixtos y crear un archivo (con los mismos datos) en los que 
modifiques los códigos de especie 1 y 2 en la hoja árboles y parcelas (también puedes dejar todo en un mismo archivo, 
pero entonces hay que cambiar los códigos de parela); si haces un archivo por mezcla, entonces haz otro archivo de 
escenario para cada mezcla, donde modifiques el nombre del output y nombre del input

---

### 11 de agosto de 2023

Corrijo un error en la lectura de archivos XLSX - :pushpin: habría que intentar corregirlo para archivos csv

Introduzco índices de diversidad de especies: shannon, simpson, margalef y pielou

Introduzco una nueva variable de biomasa para agrupar todas las biomasas de ramas < 7 cm y hojas

Introduzco 3 nuevas variables para registrar el crecimiento de cada árbol: dbh_i, basal_area_i, height_i

Creo todas las variables nuevas y otras adicionales para usar posteriormente

:brain: Con las variables de crecimiento he intentado ponerlas a 0 cuando se aplican cortas (he creado una función nueva para ello).
Cuando lo hago así, por algún motivo se sobreescriben los valores en los procesos que no son corta y se ponen a 0.

He decidido dejarlo en las cortas con el valor del crecimiento anterior para no complicarme.

---

### 16 de agosto de 2023

Incluyo el modelo Life Rebollo con las modificaciones necesarias para que se aplique el clima en la ecuación de mortalidad.

---

### 17 de agosto de 2023

- Corregido el Martonne > 2100 (ahora se aplica el del periodo 2080-2100 en lugar del valor actual 2000-2020)

---

### 18 de agosto de 2023

- Incluidas cortas sistemáticas con árboles de porvenir
- Incluidas cortas por lo alto con árboles de porvenir
- Incluida la variable "preserve_trees" para poder indicar la cantidad de árboles que queremos conservar en las cortas
- Creado cut_down_support para partes comunes de los modelos de corta

---

### 07 de septiembre de 2023

- Incluidas dos variables nuevas que calculan un índice de biodiversidad de madera muerta propuesto por CESEFOR (Life Rebollo)

---

### 12 de septiembre de 2023

- comienzo a hacer pruebas con los datos de Soria y Segovia para LifeRebollo
- correcciones menores en el código
- he encontrado que cuando se quiere aplicar ingrowth pero no hay árboles en el rango diamétrico al que ha de aplicar, 
  entonces este ingrowth es 0; voy a intentar que en estas situaciones se cree un árbol nuevo

---

### 21 de septiembre de 2023

- creo el código necesario para poder añadir árboles nuevos como ingrowth en aquellas clases diamétricas en las que ya no quedan árboles.
Los árboles, pese a que se incorporan al inventario, no entran ni en la función recalculate ni en la función update_model que están justo a continuación,
y por lo tanto este código nuevo no me funciona bien

---

### 26 de septiembre de 2023

- problemas con el ingrowth corregidos, ahora ya se pueden añadir árboles nuevos al inventario si no hay ninguno que cumpla la condición
de clase diamétrica
- ahora habría que replicar el proceso para masas mixtas

---

### 27 de septiembre de 2023

incluyo lo siguiente en los modelos de corta para que se mantengan los árboles creados por ingrowth en la simulación:

```
new_plot.clone(plot, full=True)  # full = True also includes trees created by ingrowth
```

### 16 de octubre de 2023

incluyo una función que permite hacer cálculo de contenido de carbono y biomasa

---

### 01 de noviembre de 2023

- he encontrado un error en las cortas. El error era que la corrección hecha el 27 de septiembre en los modelos de corta debe de ser aplicada únicamente cuando se han incluido árboles nuevos
desde la función ingrowth, para los casos contrarios hay que dejar el argumento *full* por defecto

- creo una función nueva en el documento cut_down_support para homogeneizar esto en todos los modelos de corta

---

### 20 de noviembre de 2023

- creo modelos de corta que hacer filtros por especie y creo la variable para poder utilizarla desde el escenario

---

### 21 de noviembre de 2023

- a los modelos anteriores incluyo la variable de escenario "volume_target" para poder expresar la intensidad de corta sobre la parcela o la especie

---

### 22 de noviembre de 2023

- incluyo la variable "volume_target" en los modelos de corta, ahora corregido
- incluyo esto en las plantillas de escenario
- corrijo modelos h/d para masas mixtas
- incluyo combinaciones faltantes para bai en masas mixtas

---

### 27 de noviembre de 2023

- corrijo ids de especies y añado nuevos
- corrijo parámetros ecuaciones h/d

---

### 28 de noviembre de 2023

- corrijo parámetros ecuaciones bai y sdi
- nueva estructura para ecuaciones sdi (basic + climatic)

---

### 30 de noviembre de 2023

- añadidas variables de masa para especie 3 y variables lidar
- ecuaciones BAI y HD funcionan correctamente en masas mixtas
- SDI parece que también funciona

---

### 01 de diciembre de 2023

- añado variables de biomasa para agrupación de tronco y ramas
- añado variables de carbono para tronco, ramas y raíces
- creo el archivo equations_tree_biomass donde recopilo todas las ecuaciones de biomasa y carbono para árbol, parcela y parcela por especies
- creadas variables de parcelas hasta PLOT_VAR79
- incluidas entre nuevas variables de W y C por especie

---

### 11 de diciembre de 2023

- corrijo ecuaciones de volumen
- creo variables de volumen de masa para sp3
- creo función para volumen de masa y de masa por especie
- corrijo ecuaciones de biomasa de masa para masas mixtas
- incluyo más especies en la lista de ids

---

### 12 de diciembre de 2023

- incluyo funciones para obtener los valores de la ecuación de Fang
- incluyo volúmenes comerciales para árboles individuales, parcelas y parcelas por especies
- incluyo variables de volumen comercial para sp3

---

### 22 de diciembre de 2023

- corrijo cálculos de parcela para masas puras y mixtas tras corta
- elimino recalculate_after_cut

*** Tareas pendientes ***:
- revisar ecuaciones h/d en la inicialización
- completar cálculos básicos como dbh promedio o coordenadas
- crear archivos para recopilar ecuaciones de V, merch, h/d, crown...