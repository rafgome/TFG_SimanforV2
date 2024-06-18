################################################################################
#
#           Preparación datos para shiny y aplicación Shiny
#                       Irene Arroyo Hernantes
#
################################################################################
library(utils)
library(readxl)
library(plyr)
library(dplyr)
library(ggplot2)
library(tidyverse)
library(shiny)
library(openxlsx)
library(plotly)

rm(list=ls())

################################################################################
#
#                     Preparación datos
#
################################################################################

# setwd("C:/Users/Irene/Documents/simulator/GraficosR/AbrirDatos")
# setwd("/home/spiros/dev/repos/simanfor-dask/simulator/GraficosR/AbrirDatos")
# setwd("C:/Users/spiro/dev/UVa/simanfor-dask/simulator/GraficosR/AbrirDatos")
# setwd("C:/Users/spiro/dev/UVa/simanfor-dask/simulator/GraficosR/AbrirDatos_spiros")
# setwd("C:/Users/spiro/dev/UVa/simanfor-dask/simulator/GraficosR/AbrirDatos_min")
# setwd("C:/Users/spiro/dev/UVa/simanfor-dask/simulator/GraficosR/AbrirDatos_rafa")
# setwd("C:/Users/spiro/dev/UVa/simanfor-dask/simulator/GraficosR/ShinyRDatos")
setwd("/home/rstudio/simanfor-rscripts/simulator/GraficosR/AbrirDatos")

listaZip<-dir(pattern = "*.zip")

## Descomrpimimos los zips en su carpeta correspondiente
listaEscenarios<-c()
# for(i in 1:length(listaZip)){
#   listaEscenarios<-c(listaEscenarios,paste0("Escenario",i))
#   unzip(zipfile = listaZip[i],exdir=paste0("Escenario",i))
# }

listaEscenarios <- c(listaEscenarios, paste0("Escenario", 1))
unzip(zipfile = listaZip[1], exdir = paste0("Escenario", 1))


datos<-c()
datosArchivo<-c()
## Leemos los archivos de cada uno de los escenarios para juntarles en 1
idEscenario<-0

# for(i in 1:length(listaEscenarios)){
idEscenario <- idEscenario+1
dirEscenario<-paste0(getwd(),"/",listaEscenarios[1])
#setwd(dirEscenario)
archivos<-list.files(dirEscenario,pattern = "xlsx")

plots <- tryCatch({
  read_excel(paste0(dirEscenario, "/", archivos[1]), sheet = "Plots")
}, error=function(e){
  read_excel(paste0(dirEscenario, "/", archivos[1]), sheet = "Parcelas")
})

# plots <- read_excel(paste0(dirEscenario, "/", archivos[1]), sheet = "Parcelas")
plots$IdNombre <- archivos[1]
plots$IdArchivo <- 1
plots$IdEscenario <- idEscenario
datos <- rbind(datos,plots)


plotsArchivo <- tryCatch({
  read.xlsx(paste0(dirEscenario,"/",archivos[1]),startRow = 7,sheet="Summary")
}, error = function(e) {
  read.xlsx(paste0(dirEscenario,"/",archivos[1]),startRow = 7,sheet="Resumen")
})

# check = tryCatch({
#   plotsArchivo <- read.xlsx(paste0(dirEscenario,"/",archivos[1]),startRow = 7,sheet="Summary")
# }, error = function(e) {
#   plotsArchivo<-read.xlsx(paste0(dirEscenario,"/",archivos[1]),startRow = 7,sheet="Resumen")
# })

plotsArchivoVars <- c("Age","Ho","SBT_N","SBT_dg","SBT_G","SBT_V","T_N","T_dg",
                     "T_V","SAT_N","SAT_dg","SAT_G","SAT_V","M_N","M_dg","M_V")
# names(plotsArchivo) <- c("Age","Ho","SBT_N","SBT_dg","SBT_G","SBT_V","T_N","T_dg",
#                        "T_V","SAT_N","SAT_dg","SAT_G","SAT_V","M_N","M_dg","M_V")
names(plotsArchivo) <- plotsArchivoVars

# spiros: here need to remove the unnecessary variables
lengthPlotsArchivo <- length(names(plotsArchivo))

sub <- lengthPlotsArchivo-length(plotsArchivoVars)

plotsArchivo <- plotsArchivo[, -17:-19]


# for(i in 1:sub){
#   plotsArchivo <- plotsArchivo[, -1]
#   print(i)
# }
  
# plotsArchivo <- plotsArchivo[, -1]
# plotsArchivo <- plotsArchivo[, -1]
# plotsArchivo <- plotsArchivo[, -1]


plotsArchivo$IdNombre <- archivos[1]
plotsArchivo$IdArchivo <- 1
plotsArchivo$IdEscenario <- idEscenario
datosArchivo <- rbind(datosArchivo, plotsArchivo)
# }

## Transformamos a df que es mas sencillo su manejo
df<-as.data.frame(datos)

## Añadimos un identificador
df$ID_Escenario_Archivo<-with(df,paste0(IdEscenario,".",IdArchivo))

## Eliminamos las filas innesarias

if ("Action" %in% colnames(df)){
  df <- df[!df$Action == "Initial load", ]
} else {
  df <- df[!df$Accion == "Carga Inicial", ]
}

# df <- tryCatch({
#   df[!df$Action == "Initial load", ]
# }, error = function(e) {
#   df[!df$Accion == "Carga Inicial", ]
# })


write.csv(df,"datosCompletos.csv")
write.csv(datosArchivo,"datosArchivo.csv")
archivos_SBT_N<-data.frame(cbind(
  datosArchivo$Age,
  datosArchivo$Ho,
  datosArchivo$SAT_N,
  datosArchivo$IdNombre,
  datosArchivo$IdArchivo,
  datosArchivo$IdEscenario
))
archivos_SBT_N<-na.omit(archivos_SBT_N)
names(archivos_SBT_N)<-c("Age","Ho","SBT_N","IdNombre","IdArchivo","IdEscenario")
#Añadimos las variables que no estan para asi poderlo unir en un data frame por filas
archivos_SBT_N$SBT_dg<-NA
archivos_SBT_N$SBT_G<-NA
archivos_SBT_N$SBT_V<-NA
archivos_SBT_N$T_N<-NA
archivos_SBT_N$T_dg<-NA
archivos_SBT_N$T_V<-NA
archivos_SBT_N$SAT_N<-NA
archivos_SBT_N$SAT_dg<-NA
archivos_SBT_N$SAT_G<-NA
archivos_SBT_N$SAT_V<-NA
archivos_SBT_N$M_N<-NA
archivos_SBT_N$M_dg<-NA
archivos_SBT_N$M_V<-NA

archivos_SBT_dg<-data.frame(cbind(datosArchivo$Age,datosArchivo$Ho,datosArchivo$SAT_dg,datosArchivo$IdNombre,datosArchivo$IdArchivo,datosArchivo$IdEscenario))
archivos_SBT_dg<-na.omit(archivos_SBT_dg)
names(archivos_SBT_dg)<-c("Age","Ho","SBT_dg","IdNombre","IdArchivo","IdEscenario")
#Añadimos las variables que no estan para asi poderlo unir en un data frame por filas
archivos_SBT_dg$SBT_N<-NA
archivos_SBT_dg$SBT_G<-NA
archivos_SBT_dg$SBT_V<-NA
archivos_SBT_dg$T_N<-NA
archivos_SBT_dg$T_dg<-NA
archivos_SBT_dg$T_V<-NA
archivos_SBT_dg$SAT_N<-NA
archivos_SBT_dg$SAT_dg<-NA
archivos_SBT_dg$SAT_G<-NA
archivos_SBT_dg$SAT_V<-NA
archivos_SBT_dg$M_N<-NA
archivos_SBT_dg$M_dg<-NA
archivos_SBT_dg$M_V<-NA

