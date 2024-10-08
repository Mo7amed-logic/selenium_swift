from .page_event import PageEvent,BrowserManager,NextPage
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
        Initiates the crawling process by opening the BrowserManager and handling responses.
        
    open():
        Placeholder method for opening the BrowserManager.
    """
    async def onResponse(self,**arg):
        pass 
    async def crawl(self,**args):
        await super().open()  
        await self.onResponse(**args)
    async def open(self):
        pass
        
# ********************* chrome *****************************
class ChromeBrowser(BrowserManager):
    """
    A class for managing a Chrome BrowserManager instance.
    
    Inherits from the BrowserManager class and provides initialization for Chrome-specific
    options and services.

    Parameters
    ----------
    option : ChromeOption
        The options to configure the Chrome BrowserManager.
    service : ChromeService
        The service to manage the Chrome BrowserManager instance.
    keep_alive : bool, optional
        Whether to keep the BrowserManager session alive (default is False).
    remote_server_url: |None
        example:'http://127.0.0.1:4444/wd/hub' | None
        To use the remote WebDriver, you should have the Selenium server running. To run the server, use this command:
        java -jar selenium-server-standalone-2.x.x.jar
        example:java -jar selenium-server-4.23.1.jar standalone
    """
    def __init__(self,option:ChromeOption,service:ChromeService,keep_alive=False,remote_server_url=None) -> None:
        if not option:option = ChromeOption()
        super().__init__(option,service,keep_alive,remote_server_url)

# ********************* firefoxe ***************************
class FireFoxBrowser(BrowserManager):
    """
    A class for managing a Firefox BrowserManager instance.
    
    Inherits from the BrowserManager class and provides initialization for Firefox-specific
    options and services.

    Parameters
    ----------
    option : FirefoxOption
        The options to configure the Firefox BrowserManager.
    service : FirefoxService
        The service to manage the Firefox BrowserManager instance.
    keep_alive : bool, optional
        Whether to keep the BrowserManager session alive (default is False).
    remote_server_url: 'http://127.0.0.1:4444/wd/hub' | None
        To use the remote WebDriver, you should have the Selenium server running. To run the server, use this command:
        java -jar selenium-server-standalone-2.x.x.jar
        example:java -jar selenium-server-4.23.1.jar standalone
    """
    def __init__(self,option:FirefoxOption,service:FirefoxService,keep_alive=False,remote_server_url=None) -> None:
        if not option:option = FirefoxOption()
        super().__init__(option,service,keep_alive,remote_server_url)

# ********************* edge *******************************
class EdgeBrowser(BrowserManager):
    """
    A class for managing an Edge BrowserManager instance.
    
    Inherits from the BrowserManager class and provides initialization for Edge-specific
    options and services.

    Parameters
    ----------
    option : EdgeOption
        The options to configure the Edge BrowserManager.
    service : EdgeService
        The service to manage the Edge BrowserManager instance.
    keep_alive : bool, optional
        Whether to keep the BrowserManager session alive (default is False).
    remote_server_url: 'http://127.0.0.1:4444/wd/hub' | None
        To use the remote WebDriver, you should have the Selenium server running. To run the server, use this command:
        java -jar selenium-server-standalone-2.x.x.jar
        example:java -jar selenium-server-4.23.1.jar standalone
    """
    def __init__(self,option:EdgeOption,service:EdgeService,keep_alive=False,remote_server_url=None) -> None:
        if not option:option = EdgeOption()
        super().__init__(option,service,keep_alive,remote_server_url)
    
    
    
        