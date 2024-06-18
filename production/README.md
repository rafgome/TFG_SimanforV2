## Servidores

Simanfor está desplegado sobre 2 servidores en los que se despliegan todos los componentes. La distribución que se ha seguido en el despliegue es:

#### Servidor de aplicación web

Contiene el frontend, backend y base de datos que permiten la gestión visual de las simulaciones. Todos los componentes están empaquetados en contenedores que se despliegan de forma automática.

#### Servidor de simulación

Contiene los scripts que permiten lanzar una simulación nueva.

## Arquitectura general

Simanfor está separado en 4 elementos principales que gestionan toda la operativa del simulador. Estos elementos son:

#### Frontend (aplicación web)

Aplicación desarrollada sobre Angular 9 que contiene la parte visual de la herramienta web que permite gestionar el simulador.

#### Backend (aplicación web)

Aplicación desarrollada sobre Node.js + Express. Disponibiliza un API Rest al que se conecta el Front que permite realizar toda la operativa del Simulador en el backend.

TODO: Añadir documentación API Rest.

Además, esta aplicación se conecta al servidor de simulación y la base de datos para realizar todas las operativas necesarias en Simanfor.

#### Base de datos

Base de datos MongoDB que ofrece almacenamiento persistente a Simanfor. Almacena 4 tipos de documentos:

- Usuarios
- Inventarios
- Modelos
- Escenarios

El almacenamiento persistente de Simanfor está alojado en el directorio ``~/data_mongo`` del ``Servidor de aplicación web``.

#### Scripts simulación

Están alojados en el servidor de simulación y permiten lanzar una nueva simulación. El proceso para lanzar una nueva simulación es el siguiente:

1. Se sube el inventario en formato xlsx al directorio ``$SCRATCH/input/inventory/``.
2. Se sube la descripción del escenario en formato JSON al directorio ``$SCRATCH/input/scenario/``.
3. Se lanza la simulacion con el comando:

```
sbatch $HOME/auto/launch.sh ${scenarioJSONFile} ${scenarioId}
```

4. Esperamos a que la simulación se finalice a través del comando ``sbatch``.
5. Descargamos el fichero zip resultante del directorio ``$SCRATCH/output/``.

Toda la comunicación entre backend y el servidor de simulación se realiza a través de protocolo SSH. Las funciones que gestionan la comunicación en el backend son:

