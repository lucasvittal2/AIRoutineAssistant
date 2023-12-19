from Interfaces.ETLJobInterface import ETLJobInterface
from Env.project_types import *
from Env.paths import DATA_TRACK_PATH
import datetime

class TodoIstExtractor(ETLJobInterface):
    def __init__(self):
        last_update = self.__get_last_data_update_record_track(DATA_TRACK_PATH + 'extraction_records.txt')
        self.last_update = last_update if last_update != '' else None
            
    def __get_last_data_update_record_track(self, file_path: str, time_format: str = "%Y-%m-%d %H:%M:%S") -> TimeRecord:
        with open(file_path, 'r') as file:
            last_record = file.readlines()[-1]
            timestamp = datetime.datetime.strptime(last_record.strip(), time_format)
        return timestamp
    
    def __update_extractrion_record_track(self, file_path: str, timestamp: TimeRecord) -> None:
        with open(file_path, 'a') as file:
            file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S") + '\n')

    def extract_data(self) -> Json:
        pass

    def parse_to_df(self, data: Dict)-> Table:
        pass

    def load_on_database(self, data: DataFrame) -> None:
        pass

