db = connect( 'mongodb://localhost/simanfor_min' );
db.dropDatabase();

db.user.insertMany( [
   { 
      "_id" : ObjectId("6673faf57a8035fd9a8930a8"), 
      "user" : "admin", 
      "password" : "$2b$10$3Cm0D8.wBpDo91hAfFAwU.G3n5.yNI7.LmkOW3n/fw7wM6rPfJqBC", 
      "role" : "admin", 
      "name" : "Admin", 
      "surname" : "Istrator", 
      "center" : "Centro", 
      "department" : "Dept", 
      "email" : "admin@istrator.com", 
      "phone" : "123456123" 
   },
   { 
      "_id" : ObjectId("6673fb257a8035a6158930a9"), 
      "user" : "basic", 
      "password" : "$2b$10$0OqqvkbaChlB3.ucS9lgr.mEl2k4YKKJ82ukpgEBIZECJ2MAqLqYa", 
      "role" : "basic", 
      "name" : "Basic", 
      "surname" : "User", 
      "center" : "Centro", 
      "department" : "Dept", 
      "email" : "basic@user.com", 
      "phone" : "987654321" 
   }
] );

db.model.insertMany( [
   { 
      "_id" : ObjectId("608581378bd5b8b2624c56f3"), 
      "name" : "Psylvestris__sisc__v01", 
      "description" : "IBERO-PS , modelo de crecimiento de árbol individual para Pinus sylvestris en el Sistema Central y Sistema Ibérico", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Psylvestris_sisc_ES.pdf", 
      "status" : "stable", 
      "modelPath" : "models.trees.Psylvestris__sisc__v01", 
      "modelClass" : "PinusSylvestrisSISC", 
      "creatorId" : "5f7d6b48aa4cea7998c61a6b", 
      "operation" : "EXECUTION", 
      "specie" : "Pinus sylvestris", 
      "applicationArea" : "Sistema Ibérico y Sistema Central (Ávila, Burgos, Segovia y Soria)", 
      "executionPeriod" : "5", 
      "operatingDimensions" : "-" 
   },
   { 
      "_id" : ObjectId("6209673a09d76f93c74442c0"), 
      "name" : "Phalepensis__aragon__v01", 
      "description" : "Modelo de crecimiento de árbol individual para Pinus halepensis de Aragón", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Phalepensis_ar_ES.pdf", 
      "status" : "stable", 
      "modelPath" : "models.trees.Phalepensis__aragon__v01", 
      "modelClass" : "PinusHalepensisAragon", 
      "creatorId" : "5f7d6b48aa4cea7998c61a6b", 
      "operation" : "EXECUTION", 
      "specie" : "Pinus halepensis", 
      "applicationArea" : "Aragón (Zaragoza, Huesca y Teruel)", 
      "executionPeriod" : "10", 
      "operatingDimensions" : "-" 
   },
   { 
      "_id" : ObjectId("62711c6be1a38adeda0fed13"), 
      "name" : "Phalepensis__cat_ar__v01", 
      "description" : "Modelo de crecimiento de árbol individual para Pinus halepensis de Cataluña y Aragón", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Phalepensis_cat_ar_ES.pdf", 
      "status" : "stable", 
      "modelPath" : "models.trees.Phalepensis__cat_ar__v01", 
      "modelClass" : "PinusHalepensisCataluña", 
      "creatorId" : "6009906619372c4b7b06b3f8", 
      "operation" : "EXECUTION", 
      "specie" : "Pinus halepensis", 
      "applicationArea" : "Valle medio del Ebro (Aragón) y Cataluña (Huesca, Zaragoza, Girona, Barcelona, Lleida y Tarragona)", 
      "executionPeriod" : "10", 
      "operatingDimensions" : "-" 
   },
   // { 
   //    "_id" : ObjectId("6271440fe1a38a8a480fed1c"), 
   //    "name" : "Psylvestris__cat_nat__v01", 
   //    "description" : "Modelo de crecimiento de árbol individual para Pinus sylvestris en masas naturales de Cataluña", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Psylvestris_cat_nat_ES.pdf", 
   //    "status" : "stable", 
   //    "modelPath" : "models.trees.Psylvestris__cat_nat__v01", 
   //    "modelClass" : "PinusSylvestrisCataluña", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Pinus sylvestris", 
   //    "applicationArea" : "Cataluña (Gerona, Lleida, Barcelona y Tarragona)", 
   //    "executionPeriod" : "5", 
   //    "operatingDimensions" : "-" 
   // },
   // { 
   //    "_id" : ObjectId("62714440e1a38a16010fed1d"), 
   //    "name" : "Psylvestris__cat_plant__v01", 
   //    "description" : "Modelo de crecimiento de árbol individual para Pinus sylvestris en repoblaciones forestales de Cataluña", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Psylvestris_cat_plant_ES.pdf", 
   //    "status" : "stable", 
   //    "modelPath" : "models.trees.Psylvestris__cat_plant__v01", 
   //    "modelClass" : "PinusSylvestrisCataluña", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Pinus sylvestris", 
   //    "applicationArea" : "Cataluña (Gerona, Lleida, Barcelona y Tarragona)", 
   //    "executionPeriod" : "5", 
   //    "operatingDimensions" : "-" 
   // },
   { 
      "_id" : ObjectId("627144a8e1a38a623e0fed1e"), 
      "name" : "Psylvestris__sisc__v02", 
      "description" : "IBERO-PS , modelo de crecimiento de árbol individual para Pinus sylvestris en el Sistema Central y Sistema Ibérico, versión 2", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Psylvestris_sisc_v02_ES.pdf", 
      "status" : "stable", 
      "modelPath" : "models.trees.Psylvestris__sisc__v02", 
      "modelClass" : "PinusSylvestrisSISC", 
      "creatorId" : "6009906619372c4b7b06b3f8", 
      "operation" : "EXECUTION", 
      "specie" : "Pinus sylvestris", 
      "applicationArea" : "Sistema Ibérico y Sistema Central (Ávila, Burgos, Segovia y Soria)", 
      "executionPeriod" : "5", 
      "operatingDimensions" : "-" 
   },
   // { 
   //    "_id" : ObjectId("62714670e1a38ad6680fed28"), 
   //    "name" : "Psylvestris_stand__gal__v01", 
   //    "description" : "Modelo dinámico de masa para Pinus sylvestris en Galicia", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/masa/Psylvestris_stand_gal_ES.pdf", 
   //    "status" : "stable", 
   //    "modelPath" : "models.stand.Psylvestris_stand__gal__v01", 
   //    "modelClass" : "PinusSylvestrisGaliciaStand", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Pinus sylvestris", 
   //    "applicationArea" : "Galicia (A Coruña, Lugo, Ourense y Pontevedra)", 
   //    "executionPeriod" : "1", 
   //    "operatingDimensions" : "-" 
   // },
   // { 
   //    "_id" : ObjectId("62714697e1a38a334c0fed29"), 
   //    "name" : "Psylvestris_stand__High_Ebro_Basin__v01", 
   //    "description" : "Modelo dinámico de masa para Pinus sylvestris en el Alto Valle del Ebro", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/masa/Psylvestris_stand_ebro_ES.pdf", 
   //    "status" : "stable", 
   //    "modelPath" : "models.stand.Psylvestris_stand__High_Ebro_Basin__v01", 
   //    "modelClass" : "PinusSylvestrisHighEbroBasinStand", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Pinus sylvestris", 
   //    "applicationArea" : "Alto Valle del Ebro (Burgos y Álava)", 
   //    "executionPeriod" : "5", 
   //    "operatingDimensions" : "-" 
   // },
   { 
      "_id" : ObjectId("627146ebe1a38ae5700fed2a"), 
      "name" : "Psylvestris_stand__SILVES__sisc__v01", 
      "description" : "SILVES, modelo dinámico de masa para Pinus sylvestris en el Sistema Ibérico y Sistema Central", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/masa/Psylvestris_stand_SILVES_sisc_ES.pdf", 
      "status" : "stable", 
      "modelPath" : "models.stand.Psylvestris_stand__SILVES__cyl__v01", 
      "modelClass" : "PinusSylvestrisMadridStand", 
      "creatorId" : "6009906619372c4b7b06b3f8", 
      "operation" : "EXECUTION", 
      "specie" : "Pinus sylvestris", 
      "applicationArea" : "Sistema Ibérico y Sistema Central (Madrid, Segovia, Soria y Burgos)", 
      "executionPeriod" : "10 ó 15", 
      "operatingDimensions" : "-" 
   },
   // { 
   //    "_id" : ObjectId("62714712e1a38a6fd10fed2b"), 
   //    "name" : "Psylvestris_stand__SILVES__mad__v01", 
   //    "description" : "SILVES, modelo dinámico de masa para Pinus sylvestris en Madrid", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/masa/Psylvestris_stand_SILVES_mad_ES.pdf", 
   //    "status" : "stable", 
   //    "modelPath" : "models.stand.Psylvestris_stand__SILVES__mad__v01", 
   //    "modelClass" : "PinusSylvestrisSISCStand", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Pinus sylvestris", 
   //    "applicationArea" : "Madrid", 
   //    "executionPeriod" : "10 ó 15", 
   //    "operatingDimensions" : "-" 
   // },
   // { 
   //    "_id" : ObjectId("62714742e1a38a03900fed2c"), 
   //    "name" : "Psylvestris_stand__Ukraine__v01", 
   //    "description" : "Modelo dinámico de masa para Pinus sylvestris en Ucrania", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/masa/Psylvestris_stand_ukraine_ES.pdf", 
   //    "status" : "indevelopment", 
   //    "modelPath" : "models.stand.Psylvestris_stand__Ukraine__v01", 
   //    "modelClass" : "PinusSylvestrisUkraine", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Pinus sylvestris", 
   //    "applicationArea" : "Ucrania", 
   //    "executionPeriod" : "5", 
   //    "operatingDimensions" : "-" 
   // },
   { 
      "_id" : ObjectId("627144dde1a38aa7460fed1f"), 
      "name" : "Qpetraea__pal__v01", 
      "description" : "Modelo estático de árbol individual para Quercus petraea en Palencia", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Qpetraea_pal_ES.pdf", 
      "status" : "indevelopment", 
      "modelPath" : "models.trees.Qpetraea__pal__v01", 
      "modelClass" : "QuercusPetraeaPalencia", 
      "creatorId" : "6009906619372c4b7b06b3f8", 
      "operation" : "EXECUTION", 
      "specie" : "Quercus petraea", 
      "applicationArea" : "Palencia", 
      "executionPeriod" : "0", 
      "operatingDimensions" : "-" 
   },
   { 
      "_id" : ObjectId("6271450de1a38a9cd00fed20"), 
      "name" : "Qpyrenaica__cyl__v01", 
      "description" : "Modelo de crecimiento de árbol individual para Quercus pyrenaica en Castilla y León", 
      "type" : "projection", 
      "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Qpyrenaica_cyl_ES.pdf", 
      "status" : "stable", 
      "modelPath" : "models.trees.Qpyrenaica__cyl__v01", 
      "modelClass" : "QuercusPyrenaicaCyL", 
      "creatorId" : "6009906619372c4b7b06b3f8", 
      "operation" : "EXECUTION", 
      "specie" : "Quercus pyrenaica", 
      "applicationArea" : "Castilla y León (León, Palencia, Burgos, Zamora, Valladolid, Soria, Salamanca, Ávila y Segovia)", 
      "executionPeriod" : "10", 
      "operatingDimensions" : "-" 
   },
   // { 
   //    "_id" : ObjectId("62714536e1a38a1b200fed21"), 
   //    "name" : "Qrobur__gal__v01", 
   //    "description" : "Modelo estático de árbol individual para Quercus robur en Galicia", 
   //    "type" : "projection", 
   //    "docs" : "https://raw.githubusercontent.com/simanfor-dask/SIMANFOR-first_steps/main/modelos/arbol/Qrobur_gal_ES.pdf", 
   //    "status" : "indevelopment", 
   //    "modelPath" : "models.trees.Qrobur__gal__v01", 
   //    "modelClass" : "QuercusRoburGalicia", 
   //    "creatorId" : "6009906619372c4b7b06b3f8", 
   //    "operation" : "EXECUTION", 
   //    "specie" : "Quercus robur", 
   //    "applicationArea" : "Galicia (A Coruña, Lugo, Ourense y Pontevedra)", 
   //    "executionPeriod" : "0", 
   //    "operatingDimensions" : "-" 
   // },
   { 
      "_id" : ObjectId("5f28ff42ad6abc5c2dbf0996"), 
      "name" : "by above", 
      "description" : "Clara por lo alto", 
      "type" : "cutting", 
      "docs" : "https://www.simanfor.es", 
      "status" : "stable", 
      "modelPath" : "models.harvest.cut_down_by_tallest", 
      "modelClass" : "CutDownByTallest", 
      "creatorId" : "5ede024cbac06261fcba6a87", 
      "operation" : "HARVEST", 
      "allowedVariables" : "time(number),percent(text),type(text)", "applicationArea" : "all", 
      "executionPeriod" : "0", 
      "operatingDimensions" : "-", 
      "specie" : "all" }
] )
