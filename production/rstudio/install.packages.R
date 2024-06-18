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