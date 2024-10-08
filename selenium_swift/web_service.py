from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirfox
from selenium.webdriver.edge.service import Service as ServiceEdge
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import Literal

from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.edge.service import Service as ServiceEdge
from selenium.webdriver.firefox.service import Service as ServiceFirfox
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import Literal

class WebService:
    def __init__(self, BrowserManager: Literal['chrome', 'edge', 'firefox'] = 'chrome', executable_path=None) -> None:
        """
        Initialize WebService for the specified BrowserManager.

        Args:
            BrowserManager: The BrowserManager type ('chrome', 'edge', 'firefox').
            executable_path: The path to the BrowserManager driver executable. 
                If not provided, WebDriverManager installs the driver automatically.

        Raises:
            ValueError: If an unsupported BrowserManager type is specified.
        """
        def show_message(executable_path):
            print('************************************')
            print('You can copy this path and save it to use it again...')
            print('executable_path: ', executable_path)
            print('Save this path to avoid reinstalling until it no longer works, then use install for a newer version.')
            print('************************************')
        if BrowserManager == 'chrome':
            if not executable_path:
                executable_path = ChromeDriverManager().install()
                show_message(executable_path)
            self.service = ServiceChrome(executable_path=executable_path)

        if BrowserManager == 'edge':
            if not executable_path:
                executable_path = EdgeChromiumDriverManager().install()
                show_message(executable_path)
            self.service = ServiceEdge(executable_path=executable_path)

        if BrowserManager == 'firefox':
            if not executable_path:
                executable_path = GeckoDriverManager().install()
                show_message(executable_path)
            self.service = ServiceFirfox(executable_path=executable_path)



# ******************* Chrome **********************
class ChromeService(WebService):
    def __init__(self, executable_path=None) -> None:
        super().__init__('chrome', executable_path)

# ******************* Firefox **********************
class FirefoxService(WebService):
    def __init__(self, executable_path=None) -> None:
        super().__init__('firefox', executable_path)

# ******************* Edge **********************
class EdgeService(WebService):
    def __init__(self, executable_path=None) -> None:
        super().__init__('edge', executable_path)

