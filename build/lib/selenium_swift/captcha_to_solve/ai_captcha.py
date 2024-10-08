import importlib
def check_required_libraries(libraries):
    """
    Check if the required libraries are installed.
    
    Parameters:
        libraries (dict): A dictionary where keys are library names and values are installation commands.
        
    Returns:
        None
    """
    isAll = True
    for library, install_command in libraries.items():
        try:
            importlib.import_module(library)
        except :
            print(f"{library} is not installed. Please run: {install_command}")
            isAll = False
    if not isAll:
        raise ImportError('Required libraries are missing.')

# Define required libraries and their installation commands
required_libraries = {
    'pytesseract': 'pip install pytesseract',
    'cv2': 'pip install opencv-python',
    'requests': 'pip install requests',
    'numpy': 'pip install numpy'
}
try:
    from io import BytesIO
    import aiohttp  # Make sure to import aiohttp
    import os
    import base64
    import cv2
    import pytesseract
    import numpy as np
except:
    check_required_libraries(required_libraries)
     

async def solve_image_captcha(captcha_image: str, timeout: int = 10) -> str:
    
    """
    Solve a CAPTCHA using Tesseract OCR.
    
    Parameters:
        captcha_image: Image as base64 string, URL of the image, or file path of the image.
        timeout: The timeout for the HTTP request, in seconds.
    
    Returns:
        The solved CAPTCHA text.
    """
    
    # Determine the type of input and prepare the image data for processing
    if captcha_image.startswith('http://') or captcha_image.startswith('https://'):
        # Image is a URL
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(captcha_image, timeout=timeout) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download image from URL: {captcha_image}")
                    image_data = await response.read()  # Read response data
                    captcha_image_data = BytesIO(image_data)
                    captcha_image_np = cv2.imdecode(np.frombuffer(captcha_image_data.read(), np.uint8), cv2.IMREAD_COLOR)
            except aiohttp.ClientError as e:
                raise Exception(f"Error while fetching image from URL: {e}")
    elif os.path.isfile(captcha_image):
        # Image is a file path
        captcha_image_np = cv2.imread(captcha_image)
        if captcha_image_np is None:
            raise Exception(f"Failed to read image from file: {captcha_image}")
    else:
        # Image is assumed to be a base64 string
        captcha_image_base64 = captcha_image.replace('data:image/png;base64,', '')
        captcha_image_data = base64.b64decode(captcha_image_base64)
        captcha_image_np = cv2.imdecode(np.frombuffer(captcha_image_data, np.uint8), cv2.IMREAD_COLOR)
        if captcha_image_np is None:
            raise Exception("Failed to decode base64 image.")

    # Use Tesseract to solve the CAPTCHA
    captcha_text = pytesseract.image_to_string(captcha_image_np, config='--psm 6')

    return captcha_text  # Return the solved CAPTCHA text
