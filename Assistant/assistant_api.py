from Assistant.GPTAssistant import GPTAssistant
from Env.paths import ASSISTANT_FUNCTIONS_CONFIG_PATH
assistant = GPTAssistant(assistant_functions_config_file=ASSISTANT_FUNCTIONS_CONFIG_PATH +  "todoist_assistant_functions_config.json")
answer = assistant.get_answer("Quantas tarefas foram concluidas no dia '2024-01-02'?")
print(answer)