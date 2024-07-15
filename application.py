# Import necessary libraries and modules
from flask import Flask, request, render_template

# Initialize Flask application
application = Flask(__name__)

# Alias for the Flask application
app = application

# Route for the home page
@app.route('/')
def index():
    """
    Render the home page.
    """
    return render_template('index.html')

# Main entry point for running the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0")