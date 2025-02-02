import pandas as pd
from flask import Flask, render_template

# Initialise the Flask application
app = Flask(__name__)

# Definf the route for the homepage
@app.route("/")
def index():
    #Read the CSV file
    df = pd.read_csv("vacancies.csv")

    # Convert the DataFrame to a list of dictionaries
    apprenticeships = df.to_dict(orient="records")

    # Pass the apprenticeship data to the template
    return render_template("index.html", apprenticeships=apprenticeships) # Render the index.html template

if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode