################################################################################
#
#                  Preparación datos para shiny 
#                         Irene Arroyo
#
################################################################################
library(utils)
library(readxl)
library(plyr)
library(dplyr)
library(ggplot2)
library(tidyverse)

rm(list=ls())

setwd("C:/Users/Irene/Documents/simulator/GraficosR/AbrirDatos")
listaZip<-dir(pattern = "*.zip")

## Descomrpimimos los zips en su carpeta correspondiente
listaEscenarios<-c()
for(i in 1:length(listaZip)){
  listaEscenarios<-c(listaEscenarios,paste0("Escenario",i))
  unzip(zipfile = listaZip[i],exdir=paste0("Escenario",i))
}

datos<-c()
datosArchivo<-c()
## Leemos los archivos de cada uno de los escenarios para juntarles en 1
idEscenario<-0
for(i in 1:length(listaEscenarios)){
  idEscenario<-idEscenario+1
  dirEscenario<-paste0(getwd(),"/",listaEscenarios[i])
  #setwd(dirEscenario)
  archivos<-list.files(dirEscenario,pattern = "xlsx")
  
  for(i in 1:length(archivos)){
    plots<-read_excel(paste0(dirEscenario,"/",archivos[i]),sheet = "Plots")
    plots$IdNombre<-archivos[i]
    plots$IdArchivo<-i
    plots$IdEscenario<-idEscenario
    datos<-rbind(datos,plots)
    
    plotsArchivo<-read.xlsx(paste0(dirEscenario,"/",archivos[i]),startRow = 7,sheet="Summary" )
    names(plotsArchivo)<-c("Age","Ho","SBT_N","SBT_dg","SBT_G","SBT_V","T_N","T_dg","T_V","SAT_N","SAT_dg","SAT_G","SAT_V","M_N","M_dg","M_V")
    plotsArchivo$IdNombre<-archivos[i]
    plotsArchivo$IdArchivo<-i
    plotsArchivo$IdEscenario<-idEscenario
    datosArchivo<-rbind(datosArchivo,plotsArchivo)
  }
}

## Transformamos a df que es mas sencillo su manejo
df<-as.data.frame(datos)

## Añadimos un identificador
df$ID_Escenario_Archivo<-with(df,paste0(IdEscenario,".",IdArchivo))

## Eliminamos las filas innesarias
df <- df[!df$Action == "Initial load", ]

write.csv(df,"datosCompletos.csv")
write.csv(datosArchivo,"datosArchivo.csv")
archivos_SBT_N<-data.frame(cbind(datosArchivo$Age,datosArchivo$Ho,datosArchivo$SAT_N,datosArchivo$IdNombre,datosArchivo$IdArchivo,datosArchivo$IdEscenario))
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
datosCorta<-datosCorta[order(datosCorta$IdEscenario,datosCorta$IdArchivo,as.numeric(datosCorta$Age)), ]

write.csv(datosCorta,"datosCorta.csv")



## Creamos un data frame con el resumen de variables que nos interesan
df_medias<- ddply(df, c('IdEscenario', 'T'), summarise, 
                          # Variables generales                       
                          N=mean(N, na.rm = TRUE),                  
                          dg=mean(dg, na.rm = TRUE),
                          Ho=mean(Ho, na.rm = TRUE),  
                          V=mean(V, na.rm = TRUE), 
                          WT=mean(WT, na.rm = TRUE), 
                          G=mean(G, na.rm = TRUE),
                          # Biomasa
                          WSW=mean(WSW, na.rm = TRUE),
                          WTHICKB=mean(WTHICKB, na.rm = TRUE),
                          WB2_7=mean(WB2_7, na.rm = TRUE),
                          WTHINB=mean(WTHINB, na.rm = TRUE),
                          WTBL=mean(WTBL, na.rm = TRUE),
                          WR=mean(WR, na.rm = TRUE)
)

################################################################################
              ## Calcular las diferencias entre cada escenario
