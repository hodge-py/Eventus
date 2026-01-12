import os
import mysql.connector
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('index.html',message="connected to db")
    except Exception as e:
        return f"Error connecting to database: {str(e)}"
    

@app.route('/event')
def main():
    try:
        return render_template('main.html')
    except Exception as e:
        return f"Error"
    

@app.route('/emailSent', methods=['GET','POST'])
def email():
    try:
        if request.method == 'POST':
            #request = request.get_json()
            print(request)
            return jsonify("hey")
        
    except Exception as e:
        print("hey")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)