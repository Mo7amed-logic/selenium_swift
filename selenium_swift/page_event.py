from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome,Firefox,Edge
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Literal
from .web_option import _WebOption
from .web_service import WebService
from .element import Element,_ElementHandler,Expect,Select2,Frame
from .mouse_controller import MouseController
import undetected_chromedriver as uc
import asyncio
from time import time 
import os 
from selenium_swift.alert_handler import AlertHandler
_BY = Literal['css_selector','id','xpath','class','name','link_text','partial_link_text','tag_name']
def normalize_url(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Remove 'www.' from the netloc (domain) if present
    netloc = parsed_url.netloc.lower()
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    # Sort query parameters alphabetically
    query = parse_qs(parsed_url.query)
    sorted_query = urlencode(sorted(query.items()), doseq=True)

    # Rebuild the URL without redundant parts (like the fragment)
    normalized_url = urlunparse((
        parsed_url.scheme,
        netloc,  # Use the netloc without 'www.'
        parsed_url.path.rstrip('/'),  # Remove trailing slashes
        parsed_url.params,
        sorted_query,  # Use sorted query string
        ''  # Ignore fragment
    ))
    return normalized_url

def are_urls_equal(url1, url2):
    return normalize_url(url1) == normalize_url(url2)
class Browser:
    ACTUAL_DRIVER= None
    def __init__(self,option:_WebOption,service:WebService,keep_alive=False,isUndetectChromedriver=False) -> None:
        def __getDriver(options:_WebOption = None, service: WebService = None, keep_alive: bool = True,isUndetectChromedriver=False):
            browser = options.browser
            options = options.options if options else None
            service = service.service if service else None
            if browser == "chrome":
                if isUndetectChromedriver:
                    return uc.Chrome(options=options,service=service, keep_alive=keep_alive)
                return Chrome(options, service, keep_alive)
            elif browser == 'firefox':
                return Firefox(service=service,options=options)
            elif browser == 'edge':
                return Edge(options=options,service=service) 
        self._driver = __getDriver(option,service,keep_alive,isUndetectChromedriver)
    
    @classmethod
    def startBrowsers(cls,browsers:list['Browser']):
        """
        Starts multiple browser instances concurrently.

        Args:
            browsers (list['Browser']): A list of Browser instances to start.
        """
        async def __main(browser:'Browser',task:'PageEvent',is_new_tab=False):
            if is_new_tab:
                browser._driver.switch_to.new_window('tab')
            browser._driver.isOpen = False 
            cls.ACTUAL_DRIVER = browser._driver
            await task()
        async def gen_main(browser:Browser):
            methods = [getattr(browser, attr) for attr in dir(browser) if callable(getattr(browser, attr)) and attr.startswith('tab')]
            methods = [method for method in methods if asyncio.iscoroutinefunction(method)]
             
            await asyncio.gather(*(__main(browser,methods[i], is_new_tab = i ) for i in range(len(methods))))
            browser._driver.quit()
        async def main():
            await asyncio.gather(*(gen_main(browser) for browser in browsers))
        asyncio.run(main())  
    async def get(self,url,in_:Literal['new-tab','this-tab']='this-tab')->'PageEvent':
        """
        Opens a specified URL in a new or existing browser tab.

        Args:
            url (str): The URL to open.
            in_ (Literal['new-tab', 'this-tab']): The tab type to open the URL in.

        Returns:
            PageEvent: An instance of PageEvent for further interactions.
        """
        return await PageEvent(url).open(in_)
    def alert(self):
        """
        Returns an AlertHandler for handling browser alerts.

        Returns:
            AlertHandler: An instance of AlertHandler.
        """
        return AlertHandler(self._driver)

class PageEvent:
    __WINDOWS = []
    __PAGE_INDEX = 0
    __ACTUAL_PAGE_INDEX = -1
    def __init__(self,url) -> None:
        """
        Initializes a new PageEvent instance.

        Args:
            url (str): The URL of the page to interact with.
        """
        self.__page_index = PageEvent.__PAGE_INDEX
        PageEvent.__PAGE_INDEX += 1
        self.url = url 
        self.driver:Chrome = None
        self.iframes = []
        self._timeout = 10
        self.__mouse_controller = None
    def set_implicite_timeout(self,timeout):
        """
        Sets the implicit timeout for the driver.

        Args:
            timeout (int): The timeout duration in seconds.
        """
        self._timeout = timeout
    def alert(self):
        """
        Returns an AlertHandler instance for handling alerts.

        Returns:
            AlertHandler: An instance of AlertHandler.
        """
        if self.driver:
            return AlertHandler(self.driver)
        return AlertHandler(Browser.ACTUAL_DRIVER)
        
    async def wait_for_Download(self,download_path,timeout=60):
        """
        Waits for a download to complete in the specified directory.

        Args:
            download_path (str): The path where downloads are saved.
            timeout (int): The maximum time to wait in seconds.

        Returns:
            bool: True if the download completed, False if it timed out.
        """
        def __is_download_in_progress(download_path):
            files = os.listdir(download_path)
            for file in files:
                # Check for known in-progress download file extensions
                if file.endswith(('.crdownload', '.part', '.tmp')):  # Chrome, Firefox, Edge
                    return True
            return False
        t0 = t1 = time()
        k_check = 0
        n=1
        while (t1-t0) < timeout:
            await asyncio.sleep(0.5)
            print('downloads:please wait'+n*'.',end="\r")
            n += 1
            if n == 10:
                print('downloads:please wait          ',end='\r')
                n=1
            if not __is_download_in_progress(download_path):
                if k_check == 4:
                    print('downloads success...       ')
                    return True
                else:k_check +=1
            t1 = time()
        return False
    
    async def open(self,in_:Literal['new-tab','this-tab']='this-tab'):
        """
        Opens the specified URL in a new or existing browser tab.

        Args:
            in_ (Literal['new-tab', 'this-tab']): The tab type to open the URL in.

        Returns:
            PageEvent: The current PageEvent instance.
        """
        if not self.driver:self.driver = Browser.ACTUAL_DRIVER
        if in_ == 'new-tab' and Browser.ACTUAL_DRIVER.isOpen:
            self.driver.switch_to.new_window(in_)
        Browser.ACTUAL_DRIVER.isOpen=True
        self.driver.get(self.url)
        self._focus()
        await self.sleep(0)
        return self 
    async def sleep(self,seconds):
        """
        Pauses execution for a specified number of seconds.

        Args:
            seconds (int): The duration to sleep in seconds.
        """
        await asyncio.sleep(seconds)
        self._focus()
    
    def _bind(self): 
        self._focus(True) 
        self.driver.switch_to.default_content() 
    def _focus(self,isFromeBind = False): 
        def __gotoPageInTab(tab:dict):
            if tab['page_id'] != self.driver.current_window_handle:
                self.driver.switch_to.window(tab['page_id'])
            index1 = tab['indices'].index(tab['actual_index'])
            index0 = tab['indices'].index(self.__page_index)
            dx = index0 - index1 
            if dx > 0:
                for i in range(dx):self.driver.forward()
                url = None
                while not are_urls_equal(self.driver.current_url,self.url) and url != self.driver.current_url:
                    url = self.driver.current_url
                    self.driver.forward()
                if not are_urls_equal(self.driver.current_url,self.url):
                    self.driver.get(self.url)
            else:
                for i in range(-dx):self.driver.back()
                url = None
                while not are_urls_equal(self.driver.current_url,self.url) and url != self.driver.current_url:
                    url = self.driver.current_url
                    self.driver.back()
                if not are_urls_equal(self.driver.current_url,self.url):
                    self.driver.get(self.url)
            PageEvent.__ACTUAL_PAGE_INDEX = self.__page_index
            
            tab['actual_index'] = self.__page_index    
        if not self.driver :
            self.driver = Browser.ACTUAL_DRIVER
        Browser.ACTUAL_DRIVER = self.driver
        if not isFromeBind:
            isActive = False
            for iframe in self.iframes:
                if iframe.isActive:
                    iframe._reset()
                    isActive = True
                    iframe.isActive = False
            if isActive:self._bind()
        else:return
        if PageEvent.__ACTUAL_PAGE_INDEX != self.__page_index:
            for p in PageEvent.__WINDOWS:
                if self.__page_index in p['indices']:
                    __gotoPageInTab(p)
                    return
        else:return
        id = self.driver.current_window_handle #self.driver.window_handles[-1]
        self.driver.switch_to.window(id)
        PageEvent.__ACTUAL_PAGE_INDEX = self.__page_index
        
        for window in PageEvent.__WINDOWS:
            if id in window['page_id']:
                actual_index = window['actual_index']
                index0 = window['indices'].index(actual_index)
                las_index = len(window['indices'])-1
                dx = las_index-index0
                for i in range(dx):window['indices'].pop()
                window['indices'].append(self.__page_index)
                window['actual_index'] = self.__page_index 
                return 
        PageEvent.__WINDOWS.append({'page_id':id,'indices':[self.__page_index],'actual_index':self.__page_index})
    def focus_to_new_page(self):
        """
        Focuses on the newly opened page.

        Returns:
            NextPage: An instance of NextPage for further interactions.
        """
        
        return NextPage()
    def wait_for(self,by:_BY,value:str,timeout=10):
        """
         Waits for an element of the current page to be present within the specified timeout. 

    Example usage:
        page.wait_for('id', 'inp1', 5).has_attribute('display', 'block')

    Args:
        by (str): The type of locator to search by (e.g., 'id', 'name', 'css_selector', etc.).
        value (str): The value of the locator to identify the target element.
        timeout (int, optional): Maximum wait time in seconds. Defaults to 10.

    Returns:
        Expect: An Expect object, which allows chaining additional conditions like `has_attribute` or `to_be_present`.
        """
        self._focus
        isAsync = timeout > 3
        if isAsync:return Expect(self.find_element(by,value),timeout)
        else:return Expect(lambda:self.find_element_sync(by,value),timeout)
    async def find_element(self,by:_BY,value:str,**args)->Element | Frame | Select2:
        """
        Finds a single element asynchronously.

        Args:
            by (_BY): The method to locate the element.
            value (str): The value used to find the element.

        Returns:
            Element | Frame | Select2: The found element.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':False})
        return await _ElementHandler._async_handler(self,args)
    async def find_elements(self,by:_BY,value,**args)->list[Element]:
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':True})
        return await _ElementHandler._async_handler(self,args)
    def find_element_sync(self,by:_BY,value,**args)->Element:
        """
        Finds a single element synchronously.

        Args:
            by (_BY): The method to locate the element.
            value (str): The value used to find the element.

        Returns:
            Element: The found element.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':False})
        return _ElementHandler._sync_handler(self,args)
    def find_elements_sync(self,by:_BY,value,**args)->list[Element]:
        """
        Finds multiple elements asynchronously.

        Args:
            by (_BY): The method to locate the elements.
            value: The value used to find the elements.

        Returns:
            list[Element]: A list of found elements.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':True})
        return _ElementHandler._sync_handler(self,args) 
    async def close(self):
        """
        Closes the current tab and switches to the previous one.
        """
        self._focus()
        id = self.driver.current_window_handle
        for window in PageEvent.__WINDOWS:
            if id in window['page_id']:
                PageEvent.__WINDOWS.remove(window)
                break
        self.driver.close()
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:pass
        await asyncio.sleep(0)
    def is_at_bottom(self):
        """
        Checks if the current page is scrolled to the bottom.

        Returns:
            bool: True if at the bottom, False otherwise.
        """
        return self.driver.execute_script("""
            return document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight;
        """)

    def is_at_right(self):
        """
        Checks if the current page is scrolled to the right.

        Returns:
            bool: True if at the right, False otherwise.
        """
        return self.driver.execute_script("""
            return document.documentElement.scrollLeft + document.documentElement.clientWidth >= document.documentElement.scrollWidth;
        """)

    def scroll_x_by(self, dx):
        """
        Scrolls the page horizontally by the specified amount.

        Args:
            dx (int): The amount to scroll in the x direction.
        
        Returns:
            PageEvent: The current instance for method chaining.
        """
        self.driver.execute_script(f"document.documentElement.scrollLeft += {dx};")
        return self

    def scroll_y_by(self, dy):
        """
        Scrolls the page vertically by the specified amount.

        Args:
            dy (int): The amount to scroll in the y direction.
        
        Returns:
            PageEvent: The current instance for method chaining.
        """
        
        #self.driver.execute_script(f"document.documentElement.scrollTop += {dy};")
        self.driver.execute_script(f"window.scrollBy(0,{dy});") 
        return self

    def scroll_xy_by(self, dx, dy):
        """
        Scrolls the page by the specified amounts in both x and y directions.

        Args:
            dx (int): The amount to scroll in the x direction.
            dy (int): The amount to scroll in the y direction.
        
        Returns:
            PageEvent: The current instance for method chaining.
        """
        self.driver.execute_script(f"""
            document.documentElement.scrollLeft += {dx};
            document.documentElement.scrollTop += {dy};
        """)
        return self

    def scrollToBottom(self):
        """
        Scrolls to the bottom of the page.

        Returns:
            PageEvent: The current instance for method chaining.
        """
        self.driver.execute_script("""
            document.documentElement.scrollTop = document.documentElement.scrollHeight;
        """)
        return self
    def scroll_to_top(self):
        """
        Scrolls to the top of the page.

        Returns:
            PageEvent: The current instance for method chaining.
        """
        self.driver.execute_script("""
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0; // For compatibility with older browsers
        """)
        return self
    @property
    def mouse(self)->MouseController:
        if not self.__mouse_controller:
            self.__mouse_controller = MouseController(self.driver)
        return self.__mouse_controller 

class NextPage(PageEvent):
    def __init__(self) -> None:
        super().__init__(None)
        self._focus()
    def open(self):
        return self
    
     

     
    