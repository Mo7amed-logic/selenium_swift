from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #dynamic_controls
        page = await self.get('https://the-internet.herokuapp.com/dynamic_controls') 
        button_add_remove = await page.find_element('css_selector',"#checkbox-example button")
        button_add_remove.click()
        while button_add_remove.text == "Remove":
            print('please wait ....')
            await page.sleep(1)
        print('removed successfuly...')
        # enable <input type="text">    
        button_enable = await page.find_element('css_selector','#input-example button')
        button_enable.click()
        while button_enable.text == 'Enable':
            print('please wait ...')
            await page.sleep(1)
        print('input enabled successfuly...')
        input_element = await page.find_element('css_selector',"input[type='text']")
        input_element.send_keys('Hello world!!!')
        await page.sleep(2)
         

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])