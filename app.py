from flask import Flask, request, render_template
import numpy as np
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the saved model and scaler
ridge_model= pickle.load(open('D:/ML_project/Final_project_ML/Model/ridge.pkl','rb'))

scaler = pickle.load(open('D:/ML_project/Final_project_ML/Model/scaler.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        # If GET request, show the form
        return render_template('home.html', result=None)
    
    if request.method == 'POST':
        try:
            # Collecting data from form
            features = [
                float(request.form['Temperature']),
                float(request.form['RH']),
                float(request.form['Ws']),
                float(request.form['Rain']),
                float(request.form['FFMC']),
                float(request.form['DMC']),
                float(request.form['ISI']),
                int(request.form['Classes']),
                int(request.form['Region'])
            ]

            # Scaling input
            scaled_features = scaler.transform([features])

            # Predict using model
            prediction = ridge_model.predict(scaled_features)[0]
            result = "Fire" if prediction == 1 else "Not Fire"

        except KeyError as e:
            # Handle missing form keys
            result = f"Error: Missing input for {str(e)}"
        except ValueError:
            # Handle invalid form values
            result = "Error: Invalid input. Please check the entered values."
        except Exception as e:
            # General error handler
            result = f"An error occurred: {str(e)}"
        


        return render_template('single_prediction.html', result=result)
    
    
if __name__ == '__main__':
    app.run(debug=True)