- initScenario(): Lanza el job de un nuevo escenario en el supercomputador usando el script alojado en ``$HOME/auto/launch.sh`` (https://github.com/simanfor-dask/web-backend/blob/master/tools/ssh.js#L87).
- upload(): Sube un fichero al supercomputador (https://github.com/simanfor-dask/web-backend/blob/master/tools/ssh.js#L87).
- download(): Descarga un fichero del supercomputador (https://github.com/simanfor-dask/web-backend/blob/master/tools/ssh.js#L155).
- squeue(): Obtiene el estado de los jobs lanzados en el supercomputador (https://github.com/simanfor-dask/web-backend/blob/master/tools/ssh.js#L64).

## Arquitectura frontend

El frontend está alojado en el repositorio https://github.com/simanfor-dask/web-frontend y está desarrollador sobre Angular 9.

Para lanzar el front en local, debes ejecutar los siguientes comandos:

- git clone https://github.com/simanfor-dask/web-frontend
- npm install
- npm start

Podrás acceder a la web en local desde ``http://localhost:4200/`` en un navegador web.

Cuando subas nuevo código y quieras desplegarlo en producción, tendrás que generar una nueva versión del frontend. Puedes hacerlo desde el siguiente enlace: https://github.com/simanfor-dask/web-frontend/releases/new.

Si generas una nueva versión, se lanzará el pipeline que construye el paquete de producción. Puedes ver todos los pipelines ejecutados en https://github.com/simanfor-dask/web-frontend/actions. Antes de poder usar una nueva versión en producción, tendrás que esperar a que su pipeline finalice.

Los directorios más útiles que contienen los estáticos de Simanfor son los siguientes:

| Directorio / fichero | Descripción |
| - | - |
| https://github.com/simanfor-dask/web-frontend/tree/master/src/assets/i18n | Ficheros JSON de idiomas. Al añadir un idioma, se debe añadir [aquí](https://github.com/simanfor-dask/web-frontend/blob/master/src/app/app.component.ts#L25) y definir el idioma de fallback [aquí](https://github.com/simanfor-dask/web-frontend/blob/master/src/app/app.component.ts#L27) |
| https://github.com/simanfor-dask/web-frontend/tree/master/src/assets/images | Imágenes |
| https://github.com/simanfor-dask/web-frontend/tree/master/src/assets/styles | Hojas de estilo |
| https://github.com/simanfor-dask/web-frontend/blob/master/src/app/pages/help/help.component.html | Página de ayuda |
| https://github.com/simanfor-dask/web-frontend/blob/master/src/app/pages/home/home.component.html | Página Home |
| https://github.com/simanfor-dask/web-frontend/blob/master/src/app/pages/legal/legal.component.html | Página legal |
| https://github.com/simanfor-dask/web-frontend/blob/master/src/app/pages/login/login.component.html | Página login |

Recuerda que cuando quieras añadir un texto nuevo con traducciones, deberás actualizar los JSON de traducciones con el nuevo texto y podrás usarlo en cualquier documento ``html`` escribiendo ``{{ 'tu.clave.del.string' | translate }}``.

## Arquitectura backend

El backend está alojado en el repositorio https://github.com/simanfor-dask/web-backend y está desarrollado sobre Node.js v10.16.0.

Para lanzar el back en local, debes ejecutar los siguientes comandos:

- git clone https://github.com/simanfor-dask/web-backend
- npm install
- npm start

Para que el back funcione correctamente, debes crear un documento ``.env`` en la raiz del directorio donde descargues todos los ficheros. Este documento contiene todas las variables de entorno de configuración para conectar el back al resto de elementos de la infraestructura. Aquí te dejamos un ejemplo del contenido:

```
SSH_HOST="ssh_host_servidor_simulacion"
SSH_PORT="ssh_port_servidor_simulacion"
SSH_USERNAME="ssh_username_servidor_simulacion"
SSH_PASSWORD="ssh_password_servidor_simulacion"
SCRATCH_PATH="servidor_simulacion_scratch_path"
INPUT_SCRATCH_PATH="servidor_simulacion_input_path"
OUTPUT_SCRATCH_PATH="servidor_simulacion_output_path"
MONGO_HOST="mongodb+srv://user:password@host:port"
MONGO_DB="mongodb_database_name"
JWT_MASTER_TOKEN="random_string_to_encrypt_passwords"
SERVER_PATH="domain_path_where_app_is_hosted"
```

```
SERVER_PATH="" ##for local deploiment
```

Cuando subas nuevo código y quieras desplegarlo en producción, tendrás que generar una nueva versión del backend. Puedes hacerlo desde el siguiente enlace: https://github.com/simanfor-dask/web-backend/releases/new.

Si generas una nueva versión, se lanzará el pipeline que construye el paquete de producción. Puedes ver todos los pipelines ejecutados en https://github.com/simanfor-dask/web-backend/actions. Antes de poder usar una nueva versión en producción, tendrás que esperar a que su pipeline finalice.

## Despliegue

#### Servidor de aplicación web

1. Generar una nueva build del frontend: https://github.com/simanfor-dask/web-frontend/releases/new.
2. Generar una nueva build del backend: https://github.com/simanfor-dask/web-backend/releases/new.
3. Actualizar versiones en https://github.com/simanfor-dask/production/blob/master/docker-compose.yml#L33 y https://github.com/simanfor-dask/production/blob/master/docker-compose.yml#L22.
4. Desplegar el servidor de aplicación web:

```
ssh root@157.88.224.247
cd ~/
make update && make up
```

#### Servidor de simulación

TODO
