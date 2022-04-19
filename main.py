# Make flask initialization

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/hook/temperature', methods=['POST'])
def temperature():
    if request.method == 'POST':
        data = request.json
        
        if "value" not in data:
            return ("'value' not found", 400)
        
        print(data)
        print("Received:", "temperature:", data['value'])
        return ""

app.run(host='0.0.0.0', port=8000)