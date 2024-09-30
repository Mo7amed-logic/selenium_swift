from .page_event import PageEvent,Browser,NextPage
from .web_option import ChromeOption,EdgeOption,FirefoxOption
from .web_service import ChromeService,EdgeService,FirefoxService

from selenium.webdriver.common.keys import Keys
from typing import Literal

class PageScrape(PageEvent):
    """
    A class to handle the scraping of web pages.
    
    Inherits from the PageEvent class to utilize event-driven mechanisms for
    web scraping.

    Methods
    -------
    onResponse(**arg):
        Handles the response from web requests.
        
    crawl(**args):
        Initiates the crawling process by opening the browser and handling responses.
        
    open():
        Placeholder method for opening the browser.
    """
    async def onResponse(self,**arg):
        pass 
    async def crawl(self,**args):
        await super().open()  
        await self.onResponse(**args)
    async def open(self):
        pass
        
# ********************* chrome *****************************
class ChromeBrowser(Browser):
    """
    A class for managing a Chrome browser instance.
    
    Inherits from the Browser class and provides initialization for Chrome-specific
    options and services.

    Parameters
    ----------
    option : ChromeOption
        The options to configure the Chrome browser.
    service : ChromeService
        The service to manage the Chrome browser instance.
    keep_alive : bool, optional
        Whether to keep the browser session alive (default is False).
    isUndetectChromedriver : bool, optional
        Whether to use an undetectable ChromeDriver (default is False).
    """
    def __init__(self,option:ChromeOption,service:ChromeService,keep_alive=False,isUndetectChromedriver=False) -> None:
        if not option:option = ChromeOption()
        super().__init__(option,service,keep_alive,isUndetectChromedriver)

# ********************* firefoxe ***************************
class FireFoxBrowser(Browser):
    """
    A class for managing a Firefox browser instance.
    
    Inherits from the Browser class and provides initialization for Firefox-specific
    options and services.

    Parameters
    ----------
    option : FirefoxOption
        The options to configure the Firefox browser.
    service : FirefoxService
        The service to manage the Firefox browser instance.
    keep_alive : bool, optional
        Whether to keep the browser session alive (default is False).
    """
    def __init__(self,option:FirefoxOption,service:FirefoxService,keep_alive=False) -> None:
        if not option:option = FirefoxOption()
        super().__init__(option,service,keep_alive)

# ********************* edge *******************************
class EdgeBrowser(Browser):
    """
    A class for managing an Edge browser instance.
    
    Inherits from the Browser class and provides initialization for Edge-specific
    options and services.

    Parameters
    ----------
    option : EdgeOption
        The options to configure the Edge browser.
    service : EdgeService
        The service to manage the Edge browser instance.
    keep_alive : bool, optional
        Whether to keep the browser session alive (default is False).
    """
    def __init__(self,option:EdgeOption,service:EdgeService,keep_alive=False) -> None:
        if not option:option = EdgeOption()
        super().__init__(option,service,keep_alive)
    
    
    
        