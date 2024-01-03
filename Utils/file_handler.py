import yaml
import json

def read_yaml(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def write_yaml(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        yaml.dump(data, file)
        
def append_on_yaml(file_path: str, data: dict) -> None:
    with open(file_path, 'a') as file:
        yaml.dump(data, file)
        
def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)