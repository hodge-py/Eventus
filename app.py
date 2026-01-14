import os
import mysql.connector
from flask import Flask, render_template, request, jsonify
import smtplib
import ssl
from email.message import EmailMessage

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
            data = request.get_json()
            sender_email = "eventus1188@gmail.com"
            receiver_email = data['email']
            print(receiver_email)
            password = "ygba fufj nnee vjmz"

            msg = EmailMessage()
            msg.set_content("Hello, this is a test email sent from Python in 2026!")
            msg['Subject'] = "Python Email Test"
            msg['From'] = sender_email
            msg['To'] = receiver_email

            context = ssl.create_default_context()

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error: {e}")
            
            return jsonify("hey")
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=True)