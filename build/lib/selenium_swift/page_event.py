from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome,Firefox,Edge
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Literal
from .web_option import _WebOption
from .web_service import WebService
from .element import Element,ElementIter,_ElementHandler,Expect,Select2,Frame,_BY
from .mouse_controller import MouseController
import undetected_chromedriver as uc
import asyncio
from time import time 
import os 
from selenium_swift.alert_handler import AlertHandler
from concurrent.futures import ThreadPoolExecutor

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

class BrowserManager:
    class Browser:pass 
    ACTUAL_DRIVER = None
    @staticmethod
    def __getDriver(options:_WebOption = None, service: WebService = None, keep_alive: bool = True,remote_server_url:str = None):
            browser_name = options.browser_name
            undetect_chrome = options.undetect_chrome if browser_name=="chrome" else None
            options = options.options if options else None
            service = service.service if service else None
            if remote_server_url: return webdriver.Remote(command_executor=remote_server_url,options=options)
            if browser_name == "chrome":
                if undetect_chrome:
                    return uc.Chrome(options=options,service=service, keep_alive=keep_alive)
                return Chrome(options, service, keep_alive)
            elif browser_name == 'firefox':
                return Firefox(service=service,options=options)
            elif browser_name == 'edge':
                return Edge(options=options,service=service) 
        
    def __init__(self,option:_WebOption,service:WebService,keep_alive=False,remote_server_url = None) -> None:
        self._driver = BrowserManager.__getDriver(option,service,keep_alive,remote_server_url)
    
    def __del__(self):
        self.onClose()
    def onClose(self):
        pass 
    @classmethod
    async def startBrowsers(cls,browsers:list['Browser'], mode: Literal['async','parallel'] = 'async', max_workers: int = 2):
        """
        Starts multiple browser instances either concurrently using async or parallel using threads.

        Args:
            browsers (list['Browser']): A list of browser instances to start.
            mode (str): Mode of execution, either 'async' for concurrency or 'parallel' for parallelism. Default is 'async'.
            max_workers (int): Maximum number of workers/threads if 'parallel' mode is selected. Default is 2.
        """
        async def onfinish(tab):
            page = await PageEvent('about:blank').open()
            await tab()
           
        async def __main(browser:'BrowserManager',task:'PageEvent',is_new_tab=False):
            if is_new_tab:
                browser._driver.switch_to.new_window('tab')
            browser._driver.isOpen = False 
            cls.ACTUAL_DRIVER = browser._driver
            await onfinish(task)
        async def gen_main(browser:BrowserManager):
            methods = [getattr(browser, attr) for attr in dir(browser) if callable(getattr(browser, attr)) and attr.startswith('tab')]
            methods = [method for method in methods if asyncio.iscoroutinefunction(method)]
            await asyncio.gather(*(__main(browser,methods[i], is_new_tab = i ) for i in range(len(methods))))
            browser._driver.quit()
        
        async def async_mode():
            await asyncio.gather(*(gen_main(browser) for browser in browsers))

        # Parallel mode: Executes browsers in parallel threads
        async def parallel_mode():
            loop = asyncio.get_running_loop()

            async def run_in_thread(browser):
                return await gen_main(browser)

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                tasks = []
                for b in browsers:
                    # Schedule each browser to run in a separate thread
                    tasks.append(loop.run_in_executor(executor, lambda b=b: asyncio.run(run_in_thread(b))))
                    # Add a delay between starting each browser
                    await asyncio.sleep(1)

                # Await all the tasks after they have been scheduled
                await asyncio.gather(*tasks)
        # Determine which mode to run
        if mode == 'async':
            await async_mode()  # Run concurrently using asyncio
        elif mode == 'parallel':
            await parallel_mode()  # Run in parallel using ThreadPoolExecutor
        else:
            raise ValueError(f"Invalid mode '{mode}'. Choose either 'async' or 'parallel'.")
    
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
        return AlertHandler(BrowserManager.ACTUAL_DRIVER)
        
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
        Opens the specified URL in a new or existing BrowserManager tab.

        Args:
            in_ (Literal['new-tab', 'this-tab']): The tab type to open the URL in.

        Returns:
            PageEvent: The current PageEvent instance.
        """
        if not self.driver:self.driver = BrowserManager.ACTUAL_DRIVER
        if in_ == 'new-tab' and BrowserManager.ACTUAL_DRIVER.isOpen:
            self.driver.switch_to.new_window(in_)
        BrowserManager.ACTUAL_DRIVER.isOpen=True
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
            try:
                index1 = tab['indices'].index(tab['actual_index'])
            except:
                index1 = tab['destroyed_index']
                del tab['destroyed_index']
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
            self.driver = BrowserManager.ACTUAL_DRIVER
        BrowserManager.ACTUAL_DRIVER = self.driver
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
                try:
                    actual_index = window['actual_index']
                    index0 = window['indices'].index(actual_index)
                except:
                    index0 = window['destroyed_index']
                    del window['destroyed_index']
                
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
    async def find_elements(self,by:_BY,value,**args)->ElementIter:
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
    def find_elements_sync(self,by:_BY,value,**args)->ElementIter:
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
    
    def close(self):
        """
        Closes the current tab and switches to the previous one.
        """
        self._focus()
        id = self.driver.current_window_handle
        for window in PageEvent.__WINDOWS:
            if id == window['page_id']:
                PageEvent.__WINDOWS.remove(window)
                break
        self.driver.close()
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:pass
        
    def is_at_bottom(self):
        """
        Checks if the current page is scrolled to the bottom.

        Returns:
            bool: True if at the bottom, False otherwise.
        """
        return self.driver.execute_script("""
            return document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight;
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

    def scroll_by(self, dx, dy):
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
     
    def scroll_to(self,x,y):
        self.driver.execute_script(f"window.scrollTo({x}, {y});")
        return self
    def scroll_x_to(self,x):
        y = self.driver.execute_script("return window.pageYOffset;")
        self.driver.execute_script(f"window.scrollTo({x}, {y});")
        return self
    def scroll_y_to(self,y):
        x = self.driver.execute_script("return window.pageXOffset;")
        self.driver.execute_script(f"window.scrollTo({x}, {y});")
        return self

    def scroll_to_bottom(self):
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
            document.body.scrollTop = 0; // For compatibility with older BrowserManagers
        """)
        return self
    def __del__(self):
        pass
        #print(f"Object '{self.__page_index}' is being destroyed.")
        
        for window in PageEvent.__WINDOWS:
            #print(self.__page_index,window['indices'])
            if self.__page_index in window['indices']:
                if len(window['indices']) == 1:
                    self.close()
                index = window['indices'].index(self.__page_index)
                window['indices'].remove(self.__page_index)
                window['destroyed_index'] = index 
                break
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
    
     

     
    