from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')
CORS(app)

# Route for Monitor (Mobile A)
@app.route("/monitor")
def monitor():
    return render_template("monitor.html")

# Route for Keyboard (Mobile B)
@app.route("/keyboard")
def keyboard():
    return render_template("keyboard.html")

# Handle real-time text input from Mobile B
@socketio.on("text_input")
def handle_text_input(data):
    emit("update_text", data, broadcast=True)

# Handle real-time sketch data from Mobile B
@socketio.on("sketch_data")
def handle_sketch_data(data):
    emit("update_sketch", data, broadcast=True)

# Handle canvas clearing signal
@socketio.on("clear_canvas")
def handle_clear_canvas():
    emit("clear_canvas", broadcast=True)

if __name__ == "__main__":
    print("Starting the server")
    socketio.run(app, host="0.0.0.0", port=9000)