archivos_SBT_G<-data.frame(cbind(datosArchivo$Age,datosArchivo$Ho,datosArchivo$SAT_G,datosArchivo$IdNombre,datosArchivo$IdArchivo,datosArchivo$IdEscenario))
archivos_SBT_G<-na.omit(archivos_SBT_G)
names(archivos_SBT_G)<-c("Age","Ho","SBT_G","IdNombre","IdArchivo","IdEscenario")
#Añadimos las variables que no estan para asi poderlo unir en un data frame por filas
archivos_SBT_G$SBT_dg<-NA
archivos_SBT_G$SBT_N<-NA
archivos_SBT_G$SBT_V<-NA
archivos_SBT_G$T_N<-NA
archivos_SBT_G$T_dg<-NA
archivos_SBT_G$T_V<-NA
archivos_SBT_G$SAT_N<-NA
archivos_SBT_G$SAT_dg<-NA
archivos_SBT_G$SAT_G<-NA
archivos_SBT_G$SAT_V<-NA
archivos_SBT_G$M_N<-NA
archivos_SBT_G$M_dg<-NA
archivos_SBT_G$M_V<-NA

archivos_SBT_V<-data.frame(cbind(datosArchivo$Age,datosArchivo$Ho,datosArchivo$SAT_V,datosArchivo$IdNombre,datosArchivo$IdArchivo,datosArchivo$IdEscenario))
archivos_SBT_V<-na.omit(archivos_SBT_V)
names(archivos_SBT_V)<-c("Age","Ho","SBT_V","IdNombre","IdArchivo","IdEscenario")
#Añadimos las variables que no estan para asi poderlo unir en un data frame por filas
archivos_SBT_V$SBT_dg<-NA
archivos_SBT_V$SBT_G<-NA
archivos_SBT_V$SBT_N<-NA
archivos_SBT_V$T_N<-NA
archivos_SBT_V$T_dg<-NA
archivos_SBT_V$T_V<-NA
archivos_SBT_V$SAT_N<-NA
archivos_SBT_V$SAT_dg<-NA
archivos_SBT_V$SAT_G<-NA
archivos_SBT_V$SAT_V<-NA
archivos_SBT_V$M_N<-NA
archivos_SBT_V$M_dg<-NA
archivos_SBT_V$M_V<-NA

## Unimos los datos
datosCorta<-rbind(datosArchivo,archivos_SBT_N,archivos_SBT_dg,archivos_SBT_G,archivos_SBT_V)

## Ordenamos por año, escenario y archivo
dfArchivo<-datosCorta[order(datosCorta$IdEscenario,datosCorta$IdArchivo,as.numeric(datosCorta$Age)), ]


################################################################################
## Calcular las diferencias entre cada escenario
################################################################################
# if ("Scenario_file_name" %in% names(df)) {
#   scenario_file <- df$Scenario_file_name 
#   print("it exists")
# } else {
#   scenario_file <- df$Nombre_archivo_escenario 
#   print("it doesn't")
# }

# diferencias <- df %>% group_by(IdNombre, Nombre_archivo_escenario)

if ("Scenario_file_name" %in% colnames(df)) {
  diferencias <- df %>%
    group_by(IdNombre, Scenario_file_name) %>%
    # group_by(IdNombre, Nombre_archivo_escenario) %>%
    mutate(
      V_diff = V - lag(V),
      WSW_diff= WSW - lag(WSW),
      WTHICKB_diff= WTHICKB - lag(WTHICKB),
      WB2_7_diff= WB2_7 - lag(WB2_7),
      WTHINB_diff= WTHINB - lag(WTHINB),
      WTBL_diff= WTBL - lag(WTBL),
      WR_diff= WR - lag(WR),
      WT_diff= WT - lag(WT),
      V_unwinding_diff = V_unwinding - lag(V_unwinding),
      V_veneer_diff = V_veneer - lag(V_veneer),
      V_saw_small_diff = V_saw_small - lag(V_saw_small),
      V_saw_big_diff = V_saw_big - lag(V_saw_big),
      V_saw_canter_diff = V_saw_canter - lag(V_saw_canter),
      V_post_diff = V_post - lag(V_post),
      V_stake_diff = V_stake - lag(V_stake),
      V_chips_diff = V_chips - lag(V_chips)
    )
} else {
  diferencias <- df %>%
    group_by(IdNombre, Nombre_archivo_escenario) %>%
    mutate(
      # V_diff = V - lag(V),
      WSW_diff= WSW - lag(WSW),
      # WTHICKB_diff= WTHICKB - lag(WTHICKB),
      WB2_t_diff= WB2_t - lag(WB2_t),
      # WTHINB_diff= WTHINB - lag(WTHINB),
      WTBL_diff= WTBL - lag(WTBL),
      WR_diff= WR - lag(WR),
      WT_diff= WT - lag(WT),
      # V_unwinding_diff = V_unwinding - lag(V_unwinding),
      V_incorporado_diff = V_incorporado - lag(V_incorporado),
      # V_veneer_diff = V_veneer - lag(V_veneer),
      # V_saw_small_diff = V_saw_small - lag(V_saw_small),
      V_sierra_diff = V_sierra - lag(V_sierra),
      # V_saw_big_diff = V_saw_big - lag(V_saw_big),
      V_sierra_gruesa_diff = V_sierra_gruesa - lag(V_sierra_gruesa),
      # V_unwinding_diff = V_unwinding - lag(V_unwinding),
      V_sierra_canter_diff = V_sierra_canter - lag(V_sierra_canter),
      # V_post_diff = V_post - lag(V_post),
      V_trituracion_diff = V_trituracion - lag(V_trituracion),
      # V_unwinding_diff = V_unwinding - lag(V_unwinding),
      # V_stake_diff = V_stake - lag(V_stake),
      # V_chips_diff = V_chips - lag(V_chips)
    )
}


df_diferencias<-as.data.frame(diferencias)

################################################################################
## Cálculos acumulados
################################################################################
## Vamos a calcular el total acumulado en cada uno de los escenarios para cada
## uno de los plots
df_acum<-tibble()

## COMPROBAR QUE ESTA LA VARIABLE EN EL DATA FRAME!!!!!

