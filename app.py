from flask import Flask, render_template, request, send_from_directory
import torch
from diffusers import StableDiffusionPipeline
import os
from datetime import datetime
from PIL import Image

app = Flask(__name__)

# Directory for storing images
IMAGE_FOLDER = "static/generated_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Load Stable Diffusion model (Choose best version for Render)
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "runwayml/stable-diffusion-v1-5"  # Lighter model for better speed
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.to(device)

def generate_image(prompt):
    """Generate and save an image based on the prompt."""
    image = pipe(prompt).images[0]  
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(IMAGE_FOLDER, filename)
    image.save(filepath)
    return filename

@app.route("/", methods=["GET", "POST"])
def home():
    """Render homepage & handle image generation."""
    if request.method == "POST":
        prompt = request.form["prompt"]
        filename = generate_image(prompt)
        return render_template("index.html", image_url=f"/static/generated_images/{filename}", prompt=prompt)
    
    return render_template("index.html", image_url=None)

# Serve static images
@app.route('/static/generated_images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    app.run(host="0.0.0.0", port=port)
