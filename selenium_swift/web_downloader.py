import requests
from PIL import Image
from io import BytesIO
import os
import requests
import mimetypes
def __create_folder(file_path: str):
    """Create the directory for the specified file path if it doesn't exist."""
    folder_path = os.path.dirname(file_path)
    if folder_path and not os.path.exists(folder_path):
        os.makedirs(folder_path)
def download_image(image_url: str, file_path: str) -> bool:
    """Download an image from the given URL and save it to the specified file path."""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_format = image.format.lower()

            if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path += f'.{image_format}'

            __create_folder(file_path)
            image.save(file_path)
            print("Image saved successfully at:", file_path)
            return True
        else:
            print("Failed to load the image. Status code:", response.status_code)
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def download_media(media_url: str, file_path: str) -> bool:
    """Download media (video/audio) from the given URL and save it to the specified file path."""
    try:
        with requests.get(media_url, stream=True) as response:
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                extension = mimetypes.guess_extension(content_type) or ''

                if extension and not file_path.lower().endswith(extension):
                    file_path += extension

                __create_folder(file_path)
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print(f"Media downloaded successfully at: {file_path}")
                return True
            else:
                print("Failed to download media. Status code:", response.status_code)
                return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def download_file(file_url: str, file_path: str) -> bool:
    """Download a file from the given URL and save it to the specified file path."""
    return download_media(file_url, file_path)

if __name__ == "__main__":
    #url = """https://tikcdn.io/ssstik/aHR0cHM6Ly9wMTktcHUtc2lnbi11c2Vhc3Q4LnRpa3Rva2Nkbi11cy5jb20vdG9zLXVzZWFzdDUtaS1waG90b21vZGUtdHgvZDkzZWE4OWFmZDg5NGNmY2I2MzgxNmY2MTM2YWUyZTh+dHBsdi1waG90b21vZGUtaW1hZ2UtdjE6cTcwLndlYnA/ZnJvbT1waG90b21vZGUuQVdFTUVfREVUQUlMJmxrM3M9ZDA1YjE0YmQmbm9uY2U9ODk4NjQmcmVmcmVzaF90b2tlbj0yNTliODNlNzhmYzAyYjFhMTVhNWFiYjYzNGExOGQzMCZ4LWV4cGlyZXM9MTcxNjAxOTIwMCZ4LXNpZ25hdHVyZT1PVWJRQ0dHSjZDemN5Q2NSdUFMJTJCYjJxczVlZyUzRA=="""
    #file_name = r"D:\movie_py\tik_tok_upload_video\videos\video.mp4"
    url="https://m.media-amazon.com/images/S/al-na-9d5791cf-3faf/db6c629d-d3aa-4c19-b201-7c90e84bef20.mp4/mp4_1500Kbs_24fps_48khz_96Kbs_576p.mp4"
    folder_path="./"
    print(download_media(url,folder_path,"vid_0"))

