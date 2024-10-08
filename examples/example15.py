from selenium_swift.BrowserManager import *


class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #Key Presses
        page = await self.get('https://the-internet.herokuapp.com/key_presses')
        input_element = await page.find_element('id',"target")
        input_element.press('h','e','l','l','o',' ','w','o','r','l','d',delay_in_miliseconds=200)
         
        
        await page.sleep(2)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])