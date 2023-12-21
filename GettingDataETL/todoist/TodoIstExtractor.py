import requests
from todoist_api_python.api import TodoistAPI
from Env.project_types import Dict, Table
from Interfaces.ETLJobInterface import ETLJobInterface
from Env.project_types import *
from Env.paths import *
from Utils.file_handler import read_yaml
from pandas import DataFrame
import datetime

class TodoIstExtractor(ETLJobInterface):
    def __init__(self):
        
        #get api key
        api_key = read_yaml(CONFIG_PATH + 'app_config.yaml')['API_KEYS']['TODOIST_API_KEY']
        self.todoist_api = TodoistAPI(token=api_key)
        
        #get record data update track
        last_update = self.__get_last_data_update_record_track(DATA_TRACK_PATH + 'extraction_records.txt')
        self.last_update = last_update if last_update != '' else None
        
    def __get_last_data_update_record_track(self, file_path: str, time_format: str = "%Y-%m-%d %H:%M:%S") -> TimeRecord:
        with open(file_path, 'r') as file:
            if len(file.readlines()) == 0:
                return None
            last_record = file.readlines()[-1]
            timestamp = datetime.datetime.strptime(last_record.strip(), time_format)
        return timestamp
    
    def __update_extractrion_record_track(self, file_path: str, timestamp: TimeRecord) -> None:
        with open(file_path, 'a') as file:
            file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S") + '\n')
    
    def __get_open_tasks(self) -> TodoistOpenedTasks:

        try:
            url = "https://api.todoist.com/sync/v9/sync"
            headers = {
                "Authorization": f"Bearer {self.todoist_api.token}",
            }
            data = {
                "sync_token": "*",
                "resource_types": '["projects"]',
            }

            response = requests.post(url, headers=headers, data=data)
            return response.json()
        except Exception as error:
            print(error)
            return None
        
    def __get_completed_tasks(self) -> TodoistCompletedTasks:

        try:
            closed_tasks = self.todoist_api.get_completed_items()
            return dict([task.__dict__ for task in closed_tasks])
        except Exception as error:
            
            print(error)
            return None
            
    def __get_projects(self) -> TodoistProjects:
        
        try:
            projects = self.todoist_api.get_projects()
            return dict([proj.to_dict() for proj in projects])
        except Exception as error:
            print(error)
            return None
        
    def __get_comments(self) -> TodoistComments:

        try:
            comments = self.todoist_api.get_comments()
            return [ comment.to_dict for comment in comments]
        except Exception as error:
            print(error)
            return None
    def parse_to_df(self, data: Dict) -> Table:
        
        fields = data.keys()
        
        df = DataFrame(data, columns=fields)
        return df
    
    def extract_data(self) -> Json:
        
        open_tasks = self.__get_open_tasks()
        closed_tasks = self.__get_completed_tasks()
        #projects = self.__get_projects()
        #commets= self.__get_comments()
        
        open_tasks_df = self.parse_to_df(open_tasks)
        # closed_tasks_df = self.parse_to_df(closed_tasks)
        # projects_df = self.parse_to_df(projects)
        # comments_df = self.parse_to_df(commets) 
        
        return {
            "opened_tasks": open_tasks_df,
            "closed_tasks": closed_tasks,
            # "projects": projects_df,
            # "comments": comments_df
        }
           
    #This method is not implemented yet, it actually mocked!!!!!
    # Future work: implement this method to load data on postgresql database
    def load_on_database(self, data: DataFrame, file_name: str) -> None:
        
        data.to_csv(DATABASE_PATH + file_name, index=False)

