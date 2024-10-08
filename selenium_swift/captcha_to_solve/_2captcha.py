import aiohttp  # Use aiohttp for asynchronous requests
from selenium_swift.page_event import Element
import asyncio  # Required for sleep and async operations
import base64
import os

async def solve_image_captcha(api_key: str, captcha_image: str) -> str:
    """
    Solve a CAPTCHA using the 2Captcha service.
    
    Parameters:
        api_key: Your 2Captcha API key.
        captcha_image: Image as base64 string, URL of the image, or file path of the image.
    
    Returns:
        The solved CAPTCHA text.
    """
    # Determine the type of input and prepare the image data for submission
    if captcha_image.startswith('http://') or captcha_image.startswith('https://'):
        # Image is a URL
        async with aiohttp.ClientSession() as session:
            async with session.get(captcha_image) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download image from URL: {captcha_image}")
                captcha_image_data = await response.read()
                captcha_image_base64 = base64.b64encode(captcha_image_data).decode('utf-8')
    elif os.path.isfile(captcha_image):
        # Image is a file path
        with open(captcha_image, 'rb') as img_file:
            captcha_image_data = img_file.read()
            captcha_image_base64 = base64.b64encode(captcha_image_data).decode('utf-8')
    else:
        # Image is assumed to be a base64 string
        captcha_image_base64 = captcha_image.replace('data:image/png;base64,', '')  # Remove header if present

    # Submit image to 2Captcha
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://2captcha.com/in.php",
            data={
                'key': api_key,
                'method': 'base64',
                'body': captcha_image_base64,
                'json': 1
            }
        ) as response:
            captcha_response = await response.json()
            if captcha_response.get('status') != 1:
                raise Exception(f"Error submitting CAPTCHA: {captcha_response.get('request')}")

            captcha_id = captcha_response.get('request')

    # Poll for the result
    result = None
    while result is None:
        await asyncio.sleep(5)
        async with session.get(
            f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1"
        ) as response:
            response_json = await response.json()
            if response_json['status'] == 1:
                result = response_json['request']
            elif response_json['request'] != 'CAPCHA_NOT_READY':
                raise Exception(f"Error retrieving CAPTCHA result: {response_json['request']}")

    return result  # Return the CAPTCHA solution
