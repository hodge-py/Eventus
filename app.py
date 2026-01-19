import os
import mysql.connector
import uuid
from flask import Flask, render_template, request, jsonify
import smtplib
import ssl
from email.message import EmailMessage
from nanoid import generate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from pathlib import Path
from werkzeug.utils import secure_filename


app = Flask(__name__)

host=os.getenv('DB_HOST')
user=os.getenv('MARIADB_USER')
password=os.getenv('MARIADB_PASSWORD')
database=os.getenv('MARIADB_DATABASE')
root_pass = os.getenv('MARIADB_ROOT_PASSWORD')
port = os.getenv("PORT")
database_port = os.getenv("DB_PORT")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mariadb+mariadbconnector://{user}:{password}@{host}:{database_port}/{database}"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 3600}

directory = Path('uploads')

directory.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = directory

db = SQLAlchemy(app)

def generate_slug():
    return generate(size=14)

class LinkPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    admin_slug = db.Column(db.String(15), nullable=False, unique=True, default=generate_slug)
    public_slug = db.Column(db.String(15), nullable=False, unique=True, default=generate_slug)

    email = db.Column(db.String(100),nullable=False)

    title = db.Column(db.String(100))

    imageName = db.Column(db.String(200))

    startTime = db.Column(db.DateTime)

    endTime = db.Column(db.DateTime)

    description = db.Column(db.String(10000))
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    """
    def __repr__(self):
        return f'{self.email}'
    """


@app.route('/')
def index():
    try:
        return render_template('index.html',message="connected to db")
    except Exception as e:
        return f"Error connecting to database: {str(e)}"
    

@app.route('/emailSent', methods=['GET','POST'])
def email():
    try:
        if request.method == 'POST':
            data = request.get_json()
            receiver_email = data['email']
            new_event = LinkPair(email=receiver_email)
            db.session.add(new_event)
            db.session.commit()
            
            # Generate full links only when showing them to the user
            admin_url = f"{request.host_url}admin/{new_event.admin_slug}"
            public_url = f"{request.host_url}view/{new_event.public_slug}"
            
            #return {"admin": admin_url, "public": public_url}

            
            sender_email = "eventus1188@gmail.com"
            print(receiver_email)
            password = "ygba fufj nnee vjmz"

            msg = EmailMessage()
            msg.set_content(f"""
                            Here are the links for accessing your event.
                            Admin: {admin_url} 
                            Public: {public_url}
                            Thanks for using Eventus!
                            """)
            msg['Subject'] = "Eventus Links"
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
        return jsonify("failure")


@app.route('/admin/<slug>')
def admin_dashboard(slug):
    stmt = db.select(LinkPair).where(LinkPair.admin_slug == slug)
    event = db.session.execute(stmt).scalar_one()
    hold = {"email": event.email, "public_slug": event.public_slug, 
            "created_at": event.created_at, "description":event.description, 'title': event.title, 
            'fileName':event.imageName}
    
    return render_template('admin.html', event=hold)

@app.route('/view/<slug>')
def view_dashboard(slug):

    stmt = db.select(LinkPair).where(LinkPair.public_slug == slug)
    event = db.session.execute(stmt).scalar_one()
    pathDir = Path(f"uploads/{event.imageName}")
    hold = {"email": event.email, "public_slug": event.public_slug, 
            "created_at": event.created_at, "description":event.description,
            "title": event.title, 'fileName': pathDir, 'startTime': event.startTime, 'endTime': event.endTime}
    
    return render_template('main.html', event=hold)


@app.route('/admin/titleSave', methods=["POST"])
def save_title():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        
            if 'title' in data:
                stmt = db.update(LinkPair).where(LinkPair.admin_slug == data['secret']).values(title=data['title'])

                db.session.execute(stmt)

                db.session.commit()

            elif 'description' in data:
                stmt = db.update(LinkPair).where(LinkPair.admin_slug == data['secret']).values(description=data['description'])

                db.session.execute(stmt)

                db.session.commit()

            elif 'start' in data:
                stmt = db.update(LinkPair).where(LinkPair.admin_slug == data['secret']).values({LinkPair.startTime:data['start'],LinkPair.endTime:data['end']})

                db.session.execute(stmt)

                db.session.commit()

        else:
            dataFile = request.files
            if 'file' in dataFile:
                filename2 = secure_filename(uuid.uuid4().hex + dataFile['file'].filename)

                stmt = db.update(LinkPair).where(LinkPair.admin_slug == request.form.get('secret')).values(imageName=filename2)

                db.session.execute(stmt)

                db.session.commit()

                directory_path = Path(f"static/uploads")

                directory_path.mkdir(parents=True, exist_ok=True)

                newPath = Path(f"static/uploads/{filename2}")

                dataFile['file'].save(newPath)





    return jsonify({"test":"hey"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=True)