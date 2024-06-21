# Lista de paquetes necesarios
packages <- c("plyr", "openxlsx", "plotly")

# Función para verificar e instalar paquetes
install_if_missing <- function(pkg) {
    if (!require(pkg, character.only = TRUE)) {
        install.packages(pkg, repos = "https://cran.rstudio.com/")
    }
}

# Verificar e instalar cada paquete
sapply(packages, install_if_missing)

# Descomentar estas líneas y comentar las anteriores si se quiere forzar la instalación de los paquetes
# # Lista de paquetes necesarios
# packages <- c("plyr", "openxlsx", "plotly")

# # Instalar cada paquete directamente
# install.packages(packages, repos = "https://cran.rstudio.com/")