################################################################################
diferencias <- df %>%
  group_by(IdNombre, Scenario_file_name) %>%
  mutate(V_diff = V - lag(V),
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

df_diferencias<-as.data.frame(diferencias)

################################################################################
                        ## Cálculos acumulados
################################################################################
## Vamos a calcular el total acumulado en cada uno de los escenarios para cada
## uno de los plots
df_acum<-tibble()

## COMPROBAR QUE ESTA LA VARIABLE EN EL DATA FRAME!!!!!

##Seleccionamos el escenario correspondiente
for(i in unique(df_diferencias$Scenario_file_name)){
  ##Seleccionamos los datos que lo cumplen
  aux<-df_diferencias[df_diferencias$Scenario_file_name==i,]
  ##Seleccionamos el plot
  for(j in unique(aux$IdNombre)){
    ##Seleccionamos los datos que lo cumplen
    aux2<-aux[aux$IdNombre==j,]
    ## Valores iniciales de las variables que se van a crear
    all_V <- all_WSW <- all_WTHICKB <- all_WB2_7 <- all_WTHINB <- all_WTBL <- all_WR <- all_WT <- all_V_unwinding <- all_V_veneer <- all_V_saw_big <- all_V_saw_small <- all_V_saw_canter <- all_V_post <- all_V_stake <- all_V_chips <- 0
    ## para cada fila
    for(k in 1:nrow(aux2)){
      # seleccionamos los datos
      new_row <- aux2[k, ]
      
      # si es la primera, tomamos el valor inicial
      if(k == 1){
  
        # valores inciales
        all_V <- new_row$V
        all_WSW <- new_row$WSW
        all_WTHICKB <- new_row$WTHICKB
        all_WB2_7 <- new_row$WB2_7
        all_WTHINB <- new_row$WTHINB
        all_WTBL <- new_row$WTBL
        all_WR <- new_row$WR
        all_WT <- new_row$WT
        all_V_unwinding <- new_row$V_unwinding
        all_V_veneer <- new_row$V_veneer
        all_V_saw_big <- new_row$V_saw_big
        all_V_saw_small <- new_row$V_saw_small
        all_V_saw_canter <- new_row$V_saw_canter
        all_V_post <- new_row$V_post
        all_V_stake <- new_row$V_stake
        all_V_chips <- new_row$V_chips
        
        # añadimos el valor
        new_row$V_all <- all_V
        new_row$WSW_all <- all_WSW
        new_row$WTHICKB_all <- all_WTHICKB
        new_row$WB2_7_all <- all_WB2_7
        new_row$WTHINB_all <- all_WTHINB
        new_row$WTBL_all <- all_WTBL
        new_row$WR_all <- all_WR
        new_row$WT_all <- all_WT
        new_row$V_unwinding_all <- all_V_unwinding
        new_row$V_veneer_all <- all_V_veneer
        new_row$V_saw_big_all <- all_V_saw_big
        new_row$V_saw_small_all <- all_V_saw_small
        new_row$V_saw_canter_all <- all_V_saw_canter
        new_row$V_post_all <- all_V_post
        new_row$V_stake_all <- all_V_stake
        new_row$V_chips_all <- all_V_chips
        
        # añadir la diferencia
      }else{
        
        # sumar el incremento 
        all_V <- all_V + abs(new_row$V_diff)
        all_WSW <- all_WSW + abs(new_row$WSW_diff)
        all_WTHICKB <- all_WTHICKB + abs(new_row$WTHICKB_diff)
        all_WB2_7 <- all_WB2_7 + abs(new_row$WB2_7_diff)
        all_WTHINB <- all_WTHINB + abs(new_row$WTHINB_diff)
        all_WTBL <- all_WTBL + abs(new_row$WTBL_diff)
        all_WR <- all_WR + abs(new_row$WR_diff)
        all_WT <- all_WT + abs(new_row$WT_diff)
        all_V_unwinding <- all_V_unwinding + abs(new_row$V_unwinding_diff) 
        all_V_veneer <- all_V_veneer + abs(new_row$V_veneer_diff)
        all_V_saw_big <- all_V_saw_big + abs(new_row$V_saw_big_diff)
        all_V_saw_small <- all_V_saw_small + abs(new_row$V_saw_small_diff)
        all_V_saw_canter <- all_V_saw_canter + abs(new_row$V_saw_canter_diff)
        all_V_post <- all_V_post + abs(new_row$V_post_diff)
        all_V_stake <- all_V_stake + abs(new_row$V_stake_diff)
        all_V_chips <- all_V_chips + abs(new_row$V_chips_diff)
        
        
        # add value to the row
        new_row$V_all <- all_V
        new_row$WSW_all <- all_WSW
        new_row$WTHICKB_all <- all_WTHICKB
        new_row$WB2_7_all <- all_WB2_7
        new_row$WTHINB_all <- all_WTHINB
        new_row$WTBL_all <- all_WTBL
        new_row$WR_all <- all_WR
        new_row$WT_all <- all_WT
        new_row$V_unwinding_all <- all_V_unwinding
        new_row$V_veneer_all <- all_V_veneer
        new_row$V_saw_big_all <- all_V_saw_big
        new_row$V_saw_small_all <- all_V_saw_small
        new_row$V_saw_canter_all <- all_V_saw_canter
        new_row$V_post_all <- all_V_post
        new_row$V_stake_all <- all_V_stake
        new_row$V_chips_all <- all_V_chips
      }

      # add new row to a new df
      #df_acum <- bind_rows(df_acum, new_row)
      df_acum <- rbind(df_acum, new_row)
      
    } # row
  } # plot
} # scenario

df_acum<-as.data.frame(df_acum)

# round ages
#df_acum$T <- round(df_acum$T, 5) 

# get scenario code
df_acum$n_scnr <- substr(df_acum$Scenario_file_name, 17, 19)

# delete empty rows
df_acum <- df_acum[!is.na(df_acum$n_scnr), ]


acumulado <- df %>%
  group_by(Scenario_file_name,IdNombre) %>%
  mutate(V_all = cumsum(V),
         WSW_all= cumsum(WSW),
         WTHICKB_all= cumsum(WTHICKB),
         WB2_7_all= cumsum(WB2_7),
         WTHINB_all= cumsum(WTHINB),
         WTBL_all= cumsum(WTBL),
         WR_all= cumsum(WR),
         WT_all= cumsum(WT),
  )

################################################################################
#                         Cálculos medios
################################################################################
# mean values by scenario and year
df_medias_evolucion<- ddply(df_acum, c('IdEscenario', 'T'), summarise, 
                         
                         # general variables                         
                         N = mean(N, na.rm = TRUE),                  
                         dg = mean(dg, na.rm = TRUE),
                         Ho = mean(Ho, na.rm = TRUE),  
                         V = mean(V, na.rm = TRUE), 
                         WT = mean(WT, na.rm = TRUE), 
                         G = mean(G, na.rm = TRUE),
                         SDI = mean(SDI, na.rm=TRUE),
                         HartBecking__Simple_rows = mean(HartBecking__Simple_rows, na.rm=TRUE),
                         
                         # volume classification 
                         V_unwinding = mean(V_unwinding, na.rm=TRUE),
                         V_veneer = mean(V_veneer, na.rm=TRUE),
                         V_saw_big = mean(V_saw_big, na.rm=TRUE),
                         V_saw_small = mean(V_saw_small, na.rm=TRUE),
                         V_saw_canter = mean(V_saw_canter, na.rm=TRUE),
                         V_post = mean(V_post, na.rm=TRUE),
                         V_stake = mean(V_stake, na.rm=TRUE),
                         V_chips = mean(V_chips, na.rm=TRUE),
                         
                         # biomass classification - stand variables
                         WSW = mean(WSW, na.rm = TRUE),
                         WTHICKB = mean(WTHICKB, na.rm = TRUE),
                         WB2_7 = mean(WB2_7, na.rm = TRUE),
                         WTHINB = mean(WTHINB, na.rm = TRUE),
                         WTBL = mean(WTBL, na.rm = TRUE),
                         WR = mean(WR, na.rm = TRUE),
                         
                         
                         # all accumulated stand variables
                         WSW_all = mean(WSW_all, na.rm = TRUE),
                         WTHICKB_all = mean(WTHICKB_all, na.rm = TRUE),
                         WB2_7_all = mean(WB2_7_all, na.rm = TRUE),
                         WTHINB_all = mean(WTHINB_all, na.rm = TRUE),
                         WTBL_all = mean(WTBL_all, na.rm = TRUE),
                         WR_all = mean(WR_all, na.rm = TRUE),
                         WT_all = mean(WT_all, na.rm = TRUE),
                         V_all = mean(V_all, na.rm = TRUE),
                         V_unwinding_all = mean(V_unwinding_all, na.rm=TRUE),
                         V_veneer_all = mean(V_veneer_all, na.rm=TRUE),
                         V_saw_big_all = mean(V_saw_big_all, na.rm=TRUE),
                         V_saw_small_all = mean(V_saw_small_all, na.rm=TRUE),
                         V_saw_canter_all = mean(V_saw_canter_all, na.rm=TRUE),
                         V_post_all = mean(V_post_all, na.rm=TRUE),
                         V_stake_all = mean(V_stake_all, na.rm=TRUE),
                         V_chips_all = mean(V_chips_all, na.rm=TRUE),
)

write.csv(df_medias_evolucion,"datosMediasEvolucion.csv")
