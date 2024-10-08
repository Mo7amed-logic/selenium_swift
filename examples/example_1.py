from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        option = ChromeOption()
        service = ChromeService()
        super().__init__(option, service)
    async def tab_1(self):
        url = "https://the-internet.herokuapp.com/add_remove_elements/"
        page = await self.get(url)
        #***** button for adding element 
        button = await page.find_element('tag_name','button')
        button.click()
        await page.sleep(1)
        button.click()
        await page.sleep(1)
        button.click()
        await page.sleep(1)
        button.click()
        #****** button for delete element
        button2 = await page.find_element('class','added-manually')
        button2.click()
        await page.sleep(1)
        button2.click()
        await page.sleep(1)
        button2.click()
    async def tab_2(self):
        page = await PageEvent('https://the-internet.herokuapp.com/challenging_dom').open()
        rows = await page.find_elements('css_selector','table tr')
        for r in rows:
            print(r.text)

        

if __name__ == '__main__':
    BrowserManager.startBrowserManagers([MyBrowserManager()])

