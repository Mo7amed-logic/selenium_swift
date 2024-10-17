from selenium_swift.browser import *
import asyncio

class MyBrowser(ChromeBrowser):
    def __init__(self):
        super().__init__(ChromeOption(),ChromeService())

    async def tab_drag_drop(self):
        page = await self.get('https://the-internet.herokuapp.com/drag_and_drop')
        element1 = await page.find_element('css_selector','#column-b')
        element2 = await page.find_element('css_selector',"#column-a")
        element1.dragTo(element2)
        await page.sleep(2)
        element2.dragTo(element1)

async def main():
    await BrowserManager.startBrowsers([MyBrowser()])

if __name__ == '__main__':
    asyncio.run(main())