from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw
import io

app = Flask(__name__)

def generate_pixel_grid(canvas_size, square_size, background_color, border_color):
    num_squares_x = canvas_size // square_size
    num_squares_y = canvas_size // square_size
    
    img = Image.new("RGB", (canvas_size, canvas_size), background_color)
    draw = ImageDraw.Draw(img)
    
    for x in range(num_squares_x):
        for y in range(num_squares_y):
            x0 = x * square_size
            y0 = y * square_size
            x1 = x0 + square_size - 1
            y1 = y0 + square_size - 1
            
            draw.line([(x0, y1), (x1, y1), (x1, y0)], fill=border_color)

    return img

def hex_to_rgb(hex:str)->tuple:
    return tuple(int(hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    canvas_size = int(request.form['canvas_size'])
    square_size = int(request.form['square_size'])
    background_color = hex_to_rgb(request.form['background_color'])
    border_color = hex_to_rgb(request.form['border_color'])

    grid_img = generate_pixel_grid(canvas_size, square_size, background_color, border_color)

    img_io = io.BytesIO()
    grid_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
