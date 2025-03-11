import numpy as np
from PIL import Image

def load_bmp_as_array(image_path: str):
    """
    Loads a grayscale BMP image as a NumPy array using PIL.

    :param image_path: Path to the BMP file.
    :return: (Header bytes, NumPy array of image data).
    """
    with open(image_path, "rb") as f:
        header = f.read(54)  # Read the BMP header

    # Load image using PIL
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    image_array = np.array(image, dtype=np.uint8)  # Convert to NumPy array

    return header, image_array

def save_array_as_bmp(image_array: np.ndarray, header: bytes, save_path: str):
    """
    Saves a NumPy array as a BMP file using PIL.

    :param image_array: NumPy array of pixel values.
    :param header: The original BMP header (not used, kept for compatibility).
    :param save_path: Path to save the BMP file.
    """
    image = Image.fromarray(image_array)  # Convert back to PIL image
    image.save(save_path, format="BMP")  # Save as BMP

def pixel_wise_average(image_arrays: list) -> np.ndarray:
    """
    Computes the pixel-wise average of a list of images.

    :param image_arrays: List of NumPy arrays representing images.
    :return: Averaged NumPy array.
    """
    if not image_arrays:
        raise ValueError("No images provided for averaging.")

    stacked_images = np.stack(image_arrays, axis=0)
    return np.mean(stacked_images, axis=0).astype(np.uint8)  # Compute mean pixel-wise
