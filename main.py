
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Create a Flask application
app = Flask(__name__)

# Define the home page route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Define the route to handle submission of requests
@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    deadline = request.form['deadline']
    preferred_time = request.form['preferred_time']

    # Connect to the database and insert the submitted data
    connection = sqlite3.connect('schedule.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO requests (task, deadline, preferred_time) VALUES (?, ?, ?)",
                    (task, deadline, preferred_time))
    connection.commit()
    connection.close()

    return redirect(url_for('home'))

# Define the route to generate the daily schedule
@app.route('/schedule', methods=['GET'])
def schedule():
    # Connect to the database and retrieve the submitted requests
    connection = sqlite3.connect('schedule.db')
    cursor = connection.cursor()
    requests = cursor.execute("SELECT * FROM requests").fetchall()
    connection.close()

    # Generate the daily schedule based on the requests
    schedule = generate_schedule(requests)

    # Render the schedule page with the generated schedule
    return render_template('schedule.html', schedule=schedule)

# Define a helper function to generate the daily schedule
def generate_schedule(requests):
    # Initialize the schedule as an empty list
    schedule = []

    # Sort the requests by their deadlines
    requests.sort(key=lambda request: request[2])

    # Add each request to the schedule, considering the preferred times and travel time
    for request in requests:
        task, deadline, preferred_time = request
        if not schedule:
            schedule.append([task, preferred_time])
        else:
            # Calculate the travel time to the next request
            travel_time = calculate_travel_time(schedule[-1][1], preferred_time)

            # Add the request to the schedule if it doesn't conflict with existing tasks
            if schedule[-1][1] + travel_time <= deadline:
                schedule.append([task, preferred_time])

    return schedule

# Define a helper function to calculate the travel time between two locations
def calculate_travel_time(location1, location2):
    # Placeholder code for calculating travel time
    return 15  # Assuming a fixed 15 minutes of travel time for simplicity

# Define the route to serve the CSS file
@app.route('/style.css', methods=['GET'])
def css():
    return render_template('style.css')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
