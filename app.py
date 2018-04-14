# import the Flask class from the flask module
from flask import Flask, render_template

# create the application object
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"  

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)