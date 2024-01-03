from flask import Flask, request, jsonify
from flask_cors import CORS
from Assistant.GPTAssistant import GPTAssistant
from Env.paths import ASSISTANT_FUNCTIONS_CONFIG_PATH


#flask app
app = Flask(__name__)
CORS(app)

assistant = GPTAssistant(assistant_functions_config_file=ASSISTANT_FUNCTIONS_CONFIG_PATH +  "todoist_assistant_functions_config.json")

@app.route('/getAnswer', methods = ['POST', 'GET'])
def get_answer():
    print(request.json)
    query = request.json['query']
    answer = assistant.get_answer(query)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)