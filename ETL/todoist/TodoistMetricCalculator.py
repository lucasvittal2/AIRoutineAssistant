from DatabaseHandler.PostgresHandler import PostgresHandler


class TodoistMetricCalculator:
    def __init__(self):
        self.postgres_handler = PostgresHandler()
        self.postgres_handler.connect('todoist')
        

    def get_opened_tasks_amount(self):
        query = "SELECT COUNT(*) FROM openedtasks;"
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_opened_tasks(self):
        query = """
            SELECT t.content  FROM openedtasks ot 
            INNER JOIN  tasks t on ot.id = t.id 
            WHERE ot.parent_id IS NULL;
        """
        response = self.postgres_handler.read_data(query)
        return response['content'].tolist()
    
    def get_subtasks_amount(self, task:str = None):
        if task:
            query = f"""
                SELECT COUNT(ot.id)
                FROM openedtasks ot 
                INNER JOIN  tasks t 
                ON ot.parent_id = t.id 
                WHERE ot.parent_id IS NOT NULL
                AND t.content='{task}';
            """
        else:
            query = """
                SELECT COUNT(parent_id)  
                FROM openedtasks
                WHERE parent_id IS NOT NULL;
            """
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_completed_taks_amount(self, date:str = None):
        if date:
            query = f"""
                SELECT COUNT(*) FROM completedtasks
                WHERE DATE(completed_at)=DATE('{date}');
            """
        else:
            query = """
                SELECT COUNT(*) FROM completedtasks;
            """
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_completed_taks_avg_amount(self):

        query = """
            SELECT 
            COUNT(*)/COUNT(DISTINCT(DATE(completed_at))) as count
            FROM completedtasks;
        """
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_completed_taks(self, date:str = None):
        if date:
            query = f"""
                    SELECT t.content  
                    FROM completedtasks ct 
                    INNER JOIN tasks t
                    ON t.id=ct.id
                    WHERE DATE(completed_at)=DATE('{date}') ;

                """
        else:
            return None
        response = self.postgres_handler.read_data(query)
        return response['content'].tolist()
    
    def get_projects_completed_tasks(self, date:str = None):
        if date:
            query = f"""
                SELECT p.name, COUNT(*) as count
                FROM completedtasks ct 
                INNER JOIN tasks t
                ON t.id=ct.id
                INNER JOIN projects p
                ON t.project_id=p.id
                WHERE DATE(completed_at)=DATE('{date}')
                GROUP BY p.name
                ORDER BY count DESC;
            """
        else:
            query = f"""
                SELECT p.name, COUNT(*) as count
                FROM completedtasks ct 
                INNER JOIN tasks t
                ON t.id=ct.id
                INNER JOIN projects p
                ON t.project_id=p.id
                GROUP BY p.name
                ORDER BY count DESC;
            """
        response = self.postgres_handler.read_data(query)
        return response.to_dict('records')
    
    def get_comments(self, task: str, date:str = None):
        
        if date:
            query = f"""
            SELECT c.posted_at, c.content 
            FROM comments c INNER JOIN  tasks t 
            on t.id=c.task_id 
            WHERE t.content='{task}'
            AND DATE(c.posted_at)=DATE('{date}');
            """
        else:
            query = f"""
            SELECT c.posted_at, c.content 
            FROM comments c INNER JOIN  tasks t 
            on t.id=c.task_id 
            WHERE t.content='{task}';
            """
        response = self.postgres_handler.read_data(query)
        return response['content'].tolist()
    
    def get_comments_by_word(self, key_word:str):
        query= f"""
            SELECT content 
            FROM comments 
            WHERE LOWER(content) LIKE LOWER('%{key_word}%');
        """
        response = self.postgres_handler.read_data(query)
        return response['content'].tolist()