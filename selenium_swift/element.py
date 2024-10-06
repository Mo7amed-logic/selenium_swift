from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from typing import Callable, Coroutine, Union, Any
import asyncio
from typing import Literal
from time import sleep
import re
_BY = Literal['css_selector','id','class','name','link_text','partial_link_text','tag_name']

class _ElementHandler:
    @staticmethod
    def _refresh(element):
        parent_element:Element = element._info['parent_element']
        by = element._info['by']
        value = element._info['value']
        index = element._info['index']
        if index == -1:
            element._info['e'] = (parent_element.find_element_sync(by,value))._info['e']
        else:
            elements = (parent_element.find_elements_sync(by,value))
            element._info['e'] = elements[index]._info['e']
        element._focus()
    @staticmethod
    def _update(element, callback,isRefresh=False):
        element._focus()
        try:
            if isRefresh:_ElementHandler._refresh(element)
            return callback()
        except:
            _ElementHandler._refresh(element)
            return callback()
         
    @staticmethod
    def _try_find(parent_element:WebElement,locator:By,value:str,timeout,condition_wait,k):
        try:page = parent_element._info['page']
        except:page = parent_element
        def get_driver(isCanWebElement=True):
            if not isCanWebElement:
                return page.driver 
            try:driver = parent_element._info['e']
            except:driver = page.driver
            if type(parent_element) == Frame:
                driver = page.driver
            return driver 
        driver = get_driver()
        isAll = condition_wait == EC.presence_of_all_elements_located
        try:
            
            if isAll:
                e = driver.find_elements(locator,value)
                if not e:
                    raise TimeoutError(f"Operation timed out after {timeout} seconds while waiting to find the elements (by='{locator}', value='{value}')") 
            elif condition_wait == EC.presence_of_element_located:
                e = driver.find_element(locator,value)
            else:
                e = condition_wait()
            if e : return e
        except Exception as e :
            if k >= timeout : raise e
            element = _ElementHandler._check_in_shadow_root(driver,get_driver(False),locator,value,isAll)
            if element: return element
            if type(driver) == WebElement and (k % 4 == 0):
                _ElementHandler._refresh(parent_element)
                driver = get_driver()
             
            parent_element._focus()
            return False
    @staticmethod
    def _find_sync(parent_element,locator:By,value:str,timeout,condition_wait,on_try):
        #parent_element._focus()
        k = 0
        
        while True:
            e = _ElementHandler._try_find(parent_element,locator,value,timeout,condition_wait,k)
            if e:return e 
            if on_try:on_try()
            k += 0.5
            sleep(0.5)
    
    @staticmethod
    async def _find_async(parent_element,locator:By,value:str,timeout,condition_wait,on_try):
        #parent_element._focus()
        k = 0
        while True:
            e = _ElementHandler._try_find(parent_element,locator,value,timeout,condition_wait,k)
            if e:return e 
            if on_try:
                on_try()
            k += 0.5
            await asyncio.sleep(0.5)
    @staticmethod
    def _getpredict(page,args,isAll):
        if 'condition_wait' in args : 
            timeOut = args['timeout']
            condition_wait = args['condition_wait']
            on_try = args['on_try']
        else:
            timeOut = page._timeout
            if isAll: condition_wait=EC.presence_of_all_elements_located
            else:condition_wait = EC.presence_of_element_located
            on_try = None
        return timeOut , condition_wait, on_try
    @staticmethod
    def __predictElement(element,parent_element,page,by,value,*d):
        are_all_element = isinstance(element,Element) or type(element) == list and \
                        all(isinstance(item, Element) for item in element)
        if(are_all_element):
            if isinstance(element,Element):return _ElementHandler._convertElement(element)
            else : return [_ElementHandler._convertElement(e) for e in element]
        elif type(element) == list:
            return [_ElementHandler._convertElement(Element(e,parent_element,page,by,value,i,*d)) for i,e in enumerate(element)]
        return _ElementHandler._convertElement(Element(element,parent_element,page,by,value,-1))
    @staticmethod
    async def _async_handler(parent_element,args):
        by,value,isAll = args['by'],args['value'],args['isAll']

        if type(parent_element) == Element or type(parent_element) == Frame:
            page = parent_element._info['page']
        else:page = parent_element
        
        if Element._EXPECT_:
            return Element(None,parent_element,page,by,value,-1)
        else:
            d = _ElementHandler._getpredict(page,args,isAll)
            element = await _ElementHandler._find_async(parent_element,by,value,*d)
            return _ElementHandler.__predictElement(element,parent_element,page,by,value,*d)
            
    @staticmethod
    def _sync_handler(parent_element,args):
        by,value,isAll = args['by'],args['value'],args['isAll']
        if type(parent_element) == Element or type(parent_element) == Frame:
            page = parent_element._info['page']
        else:page = parent_element
        if Element._EXPECT_:
            return Element(None,parent_element,page,by,value,-1)
        else:
            d = _ElementHandler._getpredict(page,args,isAll)
            element = _ElementHandler._find_sync(parent_element,by,value,*d)
            return _ElementHandler.__predictElement(element,parent_element,page,by,value,*d) 
    @staticmethod
    def _getSelector(selector:_BY):
        if selector == "css_selector":return By.CSS_SELECTOR
        if selector == 'xpath':return By.XPATH
        if selector == "id" : return By.ID 
        if selector == 'class': return By.CLASS_NAME
        if selector == 'name': return By.NAME
        if selector == 'link_text':return By.LINK_TEXT
        if selector == 'partial_link_text':return By.PARTIAL_LINK_TEXT
        if selector == 'tag_name':return By.TAG_NAME
        return selector
    @staticmethod
    def __getResverseSelector(selector:By):
        if selector == By.CSS_SELECTOR:return "css_selector"
        if selector == By.XPATH:return "xpath"
        if selector == By.ID:return "id"
        if selector == By.CLASS_NAME:return "class"
        if selector == By.NAME:return "name"
        if selector == By.LINK_TEXT:return "link_text"
        if selector == By.PARTIAL_LINK_TEXT:return "partial_link_text"
        if selector == By.TAG_NAME:return "tag_name"
        return selector
    
    @staticmethod
    def _convertElement(element:'Element'):
        e:WebElement = element._info['e']
        if not e:return element
        def get(e):
            parent_element:Element = element._info['parent_element'] 
            by = element._info['by'] 
            page = element._info['page'] 
            value = element._info['value'] 
            index = element._info['index'] 
            timeout = element._info['timeout'] 
            condition_wait = element._info['condition_wait'] 
            on_try = element._info['on_try'] 
            return e,parent_element,page,by,value,index,timeout,condition_wait,on_try
        if e.tag_name == 'iframe' or e.tag_name == 'frame' or e.tag_name == 'select':
            if e.tag_name == 'iframe' or e.tag_name == 'frame':
                return Frame(*get(e))
            return Select2(*get(e))
        return element
    @staticmethod
    def _check_in_shadow_root(parent_element,driver,by,value,isAll):
        try:
            if isinstance(parent_element,WebElement) and driver.execute_script('return arguments[0].shadowRoot != null;', parent_element):
                js_script = r'''function xpathToCss(xpath) {
                        // Replace the basic XPath expressions with CSS equivalents
                        return xpath
                            .replace(/\/\//g, ' ')
                            .replace(/\s+/g, ' ').trim() // Replace // with space
                            .replace(/\/([^\/\[\]]+)/g, ' $1') // Replace /node with space node
                            .replace(/\[@id="([^"]+)"\]/g, '#$1') // Replace @id="value" with #value
                            .replace(/\[@id = "([^"]+)"\]/g, '#$1') // Replace @id="value" with #value
                            .replace(/\[@class="([^"]+)"\]/g, '.$1') // Replace @class="value" with .value
                            .replace(/\[@class = "([^"]+)"\]/g, '.$1') // Replace @class="value" with .value
                            .replace(/\[(\d+)\]/g, ':nth-child($1)') // Handle nth-child
                            .trim(); // Trim whitespace
                    }
                    function getElement(host_element,locator,value,isAll = false){
                        const shadowRoot = host_element.shadowRoot;
                        function getE(is_exact) {
                            const all = [];
                            const elements = shadowRoot.querySelectorAll('*')
                            for (let i = 0; i < elements.length; i++) {
                                const el = elements[i];
                                const textNodes = Array.from(el.childNodes).filter(node => node.nodeType === Node.ELEMENT_NODE && node.textContent.trim() !== '');
                                const matchingTextNode = textNodes.reverse().find(node => 
                                    (is_exact ? node.textContent.trim() == value : node.textContent.includes(value))
                                );
                                if (matchingTextNode) {
                                    if (isAll) {
                                        all.push(matchingTextNode); 
                                    } else {
                                        return matchingTextNode; // Return the parent element of the last matching text node
                                    }
                                }
                            }
                            return all.length !== 0 ? all : null; 
                        }
                        let css_locator;
                        if (locator == 'id') css_locator = "#" + value;
                        else if (locator == 'css_selector' || locator == 'tag_name') css_locator = value;
                        else if (locator == 'class') css_locator = '.' + value;
                        else if (locator == 'xpath') css_locator = xpathToCss(value);
                        else if (locator == 'link_text') css_locator = getE(true);
                        else if (locator == 'partial_link_text') css_locator = getE(false);
                        else if (locator == 'name') css_locator = `[name ="${value}"]`;

                        if (css_locator instanceof Element || Array.isArray(css_locator)) return css_locator;
                        else if (css_locator == null) return null;

                        try {
                            console.log(css_locator);
                            
                            if (!isAll) {
                                return shadowRoot.querySelector(css_locator)
                            }
                            const elements = [] 
                            const matchedElements = shadowRoot.querySelectorAll(css_locator)
                            elements.push(...Array.from(matchedElements));
                            return elements
                        } catch (err) {
                            console.error(err);
                            return null;
                        }
                    }   
                    return getElement(arguments[0],arguments[1], arguments[2], arguments[3]);
                    '''

                if not isinstance(parent_element,WebElement):
                    parent_element = None
                # Execute the script
                #print(_ElementHandler.__getResverseSelector(by), value, isAll)
                element = driver.execute_script(js_script, parent_element, _ElementHandler.__getResverseSelector(by), value, isAll)
                return element 
             
        except Exception as e:
            print(e,"")
        
