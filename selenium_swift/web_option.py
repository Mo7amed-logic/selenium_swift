from selenium import webdriver
from typing import Literal
 
args = Literal[
    '--user-data-dir=...',       # Path to the user data directory to retain browser state (cookies, cache)
    '--headless',                # Run the browser in headless mode (without UI)
    '--no-sandbox',              # Disable the sandbox mode (required for some environments)
    'download.default_directory=...',  # Set default download directory
    '--proxy-server=...',        # Use a proxy server for the browser
    'load-extension=...',        # Load a Chrome extension (used for automation or ad blocking)
    '--blink-settings=imagesEnabled=false', # Disable image loading for faster browsing
    '--disable-css',             # Disable CSS for speed improvements
    '--disable-javascript',      # Disable JavaScript execution
    '--disable-dev-shm-usage',   # Prevent using /dev/shm in Docker environments
    '--disable-gpu',             # Disable GPU usage for headless mode
    '--disable-features=VizDisplayCompositor',  # Improve headless mode performance
    '--blink-settings=imagesEnabled=false',  # (Duplicate, can remove)
    '--disable-infobars',        # Hide the "Chrome is being controlled by automated software" message
    '--incognito',               # Launch the browser in incognito mode for privacy
    '--start-maximized',         # Start browser maximized to avoid viewport issues
    '--disable-extensions',      # Disable all browser extensions
    '--window-size=1920,1080',   # Set custom window size
    '--remote-debugging-port=9222'   # Enable remote debugging for troubleshooting
    
]

class _WebOption:
    def __init__(self,browser:Literal['chrome','edge','firefox'],page_load_strategy:Literal['normal','eager','none']='eager',*args:args) -> None:
        """
        Initialize WebDriver options for the specified browser.

        Args:
            browser: The browser type ('chrome', 'edge', 'firefox').
            page_load_strategy: Strategy for loading pages ('normal', 'eager', 'none').
            args: Additional arguments for configuring the WebDriver.

        Raises:
            ValueError: If an unsupported browser type is specified.
        --user-data-dir=...:

        Definition: Specifies the directory where the user profile data (cookies, local storage, etc.) is stored. This can be used to load a specific user profile or to persist data across sessions.
        \n--headless:

        Definition: Runs the browser in headless mode, which means no GUI is shown. Useful for automated testing or scraping where a graphical interface is not required.
        \n--no-sandbox:

        Definition: Disables the sandboxing feature of the browser, which can be necessary in some environments (like Docker containers) where sandboxing may cause issues. However, this can reduce security.
        \ndownload.default_directory=...:

        Definition: Sets the default directory for downloaded files. This option is specific to the Chrome and Edge browsers and is used to specify where files should be saved automatically.
        \n--proxy-server=...:

        Definition: Specifies a proxy server for the browser to use. This is useful for routing traffic through a proxy or for bypassing geographical restrictions.
        \nload-extension=...:

        Definition: Loads a browser extension from the specified directory. This can be used to add custom functionality to the browser during automation.
        \n--blink-settings=imagesEnabled=false:

        Definition: Disables image loading in the browser, which can speed up page loading times and reduce bandwidth usage. This is particularly useful for web scraping.
        \n--disable-css:

        Definition: Disables the loading of CSS files. This can help speed up page loading times, but may result in pages being rendered incorrectly.
        \n--disable-javascript:

        Definition: Disables JavaScript execution in the browser. This can be useful for scenarios where JavaScript execution is not required or could interfere with automation tasks.
        \n--disable-dev-shm-usage:

        Definition: Disables the use of /dev/shm for shared memory in Linux environments. This option can help avoid issues related to shared memory limitations in certain environments.
        \n--disable-gpu:

        Definition: Disables GPU hardware acceleration. This can be useful if there are issues related to GPU rendering or if you are running in an environment without a GPU.
        \n--disable-features=VizDisplayCompositor:

        Definition: Disables specific browser features, in this case, the VizDisplayCompositor. This can be used to bypass certain rendering issues or improve performance.
        \n--blink-settings=imagesEnabled=false:

        Definition: (Duplicate of the earlier argument) Disables image loading to speed up browsing.
        \n--window-size=1920,1080:
        Definition:Set custom window size

        \n--remote-debugging-port=9222:
        Definition:Enable remote debugging for troubleshooting

        \n--start-maximized
        Definition:Start browser maximized to avoid viewport issues

        \n--incognito
        Definition:Launch the browser in incognito mode for privacy

        \n--disable-infobars
        Definition:Hide the "Chrome is being controlled by automated software" message
        """
        def __addArg(arg:args):
            if  'download.default_directory' in arg:
                download_dir = arg[arg.index('=')+1:]
                if self.browser in ['chrome', 'edge']:
                    self.options.add_experimental_option('prefs',{
                        "download.default_directory": download_dir,
                        "download.prompt_for_download": False,
                        "download.directory_upgrade": True,
                        "safebrowsing.enabled": True
                    })
                else:
                    profile = webdriver.FirefoxProfile()
                    profile.set_preference("browser.download.dir", download_dir)
                    profile.set_preference("browser.download.folderList", 2)  # Use custom download directory
                    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # Adjust as needed
            else:
                self.options.add_argument(arg)
            return self 
        self.browser = browser
        if browser == 'chrome':self.options = webdriver.ChromeOptions()
        if browser == 'edge': self.options = webdriver.EdgeOptions()
        if browser == 'firefox':self.options = webdriver.FirefoxOptions()
        for arg in args:
            __addArg(arg)
        self.options.page_load_strategy = page_load_strategy 

 
# ******************* Chrome **********************
class ChromeOption(_WebOption):
    def __init__(self,*args:args,page_load_strategy:Literal['normal','eager','none']='eager') -> None:
        super().__init__('chrome',page_load_strategy,*args)

# ******************* Firefox **********************
class FirefoxOption(_WebOption):
    def __init__(self,*args:args,page_load_strategy:Literal['normal','eager','none']='eager') -> None:
        super().__init__('firefox',page_load_strategy,*args)
 
# ******************* Edge **********************
class EdgeOption(_WebOption):
    def __init__(self,*args:args,page_load_strategy:Literal['normal','eager','none']='eager') -> None:
        super().__init__('edge',page_load_strategy,*args)
 


        
    
        
     