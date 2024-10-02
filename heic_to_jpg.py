import os
from PIL import Image
from pillow_heif import register_heif_opener

def convert_heic_to_jpg(input_path, output_path=None):
    """
    Convert HEIC image to JPG format
    :param input_path: Path to input HEIC file
    :param output_path: Path to output JPG file (optional)
    """
    # Register HEIF opener
    register_heif_opener()

    # If output path is not specified, create one based on input path
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.jpg'

    try:
        # Open the HEIC image
        with Image.open(input_path) as img:
            # Convert to RGB (in case it's in RGBA format)
            img = img.convert('RGB')
            # Save as JPG
            img.save(output_path, 'JPEG')

        print(f"Converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")

def batch_convert_heic_to_jpg(input_directory, output_directory=None):
    """
    Convert all HEIC images in a directory to JPG format
    :param input_directory: Path to directory containing HEIC files
    :param output_directory: Path to directory for output JPG files (optional)
    """
    if output_directory is None:
        output_directory = input_directory

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.heic'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.jpg')
            convert_heic_to_jpg(input_path, output_path)

# Example usage
# For single file conversion
# convert_heic_to_jpg('path/to/your/image.heic')

# For batch conversion
# batch_convert_heic_to_jpg('path/to/your/heic/directory', 'path/to/output/directory')