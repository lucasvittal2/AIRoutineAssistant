import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_base_dir = os.path.dirname(current_file_dir)


PROJECT_PATH=project_base_dir + '/'
ASSETS_PATH=PROJECT_PATH+'Assets/'
DATA_TRACK_PATH=ASSETS_PATH+'DataTrack/'
CONFIG_PATH=ASSETS_PATH+'Configs/'
EXTRACTED_DATA_PATH=ASSETS_PATH+'ExtractedData/'
ASSISTANT_FUNCTIONS_CONFIG_PATH = CONFIG_PATH+'assistant_functions_config/'
ETL_PATH=PROJECT_PATH+'ETL/'
DRIVERS_PATH=ASSETS_PATH+'Drivers/'