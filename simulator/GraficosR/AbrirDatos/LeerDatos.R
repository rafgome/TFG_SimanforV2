rm(list=ls())

library(utils)
library(readxl)
library(plyr)
library(dplyr)
library(ggplot2)
library(tidyverse)

setwd("C:/Users/Irene/Documents/simulator/GraficosR/AbrirDatos")
listaZip<-dir(pattern = "*.zip")

## Descomrpimimos los zips en su carpeta correspondiente
listaEscenarios<-c()
for(i in 1:length(listaZip)){
  listaEscenarios<-c(listaEscenarios,paste0("Escenario",i))
  unzip(zipfile = listaZip[i],exdir=paste0("Escenario",i))
}

datos<-c()
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
  }
}

## Transformamos a df que es mas sencillo su manejo
df<-as.data.frame(datos)

## Añadimos un identificador
df$ID_Escenario_Archivo<-with(df,paste0(IdEscenario,".",IdArchivo))

## Eliminamos las filas innesarias
df <- df[!df$Action == "Initial load", ]

