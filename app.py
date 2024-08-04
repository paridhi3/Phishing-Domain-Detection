# Import necessary libraries and modules
from flask import Flask, request, render_template
from src.PDD.pipeline.prediction_pipeline import CustomData, PredictPipeline

# Initialize Flask application
app = Flask(__name__)

# Route for the home and prediction page
@app.route('/', methods=['GET'])
def index():    
    return render_template('index.html')

# Define a separate route for handling predictions
@app.route('/predictdata', methods=['POST'])
def predict_datapoint():
    # Create an instance of CustomData with the form input values entered by user
    # data = CustomData(url = request.form.get('url'))
    data = CustomData.from_url(request.form.get('url'))

    # Convert the input data into a DataFrame
    pred_df = data.get_data_as_data_frame()
    print(pred_df)
    print("Before Prediction")

    # Create an instance of the prediction pipeline
    predict_pipeline = PredictPipeline()
    print("Mid Prediction")
    
    # Perform prediction
    results = predict_pipeline.predict(pred_df)
    print("After Prediction")
    
    # Render the results on the form page
    return render_template('index.html', results=results[0])

# Main entry point for running the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0")