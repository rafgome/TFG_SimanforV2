# SIMANFOR web back-end
## Purpose of this repository
Contains backend for simanfor web page

It has been developed by sngular

## Local config for UBUNTU 
### .env file contents for environment config of local backend
```
SSH_HOST="localhost"
SSH_PORT="2222"
SSH_USERNAME="simanfor"
SSH_PASSWORD="SM$sm4"
SCRATCH_PATH="/scratch/uva_iufor_1/uva_iufor_1_3"
INPUT_SCRATCH_PATH="/input"
OUTPUT_SCRATCH_PATH="/output"
MONGO_HOST="mongodb://127.0.0.1:27017"
MONGO_DB="simanfor"
JWT_MASTER_TOKEN="simanforsngular"
SERVER_PATH=""
```
### mongoDB
install mongo following official web repository (not ubuntu) https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
open mongo console and do following task
- create a database named as in connection file: simanfor (MONGO_DB="simanfor")
- create user to login in command:
```
db.user.insert({ user: 'test',
  password: '$2b$10$lTtjPZVletBcpY0ctLI27efMch/KRKg3SiE.YQp7.cYWgUGNRYs6m',
  role: 'admin',
  name: 'name',
  surname: 'surname',
  center: 'center',
  department: 'department',
  email: 'email',
  phone: 'phone'
});
```

### ssh in localhost
It is adviseble to create a normal user to access throught ssh
To add a new user in Ubuntu run ``sudo adduser simanfor``
To install and enable ssh you can follow lot of webpages, such as https://linuxize.com/post/how-to-enable-ssh-on-ubuntu-20-04/ or https://devconnected.com/how-to-install-and-enable-ssh-server-on-ubuntu-20-04/

```
sudo apt update
sudo apt install openssh-server
```

Once the installation is complete, the SSH service will start automatically. You can verify that SSH is running by typing: ``sudo systemctl status ssh``

Modify ssh configuration to allow only local access editing your ``/etc/ssh/sshd_config`` file, changing some lines to your desires values:
```
ListenAddress 127.0.0.1
Port 2222
PermitRootLogin no
```

And restart the service: ``sudo systemctl restart sshd ``

Check whether you are able to connect with user simanfor ``ssh -p 2222 simanfor@127.0.0.1``

Ubuntu ships with a firewall configuration tool called UFW. If the firewall is enabled on your system, make sure to open the SSH port: ``sudo ufw allow ssh``

### sbatch sin slurm
Rather than installing and configuring SLURM to emulate HPC, create an alias of normal scripting ``alias sbatch='sh'``
You can include in your local configuration to avoid typing alias in every sesion including previous line in file
``~/.bashrc``
For loading run ``source ~/.bashrc``

### Scratch folders for SM4 and auto.sh file 
SIMANFOR Web will run the script ``$HOME/auto/launch.sh`` after connecting throught ssh. For local running you should include a proper file with following structure:
```
#!/bin/bash

ROOT=/home/cristobal/simanfor/simulator/simulator

SCRATCH=/scratch/uva_iufor_1/uva_iufor_1_3

EXPERIMENT_JSON=$1
EXPERIMENT_ID=$2

currentDir=${pwd}

cd $ROOT/src
python3 main.py -s $SCRATCH/input/$EXPERIMENT_JSON -logging_config_file $ROOT/config_files/logging.conf

cd $SCRATCH/output
zip -m ${EXPERIMENT_ID}.zip ${EXPERIMENT_ID}_Output_Plot_*

cd $currentDir
```

You should also create folder structure for scratch contents:
```
sudo mkdir /scratch
sudo mkdir /scratch/uva_iufor_1
cd /scratch
sudo chmod 777 uva_iufor_1
cd /uva_iufor_1
mkdir /scratch/uva_iufor_1_3
cd /uva_iufor_1_3
mkdir /input
mkdir /outout
```

The ``input`` folder will store scenario files as well as input inventory files, while ``output`` folder will store the result of the simulations
