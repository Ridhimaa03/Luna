from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/start-streamlit', methods=['POST'])
def start_streamlit():
    subprocess.Popen(['streamlit', 'run', 'main.py'])
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
