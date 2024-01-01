from pandas import DataFrame as PandasDataFrame
from sqlalchemy import create_engine
from Interfaces.DatabaseHandler import DatabaseHandler
from Env.paths import DRIVERS_PATH,CONFIG_PATH
from Utils.file_handler import read_yaml
from Env.project_types import *
import psycopg2

class PostgresHandler(DatabaseHandler):
    def __init__(self):
       
        self.postgres_configs  = read_yaml(CONFIG_PATH + 'app_config.yaml')['databases']['postgres']
        #set disconnect statte
        self.url = None
        self.properties= None

    def connect(self, db_name: str) -> None:
        host = self.postgres_configs['host']
        port = self.postgres_configs['port']
        user = self.postgres_configs['user']
        password = self.postgres_configs['password']

        # Create connection string
        self.conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

        # Create connection
        self.conn = psycopg2.connect(self.conn_str)

    def disconnect(self):
        #set disconnect statte
        self.conn = None
        
    def __filter_duplicates(self, table_name: str, data: PandasDataFrame) -> PandasDataFrame:
        df = self.read_data(f"SELECT * FROM {table_name}")
        
        if len(df) == 0:
            return data #do full load
        
        last_update = df['extraction_datetime'].max()
        filtered_df = data[data['extraction_datetime'] > last_update]
        return filtered_df

    def write_data(self, table_name: str, data: PandasDataFrame) -> None:
        postgresdb = create_engine(self.conn_str)
        filtered_df = self.__filter_duplicates(table_name, data)
        filtered_df.to_sql(table_name, postgresdb.engine, if_exists='append', index=False)

    def read_data(self, query: str) -> PandasDataFrame:
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
        return PandasDataFrame(data)