# ##Seleccionamos el escenario correspondiente
# for(i in unique(df_diferencias$Scenario_file_name)){
#   ##Seleccionamos los datos que lo cumplen
#   aux<-df_diferencias[df_diferencias$Scenario_file_name==i,]
#   ##Seleccionamos el plot
#   for(j in unique(aux$IdNombre)){
#     ##Seleccionamos los datos que lo cumplen
#     aux2<-aux[aux$IdNombre==j,]
#     ## Valores iniciales de las variables que se van a crear
#     all_V <- all_WSW <- all_WTHICKB <- all_WB2_7 <- all_WTHINB <- all_WTBL <- all_WR <- all_WT <- all_V_unwinding <- all_V_veneer <- all_V_saw_big <- all_V_saw_small <- all_V_saw_canter <- all_V_post <- all_V_stake <- all_V_chips <- 0
#     ## para cada fila
#     for(k in 1:nrow(aux2)){
#       # seleccionamos los datos
#       new_row <- aux2[k, ]
# 
#       # si es la primera, tomamos el valor inicial
#       if(k == 1){
# 
#         # valores inciales
#         all_V <- new_row$V
#         all_WSW <- new_row$WSW
#         all_WTHICKB <- new_row$WTHICKB
#         all_WB2_7 <- new_row$WB2_7
#         all_WTHINB <- new_row$WTHINB
#         all_WTBL <- new_row$WTBL
#         all_WR <- new_row$WR
#         all_WT <- new_row$WT
#         all_V_unwinding <- new_row$V_unwinding
#         all_V_veneer <- new_row$V_veneer
#         all_V_saw_big <- new_row$V_saw_big
#         all_V_saw_small <- new_row$V_saw_small
#         all_V_saw_canter <- new_row$V_saw_canter
#         all_V_post <- new_row$V_post
#         all_V_stake <- new_row$V_stake
#         all_V_chips <- new_row$V_chips
# 
#         # añadimos el valor
#         new_row$V_all <- all_V
#         new_row$WSW_all <- all_WSW
#         new_row$WTHICKB_all <- all_WTHICKB
#         new_row$WB2_7_all <- all_WB2_7
#         new_row$WTHINB_all <- all_WTHINB
#         new_row$WTBL_all <- all_WTBL
#         new_row$WR_all <- all_WR
#         new_row$WT_all <- all_WT
#         new_row$V_unwinding_all <- all_V_unwinding
#         new_row$V_veneer_all <- all_V_veneer
#         new_row$V_saw_big_all <- all_V_saw_big
#         new_row$V_saw_small_all <- all_V_saw_small
#         new_row$V_saw_canter_all <- all_V_saw_canter
#         new_row$V_post_all <- all_V_post
#         new_row$V_stake_all <- all_V_stake
#         new_row$V_chips_all <- all_V_chips
# 
#         # añadir la diferencia
#       }else{
# 
#         # sumar el incremento
#         all_V <- all_V + abs(new_row$V_diff)
#         all_WSW <- all_WSW + abs(new_row$WSW_diff)
#         all_WTHICKB <- all_WTHICKB + abs(new_row$WTHICKB_diff)
#         all_WB2_7 <- all_WB2_7 + abs(new_row$WB2_7_diff)
#         all_WTHINB <- all_WTHINB + abs(new_row$WTHINB_diff)
#         all_WTBL <- all_WTBL + abs(new_row$WTBL_diff)
#         all_WR <- all_WR + abs(new_row$WR_diff)
#         all_WT <- all_WT + abs(new_row$WT_diff)
#         all_V_unwinding <- all_V_unwinding + abs(new_row$V_unwinding_diff)
#         all_V_veneer <- all_V_veneer + abs(new_row$V_veneer_diff)
#         all_V_saw_big <- all_V_saw_big + abs(new_row$V_saw_big_diff)
#         all_V_saw_small <- all_V_saw_small + abs(new_row$V_saw_small_diff)
#         all_V_saw_canter <- all_V_saw_canter + abs(new_row$V_saw_canter_diff)
#         all_V_post <- all_V_post + abs(new_row$V_post_diff)
#         all_V_stake <- all_V_stake + abs(new_row$V_stake_diff)
#         all_V_chips <- all_V_chips + abs(new_row$V_chips_diff)
# 
# 
#         # add value to the row
#         new_row$V_all <- all_V
#         new_row$WSW_all <- all_WSW
#         new_row$WTHICKB_all <- all_WTHICKB
#         new_row$WB2_7_all <- all_WB2_7
#         new_row$WTHINB_all <- all_WTHINB
#         new_row$WTBL_all <- all_WTBL
#         new_row$WR_all <- all_WR
#         new_row$WT_all <- all_WT
#         new_row$V_unwinding_all <- all_V_unwinding
#         new_row$V_veneer_all <- all_V_veneer
#         new_row$V_saw_big_all <- all_V_saw_big
#         new_row$V_saw_small_all <- all_V_saw_small
#         new_row$V_saw_canter_all <- all_V_saw_canter
#         new_row$V_post_all <- all_V_post
#         new_row$V_stake_all <- all_V_stake
#         new_row$V_chips_all <- all_V_chips
#       }
# 
#       # add new row to a new df
#       #df_acum <- bind_rows(df_acum, new_row)
#       df_acum <- rbind(df_acum, new_row)
# 
#     } # row
#   } # plot
# } # scenario

##Seleccionamos el escenario correspondiente
# for(i in unique(df_diferencias$Scenario_file_name)){
for(i in unique(df_diferencias$Nombre_archivo_escenario)) {
  # i <- df_diferencias$Nombre_archivo_escenario
    
  ##Seleccionamos los datos que lo cumplen
  # aux<-df_diferencias[df_diferencias$Scenario_file_name==i,]
  aux<-df_diferencias[df_diferencias$Nombre_archivo_escenario==i,]

  ##Seleccionamos el plot
  # for(j in unique(aux$IdNombre)){
  for(j in unique(aux$IdNombre)) {
  # j <- aux$IdNombre[1]
    
    ##Seleccionamos los datos que lo cumplen
    aux2<-aux[aux$IdNombre==j,]
    ## Valores iniciales de las variables que se van a crear
    # all_V <- all_WSW <- all_WTHICKB <- all_WB2_7 <- all_WTHINB <- all_WTBL <- all_WR <- all_WT <- all_V_unwinding <- all_V_veneer <- all_V_saw_big <- all_V_saw_small <- all_V_saw_canter <- all_V_post <- all_V_stake <- all_V_chips <- 0
    # all_V <- 0
    all_WSW <- 0
    # all_WTHICKB <- 0 
    all_WB2_t <- 0 
    # all_WTHINB <- 0
    all_WTBL <- 0
    all_WR <- 0
    all_WT <- 0
    all_V_incorporado <- 0 
    all_V_sierra <- 0
    all_V_sierra_gruesa <- 0
    # all_V_saw_small <- 0
    all_V_sierra_canter <- 0
    all_V_trituracion <- 0
    # all_V_stake <- 0
    # all_V_chips <- 0
    
    ## para cada fila
    # for(k in 1:nrow(aux2)){
    for(k in 1:nrow(aux2)) {
      # k <- 2
        
      # seleccionamos los datos
      new_row <- aux2[k, ]
      
      # si es la primera, tomamos el valor inicial
      if(k == 1) {

        # valores inciales
        # all_V <- new_row$V
        all_WSW <- new_row$WSW
        # all_WTHICKB <- new_row$WTHICKB
        all_WB2_t <- new_row$WB2_t
        # all_WTHINB <- new_row$WTHINB
        all_WTBL <- new_row$WTBL
        all_WR <- new_row$WR
        all_WT <- new_row$WT
        # all_V_unwinding <- new_row$V_unwinding
        all_V_incorporado <- new_row$V_incorporado
        # all_V_veneer <- new_row$V_veneer
        # all_V_saw_big <- new_row$V_saw_big
        all_V_sierra_gruesa <- new_row$V_sierra_gruesa
        # all_V_saw_small <- new_row$V_saw_small
        all_V_sierra_canter <- new_row$V_sierra_canter
        # all_V_post <- new_row$V_post
        all_V_trituracion <- new_row$V_trituracion
        # all_V_stake <- new_row$V_stake
        # all_V_chips <- new_row$V_chips

        # añadimos el valor
        # new_row$V_all <- all_V
        new_row$WSW_all <- all_WSW
        # new_row$WTHICKB_all <- all_WTHICKB
        new_row$WB2_t_all <- all_WB2_t
        # new_row$WTHINB_all <- all_WTHINB
        new_row$WTBL_all <- all_WTBL
        new_row$WR_all <- all_WR
        new_row$WT_all <- all_WT
        new_row$V_incorporado_all <- all_V_incorporado
        # new_row$V_veneer_all <- all_V_veneer
        new_row$V_sierra_gruesa_all <- all_V_sierra_gruesa
        new_row$V_sierra_all <- all_V_sierra
        new_row$V_sierra_canter_all <- all_V_sierra_canter
        new_row$V_trituracion_all <- all_V_trituracion
        # new_row$V_stake_all <- all_V_stake
        # new_row$V_chips_all <- all_V_chips

        # añadir la diferencia
      } else {
        
        # sumar el incremento
        # all_V <- all_V + abs(new_row$V_diff)
        all_WSW <- all_WSW + abs(new_row$WSW_diff)
        # all_WTHICKB <- all_WTHICKB + abs(new_row$WTHICKB_diff)
        all_WB2_t <- all_WB2_t + abs(new_row$WB2_t_diff)
        # all_WTHINB <- all_WTHINB + abs(new_row$WTHINB_diff)
        all_WTBL <- all_WTBL + abs(new_row$WTBL_diff)
        all_WR <- all_WR + abs(new_row$WR_diff)
        all_WT <- all_WT + abs(new_row$WT_diff)
        # all_V_unwinding <- all_V_unwinding + abs(new_row$V_unwinding_diff)
        all_V_incorporado <- all_V_incorporado + abs(new_row$V_incorporado_diff)
        # all_V_veneer <- all_V_veneer + abs(new_row$V_veneer_diff)
        all_V_sierra <- all_V_sierra + abs(new_row$V_sierra_diff)
        # all_V_saw_big <- all_V_saw_big + abs(new_row$V_saw_big_diff)
        all_V_sierra_gruesa <- all_V_sierra_gruesa + abs(new_row$V_sierra_gruesa_diff)
        # all_V_saw_small <- all_V_saw_small + abs(new_row$V_saw_small_diff)
        all_V_sierra_canter <- all_V_sierra_canter + abs(new_row$V_sierra_canter_diff)
        # all_V_post <- all_V_post + abs(new_row$V_post_diff)
        all_V_trituracion <- all_V_trituracion + abs(new_row$V_trituracion_diff)
        # all_V_stake <- all_V_stake + abs(new_row$V_stake_diff)
        # all_V_chips <- all_V_chips + abs(new_row$V_chips_diff)
        
        
        # add value to the row
        # new_row$V_all <- all_V
        new_row$WSW_all <- all_WSW
        # new_row$WTHICKB_all <- all_WTHICKB
        # new_row$WB2_7_all <- all_WB2_7
        new_row$WB2_t_all <- all_WB2_t
        # new_row$WTHINB_all <- all_WTHINB
        new_row$WTBL_all <- all_WTBL
        new_row$WR_all <- all_WR
        new_row$WT_all <- all_WT
        # new_row$V_unwinding_all <- all_V_unwinding
        new_row$V_incorporado_all <- all_V_incorporado
        # new_row$V_veneer_all <- all_V_veneer
        # new_row$V_saw_big_all <- all_V_saw_big
        # new_row$V_saw_small_all <- all_V_saw_small
        # new_row$V_saw_canter_all <- all_V_saw_canter
        # new_row$V_post_all <- all_V_post
        # new_row$V_stake_all <- all_V_stake
        # new_row$V_chips_all <- all_V_chips
        new_row$V_sierra_all <- all_V_sierra
        new_row$V_sierra_gruesa_all <- all_V_sierra_gruesa
        new_row$V_sierra_canter_all <- all_V_sierra_canter
        new_row$V_trituracion_all <- all_V_trituracion
      }
      
      # add new row to a new df
      #df_acum <- bind_rows(df_acum, new_row)
      df_acum <- rbind(df_acum, new_row)
      
    } # row
  } # plot
} # scenario

