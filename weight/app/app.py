from flask import Flask
from routes.weight import weight_blueprint
# Create the Flask application instance
app = Flask(__name__)

app.register_blueprint(weight_blueprint)
# Define a route for the root URL ("/") to return "Hello, World!"
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Check if the run.py script is executed directly (and not imported) and then run the app

if __name__ == '__main__':
    app.run(debug=True)
