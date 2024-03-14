from flask import Flask

# Create the Flask application instance
backend = Flask(__name__)

# Define a route for the root URL ("/") to return "Hello, World!"
@backend.route('/')
def hello_world():
    return 'Hello, World!'

# Check if the run.py script is executed directly (and not imported) and then run the app
if __name__ == '__main__':
    backend.run(debug=True)