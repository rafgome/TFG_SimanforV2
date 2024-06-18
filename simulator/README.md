<center>
<img src="https://raw.githubusercontent.com/simanfor/web/main/logos/simanfor.png" alt="simanfor" width="350"/>
</center>

---

# SIMANFOR

SIMANFOR, Support system for simulating Sustainable Forest Management Alternatives 

SIMANFOR is a tool to simulate different kind of operations over trees' plot. This tool has been designed by iuFOR-UVa (Felipe Bravo's group) and is being develop in cooperation with S|ngular using python and Apache Dask. A detailed description of contributing team and funding project is available at https://www.simanfor.es/help


## Prerequisites

Open your terminal and set your directory on the folder simulator by using:

```
cd <path ending on simulator/simulator>
```

## Python Virtual Environment

Before the installation, it's recommended to create a Python Virtual Environment to be sure that your libraries doesn't have interferences with another ones you have already installed. To do that, just:

1. Create the virtual environment on the desired folder:

*Linux and Windows*

`python -m venv venv`

2. Activate the virtual environment:

*Linux*

`source venv/bin/activate`

*Windows*

`venv/Scripts/activate.bat`

3. Install the libraries needed from a requirements.txt file:

*Linux and Windows*

`pip install -r requirements.txt`


## Installation

Installing process. This tools includes some instalation script for each platform:

#### Windows Instalation: run the next command

```
install.sh
```

*in case it didn't work, run this*

```
pip install -r "requirements.txt"
```


#### Linux and Mac Instalation  
  
(you must have pip3 already installed; if not, run this before: sudo apt install python3-pip)  
(if you have problems installing python libraries, run this: pip3 install -r requirements.txt)


```
sudo ./install.sh
```

*in case it didn't work, run this*

```
pip3 install -r "requirements.txt"
```

*The document requirements_avv2023.txt is an alternative with the libraries version fixed to be sure that new libraries versions doesn't make problems to the simulator. If the simulator doesn't work, then create a new environment and install requirements_avv2023.txt libraries*

### Creating Scenario files


### How to use

Finally the simulator can be executed using the python program called main.py or using the run.sh script. For example if we can run a basic execution on *Linux* or *Windows* using a simple scenario file we should execute next line:

```
python main.py -s scenario.json
```

If we want the output translated to another language, then we should include the next comand:

*Available languages: english (en), spanish (es, by default) and galician (gl)*

```
python main.py -l language -s scenario.json
```


There are different options to execute this software:

```
usage: main.py [-h] -s scenario_file [-c configuration_file] [-e engine]
               [-logging_config_file logging_config_file] [-log_path log_path]
               [-v verbosity_level]
               [-l output language]
main.py: error: the following arguments are required: -s


```

Planning tool to run planners and domains using singularity containers. These are the different arguments:
```
-h, --help                show this help message and exit.
-l language               change the language of the output:
                            - english: language == en
                            - spanish (by default): language == es
                            - galician: language == gl
-s scenario_file     	  a path to the file with the information about 
			  the simulator and the scenario. 
-c configuration_file     a path to the file with the information about 
                          the main configuration of the simulator. The default 
			  configuration file is called simanfor.conf
-e engine                 a number parameter (integer) which defines 
			  the execution engine (1: Machine, 2: Cloud, 3: Super). 
			  The default value is 1 (Machine). 
-logging_config_file      a path to the file with the logging configuration.
-log_path path     	  a path to the location of the logging file. 
--v verbosity_level       a number parameter (integer) which defines the verbosity 
                          level of the simulator (1: Error, 5: Warning, 10 Warn, 15 Debug, 20 Info). 
			  The default value is 1 (Error).
```

## Execute www.simanfor.es on localhost during development
There are two ways to execute the full web version of simanfor locally:
    
### Using docker with docker-compose
TODO:
work in progress, soon to be explained here.

### Running everything locally

#### web-frontend 
explained here: ... TODO

#### web-backend and mongodb

You need to use the branch `infra/local-simulator`.

You need a `.env` file at the same level as web-backend, e.g. 
`/home/spiros/dev/repos/simanfor-dask/web-backend/.env` with similar content to this:

```
SCRATCH_PATH="/home/spiros/dev/repos/simanfor-dask/simulator/simulator/scratch/simanfor"
INPUT_SCRATCH_PATH="/input"
OUTPUT_SCRATCH_PATH="/output"
MONGO_HOST="mongodb://127.0.0.1:27017"
MONGO_DB="simanfor"
JWT_MASTER_TOKEN="simanforsngular"
SERVER_PATH=""
```

Further information explained here: ... TODO

#### simulator
You need to use the branch `infra/local-simulator` and edit the file: `./simulator/launch.sh`

For example:

```
ROOT=/home/spiros/dev/simanfor-dask/simulator/simulator
SCRATCH=/home/spiros/dev/simanfor-dask/web-backend
EXPERIMENT_JSON=$1

python3 $ROOT/src/main.py -s $SCRATCH/input/scenario/$EXPERIMENT_JSON -logging_config_file $ROOT/config_files/logging.conf
```
The above file is called when a scenario is run.

If this `README.md` is in the `path/to/simanfor-dask/simulator` directory, 
the `launch.sh` file needs to be in the same directory pointed to by `$ROOT`

here: `path/to/simanfor-dask/simulator/simulator/launch.sh`

`SCRATCH` needs to point to `path/to/simanfor-dask/web-backend`

and the output of the simulation will be found at what `SCRATCH_PATH` + `OUTPUT_SCRATCH_PATH` is pointing to in `web-backend/.env`.

For the above `web-backend/.env` file, the output is found here:
`/home/spiros/dev/repos/simanfor-dask/simulator/simulator/scratch/simanfor/output`


## Support information (spanish)

*   [Escenarios en SIMANFOR](https://github.com/simanfor/escenarios)
*   [Introducción a SIMANFOR](https://github.com/simanfor/introduccion)
*   [Inventarios en SIMANFOR](https://github.com/simanfor/inventarios)
*   [Manual de uso de SIMANFOR](https://github.com/simanfor/manual)
*   [Modelos en SIMANFOR](https://github.com/simanfor/modelos)
*   [Publicaciones acerca de SIMANFOR](https://github.com/simanfor/publicaciones)
*   [Resultados de simulación en SIMANFOR](https://github.com/simanfor/resultados)
*   [Web de SIMANFOR](https://github.com/simanfor/web)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Cómo citar SIMANFOR

El uso de SIMANFOR debe citarse de la siguiente forma:

*SIMANFOR (s.f.). Sistema de apoyo para la simulación de alternativas de manejo forestal sostenible. Recuperado el 01 de agosto de 2022 en https://www.simanfor.es*

Además, debe citarse el uso cada modelo incluido en el simulador de acuerdo con la forma de cita propuesta para cada uno de ellos, que puedes consultar en su correspondiente [ficha](https://github.com/simanfor/modelos).


## Contacto

*Para cualquier duda o sugerencia puedes contactar con el equipo técnico de SIMANFOR en simanfor.data@forest.uva.es*.
  

SIMANFOR ha sido desarrollado por: 

<center>
<img src="https://raw.githubusercontent.com/simanfor/web/main/logos/iufor.png" alt="iufor" width="350"/>
<img src="https://raw.githubusercontent.com/simanfor/web/main/logos/UVa-ETSIIAA.png" alt="uva_etsiiaa" width="250"/>
<img src="https://raw.githubusercontent.com/simanfor/web/main/logos/sngular.png" alt="sngular" width="250"/>
</center>
