# TFG_SimanforV2
SIMANFOR V2. TFG de Ingeniería Informática de Rafael Gómez Carrión

## Puesta en marcha del proyecto
Para poner clonar el repositorio en una máquina Linux local, eejcutar el siguiente comando: git clone https://github.com/rafgome/TFG_SimanforV2.git.

Una vez se tiene el proyecto en local, abrir el fichero docker-compose.yml del directorio TFG_SimanforV2/production. En él, modificar los siguientes elementos:

- Volúmenes de persistencia del backend: Cambiar las rutas a las de la máquina local
- Volúmenes de persistencia de la base de datos (contenedor mongo): Cambiar la ruta a la de la máquina local, pero sin que esa ruta se encuentre dentro del directorio padre del proyecto
- Volúmenes de persistencia de RSTudio Server (contenedor simforstudio): Cambiar las rutas a las de la máquina local

En ese mismo directorio (TFG_SimanforV2/production), ejecutar los siguientes comandos:

- docker compose build, para generar las imágenes del proyecto Docker
- docker compose up, para lanzar los contenedores

Antes de probar el proyecto, se debe configurar la base de datos. Leer la siguiente sección.

## Base de datos
Se incluyen una base de datos mongo con dos usuarios:

- Un usuario administrador: username = admin, password = admin
- Un usuario normal: username = basic, password = basic

Se incluyen también varios modelos, un inventario y tres escenarios que servirán como ejemplo para realizar pruebas.

Todos estos elementos se incluyen en forma de un mongo dump que debe ser restaurado en el contenedor para disponer de una base de datos. Los pasos a seguir son los siguientes:

- Acceder al directorio TFG_SimanforV2/web-backend/mongo/, donde está almacenado el mongodump.
- Ejecutar el siguiente comando, para copiarlo en el contenedor de mongoDB: docker cp ./dump/ mongo:mongo_dump
- Entrar al bash del contenedor mongo, ejecutando el siguiente comando: docker exec -it mongo bash
- Una vez dentro del contenedor, restaurar la base de datos indicando la contraseña especificada en el contenedor del backend del archivo docker-compose.yml: mongorestore -u database_simanfor mongo_dump/

Tras esto, la base de datos del proyecto está poblada y lista para ser utilizada.

