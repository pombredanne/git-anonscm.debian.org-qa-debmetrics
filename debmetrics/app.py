from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def sources():
    return render_template('sources.html')

@app.route('/releases')
def releases():
    return render_template('releases.html')

@app.route('/rc_bugs')
def rc_bugs():
    return render_template('rc_bugs.html')

if __name__ == '__main__':
    app.run()
