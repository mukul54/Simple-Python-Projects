from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import random
import math

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def scale_image(img, target_size, scale_mode):
    """Scale image based on the selected mode."""
    if scale_mode == 'fit':
        return img.resize(target_size, Image.LANCZOS)
    elif scale_mode == 'fill':
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        if img_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
        resized = img.resize((new_width, new_height), Image.LANCZOS)
        result = Image.new('RGB', target_size)
        result.paste(resized, ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2))
        return result
    else:  # 'stretch'
        return img.resize(target_size, Image.LANCZOS)

def create_collage(images, layout, scale_mode, target_size=None):
    if target_size is None:
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        target_size = (max_width, max_height)
    
    scaled_images = [scale_image(img, target_size, scale_mode) for img in images]
    
    if layout == "grid":
        return create_grid_layout(scaled_images)
    elif layout == "horizontal":
        return create_horizontal_layout(scaled_images)
    elif layout == "vertical":
        return create_vertical_layout(scaled_images)
    elif layout == "random":
        return create_random_layout(scaled_images)
    elif layout == "diagonal":
        return create_diagonal_layout(scaled_images)
    elif layout == "circular":
        return create_circular_layout(scaled_images)
    else:
        return create_grid_layout(scaled_images)  # Default to grid layout

def create_grid_layout(images):
    cols = int(math.sqrt(len(images)))
    rows = math.ceil(len(images) / cols)
    
    img_width, img_height = images[0].size
    collage_width = cols * img_width
    collage_height = rows * img_height
    
    collage = Image.new('RGB', (collage_width, collage_height))
    
    for i, img in enumerate(images):
        x = (i % cols) * img_width
        y = (i // cols) * img_height
        collage.paste(img, (x, y))
    
    return collage

def create_horizontal_layout(images):
    img_width, img_height = images[0].size
    collage_width = len(images) * img_width
    collage_height = img_height
    
    collage = Image.new('RGB', (collage_width, collage_height))
    
    for i, img in enumerate(images):
        collage.paste(img, (i * img_width, 0))
    
    return collage

def create_vertical_layout(images):
    img_width, img_height = images[0].size
    collage_width = img_width
    collage_height = len(images) * img_height
    
    collage = Image.new('RGB', (collage_width, collage_height))
    
    for i, img in enumerate(images):
        collage.paste(img, (0, i * img_height))
    
    return collage

def create_random_layout(images):
    img_width, img_height = images[0].size
    canvas_size = int(math.sqrt(len(images))) * max(img_width, img_height)
    collage = Image.new('RGB', (canvas_size, canvas_size))
    
    for img in images:
        max_attempts = 50
        for _ in range(max_attempts):
            x = random.randint(0, canvas_size - img_width)
            y = random.randint(0, canvas_size - img_height)
            box = (x, y, x + img_width, y + img_height)
            crop_area = collage.crop(box)
            if all(min(band) == max(band) == 0 for band in crop_area.split()):
                collage.paste(img, (x, y))
                break
        else:
            collage.paste(img, (x, y))
    
    return collage

def create_diagonal_layout(images):
    img_width, img_height = images[0].size
    collage_width = len(images) * img_width
    collage_height = len(images) * img_height
    
    collage = Image.new('RGB', (collage_width, collage_height))
    
    for i, img in enumerate(images):
        collage.paste(img, (i * img_width, i * img_height))
    
    return collage

def create_circular_layout(images):
    img_width, img_height = images[0].size
    canvas_size = int(math.sqrt(len(images))) * max(img_width, img_height) * 2
    center = canvas_size // 2
    collage = Image.new('RGB', (canvas_size, canvas_size))
    
    radius = min(center - max(img_width, img_height), canvas_size // 3)
    
    for i, img in enumerate(images):
        angle = (2 * math.pi * i) / len(images)
        x = int(center + radius * math.cos(angle) - img_width // 2)
        y = int(center + radius * math.sin(angle) - img_height // 2)
        collage.paste(img, (x, y))
    
    return collage

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return 'No file part'
        files = request.files.getlist('files[]')
        layout = request.form.get('layout', 'grid')
        output_format = request.form.get('output_format', 'jpeg')
        scale_mode = request.form.get('scale_mode', 'fit')
        custom_size = request.form.get('custom_size', '')
        
        images = []
        for file in files:
            if file and allowed_file(file.filename):
                img = Image.open(file).convert('RGB')
                images.append(img)
        
        if len(images) < 2:
            return 'Please upload at least 2 images'
        
        if custom_size:
            try:
                width, height = map(int, custom_size.split('x'))
                target_size = (width, height)
            except ValueError:
                return 'Invalid custom size format. Use WIDTHxHEIGHT (e.g., 800x600)'
        else:
            target_size = None
        
        collage = create_collage(images, layout, scale_mode, target_size)
        
        img_io = io.BytesIO()
        if output_format == 'webp':
            collage.save(img_io, 'WEBP', quality=80)
            mimetype = 'image/webp'
        else:
            collage.save(img_io, 'JPEG', quality=85)
            mimetype = 'image/jpeg'
        img_io.seek(0)
        return send_file(img_io, mimetype=mimetype)

    return '''
    <!doctype html>
    <html>
    <body>
    <h1>Upload images for collage</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="files[]" multiple accept=".png,.jpg,.jpeg,.gif,.webp"><br><br>
        <label for="layout">Layout:</label>
        <select name="layout" id="layout">
            <option value="grid">Grid</option>
            <option value="horizontal">Horizontal</option>
            <option value="vertical">Vertical</option>
            <option value="random">Random</option>
            <option value="diagonal">Diagonal</option>
            <option value="circular">Circular</option>
        </select><br><br>
        <label for="scale_mode">Scaling Mode:</label>
        <select name="scale_mode" id="scale_mode">
            <option value="fit">Fit (maintain aspect ratio)</option>
            <option value="fill">Fill (crop if necessary)</option>
            <option value="stretch">Stretch (ignore aspect ratio)</option>
        </select><br><br>
        <label for="custom_size">Custom Size (optional, format: WIDTHxHEIGHT):</label>
        <input type="text" name="custom_size" id="custom_size" placeholder="e.g., 800x600"><br><br>
        <label for="output_format">Output Format:</label>
        <select name="output_format" id="output_format">
            <option value="jpeg">JPEG</option>
            <option value="webp">WebP</option>
        </select><br><br>
        <input type="submit" value="Create Collage">
    </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)