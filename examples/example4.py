from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #dropdown
        page = await self.get('https://the-internet.herokuapp.com/dropdown') 
        select = await page.find_element('id','dropdown')
        select.select_by_value("1")
        await page.sleep(1)
        select.select_by_visible_text('Option 2')
        await page.sleep(1)
        select.select_by_index(1)
        await page.sleep(1)
        


if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])