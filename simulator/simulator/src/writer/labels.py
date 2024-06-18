
from data import Tree
from data import Plot
from data.general import Area, Model, Warnings
from simulation.simulation_lists import *
from data.variables import *

import i18n

class Labels:

    def get_labels():
        """
        Function neccesary to set the label names of the used variables.
        That function is needed to print the output. 
        All the variables to show in the output must appear on that function.
        """

        labels = dict()

        # 
        # area
        # 
        for j in range(len(AREA_VARS)):
            labels['simanfor.area.' + AREA_VARS[j]] = i18n.t('simanfor.area.' + AREA_VARS[j])
            labels['simanfor.metadata.' + AREA_VARS[j]] = i18n.t('simanfor.metadata.' + AREA_VARS[j])

        #
        # cuts
        #
        for j in range(len(CUTS)):
            labels['simanfor.metadata.' + CUTS[j]] = i18n.t('simanfor.metadata.' + CUTS[j])  

        # 
        # general
        # 
        for j in range(len(GENERAL_INFO)):
            labels['simanfor.general.' + GENERAL_INFO[j]] = i18n.t('simanfor.general.' + GENERAL_INFO[j])

        #
        # metadata
        #
        for j in range(len(METADATA)):
            labels['simanfor.metadata.' + METADATA[j]] = i18n.t('simanfor.metadata.' + METADATA[j]) 

        # 
        # model
        # 
        for j in range(len(MODEL_VARS)):
            labels['simanfor.model.' + MODEL_VARS[j]] = i18n.t('simanfor.model.' + MODEL_VARS[j])
            labels['simanfor.metadata.' + MODEL_VARS[j]] = i18n.t('simanfor.metadata.' + MODEL_VARS[j])
        
        # 
        # plot
        # 
        for j in range(len(SCENARIO_VARS)):
            labels['simanfor.plot.' + SCENARIO_VARS[j]] = i18n.t('simanfor.plot.' + SCENARIO_VARS[j])
            labels['simanfor.metadata.' + SCENARIO_VARS[j]] = i18n.t('simanfor.metadata.' + SCENARIO_VARS[j])  
        for j in range(len(PLOT_VARS)):
            labels['simanfor.plot.' + PLOT_VARS[j]] = i18n.t('simanfor.plot.' + PLOT_VARS[j])
            labels['simanfor.metadata.' + PLOT_VARS[j]] = i18n.t('simanfor.metadata.' + PLOT_VARS[j]) 

        # 
        # tree
        # 
        for i in range(len(Tree.variables_names())):
            labels['simanfor.tree.' + Tree.variables_names()[i]] = i18n.t('simanfor.tree.' + Tree.variables_names()[i])
            labels['simanfor.metadata.' + Tree.variables_names()[i]] = i18n.t('simanfor.metadata.' + Tree.variables_names()[i])            
        for i in range(len(Tree.variables_names_original())):
            labels['simanfor.tree.' + Tree.variables_names_original()[i]] = i18n.t('simanfor.tree.' + Tree.variables_names_original()[i])
            labels['simanfor.metadata.' + Tree.variables_names_original()[i]] = i18n.t('simanfor.metadata.' + Tree.variables_names_original()[i])
        labels['simanfor.tree.status'] = i18n.t('simanfor.tree.status') 
        labels['simanfor.metadata.status'] = i18n.t('simanfor.metadata.status') 

        #
        # summary contents
        #
        for j in range(len(SUMMARY)):
            labels['simanfor.general.' + SUMMARY[j]] = i18n.t('simanfor.general.' + SUMMARY[j]) 
            labels['simanfor.metadata.' + SUMMARY[j]] = i18n.t('simanfor.metadata.' + SUMMARY[j]) 

        #
        # special summary contents
        #
        for j in range(len(SUMMARY_EXTENSION)):
            labels['simanfor.general.' + SUMMARY_EXTENSION[j]] = i18n.t('simanfor.general.' + SUMMARY_EXTENSION[j]) 
            labels['simanfor.metadata.' + SUMMARY_EXTENSION[j]] = i18n.t('simanfor.metadata.' + SUMMARY_EXTENSION[j]) 
        labels['simanfor.metadata.QSUBER_VARS'] = i18n.t('simanfor.metadata.QSUBER_VARS')
        labels['simanfor.metadata.PPINEA_VARS'] = i18n.t('simanfor.metadata.PPINEA_VARS')
        labels['simanfor.metadata.MUSHROOMS_VARS'] = i18n.t('simanfor.metadata.MUSHROOMS_VARS')

        # 
        # warnings
        # 
        for j in range(len(WARNING_VARS)):
            labels['simanfor.warnings.' + WARNING_VARS[j]] = i18n.t('simanfor.warnings.' + WARNING_VARS[j])
            labels['simanfor.metadata.' + WARNING_VARS[j]] = i18n.t('simanfor.metadata.' + WARNING_VARS[j])

        return labels


    def get_metadata_labels(var):
        """
        Function to get the possibility of create a new metadata label.
        """

        labels = dict()
        labels['simanfor.metadata.' + var] = i18n.t('simanfor.metadata.' + var)
        return labels
