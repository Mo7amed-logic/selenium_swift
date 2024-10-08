from selenium_swift.BrowserManager import *


class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #Shadow - root
        page = await self.get('https://the-internet.herokuapp.com/shadowdom')
        shadow_element = await page.find_element('css_selector','my-paragraph:nth-of-type(1)')
        shadow_element2 = await page.find_element('css_selector','my-paragraph:nth-of-type(2)')
        print(shadow_element.text)
        print(shadow_element2.text)
        await page.sleep(3)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])