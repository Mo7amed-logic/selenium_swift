import requests
import pkg_resources  # Part of setuptools

__version__ = '0.1.3'  # Current version of your library

def check_for_update():
    try:
        # Assuming your package is hosted on PyPI
        latest_version = requests.get("https://pypi.org/pypi/my_library/json").json()["info"]["version"]

        if pkg_resources.parse_version(__version__) < pkg_resources.parse_version(latest_version):
            print(f"New version available: {latest_version}. Please update your library!")
    except Exception as e:
        print(f"Error checking for updates: {e}")

# Call the function when the library is imported or executed
check_for_update()
