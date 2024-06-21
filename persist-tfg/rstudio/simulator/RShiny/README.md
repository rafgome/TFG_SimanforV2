# Leer datos
En este script se preparan los archivos necesarios para el RShiny, apartir de los ficheros zip descargados de la web de simanfor.

INSTRUCCIONES DE USO:
Debes de tener los zips (que cada uno de ellos representará un escenario distinto) descargados en la misma ruta. Este será el "input", la ruta donde se hayan descargado estos zips. 
Se cambia el setwd por la ruta donde estén descargados.
Se generaran outputs que se guardan en la ruta que se ha establecito, y se usarán para el script de Shiny

# Gráficos plotly idiomas
En este script se encuentra la aplicación Shiny. Se representan gráficos interactivos para poder visualizar los resultados. En el shiny el usuario podrá elegir la variable que quiere representar en cada gráfico, el archivo, el escenario...  Entre los resultados que se muestran destacan la evolución de las variables generales para cada uno de los archivos al ser aplicado cada proceso, frente al año o a la altura dominante;  el resumen básico de las variables que se utilizan; la representación del volumen frente a la edad tanto cuando se tiene en cuenta solamente la masa actual del árbol a cuando se va acumulando lo que se ha cortado; la represenatción de la biomasa frente a la edad teniendo en cuanta la masa actual del árbol o también recogiendo las cortas y gráficos para las variables generales.

INSTRUCCIONES DE USO:
Los inputs de este script son los outputs del anterior, por lo que tendras que introducir la ruta donde se han guardado, que será la misma que la que has introducido en el script de leer datos. Por tanto, se camabia el setwd.
Se permite seleccionar el idioma. La variable idioma es 1 para inglés, y 2 para español. Por defecto se establece el español.

# Shiny completo
Este script es una fusión de ambos scripts para agilizar el proceso

INSTRUCCIONES DE USO:
En este script se tendrá que cambiar la ruta (setwd) para que esté en el directorio en el que se han descargado todos los zips con los que se desea trabajar. En este caso no se generan outputs ya que los archivos necesarios para el RShiny se quedan en el entorno de R sin necesidad de ser guardados. 
También se permite la selección de idioma (1=> Inglés, 2=>Español)
