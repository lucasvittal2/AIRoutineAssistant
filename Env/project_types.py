from typing import Dict
from pandas import DataFrame
from datetime import datetime
from todoist_api_python.models import Task, CompletedItems,Project, Comment
from todoist_api_python.models import Project
from typing import List

type Table = DataFrame
type Json = Dict
type TimeRecord = datetime
type TodoistOpenedTask = Task
type TodoistOpenedTasks = List[TodoistOpenedTask]
type TodoistCompletedTasks = CompletedItems
type TodoistProject = List[Project]
type TodoistProjects = List[TodoistProject]
type TodoistComment = Comment
type TodoistComments = List[TodoistComment]
type TodoistKarmaProductivity = Dict