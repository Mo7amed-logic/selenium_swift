from selenium_swift.browser import *
import asyncio

class MyBrowser(ChromeBrowser):
    def __init__(self):
        super().__init__(ChromeOption(),ChromeService())

    async def tab_drag_drop(self):
        page = await self.get('https://the-internet.herokuapp.com/dropdown')
        select_element = await page.find_element('id','dropdown')
        select_element.select_by_value('1')
        await page.sleep(1)
        select_element.select_by_value('2')
        await page.sleep(1)
        select_element.select_by_visible_text('Option 1')
        await page.sleep(1)

async def main():
    await BrowserManager.startBrowsers([MyBrowser()])

if __name__ == '__main__':
    asyncio.run(main())