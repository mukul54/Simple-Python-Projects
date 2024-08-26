import qrcode
import sys
import os

def generate_qr_code(data, output_path="qr_code.png"):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the image
    qr_image.save(output_path)
    print(f"QR code saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "qr_code.png"
        generate_qr_code(data, output_path)
    else:
        print("Please provide a string to encode as a QR code.")
        print("Usage: python script_name.py 'Your string here' [output_path]")

