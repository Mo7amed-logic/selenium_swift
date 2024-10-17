import aiohttp
import asyncio
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
    
    Raises:
        Exception: If the CAPTCHA submission or retrieval fails.
    """
    async def download_image(image_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                response.raise_for_status()  # Raise error for HTTP errors
                return await response.read()

    async def get_captcha_result(session: aiohttp.ClientSession, captcha_id: str) -> str:
        while True:
            await asyncio.sleep(5)
            async with session.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1") as response:
                response_json = await response.json()
                if response_json['status'] == 1:
                    return response_json['request']
                if response_json['request'] != 'CAPCHA_NOT_READY':
                    raise Exception(f"Error retrieving CAPTCHA result: {response_json['request']}")

    # Prepare the CAPTCHA image data
    if captcha_image.startswith(('http://', 'https://')):
        captcha_image_data = await download_image(captcha_image)
    elif os.path.isfile(captcha_image):
        with open(captcha_image, 'rb') as img_file:
            captcha_image_data = img_file.read()
    else:
        captcha_image_data = base64.b64decode(captcha_image.replace('data:image/png;base64,', ''))

    # Submit image to 2Captcha
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://2captcha.com/in.php",
            data={
                'key': api_key,
                'method': 'base64',
                'body': base64.b64encode(captcha_image_data).decode('utf-8'),
                'json': 1
            }
        ) as response:
            captcha_response = await response.json()
            if captcha_response.get('status') != 1:
                raise Exception(f"Error submitting CAPTCHA: {captcha_response.get('request')}")
            captcha_id = captcha_response.get('request')

        # Poll for the result
        return await get_captcha_result(session, captcha_id)
