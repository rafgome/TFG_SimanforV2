library(shiny)
library(readxl)
library(openxlsx)
library(ggplot2)
library(plotly)

rm(list=ls())

df<-read.xlsx("C:/Users/Irene/Documents/COMFOR.NFI2/Shiny/PRAD_GAL__Output_Plot_1.0.xlsx",startRow = 7,sheet="Resumen")

names(df)<-c("Age","Ho","SBT_N","SBT_dg","SBT_G","SBT_V","T_N","T_dg","T_V","SAT_N","SAT_dg","SAT_G","SAT_V","M_N","M_dg","M_V")

# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # Titulo
  titlePanel("Graficos SIMANFOR"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      selectInput("variable","Variable:",
                  c("N"="N",
                    "G"="G",
                    "V"="V",
                    "dg"="dg"))
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: Histogram ----
      plotOutput(outputId = "grafico"),
      plotOutput(outputId = "grafico2")
      
    )
  )
)

# Define server logic required to draw a histogram ----
server <- function(input, output,session) {
  
  output$grafico <- renderPlot({
    
    if(input$variable=="G"){
      ggplot(df, aes(x = Age)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_point(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        geom_line(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        labs(x = "Age", y = "Valor", title = paste0("Variable ",input$variable," en los distintos escenarios")) +
        scale_color_manual(name = "Proceso", 
                           values = c("SBT" = "lightblue", "T" = "lightgreen", "SAT" = "red"),
                           labels = c("SBT", "T", "SAT")) +
        theme_minimal()
    }else{
      ggplot(df, aes(x = Age)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_point(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "T")) +
        geom_line(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "T")) +
        geom_point(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        geom_line(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        labs(x = "Age", y = "Valor", title = paste0("Variable ",input$variable," en los distintos escenarios")) +
        scale_color_manual(name = "Proceso", 
                           values = c("SBT" = "lightblue", "T" = "lightgreen", "SAT" = "red"),
                           labels = c("SBT", "T", "SAT")) +
        theme_minimal()
    }

    
  })
  
  
  output$grafico2 <- renderPlot({
    
    if(input$variable=="G"){
      ggplot(df, aes(x = Ho)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_point(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        geom_line(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        labs(x = "Ho", y = "Valor", title = paste0("Variable ",input$variable," frente altura dominate")) +
        scale_color_manual(name = "Proceso", 
                           values = c("SBT" = "lightblue", "T" = "lightgreen", "SAT" = "red"),
                           labels = c("SBT", "T", "SAT")) +
        theme_minimal()
    }else{
      ggplot(df, aes(x = Ho)) +
        geom_point(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_line(aes(y = eval(parse(text=paste0("SBT_",input$variable))), color = "SBT")) +
        geom_point(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "T")) +
        geom_line(aes(y = eval(parse(text=paste0("T_",input$variable))), color = "T")) +
        geom_point(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        geom_line(aes(y = eval(parse(text=paste0("SAT_",input$variable))), color = "SAT")) +
        labs(x = "Ho", y = "Valor", title = paste0("Variable ",input$variable," frente altura dominante")) +
        scale_color_manual(name = "Proceso", 
                           values = c("SBT" = "lightblue", "T" = "lightgreen", "SAT" = "red"),
                           labels = c("SBT", "T", "SAT")) +
        theme_minimal()
    }
    
    
  })
  
}

# Create Shiny app ----
shinyApp(ui = ui, server = server)
