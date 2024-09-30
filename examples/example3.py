from selenium_swift.browser import *


class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #DRAG AND DROP
        page = await self.get('https://the-internet.herokuapp.com/drag_and_drop') 
        element1 = await page.find_element('css_selector','#column-a')
        element2 = await page.find_element('css_selector','#column-b')
        element1.dragTo(element2)
        await page.sleep(1)
        element2.dragTo(element1)
        await page.sleep(1)


if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])