##Seleccionamos el escenario correspondiente
i = 1

##Seleccionamos los datos que lo cumplen
aux <- tryCatch({
  df_diferencias[df_diferencias$Scenario_file_name == i,]
}, error = function(e) {
  df_diferencias[df_diferencias$Nombre_archivo_escenario == i,]
})

##Seleccionamos el plot
for(j in unique(aux$IdNombre)){
  ##Seleccionamos los datos que lo cumplen
  aux2<-aux[aux$IdNombre==j,]
  ## Valores iniciales de las variables que se van a crear
  # all_V <- all_WSW <- all_WTHICKB <- all_WB2_7 <- all_WTHINB <- all_WTBL <- all_WR <- all_WT <- all_V_unwinding <- all_V_veneer <- all_V_saw_big <- all_V_saw_small <- all_V_saw_canter <- all_V_post <- all_V_stake <- all_V_chips <- 0
  all_WSW <- all_WB2_t <- all_WTBL <- all_WR <- all_WT <- all_V_incorporado <- all_V_sierra <- all_V_sierra_gruesa <- all_V_sierra_canter <- all_V_trituracion <- 0
  ## para cada fila
  for(k in 1:nrow(aux2)){
    # seleccionamos los datos
    new_row <- aux2[k, ]
    
    # si es la primera, tomamos el valor inicial
    if(k == 1){
      
      # valores inciales
      # all_V <- new_row$V
      all_WSW <- new_row$WSW
      # all_WTHICKB <- new_row$WTHICKB
      all_WB2_t <- new_row$WB2_t
      # all_WTHINB <- new_row$WTHINB
      all_WTBL <- new_row$WTBL
      all_WR <- new_row$WR
      all_WT <- new_row$WT
      all_V_incorporado <- new_row$V_incorporado
      all_V_sierra <- new_row$V_sierra
      all_V_sierra_gruesa <- new_row$V_sierra_gruesa
      # all_V_saw_small <- new_row$V_saw_small
      all_V_sierra_canter <- new_row$V_sierra_canter
      all_V_trituracion <- new_row$V_trituracion
      # all_V_stake <- new_row$V_stake
      # all_V_chips <- new_row$V_chips
      
      # añadimos el valor
      # new_row$V_all <- all_V
      new_row$WSW_all <- all_WSW
      # new_row$WTHICKB_all <- all_WTHICKB
      new_row$WB2_t_all <- all_WB2_t
      # new_row$WTHINB_all <- all_WTHINB
      new_row$WTBL_all <- all_WTBL
      new_row$WR_all <- all_WR
      new_row$WT_all <- all_WT
      new_row$V_incorporado_all <- all_V_incorporado
      # new_row$V_veneer_all <- all_V_veneer
      new_row$V_sierra_gruesa_all <- all_V_sierra_gruesa
      # new_row$V_saw_small_all <- all_V_saw_small
      new_row$V_sierra_canter_all <- all_V_sierra_canter
      new_row$V_trituracion_all <- all_V_trituracion
      # new_row$V_stake_all <- all_V_stake
      # new_row$V_chips_all <- all_V_chips
      
      # añadir la diferencia
    }else{
      
      # sumar el incremento 
      # all_V <- all_V + abs(new_row$V_diff)
      all_WSW <- all_WSW + abs(new_row$WSW_diff)
      # all_WTHICKB <- all_WTHICKB + abs(new_row$WTHICKB_diff)
      all_WB2_t <- all_WB2_t + abs(new_row$WB2_t_diff)
      # all_WTHINB <- all_WTHINB + abs(new_row$WTHINB_diff)
      all_WTBL <- all_WTBL + abs(new_row$WTBL_diff)
      all_WR <- all_WR + abs(new_row$WR_diff)
      all_WT <- all_WT + abs(new_row$WT_diff)
      all_V_incorporado <- all_V_incorporado + abs(new_row$V_incorporado_diff) 
      all_V_sierra <- all_V_sierra + abs(new_row$V_sierra_diff)
      all_V_sierra_gruesa <- all_V_sierra_gruesa + abs(new_row$V_sierra_gruesa_diff)
      # all_V_saw_small <- all_V_saw_small + abs(new_row$V_saw_small_diff)
      all_V_sierra_canter <- all_V_sierra_canter + abs(new_row$V_sierra_canter_diff)
      all_V_trituracion <- all_V_trituracion + abs(new_row$V_trituracion_diff)
      # all_V_stake <- all_V_stake + abs(new_row$V_stake_diff)
      # all_V_chips <- all_V_chips + abs(new_row$V_chips_diff)
      
      
      # add value to the row
      # new_row$V_all <- all_V
      new_row$WSW_all <- all_WSW
      # new_row$WTHICKB_all <- all_WTHICKB
      new_row$WB2_t_all <- all_WB2_t
      # new_row$WTHINB_all <- all_WTHINB
      new_row$WTBL_all <- all_WTBL
      new_row$WR_all <- all_WR
      new_row$WT_all <- all_WT
      new_row$V_incorporado_all <- all_V_incorporado
      new_row$V_sierra_all <- all_V_sierra
      new_row$V_sierra_gruesa_all <- all_V_sierra_gruesa
      # new_row$V_saw_small_all <- all_V_saw_small
      new_row$V_sierra_canter_all <- all_V_sierra_canter
      new_row$V_trituracion_all <- all_V_trituracion
      # new_row$V_stake_all <- all_V_stake
      # new_row$V_chips_all <- all_V_chips
    }
    
    # add new row to a new df
    #df_acum <- bind_rows(df_acum, new_row)
    df_acum <- rbind(df_acum, new_row)
    
  } # row
} # plot
# } # scenario


df_acum<-as.data.frame(df_acum)

# round ages
#df_acum$T <- round(df_acum$T, 5) 

# get scenario code
# df_acum$n_scnr <- tryCatch({
#   substr(df_acum$Scenario_file_name, 17, 19)
# }, error = function(e) {
#   substr(df_acum$Nombre_archivo_escenario, 17, 19)
# })

df_acum$n_scnr <- substr(df_acum$Nombre_archivo_escenario, 17, 19)

# delete empty rows
df_acum <- df_acum[!is.na(df_acum$n_scnr), ]

