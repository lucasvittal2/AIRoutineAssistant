from typing import Dict
from pandas import DataFrame
from datetime import datetime
from todoist_api_python.models import Task, CompletedItems,Project, Comment
from todoist_api_python.models import Project
from typing import List

Table = DataFrame
Json = Dict
TimeRecord = datetime
TodoistOpenedTask = Task
TodoistOpenedTasks = List[TodoistOpenedTask]
TodoistCompletedTasks = CompletedItems
TodoistProject = List[Project]
TodoistProjects = List[TodoistProject]
TodoistComment = Comment
TodoistComments = List[TodoistComment]
TodoistKarmaProductivity = Dict



Documents = List[dict]