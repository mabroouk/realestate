
from flask import Flask, render_template, request, redirect, session, flash
from flask_mail import Mail, Message
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# إعداد البريد
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

mail = Mail(app)

users = {
    'mabroouk@hotmail.com': {
        'password': 'Ahmed0555156740*',
        'role': 'admin',
        'redirect': 'dashboard'
    },
    'owner1@building.com': {
        'password': 'ownerpass123',
        'role': 'owner',
        'redirect': 'owner_building1'
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)

        if user and user['password'] == password:
            # Get IP and location
            try:
                location = requests.get('https://ipapi.co/json/').json()
                ip = location['ip']
                loc = f"{location['city']}, {location['country_name']}"

                msg = Message(subject='🚨 محاولة دخول',
                              sender=app.config['MAIL_USERNAME'],
                              recipients=['mabroouk@hotmail.com'],
                              body=f"محاولة دخول جديدة:\nالبريد: {email}\nIP: {ip}\nالموقع: {loc}")
                mail.send(msg)
            except Exception as e:
                print('فشل إرسال البريد:', e)

            session['email'] = email
            return redirect(f"/{user['redirect']}")
        else:
            flash('بيانات الدخول غير صحيحة')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session.get('email') != 'mabroouk@hotmail.com':
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/owner_building1')
def owner_building1():
    if session.get('email') != 'owner1@building.com':
        return redirect('/')
    return render_template('owner_building1.html')

if __name__ == '__main__':
    app.run(debug=True)
