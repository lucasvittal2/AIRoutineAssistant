from Utils.file_handler import read_yaml

app_configs = read_yaml("../Assets/Configs/app_config.yaml")
PROEJCT_PATH=app_configs['proj_base_path']
ASSETS_PATH=PROEJCT_PATH+'Assets/'
DATA_TRACK_PATH=ASSETS_PATH+'DataTrack/'
CONFIG_PATH=ASSETS_PATH+'Configs/'
EXTRACTED_DATA_PATH=ASSETS_PATH+'ExtractedData/'
ASSISTANT_FUNCTIONS_CONFIG_PATH = CONFIG_PATH+'assistant_functions_config/'
ETL_PATH=PROEJCT_PATH+'ETL/'
DRIVERS_PATH=ASSETS_PATH+'Drivers/'