Test documents developed by Aitor:  
  
* all_models_test --> test to be sure that all the models run well after model updates
* inputs (folder) --> excel documents with some non-real data to check if the model updates are well done
* scenarios (folder) --> json documents with an example scenario to check if the model updates are well done
* outputs (folder) --> excel documents with the test output
* terminal_info (folder) --> terminal information obtained after execute all_models_test file
    
    
To run all_models_test, the user must be at the tests folder:  
  
simulator/simulator/tests  
  
and run:   
  
bash all_models_test  
  
  
Para comprobar si hay errores en las ejecuciones, bastaría con el siguiente comando:  
  
  grep -r "mistake"  
  
  grep -r "Traceback"  
    
    



