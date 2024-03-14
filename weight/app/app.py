from flask import Flask
from config import Config
from database import db
from routes import weight, health

# Create the Flask application instance
app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(weight.weight_blueprint)
app.register_blueprint(health.health_blueprint)

# Define a route for the root URL ("/") to return "Hello, World!"
@app.route('/')
def hello_world():
    return 'Hello, World!'

db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(debug=True)
