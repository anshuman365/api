import time
import threading
import subprocess  # Import subprocess here
from sqlalchemy import create_engine, text

# Database configuration
DATABASE_URI = "mysql+pymysql://root:1234@localhost/location_db_1"

# SQLAlchemy Engine
engine = create_engine(DATABASE_URI)

# Variables to track the last known row count
last_row_count = 0

# Alarm function
def play_alarm():
    try:
        # Use mpv to play the alarm sound
        subprocess.run(["mpv", "alarm.mp3"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing sound: {e}")
        
# Function to check the database for new entries
def monitor_database():
    global last_row_count
    while True:
        with engine.connect() as conn:
            # Query to count rows in the table
            result = conn.execute(text("SELECT COUNT(*) FROM location"))
            row_count = result.scalar()

            # Check for new rows
            if row_count > last_row_count:
                last_row_count = row_count
                print("New data found in the table!")
                
                # Play alarm
                play_alarm()

        # Sleep for 5 seconds before checking again
        time.sleep(5)

# Start the database monitoring in a separate thread
def start_monitoring():
    monitor_thread = threading.Thread(target=monitor_database, daemon=True)
    monitor_thread.start()
    print("Started monitoring the database for new data.")

# Flask app for notifications (optional)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "Monitoring is active", "last_row_count": last_row_count})

if __name__ == "__main__":
    # Start monitoring in a separate thread
    start_monitoring()
    
    # Run Flask server for status notifications
    app.run(debug=True, port=6000)