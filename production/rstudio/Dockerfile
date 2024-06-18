FROM rocker/verse:latest

# Copia el script de instalación de paquetes a la imagen
COPY ./install.packages.R /usr/local/bin/install_packages.R

# Ejecuta el script R para instalar los paquetes si es necesario
RUN Rscript /usr/local/bin/install_packages.R