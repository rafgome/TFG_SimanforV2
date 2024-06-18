################################################################################
#
#                     Shiny app for simanfor
#                     Irene Arroyo Hernantes
#
################################################################################

library(dygraphs)
library(shiny)
library(readxl)
library(openxlsx)
library(ggplot2)
library(plotly)

rm(list=ls())

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

setwd("C:/Users/Irene/Documents/simulator/GraficosR/AbrirDatos")
dfMedias<-read.csv("datosMediasEvolucion.csv")
dfMedias<-dfMedias[,-1]
dfArchivo<-read.csv("datosCorta.csv")
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
    dfFilteredFile <- dfArchivo[dfArchivo$IdNombre %in% selected_file, 2:17]
    
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