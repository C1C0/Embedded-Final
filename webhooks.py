from flask import Flask, request, Response
import sqlite3

def setup() -> None:
    """Setup basic webhooks for our application"""
    
    app = Flask(__name__)

    @app.route('/hook/data', methods=['POST'])
    def temperature():
        con = sqlite3.connect('station.db')
        cur = con.cursor()
        
        if request.method == 'POST':
            data = request.json
            
            temperature = 0
            humidity = 0
            pressure = 0
            
            if "temperature" in data:
                print(data['temperature'])
                temperature = float(data['temperature'])
                
                        
            if "humidity" in data:
                print(data['humidity'])
                humidity = float(data['humidity'])
                        
            if "pressure" in data:
                print(data['pressure'])
                pressure = float(data['pressure'])
                
            cur.execute(f'INSERT INTO measurements (temperature, humidity, pressure) VALUES({temperature}, {humidity}, {pressure})')
            con.commit()
            con.close()
            
            return ""

    app.run(host='0.0.0.0', port=8000)
    
if __name__ == '__main__':
    setup()