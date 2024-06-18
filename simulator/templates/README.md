That folder contains templates ready to be used on SIMANFOR simulator:  
  
* **scenarios**
  * csv_template: file with the specified form to use a csv input
  * hpc_template: file with a example path to be run on HPC
  * json_template: file with the specified form to use a json input
  * stand_template: file with the structure to be used for a new dinamic stand model; condensed version
  * stand_template_long: file with the structure to be used for a new static stand model; extended version  
  * template_explained: file with explanations to build a new scenario file (spanish)  
  * tree_template: file with the structure to be used for a new dinamic tree model; condensed version
  * tree_template_long: file with the structure to be used for a new dinamic tree model; extended version  
  * tree_static_template: file with the structure to be used for a new static tree model; condensed version
  * tree_static_template_long: file with the structure to be used for a new static tree model; extended version
   
* **inventories**
  * mix_template: template to mixed tree models (red columns must have information; orange is reccomended)
  * input_template: template to tree and stand models (red column required; orange reccomended; yellow depending on the model to use (see model cards)):  
    * tree models: information about trees is needed
    * stand models: information about trees is required only is the stand information is not enough to the first calculation process (initialize)
  * sparql_plot: example file of inventory generated with sparql (plot data)
  * sparql_tree: example file of inventory generated with sparql (tree data)
* **models**
  * stand_template: to stand models
  * tree_template: to tree models (1 specie)
  * tree_mix_template: to tree models (2 species)  
  
To the case of models, before use them is important to check at simulator/src/models/tree or simulator/src/models/stand for the updated one.  