class Element:
    _EXPECT_ = False
    _FRAME_ON = False
    def __init__(self,e:WebElement,parent_element,page,by,value,index=-1,timeout=10,condition_wait=None,on_try=None) -> None:
        self._info = {"e":e,"parent_element":parent_element,"page":page,"by":by,"value":value,"index":index,
                               "timeout":timeout,"condition_wait":condition_wait,
                               "on_try":on_try}
    def _focus(self):
        self._info['page']._focus() 
    
    async def find_element(self,by:_BY,value:str,**args)-> Union['Element','Frame','Select2']:
        """
        Asynchronously finds a single element by the given selector.

        :param by: The strategy to locate the element (e.g., "id", "css_selector").
        :param value: The value of the selector to locate the element.
        :param args: Additional arguments for element handling .
        :return: An Element, Frame, or Select2 object.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':False})
        return await _ElementHandler._async_handler(self,args)
    async def find_elements(self,by:_BY,value:str,**args)->list[Union['Element','Frame','Select2']]:
        """
        Asynchronously finds multiple elements by the given selector.

        :param by: The strategy to locate elements (e.g., "id", "css_selector").
        :param value: The value of the selector to locate the elements.
        :param args: Additional arguments for element handling.
        :return: A list of Element, Frame, or Select2 objects.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':True})
        return await _ElementHandler._async_handler(self,args)
    def find_element_sync(self,by:_BY,value,**args)-> Union['Element','Frame','Select2']:
        """
        Synchronously finds a single element by the given selector.

        :param by: The strategy to locate the element (e.g., "id", "css_selector").
        :param value: The value of the selector to locate the element.
        :param args: Additional arguments for element handling.
        :return: An Element, Frame, or Select2 object.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':False})
        return _ElementHandler._sync_handler(self,args)
    def find_elements_sync(self,by:_BY,value,**args)->list[Union['Element','Frame','Select2']]:
        """
        Synchronously finds multiple elements by the given selector.

        :param by: The strategy to locate elements (e.g., "id", "css_selector").
        :param value: The value of the selector to locate the elements.
        :param args: Additional arguments for element handling.
        :return: A list of Element, Frame, or Select2 objects.
        """
        self._focus()
        by = _ElementHandler._getSelector(by)
        args.update({"by":by,"value":value,'isAll':True})
        return _ElementHandler._sync_handler(self,args) 
    def __update(self, callback,isRefresh=False,is_focus=True):
        def refresh():
            parent_element:Element = self._info['parent_element']
            by = self._info['by']
            value = self._info['value']
            index = self._info['index']
            
            if type(parent_element) == Select2:
                e:WebElement =  parent_element._getBy(by,index)
                if e:
                    self._info['e'] = e
                    return 
            if index == -1:
                self._info['e'] = (parent_element.find_element_sync(by,value))._info['e']
            else:
                elements = (parent_element.find_elements_sync(by,value))
                self._info['e'] = elements[index]._info['e']
        if is_focus:
            self._focus()
        try :
            if isRefresh:refresh()
            return callback()
        except:
            refresh()
            return callback()
    def wait_for(self,by:_BY,value:str,timeout=10)->'Expect':
        """
         Waits for a child element of the current element to be present on the page within the specified timeout. 

    Example usage:
        parent_element.wait_for('id', 'inp1', 5).has_attribute('display', 'block')

    Args:
        by (str): The type of locator to search by (e.g., 'id', 'name', 'css_selector', etc.).
        value (str): The value of the locator to identify the target element.
        timeout (int, optional): Maximum wait time in seconds. Defaults to 10.

    Returns:
        Expect: An Expect object, which allows chaining additional conditions like `has_attribute` or `to_be_present`.
        """
        isAsync = timeout >3
        if isAsync:return Expect(self.find_element(by,value),timeout)
        else:return Expect(lambda:self.find_element_sync(by,value),timeout)
    def is_at_bottom(self):
        """
        Checks if the element is scrolled to the bottom.

        :return: True if the element is at the bottom, False otherwise.
        """
        def callback():
            element = self._info['e']
            return self._info['page'].driver.execute_script("""
                return arguments[0].scrollTop + arguments[0].clientHeight >= arguments[0].scrollHeight;
            """, element)
        return self.__update(callback)
    def is_at_right(self):
        """
        Checks if the element is scrolled to the right edge.

        :return: True if the element is at the right edge, False otherwise.
        """
        def callback():
            element = self._info['e']
            return self._info['page'].driver.execute_script("""
                return arguments[0].scrollLeft + arguments[0].clientWidth >= arguments[0].scrollWidth;
            """, element)
        return self.__update(callback)
    def scroll_x_by(self,dx):
        """
        Scrolls the element horizontally by the given offset.

        :param dx: Horizontal scroll offset (in pixels).
        :return: The current element.
        """
        def callback():
            nonlocal dx 
            element = self._info['e']
            self._info['page'].driver.execute_script(f"arguments[0].scrollLeft += {dx}",element)
            return self 
        return self.__update(callback)
    def scroll_y_by(self,dy):
        """
        Scrolls the element vertically by the given offset.

        :param dy: Vertical scroll offset (in pixels).
        :return: The current element.
        """
        def callback():
            nonlocal dy
            element = self._info['e']
            self._info['page'].driver.execute_script(f"arguments[0].scrollTop += {dy}",element)
            return self 
        return self.__update(callback)
    def scroll_xy_by(self,dx,dy):
        """
        Scrolls the element both horizontally and vertically by the given offsets.

        :param dx: Horizontal scroll offset (in pixels).
        :param dy: Vertical scroll offset (in pixels).
        :return: The current element.
        """
        def callback():
            nonlocal dx,dy 
            element = self._info['e']
            self._info['page'].driver.execute_script(f"arguments[0].scrollLeft += {dx}; arguments[0].scrollTop += {dy};", element)
            return self 
        return self.__update(callback)
    def scrollToBottom(self):
        """
        Scrolls the element to the bottom.

        :return: The current element.
        """
        def callback():
            element = self._info['e']
            self._info['page'].driver.execute_script("""
                arguments[0].scrollTop = arguments[0].scrollHeight;
            """, element)
            return self 
        return self.__update(callback)
    def scroll_to_top(self):
        """
        Scrolls the given element to the top.
        :param element: The WebElement to scroll.
        """
        def callback():
            self._focus()
            element = self._info['e']
            self._info['page'].driver.execute_script("""
                arguments[0].scrollTop = 0;
            """, element)
            return self
        return self.__update(callback)
    def send_keys(self, *value: str) :
        """
        Sends the specified keys to the element.

        :param value: The keys to be sent.
        :return: The current element.
        """ 
        def callback():
            nonlocal value
            element = self._info['e']                 
            element.send_keys(*value)      
            return self   
        return self.__update(callback)                 
    def send_file(self, file_path):
        """
        Sends a file to the input element (used for file upload fields).

        :param file_path: The path of the file to be uploaded.
        :return: The current element.
        """
        def callback():
            nonlocal file_path
            self._focus()
            element = self._info['e']
            input_element = element
            driver = self._info['page'].driver

            # Enable the input if it's disabled
            driver.execute_script("arguments[0].removeAttribute('disabled');", input_element)

            # If the input is hidden, make it visible by changing display property
            original_display = driver.execute_script("return arguments[0].style.display;", input_element)
            if original_display == 'none':
                driver.execute_script("arguments[0].style.display = 'block';", input_element)

            # If the input is not visible, set visibility to visible
            original_visibility = driver.execute_script("return arguments[0].style.visibility;", input_element)
            if original_visibility == 'hidden':
                driver.execute_script("arguments[0].style.visibility = 'visible';", input_element)

            # Send the file
            input_element.send_keys(file_path)

            # Restore the original state (if needed)
            if original_display == 'none':
                driver.execute_script("arguments[0].style.display = 'none';", input_element)
            if original_visibility == 'hidden':
                driver.execute_script("arguments[0].style.visibility = 'hidden';", input_element)
            return self
        return self.__update(callback)
    def dragTo(self,element:'Element'):
        """
        Drags the current element to the specified target element.

        :param element: The target element to drag to.
        :return: The current element.
        """
        def callback():
            nonlocal element
            element0 = self._info['e']
            driver = self._info['page'].driver
            actions = ActionChains(driver)
            #element = _ElementHandler._refresh(element)
            actions.drag_and_drop(element0,element._info['e']).perform()
            return self 
        return self.__update(callback)
    def drag_and_drop_by_offset(self,dx,dy):
        """
        Drags the element by the specified horizontal and vertical offsets.

        :param dx: Horizontal drag offset (in pixels).
        :param dy: Vertical drag offset (in pixels).
        :return: The current element.
        """
        def callback():
            nonlocal dx,dy 
            element = self._info['e']
            driver = self._info['page'].driver
            actions = ActionChains(driver)
            actions.drag_and_drop_by_offset(element,dx,dy).perform()
            return self 
        return self.__update(callback)
    def double_click(self):
        """
        Performs a double-click action on the element.

        :return: The current element.
        """
        def callback():
            element = self._info['e']
            driver = self._info['page'].driver
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            return self 
        return self.__update(callback)
     
    def check(self):
        """
        Checks or toggles the checkbox or radio button element if it is not already checked.

        :return: The current element.
        """
        def callback():
            element = self._info['e']
            # Ensure the element is a checkbox or radio button
            if element.tag_name not in ['input'] or element.get_attribute('type') not in ['checkbox', 'radio']:
                raise ValueError("The provided WebElement is not a checkbox or radio button.")
            
            # Check if the element is already selected
            if not element.is_selected():
                element.click()  # Click to check the checkbox or select the radio button
            return self 
        return self.__update(callback)
    def uncheck(self):
        """
            Uncheck a checkbox if it is already checked. Radio buttons are typically not unchecked.
            
            :param element: The WebElement to uncheck.
            :raises ValueError: If the element is not a checkbox.
        """
        def callback():
            
            element = self._info['e']
            # Ensure the element is a checkbox
            if element.tag_name != 'input' or element.get_attribute('type') != 'checkbox' or element.get_attribute('type')!="radio":
                raise ValueError("The provided WebElement is not a checkbox.")
            
            # Check if the element is already selected
            if element.is_selected():
                element.click()  # Click to uncheck the checkbox
            return self 
        return self.__update(callback)
    def click(self):
        """
        Clicks the element.

        :return: The current element.
        """
        def callback(): 
            element = self._info['e']
            element.click()
            return self
        return self.__update(callback)
    def clear(self):
        """
        Clears the content of an input or textarea element.

        :return: The current element.
        """
        def callback(): 
            element = self._info['e']
            element.clear()
            return self 
        return self.__update(callback)
    def value_of_css_property(self, property_name) -> str:
        """
        Retrieves the value of a specific CSS property of the element.

        :param property_name: The name of the CSS property.
        :return: The value of the CSS property.
        """
        def callback():
            nonlocal property_name
            element = self._info['e']
            return element.value_of_css_property(property_name)
        return self.__update(callback)    
    def is_displayed(self) -> bool:
        """
        Checks if the element is currently displayed.

        :return: True if the element is displayed, False otherwise.
        """
        def callback():
            element = self._info['e']
            return element.is_displayed()
        return self.__update(callback)
    def is_enabled(self) -> bool:
        """
        Checks if the element is currently enabled.

        :return: True if the element is enabled, False otherwise.
        """
        def callback():
            element = self._info['e']
            return element.is_enabled()
        return self.__update(callback)
    def is_selected(self) -> bool:
        """
        Checks if the element (checkbox or radio button) is selected.

        :return: True if the element is selected, False otherwise.
        """
        def callback():
            element = self._info['e']
            return element.is_selected()
        return self.__update(callback)
    def get_attribute(self, name) -> str | None:
        """
        Retrieves the value of a specified attribute of the element.

        :param name: The name of the attribute.
        :return: The value of the attribute, or None if not present.
        """
        def callback():
            nonlocal name
            self._focus()
            element = self._info['e']
            return element.get_attribute(name)
        return self.__update(callback)
    def get_dom_attribute(self, name) -> str:
        """
        Retrieves the value of a DOM attribute.

        :param name: The name of the DOM attribute.
        :return: The value of the DOM attribute.
        """
        def callback():
            nonlocal name
            element = self._info['e']
            return element.get_dom_attribute(name)
        return self.__update(callback) 
    def get_property(self, name) -> str | None:
        """
        Retrieves the value of a specified property of the element.

        :param name: The name of the property.
        :return: The value of the property.
        """
        def callback():
            nonlocal name
            element = self._info['e']
            return element.get_property(name)
        return self.__update(callback)
    def screenshot(self, filename) -> bool:
        """
        Takes a screenshot of the element and saves it to the specified file.

        :param filename: The path where the screenshot will be saved.
        :return: True if the screenshot is saved successfully, False otherwise.
        """
        def callback():
            nonlocal filename
            element = self._info['e']
            element.screenshot(filename)
            return self 
        return self.__update(callback)
    def submit(self):
        """
        Submits a form element.

        :return: The current element.
        """
        def callback():
            element = self._info['e']
            element.submit()
            return self 
        return self.__update(callback)
    def press(self,*keys:Keys,delay_in_miliseconds=0):
        """
        Sends one or more key presses to the element.

        :param keys: The keys to be pressed.
        :param delay_in_milliseconds: Delay between key presses (in milliseconds).
        :return: The current element.
        """
        def callback():
            nonlocal keys,delay_in_miliseconds
            element = self._info['e']
            for key in keys:
                element.send_keys(key)
                if delay_in_miliseconds:
                    sleep(delay_in_miliseconds/1000)
            return self 
        return self.__update(callback)
    @property
    def text(self)->str:
        """
        Retrieves the visible text content of the element.

        :return: The text content of the element.
        """
        def callback():
            element = self._info['e']
            return element.text
        return self.__update(callback)
    @property
    def location(self)->tuple:
        """
        Retrieves the X and Y coordinates of the element's position.

        :return: A tuple containing the X and Y coordinates.
        """
        def callback():
            location = self._info['e'].location
            return (location['x'],location['y'])
        return self.__update(callback)
    @property 
    def accessible_name(self)->str:
        """
        Retrieves the accessible name of the element.

        :return: The accessible name of the element.
        """
        def callback():
            return self._info['e'].accessible_name
        return self.__update(callback)
    @property     
    def aria_role(self)->str:
        """
        Retrieves the ARIA role of the element.

        :return: The ARIA role of the element.
        """
        def callback():
            return self._info['e'].aria_role
        return self.__update(callback)
    @property 
    def id(self)->str:
        def callback():
            return self._info['e'].id
        return self.__update(callback)
    @property 
    def location_once_scrolled_into_view(self)->tuple:
        """
        Retrieves the X and Y coordinates of the element once it is scrolled into view.

        :return: A tuple containing the X and Y coordinates, representing the coordinates of the element.
        """
        WebElement().location_once_scrolled_into_view
        def callback():
            loc = self._info['e'].location_once_scrolled_into_view
            return (loc['x'],loc['y'])
        return self.__update(callback)
    @property 
    def parent(self)->'Element':
        """
        Retrieves the parent element of the current element.

        :return: The parent Element.
        """
        def callback():
            return self._info['paren_element'] 
        return self.__update(callback)
    @property 
    def screenshot_as_base64(self)->str:
        """
        Takes a screenshot of the element and returns it as a base64-encoded string.

        :return: A base64-encoded string representing the screenshot of the element.
        """
        def callback():
            return self._info['e'].screenshot_as_base64
        return self.__update(callback)
    @property 
    def screenshot_as_png(self)->bytes:
        """
        Takes a screenshot of the element and returns it as a PNG image in byte format.

        :return: A byte object representing the screenshot of the element in PNG format.
        """
        def callback():
            return self._info['e'].screenshot_as_png
        return self.__update(callback)
    @property 
    def shadow_root(self)->ShadowRoot:
        """
        Retrieves the shadow root of the element if it exists.

        :return: A ShadowRoot object if the element has a shadow DOM, otherwise None.
        :raises NoSuchElementException: If the element does not have a shadow root.
        """
        def callback():
            return self._info['e'].shadow_root
        return self.__update(callback)
    @property 
    def size(self)->tuple:
        """
        Retrieves the width and height of the element.

        :return: A dictionary with the keys 'width' and 'height', representing the size of the element.
        """
        def callback():
            size = self._info['e'].size
            return (size['width'],size['height'])
        return self.__update(callback)
    
class Frame(Element):
    ACTUAL_FRAME_ID = -1
    ID_INC = 0
    def __init__(self, e , parent_element, page, by, value, index=-1,timeout=10,condition_wait=None,on_try=None) -> None:
        super().__init__(e, parent_element, page, by, value, index, timeout, condition_wait, on_try) 
        self.driver = page.driver
        page.iframes.append(self)
        self.index_id = Frame.ID_INC
        Frame.ID_INC += 1
        self.isActive = False
    def _bind(self):
        def callback():
            if(type(self._info['parent_element']) == Frame):
                self._info['parent_element']._bind()
            else:
                self._info['page']._bind()
            self.driver.switch_to.frame(self._info['e'])
            self.isActive = True
        self._Element__update(callback,False,False)
    def _reset(self):
        Frame.ACTUAL_FRAME_ID = -1
    def _focus(self):
        Element._FRAME_ON = True
        if self.index_id != Frame.ACTUAL_FRAME_ID:
            Frame.ACTUAL_FRAME_ID = self.index_id
            self._bind()

class Select2(Element):
    def __init__(self, e: WebElement, parent_element, page, by, value, index=-1, timeout=10, condition_wait=None, on_try=None) -> None:
        super().__init__(e, parent_element, page, by, value, index, timeout, condition_wait, on_try)
        self.select = Select(e)
    def select_by_index(self,index):
        """
        Select an option by its index in the dropdown.

        Args:
            index (int): The index of the option to select (0-based).
        """
        def callback():
            self.select.select_by_index(index)
        self._Element__update(callback)
    def select_by_value(self,value):
        """
        Select an option by its value attribute.

        Args:
            value (str): The value attribute of the option to select.
        """
        def callback():
            self.select.select_by_value(value)
        self._Element__update(callback)
    def select_by_visible_text(self,text):
        """
        Select an option by the visible text of the option.

        Args:
            text (str): The visible text of the option to select.
        """
        def callback():
            self.select.select_by_visible_text(text)
        self._Element__update(callback)
    def deselect_all(self):
        """
        Deselect all selected options in a multi-select dropdown.
        """
        def callback():
            self.select.deselect_all()
        self._Element__update(callback)
    def deselect_by_index(self,index):
        """
        Deselect an option by its index in the dropdown.

        Args:
            index (int): The index of the option to deselect (0-based).
        """
        def callback():
            self.select.deselect_by_index(index)
        self._Element__update(callback)
    def deselect_by_value(self,value):
        """
        Deselect an option by its value attribute.

        Args:
            value (str): The value attribute of the option to deselect.
        """
        def callback():
            self.select.deselect_by_value(value)
        self._Element__update(callback)
    def deselect_by_visible_text(self,text):
        """
        Deselect an option by the visible text of the option.

        Args:
            text (str): The visible text of the option to deselect.
        """
        def callback():
            self.select.deselect_by_visible_text(text)
        self._Element__update(callback)
    def _getBy(self,by,index):
        if by == 'all_selected_options':
            return self.select.all_selected_options[index]
        elif by == 'first_selected_option':
            return self.select.first_selected_option 
        elif by == 'options':
            return  self.select.options[index]
        return None 
    @property
    def all_selected_options(self):
        """
        Retrieve all selected options in the dropdown.

        Returns:
            list[Element]: A list of Element objects for each selected option.
        """
        def callback():
            return [Element(e,self,self._info['page'],'all_selected_options',None,i) for i,e in enumerate(self.select.all_selected_options)]
        return self._Element__update(callback)
    @property
    def first_selected_option(self):
        """
        Retrieve the first selected option in the dropdown.

        Returns:
            Element: The first selected option as an Element object.
        """
        def callback():
            return Element(self.select.first_selected_option,self,self._info['page'],'first_selected_option',None)
        return self._Element__update(callback)
    @property
    def options(self):
        """
        Retrieve all available options in the dropdown.

        Returns:
            list[Element]: A list of Element objects for each option in the dropdown.
        """
        def callback():
            return [Element(e,self,self._info['page'],'options',None,i) for i,e in enumerate(self.select.options)]
        return self._Element__update(callback)
    @property
    def is_multiple(self):
        """
        Check if the dropdown allows selecting multiple options.

        Returns:
            bool: True if the dropdown allows multiple selections, False otherwise.
        """
        return self.select.is_multiple
    

class Expect:
    class __INIT_EXPECT:
        def __init__(self,handler) -> None:
            self.handler = handler
        def __setInfoAndGet(self,_predict,timeout,on_try):
            arg = {'condition_wait':_predict,
                'timeout':timeout,
                'on_try':on_try}
            info = self.element._info
            info['timeout'] = timeout
            info['condition_wait'] = _predict
            info['on_try'] = on_try
            return info,arg
        async def _finaly(self,_predict,timeout,on_try,isAll=False):
            info,arg = self.__setInfoAndGet(_predict,timeout,on_try)
            parent_element:Element = info["parent_element"]
            if not isAll:
                return await parent_element.find_element(info['by'],
                                                        info['value'],**arg)
            return await parent_element.find_elements(info['by'],
                                                    info['value'],**arg)
        async def _initExpect(self):
            Element._EXPECT_ = True
            try:self.element = await self.handler
            except:self.element = self.handler()
            Element._EXPECT_ = False
            info = self.element._info
            p_e:Element = info["parent_element"]
            try:p_e = p_e._info['e']
            except:p_e = p_e.driver
            return info ,p_e
        def _ps(self,info,p_e:WebElement,timeout,isAll=False):
            def _predict():
                nonlocal p_e
                try:
                    if not isAll:
                        e = p_e.find_element(info['by'],info['value'])
                        info['e'] = e
                        return self.element
                    else:
                        elements:list[WebElement] = p_e.find_elements(info['by'],info['value'])
                        p_e = info['parent_element']
                        return [Element(e,p_e,info['page'],info['by'],
                                        info['value'],i,info['timeout'],
                                        info["condition_wait"],
                                        info['on_try']) for i,e in enumerate(elements)]
                except:
                    by,value=info['by'],info['value']
                    raise TimeoutError(f"Operation timed out after '{timeout} seconds' while waiting to find the element (by='{by}',value='{value}')")
            return _predict
        def _att(self,info,p_e:WebElement,timeout,attr_name):
            def _predict():
                self._ps(info,p_e,timeout)()
                e:WebElement = info['e']
                if e.get_attribute(attr_name):return self.element
                raise TimeoutError(f"Operation timed out after '{timeout} seconds' while waiting for attribute '{attr_name}' to be found.")
            return _predict
    def __init__(self, handler: Union[Callable[[], None], Coroutine[Any, Any, None]],timeout=10) -> None:
        if not isinstance(handler, (Callable, Coroutine)):
            raise TypeError("handler must be a Callable or Coroutine")
        self.__Exp = Expect.__INIT_EXPECT(handler)
        self.timeout = timeout 
    async def to_be_present(self,on_try=None)->Element:
        """
        Waits for the element to be present in the DOM.
        
        Args:
            on_try (callable, optional): Optional retry function.
        
        Returns:
            Element: The web element if present, otherwise raises TimeoutError.
        """
        exp = self.__Exp
        info,p_e = await exp._initExpect()
        _predict = exp._ps(info,p_e)
        return await exp._finaly(_predict,self.timeout,on_try)
    async def has_attribute(self,attr_name,on_try=None)->Element:
        """
        Waits for the element to have the specified attribute.
        
        Args:
            attr_name (str): The name of the attribute to check for.
            on_try (callable, optional): Optional retry function.
        
        Returns:
            Element: The web element if the attribute is present, otherwise raises TimeoutError.
        """
        exp = self.__Exp
        info ,p_e = await exp._initExpect()
        _predict = exp._att(info,p_e,self.timeout,attr_name)
        return await exp._finaly(_predict,self.timeout,on_try)
    async def attribute_has_value(self,attr_name,value,on_try=None)->Element:
        """
        Waits for the element's specified attribute to have a particular value.
        
        Args:
            attr_name (str): The name of the attribute to check.
            value (str): The expected value of the attribute.
            on_try (callable, optional): Optional retry function.
        
        Returns:
            Element: The web element if the attribute has the expected value, otherwise raises TimeoutError.
        """
        exp = self.__Exp
        info ,p_e = await exp._initExpect()
        def _predict():
            exp._att(info,p_e,self.timeout,attr_name)() 
            e:WebElement = info['e']
            if e.get_attribute(attr_name) == value:return exp.element
            raise TimeoutError(f"Operation timed out after '{self.timeout} seconds' while waiting for attribute '{attr_name}' has value = '{value}'")
        return await exp._finaly(_predict,self.timeout,on_try)
    async def has_text_exact_match(self,text:str,is_case_sensitive=True,on_try=None)->Element:
        """
        Waits for the element to have an exact text match.
        
        Args:
            text (str): The expected text content of the element.
            is_case_sensitive (bool, optional): Whether the text comparison should be case-sensitive, default is True.
            on_try (callable, optional): Optional retry function.
        
        Returns:
            Element: The web element if the text matches, otherwise raises TimeoutError.
        """
        exp = self.__Exp
        info, p_e = await exp._initExpect()
        def _predict():
            exp._ps(info,p_e,self.timeout)()
            e:WebElement = info['e']
            check = text.strip() == e.text.strip() or \
                not is_case_sensitive and text.strip().lower() == e.text.strip().lower()
            if check:return exp.element
            raise TimeoutError(f"Operation timed out after '{self.timeout} seconds' while waiting for exact text '{text}'.") 
        return await exp._finaly(_predict,self.timeout,on_try)
    async def contains_sub_text(self,text:str,is_case_sensitive=True,on_try=None):
        """
        Waits for the element to contain the specified subtext.
        
        Args:
            text (str): The expected subtext within the element's content.
            is_case_sensitive (bool, optional): Whether the text comparison should be case-sensitive, default is True.
            on_try (callable, optional): Optional retry function.
        
        Returns:
            Element: The web element if the subtext is found, otherwise raises TimeoutError.
        """
        exp = self.__Exp
        info ,p_e = await exp._initExpect()
        def _predict():
            exp._ps(info,p_e,self.timeout)()
            e:WebElement = info['e']
            check = text.strip() in e.text.strip() or \
                    not is_case_sensitive and text.strip().lower() in e.text.strip().lower()
            if check:return exp.element
            raise TimeoutError(f"TimeoutError:Operation timed out after '{self.timeout} seconds' while waiting for subtext '{text}' in the element.") 
        return await exp._finaly(_predict,self.timeout,on_try)
    async def all_to_be_present(self,on_try=None)->list[Element | Frame | Select2]:
        """
        Waits for all elements matching the criteria to be present in the DOM.
        
        Args:
            on_try (callable, optional): Optional retry function.
        
        Returns:
            list[Element]: A list of elements if found, otherwise raises TimeoutError.
        """
        exp = self.__Exp 
        info, p_e = await exp._initExpect()
        _predict = exp._ps(info,p_e,self.timeout,True)
        return await exp._finaly(_predict,self.timeout,on_try,True)     
   