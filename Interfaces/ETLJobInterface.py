from abc import ABC
from Env.project_types import *


class ETLJobInterface(ABC):
    def __init__(self):
        pass
    def __update_extractrion_record_track(self, file_path: str, timestamp: TimeRecord) -> None:
        pass

    
    def __parse_to_df(self, data: Dict)-> Table:
        pass

    def extract_data(self) -> Json:
        pass
    
    def get_last_data_update_record_track(self, file_path: str, time_format: str = "%Y-%m-%d %H:%M:%S") -> TimeRecord:
        pass
    
    def load_on_database(self, data: DataFrame) -> None:
        pass