################################################################################
#                         Cálculos medios
################################################################################
# mean values by scenario and year
df_medias_evolucion<- ddply(df_acum, c('IdEscenario', 'T'), summarise, 
                            
  # general variables                         
  N = mean(N, na.rm = TRUE),                  
  dg = mean(dg, na.rm = TRUE),
  Ho = mean(Ho, na.rm = TRUE),  
  # V = mean(V, na.rm = TRUE), 
  WT = mean(WT, na.rm = TRUE), 
  G = mean(G, na.rm = TRUE),
  SDI = mean(SDI, na.rm=TRUE),
  # HartBecking__Simple_rows = mean(HartBecking__Simple_rows, na.rm=TRUE),
  
  # volume classification 
  # V_unwinding = mean(V_unwinding, na.rm=TRUE),
  V_incorporado = mean(V_incorporado, na.rm=TRUE),
  # V_veneer = mean(V_veneer, na.rm=TRUE),
  # V_saw_big = mean(V_saw_big, na.rm=TRUE),
  # V_saw_small = mean(V_saw_small, na.rm=TRUE),
  # V_saw_canter = mean(V_saw_canter, na.rm=TRUE),
  # V_post = mean(V_post, na.rm=TRUE),
  # V_stake = mean(V_stake, na.rm=TRUE),
  # V_chips = mean(V_chips, na.rm=TRUE),
  V_sierra = mean(V_sierra, na.rm=TRUE),
  V_sierra_gruesa = mean(V_sierra_gruesa, na.rm=TRUE),
  V_sierra_canter = mean(V_sierra_canter, na.rm=TRUE),
  V_trituracion = mean(V_trituracion, na.rm=TRUE),

  # biomass classification - stand variables
  WSW = mean(WSW, na.rm = TRUE),
  # WTHICKB = mean(WTHICKB, na.rm = TRUE),
  # WB2_7 = mean(WB2_7, na.rm = TRUE),
  WB2_t = mean(WB2_t, na.rm = TRUE),
  # WTHINB = mean(WTHINB, na.rm = TRUE),
  WTBL = mean(WTBL, na.rm = TRUE),
  WR = mean(WR, na.rm = TRUE),
  
  
  # all accumulated stand variables
  WSW_all = mean(WSW_all, na.rm = TRUE),
  # WTHICKB_all = mean(WTHICKB_all, na.rm = TRUE),
  WB2_t_all = mean(WB2_t_all, na.rm = TRUE),
  # WTHINB_all = mean(WTHINB_all, na.rm = TRUE),
  WTBL_all = mean(WTBL_all, na.rm = TRUE),
  WR_all = mean(WR_all, na.rm = TRUE),
  WT_all = mean(WT_all, na.rm = TRUE),
  # V_all = mean(V_all, na.rm = TRUE),
  # V_unwinding_all = mean(V_unwinding_all, na.rm=TRUE),
  V_sierra_all = mean(V_sierra_all, na.rm=TRUE),
  V_sierra_gruesa_all = mean(V_sierra_gruesa_all, na.rm=TRUE),
  # V_saw_small_all = mean(V_saw_small_all, na.rm=TRUE),
  V_sierra_canter_all = mean(V_sierra_canter_all, na.rm=TRUE),
  V_trituracion_all = mean(V_trituracion_all, na.rm=TRUE),
  # V_stake_all = mean(V_stake_all, na.rm=TRUE),
  # V_chips_all = mean(V_chips_all, na.rm=TRUE),
)

dfMedias<-df_medias_evolucion


