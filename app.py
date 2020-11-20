from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/essay-editing')
def essay_editing():
    return render_template('essay-editing.html')\

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/our-team')
def our_team():
    return render_template('our-team.html')

@app.route('/join-us')
def join_us():
    return render_template('join-us.html')

if __name__ == '__main__':
    app.run(debug=True)