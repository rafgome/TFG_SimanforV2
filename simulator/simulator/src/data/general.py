
from util import Tools
from data.variables import AREA_VARS, MODEL_VARS, PLOT_VARS, WARNING_VARS

import logging


class Area:
    """
    Class wich contains the declaration of area variables needed to be used across the simulator.
    Variables list are available at "variables.py" file.
    That variables are received to the simulator as PLOT variables, and then obtained from that variables, 
    in order to show them in a different place of the output.
    """

    @staticmethod
    def get_index_by_name(name):
        return AREA_VARS.index(name)

    @staticmethod
    def get_name_by_index(index):
        return AREA_VARS[index]


    # VARIABLES

    @property
    def plot_type(self):
        return self.__values['PLOT_TYPE']

    @property
    def plot_area(self):
        return self.__values['PLOT_AREA']

    @property
    def province(self):
        return self.__values['PROVINCE']

    @property
    def study_area(self):
        return self.__values['STUDY_AREA']

    @property
    def municipality(self):
        return self.__values['MUNICIPALITY']

    @property
    def forest(self):
        return self.__values['FOREST']

    @property
    def prov_region(self):
        return self.__values['PROV_REGION']

    @property
    def main_specie(self):
        return self.__values['MAIN_SPECIE']

    @property
    def specie_ifn_id(self):
        return self.__values['SPECIE_IFN_ID']

    @property
    def slope(self):
        return self.__values['SLOPE']

    @property
    def aspect(self):
        return self.__values['ASPECT']

    @property
    def continentality(self):
        return self.__values['CONTINENTALITY']
 
    @property
    def altitude(self):
        return self.__values['ALTITUDE']

    @property
    def longitude(self):
        return self.__values['LONGITUDE']

    @property
    def latitude(self):
        return self.__values['LATITUDE']

    @property
    def aa_rainfall(self):
        return self.__values['AA_RAINFALL']

    @property
    def ma_temperature(self):
        return self.__values['MA_TEMPERATURE']        

    @property
    def september_rain(self):
        return self.__values['SEPTEMBER_RAIN']

    @property
    def september_temp(self):
        return self.__values['SEPTEMBER_TEMP']

    @property
    def november_rain(self):
        return self.__values['NOVEMBER_RAIN']

    @property
    def november_temp(self):
        return self.__values['NOVEMBER_TEMP']

    @property
    def martonne(self):
        return self.__values['MARTONNE']
   
    @property
    def martonne_2020(self):
        return self.__values['MARTONNE_2020']

    @property
    def martonne_2040(self):
        return self.__values['MARTONNE_2040']

    @property
    def martonne_2060(self):
        return self.__values['MARTONNE_2060']

    @property
    def martonne_2080(self):
        return self.__values['MARTONNE_2080']        

    @property
    def tr(self):
        return self.__values['TR']
   
    @property
    def time_at(self):
        return self.__values['TIME_AT']

    @property
    def rain_as(self):
        return self.__values['RAIN_AS']

    @property
    def tmin_so(self):
        return self.__values['TMIN_SO']

    @property
    def tmin_on(self):
        return self.__values['TMIN_ON']  

    @property
    def tmin_ond(self):
        return self.__values['TMIN_OND']
   
    @property
    def tmmin_oct(self):
        return self.__values['TMMIN_OCT']

    @property
    def tsum_mean_so(self):
        return self.__values['TSUM_MEAN_SO']

    @property
    def tsum_mmin_so(self):
        return self.__values['TSUM_MMIN_SO']

    @property
    def tsum_mmin_on(self):
        return self.__values['TSUM_MMIN_ON']     

    @property
    def tsum_mmin_sond(self):
        return self.__values['TSUM_MMIN_SOND']     


class Model:
    """
    Class wich contains the declaration of model variables needed to be used across the simulator.
    Variables list are available at "variables.py" file.
    That variables will be created at the model used on the scenario.
    """

    @staticmethod
    def get_index_by_name(name):
        return MODEL_VARS.index(name)

    @staticmethod
    def get_name_by_index(index):
        return MODEL_VARS[index]


    # VARIABLES

    @property
    def model_name(self):
        return self.__values['MODEL_NAME']

    @property
    def specie_ifn_id(self):
        return self.__values['SPECIE_IFN_ID'] 

    @property
    def aplication_area(self):
        return self.__values['APLICATION_AREA']    

    @property
    def valid_prov_reg(self):
        return self.__values['VALID_PROV_REG']                        

    @property
    def exec_time(self):
        return self.__values['EXEC_TIME']   

    @property
    def model_type(self):
        return self.__values['MODEL_TYPE']    

    @property
    def model_card_es(self):
        return self.__values['MODEL_CARD_ES']    

    @property
    def model_card_en(self):
        return self.__values['MODEL_CARD_EN']    


class Warnings:
    """
    Class wich contains the declaration of warning variables needed to be used across the simulator.
    Variables list are available at "variables.py" file.
    To activate that warning variables, they must receive the value 1.
    """

    @staticmethod
    def get_index_by_name(name):
        return WARNING_VARS.index(name)

    @staticmethod
    def get_name_by_index(index):
        return WARNING_VARS[index]

    @property
    def values(self):
        return self.__values

    def get_value(self, var: str):
        """
        Function neccesary to obtain the variable value
        """
        return self.__values[var]

    def print_value(variable, dec_pts: int = 2):
        """
        Function neccesary to print the tree values on the output.
        """

        if isinstance(self.__values[variable], float):
            return round(self.__values[variable], dec_pts)
        return self.__values[variable]

    def add_value(self, variable, value):
        """
        Function neccesary to add a value to a variable by sustitution from the past value.
        """
        self.__values[variable] = value

        
    # VARIABLES

    @property
    def specie_error(self):
        return self.__values['SPECIE_ERROR']

    @property
    def specie_error_trees(self):
        return self.__values['SPECIE_ERROR_TREES']

    @property
    def exec_error(self):
        return self.__values['EXEC_ERROR']

    @property
    def exec_error_summary(self):
        return self.__values['EXEC_ERROR_SUMMARY']

    @property
    def cut_error(self):
        return self.__values['CUT_ERROR']

    @property
    def cut_error_summary(self):
        return self.__values['CUT_ERROR_SUMMARY']