################################################################################
#
#                             Shiny app
#
################################################################################
lLanguage<-list("comentario 1"=c("Graphs for SIMANFOR","Gráficos para SIMANFOR"),
                "comentario 2"=c("Variable to be represented graphically:","Variable para ser representada gráficamente"),
                "comentario 3"=c("Variable of biomass to be represented graphically:(1º graph)","Variable de volumen para ser representada gráficamente(1º gráfico)"),
                "comentario 4"=c("TAKING INTO A COUNT THINNING: Variable of biomass to be represented graphically:(2º graph)","TENIENDO EN CUENTA LAS CORTAS: Variable de biomasa para ser representada gráficamente(2º gráfico)"),
                "comentario 5"=c("General variable to be represented graphically:", "Variable general para ser representada gráficamente"),
                "comentario 6"=c("Variable of volume to be represented graphically:(1º graph)","Variable de volumen para ser representada gráficamente(1º gráfico)"),
                "comentario 7"=c("TAKING INTO A COUNT THINNING: Variable of volume to be represented graphically:(2º graph)","TENIENDO EN CUENTA LAS CORTAS: Variable de volumen para ser representada gráficamente(2º gráfico)"),
                "comentario 8"=c("Select Scenarios:","Seleccionar escenarios"),
                "comentario 9"=c("File of data of a plot: ","Fichero de datos de una parcela"),
                "comentario 10"=c("Welcome to the SIMANFOR results for differents scenarios. To use this app,
      travel through the different pages and manipulate the widgets on the side to 
      display the data as you wish. In one of them, you can select which variable
      you want to represent. In the other, you select which scenarios do you want 
      to represent in the graph. Furthermore, there is another panel which allows to select the data file you want.","Bienvenido a la visualización de los resultados de SIMANFOR para los diferentes escenarios. Para usa esta aplicación, navega a través de las
                                 diferentes pestañas y manipula los desplegables y paneles en el lateral para obtener los datos en la forma que desees. En uno de ellos puedes 
                                 elegir la variable que quieres representar. En el otro, puedes seleccionar que escenarios quieres que se representen en el gráfico. Además, 
                                 hay otro desplegable que permite seleccionar el archivo de datos."),
                "comentario 11"=c("The following list are the variables we will study.","La siguiente lista son las variables que vamos a estudiar"),
                "comentario 12"=c("GENERAL VARIABLES: ","VARIABLES GENERALES:"),
                "comentario 13"=c(": Plot density (nº trees/ha)",": Densidad de la parcela (nº árboles/ha)"),
                "comentario 14"=c(": Plot basal area (m2/ha)"," : Área basimétrica de la parcela (m2/ha)"),
                "comentario 15"=c(": Quadratic mean diameter of the plot (cm)",": Diámetro cuadrático medio de la parcela (cm)"),
                "comentario 16"=c(": Dominant height of the plot (m)",": Altura dominante de la parcela (m)"),
                "comentario 17"=c(": Reineke Index (SDI)",": Índice de Reineke (SDI)"),
                "comentario 18"=c(": Hart-Becking Index (S) calculated to simple rows",": Índice Hart-Becking (S) calculado para marco cuadrado "),
                "comentario 19"=c("VOLUME VARIABLES: ","VARIABLES DE VOLUMEN: "),
                "comentario 20"=c(": Wood volume over bark (m3/ha)",": Volumen de madera de corteza (m3/ha)"),
                "comentario 21"=c(": Wood volume useful to unwinding (m3/ha)",": Volumen de madera útil para desenrrollo (m3/ha)"),
                "comentario 22"=c(": Wood volume useful to veneer (m3/ha)",": Volumen de madera útil para chapa (m3/ha)"),
                "comentario 23"=c(": Wood volume useful to big saw (m3/ha)",": Volumen de madera grande útil para sierra (m3/ha)"),
                "comentario 24"=c(": Wood volume useful to small saw (m3/ha)",": Volumen de madera pequeña útil para sierra (m3/ha)"),
                "comentario 25"=c(": Wood volume useful to canter saw (m3/ha)",": Volumen de madera canter útil para sierra (m3/ha)"),
                "comentario 26"=c(": Wood volume useful to posts (m3/ha)",": Volumen de madera útil para postes y apeas"),
                "comentario 27"=c(": Wood volume useful to stakes (m3/ha)",": Volumen de madera útil para estacas"),
                "comentario 28"=c(": Wood volume useful to chips (m3/ha)",": Volumen de madera útil para astillas"),
                "comentario 29"=c("BIOMASS VARIABLES: ","VARIABLES DE BIOMASA: "),
                "comentario 30"=c(": Total plot biomass, calculated by using all the values calculated before (t/ha)",": Biomasa total de la parcela, calculada usando todos los valores calculados anteriormente (t/ha)"),
                "comentario 31"=c(": Stem wood biomass under bark (t/ha)",": Biomasa de madera del tallo debajo de la corteza (t/ha)"),
                "comentario 32"=c(": Thick branches > 7 cm biomass (t/ha)",": Ramas gruesas > 7 cm de biomasa (t/ha)"),
                "comentario 33"=c(": Branches biomass between 2 and 7 cm as minimum and top height diameter (t/ha)",": Ramas de biomasa entre 2 y 7 cm como mínimo y máximo diámetro de altura (t/ha)"),
                "comentario 34"=c(": Thin branches biomass between 0.5 and 2 cm as minimum and top height diameter (t/ha)",": Ramas finas de biomasa entre 0.5 y 2 cm como mínimo y máximo diámetro de altura (t/ha)"),
                "comentario 35"=c(": Thin branches < 2 cm as top height diameter and leaves biomass (t/ha)",": Ramas finas < 2 cm como diámetro máximo y biomasa de hojas"),
                "comentario 36"=c(": Roots biomass (t/ha)",": Biomasa de las raices (t/ha)"),
                "comentario 37"=c("The first summary refers to the data selected. The second is the general summary of all scenarios", "El primer resumen se refiere al del los datos del archivo seleccionado. El segundo es el resumen general de todos los escenarios."),
                "comentario 38"=c("In the tabs of 'Plot vs Age' and 'Plot vs Ho', we will study the evolutions of the mass of the mount when several
                    processes are carried out, such as thining. The variables used in this web page tabs are summarised in the first summary.",
                                  "En las pestañas 'Plot vs Age' y 'Plot vs Ho', estudiaremos la evolución de la masa en el monte cuando se llevan a cabo
                                  diversos procesos, como la corta. Las variables usadas en esta pestaña de la página web estan recogidas en el primer resumen."),
                "comentario 39"=c(" Stand before thinning, the mass in the mount befaure aplying thinning."," Masa antes de la corta, la masa que hay en el monte antes de que se aplique alguna corta "),
                "comentario 40"=c(": Stand before thinning for the variable N (density)", ": Masa antes de la corta para la variable N (densidad)"),
                "comentario 41"=c(": Stand before thinning for the variable G (basal area)",": Masa antes de la corta para la variable G (área basimétrica)"),
                "comentario 42"=c(": Stand before thinning for the variable V (volume)",": Masa antes de la corta para la variable V (volumen)"),
                "comentario 43"=c(": Stand before thinning for the variable dg (quadratic mean diameter)",": Masa antes de la corta para la variable dg (diámetro cuadrático medio)"),
                "comentario 44"=c(" Thinning, the mass in the mount which is been thinning."," Corta, la masa del monte que va a ser cortada"),
                "comentario 45"=c(": Thinning for the variable N (density)", ": Corta para la variable N (densidad)"),
                "comentario 46"=c(": Thinning for the variable V (volume)", ": Corta para la variable V (volumen)"),
                "comentario 47"=c(": Thinning for the variable dg (quadratic mean diameter)", ": Corta para la variable dg (diámetro cuadrático medio)"),
                "comentario 48"=c(" Stand after thinning, the mass in the mount after the thinning."," Masa después de la corta, la masa en el monte después de la corta"),
                "comentario 49"=c(": Stand after thinning for the variable N (density)", ": Masa después de la corta para la variable N (densidad)"),
                "comentario 50"=c(": Stand after thinning for the variable G (basal area)", ": Masa después de la corta para la variable G (área basimétrica)"),
                "comentario 51"=c(": Stand after thinning for the variable V (volume)", ": Masa después de la corta para la variable V (volumen)"),
                "comentario 52"=c(": Stand after thinning for the variable dg (quadratic mean diameter)", ": Masa después de la corta para la variable dg (diámetro cuadrático medio)"),
                "comentario 53"=c(" Mortality, the mass in the mount which is dead."," Mortalidad, la masa en el monte que muere"),
                "comentario 54"=c(": Mortality for the variable N (density)",": Mortalidad para la variable N (densidad)"),
                "comentario 55"=c(": Mortality for the variable V (volume)",": Mortalidad para la variable V (volumen)"),
                "comentario 56"=c(": Mortality for the variable dg (quadratic mean diameter)",": Mortalidad para la variable dg (diámetro cuadrático medio)"),
                "comentario 57"=c("This is a visual representation of the evolution of some of the general variables for the data selected.","Esto es una representación visual de la evolución de algunas de las variables generales para los datos seleccionados."),
                "comentario 58"=c("This is a visual representation of the evolution of some of the general variables for the data selected. We represent the variables against 
                                       the dominant height.","Esto es una representación visual de la evolución de algunas de las variables generales para los datos seleccionados. Representamos las variables frente la altura dominante."),
                "comentario 59"=c("This is a visual representation of the evolution of general variables in the differents scenarios. By default, N is represented and all the scenarios are display.", 
                                  "Es una representación gráfica de la evolución de las variables generales en los difrerentes escenarios. Por defecto, N esta representado y todos los escenarios se muestran."),
                "comentario 60"=c("In this window it is represented the volume. The first graph only represent the trees that are on the mount. In the second one we have the variables taking into acount the thinning.",
                                  "En esta pestaña se representa el volumen. El primer gráfico representa solamente los árboles que están en el monte. En el segundo gráfico tenemos las variables teniendo en cuenta la corta."),
                "comentario 61"=c("This is a visual representation of the volume. By default, the total volume is represented and all the scenarios are display. If all the values of a variable are zero, it indicates that this variable isn't available for that data.",
                                  "Esto es una representación visual del volumen. Por defecto, se representa el volumen total y todos los escenarios. Si todos los valores de una variable son cero, indica que la variable no está disponible para esos datos."),
                "comentario 62"=c("This graph represent the volume taking into a count the thining.","Este gráfico representa el volumen teniendo en cuenta la corta."),
                "comentario 63"=c("In this window it is represented the biomass. The first graph only represent the trees that are on the mount. In the second one we have the variables after thinning.","En esta pestaña se representa la biomnasa. El primer gráfico solo representa los los árboles que están en elo monte. En el segundo tenemos la representación de las variables teniendo en cuenta la corta."),
                "comentario 64"=c("This is a visual representation of the biomass. By default, the total biomass is represented and all the scenarios are display. If all the values of a variable are zero, it indicates that this variable isn't available for that data.",
                                  "Es una representación gráfica de la biomasa. Por defecto, se representa la biomasa total y todos los escenarios. Si una variable tiene todos sus valores por cero, indica que es una variable que no está disponible para esos datos."),
                "comentario 65"=c("This graph represent the biomass taking into a count the thining.","Este gráfico representa el biomasa teniendo en cuenta la corta."))

#Seleccionar idioma
# 1=> ingles
# 2=> español
idioma<-2

dfArchivo$Age<-as.numeric(dfArchivo$Age)
dfArchivo$Ho<-as.numeric(dfArchivo$Ho)
dfArchivo$SBT_N<-as.numeric(dfArchivo$SBT_N)
dfArchivo$SBT_dg<-as.numeric(dfArchivo$SBT_dg)
dfArchivo$SBT_G<-as.numeric(dfArchivo$SBT_G)
dfArchivo$SBT_V<-as.numeric(dfArchivo$SBT_V)
dfArchivo$IdArchivo<-as.numeric(dfArchivo$IdArchivo)
dfArchivo$IdEscenario<-as.numeric(dfArchivo$IdEscenario)

escenarios<-unique(dfMedias$IdEscenario)
nombreArchivos<-unique(dfArchivo$IdNombre)

ui <- fluidPage(
  # Icono simanfor
  img(src = "https://raw.githubusercontent.com/simanfor/web/main/logos/simanfor.png", width = "250px", height = "100px"),
  
  # Titulo
  #tags$b(style = "font-size: 30px;", "Graphs for SIMANFOR"),
  h1(style = "font-size: 30px; margin-top: 10px;", lLanguage[[1]][idioma]),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      
      conditionalPanel(
        condition = "input.tabset == 'Plot vs Age' || input.tabset == 'Plot vs Ho'",
        selectInput("variable", lLanguage[[2]][idioma],
                    c("N" = "N",
                      "G" = "G",
                      "V" = "V",
                      "dg" = "dg"))
      ),
      conditionalPanel(
        condition = "input.tabset == 'Biomass vs Age'",
        selectInput("variableB", lLanguage[[3]][idioma],
                    c("WT" = "WT",
                      "WSW" = "WSW",
                      "WTHICKB" = "WTHICKB",
                      "WB2_7" = "WB2_7",
                      "WTHINB" = "WTHINB",
                      "WTBL" = "WTBL",
                      "WR" = "WR"))
      ),
      conditionalPanel(
        condition = "input.tabset == 'Biomass vs Age'",
        selectInput("variableB_all", lLanguage[[4]][idioma],
                    c("WT_all" = "WT_all",
                      "WSW_all" = "WSW_all",
                      "WTHICKB_all" = "WTHICKB_all",
                      "WB2_7_all" = "WB2_7_all",
                      "WTHINB_all" = "WTHINB_all",
                      "WTBL_all" = "WTBL_all",
                      "WR_all" = "WR_all"))
      ),
      conditionalPanel(
        condition = "input.tabset == 'General variables'",
        selectInput("variableG", lLanguage[[5]][idioma],
                    c("N" = "N",
                      "G" = "G",
                      "dg" = "dg",
                      "Ho" = "Ho",
                      "SDI" = "SDI",
                      "HartBecking__Simple_rows" = "HartBecking__Simple_rows"))
      ),
      conditionalPanel(
        condition = "input.tabset == 'Volume vs Age'",
        selectInput("variableV", lLanguage[[6]][idioma],
                    c("V" = "V",
                      "V_unwinding" = "V_unwinding",
                      "V_veneer" = "V_veneer",
                      "V_saw_big" = "V_saw_big",
                      "V_saw_small" = "V_saw_small",
                      "V_saw_canter" = "V_saw_canter",
                      "V_post" = "V_post",
                      "V_stake" = "V_stake",
                      "V_chips" = "V_chips"))
      ),
      
      conditionalPanel(
        condition = "input.tabset == 'Volume vs Age'",
        selectInput("variableV_all", lLanguage[[7]][idioma],
                    c("V_all" = "V_all",
                      "V_unwinding_all" = "V_unwinding_all",
                      "V_veneer_all" = "V_veneer_all",
                      "V_saw_big_all" = "V_saw_big_all",
                      "V_saw_small_all" = "V_saw_small_all",
                      "V_saw_canter_all" = "V_saw_canter_all",
                      "V_post_all" = "V_post_all",
                      "V_stake_all" = "V_stake_all",
                      "V_chips_all" = "V_chips_all"))
      ),
      
      
      conditionalPanel(
        condition = "input.tabset == 'Volume vs Age' || input.tabset == 'General variables' || input.tabset =='Biomass vs Age'",
        checkboxGroupInput("scenarios", lLanguage[[8]][idioma],
                           choices = escenarios,
                           selected = escenarios),
      ),
      conditionalPanel(
        condition = "input.tabset == 'Plot vs Ho' || input.tabset == 'Plot vs Age'|| input.tabset =='Summary'",
        selectInput("nombreArchivos",lLanguage[[9]][idioma],
                    choices = nombreArchivos,
                    selected = nombreArchivos[1])
      ),
      width = 4,  # Ajustar el ancho de la barra lateral si es necesario
      br(),
      hr()    
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      p(lLanguage[[10]][idioma]),
      p(lLanguage[[11]][idioma]),
      tags$ul(
        tags$b(lLanguage[[12]][idioma]),
        tags$li(tags$b("N"), lLanguage[[13]][idioma]),
        tags$li(tags$b("G"), lLanguage[[14]][idioma]),
        tags$li(tags$b("dg"), lLanguage[[15]][idioma]),
        tags$li(tags$b("Ho"), lLanguage[[16]][idioma]),
        tags$li(tags$b("SDI"), lLanguage[[17]][idioma]),
        tags$li(tags$b("HartBecking__Simple_rows"), lLanguage[[18]][idioma]),
      ),
      tags$ul(
        tags$div(style = "margin-bottom: 20px;"), 
        tags$b(lLanguage[[19]][idioma]),
        tags$li(tags$b("V"), lLanguage[[20]][idioma]),
        tags$li(tags$b("V_unwinding"), lLanguage[[21]][idioma]),
        tags$li(tags$b("V_veneer"), lLanguage[[22]][idioma]),
        tags$li(tags$b("V_saw_big"), lLanguage[[23]][idioma]),
        tags$li(tags$b("V_saw_small"), lLanguage[[24]][idioma]),
        tags$li(tags$b("V_saw_canterl"), lLanguage[[25]][idioma]),
        tags$li(tags$b("V_post"), lLanguage[[26]][idioma]),
        tags$li(tags$b("V_stake"), lLanguage[[27]][idioma]),
        tags$li(tags$b("V_chips"), lLanguage[[28]][idioma]),
      ),
      tags$ul(
        tags$div(style = "margin-bottom: 20px;"), 
        tags$b(lLanguage[[29]][idioma]),
        tags$li(tags$b("WT"), lLanguage[[30]][idioma]),
        tags$li(tags$b("WSW"), lLanguage[[31]][idioma]),
        tags$li(tags$b("WTHICKB"), lLanguage[[32]][idioma]),
        tags$li(tags$b("WB2_7"), lLanguage[[33]][idioma]),
        tags$li(tags$b("WTHINB"), lLanguage[[34]][idioma]),
        tags$li(tags$b("WTBL"), lLanguage[[35]][idioma]),
        tags$li(tags$b("WR"), lLanguage[[36]][idioma])
      ),
      
      # Output: Histogram ----
      tabsetPanel(
        id = "tabset",
        type = "tabs",
        tabPanel("Summary",helpText(lLanguage[[37]][idioma]),
                 p(lLanguage[[38]][idioma]),
                 tags$ul(
                   tags$div(style = "margin-bottom: 20px;"),
                   tags$b("SBT :"), lLanguage[[39]][idioma],
                   tags$li(tags$b("SBT_N"), lLanguage[[40]][idioma]),
                   tags$li(tags$b("SBT_G"), lLanguage[[41]][idioma]),
                   tags$li(tags$b("SBT_V"), lLanguage[[42]][idioma]),
                   tags$li(tags$b("SBT_dg"),lLanguage[[43]][idioma])
                 ),
                 tags$ul(
                   tags$div(style = "margin-bottom: 20px;"),
                   tags$b("T :"), lLanguage[[44]][idioma],
                   tags$li(tags$b("T_N"), lLanguage[[45]][idioma]),
                   tags$li(tags$b("T_V"), lLanguage[[46]][idioma]),
                   tags$li(tags$b("T_dg"),lLanguage[[47]][idioma])
                 ),
                 tags$ul(
                   tags$div(style = "margin-bottom: 20px;"),
                   tags$b("SAT :"), lLanguage[[48]][idioma],
                   tags$li(tags$b("SAT_N"), lLanguage[[49]][idioma]),
                   tags$li(tags$b("SAT_G"), lLanguage[[50]][idioma]),
                   tags$li(tags$b("SAT_V"), lLanguage[[51]][idioma]),
                   tags$li(tags$b("SAT_dg"),lLanguage[[52]][idioma])
                 ),
                 tags$ul(
                   tags$div(style = "margin-bottom: 20px;"),
                   tags$b("M :"), lLanguage[[53]][idioma],
                   tags$li(tags$b("M_N"), lLanguage[[54]][idioma]),
                   tags$li(tags$b("M_V"), lLanguage[[55]][idioma]),
                   tags$li(tags$b("M_dg"),lLanguage[[56]][idioma])
                 ),
                 verbatimTextOutput("summary"),
                 verbatimTextOutput("summaryCompleto")),
        tabPanel("Plot vs Age",helpText(lLanguage[[57]][idioma]),
                 plotlyOutput(outputId = "grafico")),
        tabPanel("Plot vs Ho",helpText(lLanguage[[58]][idioma]), 
                 plotlyOutput(outputId = "grafico2")),
        tabPanel("General variables",helpText(lLanguage[[59]][idioma]),
                 plotlyOutput(outputId = "graficoGeneral")),
        tabPanel("Volume vs Age",p(lLanguage[[60]][idioma]),
                 helpText(lLanguage[[61]][idioma]),
                 plotlyOutput(outputId = "graficoVolumen"),helpText(lLanguage[[62]][idioma]),plotlyOutput(outputId = "graficoVolumenAll")),
        tabPanel("Biomass vs Age",p(lLanguage[[63]][idioma]),
                 helpText(lLanguage[[64]][idioma]),
                 plotlyOutput(outputId = "graficoBiomasa"),helpText(lLanguage[[65]][idioma]), plotlyOutput(outputId = "graficoBiomasaAll"))
        
      )
    )
  )
)


# Define server logic required to draw a histogram ----
server <- function(input, output,session) {
  
  output$graficoBiomasa <- renderPlotly({
    
    selected_scenarios <- input$scenarios
    dfFiltered <- dfMedias[dfMedias$IdEscenario %in% selected_scenarios, ]
    
    gb<-ggplot(dfFiltered, aes(x = T, y = eval(parse(text = input$variableB)), color = as.factor(IdEscenario), group = IdEscenario)) +
      geom_point() +
      geom_line() +
      labs(title = bquote("Biomass vs Age"),
           subtitle = input$variableB,
           x = "Age",
           y = paste0("Value ", input$variableB),
           color = "Scenario") +
      theme_bw()+
      theme(plot.title = element_text(size = 20))+
      theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
            axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
    ggplotly(gb,tooltip = c("x","y"))
  })
  
  output$graficoBiomasaAll <- renderPlotly({
    
    selected_scenarios <- input$scenarios
    dfFiltered <- dfMedias[dfMedias$IdEscenario %in% selected_scenarios, ]
    
    gb<-ggplot(dfFiltered, aes(x = T, y = eval(parse(text = input$variableB_all)), color = as.factor(IdEscenario), group = IdEscenario)) +
      geom_point() +
      geom_line() +
      labs(title = bquote("Biomass vs Age with thinning"),
           subtitle = input$variableB_all,
           x = "Age",
           y = paste0("Value ", input$variableB_all),
           color = "Scenario") +
      theme_bw()+
      theme(plot.title = element_text(size = 20))+
      theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
            axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
    ggplotly(gb,tooltip = c("x","y"))
  })
  
  output$graficoGeneral <- renderPlotly({
    
    selected_scenarios <- input$scenarios
    dfFiltered <- dfMedias[dfMedias$IdEscenario %in% selected_scenarios, ]
    
    gg<-ggplot(dfFiltered, aes(x = T, y = eval(parse(text = input$variableG)), color = as.factor(IdEscenario), group = IdEscenario)) +
      geom_point() +
      geom_line() +
      labs(title = bquote("General variables vs Age"),
           subtitle = input$variableG,
           x = "Age",
           y = paste0("Value ", input$variableG),
           color = "Scenario") +
      theme_bw()+
      theme(plot.title = element_text(size = 20))+
      theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
            axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
    ggplotly(gg,tooltip = c("x","y"))
  })
  
  
  output$graficoVolumen <- renderPlotly({
    
    selected_scenarios <- input$scenarios
    dfFiltered <- dfMedias[dfMedias$IdEscenario %in% selected_scenarios, ]
    
    gv<-ggplot(dfFiltered, aes(x = T, y = eval(parse(text = input$variableV)), color = as.factor(IdEscenario), group = IdEscenario)) +
      geom_point() +
      geom_line() +
      labs(title =bquote("Volume vs Age"),
           subtitle = input$variableV,
           x = "Age",
           y = paste0("Value ", input$variableV),
           color = "Scenario") +
      theme_bw()+
      theme(plot.title = element_text(size = 20))+
      theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
            axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
    ggplotly(gv,toltip = c("x","y"))
  })
  
  output$graficoVolumenAll <- renderPlotly({
    
    selected_scenarios <- input$scenarios
    dfFiltered <- dfMedias[dfMedias$IdEscenario %in% selected_scenarios, ]
    
    gv<-ggplot(dfFiltered, aes(x = T, y = eval(parse(text = input$variableV_all)), color = as.factor(IdEscenario), group = IdEscenario)) +
      geom_point() +
      geom_line() +
      labs(title =bquote("Volume vs Age with thinning"),
           subtitle = input$variableV_all,
           x = "Age",
           y = paste0("Value ", input$variableV_all),
           color = "Scenario") +
      theme_bw()+
      theme(plot.title = element_text(size = 20))+
      theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
            axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
    ggplotly(gv,tooltip = c("x","y"))
  })
  
  output$summary <- renderPrint({
    selected_file <- input$nombreArchivos
    dfFilteredFile <- dfArchivo[dfArchivo$IdNombre %in% selected_file, ]
    summary(dfFilteredFile)
  })
  
  output$summaryCompleto<- renderPrint({
    summary(dfMedias)
  })
  
  output$grafico <- renderPlotly({
    
    selected_file <- input$nombreArchivos
    dfFilteredFile <- dfArchivo[dfArchivo$IdNombre %in% selected_file, 1:17]
    
    data_filtered <- dfFilteredFile %>%
      filter(!is.na(eval(parse(text=paste0("SBT_",input$variable)))))
    
    if(input$variable=="G"){
      g1<-ggplot(data_filtered, aes(x = Age)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        labs(x = "Age",
             y = "Valor",
             title = paste0("Variable ",input$variable," in the different stages")) +
        scale_color_manual(name = "Proceso", 
                           values = c("Stand Before Thinning" = "purple", "Thinning" = "lightgreen"),
                           labels = c("Stand Before Thinning", "Thinning")) +
        theme_minimal()+
        theme(plot.title = element_text(size = 20))+
        theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
              axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
      ggplotly(g1)
    }else{
      g2<-ggplot(data_filtered, aes(x = Age)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        geom_point(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "Thinning")) +
        geom_line(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "Thinning")) +
        labs(x = "Age", y = "Value", title = paste0("Variable ",input$variable," in the different stages")) +
        scale_color_manual(name = "Proceso", 
                           values = c("Stand Before Thinning" = "purple", "Thinning" = "lightgreen"),
                           labels = c("Stand Before Thinning", "Thinning")) +
        theme_minimal()+
        theme(plot.title = element_text(size = 20))+
        theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
              axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
      ggplotly(g2)
    }
    
    
  })
  
  
  output$grafico2 <- renderPlotly({
    
    selected_file <- input$nombreArchivos
    dfFilteredFile <- dfArchivo[dfArchivo$IdNombre %in% selected_file, 2:17]
    
    data_filtered <- dfFilteredFile %>%
      filter(!is.na(eval(parse(text=paste0("SBT_",input$variable)))))
    
    if(input$variable=="G"){
      g3<-ggplot(data_filtered, aes(x = Ho)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        labs(x = "Ho", y = "Value", title = paste0("Variable ",input$variable," vs dominant height ")) +
        scale_color_manual(name = "Proceso", 
                           values = c("Stand Before Thinning" = "lightblue", "T" = "red"),
                           labels = c("Stand Before Thinning", "Thinning")) +
        theme_minimal()+
        theme(plot.title = element_text(size = 20))+
        theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
              axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes+
      ggplotly(g3)
    }else{
      g4<-ggplot(data_filtered, aes(x = Ho)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "Stand Before Thinning")) +
        geom_point(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "Thinning")) +
        geom_line(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "Thinning")) +
        labs(x = "Ho", y = "Value", title = paste0("Variable ",input$variable," vs dominant height")) +
        scale_color_manual(name = "Proceso", 
                           values = c("Stand Before Thinning" = "lightblue", "Thinning" = "red"),
                           labels = c("Stand Before Thinning", "Thinning")) +
        theme_minimal()+
        theme(plot.title = element_text(size = 20))+
        theme(axis.text = element_text(size = 14),  # Ajusta el tamaño del texto de los ejes
              axis.title = element_text(size = 16))  # Ajusta el tamaño del título de los ejes
      ggplotly(g4)
    }
    
  })
  
}

# Create Shiny app ----
shinyApp(ui = ui, server = server)
