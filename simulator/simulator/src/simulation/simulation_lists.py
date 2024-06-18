# Auxiliar lists of information to use on simulation.py document


# lists of variables created to print them at the output file

METADATA = [  # metadata permanent information about simulator developement
    'web_sima',
    'link_sima',
    'webs_iufor',
    'web_iufor',
    'link_iufor',
    'facebook',
    'iufor_facebook',
    'twitter',
    'iufor_twitter',
    'instagram',
    'iufor_instagram',
    'linkedin',
    'iufor_linkedin',
    'youtube',
    'iufor_youtube',
    'flickr', 
    'iufor_flickr',
    'model',
    'vars',
    'plot',
    'tree',
    'summary', 
    'plot_type',
    'area',
    'scenario', 
    'cuts',
    'under_development',
    'tree_independent',
    'tree_dependent',
    'stand_model',
    'size-class models'
]

SUMMARY = [  # summary information variables, with repeated variables silenced
    'sum_hdom',  #Ho m
    'sum_density_b_cut',  #N pies/ha
    'sum_qmdbh_b_cut',  #Dg cm
    'sum_ba_b_cut',  #G m2/ha
    'sum_vol_b_cut',  #V m3/ha
    'sum_density_cut',  #N pies/ha
    #'sum_qmdbh_cut',  #Dg cm
    #'sum_vol_cut',  #V m3/ha
    #'sum_density_a_cut',  #N pies/ha
    #'sum_qmdbh_a_cut',  #Dg cm
    #'sum_ba_a_cut',  #G m2/ha
    #'sum_vol_a_cut',  #V m3/ha
    #'sum_density_dead',  #N pies/ha
    #'sum_qmdbh_dead',  #Dg cm
    #'sum_vol_dead',  #V m3/ha
    #'sum_density_ing',  #N pies/ha
    #'sum_ba_ing',  #G m2/ha
    'stand_before_cut',  #Masa principal antes de la clara
    'stand_cut',  #Masa extraída
    'stand_after_cut'  #Masa principal después de la clara
]

SUMMARY_EXTENSION = [  # some variables that can be added (or not) to the output file
    'stand_dead',  # Mortality
    'stand_ingrowth',  # Ingrowth
    # Special variables about no timber products
    'QSUBER_VARS',  # Quercus suber - no timber products
    'W_CORK',  # W Fresh Cork (Tn/ha)
    'TOTAL_W_DEBARK',
    'BARK_VOL',  # V Cork (m3/ha)
    'TOTAL_V_DEBARK',
    'PPINEA_VARS',  # Pinus pinea - no timber products
    'ALL_CONES',  # Cones/(ha*year)
    'SOUND_CONES',  # Sound cones/(ha*year)
    'SOUND_SEEDS',  # Sound seeds/(ha*year)
    'W_SOUND_CONES',  # Sound cones biomass (Tn/ha*year)
    'W_ALL_CONES',  # Total cones biomass (Tn/ha*year)
    'MUSHROOMS_VARS',  # Mushrooms production
    'EDIBLE_MUSH',  # Edible (kg/ha*year)
    'MARKETED_MUSH',  # Marketed (kg/ha*year)
    'MARKETED_LACTARIUS',  # Marketed Lactarius (kg/ha*year)
    'MUSHROOM_PRODUCTIVITY'  # Total fresh-weight mushroom productivity (kg fw/ha)
]

GENERAL_INFO = [
    # Cuts
    'PercentOfTrees',
    'Percent of trees',
    'Volumen',
    'Area',
    'Cut Down by Tallest',
    'Cut Down by Smallest',
    'Systematics cut down',

    # Output sheets information
    'plot_sheet',
    'node_sheet',
    'trees_sheet',
    'description_sheet',
    'summary_sheet',
    'metadata_sheet',   
    'initial_inventory',

    # Output titles - summary
    'main_specie',
    'specie_ifn_id',
    'forest',
    'study_area',
    'model',
    'scenario',
    'inventory',
    'plot',
    'sum_age',
    'sum_year',
    'sum_hdom',
    'sum_density_b_cut',
    'sum_qmdbh_b_cut',
    'sum_ba_b_cut',
    'sum_vol_b_cut',
    'sum_density_cut',
    'sum_qmdbh_cut',
    'sum_vol_cut',
    'sum_density_a_cut',
    'sum_qmdbh_a_cut',
    'sum_ba_a_cut',
    'sum_vol_a_cut',
    'sum_density_dead',
    'sum_qmdbh_dead',
    'sum_vol_dead',
    'sum_density_ing',
    'sum_ba_ing',
    'stand_before_cut',
    'stand_cut',
    'stand_after_cut',
    'stand_dead',
    'stand_ingrowth',
    # Special variables about no timber products
    'QSUBER_VARS',
    'W_CORK',
    'BARK_VOL',
    'PPINEA_VARS',
    'ALL_CONES',
    'SOUND_CONES',
    'SOUND_SEEDS',
    'W_SOUND_CONES',
    'W_ALL_CONES',
    'MUSHROOMS_VARS',
    'EDIBLE_MUSH',
    'MARKETED_MUSH',
    'MARKETED_LACTARIUS',
    'MUSHROOM_PRODUCTIVITY',  # Total fresh-weight mushroom productivity (kg fw/ha)

    # Output titles - description
    'model_info',    
    'plot_info',
    'datetime',

    # Output contents - Scenario variable contents
    'LOAD',
    'INIT',
    'EXECUTION',
    'HARVEST',
    'DEBARK'
    ]

CUTS = [  # cuts information
    # cut types
    'Cut Down by Tallest',
    'Cut Down by Smallest',
    'Systematics cut down',
    # cut criterias
    'Percent of trees', 
    'Volumen', 
    'Area'
]