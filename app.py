from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/recommend')
def recommend():
   return render_template('recommend.html')

@app.route('/scadule')
def scadule():
   return render_template('scadule.html')

@app.route('/showing')
def showing():
   return render_template('showing.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)