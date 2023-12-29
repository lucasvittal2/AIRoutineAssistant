import pytest
from ETL.todoist.TodoIstExtractor import TodoIstExtractor
from Env.paths import *
import os
import pandas as pd


def is_directory_empty(directory_path):
    return len(os.listdir(directory_path)) == 0

def get_data(todoextractor: TodoIstExtractor) -> tuple:
    
    if is_directory_empty(EXTRACTED_DATA_PATH):
        data = todoextractor.extract_data()
        todoextractor.load_on_database(data['opened_tasks'], 'opened_tasks.csv')
        todoextractor.load_on_database(data['completed_tasks'], 'completed_tasks.csv')
        todoextractor.load_on_database(data['projects'], 'projects.csv')
        todoextractor.load_on_database(data['comments'], 'comments.csv')
        todoextractor.load_on_database(data['productivity_stats'], 'productivity_stats.csv')

    files = [f for f in os.listdir(EXTRACTED_DATA_PATH) if os.path.isfile(os.path.join(EXTRACTED_DATA_PATH, f))]
    dfs = [ pd.read_pickle(os.path.join(EXTRACTED_DATA_PATH, f)) for f in files ]
    
    return files, dfs



@pytest.fixture(scope='module')
def todoist_extractor():
    extractor = TodoIstExtractor()
    return extractor



def test_if_extraction_datetime_on_schema(todoist_extractor):
    files, dfs = get_data(todoist_extractor)
    for database, df in zip(files, dfs):
        assert 'extraction_datetime' in df.columns, f"The field extraction_datetime should be at {database.replace('.pkl', '')} table schema."
        
def test_if_extractiondate_is_datetime(todoist_extractor):
    files, dfs = get_data(todoist_extractor)
    for database, df in zip(files, dfs):
        assert df['extraction_datetime'].dtype == 'datetime64[ns]', f"The field extraction_datetime should be datetime type at {database.replace('.pkl', '')} table schema."

def test_if_duplicates(todoist_extractor):
    files, dfs = get_data(todoist_extractor)
    for database, df in zip(files,dfs):
        try:
            duplicates = df.duplicated(subset=['id']).sum()
            assert duplicates == 0, f'There are {duplicates} duplicates on {database.replace('.pkl', '')} table.'
        except:
            duplicates = df.duplicated(subset=['date']).sum()
            assert duplicates == 0, f'There are {duplicates} duplicates on {database.replace('.pkl', '')} table.'
            


def test_if_extraction_datetime_is_null(todoist_extractor):
    files, dfs = get_data(todoist_extractor)
    for database, df in zip(files, dfs):
        assert df['extraction_datetime'].isnull().sum() == 0, f"The field extraction_datetime should not be null at {database.replace('.pkl', '')} table schema."