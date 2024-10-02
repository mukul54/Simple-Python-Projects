import os
import subprocess

def compress_pdf(input_path, output_path, power=3):
    """
    Compress PDF file using Ghostscript
    :param input_path: Path to input PDF file
    :param output_path: Path to output PDF file
    :param power: 0-4, where 0 is least compressed and 4 is most compressed
    """
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Ghostscript command
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality[power]}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    try:
        # Run Ghostscript
        subprocess.run(gs_command, check=True)
        
        # Calculate compression percentage
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        compression_ratio = (1 - (output_size / input_size)) * 100

        print(f"Compressed PDF saved to {output_path}")
        print(f"Original size: {input_size / 1024:.2f} KB")
        print(f"Compressed size: {output_size / 1024:.2f} KB")
        print(f"Compression ratio: {compression_ratio:.2f}%")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while compressing: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# Example usage
input_file = "/Users/mukul/Desktop/mbzuai/research/t2i/2407_ReCorD.pdf"
output_file = "/Users/mukul/Desktop/mbzuai/research/t2i/2407_ReCorD_compressed.pdf"
compress_pdf(input_file, output_file)