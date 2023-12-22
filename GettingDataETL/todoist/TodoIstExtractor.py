import subprocess
import json
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
            open_tasks = self.todoist_api.get_tasks()
            return open_tasks
           
        # Check for authentication error
        except Exception as error:
            print(error)
            return None
            
    def __get_completed_tasks(self, project_ids: List[str]) -> TodoistCompletedTasks:
        completed_tasks = []
        try:
            for project_id in project_ids:
                shell_command = f"""
                curl https://api.todoist.com/sync/v9/completed/get_all\
                -d "project_id={project_id}"\
                -H "Authorization: Bearer {self.todoist_api._token}"
                """
                response = subprocess.run(shell_command, shell=True, capture_output=True)
                completed_tasks += json.loads(response.stdout)['items']
          
            return completed_tasks
        
        except Exception as error:
            
            print(error)
            return None
            
    def __get_projects(self) -> TodoistProjects:
        
        try:
            projects = self.todoist_api.get_projects()
            return projects
        except Exception as error:
            print(error)
            return None
        
    def __get_comments(self, task_ids: List[str]) -> TodoistComments:

        try:
            comments = [ comment
                        for task_id in task_ids
                        for comment in self.todoist_api.get_comments(task_id=task_id) 
                        if self.todoist_api.get_comments(task_id=task_id) 
                    ]
            return comments
        except Exception as error:
            print(error)
            return None
        
    def __get_productivity_stats(self) -> TodoistKarmaProductivity:
            
            try:
                shell_command = f"""
                    curl https://api.todoist.com/sync/v9/completed/get_stats \
                    -H "Authorization: Bearer {self.todoist_api._token}"
                """
                response = subprocess.run(shell_command, shell=True, capture_output=True)
                karma_stats = json.loads(response.stdout)['days_items']
                return karma_stats
            except Exception as error:
                print(error)
                return None
    def __parse_to_df(self, data: Dict) -> Table:
        
        
        if type(data) == list:
            if type(data[0]) != dict:
                
                fields = data[0].__dict__.keys()
            else:
                fields = data[0].keys()
            
            df = DataFrame(data, columns=fields)

            
        return df 
    
    def extract_data(self) -> Json:
        
        print("Extracting open tasks data...")
        open_tasks = self.__get_open_tasks()
        print("open tasks data extracted !!")
        
        print("Extracting projects data...")
        projects = self.__get_projects()
        print("projects data extracted !!")
        
        
        open_tasks_df = self.__parse_to_df(open_tasks)
        projects_df = self.__parse_to_df(projects)
        
        
        
        # to get completed task  it is necessary to get the project id
        print('Extracting completed tasks data...')
        completed_tasks = self.__get_completed_tasks(projects_df['id'].tolist())
        completed_tasks_df = self.__parse_to_df(completed_tasks)
        print('completed tasks data extracted !!')
        
        
        print('Extracting productivity stats data...')
        prod_stats= self.__get_productivity_stats()
        prod_stats_df = self.__parse_to_df(prod_stats)
        print('productivity stats data extracted !!')
        task_ids = completed_tasks_df['task_id'].tolist()
        task_ids.extend(open_tasks_df['id'].tolist())
        
        
        # to get comments its is needed task ids
        print('Extracting comments data...')
        commets= self.__get_comments(task_ids)
        comments_df = self.__parse_to_df(commets) 
        print("Comments data extracted !!")
        
        
        return {
            "opened_tasks": open_tasks_df,
            "completed_tasks": completed_tasks_df,
            "projects": projects_df,
            "comments": comments_df,
            'productivity_stats': prod_stats_df
        }
           
    #This method is not implemented yet, it actually mocked!!!!!
    # Future work: implement this method to load data on postgresql database
    def load_on_database(self, data: DataFrame, file_name: str) -> None:
        
        data.to_csv(DATABASE_PATH + file_name, index=False)
        print(f'Saved data on {file_name}!')

