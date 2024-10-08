from selenium_swift.BrowserManager import *


class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #Multiple Windows
        page = await self.get('https://the-internet.herokuapp.com/windows')
        link_element = await page.find_element('css_selector',"div#content a")
        link_element.click()
        page2 = page.focus_to_new_page()
        print(page2.driver.page_source)
        await page2.sleep(2)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])