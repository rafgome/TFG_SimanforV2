setHook("rstudio.sessionInit", function(newSession) {
# .First <- function() {

  if (newSession) {
    message("Welcome to RStudio ", rstudioapi::getVersion());
    
    # Package installation
    # install.packages("plyr")
    # install.packages("openxlsx")
    # install.packages("plotly")
    
    # if (rstudioapi::isAvailable()) {
    #   
    #   # determine more information via
    #   info <- rstudioapi::versionInfo()
    #   # check for desktop mode
    #   info$mode == "desktop"
    #   # check for server mode
    #   info$mode == "server"
    #   # check the version of RStudio in use
    #   info$version >= "1.4"
    #   print(info);
    # }
    
    # Show shiny app in a new tab
    if (
      # Make sure that {rstudioapi} is available
      requireNamespace("rstudioapi", quietly = TRUE) &&
      # Returns TRUE if RStudio is running
      rstudioapi::hasFun("viewer")
    ) {
      options(shiny.launch.browser = .rs.invokeShinyWindowExternal)
    }

    print("Loading the file 'Shiny_completo.R'... / Cargando el fichero 'Shiny_completo.R'...")
    source("~/simulator/RShiny/Shiny_completo.R")
    print("'Shiny_completo.R' loaded successfully. / 'Shiny_completo.R' cargado exitosamente.")
    
    # print("Inicializando la aplicación Shiny...")
    # shinyApp(ui = ui, server = server)
    # print("Aplicación Shiny inicializada exitosamente...")
    
    print("[English] To view the results using the graphical Shiny app, type 'shinyApp(ui, server)' into this console. Then, select the file whose name matches the zip file to visualize its results. To change the app language to Spanish, access the file '~/simulator/RShiny/Shiny_completo.R' and modify the value of the variable 'idioma' to 2.")
    
    print("[Español] Para ver los resultados con la aplicación Shiny gráfica, escribir 'shinyApp(ui, server)' en esta consola. Después, seleccionar el archivo cuyo nombre coincide con el fichero zip para visualizar sus resultados. Para cambiar el idioma de la aplicación a inglés, acceder al archivo '~/simulator/RShiny/Shiny_completo.R' y modificar el valor de la variable 'idioma' a 1.")

  }
}, action = "append")
