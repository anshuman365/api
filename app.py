from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/location_db_1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the database model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('track.html')

@app.route('/track', methods=['POST'])
def track_location():
    # Receive latitude and longitude from the frontend
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude and longitude:
        # Save location to the database
        new_location = Location(latitude=latitude, longitude=longitude)
        db.session.add(new_location)
        db.session.commit()

        return jsonify({"message": "Location tracked and saved successfully!"}), 200
    else:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

@app.route('/view-locations')
def view_locations():
    # Retrieve all locations from the database
    locations = Location.query.all()
    data = [
        {"id": loc.id, "latitude": loc.latitude, "longitude": loc.longitude, "timestamp": loc.timestamp}
        for loc in locations
    ]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
