# 🤖 AIRoutineAssistant

This app were idealized to be an 🤖 AI assistant to your routine 🏋️‍♂️🥋.
Its mission is to assist the user to organize its routine, get a feeling about his productivity and even being up to date to the engagements, all these stuff on the user hand's palm through the WhatsApp 📱 :

![General Schema](https://github.com/lucasvittal2/AIRoutineAssistant/assets/62555057/e7bde487-c0c4-4692-9a35-b26fb0f35c0b)

Regarding its mission, this app will have the following features:

- Extract  Data from the main organization App like TodoIst, Google Calendar  or Notion
- process this data and load it into a Relational Database designed specially to get  user routine productivity metrics
- Calculate metrics from user's routine
- Generate Vizualization from user routine metrics
- Using a GenAI able to interact throug many source and give the routine information aspect of user from a simple text query

Actualy we finished the development of MVP1 Resulting on AIRoutineAssistant v1.0:


![MVP1 Schema](https://github.com/lucasvittal2/AIRoutineAssistant/assets/62555057/c59f79cf-c673-4761-b19b-839826f6994e)


A demonstration of AIRoutineAssistant v1.0 can be seen in the video below:

https://drive.google.com/file/d/1r9hOXkVn7orffF-t7MqrrGV-mucOIuPO/view?usp=sharing



Our pupose is to enhance the app through iteraction and evoluting it along the sprints in order to take the most assertive decision until reach the final version.
Therefore a new version is being planned to be developed 🏃.
Yes, AIRoutineAssistant v2.0 is comming soon 😎


Here's the instruction to run AIRoutineAssistant v1.0, it's assuming that you have anaconda python 3.10 installed

- Firstly, go to Openai website and create your account
- After that create you api key at ![Openai webpage Apikey  section](https://platform.openai.com/api-keys)
- Get your todoist api token following the  instruction ![Todoist getting token instructions](https://todoist.com/pt-BR/help/articles/find-your-api-token-Jpzx9IIlB)
-  Config the  app_config.yaml file  putting your todoist api keys and todoist api key
-  create the env using ` conda env create -f aiassistant.yaml `
-  Install postgres using the script  `Assets\scripts\install_postgres.sh'
-  Install Apache airflow using the script `Assets\scripts\install_airflow.sh`
-  run apache airflow thorgh `airflow standalone'
-   wait the first job run
-   Access the ui throu the file `frontend\chat-uit.html` and enjoy your ai assistant

The Assistant functions is config through `Assets/Configs/assistant_functions_config/todoist_assistant_functions_config.json` and functions executed are available on `Assistant\GPTAssistant.py`
If you want add new function modify json file accordly openai instructions at ![Openai Assistant document Overview](https://platform.openai.com/docs/assistants/overview) and add new functions on GPTAssistant.py.
