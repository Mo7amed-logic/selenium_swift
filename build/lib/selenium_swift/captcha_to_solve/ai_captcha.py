import importlib
from io import BytesIO
import aiohttp
import os
import base64
import cv2
import pytesseract
import numpy as np

def check_required_libraries(libraries):
    """
    Check if the required libraries are installed.
    
    Parameters:
        libraries (dict): A dictionary where keys are library names and values are installation commands.
        
    Raises:
        ImportError: If any required libraries are missing.
    """
    is_all_installed = True
    for library, install_command in libraries.items():
        try:
            importlib.import_module(library)
        except ImportError:
            print(f"{library} is not installed. Please run: {install_command}")
            is_all_installed = False
    if not is_all_installed:
        raise ImportError('Required libraries are missing.')

# Define required libraries and their installation commands
required_libraries = {
    'pytesseract': 'pip install pytesseract',
    'opencv-python': 'pip install opencv-python',
    'numpy': 'pip install numpy'
}

try:
    check_required_libraries(required_libraries)
except ImportError as e:
    print(e)

async def solve_image_captcha(captcha_image: str, timeout: int = 10) -> str:
    """
    Solve a CAPTCHA using Tesseract OCR.
    
    Parameters:
        captcha_image: Image as base64 string, URL of the image, or file path of the image.
        timeout: The timeout for the HTTP request, in seconds.
    
    Returns:
        The solved CAPTCHA text.
    
    Raises:
        Exception: If the CAPTCHA cannot be solved.
    """
    
    async def download_image(image_url: str) -> np.ndarray:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, timeout=timeout) as response:
                response.raise_for_status()  # Raise error for HTTP errors
                image_data = await response.read()
                return cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

    # Determine the type of input and prepare the image data for processing
    if captcha_image.startswith(('http://', 'https://')):
        captcha_image_np = await download_image(captcha_image)
    elif os.path.isfile(captcha_image):
        captcha_image_np = cv2.imread(captcha_image)
        if captcha_image_np is None:
            raise Exception(f"Failed to read image from file: {captcha_image}")
    else:
        captcha_image_base64 = captcha_image.replace('data:image/png;base64,', '')
        captcha_image_data = base64.b64decode(captcha_image_base64)
        captcha_image_np = cv2.imdecode(np.frombuffer(captcha_image_data, np.uint8), cv2.IMREAD_COLOR)
        if captcha_image_np is None:
            raise Exception("Failed to decode base64 image.")

    # Use Tesseract to solve the CAPTCHA
    captcha_text = pytesseract.image_to_string(captcha_image_np, config='--psm 6')

    return captcha_text  # Return the solved CAPTCHA text
