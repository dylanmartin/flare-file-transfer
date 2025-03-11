import os
from PIL import Image
import sys

def resize_and_convert_to_bmp(input_folder: str, output_folder: str, size=(512, 512)):
    """
    Resizes all images in the input folder to 512x512 and converts them to BMP format,
    saving them in the output folder.

    :param input_folder: Path to the folder containing images to resize.
    :param output_folder: Path to save the resized BMP images.
    :param size: Target size (default is 512x512).
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each image file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Check if the file is an image
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif", ".webp")):
            try:
                with Image.open(input_path) as img:
                    resized_img = img.resize(size, Image.LANCZOS)  # Resize to 512x512
                    
                    # Convert filename to .bmp format
                    bmp_filename = os.path.splitext(filename)[0] + ".bmp"
                    output_path = os.path.join(output_folder, bmp_filename)
                    
                    # Save as BMP
                    resized_img.convert("RGB").save(output_path, format="BMP")
                    print(f"Converted: {filename} -> {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python batch_resize_to_bmp.py <input_folder> <output_folder>")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        resize_and_convert_to_bmp(input_folder, output_folder)
