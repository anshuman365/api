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

# Handle text input from Mobile B
@socketio.on("text_input")
def handle_text_input(data):
    # Broadcast text input to all connected clients
    emit("update_text", data, broadcast=True)

# Handle sketch data from Mobile B
@socketio.on("sketch_data")
def handle_sketch_data(data):
    # Broadcast sketch data to all connected clients
    emit("sketch_update", data, broadcast=True)

if __name__ == "__main__":
    print("Starting the server")
    socketio.run(app, host="0.0.0.0", port=9000)